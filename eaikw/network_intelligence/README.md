# Network Intelligence Crawler

**Purpose:** Extract actionable intelligence from your professional network (LinkedIn connections) and technical portfolio (GitHub).

## ⚠️ LEGAL & ETHICAL NOTICE

**LinkedIn Scraping:**
- LinkedIn's Terms of Service **prohibit automated scraping**
- This tool uses **public profile URLs** from your own connection export
- **Use responsibly** and only for personal research
- Consider using LinkedIn Sales Navigator API for commercial use
- We implement rate limiting and respectful crawling practices

**GitHub API:**
- GitHub API has rate limits: 5,000 requests/hour (authenticated)
- We respect rate limits and cache results
- All data accessed is public or accessible via your personal token

## 🎯 What This Does

### LinkedIn Connection Analysis
1. **Extracts from your export CSV:**
   - Full name, current company, position
   - LinkedIn profile URL
   - Connection date

2. **Enriches each connection (optional public scraping):**
   - Current position details
   - Education history
   - Skills & endorsements
   - Location
   - Industry
   - Profile headline/summary (if public)

3. **Analytics & Insights:**
   - Top companies in your network
   - Top universities/schools
   - Geographic distribution
   - Industry breakdown
   - Role/title distribution
   - Connection growth over time
   - Potential warm intro paths

### GitHub Portfolio Analysis
1. **Your Repository Stats:**
   - Total repos, stars, forks
   - Languages used (LOC count)
   - Most popular projects
   - Contribution patterns
   - Issue/PR activity

2. **Code Quality Metrics:**
   - Repos with tests
   - Repos with CI/CD
   - Documentation coverage
   - License usage
   - Active vs archived projects

3. **Technology Stack:**
   - Programming languages (ranked by usage)
   - Frameworks detected
   - DevOps tools (Docker, K8s, etc.)
   - Database technologies
   - Cloud platforms

4. **Collaboration:**
   - Contributors to your projects
   - Projects you've contributed to
   - Organizations you're part of

5. **Portfolio Assets for Marketing:**
   - README content extraction
   - Project descriptions
   - Demo/screenshot links
   - Live deployment URLs

## 📦 Installation

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your tokens

# 4. Create data directory
mkdir -p data
```

## 🔑 Setup GitHub Token

1. Go to: https://github.com/settings/tokens/new
2. Click "Generate new token (classic)"
3. Select scopes:
   - ✅ `repo` (access repositories)
   - ✅ `read:user` (read user profile)
   - ✅ `read:org` (read organization membership)
4. Generate token and copy to `.env`

## 🚀 Usage

### Quick Start: Analyze Everything

```bash
# Run full analysis
python main.py --all

# Output:
# - data/network_intel.db (SQLite database)
# - reports/network_analysis.html
# - reports/github_portfolio.html
# - exports/connections_enriched.xlsx
# - exports/github_stats.json
```

### LinkedIn Connections Only

```bash
# Basic: Use only data from your CSV export
python linkedin_analyzer.py --basic

# Enriched: Scrape public profiles (respects rate limits)
python linkedin_analyzer.py --enrich --rate-limit 5

# With specific CSV file
python linkedin_analyzer.py --csv ../Basic_LinkedInDataExport_10-22-2025.zip/Connections.csv
```

### GitHub Portfolio Only

```bash
# Analyze your GitHub profile
python github_analyzer.py --username kaw393939

# Include private repos (requires token with repo scope)
python github_analyzer.py --username kaw393939 --include-private

# Deep analysis (slower, more detailed)
python github_analyzer.py --username kaw393939 --deep
```

### Generate Marketing Assets

```bash
# Extract portfolio content for website
python export_marketing.py --format markdown

# Generate project showcase
python export_marketing.py --showcase --top 10

# Export testimonials-ready data
python export_marketing.py --testimonials
```

## 📊 Output Files

### Database Schema
```
network_intel.db
├── connections
│   ├── id (primary key)
│   ├── first_name
│   ├── last_name
│   ├── company
│   ├── position
│   ├── linkedin_url
│   ├── connected_on
│   ├── education (JSON)
│   ├── skills (JSON)
│   ├── location
│   ├── industry
│   └── enriched_at
│
├── github_repos
│   ├── id (primary key)
│   ├── name
│   ├── description
│   ├── language
│   ├── stars
│   ├── forks
│   ├── created_at
│   ├── updated_at
│   ├── topics (JSON)
│   ├── has_tests
│   ├── has_ci
│   └── readme_content
│
└── analytics_cache
    └── (cached analysis results)
```

### Reports
- `reports/network_analysis.html` - Interactive dashboard of your network
- `reports/github_portfolio.html` - Portfolio showcase page
- `reports/insights.txt` - Text summary of key findings

### Exports
- `exports/connections_enriched.xlsx` - Spreadsheet with all connection data
- `exports/github_stats.json` - JSON with all GitHub metrics
- `exports/top_connections.csv` - High-value connections ranked
- `exports/portfolio_assets.md` - Marketing-ready project descriptions

## 🔍 Analysis Features

### Network Intelligence

```python
from linkedin_analyzer import LinkedInAnalyzer

analyzer = LinkedInAnalyzer(csv_path='Connections.csv')

# Load and enrich data
analyzer.load_connections()
analyzer.enrich_connections(rate_limit=5)  # 5 requests per minute

# Get insights
top_companies = analyzer.get_top_companies(limit=20)
top_schools = analyzer.get_top_schools(limit=20)
industry_breakdown = analyzer.get_industry_distribution()
location_heatmap = analyzer.get_location_distribution()

