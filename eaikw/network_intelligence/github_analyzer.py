"""
GitHub Portfolio Analyzer

Extracts comprehensive statistics and marketing assets from your GitHub profile.
"""
import os
import re
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import Counter
import json

from github import Github, GithubException
from github.Repository import Repository as GitHubRepo
from dotenv import load_dotenv

from models import GitHubRepository, GitHubPortfolioStats
from database import NetworkDatabase


class GitHubAnalyzer:
    """Analyze GitHub profile and repositories"""
    
    def __init__(self, username: str, token: Optional[str] = None):
        load_dotenv()
        
        self.username = username
        self.token = token or os.getenv('GITHUB_TOKEN')
        
        if not self.token:
            raise ValueError(
                "GitHub token required. Set GITHUB_TOKEN in .env or pass as parameter"
            )
        
        self.github = Github(self.token)
        self.user = self.github.get_user(username)
        self.db = NetworkDatabase()
        
        print(f"✓ Connected to GitHub as: {self.user.name or self.user.login}")
        print(f"  Rate limit: {self.github.get_rate_limit().core.remaining}/5000")
    
    def fetch_all_repos(self, include_private: bool = False) -> List[GitHubRepository]:
        """Fetch all repositories"""
        print(f"\n📥 Fetching repositories for {self.username}...")
        
        repos = []
        gh_repos = self.user.get_repos()
        
        for gh_repo in gh_repos:
            if gh_repo.private and not include_private:
                continue
            
            repo = self._convert_repo(gh_repo)
            repos.append(repo)
            
            # Save to database
            self.db.save_repository(repo)
        
        print(f"✓ Fetched {len(repos)} repositories")
        return repos
    
    def analyze_repository(self, gh_repo: GitHubRepo) -> GitHubRepository:
        """Deep analysis of single repository"""
        repo = self._convert_repo(gh_repo)
        
        # Analyze README
        try:
            readme = gh_repo.get_readme()
            repo.readme_content = readme.decoded_content.decode('utf-8')
        except GithubException:
            pass
        
        # Check for tests
        try:
            contents = gh_repo.get_contents("")
            file_names = [f.name.lower() for f in contents]
            
            repo.has_tests = any(
                'test' in name or name == 'tests' or name == '__tests__'
                for name in file_names
            )
            
            repo.has_docker = any(
                name in ['dockerfile', 'docker-compose.yml', 'docker-compose.yaml']
                for name in file_names
            )
            
            # Check for CI
            try:
                gh_repo.get_contents(".github/workflows")
                repo.has_ci = True
            except GithubException:
                pass
            
            # Check for other CI configs
            if not repo.has_ci:
                ci_files = [
                    '.travis.yml', '.circleci', 'azure-pipelines.yml',
                    '.gitlab-ci.yml', 'jenkinsfile'
                ]
                repo.has_ci = any(name in file_names for name in ci_files)
        
        except GithubException:
            pass
        
        # Get language breakdown
        try:
            languages = gh_repo.get_languages()
            repo.languages = languages
        except GithubException:
            pass
        
        return repo
    
    def _convert_repo(self, gh_repo: GitHubRepo) -> GitHubRepository:
        """Convert PyGithub Repository to our model"""
        # Get license
        license_name = None
        try:
            if gh_repo.license:
                license_name = gh_repo.license.name
        except GithubException:
            pass
        
        return GitHubRepository(
            name=gh_repo.name,
            full_name=gh_repo.full_name,
            description=gh_repo.description,
            html_url=gh_repo.html_url,
            homepage=gh_repo.homepage,
            stargazers_count=gh_repo.stargazers_count,
            forks_count=gh_repo.forks_count,
            watchers_count=gh_repo.watchers_count,
            open_issues_count=gh_repo.open_issues_count,
            language=gh_repo.language,
            topics=gh_repo.get_topics() if gh_repo else [],
            created_at=gh_repo.created_at,
            updated_at=gh_repo.updated_at,
            pushed_at=gh_repo.pushed_at,
            is_fork=gh_repo.fork,
            is_archived=gh_repo.archived,
            is_private=gh_repo.private,
            has_issues=gh_repo.has_issues,
            has_wiki=gh_repo.has_wiki,
            has_pages=gh_repo.has_pages,
            license=license_name
        )
    
    def get_full_stats(self, deep_analysis: bool = True) -> GitHubPortfolioStats:
        """Get comprehensive portfolio statistics"""
        print("\n📊 Analyzing GitHub portfolio...")
        
        # Fetch all repos
        all_repos = self.db.get_all_repositories()
        
        if not all_repos or deep_analysis:
            print("  Fetching latest data from GitHub...")
            all_repos = self.fetch_all_repos()
            
            if deep_analysis:
                print("  Performing deep analysis (this may take a while)...")
                gh_repos = list(self.user.get_repos())
                for i, gh_repo in enumerate(gh_repos, 1):
                    if gh_repo.private:
                        continue
                    
                    print(f"  [{i}/{len(gh_repos)}] Analyzing {gh_repo.name}...")
                    repo = self.analyze_repository(gh_repo)
                    self.db.save_repository(repo)
                    all_repos[i-1] = repo
        
        # Filter out forks and archived
        significant_repos = [
            r for r in all_repos
            if not r.is_fork and not r.is_archived
        ]
        
        # Calculate stats
        total_stars = sum(r.stargazers_count for r in all_repos)
        total_forks = sum(r.forks_count for r in all_repos)
        total_watchers = sum(r.watchers_count for r in all_repos)
        
        # Language stats
        language_bytes = Counter()
        for repo in all_repos:
            for lang, bytes_count in repo.languages.items():
                language_bytes[lang] += bytes_count
        
        # Topics
        all_topics = []
        for repo in all_repos:
            all_topics.extend(repo.topics)
        top_topics = Counter(all_topics).most_common(20)
        
        # Quality metrics
        repos_with_tests = sum(1 for r in significant_repos if r.has_tests)
        repos_with_ci = sum(1 for r in significant_repos if r.has_ci)
        repos_with_docker = sum(1 for r in significant_repos if r.has_docker)
        repos_with_license = sum(1 for r in significant_repos if r.license)
        repos_with_readme = sum(1 for r in significant_repos if r.readme_content)
        
        # Top repos
        top_by_stars = sorted(
            significant_repos,
            key=lambda r: r.stargazers_count,
            reverse=True
        )[:10]
        
        # Recent repos
        recent = sorted(
            significant_repos,
            key=lambda r: r.updated_at or datetime.min,
            reverse=True
        )[:10]
        
        # Organizations
        try:
            orgs = [org.login for org in self.user.get_orgs()]
        except GithubException:
            orgs = []
        
        # Generate showcase projects
        showcase_projects = self._generate_showcase_projects(top_by_stars)
        
        # Generate tech stack summary
        tech_stack = self._generate_tech_stack_summary(all_repos, language_bytes)
        
        stats = GitHubPortfolioStats(
            username=self.username,
            total_repos=len(all_repos),
            public_repos=len([r for r in all_repos if not r.is_private]),
            private_repos=len([r for r in all_repos if r.is_private]),
            total_stars=total_stars,
            total_forks=total_forks,
            total_watchers=total_watchers,
            total_commits=0,  # Would need additional API calls
            repos_contributed_to=0,  # Would need additional API calls
            top_repositories=top_by_stars,
            recent_repositories=recent,
            languages_used=dict(language_bytes.most_common()),
            top_topics=top_topics,
            repos_with_tests=repos_with_tests,
            repos_with_ci=repos_with_ci,
            repos_with_docker=repos_with_docker,
            repos_with_license=repos_with_license,
            repos_with_readme=repos_with_readme,
            organizations=orgs,
            top_contributors=[],  # Would need additional API calls
            showcase_projects=showcase_projects,
            tech_stack_summary=tech_stack
        )
        
        self._print_stats(stats)
        return stats
    
    def _generate_showcase_projects(self, top_repos: List[GitHubRepository]) -> List[Dict[str, Any]]:
        """Generate marketing-ready project showcases"""
        showcases = []
        
        for repo in top_repos[:5]:  # Top 5 projects
            # Extract key features from README
            features = []
            if repo.readme_content:
                # Look for bullet points
                lines = repo.readme_content.split('\n')
                for line in lines:
                    if line.strip().startswith(('- ', '* ', '• ')):
                        feature = line.strip()[2:].strip()
                        if len(feature) < 100:  # Reasonable length
                            features.append(feature)
                    if len(features) >= 5:
                        break
            
            # Detect tech stack
            tech_stack = []
            if repo.languages:
                tech_stack = list(repo.languages.keys())[:5]
            tech_stack.extend(repo.topics[:5])
            
            showcase = {
                'name': repo.name,
                'title': repo.name.replace('-', ' ').replace('_', ' ').title(),
                'description': repo.description or f"A {repo.language} project",
                'url': repo.html_url,
                'demo_url': repo.homepage,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'language': repo.language,
                'tech_stack': tech_stack,
                'features': features,
                'last_updated': repo.updated_at.strftime('%B %Y') if repo.updated_at else 'Unknown',
                'has_tests': repo.has_tests,
                'has_ci': repo.has_ci,
                'has_docker': repo.has_docker
            }
            
            showcases.append(showcase)
        
        return showcases
    
    def _generate_tech_stack_summary(
        self,
        repos: List[GitHubRepository],
        language_bytes: Counter
    ) -> Dict[str, Any]:
        """Generate tech stack summary for marketing"""
        # Primary languages
        total_bytes = sum(language_bytes.values())
        primary_languages = []
        for lang, bytes_count in language_bytes.most_common(10):
            percentage = (bytes_count / total_bytes) * 100
            primary_languages.append({
                'name': lang,
                'bytes': bytes_count,
                'percentage': round(percentage, 1)
            })
        
        # Detect frameworks
        frameworks = set()
        databases = set()
        tools = set()
        
        framework_patterns = {
            'fastapi': 'FastAPI',
            'flask': 'Flask',
            'django': 'Django',
            'react': 'React',
            'vue': 'Vue.js',
            'angular': 'Angular',
            'next': 'Next.js',
            'express': 'Express.js',
            'langchain': 'LangChain',
            'langgraph': 'LangGraph',
        }
        
        database_patterns = {
            'postgres': 'PostgreSQL',
            'mysql': 'MySQL',
            'mongodb': 'MongoDB',
            'redis': 'Redis',
            'neo4j': 'Neo4j',
            'qdrant': 'Qdrant',
            'pinecone': 'Pinecone',
        }
        
        tool_patterns = {
            'docker': 'Docker',
            'kubernetes': 'Kubernetes',
            'terraform': 'Terraform',
            'aws': 'AWS',
            'azure': 'Azure',
            'gcp': 'Google Cloud',
            'pytest': 'pytest',
            'jest': 'Jest',
        }
        
        for repo in repos:
            # Check README
            if repo.readme_content:
                content_lower = repo.readme_content.lower()
                
                for pattern, name in framework_patterns.items():
                    if pattern in content_lower:
                        frameworks.add(name)
                
                for pattern, name in database_patterns.items():
                    if pattern in content_lower:
                        databases.add(name)
                
                for pattern, name in tool_patterns.items():
                    if pattern in content_lower:
                        tools.add(name)
            
            # Check topics
            for topic in repo.topics:
                topic_lower = topic.lower()
                for pattern, name in framework_patterns.items():
                    if pattern in topic_lower:
                        frameworks.add(name)
        
        return {
            'primary_languages': primary_languages,
            'frameworks': sorted(frameworks),
            'databases': sorted(databases),
            'tools': sorted(tools)
        }
    
    def _print_stats(self, stats: GitHubPortfolioStats):
        """Print formatted statistics"""
        print(f"\n{'='*60}")
        print(f"GITHUB PORTFOLIO ANALYSIS: {stats.username}")
        print(f"{'='*60}\n")
        
        print(f"📦 Repositories: {stats.total_repos} total ({stats.public_repos} public)")
        print(f"⭐ Stars: {stats.total_stars:,}")
        print(f"🍴 Forks: {stats.total_forks:,}")
        print(f"👀 Watchers: {stats.total_watchers:,}")
        print(f"📊 Quality Score: {stats.quality_score}/100\n")
        
        print("🔝 Top 5 Repositories by Stars:")
        for i, repo in enumerate(stats.top_repositories[:5], 1):
            print(f"  {i}. {repo.name}")
            print(f"     ⭐ {repo.stargazers_count} | 🍴 {repo.forks_count} | {repo.language or 'N/A'}")
            if repo.description:
                desc = repo.description[:70] + '...' if len(repo.description) > 70 else repo.description
                print(f"     {desc}")
            print()
        
        print("💻 Primary Languages:")
        for i, lang_info in enumerate(stats.tech_stack_summary['primary_languages'][:5], 1):
            print(f"  {i}. {lang_info['name']:<20} {lang_info['percentage']:>5.1f}%")
        
        if stats.tech_stack_summary['frameworks']:
            print(f"\n🎨 Frameworks Detected:")
            print(f"  {', '.join(stats.tech_stack_summary['frameworks'])}")
        
        if stats.tech_stack_summary['databases']:
            print(f"\n💾 Databases Used:")
            print(f"  {', '.join(stats.tech_stack_summary['databases'])}")
        
        if stats.tech_stack_summary['tools']:
            print(f"\n🛠️  DevOps/Tools:")
            print(f"  {', '.join(stats.tech_stack_summary['tools'])}")
        
        if stats.top_topics:
            print(f"\n🏷️  Top Topics:")
            topics_str = ', '.join([t[0] for t in stats.top_topics[:10]])
            print(f"  {topics_str}")
        
        print(f"\n✅ Quality Metrics:")
        total = len(stats.top_repositories)
        print(f"  Tests:   {stats.repos_with_tests}/{total} repos")
        print(f"  CI/CD:   {stats.repos_with_ci}/{total} repos")
        print(f"  Docker:  {stats.repos_with_docker}/{total} repos")
        print(f"  License: {stats.repos_with_license}/{total} repos")
        print(f"  README:  {stats.repos_with_readme}/{total} repos")
        
        print(f"\n{'='*60}\n")
    
    def export_marketing_content(self, output_path: str = "exports/github_portfolio.md"):
        """Export marketing-ready content"""
        from pathlib import Path
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        stats = self.get_full_stats(deep_analysis=False)
        
        content = [
            f"# {self.user.name or self.username}'s GitHub Portfolio\n",
            f"**Total Repositories:** {stats.total_repos} | **Stars:** {stats.total_stars:,} | **Forks:** {stats.total_forks:,}\n",
            f"**Quality Score:** {stats.quality_score}/100\n",
            "---\n",
            "## 🌟 Featured Projects\n"
        ]
        
        for project in stats.showcase_projects:
            content.append(f"\n### [{project['title']}]({project['url']})\n")
            content.append(f"{project['description']}\n")
            content.append(f"\n**Tech Stack:** {', '.join(project['tech_stack'][:8])}\n")
            
            if project['features']:
                content.append("\n**Features:**\n")
                for feature in project['features'][:5]:
                    content.append(f"- {feature}\n")
            
            badges = []
            badges.append(f"⭐ {project['stars']} stars")
            if project['has_tests']:
                badges.append("✅ Tests")
            if project['has_ci']:
                badges.append("🔄 CI/CD")
            if project['has_docker']:
                badges.append("🐳 Docker")
            
            content.append(f"\n*{' | '.join(badges)}*\n")
        
        # Tech stack
        content.append("\n---\n\n## 🛠️ Tech Stack\n")
        
        tech = stats.tech_stack_summary
        if tech['primary_languages']:
            content.append("\n**Languages:**\n")
            for lang in tech['primary_languages'][:5]:
                content.append(f"- {lang['name']}: {lang['percentage']}%\n")
        
        if tech['frameworks']:
            content.append(f"\n**Frameworks:** {', '.join(tech['frameworks'])}\n")
        
        if tech['databases']:
            content.append(f"\n**Databases:** {', '.join(tech['databases'])}\n")
        
        if tech['tools']:
            content.append(f"\n**Tools:** {', '.join(tech['tools'])}\n")
        
        # Write file
        with open(output_path, 'w') as f:
            f.writelines(content)
        
        print(f"✓ Exported marketing content to {output_path}")
        return output_path


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze GitHub portfolio')
    parser.add_argument('--username', default='kaw393939', help='GitHub username')
    parser.add_argument('--fetch', action='store_true', help='Fetch repos from GitHub')
    parser.add_argument('--deep', action='store_true', help='Deep analysis (slower)')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--export', action='store_true', help='Export marketing content')
    parser.add_argument('--all', action='store_true', help='Do everything')
    
    args = parser.parse_args()
    
    analyzer = GitHubAnalyzer(username=args.username)
    
    if args.all or args.fetch:
        analyzer.fetch_all_repos()
    
    if args.all or args.stats:
        analyzer.get_full_stats(deep_analysis=args.deep or args.all)
    
    if args.all or args.export:
        analyzer.export_marketing_content()


if __name__ == '__main__':
    main()
