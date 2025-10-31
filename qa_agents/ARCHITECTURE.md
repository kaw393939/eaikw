# QA Agents Architecture

## Overview

The QA system uses a **multi-device responsive review** approach with
**specialized AI experts** that provide **consensus-based feedback**.

```
┌─────────────────────────────────────────────────────────────┐
│                    RESPONSIVE REVIEW                        │
│         (Multi-Device Screenshot Capture)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
           ┌─────────────────────────────┐
           │    7 Device Configurations  │
           ├─────────────────────────────┤
           │ • Mobile Portrait (375×812) │
           │ • Mobile Landscape          │
           │ • Tablet Portrait           │
           │ • Tablet Landscape          │
           │ • Laptop (1440×900)         │
           │ • Desktop (1920×1080)       │
           │ • Wide Desktop (2560×1440)  │
           └─────────────┬───────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   CONSENSUS REVIEW                          │
│         (Aggregate Expert Findings)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
           ┌─────────────────────────────┐
           │    7 Expert Reviewers       │
           ├─────────────────────────────┤
           │ • Typography Expert         │
           │ • Layout Expert             │
           │ • Contrast Expert           │
           │ • Hierarchy Expert          │
           │ • Accessibility Expert      │
           │ • Conversion Expert         │
           │ • Brand Expert              │
           └─────────────┬───────────────┘
                         │
                         ▼
           ┌─────────────────────────────┐
           │   Unified Report Output     │
           │   • Critical Issues         │
           │   • Cross-Device Problems   │
           │   • Actionable Fixes        │
           └─────────────────────────────┘
```

## System Components

### 1. Entry Points

**`run_responsive_review.py`** (97 lines)

- Primary CLI entry point
- Coordinates multi-device screenshot capture
- Invokes consensus review system
- Generates comprehensive reports

**`run_consensus_review.py`** (126 lines)

- Secondary CLI for existing screenshots
- Re-runs expert analysis without re-capturing
- Useful for iterating on reviews

### 2. Core Systems

**`responsive_review.py`** (393 lines)

- Multi-device screenshot capture using Playwright
- 7 device configurations covering mobile → 4K desktop
- Async screenshot orchestration
- Cross-device issue identification

**`consensus_review.py`** (297 lines)

- Aggregates findings from all expert agents
- Runs 7 experts in parallel for each device/screenshot
- Combines reviews into unified report
- Identifies consensus issues vs. individual concerns

**`expert_agents.py`** (489 lines)

- 7 specialized AI reviewers with distinct perspectives
- Recently enhanced with above-the-fold viewport detection
- Each expert has specific evaluation criteria:
  - **Typography Expert**: Readability, hierarchy, scale
  - **Layout Expert**: Spacing, alignment, above-the-fold
  - **Contrast Expert**: WCAG compliance, visibility
  - **Hierarchy Expert**: Information architecture, hero visibility
  - **Accessibility Expert**: ARIA, keyboard nav, screen readers
  - **Conversion Expert**: CTAs, user journey, friction points
  - **Brand Expert**: Design system consistency

### 3. Configuration

**`config.py`** (37 lines)

- Central configuration management
- OpenAI API settings (gpt-4o-mini by default)
- Cost tracking (~$0.15 per 1M tokens)
- Project paths and thresholds

## Data Flow

### Responsive Review Process

```
1. User runs: python run_responsive_review.py
2. System starts development server (or connects to Docker)
3. For each device configuration:
   a. Launch Playwright browser with device dimensions
   b. Navigate to site URL
   c. Capture full-page screenshot
   d. Save to screenshots/{timestamp}/{device}.png
4. Pass all screenshots to consensus_review
5. Generate unified report
```

### Consensus Review Process

```
1. Load all device screenshots
2. For each screenshot:
   a. Send to all 7 expert agents in parallel
   b. Each expert analyzes from their perspective
   c. Each returns structured review (issues + severity)
3. Aggregate all expert reviews:
   a. Identify issues mentioned by multiple experts
   b. Flag critical cross-device problems
   c. Prioritize by severity and consensus
4. Generate comprehensive report with:
   - Executive summary
   - Per-device findings
   - Cross-device issues
   - Actionable recommendations
```

## File Structure

### Active Production Code (7 files)

```
qa_agents/
├── run_responsive_review.py    # Primary CLI entry point
├── run_consensus_review.py     # Secondary CLI for re-review
├── responsive_review.py         # Multi-device screenshot system
├── consensus_review.py          # Expert consensus aggregation
├── expert_agents.py             # 7 specialized AI experts
├── config.py                    # Central configuration
└── requirements.txt             # Python dependencies
```

