---
layout: lesson.njk
title: 'Lighthouse CI'
lessonNumber: 9
description: 'Understand performance testing and optimization with Lighthouse'
timeEstimate: '11 minutes'
level: 'Intermediate'
tags: ['lessons']
permalink: '/lessons/09-lighthouse-ci/'
---

⏱️ **Time:** Reading: 6 min | Practice: 5 min | Total: ~11 min 📚 **Level:**
Intermediate 🎯 **Goal:** Understand performance testing and optimization with
Lighthouse

---

## 🚀 TL;DR

**Lighthouse CI** automatically tests your site's performance, accessibility,
SEO, and best practices on every deployment. It provides scores and actionable
recommendations for improvement.

---

## 🤔 What Is Lighthouse?

**Lighthouse** is Google's automated tool for improving web quality.

**Tests:**

- ⚡ **Performance** - Loading speed
- ♿ **Accessibility** - Usability for all
- 🎯 **Best Practices** - Modern standards
- 🔍 **SEO** - Search engine optimization

**Score Range:** 0-100 (higher is better)

---

## 📊 The Four Categories

### 1. Performance ⚡ (Target: 90+)

**What it measures:**

- First Contentful Paint (when content appears)
- Speed Index (how quickly content loads)
- Largest Contentful Paint (largest element loads)
- Time to Interactive (when page becomes interactive)
- Total Blocking Time (how long page is unresponsive)
- Cumulative Layout Shift (visual stability)

**Why it matters:** Fast sites = happy users = better conversions

**Common issues:**

- Large images (not optimized)
- Too much JavaScript
- No caching
- Render-blocking resources

---

### 2. Accessibility ♿ (Target: 95+)

**What it measures:**

- Color contrast ratios
- ARIA attributes
- Alt text for images
- Form labels
- Keyboard navigation
- Screen reader compatibility

**Why it matters:** Everyone should be able to use your site

**Common issues:**

- Missing alt text on images
- Low color contrast
- Missing form labels
- No skip links
- Poor heading hierarchy

---

### 3. Best Practices 🎯 (Target: 95+)

**What it measures:**

- HTTPS usage
- Console errors
- Deprecated APIs
- Secure connections
- Modern JavaScript

**Why it matters:** Follow industry standards for security and reliability

**Common issues:**

- HTTP instead of HTTPS
- Console errors
- Vulnerable dependencies
- Insecure third-party scripts

---

### 4. SEO 🔍 (Target: 95+)

**What it measures:**

- Meta descriptions
- Page titles
- Crawlability
- Mobile-friendliness
- Structured data
- Canonical URLs

**Why it matters:** Help search engines find and rank your site

**Common issues:**

- Missing meta description
- Missing title tag
- Not mobile-friendly
- Blocked by robots.txt
- No viewport meta tag

---

## 📁 Configuration File

**File:** `lighthouserc.json`

**What it does:** Configures Lighthouse CI thresholds and settings

**Our configuration:**

```json
{
  "ci": {
    "collect": {
      "staticDistDir": "./_site",
      "url": [
        "http://localhost/is117_ai_test_practice/index.html",
        "http://localhost/is117_ai_test_practice/about/index.html"
      ]
    },
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "categories:performance": ["warn", { "minScore": 0.5 }],
        "categories:accessibility": ["warn", { "minScore": 0.95 }],
        "categories:best-practices": ["warn", { "minScore": 0.95 }],
        "categories:seo": ["warn", { "minScore": 0.95 }]
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

**Key parts:**

- `staticDistDir` - Where built site lives (`_site/`)
- `url` - Which pages to test
- `assertions` - Minimum acceptable scores
- `upload` - Where to store reports

---

## 🏃 Running Lighthouse

### Local Test (Development)

```bash
# Build site first
npm run build

# Run Lighthouse
npx @lhci/cli@0.14.x autorun
```

**What happens:**

```bash
✓ Running Lighthouse CI...
  ✓ Collecting reports for 2 pages
  ✓ Testing http://localhost/.../index.html
  ✓ Testing http://localhost/.../about/index.html

Performance:     98
Accessibility:   100
Best Practices:  100
SEO:             100

✓ All assertions passed
✓ Reports uploaded: https://storage.googleapis.com/...
```

**View report:** Click the uploaded URL

---

### CI/CD Test (Automatic)

**Runs automatically** when you push to GitHub (in
`.github/workflows/ci-cd.yml`):

```yaml
lighthouse:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/download-artifact@v4
      with:
        name: site
        path: _site/
    - run: npm ci
    - run: npx @lhci/cli@0.14.x autorun
      continue-on-error: true # Don't block deployment
