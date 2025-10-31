# 🚀 Quick Start: Optimized Review System

## 5-Minute Setup

### Step 1: Prerequisites Check

```bash
# Check Python version (need 3.12+)
python --version

# Check Node.js (need for dev server)
node --version

# Check OpenAI API key
echo $OPENAI_API_KEY
```

### Step 2: Install Dependencies

```bash
# From project root
cd /Users/kwilliams/Desktop/117_site

# Install Python dependencies
pip install -r qa_agents/requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Step 3: Start Dev Server

```bash
# Terminal 1: Start the web server
npm start

# Wait for: "Server running on http://localhost:8080"
```

### Step 4: Run Optimized Review

```bash
# Terminal 2: Run the review
python qa_agents/run_optimized_review.py --auto-confirm
```

**Expected Output:**

```
🚀 STARTING OPTIMIZED REVIEW PROCESS
══════════════════════════════════════════════════════════════════════

💰 COST ESTIMATE:
  - Phase 1 Triage: ~$0.03
  - Phase 2-3 Expert Review: ~$0.10-0.15
  - Phase 4 Pattern Detection: ~$0.03
  - TOTAL: ~$0.16-0.21 (vs $0.73 for parallel)

📸 CAPTURING SCREENSHOTS
══════════════════════════════════════════════════════════════════════
Device: mobile-portrait (375×812)       ✓
Device: mobile-landscape (812×375)      ✓
...

🎯 PHASE 1: TRIAGE
══════════════════════════════════════════════════════════════════════
Screening mobile-portrait... 🔴 CRITICAL
Screening tablet-landscape... ⏭️ SKIP_SIMILAR
...

🔍 PHASE 2-3: EXPERT REVIEW + SUMMARIZATION
══════════════════════════════════════════════════════════════════════
📱 Reviewing mobile-portrait...
  ✓ layout_expert
  ✓ typography_expert
  ...

🌐 PHASE 4: CROSS-DEVICE PATTERN DETECTION
══════════════════════════════════════════════════════════════════════

📊 PHASE 5: GENERATING REPORTS
══════════════════════════════════════════════════════════════════════

✅ REVIEW COMPLETE
══════════════════════════════════════════════════════════════════════

📖 Read the report: qa_agents/screenshots/optimized_review/REVIEW-2025-10-30-14-30-00.md
💰 Estimated cost: $0.15-0.25 (vs $0.73 parallel)
```

### Step 5: Review Results

```bash
# Human-readable report
open qa_agents/screenshots/optimized_review/REVIEW-*.md

# Machine-readable JSON
cat qa_agents/screenshots/optimized_review/REVIEW-*.json | jq '.'
```

---

## What You'll See

### Human Report (Markdown)

```markdown
# UX Review Report

**Generated:** 2025-10-30-14-30-00

## 📊 Executive Summary

- **Devices Reviewed:** 4 (3 skipped as similar)
- **Critical Issues:** 3
- **Important Issues:** 7

## 🔴 ACTION REQUIRED: Critical Issues

### 1. Hero section not visible on mobile without scrolling

- **Device(s):** mobile-portrait, mobile-landscape
- **Confidence:** 5/7 experts agree
- **Why it matters:** 60% of users on mobile never see value prop
- **How to fix:** Reduce .navbar height from 80px to 60px
- **File:** src/assets/css/main.css:156

### 2. Call-to-action buttons too small (accessibility)

- **Device(s):** mobile-portrait, mobile-landscape, tablet-portrait
- **Confidence:** 4/7 experts agree
- **Why it matters:** WCAG requires 44×44px touch targets
- **How to fix:** Increase .cta-button padding: 12px 24px → 14px 32px
- **File:** src/assets/css/main.css:342
```

### Machine Report (JSON)

```json
{
  "timestamp": "2025-10-30-14-30-00",
  "executive_summary": {
    "total_devices_reviewed": 4,
    "critical_issues": 3,
    "important_issues": 7
  },
  "actionable_issues": [
    {
      "id": "MOBILE-001",
      "title": "Hero below fold on mobile",
      "severity": "CRITICAL",
      "confidence": 5,
      "devices_affected": ["mobile-portrait", "mobile-landscape"],
      "why_it_matters": "60% of users never see value prop",
      "how_to_fix": "Reduce .navbar height to 60px",
      "file_locations": ["src/assets/css/main.css:156"]
    }
  ],
  "cross_device_patterns": {
    "universal_issues": ["Contrast ratio 3.2:1"],
    "mobile_only": ["Hero below fold"],
    "recommended_fix_order": ["Fix universal first"]
  }
}
```

---

## Next Steps

### Option 1: Fix Issues Manually

```bash
# Open the CSS file
code src/assets/css/main.css

# Jump to line 156 (hero issue)
# Make the change: .navbar { height: 60px; }

# Rebuild and verify
npm run build
```

### Option 2: Auto-Generate Fixes with AI

```bash
# Use the JSON to generate fixes
python qa_agents/auto_fix_generator.py \
  --report qa_agents/screenshots/optimized_review/REVIEW-*.json \
  --output src/assets/css/fixes.css

# Review and apply
git diff src/assets/css/
```

### Option 3: Track Progress Over Time

```bash
# Run review weekly, compare results
python qa_agents/run_optimized_review.py --auto-confirm

# Track improvements
python qa_agents/compare_reports.py \
  --baseline REVIEW-2025-10-23-*.json \
  --current REVIEW-2025-10-30-*.json

