# Visual UX Review with GPT-4o Vision

Automated UX analysis using GPT-4o Vision API with persona-based think-aloud protocol.

## Overview

The Visual UX Review system captures screenshots of your website at multiple viewports and analyzes them using GPT-4o Vision with different user personas. Each persona provides detailed think-aloud feedback simulating real user experiences.

## Features

- **Multi-Viewport Analysis**: Desktop (1920×1080), Tablet (768×1024), Mobile (375×667)
- **Persona-Based Reviews**:
  - First-Year Student (tech beginner, visual learner)
  - Instructor (expert validator, accessibility focus)
- **Think-Aloud Protocol**: Detailed commentary on first impressions, usability, design
- **GPT-4o Vision**: Advanced image analysis with ~$0.01 per screenshot
- **Structured Output**: Consistent ratings (excellent/good/needs_improvement/poor)

## Quick Start

### 1. Prerequisites

```bash
# Make sure your site is built and running
npm run build
npm start  # Serves at http://localhost:8080
```

### 2. Run Visual UX Review

```bash
# In a new terminal
qa_agents/venv/bin/python3 qa_agents/visual_ux_review.py
```

### 3. Review Output

The script will:
1. Capture screenshots at 3 viewports (desktop, tablet, mobile)
2. Analyze with 2 personas = 6 total reviews
3. Print detailed feedback for each review
4. Generate overall verdict (EXCELLENT/GOOD/NEEDS_IMPROVEMENT)

Example output:
```
📸 Capturing screenshots from http://localhost:8080...
   ✅ Captured 3 screenshots
   💾 Saved to qa_agents/screenshots/

🤔 Analyzing with first_year_student at desktop (1920x1080)...

======================================================================
🎭 Persona: FIRST_YEAR_STUDENT
📱 Viewport: DESKTOP
⭐ Rating: GOOD
======================================================================

Overall Impression:
The website feels welcoming and professional. The hero section...

🔍 Specific Observations:
  • Large heading text is easy to read
  • Navigation menu is clearly visible in top right
  • Color scheme is pleasant (blue/white)

⚠️  Usability Concerns:
  • Call-to-action button could be more prominent
  • Some text sections feel dense

♿ Accessibility Notes:
  • Good color contrast on main text
  • Heading hierarchy appears clear

🎨 Design Feedback:
  • Consider increasing button size for mobile users
  • Add more whitespace between sections

💭 Reasoning:
Overall good user experience with minor improvements needed...

💰 Estimated cost: $0.0506
```

## Configuration

### Environment Variables

In `.env`:
```bash
OPENAI_API_KEY=sk-...
SITE_URL=http://localhost:8080  # URL to analyze
```

### Customize Personas/Viewports

Edit `qa_agents/visual_ux_review.py`:

```python
result = run_visual_ux_review(
    site_url="http://localhost:8080",
    personas=["first_year_student", "instructor"],  # Choose personas
    viewports=["desktop", "tablet", "mobile"]  # Choose viewports
)
```

## Cost Estimation

**GPT-4o Vision Pricing** (as of 2025):
- ~$10 per 1M input tokens
- 1 screenshot ≈ 765 tokens
- 1 prompt ≈ 500 tokens
- **Total per analysis**: ~$0.012

**Full run (6 analyses)**:
- 3 viewports × 2 personas = 6 analyses
- **Cost**: ~$0.05-0.07 per commit

**Optimization Options**:
1. Run only on HTML/CSS changes (not every commit)
2. Use fewer viewports (desktop only = $0.02)
3. Use one persona (student or instructor = $0.03)

## Integration with Quality Gate

To run automatically with quality checks:

```bash
# Option 1: Run both quality checks together
npm run quality-check

# Option 2: Add to pre-commit hook (in .husky/pre-commit)
npm run build
qa_agents/venv/bin/python3 qa_agents/visual_ux_review.py
```

## Personas

### First-Year Student
- **Profile**: 18-19 years old, basic tech skills, visual learner
- **Focus**: First impressions, clarity, ease of understanding
- **Concerns**: "Is this too hard?", "Where do I find help?"
- **Language**: Casual, honest, beginner-friendly

### Instructor
- **Profile**: 10+ years teaching, expert in web standards
- **Focus**: Accessibility, pedagogy, technical excellence
- **Standards**: WCAG 2.1 AA, responsive design, clear hierarchy
- **Language**: Professional, standards-based, actionable

## Output Structure

Each review includes:

```python
{
    "persona": "first_year_student",
    "viewport": "desktop",
    "overall_impression": "...",
    "specific_observations": ["...", "..."],
    "usability_concerns": ["...", "..."],
    "accessibility_notes": ["...", "..."],
    "design_feedback": ["...", "..."],
    "recommendation": "good",  # excellent/good/needs_improvement/poor
    "reasoning": "..."
}
```

## Troubleshooting

### Site Not Running
```bash
# Error: Failed to capture screenshots
# Solution: Start the dev server first
npm start
# Then in new terminal:
qa_agents/venv/bin/python3 qa_agents/visual_ux_review.py
```

### Playwright Not Installed
```bash
qa_agents/venv/bin/pip install playwright
qa_agents/venv/bin/playwright install chromium
```

### OpenAI API Errors
```bash
# Check .env file has valid key
cat .env | grep OPENAI_API_KEY

# Test API key
qa_agents/venv/bin/python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

## Advanced Usage

### Analyze Specific URL
```python
run_visual_ux_review(site_url="http://localhost:3000/about")
```

### Save Screenshots Only
```python
from qa_agents.screenshot_utils import capture_all_viewports_sync

screenshots = capture_all_viewports_sync(
    url="http://localhost:8080",
    output_dir="qa_agents/screenshots"
)
```

### Programmatic Access
```python
from qa_agents.visual_ux_review import run_visual_ux_review

result = run_visual_ux_review(
    site_url="http://localhost:8080",
    personas=["instructor"],  # Single persona
    viewports=["desktop"]  # Single viewport
)

print(f"Verdict: {result['verdict']}")
print(f"Cost: ${result['cost']:.4f}")

for review in result['reviews']:
    print(f"{review.persona} @ {review.viewport}: {review.recommendation}")
```

## Tips for Best Results

1. **Run on built site**: Always `npm run build` before analyzing
2. **Test real content**: Use production-like content, not Lorem ipsum
3. **Check all viewports**: Mobile issues often missed on desktop
4. **Read the reasoning**: LLM provides detailed explanations
5. **Iterate**: Fix issues and re-run to validate improvements

## Example Workflow

```bash
# 1. Make changes to your site
vim src/index.njk

# 2. Build
npm run build

# 3. Start server (in one terminal)
npm start

# 4. Run visual review (in another terminal)
qa_agents/venv/bin/python3 qa_agents/visual_ux_review.py

# 5. Review feedback and iterate
# ... make improvements ...

# 6. Re-run to validate
qa_agents/venv/bin/python3 qa_agents/visual_ux_review.py
```

## Next Steps

- [ ] Add more personas (international student, instructor evaluating accessibility)
- [ ] Integrate with pre-commit hook
- [ ] Add comparison mode (before/after screenshots)
- [ ] Export reports to HTML/PDF
- [ ] Add screenshot diffing for visual regression testing