```

**View results:** GitHub Actions → lighthouse job → logs

---

## 📊 Reading Lighthouse Reports

### Score Interpretation:

| Score  | Color     | Meaning           |
| ------ | --------- | ----------------- |
| 90-100 | 🟢 Green  | Excellent         |
| 50-89  | 🟡 Orange | Needs improvement |
| 0-49   | 🔴 Red    | Poor              |

---

### Example Report:

```
⚡ Performance: 87 🟡
  Opportunities:
    • Properly size images (save 120 KB)
    • Eliminate render-blocking resources (save 0.5s)
    • Minify CSS (save 8 KB)

♿ Accessibility: 100 🟢
  Passed audits:
    ✓ Images have alt text
    ✓ Color contrast is sufficient
    ✓ Form elements have labels

🎯 Best Practices: 100 🟢
  Passed audits:
    ✓ Uses HTTPS
    ✓ No browser errors
    ✓ Secure dependencies

🔍 SEO: 100 🟢
  Passed audits:
    ✓ Has meta description
    ✓ Page has title
    ✓ Mobile-friendly
```

---

## 🔧 Common Optimizations

### Performance: Optimize Images

**Problem:** Large images slow load time

**Fix:**

```bash
# Compress images (use online tools or CLI)
# Example sizes:
# Hero image: < 200 KB
# Thumbnail: < 50 KB
# Icon: < 10 KB

# Also add width/height attributes:
<img src="hero.jpg" alt="Hero" width="800" height="600">
```

**Impact:** ⚡ Can improve score by 20+ points

---

### Performance: Minify CSS

**Problem:** Large CSS files

**Fix:**

```bash
# Already configured in our project!
# CSS automatically minified during build

# Verify:
ls -lh _site/css/style.css
# Should be small (< 10 KB)
```

**Impact:** ⚡ Improves load time by ~0.2s

---

### Accessibility: Add Alt Text

**Problem:** Images missing alt attributes

**Fix:**

```html
<!-- ❌ Bad (no alt text) -->
<img src="logo.png" />

<!-- ✅ Good (descriptive alt text) -->
<img src="logo.png" alt="Company Logo" />

<!-- ✅ Good (decorative image) -->
<img src="decorative.png" alt="" />
```

**Impact:** ♿ Can improve score by 10+ points

---

### Accessibility: Color Contrast

**Problem:** Text hard to read (low contrast)

**Fix:**

```css
/* ❌ Bad (low contrast) */
.text {
  color: #999; /* Light gray */
  background: #fff; /* White */
  /* Contrast ratio: 2.8:1 (fails) */
}

/* ✅ Good (high contrast) */
.text {
  color: #333; /* Dark gray */
  background: #fff; /* White */
  /* Contrast ratio: 12.6:1 (passes) */
}
```

**Tool:**
[WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

**Impact:** ♿ Can improve score by 5-10 points

---

### SEO: Add Meta Description

**Problem:** Missing meta description

**Fix:**

```html
<!-- In src/_includes/base.njk -->
<head>
  <meta charset="UTF-8" />
  <title>{{ title }}</title>

  <!-- Add this: -->
  <meta
    name="description"
    content="{{ description or 'Quality-first web development course' }}"
  />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
```

**Impact:** 🔍 Can improve score by 10 points

---

### SEO: Mobile-Friendly

**Problem:** Not responsive on mobile

**Fix:**

```html
<!-- Add viewport meta tag -->
<meta name="viewport" content="width=device-width, initial-scale=1.0" />

<!-- Use responsive CSS -->
<style>
  img {
    max-width: 100%;
    height: auto;
  }

  .container {
    width: 100%;
    max-width: 1200px;
    padding: 0 20px;
  }
</style>
```

**Impact:** 🔍 Required for SEO score above 90

---

## 🚨 Common Issues & Fixes

### Issue: "Lighthouse failed to load page"

**Symptom:**

```bash
✗ Error: Failed to load http://localhost/...
  Error: net::ERR_CONNECTION_REFUSED
```

**Fix:**

```bash
# Build didn't complete
npm run build

# Verify _site/ exists
ls -la _site/

# Re-run Lighthouse
npx @lhci/cli@0.14.x autorun
```

---

### Issue: "Scores lower than expected"

**Symptom:**

```bash
Performance: 45 🔴
  ✗ Below threshold of 50
