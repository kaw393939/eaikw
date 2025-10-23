"""
Data models for Network Intelligence system
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class EnrichmentStatus(Enum):
    """Status of connection enrichment"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RATE_LIMITED = "rate_limited"


@dataclass
class Education:
    """Education entry"""
    school: str
    degree: Optional[str] = None
    field: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    
    def __str__(self):
        parts = [self.school]
        if self.degree:
            parts.append(self.degree)
        if self.field:
            parts.append(f"in {self.field}")
        return " - ".join(parts)


@dataclass
class WorkExperience:
    """Work experience entry"""
    company: str
    title: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: bool = False
    description: Optional[str] = None


@dataclass
class LinkedInConnection:
    """LinkedIn connection with enriched data"""
    # From CSV export
    first_name: str
    last_name: str
    url: str
    email: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    connected_on: Optional[datetime] = None
    
    # Enriched data (from scraping/API)
    headline: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None
    summary: Optional[str] = None
    education: List[Education] = field(default_factory=list)
    work_experience: List[WorkExperience] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    profile_picture_url: Optional[str] = None
    
    # Metadata
    enrichment_status: EnrichmentStatus = EnrichmentStatus.NOT_STARTED
    enriched_at: Optional[datetime] = None
    last_error: Optional[str] = None
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_enriched(self) -> bool:
        return self.enrichment_status == EnrichmentStatus.COMPLETED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'url': self.url,
            'email': self.email,
            'company': self.company,
            'position': self.position,
            'connected_on': self.connected_on.isoformat() if self.connected_on else None,
            'headline': self.headline,
            'location': self.location,
            'industry': self.industry,
            'summary': self.summary,
            'education': [
                {
                    'school': e.school,
                    'degree': e.degree,
                    'field': e.field,
                    'start_year': e.start_year,
                    'end_year': e.end_year
                } for e in self.education
            ],
            'work_experience': [
                {
                    'company': w.company,
                    'title': w.title,
                    'location': w.location,
                    'start_date': w.start_date,
                    'end_date': w.end_date,
                    'is_current': w.is_current,
                    'description': w.description
                } for w in self.work_experience
            ],
            'skills': self.skills,
            'profile_picture_url': self.profile_picture_url,
            'enrichment_status': self.enrichment_status.value,
            'enriched_at': self.enriched_at.isoformat() if self.enriched_at else None,
            'last_error': self.last_error
        }


@dataclass
class GitHubRepository:
    """GitHub repository data"""
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    homepage: Optional[str]
    
    # Stats
    stargazers_count: int = 0
    forks_count: int = 0
    watchers_count: int = 0
    open_issues_count: int = 0
    
    # Metadata
    language: Optional[str] = None
    topics: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    pushed_at: Optional[datetime] = None
    
    # Flags
    is_fork: bool = False
    is_archived: bool = False
    is_private: bool = False
    has_issues: bool = True
    has_wiki: bool = True
    has_pages: bool = False
    
    # Content
    readme_content: Optional[str] = None
    license: Optional[str] = None
    
    # Analysis
    has_tests: bool = False
    has_ci: bool = False
    has_docker: bool = False
    languages: Dict[str, int] = field(default_factory=dict)  # Language: bytes of code
    
    @property
    def is_significant(self) -> bool:
        """Is this a significant/showcase-worthy repo?"""
        return (
            not self.is_fork and 
            not self.is_archived and
            (self.stargazers_count > 0 or self.forks_count > 0 or 
             (self.updated_at and (datetime.now() - self.updated_at).days < 365))
        )
    
    @property
    def primary_language(self) -> Optional[str]:
        """Get primary language by bytes of code"""
        if not self.languages:
            return self.language
        return max(self.languages.items(), key=lambda x: x[1])[0]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            'name': self.name,
            'full_name': self.full_name,
            'description': self.description,
            'html_url': self.html_url,
            'homepage': self.homepage,
            'stargazers_count': self.stargazers_count,
            'forks_count': self.forks_count,
            'watchers_count': self.watchers_count,
            'open_issues_count': self.open_issues_count,
            'language': self.language,
            'topics': self.topics,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'pushed_at': self.pushed_at.isoformat() if self.pushed_at else None,
            'is_fork': self.is_fork,
            'is_archived': self.is_archived,
            'is_private': self.is_private,
            'has_issues': self.has_issues,
            'has_wiki': self.has_wiki,
            'has_pages': self.has_pages,
            'readme_content': self.readme_content,
            'license': self.license,
            'has_tests': self.has_tests,
            'has_ci': self.has_ci,
            'has_docker': self.has_docker,
            'languages': self.languages
        }


