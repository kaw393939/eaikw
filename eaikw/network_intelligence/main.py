"""
Main entry point for Network Intelligence Crawler
"""
import argparse
from pathlib import Path

from linkedin_analyzer import LinkedInAnalyzer
from github_analyzer import GitHubAnalyzer


def main():
    parser = argparse.ArgumentParser(
        description='Network Intelligence Crawler - Extract insights from LinkedIn and GitHub'
    )
    
    # Data sources
    parser.add_argument('--linkedin-csv', default='../Basic_LinkedInDataExport_10-22-2025.zip/Connections.csv')
    parser.add_argument('--github-username', default='kaw393939')
    
    # LinkedIn actions
    parser.add_argument('--linkedin', action='store_true', help='Analyze LinkedIn network')
    parser.add_argument('--linkedin-load', action='store_true', help='Load connections from CSV')
    parser.add_argument('--linkedin-export', action='store_true', help='Export to Excel')
    
    # GitHub actions
    parser.add_argument('--github', action='store_true', help='Analyze GitHub portfolio')
    parser.add_argument('--github-fetch', action='store_true', help='Fetch repos from GitHub API')
    parser.add_argument('--github-deep', action='store_true', help='Deep analysis (slower)')
    parser.add_argument('--github-export', action='store_true', help='Export marketing content')
    
    # Combined actions
    parser.add_argument('--all', action='store_true', help='Analyze everything')
    
    args = parser.parse_args()
    
    if not any([args.linkedin, args.github, args.all]):
        parser.print_help()
        return
    
    print("="*70)
    print("NETWORK INTELLIGENCE CRAWLER")
    print("="*70)
    print()
    
    # LinkedIn Analysis
    if args.all or args.linkedin or args.linkedin_load:
        print("\n" + "="*70)
        print("LINKEDIN NETWORK ANALYSIS")
        print("="*70 + "\n")
        
        linkedin = LinkedInAnalyzer(args.linkedin_csv)
        
        if args.all or args.linkedin_load:
            linkedin.load_from_csv()
        
        linkedin.load_all_connections()
        insight = linkedin.analyze_network()
        
        if args.all or args.linkedin_export:
            linkedin.export_to_excel()
        
        # Print actionable insights
        print("\n📈 ACTIONABLE INSIGHTS:\n")
        
        if insight.target_companies_present:
            print("🎯 Warm Intro Opportunities:")
            for company, count in sorted(insight.target_companies_present, key=lambda x: x[1], reverse=True)[:5]:
                print(f"  • {company}: {count} connections (reach out for warm intros)")
        
        if insight.decision_makers:
            print(f"\n👔 Decision Makers in Network: {len(insight.decision_makers)}")
            print("   Consider targeted outreach to CTOs, VPs, Directors")
        
        if insight.recent_connections:
            print(f"\n🆕 Recent Connections: {len(insight.recent_connections)}")
            print("   Consider re-engaging with new connections")
    
    # GitHub Analysis
    if args.all or args.github or args.github_fetch:
        print("\n" + "="*70)
        print("GITHUB PORTFOLIO ANALYSIS")
        print("="*70 + "\n")
        
        github = GitHubAnalyzer(username=args.github_username)
        
        if args.all or args.github_fetch:
            github.fetch_all_repos()
        
        stats = github.get_full_stats(deep_analysis=args.github_deep or args.all)
        
        if args.all or args.github_export:
            github.export_marketing_content()
        
        # Print marketing insights
        print("\n📢 MARKETING INSIGHTS:\n")
        
        print(f"Portfolio Headline:")
        print(f"  \"{stats.total_repos} open source projects | {stats.total_stars} stars | {stats.quality_score}/100 quality score\"")
        
        print(f"\nTop Tech Stack Keywords:")
        if stats.tech_stack_summary['primary_languages']:
            langs = [l['name'] for l in stats.tech_stack_summary['primary_languages'][:3]]
            print(f"  Languages: {', '.join(langs)}")
        
        if stats.tech_stack_summary['frameworks']:
            print(f"  Frameworks: {', '.join(stats.tech_stack_summary['frameworks'][:5])}")
        
        if stats.showcase_projects:
            print(f"\n⭐ Showcase These Projects:")
            for proj in stats.showcase_projects[:3]:
                print(f"  • {proj['title']}: {proj['stars']} stars")
    
    print("\n" + "="*70)
    print("✓ Analysis complete!")
    print("="*70)
    print("\nNext steps:")
    print("1. Review reports in exports/ directory")
    print("2. Check database: data/network_intel.db")
    print("3. Use insights for website/LinkedIn content")
    print()


if __name__ == '__main__':
    main()