```

**Fix:**

1. View detailed report (click upload URL)
2. Check "Opportunities" section
3. Fix top 3 issues
4. Re-test

**Most common fixes:**

- Compress images
- Remove unused CSS/JS
- Add caching headers

---

### Issue: "Unable to upload report"

**Symptom:**

```bash
✗ Error: Failed to upload to temporary-public-storage
```

**Fix:**

This is non-blocking. Report still generated locally.

```bash
# View local report
cat .lighthouseci/*/lhr-*.json

# Or run with different upload target
# (Edit lighthouserc.json: "target": "filesystem")
```

---

## 💡 Pro Tips

### Tip 1: Test Locally First

```bash
# Before pushing to GitHub
npm run build
npx @lhci/cli@0.14.x autorun

# See scores immediately
# Fix issues before CI/CD runs
```

---

### Tip 2: Focus on Performance First

**Priority order:**

1. Performance (biggest impact on users)
2. Accessibility (affects everyone)
3. SEO (affects discoverability)
4. Best Practices (already high in our project)

---

### Tip 3: Optimize Images Aggressively

**Most common performance bottleneck!**

```bash
# Use image optimization tools:
# - TinyPNG (online)
# - ImageOptim (Mac)
# - Squoosh (web app)

# Target sizes:
# Hero: 200 KB
# Content: 100 KB
# Thumbnails: 50 KB
```

---

### Tip 4: Use Browser DevTools

```bash
# Chrome DevTools Lighthouse:
# 1. Open site in Chrome
# 2. Press F12
# 3. Click "Lighthouse" tab
# 4. Click "Generate report"
# 5. See detailed audits
```

---

## 🎮 Quick Practice Activity (3 minutes)

### Challenge: Improve Lighthouse Score

**1. Run baseline test:**

```bash
npm run build
npx @lhci/cli@0.14.x autorun
# Note your scores
```

**2. Make optimization:**

```markdown
<!-- In src/index.md -->

## <!-- Add meta description to front matter -->

layout: base.njk title: Quality-First Web Development description: Learn to
build modern websites with automated quality gates

---
```

**3. Re-test:**

```bash
npm run build
npx @lhci/cli@0.14.x autorun
# SEO score should improve!
```

**✅ Optimization working!**

---

## 📊 Lighthouse CI Checklist

Before moving to the next lesson, verify:

- [ ] Understand the 4 categories (Performance, Accessibility, Best Practices,
      SEO)
- [ ] Know target scores (90+ for most categories)
- [ ] Can run Lighthouse locally (`npx @lhci/cli autorun`)
- [ ] Can read and interpret Lighthouse reports
- [ ] Know how to optimize images
- [ ] Know how to fix color contrast issues
- [ ] Know how to add meta descriptions
- [ ] Understand `continue-on-error: true` in CI/CD
- [ ] Can view uploaded reports
- [ ] Know to test locally before pushing

**All checked?** Ready for Lesson 10! 🎉

---

## 📚 Key Takeaways

### ✅ DO:

- Test locally before pushing
- Focus on performance optimizations first
- Compress all images
- Add alt text to all images
- Use high contrast colors
- Add meta descriptions to all pages
- View detailed reports for guidance

### ❌ DON'T:

- Ignore Lighthouse warnings
- Use huge unoptimized images
- Use low contrast text
- Skip meta descriptions
- Remove `continue-on-error` from CI/CD
- Deploy without testing

---

## 🎯 Optimization Checklist

**Performance:**

- [ ] All images compressed (< 200 KB)
- [ ] Images have width/height attributes
- [ ] CSS minified
- [ ] JavaScript minified
- [ ] Fonts optimized

**Accessibility:**

- [ ] All images have alt text
- [ ] Color contrast > 4.5:1 for text
- [ ] Form fields have labels
- [ ] Heading hierarchy is logical
- [ ] Keyboard navigation works

**SEO:**

- [ ] Every page has unique title
- [ ] Every page has meta description
- [ ] Viewport meta tag present
- [ ] All links have descriptive text
- [ ] Site is mobile-friendly

---

## 📊 Progress Tracker

You've completed:

- [x] ~~Lesson 1: What Is This Project?~~
- [x] ~~Lesson 2: Why Quality Gates?~~
- [x] ~~Lesson 3: Prompt Engineering Basics~~
- [x] ~~Lesson 4: Setup Your Environment~~
- [x] ~~Lesson 5: Build with Eleventy~~
- [x] ~~Lesson 6: ESLint & Prettier~~
- [x] ~~Lesson 7: Pre-commit Hooks~~
- [x] ~~Lesson 8: GitHub Actions~~
- [x] ~~Lesson 9: Lighthouse CI~~
- [ ] Lesson 10: Troubleshooting

---

## 🚀 Next Steps

One final lesson: How to debug and fix common issues!

### [👉 Continue to Lesson 10: Troubleshooting](/lessons/10-troubleshooting/)

---

## 🔗 Quick Links

- [🏠 Back to Course Index](/lessons/)
- [📝 Debugging Prompts](/resources/#prompts)
- [📚 NPM Scripts Reference](/resources/#reference)
- [💡 Lighthouse Docs](https://developer.chrome.com/docs/lighthouse/)

---

**Your site is now optimized for speed, accessibility, and search!** 💡✨
