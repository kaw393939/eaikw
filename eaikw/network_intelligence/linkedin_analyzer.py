"""
LinkedIn Connection Analyzer

NOTE: LinkedIn Terms of Service prohibit automated scraping.
This tool uses your existing CSV export for basic analysis.
Enrichment features are provided for educational purposes only.
"""
import csv
import time
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path
from collections import Counter

from models import LinkedInConnection, NetworkInsight, EnrichmentStatus
from database import NetworkDatabase


class LinkedInAnalyzer:
    """Analyze LinkedIn connections from CSV export"""
    
    def __init__(self, csv_path: str, db_path: str = "data/network_intel.db"):
        self.csv_path = Path(csv_path)
        self.db = NetworkDatabase(db_path)
        self.connections: List[LinkedInConnection] = []
    
    def load_from_csv(self) -> int:
        """Load connections from LinkedIn CSV export"""
        print(f"Loading connections from {self.csv_path}...")
        
        count = 0
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            # LinkedIn CSV has this structure:
            # Line 1: "Notes:"
            # Line 2: The notes text (long quoted string)
            # Line 3: Empty line
            # Line 4: CSV header (First Name, Last Name, URL, etc.)
            # Line 5+: Actual data
            next(f)  # Skip "Notes:" line
            next(f)  # Skip notes text line  
            next(f)  # Skip empty line
            # Now csv.DictReader will use line 4 as the header
            reader = csv.DictReader(f)
            
            for row in reader:
                # Skip empty rows
                if not row.get('First Name') and not row.get('Last Name'):
                    continue
                
                # Parse connected date
                connected_on = None
                if row.get('Connected On'):
                    try:
                        connected_on = datetime.strptime(
                            row['Connected On'], 
                            '%d %b %Y'
                        )
                    except ValueError:
                        pass
                
                connection = LinkedInConnection(
                    first_name=row.get('First Name', '').strip(),
                    last_name=row.get('Last Name', '').strip(),
                    url=row.get('URL', '').strip(),
                    email=row.get('Email Address', '').strip() or None,
                    company=row.get('Company', '').strip() or None,
                    position=row.get('Position', '').strip() or None,
                    connected_on=connected_on
                )
                
                # Save to database
                self.db.save_connection(connection)
                count += 1
        
        print(f"✓ Loaded {count} connections")
        return count
    
    def load_all_connections(self) -> List[LinkedInConnection]:
        """Load all connections from database"""
        self.connections = self.db.get_all_connections()
        print(f"Loaded {len(self.connections)} connections from database")
        return self.connections
    
    def analyze_network(self) -> NetworkInsight:
        """Generate comprehensive network insights"""
        print("\n📊 Analyzing network...")
        
        if not self.connections:
            self.load_all_connections()
        
        # Company analysis
        companies = [c.company for c in self.connections if c.company]
        top_companies = Counter(companies).most_common(20)
        
        # Position/title analysis
        positions = [c.position for c in self.connections if c.position]
        top_titles = Counter(positions).most_common(20)
        
        # Location analysis
        locations = [c.location for c in self.connections if c.location]
        top_locations = Counter(locations).most_common(20)
        
        # Extract countries from locations
        countries = []
        for loc in locations:
            if ',' in loc:
                countries.append(loc.split(',')[-1].strip())
        top_countries = Counter(countries).most_common(20)
        
        # Industry analysis (if enriched)
        industries = [c.industry for c in self.connections if c.industry]
        top_industries = Counter(industries).most_common(20)
        
        # Education analysis (if enriched)
        schools = []
        degrees = []
        for conn in self.connections:
            for edu in conn.education:
                if edu.school:
                    schools.append(edu.school)
                if edu.degree:
                    degrees.append(edu.degree)
        
        top_schools = Counter(schools).most_common(20)
        top_degrees = Counter(degrees).most_common(20)
        
        # Skills analysis (if enriched)
        all_skills = []
        for conn in self.connections:
            all_skills.extend(conn.skills)
        top_skills = Counter(all_skills).most_common(50)
        
        # Temporal analysis
        connections_by_year = {}
        for conn in self.connections:
            if conn.connected_on:
                year = conn.connected_on.year
                connections_by_year[year] = connections_by_year.get(year, 0) + 1
        
        # Recent connections (last 90 days)
        ninety_days_ago = datetime.now().timestamp() - (90 * 24 * 60 * 60)
        recent = [
            c for c in self.connections 
            if c.connected_on and c.connected_on.timestamp() > ninety_days_ago
        ]
        
        # Decision makers (CTOs, VPs, Directors, etc.)
        decision_maker_keywords = [
            'cto', 'chief technology', 'chief technical',
            'vp', 'vice president', 
            'director', 'head of', 'lead',
            'founder', 'co-founder', 'ceo', 'president'
        ]
        
        decision_makers = []
        for conn in self.connections:
            if conn.position:
                pos_lower = conn.position.lower()
                if any(keyword in pos_lower for keyword in decision_maker_keywords):
                    decision_makers.append(conn)
        
        # Find target companies
        target_companies = [
            'Google', 'Amazon', 'Microsoft', 'Meta', 'Apple',
            'JPMorgan', 'Goldman Sachs', 'Bank of America', 'Citigroup',
            'Morgan Stanley', 'Wells Fargo'
        ]
        
        target_company_connections = {}
        for target in target_companies:
            matches = [
                c for c in self.connections 
                if c.company and target.lower() in c.company.lower()
            ]
            if matches:
                target_company_connections[target] = matches
        
        insight = NetworkInsight(
            total_connections=len(self.connections),
            top_companies=top_companies,
            target_companies_present=[
                (company, len(conns)) 
                for company, conns in target_company_connections.items()
            ],
            top_schools=top_schools,
            top_degrees=top_degrees,
            top_locations=top_locations,
            top_countries=top_countries,
            top_industries=top_industries,
            top_titles=top_titles,
            decision_makers=decision_makers,
            top_skills=top_skills,
            connections_by_year=connections_by_year,
            recent_connections=recent,
            warm_intro_paths=target_company_connections,
            alumni_network=[],  # Would need school data
            same_company_alumni=[]  # Would need historical data
        )
        
        self._print_insights(insight)
        return insight
    
    def _print_insights(self, insight: NetworkInsight):
        """Print formatted insights"""
        print(f"\n{'='*60}")
        print(f"NETWORK ANALYSIS RESULTS")
        print(f"{'='*60}\n")
        
        print(f"📊 Total Connections: {insight.total_connections:,}\n")
        
        print("🏢 Top 10 Companies:")
        for i, (company, count) in enumerate(insight.top_companies[:10], 1):
            print(f"  {i:2d}. {company:<40} ({count:3d} connections)")
        
        print(f"\n👔 Top 10 Job Titles:")
        for i, (title, count) in enumerate(insight.top_titles[:10], 1):
            title_short = title[:50] + '...' if len(title) > 50 else title
            print(f"  {i:2d}. {title_short:<50} ({count:3d})")
        
        print(f"\n📍 Top 10 Locations:")
        for i, (location, count) in enumerate(insight.top_locations[:10], 1):
            print(f"  {i:2d}. {location:<40} ({count:3d})")
        
        if insight.top_industries:
            print(f"\n🏭 Top 10 Industries:")
            for i, (industry, count) in enumerate(insight.top_industries[:10], 1):
                print(f"  {i:2d}. {industry:<40} ({count:3d})")
        
        if insight.top_skills:
            print(f"\n💡 Top 15 Skills in Network:")
            for i, (skill, count) in enumerate(insight.top_skills[:15], 1):
                print(f"  {i:2d}. {skill:<40} ({count:4d})")
        
        print(f"\n🎯 Decision Makers ({len(insight.decision_makers)}):")
        print(f"  (CTOs, VPs, Directors, Founders, etc.)")
        
        if insight.target_companies_present:
            print(f"\n🎯 Connections at Target Companies:")
            for company, count in sorted(
                insight.target_companies_present, 
                key=lambda x: x[1], 
                reverse=True
            ):
                print(f"  • {company:<30} {count:3d} connections")
        
        if insight.recent_connections:
            print(f"\n🆕 Recent Connections (Last 90 days): {len(insight.recent_connections)}")
        
        if insight.connections_by_year:
            print(f"\n📈 Connection Growth:")
            for year in sorted(insight.connections_by_year.keys()):
                count = insight.connections_by_year[year]
                bar = '█' * (count // 10)
                print(f"  {year}: {count:4d} {bar}")
        
        print(f"\n{'='*60}\n")
    
    def export_to_excel(self, output_path: str = "exports/connections_enriched.xlsx"):
        """Export connections to Excel"""
        import pandas as pd
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.connections:
            self.load_all_connections()
        
        # Convert to dict for DataFrame
        data = []
        for conn in self.connections:
            row = {
                'First Name': conn.first_name,
                'Last Name': conn.last_name,
                'Company': conn.company,
                'Position': conn.position,
                'Location': conn.location,
                'Industry': conn.industry,
                'LinkedIn URL': conn.url,
                'Email': conn.email,
                'Connected On': conn.connected_on.strftime('%Y-%m-%d') if conn.connected_on else '',
                'Headline': conn.headline,
                'Schools': ', '.join([e.school for e in conn.education]),
                'Degrees': ', '.join([e.degree for e in conn.education if e.degree]),
                'Skills': ', '.join(conn.skills[:10]),  # Top 10 skills
                'Is Enriched': 'Yes' if conn.is_enriched else 'No'
            }
            data.append(row)
        
        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False, sheet_name='Connections')
        
        print(f"✓ Exported {len(data)} connections to {output_path}")
        return output_path
    
    def find_warm_intros(self, target_companies: List[str]) -> Dict[str, List[LinkedInConnection]]:
        """Find connections at specific companies"""
        if not self.connections:
            self.load_all_connections()
        
        results = {}
        for target in target_companies:
            matches = [
                c for c in self.connections
                if c.company and target.lower() in c.company.lower()
            ]
            if matches:
                results[target] = matches
                print(f"\n{target}: {len(matches)} connections")
                for conn in matches[:5]:  # Show first 5
                    print(f"  • {conn.full_name} - {conn.position}")
                if len(matches) > 5:
                    print(f"  ... and {len(matches) - 5} more")
        
        return results


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze LinkedIn connections')
    parser.add_argument(
        '--csv',
        default='../Basic_LinkedInDataExport_10-22-2025.zip/Connections.csv',
        help='Path to Connections.csv from LinkedIn export'
    )
    parser.add_argument('--load', action='store_true', help='Load connections from CSV')
    parser.add_argument('--analyze', action='store_true', help='Analyze network')
    parser.add_argument('--export', action='store_true', help='Export to Excel')
    parser.add_argument('--all', action='store_true', help='Do everything')
    
    args = parser.parse_args()
    
    analyzer = LinkedInAnalyzer(args.csv)
    
    if args.all or args.load:
        analyzer.load_from_csv()
    
    if args.all or args.analyze:
        analyzer.load_all_connections()
        analyzer.analyze_network()
    
    if args.all or args.export:
        analyzer.export_to_excel()


if __name__ == '__main__':
    main()