# Find warm intro paths
potential_clients = analyzer.find_connections_at_companies(['Google', 'Amazon', 'Microsoft'])

# Export for CRM
analyzer.export_to_excel('my_network.xlsx')
```

### GitHub Portfolio

```python
from github_analyzer import GitHubAnalyzer

analyzer = GitHubAnalyzer(username='kaw393939', token='your_token')

# Get comprehensive stats
stats = analyzer.get_full_stats()

# Get top projects by stars
top_projects = analyzer.get_top_repos(by='stars', limit=10)

# Get technology stack
tech_stack = analyzer.analyze_tech_stack()

# Get marketing-ready descriptions
marketing_assets = analyzer.export_marketing_content()

# Find collaborative opportunities
contributors = analyzer.get_top_contributors()
```

## 📈 Example Insights

### From Your Network
```
Top 10 Companies in Your Network:
1. JPMorgan Chase (45 connections)
2. Goldman Sachs (32 connections)
3. Amazon (28 connections)
4. Microsoft (25 connections)
5. Google (18 connections)
...

Top Skills in Your Network:
1. Python (340 connections)
2. Machine Learning (285 connections)
3. AWS (240 connections)
...

Warm Intro Opportunities:
- Google Cloud Platform: 12 connections who work there
- OpenAI: 3 connections (including 1 engineer)
```

### From Your GitHub
```
Total Public Repositories: 87
Total Stars Received: 456
Total Forks: 123

Top Languages:
1. Python (45% of code)
2. JavaScript (25%)
3. TypeScript (12%)

Standout Projects:
1. enterprise_ai_demo1_websearch (123 stars)
2. code_quality_calc (45 stars)
3. docker_fastapi_poetry (32 stars)

Technology Stack Detected:
- Frameworks: FastAPI, React, LangChain, LangGraph
- Databases: PostgreSQL, Neo4j, Qdrant
- DevOps: Docker, Docker Compose, GitHub Actions
- Testing: pytest, Jest
- AI/ML: OpenAI, HuggingFace, scikit-learn
```

## 🛡️ Privacy & Ethics

**We prioritize ethical data collection:**

1. **Only Your Data:**
   - We only analyze connections YOU already have
   - We only access YOUR GitHub repositories

2. **Respect Rate Limits:**
   - Default: 5 requests/minute for LinkedIn
   - GitHub: Uses official API with proper authentication
   - Implements exponential backoff for retries

3. **No Spam:**
   - This is for analysis only
   - No automated messaging
   - No bulk connection requests

4. **Data Storage:**
   - All data stored locally in SQLite
   - No cloud uploads without your permission
   - Easy to delete: `rm data/network_intel.db`

5. **LinkedIn Scraping Alternatives:**
   - Consider LinkedIn Sales Navigator API (paid)
   - Use Phantombuster or similar services
   - Or just use the basic CSV data (no scraping)

## 🎯 Marketing Use Cases

### For Your Website
```bash
# Get top 10 projects with descriptions
python github_analyzer.py --export-top 10 --format markdown > ../website/github_projects.md

# Get network size stats
python linkedin_analyzer.py --stats-only > ../website/network_stats.txt
```

### For Outreach
```bash
# Find connections at target companies
python linkedin_analyzer.py --filter-companies "Goldman Sachs,JPMorgan,Citigroup" > target_outreach.csv

# Find alumni from same school
python linkedin_analyzer.py --filter-schools "NJIT,Rutgers" > alumni_network.csv
```

### For Blog Content
```bash
# Generate "Year in Code" stats
python github_analyzer.py --year-stats 2024 > blog_github_2024.md

# Network growth analysis
python linkedin_analyzer.py --growth-analysis > blog_network_growth.md
```

## 🐛 Troubleshooting

**LinkedIn scraping blocked:**
- LinkedIn actively blocks automated access
- Try reducing rate limit: `--rate-limit 2`
- Use VPN or different IP address
- Consider using only the CSV data (no enrichment)
- Use LinkedIn official APIs if available

**GitHub rate limit exceeded:**
- Wait for rate limit reset (check headers)
- Use authenticated requests (provide token)
- Cache results to avoid re-fetching

**Selenium WebDriver issues:**
```bash
# Update ChromeDriver
pip install --upgrade webdriver-manager

# Or manually specify ChromeDriver path
python linkedin_analyzer.py --chrome-driver /path/to/chromedriver
```

## 📚 Advanced Usage

### Custom Analysis Queries

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/network_intel.db')

# Find connections who might need AI consulting
query = """
SELECT first_name, last_name, company, position, linkedin_url
FROM connections
WHERE (position LIKE '%CTO%' OR position LIKE '%VP Engineering%')
  AND company IN ('Fortune500List')
  AND connected_on > '2020-01-01'
ORDER BY connected_on DESC
"""

prospects = pd.read_sql_query(query, conn)
prospects.to_csv('ai_consulting_prospects.csv', index=False)
```

### Automate Weekly Reports

```bash
# Add to cron for weekly network analysis
0 9 * * MON cd /path/to/network_intelligence && python main.py --weekly-report --email your@email.com
```

## 🔮 Future Enhancements

- [ ] Integration with CRM (Salesforce, HubSpot)
- [ ] Automated warm intro suggestions
- [ ] Email sequence generation for outreach
- [ ] Network visualization (graph database)
- [ ] AI-powered connection prioritization
- [ ] LinkedIn post performance tracking
- [ ] GitHub contribution graph analysis
- [ ] Competitive intelligence (track competitors' GitHub)

## 📞 Support

Questions? Check the docs or open an issue.

**Remember:** Use this tool responsibly and ethically. Respect others' privacy and platform terms of service.