### Supporting Files

```
qa_agents/
├── Dockerfile.qa                # Docker QA container config
├── README.md                    # QA system documentation
├── ARCHITECTURE.md              # This file
├── TECHNICAL-DEBT-AUDIT-2024.md # Recent cleanup audit
├── screenshots/                 # Screenshot output directory
└── archive/                     # Archived legacy code
    └── docs/                    # Old documentation
```

## Technology Stack

- **Python 3.12+**: Core language
- **OpenAI Agents SDK**: AI agent framework
- **Playwright**: Browser automation for screenshots
- **GPT-4o-mini**: Cost-effective AI model (~$0.15/1M tokens)
- **Pydantic**: Structured output validation
- **asyncio**: Concurrent screenshot capture

## Cost Optimization

- **Model**: gpt-4o-mini (not gpt-4) saves ~98% on costs
- **Parallel Processing**: 7 experts run concurrently per device
- **Cost Estimation**: ~$0.73 for full 7-device × 7-expert review
- **Token Limits**: Efficient prompts to minimize token usage

## Running the System

### Option 1: Standard Python Environment

```bash
# Install dependencies
cd qa_agents
python -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt

# Run responsive review
python run_responsive_review.py
```

### Option 2: Docker (Recommended)

```bash
# Start development server
docker-compose up web

# Run QA agents in separate terminal
docker-compose run --rm qa python run_responsive_review.py
```

## Development Workflow

### Making Changes to Experts

1. Edit `expert_agents.py`
2. Modify the `instructions` field for the target expert
3. No restart needed - next review uses updated prompts

### Adding New Experts

1. Define new expert in `expert_agents.py`:
   ```python
   new_expert = Agent(
       name="New Expert Name",
       instructions="...",
       model="gpt-4o-mini",
       response_format=ExpertReview
   )
   ```
2. Add to `EXPERT_AGENTS` list
3. Consensus system automatically includes it

### Adjusting Device Configurations

Edit `responsive_review.py`:

```python
DEVICE_CONFIGS = {
    "custom-device": {
        "width": 1024,
        "height": 768,
        "name": "Custom Device"
    }
}
```

## Output Format

### Screenshot Directory Structure

```
qa_agents/screenshots/
└── 2024-12-23-14-30-45/
    ├── mobile-portrait.png
    ├── mobile-landscape.png
    ├── tablet-portrait.png
    ├── tablet-landscape.png
    ├── laptop.png
    ├── desktop.png
    ├── wide-desktop.png
    └── responsive-review-report.json
```

### Report JSON Structure

```json
{
  "timestamp": "2024-12-23T14:30:45",
  "devices_reviewed": 7,
  "experts_consulted": 7,
  "total_reviews": 49,
  "critical_issues": [...],
  "important_issues": [...],
  "cross_device_issues": [...],
  "device_specific": {
    "mobile-portrait": {
      "typography_expert": {...},
      "layout_expert": {...}
    }
  },
  "recommendations": [...]
}
```

## Architecture Evolution

### Phase 1: Quality Gate (Archived)

- Linear linting approach
- Generic quality agents
- Single-perspective review
- File: `archive/quality-gate-system/`

### Phase 2: Visual UX Review (Archived)

- Screenshot-based analysis
- Full-page viewports only
- Limited expert diversity
- Files: `archive/visual-ux-system/`

### Phase 3: Targeted Section Review (Archived)

- Element-specific capture
- HTML data-attribute discovery
- Section-by-section analysis
- Files: `archive/targeted-review-system/`

### Phase 4: Responsive Multi-Device (Current)

- 7 device configurations
- 7 specialized expert perspectives
- Consensus-based aggregation
- Cross-device issue detection
- Above-the-fold viewport awareness

## Best Practices

### 1. Run Reviews Before Major Changes

```bash
# Capture baseline before edits
python run_responsive_review.py > before.log

# Make changes to site
# ...

# Compare after changes
python run_responsive_review.py > after.log
diff before.log after.log
```

### 2. Focus on Critical Issues First

- Critical issues = mentioned by 3+ experts
- Cross-device issues = affects multiple viewports
- Above-the-fold issues = affects immediate visibility

### 3. Iterate with Consensus Review

```bash
# After fixing issues, re-analyze existing screenshots
python run_consensus_review.py
```

