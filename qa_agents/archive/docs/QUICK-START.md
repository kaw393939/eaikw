# Visual UX Review - Quick Start Guide

## TL;DR

```bash
# Full-page review (Phase 1)
PYTHONPATH=. qa_agents/venv/bin/python3 qa_agents/visual_ux_review.py _site

# Section-based review (Phase 2) - NEW!
PYTHONPATH=. qa_agents/venv/bin/python3 qa_agents/section_review.py _site desktop
```

## What's New in Phase 2

### Section-Based Analysis
- **Above-fold**: First impression, value prop, primary CTA
- **Mid-page**: Content flow, scanability, engagement
- **Footer**: Contact info, legal links, trust signals

### Benefits
- Same cost as full-page (~$0.01)
- 3x more detailed feedback
- Severity ratings (Critical/Major/Minor)
- Actionable quick wins per section

## Example Output

```
🔍 First Impression Specialist - ABOVE-FOLD

**Strengths**
1. Clear value proposition
2. Clean navigation structure

**Issues**
1. Primary CTA not distinct (Critical)
2. Hero lacks imagery (Major)

**Quick Wins**
1. Transform link to button with contrast color
2. Add illustrative graphic to hero
```

## All Commands

```bash
# Phase 1: Full-page with 2 personas × 3 viewports
PYTHONPATH=. qa_agents/venv/bin/python3 qa_agents/visual_ux_review.py _site

# Phase 2: Desktop sections
PYTHONPATH=. qa_agents/venv/bin/python3 qa_agents/section_review.py _site desktop

# Phase 2: Mobile sections
PYTHONPATH=. qa_agents/venv/bin/python3 qa_agents/section_review.py _site mobile

# Run tests
PYTHONPATH=. qa_agents/venv/bin/python3 qa_agents/test_phase1.py
PYTHONPATH=. qa_agents/venv/bin/python3 qa_agents/test_phase2.py
```

## Cost Comparison

| Mode | Analyses | Cost | Feedback Detail |
|------|----------|------|----------------|
| Phase 1 (Full) | 6 (2 personas × 3 viewports) | $0.019 | Generic |
| Phase 2 (Desktop) | 3 sections | $0.0095 | Targeted |
| Phase 2 (All viewports) | 9 (3 sections × 3 viewports) | $0.0285 | Comprehensive |

## Documentation

- **Phase 1**: `PHASE-1-COMPLETION.md` - Bulletproof infrastructure
- **Phase 2**: `PHASE-2-COMPLETION.md` - Section-based analysis
- **Strategy**: `VISUAL_UX_STRATEGY.md` - Full 3-phase plan
- **Full README**: `README.md` - Complete LLM quality gate system
