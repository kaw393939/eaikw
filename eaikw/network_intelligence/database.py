"""
Database management for Network Intelligence
"""
import sqlite3
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime
from models import LinkedInConnection, GitHubRepository, EnrichmentStatus


class NetworkDatabase:
    """SQLite database manager for network intelligence"""
    
    def __init__(self, db_path: str = "data/network_intel.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self._init_database()
    
    def _init_database(self):
        """Initialize database with schema"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # Connections table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                email TEXT,
                company TEXT,
                position TEXT,
                connected_on TEXT,
                headline TEXT,
                location TEXT,
                industry TEXT,
                summary TEXT,
                education TEXT,  -- JSON
                work_experience TEXT,  -- JSON
                skills TEXT,  -- JSON
                profile_picture_url TEXT,
                enrichment_status TEXT DEFAULT 'not_started',
                enriched_at TEXT,
                last_error TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # GitHub repositories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS github_repos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                full_name TEXT UNIQUE NOT NULL,
                description TEXT,
                html_url TEXT NOT NULL,
                homepage TEXT,
                stargazers_count INTEGER DEFAULT 0,
                forks_count INTEGER DEFAULT 0,
                watchers_count INTEGER DEFAULT 0,
                open_issues_count INTEGER DEFAULT 0,
                language TEXT,
                topics TEXT,  -- JSON array
                created_at TEXT,
                updated_at TEXT,
                pushed_at TEXT,
                is_fork INTEGER DEFAULT 0,
                is_archived INTEGER DEFAULT 0,
                is_private INTEGER DEFAULT 0,
                has_issues INTEGER DEFAULT 1,
                has_wiki INTEGER DEFAULT 1,
                has_pages INTEGER DEFAULT 0,
                readme_content TEXT,
                license TEXT,
                has_tests INTEGER DEFAULT 0,
                has_ci INTEGER DEFAULT 0,
                has_docker INTEGER DEFAULT 0,
                languages TEXT,  -- JSON object
                analyzed_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Analytics cache table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics_cache (
                cache_key TEXT PRIMARY KEY,
                cache_value TEXT,  -- JSON
                cached_at TEXT DEFAULT CURRENT_TIMESTAMP,
                expires_at TEXT
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_company ON connections(company)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_position ON connections(position)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_location ON connections(location)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_enrichment_status ON connections(enrichment_status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_repo_stars ON github_repos(stargazers_count DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_repo_language ON github_repos(language)")
        
        self.conn.commit()
    
    # Connection methods
    
    def save_connection(self, connection: LinkedInConnection) -> int:
        """Save or update a connection"""
        cursor = self.conn.cursor()
        
        data = connection.to_dict()
        
        # Convert lists/dicts to JSON
        data['education'] = json.dumps(data['education'])
        data['work_experience'] = json.dumps(data['work_experience'])
        data['skills'] = json.dumps(data['skills'])
        data['updated_at'] = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO connections (
                first_name, last_name, url, email, company, position,
                connected_on, headline, location, industry, summary,
                education, work_experience, skills, profile_picture_url,
                enrichment_status, enriched_at, last_error, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                first_name=excluded.first_name,
                last_name=excluded.last_name,
                email=excluded.email,
                company=excluded.company,
                position=excluded.position,
                connected_on=excluded.connected_on,
                headline=excluded.headline,
                location=excluded.location,
                industry=excluded.industry,
                summary=excluded.summary,
                education=excluded.education,
                work_experience=excluded.work_experience,
                skills=excluded.skills,
                profile_picture_url=excluded.profile_picture_url,
                enrichment_status=excluded.enrichment_status,
                enriched_at=excluded.enriched_at,
                last_error=excluded.last_error,
                updated_at=excluded.updated_at
        """, (
            data['first_name'], data['last_name'], data['url'], data['email'],
            data['company'], data['position'], data['connected_on'],
            data['headline'], data['location'], data['industry'],
            data['summary'], data['education'], data['work_experience'],
            data['skills'], data['profile_picture_url'],
            data['enrichment_status'], data['enriched_at'],
            data['last_error'], data['updated_at']
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_connection(self, url: str) -> Optional[LinkedInConnection]:
        """Get a connection by LinkedIn URL"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM connections WHERE url = ?", (url,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        return self._row_to_connection(row)
    
    def get_all_connections(self, enriched_only: bool = False) -> List[LinkedInConnection]:
        """Get all connections"""
        cursor = self.conn.cursor()
        
        if enriched_only:
            cursor.execute(
                "SELECT * FROM connections WHERE enrichment_status = ? ORDER BY last_name, first_name",
                (EnrichmentStatus.COMPLETED.value,)
            )
        else:
            cursor.execute("SELECT * FROM connections ORDER BY last_name, first_name")
        
        return [self._row_to_connection(row) for row in cursor.fetchall()]
    
    def get_connections_to_enrich(self, limit: Optional[int] = None) -> List[LinkedInConnection]:
        """Get connections that need enrichment"""
        cursor = self.conn.cursor()
        
        query = """
            SELECT * FROM connections 
            WHERE enrichment_status IN (?, ?)
            ORDER BY connected_on DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, (
            EnrichmentStatus.NOT_STARTED.value,
            EnrichmentStatus.FAILED.value
        ))
        
        return [self._row_to_connection(row) for row in cursor.fetchall()]
    
    def _row_to_connection(self, row: sqlite3.Row) -> LinkedInConnection:
        """Convert database row to LinkedInConnection"""
        education = json.loads(row['education']) if row['education'] else []
        work_experience = json.loads(row['work_experience']) if row['work_experience'] else []
        skills = json.loads(row['skills']) if row['skills'] else []
        
        return LinkedInConnection(
            first_name=row['first_name'],
            last_name=row['last_name'],
            url=row['url'],
            email=row['email'],
            company=row['company'],
            position=row['position'],
            connected_on=datetime.fromisoformat(row['connected_on']) if row['connected_on'] else None,
            headline=row['headline'],
            location=row['location'],
            industry=row['industry'],
            summary=row['summary'],
            education=education,
            work_experience=work_experience,
            skills=skills,
            profile_picture_url=row['profile_picture_url'],
            enrichment_status=EnrichmentStatus(row['enrichment_status']),
            enriched_at=datetime.fromisoformat(row['enriched_at']) if row['enriched_at'] else None,
            last_error=row['last_error']
        )
    
    # GitHub repository methods
    
    def save_repository(self, repo: GitHubRepository) -> int:
        """Save or update a repository"""
        cursor = self.conn.cursor()
        
        data = repo.to_dict()
        
        # Convert lists/dicts to JSON
        data['topics'] = json.dumps(data['topics'])
        data['languages'] = json.dumps(data['languages'])
        
        cursor.execute("""
            INSERT INTO github_repos (
                name, full_name, description, html_url, homepage,
                stargazers_count, forks_count, watchers_count, open_issues_count,
                language, topics, created_at, updated_at, pushed_at,
                is_fork, is_archived, is_private, has_issues, has_wiki, has_pages,
                readme_content, license, has_tests, has_ci, has_docker, languages
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(full_name) DO UPDATE SET
                description=excluded.description,
                homepage=excluded.homepage,
                stargazers_count=excluded.stargazers_count,
                forks_count=excluded.forks_count,
                watchers_count=excluded.watchers_count,
                open_issues_count=excluded.open_issues_count,
                language=excluded.language,
                topics=excluded.topics,
                updated_at=excluded.updated_at,
                pushed_at=excluded.pushed_at,
                is_archived=excluded.is_archived,
                readme_content=excluded.readme_content,
                license=excluded.license,
                has_tests=excluded.has_tests,
                has_ci=excluded.has_ci,
                has_docker=excluded.has_docker,
                languages=excluded.languages,
                analyzed_at=CURRENT_TIMESTAMP
        """, (
            data['name'], data['full_name'], data['description'],
            data['html_url'], data['homepage'],
            data['stargazers_count'], data['forks_count'],
            data['watchers_count'], data['open_issues_count'],
            data['language'], data['topics'],
            data['created_at'], data['updated_at'], data['pushed_at'],
            int(data['is_fork']), int(data['is_archived']), int(data['is_private']),
            int(data['has_issues']), int(data['has_wiki']), int(data['has_pages']),
            data['readme_content'], data['license'],
            int(data['has_tests']), int(data['has_ci']), int(data['has_docker']),
            data['languages']
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_repositories(self, include_forks: bool = False, include_archived: bool = False) -> List[GitHubRepository]:
        """Get all repositories"""
        cursor = self.conn.cursor()
        
        conditions = []
        if not include_forks:
            conditions.append("is_fork = 0")
        if not include_archived:
            conditions.append("is_archived = 0")
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        cursor.execute(f"""
            SELECT * FROM github_repos 
            WHERE {where_clause}
            ORDER BY stargazers_count DESC, updated_at DESC
        """)
        
        return [self._row_to_repository(row) for row in cursor.fetchall()]
    
    def _row_to_repository(self, row: sqlite3.Row) -> GitHubRepository:
        """Convert database row to GitHubRepository"""
        topics = json.loads(row['topics']) if row['topics'] else []
        languages = json.loads(row['languages']) if row['languages'] else {}
        
        return GitHubRepository(
            name=row['name'],
            full_name=row['full_name'],
            description=row['description'],
            html_url=row['html_url'],
            homepage=row['homepage'],
            stargazers_count=row['stargazers_count'],
            forks_count=row['forks_count'],
            watchers_count=row['watchers_count'],
            open_issues_count=row['open_issues_count'],
            language=row['language'],
            topics=topics,
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None,
            pushed_at=datetime.fromisoformat(row['pushed_at']) if row['pushed_at'] else None,
            is_fork=bool(row['is_fork']),
            is_archived=bool(row['is_archived']),
            is_private=bool(row['is_private']),
            has_issues=bool(row['has_issues']),
            has_wiki=bool(row['has_wiki']),
            has_pages=bool(row['has_pages']),
            readme_content=row['readme_content'],
            license=row['license'],
            has_tests=bool(row['has_tests']),
            has_ci=bool(row['has_ci']),
            has_docker=bool(row['has_docker']),
            languages=languages
        )
    
    # Analytics cache methods
    
    def cache_get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached analytics result"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT cache_value, expires_at FROM analytics_cache
            WHERE cache_key = ? AND (expires_at IS NULL OR expires_at > ?)
        """, (key, datetime.now().isoformat()))
        
        row = cursor.fetchone()
        if row:
            return json.loads(row['cache_value'])
        return None
    
    def cache_set(self, key: str, value: Dict[str, Any], ttl_seconds: Optional[int] = None):
        """Set cached analytics result"""
        cursor = self.conn.cursor()
        
        expires_at = None
        if ttl_seconds:
            expires_at = datetime.fromtimestamp(
                datetime.now().timestamp() + ttl_seconds
            ).isoformat()
        
        cursor.execute("""
            INSERT INTO analytics_cache (cache_key, cache_value, expires_at)
            VALUES (?, ?, ?)
            ON CONFLICT(cache_key) DO UPDATE SET
                cache_value=excluded.cache_value,
                cached_at=CURRENT_TIMESTAMP,
                expires_at=excluded.expires_at
        """, (key, json.dumps(value), expires_at))
        
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
