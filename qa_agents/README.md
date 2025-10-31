# QA Agents System

> **Multi-device responsive UX review with specialized AI expert agents**

Automated quality assurance using OpenAI's Agents SDK with a consensus-based
approach to identify critical UX issues across all device sizes.

## Overview

```
┌──────────────────┐
│ Responsive Review│  Captures screenshots at 7 device sizes
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Consensus System │  7 expert agents analyze each screenshot
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Unified Report   │  Aggregated findings with severity + consensus
└──────────────────┘
```

**Key Innovation:** Multiple expert perspectives create consensus-based feedback
that's more reliable than single-agent reviews.

## Architecture

See **[ARCHITECTURE.md](ARCHITECTURE.md)** for complete system design, data
flow, and best practices.

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js (for development server)
- OpenAI API key

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Configure API key
cp ../.env.example ../.env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here
```

### Run Review

**Option A: Optimized Pipeline (Recommended - 70% Cost Savings)**

```bash
# Start development server first (separate terminal)
cd ..
npm start

# Run optimized review with triage + sequential experts
python run_optimized_review.py --auto-confirm
```

- **Cost:** ~$0.16-0.21 per review
- **Output:** Human-readable `.md` + machine-readable `.json`
- **Features:** Smart triage, sequential expert chain, cross-device patterns

**Option B: Original Parallel Pipeline**

```bash
# Run all 49 reviews in parallel (faster but more expensive)
python run_responsive_review.py
```

- **Cost:** ~$0.73 per review
- **Output:** Consensus markdown report

## What You Get

### 7 Device Configurations

- 📱 **Mobile Portrait** (375×812) - iPhone SE
- 📱 **Mobile Landscape** (812×375)
- 📱 **Tablet Portrait** (768×1024) - iPad
- 📱 **Tablet Landscape** (1024×768)
- 💻 **Laptop** (1440×900) - MacBook Pro
- 🖥️ **Desktop** (1920×1080) - Standard monitor
- 🖥️ **Wide Desktop** (2560×1440) - 2K display

### 7 Expert Agents

Each agent has specialized knowledge:

1. **Typography Expert** - Font sizes, readability, hierarchy
2. **Layout Expert** - Spacing, alignment, above-the-fold content
3. **Contrast Expert** - WCAG AA compliance (4.5:1 ratios)
4. **Hierarchy Expert** - Information architecture, visual weight
5. **Accessibility Expert** - ARIA, keyboard nav, screen readers
6. **Conversion Expert** - CTAs, user journey, friction points
7. **Brand Expert** - Design system consistency

### Comprehensive Reports

Output includes:

- 📊 JSON data (machine-readable)
- 📄 Text report (human-readable)
- 📸 Screenshots (all devices)
- 🎯 Severity ratings (critical/important/minor)
- 🌐 Cross-device issue detection
- 💡 Prioritized recommendations

## Usage

### Basic Workflow

```bash
# 1. Start development server
cd ..
docker-compose up web
# OR: npm start

# 2. Run responsive review (captures + analyzes)
python run_responsive_review.py

# 3. Check results
cat screenshots/YYYY-MM-DD-HH-MM-SS/RESPONSIVE-REVIEW-REPORT.txt
```

### Advanced Usage

**Re-analyze existing screenshots (fast):**

```bash
python run_consensus_review.py
```

**Docker integration:**

```bash
# Run QA system in Docker container
docker-compose run --rm qa python run_responsive_review.py
```

**Custom configuration:** Edit `config.py` for:

- Model selection (default: gpt-4o-mini)
- Cost tracking settings
- Output paths

## Understanding Results

### Severity Levels

**🔴 Critical** - Mentioned by 3+ experts

- Hero below the fold (not visible without scroll)
- WCAG AA failures (contrast < 4.5:1)
- Typography below 14px minimum
- Navigation taking >15% viewport height
- Design system violations (glassmorphism, wrong colors)

**🟡 Important** - Mentioned by 2 experts

- Inconsistent spacing
- Hierarchy problems
- Suboptimal CTAs
- Mobile-specific issues

**🔵 Minor** - Single expert observation

- Refinement opportunities
- Nice-to-have improvements
- Stylistic preferences

### Cross-Device Issues

Issues appearing across multiple device sizes indicate systemic problems:

- Mobile + Tablet = Touch interface problem
- Laptop + Desktop = Large screen optimization needed
- All devices = Fundamental design flaw

### Consensus Scoring

**High Consensus (3+ experts agree):**

- These are your highest priority fixes
- Multiple perspectives confirm the issue
- Likely visible to end users

**Medium Consensus (2 experts agree):**

- Important but not critical
- May depend on context
- Review and decide

**Low Consensus (1 expert only):**

- Refinement opportunities
- May be edge cases
- Consider for future iterations
- Optional improvements

## Cost Optimization

**Full Responsive Review:**

- 7 devices × 7 experts = 49 reviews
- ~1500 tokens per review
- gpt-4o-mini: $0.15 per 1M input tokens, $0.60 per 1M output
- **Total: ~$0.73 per full review**

**Strategic Usage:**

- Run on major changes (not every commit)
- Use consensus review for iterations (~$0.10)
- Set up monthly budget alerts in OpenAI dashboard

**Cost Comparison:**

- gpt-4o-mini (current): $0.73 per review
- gpt-4o: ~$48 per review (65x more expensive)
- Manual QA: Hours of human time

## File Structure

```
qa_agents/
├── run_responsive_review.py    # Primary entry point
├── run_consensus_review.py     # Re-analyze existing screenshots
├── responsive_review.py         # Multi-device capture system
├── consensus_review.py          # Expert aggregation
├── expert_agents.py             # 7 specialized agents
├── config.py                    # Configuration
├── requirements.txt             # Dependencies
├── Dockerfile.qa                # Docker container config
├── ARCHITECTURE.md              # System design docs
├── README.md                    # This file
├── screenshots/                 # Output directory
└── archive/                     # Legacy code (preserved)
```

## Configuration

Edit `config.py`:

```python
# Model selection
LLM_MODEL = "gpt-4o-mini"  # Cost-effective default

