# UX Review Data Attributes - Implementation Guide

## Overview

Add `data-ux-section` attributes to your HTML templates to enable automatic UX review discovery and targeted screenshot capture.

## Quick Start

### 1. Basic Syntax

```html
<section data-ux-section="section-name" data-ux-priority="high">
  <!-- Your content -->
</section>
```

### 2. Attributes

**`data-ux-section`** (required)
- Unique identifier for the section
- Use kebab-case (e.g., `hero-section`, `feature-grid`)
- Will be used in reports and config files

**`data-ux-priority`** (optional)
- Values: `critical`, `high`, `medium`, `low`
- Defaults inferred from section name if not specified

## Example Templates

### Base Layout (`src/_includes/layouts/base.njk`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title }}</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <!-- Navigation - Critical UX element -->
  <nav class="site-nav" data-ux-section="navigation" data-ux-priority="critical">
    <div class="site-nav__container">
      <a href="/" class="site-nav__logo">IS117</a>
      <ul class="site-nav__menu">
        <li><a href="/lessons/">Lessons</a></li>
        <li><a href="/resources/">Resources</a></li>
        <li><a href="/for-instructors/">For Instructors</a></li>
      </ul>
    </div>
  </nav>

  <!-- Main content area -->
  <main>
    {{ content | safe }}
  </main>

  <!-- Footer - Always reviewed for trust signals -->
  <footer class="site-footer" data-ux-section="footer" data-ux-priority="medium">
    <div class="site-footer__container">
      <div class="site-footer__links">
        <h3>Quick Links</h3>
        <ul>
          <li><a href="/about/">About</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="/privacy/">Privacy Policy</a></li>
        </ul>
      </div>

      <div class="site-footer__social">
        <h3>Connect</h3>
        <a href="https://github.com/kaw393939" aria-label="GitHub">GitHub</a>
      </div>
    </div>
  </footer>
</body>
</html>
```

### Homepage (`src/index.njk`)

```html
---
layout: layouts/base.njk
title: "IS117: AI-Assisted Web Development"
---

<!-- Hero Section - Critical first impression -->
<section class="hero" data-ux-section="hero" data-ux-priority="critical">
  <div class="hero__container">
    <h1 class="hero__title">Master Web Development with AI</h1>
    <p class="hero__subtitle">
      Learn modern web development techniques enhanced by AI-powered tools
    </p>
    <a href="/lessons/lesson-01/" class="hero__cta">Start Learning</a>
  </div>
</section>

<!-- Course Overview - High priority content -->
<section class="course-overview" data-ux-section="course-overview" data-ux-priority="high">
  <div class="course-overview__container">
    <h2>What You'll Learn</h2>
    <div class="course-overview__grid">
      <div class="course-overview__item">
        <h3>HTML & CSS Fundamentals</h3>
        <p>Build a strong foundation in web markup and styling</p>
      </div>
      <div class="course-overview__item">
        <h3>AI-Assisted Development</h3>
        <p>Leverage AI tools to accelerate your workflow</p>
      </div>
      <div class="course-overview__item">
        <h3>Quality Assurance</h3>
        <p>Automated testing and validation</p>
      </div>
    </div>
  </div>
</section>

<!-- Quality Gates Feature -->
<section class="features" data-ux-section="quality-gates" data-ux-priority="high">
  <div class="features__container">
    <h2>Quality Gates Guard Your Code</h2>
    <ul class="features__list">
      <li>Zero code duplication</li>
      <li>Perfect semantic HTML</li>
      <li>Automated testing</li>
    </ul>
  </div>
</section>

<!-- Call to Action -->
<section class="cta-section" data-ux-section="cta-secondary" data-ux-priority="medium">
  <div class="cta-section__container">
    <h2>Ready to Begin Your Journey?</h2>
    <a href="/lessons/lesson-01/" class="cta-section__button">Start Lesson 1</a>
  </div>
</section>
```

### Lessons Page (`src/lessons/index.njk`)

```html
---
layout: layouts/base.njk
title: "Course Lessons"
---

<!-- Page Header -->
<section class="page-header" data-ux-section="lessons-header" data-ux-priority="high">
  <div class="page-header__container">
    <h1>Course Lessons</h1>
    <p>Progress through structured lessons at your own pace</p>
  </div>
</section>

<!-- Lesson Grid -->
<section class="lesson-grid" data-ux-section="lesson-list" data-ux-priority="critical">
  <div class="lesson-grid__container">
    {% for lesson in collections.lessons %}
      <article class="lesson-card">
        <h2>{{ lesson.data.title }}</h2>
        <p>{{ lesson.data.description }}</p>
        <a href="{{ lesson.url }}">Start Lesson →</a>
      </article>
    {% endfor %}
  </div>
</section>
```

### Individual Lesson (`src/lessons/lesson-01.md`)

```html
---
layout: layouts/lesson.njk
title: "Lesson 1: Getting Started"
---

