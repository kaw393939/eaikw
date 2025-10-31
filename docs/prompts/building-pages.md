# Building Pages Prompts 🏗️

**Purpose:** Copy-paste prompts for building pages, layouts, styles, and content
with Eleventy

**When to use:** Creating new pages, layouts, or features while maintaining DRY
principles

---

## 📋 Quick Reference

| Prompt                                           | Use Case             | Output                          |
| ------------------------------------------------ | -------------------- | ------------------------------- |
| [Create New Page](#prompt-1-create-new-page)     | Add page to site     | Markdown file with front matter |
| [Create Layout](#prompt-2-create-layout)         | Custom page template | Nunjucks layout file            |
| [Add Styles](#prompt-3-add-styles-dry)           | Style components     | CSS (checks existing first!)    |
| [Add JavaScript](#prompt-4-add-javascript-dry)   | Interactive features | JS (checks existing first!)     |
| [Create Navigation](#prompt-5-create-navigation) | Site navigation menu | Nav component                   |
| [Add Images](#prompt-6-add-images)               | Optimized images     | Compressed image files          |
| [Create Blog Post](#prompt-7-create-blog-post)   | Blog post page       | Markdown with metadata          |

---

## Prompt 1: Create New Page

**Use when:** Adding a new page to your site

### 📋 Copy This Prompt:

```
I need to create a new page for my Eleventy site. Please:

1. Create src/[PAGE_NAME].md with:
   - Front matter (layout: base.njk, title, description)
   - Heading structure (H1, H2, H3)
   - Content sections
   - SEO-friendly meta description

2. Page requirements:
   - Title: [YOUR_TITLE]
   - Purpose: [DESCRIBE_PURPOSE]
   - Sections: [LIST_SECTIONS]

3. Ensure:
   - Proper heading hierarchy
   - Descriptive alt text for images
   - Semantic HTML structure
   - Mobile-friendly content

Example structure:
---
layout: base.njk
title: About Us
description: Learn about our team and mission
---

# About Us

## Our Mission
[Content here]

## Our Team
[Content here]

IMPORTANT: Before creating ANY styles or scripts, check if similar code already exists in src/css/ and src/js/. Reuse existing code whenever possible!
```

---

## Prompt 2: Create Layout

**Use when:** Need a custom page template

### 📋 Copy This Prompt:

```
I need to create a custom Eleventy layout. Please:

1. Create src/_includes/[LAYOUT_NAME].njk with:
   - Proper HTML5 structure
   - Meta tags (charset, viewport, description)
   - Link to existing stylesheet (src/css/style.css)
   - Link to existing JavaScript (src/js/main.js)
   - {{ content | safe }} for page content
   - {{ title }} for page title

2. Layout features needed:
   - [DESCRIBE_FEATURES]

3. CRITICAL: Before adding ANY CSS or JavaScript:
   - Check src/css/style.css for existing styles
   - Check src/js/main.js for existing functionality
   - ONLY create new code if needed functionality doesn't exist
   - DRY principle is mandatory!

Example structure:
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title }}</title>
  <meta name="description" content="{{ description or 'Default description' }}">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <main>
    {{ content | safe }}
  </main>
  <script src="/js/main.js"></script>
</body>
</html>

Remember: Check existing styles before creating new CSS!
```

---

## Prompt 3: Add Styles (DRY!)

**Use when:** Need to style a component

### 📋 Copy This Prompt:

```
I need to add styles for [COMPONENT_NAME]. CRITICAL: We must follow DRY principles!

STEP 1 - CHECK EXISTING STYLES:
First, analyze src/css/style.css to check if we already have:
- Similar color values
- Similar layout patterns (flex, grid)
- Similar spacing utilities
- Similar font styles
- Similar button/form styles
- Similar media queries

STEP 2 - REPORT FINDINGS:
Tell me what existing styles could be reused for:
[DESCRIBE_WHAT_YOU_NEED]

STEP 3 - ADD ONLY WHAT'S NEEDED:
Only after checking existing code, add to src/css/style.css:
- Reuse existing CSS variables for colors, spacing, fonts
- Reuse existing classes where possible
- Only add NEW styles if functionality doesn't exist
- Group related styles together
- Add comments explaining purpose

Component needs:
- Description: [DESCRIBE_COMPONENT]
- Visual design: [DESCRIBE_DESIGN]
- Responsive behavior: [DESCRIBE_RESPONSIVE]

Example workflow:
1. "I see we already have .button { ... }, I'll extend that"
2. "I see we already use --primary-color, I'll reuse that"
3. "We don't have card styling, I'll add new .card class"

NEVER create duplicate selectors or properties!
```

---

## Prompt 4: Add JavaScript (DRY!)

**Use when:** Need interactive functionality

### 📋 Copy This Prompt:

```
I need to add JavaScript for [FEATURE_NAME]. CRITICAL: We must follow DRY principles!

STEP 1 - CHECK EXISTING CODE:
First, analyze src/js/main.js to check if we already have:
- Similar DOM queries (querySelector, querySelectorAll)
- Similar event listeners
- Similar functions (toggleClass, getData, etc.)
- Similar API calls
- Similar utility functions

STEP 2 - REPORT FINDINGS:
Tell me what existing JavaScript could be reused for:
[DESCRIBE_WHAT_YOU_NEED]

STEP 3 - ADD ONLY WHAT'S NEEDED:
Only after checking existing code, add to src/js/main.js:
- Reuse existing helper functions
- Reuse existing event delegation patterns
- Only add NEW code if functionality doesn't exist
- Use clear function names
- Add comments explaining purpose

Feature needs:
- Description: [DESCRIBE_FEATURE]
- User interaction: [DESCRIBE_INTERACTION]
- Data handling: [DESCRIBE_DATA]

Example workflow:
1. "I see we already have a toggleMenu() function, I'll reuse that pattern"
2. "I see we already query .nav elements, I'll use same approach"
3. "We don't have form validation, I'll add new validateForm() function"

NEVER create duplicate functions or event listeners!
```

---

## Prompt 5: Create Navigation

**Use when:** Building site navigation menu

### 📋 Copy This Prompt:

```
I need to create a navigation menu for my Eleventy site. Please:

1. FIRST: Check if navigation already exists in:
   - src/_includes/base.njk (main layout)
   - src/_includes/nav.njk (potential nav partial)
   - src/css/style.css (existing nav styles)
   - src/js/main.js (existing nav functionality)

2. IF navigation doesn't exist, create:
   - Navigation structure (semantic <nav> element)
   - Links to: [LIST_PAGES]
   - Mobile-friendly responsive menu
   - Accessible keyboard navigation
   - ARIA labels for screen readers

3. IF navigation exists:
   - Report existing structure
   - Suggest modifications to add new links
   - Reuse existing styles and scripts

Navigation requirements:
- Pages to link: [LIST_PAGES]
- Style: [DESCRIBE_STYLE]
- Mobile behavior: [DESCRIBE_MOBILE]

Example structure:
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about/">About</a></li>
    <li><a href="/contact/">Contact</a></li>
  </ul>
</nav>

Check for duplicate navigation code before creating!
```

---

## Prompt 6: Add Images

**Use when:** Adding images to site

### 📋 Copy This Prompt:

```
I need to add images to my Eleventy site. Please help me:

1. Image optimization:
   - Compress images (target < 200 KB for large images)
   - Use appropriate formats (WebP for photos, SVG for icons)
   - Specify width/height attributes (prevent layout shift)
   - Generate responsive sizes if needed

2. Image implementation:
   - Descriptive alt text (accessibility!)
   - Lazy loading for below-fold images
   - Proper file naming (lowercase, hyphens, descriptive)
   - Organize in src/images/ directory

3. BEFORE adding styles:
   - Check src/css/style.css for existing image styles
   - Reuse existing CSS for responsive images
   - Only add new styles if needed

Image details:
- Purpose: [DESCRIBE_PURPOSE]
- Location on page: [DESCRIBE_LOCATION]
- Dimensions needed: [SPECIFY_DIMENSIONS]

Example markup:
<img
  src="/images/hero.jpg"
  alt="Team collaborating on a project"
  width="800"
  height="600"
  loading="lazy"
>

Optimization tools:
- TinyPNG (online compression)
- Squoosh (web app)
- ImageOptim (Mac app)

IMPORTANT: Check existing image styles before creating new CSS!
```

---

## Prompt 7: Create Blog Post

**Use when:** Adding blog post content

### 📋 Copy This Prompt:

```
I need to create a blog post for my Eleventy site. Please:

1. Create src/blog/[POST_SLUG].md with:
   - Front matter (layout, title, description, date, author, tags)
   - Clear heading hierarchy (H1, H2, H3)
   - Introduction paragraph
   - Content sections
   - Conclusion
   - Call-to-action

2. Post details:
   - Title: [POST_TITLE]
   - Topic: [POST_TOPIC]
   - Key points: [LIST_POINTS]
   - Target audience: [DESCRIBE_AUDIENCE]

3. SEO optimization:
   - Descriptive meta description (155 chars)
   - Relevant keywords naturally integrated
   - Internal links to related content
   - Proper image alt text

4. CRITICAL: Check existing code:
   - Look for existing blog post layout
   - Check for existing blog styles
   - Reuse existing components
   - Don't duplicate CSS or JavaScript

Example structure:
---
layout: base.njk
title: "How to Build Better Websites"
description: "Learn proven techniques for building modern, accessible websites"
date: 2025-10-27
author: Your Name
tags: ["web development", "tutorial"]
---

# How to Build Better Websites

## Introduction
[Hook the reader]

## Main Content
[Value-packed content]

## Conclusion
[Summary and next steps]

REMEMBER: Check and reuse existing styles!
```

---

## 🔄 Complete Page Build Prompt

**Use when:** Building a complete page with all components

### 📋 Copy This Prompt:

```
I need to build a complete page for my Eleventy site with STRICT DRY enforcement.

Page: [PAGE_NAME]
Purpose: [DESCRIBE_PURPOSE]
Sections: [LIST_SECTIONS]

MANDATORY DRY WORKFLOW:

PHASE 1 - AUDIT EXISTING CODE:
Before creating ANYTHING, analyze:
1. src/css/style.css - Report all existing:
   - Color variables and values
   - Layout patterns (flex, grid)
   - Typography styles
   - Component classes (buttons, cards, forms)
   - Utility classes
   - Media queries

2. src/js/main.js - Report all existing:
   - Functions and their purposes
   - Event listeners
   - DOM manipulation patterns
   - Utility helpers

3. src/_includes/*.njk - Report all existing:
   - Layouts and their purposes
   - Partials and components
   - Template patterns

PHASE 2 - PLAN REUSE:
Based on the audit, tell me:
- What existing code will be reused
- What can be extended with minimal additions
- What truly needs to be created new

PHASE 3 - BUILD (ONLY IF APPROVED):
Create the page with:
- src/[PAGE_NAME].md (content and structure)
- Extensions to existing CSS (not new classes!)
- Extensions to existing JS (not new functions!)
- Proper front matter and metadata
- Accessible markup
- SEO optimization

PHASE 4 - VERIFY:
After building, run:
- npm run lint:duplication (must show 0% increase)
- npm run lint:css (catch duplicate selectors)
- npm run lint:js (catch issues)

FAIL THE BUILD if duplication detected!

I will reject any solution that:
- Creates duplicate CSS selectors
- Creates duplicate functions
- Doesn't check existing code first
- Adds unnecessary new code

Show me the audit report before building anything!
```

---

## 🧪 Testing New Pages

After building with prompts, verify:

```bash
# Build site
npm run build

# Check for errors
npm run lint

# Check for duplication
npm run lint:duplication

# Test locally
npm start
# Visit: http://localhost:8080/[PAGE_NAME]/

# Test responsiveness
# Resize browser window
# Test on mobile device

# Test accessibility
# Tab through with keyboard
# Check color contrast
# Verify alt text

# Test performance
npx @lhci/cli@0.14.x autorun
```

---

## 🚨 Common Building Issues

### Issue: "Styles not applying"

**Debug:**

```bash
# Check file path
ls -la src/css/style.css

# Check layout links to CSS
cat src/_includes/base.njk | grep stylesheet

# Check browser console for 404s
# Open browser DevTools → Network tab
```

---

### Issue: "Page not found after build"

**Debug:**

```bash
# Check file created
ls -la src/your-page.md

# Check built output
ls -la _site/your-page/index.html

# Check front matter has layout
head -n 5 src/your-page.md

# Rebuild
npm run build
```

---

### Issue: "Duplicate CSS detected"

**Fix:**

```bash
# Find duplicates
npm run lint:duplication

# View detailed report
cat .jscpd-report/jscpd-report.json

# Consolidate duplicate code
# Reuse existing classes instead
```

---

## 💡 Pro Tips

### Tip 1: Always Check Existing Code First

```bash
# Before creating CSS
grep -r "color:" src/css/
grep -r "display: flex" src/css/

# Before creating JavaScript
grep -r "function" src/js/
grep -r "addEventListener" src/js/
```

### Tip 2: Use CSS Variables for Consistency

```css
/* Define once */
:root {
  --primary-color: #007bff;
  --spacing: 1rem;
}

/* Reuse everywhere */
.button {
  background: var(--primary-color);
}
.header {
  color: var(--primary-color);
}
```

### Tip 3: Create Reusable Components

```css
/* ✅ Good: Generic, reusable */
.card {
  padding: 1rem;
  border: 1px solid #ddd;
}
.card-title {
  font-size: 1.5rem;
}

/* ❌ Bad: Too specific */
.homepage-hero-card {
  padding: 1rem;
  border: 1px solid #ddd;
}
```

### Tip 4: Test Incrementally

Build and test one section at a time:

```bash
# Add section 1
npm run build && npm start

# Verify section 1 works
# Then add section 2

# Avoid building everything at once!
```

---

## 📊 Building Checklist

Before considering a page complete:

- [ ] Content created in src/
- [ ] Front matter includes layout, title, description
- [ ] Checked existing CSS before adding new
- [ ] Checked existing JS before adding new
- [ ] No duplicate selectors (lint:css passes)
- [ ] No code duplication (lint:duplication passes)
- [ ] All images optimized and have alt text
- [ ] Page builds without errors
- [ ] Page displays correctly in browser
- [ ] Responsive on mobile
- [ ] Keyboard accessible
- [ ] Lighthouse scores acceptable

---

## 🔗 Quick Links

- [🏠 Back to Course Index](../../README.md)
- [📚 Lesson 5: Build with Eleventy](../lessons/05-build-with-eleventy.md)
- [📝 Avoiding Duplication Guide](./avoiding-duplication.md)
- [📖 File Structure Reference](../reference/file-structure.md)

---

**Build amazing pages while keeping your code DRY!** 🏗️✨