@dataclass
class NetworkInsight:
    """Analytical insights from network data"""
    total_connections: int
    
    # Company insights
    top_companies: List[tuple]  # [(company, count), ...]
    target_companies_present: List[tuple]  # [(company, count), ...]
    
    # Education insights
    top_schools: List[tuple]
    top_degrees: List[tuple]
    
    # Geographic insights
    top_locations: List[tuple]
    top_countries: List[tuple]
    
    # Industry insights
    top_industries: List[tuple]
    
    # Role insights
    top_titles: List[tuple]
    decision_makers: List[LinkedInConnection]  # CTOs, VPs, etc.
    
    # Skills insights
    top_skills: List[tuple]
    
    # Temporal insights
    connections_by_year: Dict[int, int]
    recent_connections: List[LinkedInConnection]  # Last 90 days
    
    # Opportunity insights
    warm_intro_paths: Dict[str, List[LinkedInConnection]]  # company -> connections
    alumni_network: List[LinkedInConnection]
    same_company_alumni: List[LinkedInConnection]


@dataclass
class GitHubPortfolioStats:
    """Comprehensive GitHub portfolio statistics"""
    username: str
    
    # Basic stats
    total_repos: int
    public_repos: int
    private_repos: int
    
    # Engagement
    total_stars: int
    total_forks: int
    total_watchers: int
    
    # Activity
    total_commits: int
    repos_contributed_to: int
    
    # Content
    top_repositories: List[GitHubRepository]
    recent_repositories: List[GitHubRepository]
    
    # Technology
    languages_used: Dict[str, int]  # Language: total bytes across all repos
    top_topics: List[tuple]  # [(topic, count), ...]
    
    # Quality indicators
    repos_with_tests: int
    repos_with_ci: int
    repos_with_docker: int
    repos_with_license: int
    repos_with_readme: int
    
    # Collaboration
    organizations: List[str]
    top_contributors: List[tuple]  # [(username, contribution_count), ...]
    
    # Marketing assets
    showcase_projects: List[Dict[str, Any]]
    tech_stack_summary: Dict[str, Any]
    
    @property
    def engagement_rate(self) -> float:
        """Average stars per repo"""
        return self.total_stars / self.public_repos if self.public_repos > 0 else 0
    
    @property
    def quality_score(self) -> float:
        """Quality score 0-100"""
        if self.public_repos == 0:
            return 0
        
        score = 0
        score += (self.repos_with_tests / self.public_repos) * 30
        score += (self.repos_with_ci / self.public_repos) * 25
        score += (self.repos_with_license / self.public_repos) * 20
        score += (self.repos_with_readme / self.public_repos) * 15
        score += (self.repos_with_docker / self.public_repos) * 10
        
        return round(score, 2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'username': self.username,
            'total_repos': self.total_repos,
            'public_repos': self.public_repos,
            'private_repos': self.private_repos,
            'total_stars': self.total_stars,
            'total_forks': self.total_forks,
            'total_watchers': self.total_watchers,
            'total_commits': self.total_commits,
            'repos_contributed_to': self.repos_contributed_to,
            'top_repositories': [r.to_dict() for r in self.top_repositories],
            'recent_repositories': [r.to_dict() for r in self.recent_repositories],
            'languages_used': self.languages_used,
            'top_topics': self.top_topics,
            'repos_with_tests': self.repos_with_tests,
            'repos_with_ci': self.repos_with_ci,
            'repos_with_docker': self.repos_with_docker,
            'repos_with_license': self.repos_with_license,
            'repos_with_readme': self.repos_with_readme,
            'organizations': self.organizations,
            'top_contributors': self.top_contributors,
            'showcase_projects': self.showcase_projects,
            'tech_stack_summary': self.tech_stack_summary,
            'engagement_rate': self.engagement_rate,
            'quality_score': self.quality_score
        }
