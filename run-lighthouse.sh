#!/bin/bash
# Run Lighthouse audits on the built site

cd "$(dirname "$0")"

echo "🔨 Building site..."
python3 build.py

echo ""
echo "🌐 Starting test server..."
cd docs
python3 -m http.server 8085 > /dev/null 2>&1 &
SERVER_PID=$!
cd ..

# Wait for server to start
sleep 2

echo "🔍 Running Lighthouse audit..."
lighthouse http://localhost:8085 \
  --output html \
  --output json \
  --output-path ./lighthouse-report \
  --only-categories=performance,accessibility,best-practices,seo \
  --quiet

# Extract scores
echo ""
echo "📊 Lighthouse Scores:"
python3 << 'EOF'
import json
try:
    with open('lighthouse-report.report.json') as f:
        data = json.load(f)
    cats = data['categories']
    
    scores = {
        'Performance': cats['performance']['score'] * 100,
        'Accessibility': cats['accessibility']['score'] * 100,
        'Best Practices': cats['best-practices']['score'] * 100,
        'SEO': cats['seo']['score'] * 100
    }
    
    for name, score in scores.items():
        emoji = '✅' if score == 100 else '⚠️' if score >= 90 else '❌'
        print(f"  {emoji} {name}: {score:.0f}")
    
    # Check for issues
    print("\n🔍 Issues Found:")
    for cat_id, cat in cats.items():
        audit_refs = cat.get('auditRefs', [])
        for ref in audit_refs:
            audit = data['audits'].get(ref['id'], {})
            if audit.get('score') is not None and audit['score'] < 1:
                print(f"  ⚠️  {audit.get('title', ref['id'])}")
                if 'details' in audit and 'items' in audit['details']:
                    for item in audit['details']['items'][:2]:
                        if 'text' in item:
                            print(f"     - {item.get('text', '')[:60]}")
except Exception as e:
    print(f"Error reading report: {e}")
EOF

# Clean up
echo ""
echo "🧹 Stopping test server..."
kill $SERVER_PID 2>/dev/null

echo ""
echo "✅ Report saved to: lighthouse-report.report.html"
echo "   Open with: open lighthouse-report.report.html"