### 4. Monitor Costs

- Original parallel approach: ≈ $0.73 per review
- Optimized pipeline: ≈ $0.16-0.21 per review (70% savings)
- Run strategically (not on every commit)
- Use optimized pipeline for regular reviews

## Optimization Strategy

### Two Pipeline Options

**Option A: Optimized Sequential Pipeline (Recommended)**

```
Phase 1: TRIAGE (All Devices)
         ↓
Phase 2: SEQUENTIAL EXPERT CHAIN (Priority Devices)
         ↓
Phase 3: CONSENSUS SUMMARIZATION
         ↓
Phase 4: CROSS-DEVICE PATTERN DETECTION
         ↓
Phase 5: ACTIONABLE REPORT GENERATION
```

**Benefits:**

- 70% token reduction (73,500 → 20,000 tokens)
- 73% cost reduction ($0.73 → $0.20)
- Higher quality (experts build on each other)
- Smarter prioritization (skip similar devices)
- Better reports (human + machine readable)

**Token Breakdown:**

```
Phase 1: Triage (7 devices)        ~2,100 tokens  ($0.03)
Phase 2: Expert Chain (3-5 devices) ~5,600 tokens  ($0.08 per device)
Phase 3: Summarization             ~1,000 tokens  ($0.015 per device)
Phase 4: Pattern Detection         ~2,000 tokens  ($0.03)
Phase 5: Report Generation         Free (string formatting)
────────────────────────────────────────────────
TOTAL:                             ~15-20k tokens ($0.16-0.21)
```

**Option B: Original Parallel Pipeline**

```
7 Devices × 7 Experts = 49 Reviews (Parallel)
         ↓
Consensus Aggregation
         ↓
Markdown Report
```

**Tradeoffs:**

- Faster execution (2-3 min vs 3-4 min)
- More expensive ($0.73 vs $0.20)
- Redundant analysis (same issues described 49 times)
- No cross-device pattern detection

### Key Optimizations Implemented

**1. Triage-Based Prioritization**

- Quick scan identifies which devices need deep review
- Skips devices that look identical to others
- Example: If tablet-landscape = desktop, skip tablet-landscape
- Savings: 40-50% of devices can be skipped

**2. Sequential Expert Chain**

- Experts run in dependency order (Layout → Typography → Contrast → etc.)
- Each expert sees previous findings, builds on them
- Reduces redundancy: "I agree with Layout Expert" vs repeating full analysis
- Improves quality: Experts can validate/challenge each other

**3. Cross-Device Pattern Detection**

- Identifies universal issues (all devices)
- Flags mobile-specific vs desktop-specific problems
- Suggests fix order (widest impact first)
- Prevents fixing same issue 7 times

**4. Dual-Format Reports**

- Human-readable `.md` for quick scanning
- Machine-readable `.json` for AI automation
- Structured issues with IDs, severity, file locations
- Clear "why it matters" + "how to fix" for each issue

### When to Use Which Pipeline

**Use Optimized Pipeline When:**

- Regular reviews (weekly/monthly)
- Budget-conscious projects
- Want actionable JSON output for automation
- Need cross-device pattern analysis

**Use Parallel Pipeline When:**

- Quick validation needed (2 min vs 4 min matters)
- Only need markdown output
- Budget isn't a concern ($0.73 vs $0.20 doesn't matter)
- Testing new expert agent prompts (easier to see individual outputs)

## Troubleshooting

### "No screenshots found"

```bash
# Check screenshots directory
ls -la qa_agents/screenshots/

# Run responsive review first
python run_responsive_review.py
```

### "Cannot connect to browser"

```bash
# Install Playwright browsers
playwright install chromium

# Or use Docker (browsers pre-installed)
docker-compose run --rm qa python run_responsive_review.py
```

### "OpenAI API Error"

```bash
# Check API key
echo $OPENAI_API_KEY

# Or verify .env file
cat .env | grep OPENAI_API_KEY
```

## Contributing

When extending the system:

1. **Keep experts focused** - Each expert should have ONE specialty
2. **Use structured output** - Always use Pydantic models for responses
3. **Document prompt changes** - Explain why expert instructions changed
4. **Test across devices** - Verify changes work on all 7 viewports
5. **Archive legacy code** - Don't delete, move to `archive/`

## References

- [Main Project README](../README.md)
- [Technical Debt Audit 2024](./TECHNICAL-DEBT-AUDIT-2024.md)
- [Docker Development Guide](../DEVELOPMENT.md)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