# Cost tracking
ENABLE_COST_TRACKING = True
COST_PER_1M_INPUT_TOKENS = 0.15
COST_PER_1M_OUTPUT_TOKENS = 0.60

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
```

## Troubleshooting

**"Cannot connect to browser":**

```bash
playwright install chromium
```

**"No screenshots found":**

```bash
# Run responsive review first
python run_responsive_review.py
```

**"OpenAI API Error":**

```bash
# Check API key
echo $OPENAI_API_KEY

# Verify .env file
cat ../.env | grep OPENAI_API_KEY
```

**"Port 8080 connection refused":**

```bash
# Start development server first
cd .. && npm start
# OR use Docker
docker-compose up web
```

**Review seems incomplete:**

```bash
# Check expert_agents.py for all 7 agents
# Verify consensus_review.py includes all experts
grep "EXPERT_AGENTS" expert_agents.py
```

# Switch to gpt-4o-mini in .env

LLM_MODEL=gpt-4o-mini

````

## Examples

### Successful Commit

### Example Output

```text
### RESPONSIVE REVIEW SYSTEM
📸 Capturing screenshots across 7 devices...

Device: mobile-portrait (375×812)       ✓
Device: mobile-landscape (812×375)      ✓
Device: tablet-portrait (768×1024)      ✓
Device: tablet-landscape (1024×768)     ✓
Device: laptop (1440×900)               ✓
Device: desktop (1920×1080)             ✓
Device: wide-desktop (2560×1440)        ✓

======================================================================
🤖 Running 7 expert agents on 7 devices (49 total reviews)...

Expert: Typography Expert               ✓ (7/7 devices)
Expert: Layout Expert                   ✓ (7/7 devices)
Expert: Contrast Expert                 ✓ (7/7 devices)
Expert: Hierarchy Expert                ✓ (7/7 devices)
Expert: Accessibility Expert            ✓ (7/7 devices)
Expert: Conversion Expert               ✓ (7/7 devices)
Expert: Brand Expert                    ✓ (7/7 devices)

### CONSENSUS RESULTS

🔴 CRITICAL ISSUES (3+ expert consensus):
   1. Hero section below fold on mobile-portrait
      └─ Mentioned by: Layout, Hierarchy, Conversion (3 experts)
      └─ Navigation takes 18% of viewport (>15% threshold)
      └─ Fix: Reduce nav height or increase hero prominence

   2. Contrast ratio 3.2:1 on .hero-subtitle
      └─ Mentioned by: Contrast, Accessibility, Brand (3 experts)
      └─ WCAG AA requires 4.5:1 minimum
      └─ Fix: Change color from #888 to #666

🟡 IMPORTANT ISSUES (2 expert consensus):
   3. Inconsistent spacing in .stats-grid
      └─ Mentioned by: Layout, Brand (2 experts)
      └─ Desktop: 40px gap, Mobile: 20px gap (no responsive logic)
      └─ Fix: Use CSS custom properties for consistent scaling

🌐 CROSS-DEVICE ISSUES:
   • Typography scale breaks on tablet-landscape
   • CTA buttons too small on all mobile devices (<44px touch target)
````

### Optimized Pipeline Output

The optimized pipeline generates TWO complementary reports:

**1. Human-Readable Report** (`REVIEW-{timestamp}.md`)