<!-- Lesson Content -->
<article class="lesson-content" data-ux-section="lesson-main" data-ux-priority="critical">
  <header class="lesson-content__header">
    <h1>{{ title }}</h1>
  </header>

  <div class="lesson-content__body">
    {{ content | safe }}
  </div>
</article>

<!-- Practice Exercises -->
<aside class="lesson-exercises" data-ux-section="exercises" data-ux-priority="high">
  <h2>Practice Exercises</h2>
  <!-- Exercise content -->
</aside>

<!-- Navigation -->
<nav class="lesson-nav" data-ux-section="lesson-navigation" data-ux-priority="medium">
  <a href="/lessons/lesson-02/">Next Lesson →</a>
</nav>
```

## Section Naming Conventions

### Critical Sections (Always Reviewed First)
```html
data-ux-section="hero"              <!-- Homepage hero -->
data-ux-section="navigation"        <!-- Main nav -->
data-ux-section="lesson-main"       <!-- Lesson content -->
data-ux-section="lesson-list"       <!-- Lesson index -->
```

### High Priority Sections
```html
data-ux-section="course-overview"   <!-- Feature lists -->
data-ux-section="quality-gates"     <!-- Key features -->
data-ux-section="lessons-header"    <!-- Page headers -->
data-ux-section="exercises"         <!-- Practice content -->
```

### Medium Priority Sections
```html
data-ux-section="footer"            <!-- Site footer -->
data-ux-section="cta-secondary"     <!-- Secondary CTAs -->
data-ux-section="lesson-navigation" <!-- Lesson nav -->
```

## Persona Mapping (Automatic)

The system automatically assigns personas based on section names:

| Section Name Contains | Assigned Persona | Focus Areas |
|-----------------------|-----------------|-------------|
| `hero`, `header`, `nav` | First Impression Specialist | Value prop, CTA visibility |
| `content`, `features`, `lessons` | Content Flow Analyst | Scanability, hierarchy |
| `footer`, `contact`, `social` | Trust Inspector | Legal links, contact info |

## Priority Guidelines

**Critical** - Must be perfect
- Hero sections
- Main navigation
- Primary content areas
- Core CTAs

**High** - Important but not blocking
- Feature sections
- Secondary navigation
- Important content blocks

**Medium** - Nice to have
- Footers
- Tertiary content
- Supplementary elements

**Low** - Optional
- Decorative sections
- Supplementary widgets

## Testing Your Markers

### 1. Validate Markers Exist

```bash
# Scan site for marked sections
python qa_agents/discover_ux_sections.py _site --pages / /lessons /resources
```

### 2. Generate Config

```bash
# Output: ux-review-config.yaml
python qa_agents/discover_ux_sections.py _site --pages / --output ux-review-config.yaml
```

### 3. Preview Discoveries

The discovery tool will show:
```
🔍 Scanning: /
   ✅ Found 5 sections
      - hero (critical)
      - course-overview (high)
      - quality-gates (high)
      - cta-secondary (medium)
      - footer (medium)
```

## Best Practices

### 1. Mark Semantic Containers
```html
<!-- ✅ Good - marks the semantic section -->
<section class="hero" data-ux-section="hero">
  <div class="hero__container">
    <h1>Title</h1>
  </div>
</section>

<!-- ❌ Bad - marks inner div -->
<section class="hero">
  <div class="hero__container" data-ux-section="hero">
    <h1>Title</h1>
  </div>
</section>
```

### 2. Use Consistent Naming
```html
<!-- ✅ Good - kebab-case, descriptive -->
data-ux-section="lesson-navigation"
data-ux-section="course-overview"

<!-- ❌ Bad - inconsistent, vague -->
data-ux-section="lessonNav"
data-ux-section="section1"
```

### 3. Don't Over-Mark
```html
<!-- ✅ Good - mark major sections only -->
<main data-ux-section="lesson-content">
  <h1>Lesson Title</h1>
  <p>Content</p>
</main>

<!-- ❌ Bad - too granular -->
<main>
  <h1 data-ux-section="title">Lesson Title</h1>
  <p data-ux-section="paragraph">Content</p>
</main>
```

### 4. Mark Responsive Sections
```html
<!-- Mobile-only section -->
<nav class="mobile-nav" data-ux-section="mobile-navigation" data-ux-priority="critical">
  <!-- Content -->
</nav>

<!-- Desktop-only section -->
<aside class="sidebar" data-ux-section="sidebar" data-ux-priority="low">
  <!-- Content -->
</aside>
```

## Next Steps

1. **Add markers to templates** - Start with critical sections
2. **Run discovery** - Validate markers are found
3. **Review config** - Check auto-generated personas/priorities
4. **Run targeted review** - See precise, element-based screenshots

See `QUICK-START.md` for running the full review process.
