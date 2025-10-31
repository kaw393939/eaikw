# Quick Start: Data-Attribute Based UX Reviews

## Overview

The new system uses HTML data attributes to mark sections for UX review. This provides bulletproof, self-documenting screenshot capture.

## 1. Mark Sections in HTML

Add `data-ux-section` to elements you want reviewed:

```html
<!-- Critical sections -->
<header data-ux-section="header" data-ux-priority="critical">
  ...
</header>

<section data-ux-section="hero" data-ux-priority="critical">
  ...
</section>

<!-- High priority sections -->
<nav data-ux-section="navigation" data-ux-priority="high">
  ...
</nav>

<section data-ux-section="features" data-ux-priority="high">
  ...
</section>

<!-- Medium priority sections -->
<footer data-ux-section="footer" data-ux-priority="medium">
  ...
</footer>
```

## 2. Auto-Discover Sections

Scan your site to find all marked sections:

```bash
# Discover sections on homepage
python qa_agents/discover_ux_sections.py \
  --auto-discover \
  --pages / \
  --output qa_agents/ux-review-config.yaml

# Discover sections across multiple pages
python qa_agents/discover_ux_sections.py \
  --auto-discover \
  --pages / /lessons /about \
  --output qa_agents/ux-review-config.yaml
```

This generates a config file showing all discovered sections with smart defaults:
- **Persona**: Auto-assigned based on section name (hero→first-impression, footer→trust-inspector)
- **Priority**: Auto-assigned or from HTML attribute (critical/high/medium/low)
- **Selector**: CSS selector to find the element
- **Bounds**: Element dimensions and position

## 3. Run Targeted Reviews

### Option A: Auto-Discovery Mode (Recommended)
Scan and review in one command:

```bash
# Review all sections
python qa_agents/targeted_review.py --auto-discover --pages /

# Review multiple pages
python qa_agents/targeted_review.py --auto-discover --pages / /lessons /about

# Review only critical sections
python qa_agents/targeted_review.py --auto-discover --pages / --priority critical

# Custom viewport
python qa_agents/targeted_review.py --auto-discover --pages / --viewport tablet
```

### Option B: Config-Based Mode
Use pre-generated config:

```bash
# Review using config
python qa_agents/targeted_review.py --config qa_agents/ux-review-config.yaml

# Filter by priority
python qa_agents/targeted_review.py \
  --config qa_agents/ux-review-config.yaml \
  --priority critical
```

## 4. Example Output

```
🎯 TARGETED SECTION REVIEW (Data-Attribute Based)
📄 URL: http://localhost:8080
📱 Viewport: desktop

🔍 Auto-discovering sections from HTML...
   ✅ Found 7 sections across 1 page(s)

💰 Cost Estimate: $0.0210 (7 screenshots @ high detail)

📸 Capturing 7 section(s)...
   💾 Screenshots saved to qa_agents/screenshots/

🤖 Analyzing sections with GPT-4o Vision...

   🔍 [CRITICAL] Reviewing 'hero' (first-impression)...
      ✅ Complete
   🔍 [HIGH] Reviewing 'features' (content-flow)...
      ✅ Complete
   ...

======================================================================
🎯 TARGETED SECTION REVIEW RESULTS (desktop)
======================================================================

🔴 CRITICAL PRIORITY (2 sections)
----------------------------------------------------------------------

📍 hero (/)
   Persona: first-impression
   Selector: [data-ux-section="hero"]

✅ STRENGTHS:
- Clear value proposition...
- Strong visual hierarchy...

⚠️ IMPROVEMENTS:
- Consider adding...

----------------------------------------------------------------------
...
======================================================================

✅ Targeted review complete!
   📊 Analyzed 7 section(s)
   💰 Estimated cost: ~$0.0210
```

## Naming Conventions

### Section Names (kebab-case)
- `hero` - Main hero section
- `header` - Site header
- `navigation` - Main navigation
- `features` - Features/benefits section
- `testimonials` - Social proof
- `cta-final` - Final call-to-action
- `footer` - Site footer

### Auto-Assigned Personas
| Section Pattern | Persona | Use Case |
|---|---|---|
| hero, header, nav | first-impression | Visual hierarchy, brand |
| features, content, lessons | content-flow | Readability, structure |
| footer, contact, social | trust-inspector | Credibility, legal |
| cta, pricing, signup | conversion-optimizer | Actions, forms |

### Priority Levels
- **critical**: Must review every time (hero, header)
- **high**: Important UX elements (nav, features, cta)
- **medium**: Secondary content (footer, sidebar)
- **low**: Optional elements (decorative, supplementary)

## Advanced Usage

### Priority Filtering

Review only critical sections in CI/CD:
```bash
python qa_agents/targeted_review.py \
  --auto-discover \
  --pages / \
  --priority critical
```

### Multi-Viewport Testing

Test all viewports:
```bash
for viewport in desktop tablet mobile; do
  python qa_agents/targeted_review.py \
    --auto-discover \
    --pages / \
    --viewport $viewport
done
```

### Selective Page Reviews

Review changed pages only:
```bash
python qa_agents/targeted_review.py \
  --auto-discover \
  --pages /lessons /about
```

## Best Practices

### ✅ DO

- Mark distinct visual sections
- Use descriptive, unique names
- Set explicit priorities for critical sections
- Mark responsive breakpoint variations
- Keep section granularity consistent

### ❌ DON'T

- Mark tiny elements (buttons, icons)
- Duplicate section names on same page
- Nest marked sections
- Mark hidden/conditional content
- Use spaces in section names

## Comparison with Old System

### Old (Viewport-Based)
```python
# Hardcoded 3 sections
sections = ["above-fold", "mid-page", "footer"]

# Scroll viewport to approximate positions
# Captures whatever is on screen at that scroll position
```

**Problems**:
- Fixed 3 sections per page
- Viewport scrolling is imprecise
- Breaks when layout changes
- Manual updates required

### New (Element-Based)
```html
<!-- Self-documenting HTML -->
<section data-ux-section="hero" data-ux-priority="critical">
  ...
</section>
```

**Benefits**:
- Auto-discover 1-10+ sections per page
- Precise element targeting
- Works with any layout
- Zero maintenance

## Integration with Existing Tools

### Compatible with Phase 1 & 2
All existing tools still work:
- ✅ `visual_ux_review.py` - Full-page reviews
- ✅ `section_review.py` - Viewport-based sections
- ✅ `targeted_review.py` - **NEW** Element-based targeting

### When to Use Each

- **`visual_ux_review.py`**: Full-page overview
- **`section_review.py`**: Quick 3-section checks (legacy)
- **`targeted_review.py`**: Precise, priority-aware reviews (recommended)

## Troubleshooting

### "Found 0 sections"
- Ensure `data-ux-section` attributes are in HTML
- Check build output in `_site/` directory
- Verify server is running and pages load

### "Element not found"
- Ensure selector is correct in config
- Check element is visible (not `display: none`)
- Verify element exists on page

### "Permission denied"
- Ensure screenshots directory exists
- Check file permissions on output directory

## Example Templates

See complete examples in:
- `qa_agents/examples/base-with-data-attributes.njk`
- `qa_agents/examples/index-with-data-attributes.njk`
- `qa_agents/DATA-ATTRIBUTES-GUIDE.md`

## Next Steps

1. **Add markers to templates** (15 min)
2. **Generate initial config** (5 min)
3. **Run first targeted review** (5 min)
4. **Integrate with CI/CD** (Phase 3)

---

**Questions?** See `DATA-ATTRIBUTES-GUIDE.md` for comprehensive documentation.