```markdown
# UX Review Report

**Generated:** 2025-10-30-14-30-00

## 📊 Executive Summary

- **Devices Reviewed:** 4 (3 skipped as similar)
- **Critical Issues:** 8
- **Important Issues:** 12

---

## 🔴 ACTION REQUIRED: Critical Issues

### 1. Hero section not visible on mobile without scrolling

- **Device(s):** mobile-portrait, mobile-landscape
- **Confidence:** 5/7 experts agree (Layout, Hierarchy, Conversion,
  Accessibility, Brand)
- **Why it matters:** First-time visitors never see main value proposition
- **How to fix:** Reduce nav height from 80px to 60px on mobile OR increase hero
  min-height to 100vh

### 2. Call-to-action buttons fail WCAG AA touch target size

- **Device(s):** mobile-portrait, mobile-landscape, tablet-portrait
- **Confidence:** 4/7 experts agree (Accessibility, Conversion, Layout, UX)
- **Why it matters:** 44px minimum for accessible touch targets, current is 36px
- **How to fix:** Update .cta-button padding: 12px 24px → 14px 32px (CSS
  line 342)

---

## 🌐 Cross-Device Patterns

### Universal (All Devices)

- Contrast ratio failures on `.hero-subtitle` (3.2:1, needs 4.5:1)
- Inconsistent spacing in `.stats-grid`

### Mobile-Only

- Hero below fold (navigation too tall)
- Touch targets too small (<44px)

### Desktop-Only

- Excessive whitespace in sidebar (could show more content)

---

## 🚀 Recommended Fix Order

1. **Universal issues first** (affects all devices, widest impact)
   - Fix contrast ratios
   - Standardize spacing system

2. **Mobile-critical issues** (majority of users)
   - Hero visibility
   - Touch target sizes

3. **Desktop refinements** (optimization)
   - Sidebar spacing
   - Typography scale
```

**2. Machine-Readable Report** (`REVIEW-{timestamp}.json`)

```json
{
  "timestamp": "2025-10-30-14-30-00",
  "executive_summary": {
    "total_devices_reviewed": 4,
    "critical_issues": 8,
    "important_issues": 12,
    "devices_skipped": ["tablet-landscape", "laptop", "wide-desktop"],
    "skip_reason": "Similar to desktop"
  },
  "device_summaries": {
    "mobile-portrait": {
      "critical_issues": ["Hero below fold", "CTA buttons too small"],
      "important_issues": [
        "Typography scale inconsistent",
        "Card spacing irregular"
      ],
      "expert_agreement": {
        "Hero below fold": 5,
        "CTA buttons too small": 4
      }
    }
  },
  "cross_device_patterns": {
    "universal_issues": [
      "Contrast ratio 3.2:1 on .hero-subtitle (needs 4.5:1)"
    ],
    "mobile_only": ["Hero below fold", "Touch targets <44px"],
    "desktop_only": ["Excessive sidebar whitespace"],
    "responsive_breakpoint_issues": [
      "Typography scale breaks at 768px breakpoint"
    ],
    "recommended_fix_order": [
      "Fix universal contrast issues (all devices)",
      "Fix mobile hero visibility (highest priority)",
      "Standardize spacing system (reduces future issues)",
      "Optimize desktop layout (lower priority)"
    ]
  },
  "actionable_issues": [
    {
      "id": "MOBILE-001",
      "title": "Hero section below fold on mobile",
      "severity": "CRITICAL",
      "confidence": 5,
      "devices_affected": ["mobile-portrait", "mobile-landscape"],
      "description": "Navigation takes 80px (21% of viewport), pushing hero below fold",
      "why_it_matters": "First-time mobile visitors (60% of traffic) never see value proposition without scrolling",
      "how_to_fix": "Reduce .navbar height to 60px on mobile OR set .hero min-height: 100vh",
      "file_locations": [
        "src/assets/css/main.css:156 (.navbar)",
        "src/assets/css/main.css:342 (.hero)"
      ],
      "expert_consensus": {
        "layout_expert": true,
        "hierarchy_expert": true,
        "conversion_expert": true,
        "accessibility_expert": true,
        "brand_expert": true,
        "typography_expert": false,
        "contrast_expert": false
      }
    }
  ]
}
```

**Key Benefits:**

- ✅ **Humans** can quickly scan `.md` for priorities
- ✅ **AI agents** can parse `.json` to automatically generate fixes
- ✅ **CI/CD** can track issue counts over time
- ✅ **Project managers** get executive summary
- ✅ **Developers** get specific file locations and fix instructions

## Learn More

- 📖 **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete system design, data flow,
  best practices
- 📊 **[TECHNICAL-DEBT-AUDIT-2024.md](TECHNICAL-DEBT-AUDIT-2024.md)** - Recent
  cleanup and architecture evolution
- 🚀 **[Main Project README](../README.md)** - Full course documentation and
  lessons

## Contributing

When extending the system:

1. **Keep experts focused** - Each expert should have ONE specialty
2. **Use structured output** - Always use Pydantic models for responses
3. **Test across devices** - Verify changes work on all 7 viewports
4. **Document prompt changes** - Explain why expert instructions changed
5. **Archive, don't delete** - Move deprecated code to `archive/`

## License

MIT License - Part of the AI-Assisted Web Development Learning Platform