# Output:
# 🎉 Critical issues: 8 → 3 (62% improvement)
# 🎉 Important issues: 12 → 7 (42% improvement)
```

---

## Troubleshooting

### "Cannot connect to browser"

```bash
# Install Playwright
playwright install chromium

# Verify installation
playwright --version
```

### "Connection refused to localhost:8080"

```bash
# Check if server is running
curl -I http://localhost:8080/

# If not, start it
npm start

# Wait for: "Server running on http://localhost:8080"
```

### "OpenAI API Error"

```bash
# Check API key is set
echo $OPENAI_API_KEY

# If empty, set it
export OPENAI_API_KEY=sk-your-key-here

# Or add to .env file
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
```

### "No screenshots found"

```bash
# This shouldn't happen (screenshots auto-captured)
# But if it does, check directory
ls -la qa_agents/screenshots/optimized_review/

# Manually capture screenshots
python qa_agents/responsive_review.py
```

---

## Cost Monitoring

### Track Token Usage

```bash
# View cost breakdown
cat qa_agents/screenshots/optimized_review/REVIEW-*.json | \
  jq '.token_usage'

# Expected output:
# {
#   "total_tokens": 20000,
#   "estimated_cost": 0.20,
#   "phase_breakdown": {
#     "triage": 2100,
#     "expert_review": 8800,
#     "summarization": 4000,
#     "pattern_detection": 2000
#   }
# }
```

### Set Budget Alerts

```bash
# Alert if review exceeds budget
python qa_agents/check_budget.py \
  --max-cost-per-review 0.30 \
  --report REVIEW-*.json

# Output: ✅ Cost $0.20 is within budget $0.30
```

---

## Compare with Parallel Pipeline

### Run Both Pipelines

```bash
# Optimized (recommended)
python qa_agents/run_optimized_review.py --auto-confirm

# Parallel (original)
python qa_agents/run_responsive_review.py
```

### Compare Results

```bash
# Show differences
diff \
  qa_agents/screenshots/optimized_review/REVIEW-*.md \
  qa_agents/screenshots/responsive_review/CONSENSUS-*.md

# Compare costs
echo "Optimized: ~$0.20"
echo "Parallel: ~$0.73"
echo "Savings: 73%"
```

### Compare Quality

**Optimized Output:**

```
Critical Issue: Hero below fold
- Confidence: 5/7 experts (layout, hierarchy, conversion, accessibility, brand)
- Fix: Reduce .navbar height to 60px (src/assets/css/main.css:156)
- Pattern: Mobile-only issue (not on desktop)
```

**Parallel Output:**

```
Critical Issue: Hero section below fold on mobile-portrait
- Mentioned by: Layout, Hierarchy, Conversion (3 experts)
- Fix: [Not specified]
- Pattern: [Not analyzed]
```

**Winner:** ✅ Optimized (more specific, actionable, with cross-device analysis)

---

## Integration Examples

### CI/CD (GitHub Actions)

```yaml
# .github/workflows/ux-review.yml
name: UX Quality Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r qa_agents/requirements.txt
          playwright install chromium

      - name: Start server
        run: npm start &

      - name: Run UX review
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python qa_agents/run_optimized_review.py --auto-confirm

      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: ux-review
          path: qa_agents/screenshots/optimized_review/
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "Running UX review..."
python qa_agents/run_optimized_review.py --auto-confirm

# Check if critical issues increased
CURRENT=$(cat qa_agents/screenshots/optimized_review/REVIEW-*.json | jq '.executive_summary.critical_issues')
BASELINE=$(cat qa_agents/screenshots/optimized_review/BASELINE.json | jq '.executive_summary.critical_issues')

if [ "$CURRENT" -gt "$BASELINE" ]; then
  echo "❌ Critical issues increased from $BASELINE to $CURRENT"
  echo "Review report and fix issues before committing"
  exit 1
fi

echo "✅ UX quality maintained"
```

### Weekly Scheduled Review

```bash
# crontab -e
0 9 * * 1 cd /Users/kwilliams/Desktop/117_site && python qa_agents/run_optimized_review.py --auto-confirm && mail -s "Weekly UX Review" dev@example.com < qa_agents/screenshots/optimized_review/REVIEW-*.md
```

---

## Documentation

- 📖 **[README.md](./README.md)** - Full system overview
- 🏗️ **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System design and data flow
- 📊 **[PIPELINE-COMPARISON.md](./PIPELINE-COMPARISON.md)** - Optimized vs
  Parallel comparison
- 📝 **[OPTIMIZED-SYSTEM-SUMMARY.md](./OPTIMIZED-SYSTEM-SUMMARY.md)** - Complete
  implementation details

---

## Support

**Questions?** Check the docs above or open an issue.

**Cost too high?** See [PIPELINE-COMPARISON.md](./PIPELINE-COMPARISON.md) for
optimization tips.

**Quality concerns?** Compare with parallel pipeline to verify results.

**Ready for production?** ✅ System is production-ready today.

---

## Summary

✅ **5-minute setup** ✅ **$0.20 per review** (73% savings) ✅ **Actionable JSON
output** (AI-parseable) ✅ **Cross-device patterns** (smart prioritization) ✅
**Production-ready** (use today)

**Get started now:**

```bash
python qa_agents/run_optimized_review.py --auto-confirm
```
