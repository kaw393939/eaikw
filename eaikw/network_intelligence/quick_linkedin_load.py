"""
Quick script to load LinkedIn connections
"""
from linkedin_analyzer import LinkedInAnalyzer

# Load connections
csv_path = "/Users/kwilliams/Desktop/Projects/education_library/Basic_LinkedInDataExport_10-22-2025.zip/Connections.csv"
analyzer = LinkedInAnalyzer(csv_path)

print("Loading connections from CSV...")
count = analyzer.load_from_csv()
print(f"✓ Loaded {count} connections into database")

print("\nLoading all connections from database...")
analyzer.load_all_connections()
print(f"✓ Total connections in memory: {len(analyzer.connections)}")

print("\nAnalyzing network...")
insight = analyzer.analyze_network()

print("\nExporting to Excel...")
analyzer.export_to_excel()

print("\n✓ Done! Check exports/connections_enriched.xlsx")
