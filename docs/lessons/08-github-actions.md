---
layout: lesson.njk
title: 'GitHub Actions CI/CD'
lessonNumber: 8
description: 'Understand automated testing and deployment with GitHub Actions'
timeEstimate: '13 minutes'
level: 'Intermediate'
tags: ['lessons']
permalink: '/lessons/08-github-actions/'
---

⏱️ **Time:** Reading: 8 min | Practice: 5 min | Total: ~13 min 📚 **Level:**
Intermediate 🎯 **Goal:** Understand automated testing and deployment with
GitHub Actions

---

## 🚀 TL;DR

**GitHub Actions** automatically tests your code when you push to GitHub, then
deploys it to GitHub Pages if tests pass. No manual deployment needed!

---

## 🤔 What Is CI/CD?

### CI = Continuous Integration

**What:** Automatically test code when pushed to GitHub

**Why:** Catch bugs before they reach production

**How:** GitHub Actions runs tests on every push/PR

---

### CD = Continuous Deployment

**What:** Automatically deploy code when tests pass

**Why:** Fast, consistent deployments

**How:** GitHub Actions builds and publishes to GitHub Pages

---

### The Complete Pipeline:

```
You Push Code to GitHub
      ↓
GitHub Actions Triggers
      ↓
Quality Checks (ESLint, Stylelint, etc.)
      ↓
Build Site (Eleventy)
      ↓
Performance Tests (Lighthouse CI)
      ↓
Deploy to GitHub Pages
      ↓
Live Website! 🎉
```

---

## 📁 Workflow Configuration

**File:** `.github/workflows/ci-cd.yml`

**What it does:** Defines automated pipeline

**Structure:**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality-checks:
    # Runs linters

  build:
    # Builds site

  lighthouse:
    # Tests performance

  deploy:
    # Publishes to GitHub Pages
```

---

## 🔄 The Four Jobs

### Job 1: Quality Checks ✅

**What it does:** Runs all linters and quality gates

**Steps:**

```yaml
quality-checks:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
    - run: npm ci
    - run: npm run lint:js
    - run: npm run lint:css
    - run: npm run lint:md
    - run: npm run lint:format
    - run: npm run lint:duplication
```

**Checks:**

- ✓ JavaScript (ESLint)
- ✓ CSS (Stylelint)
- ✓ Markdown (Markdownlint)
- ✓ Formatting (Prettier)
- ✓ Duplication (jscpd)

**If any fail:** Pipeline stops ❌

---

### Job 2: Build 🏗️

**What it does:** Builds production site

**Steps:**

```yaml
build:
  needs: quality-checks # Only runs if quality-checks passes
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
    - run: npm ci
    - run: npm run build
    - uses: actions/upload-artifact@v4
      with:
        name: site
        path: _site/
```

**Produces:**

- `_site/` directory with HTML/CSS/JS
- Uploaded as artifact for later jobs

**If build fails:** Pipeline stops ❌

---

### Job 3: Lighthouse 💡

**What it does:** Tests performance, accessibility, SEO

**Steps:**

```yaml
lighthouse:
  needs: build
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/download-artifact@v4
      with:
        name: site
        path: _site/
    - run: npm ci
    - run: npx @lhci/cli@0.14.x autorun
      continue-on-error: true # Don't fail pipeline
```

**Tests:**

- ⚡ Performance (speed)
- ♿ Accessibility (for all users)
- 🎯 Best Practices (modern standards)
- 🔍 SEO (search engines)

**Scoring:**

- 90-100 = ✅ Green (excellent)
- 50-89 = 🟡 Orange (needs improvement)
- 0-49 = 🔴 Red (poor)

**Note:** Uses `continue-on-error: true` so doesn't block deployment

---

### Job 4: Deploy 🚀

**What it does:** Publishes site to GitHub Pages

**Steps:**

```yaml
deploy:
  needs: [build, lighthouse]
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  permissions:
    contents: read
    pages: write
    id-token: write
  steps:
    - uses: actions/download-artifact@v4
      with:
        name: site
        path: _site/
    - uses: actions/configure-pages@v4
    - uses: actions/upload-pages-artifact@v3
      with:
        path: _site/
    - uses: actions/deploy-pages@v4
```

**Conditions:**

- ✓ Only on `main` branch
- ✓ Only on `push` (not PR)
- ✓ Only if build and lighthouse succeeded

**Result:** Live site at `https://username.github.io/repo-name/`

---

## 🏃 Triggering the Pipeline

### Trigger 1: Push to Main

```bash
# Make changes
git add .
git commit -m "add feature"
git push origin main

# GitHub Actions automatically runs pipeline
```

**View:** Go to GitHub → Your Repo → Actions tab

---

### Trigger 2: Pull Request

```bash
# Create feature branch
git checkout -b feature/new-page
git add .
git commit -m "add new page"
git push origin feature/new-page

# Create PR on GitHub
# Pipeline runs automatically
```

**Result:** PR shows check status (✓ or ✗)

---

## 📊 Monitoring Pipeline

### View Workflow Run:

1. Go to GitHub repository
2. Click "Actions" tab
3. Click on latest workflow run

**You'll see:**

```
CI/CD Pipeline #42
  ✓ quality-checks (1m 23s)
  ✓ build (45s)
  ✓ lighthouse (2m 10s)
  ✓ deploy (38s)
```

---

### View Job Details:

Click on any job to see:

- **Steps:** Each command that ran
- **Logs:** Output from each step
- **Timing:** How long each step took
- **Errors:** If any step failed

**Example log:**

```bash
Run npm run lint:js
> eslint src/**/*.js

✓ 2 files checked
✓ 0 errors
✓ 1 warning

✓ ESLint passed
```

---

### View Lighthouse Report:

1. Click "lighthouse" job
2. Scroll to "Run Lighthouse CI" step
3. See scores:

```
Performance: 98
Accessibility: 100
Best Practices: 100
SEO: 100

✓ All scores above threshold
```

---

## 🚨 When Pipeline Fails

### Failure 1: Quality Checks Failed

**Symptom:**

```
✗ quality-checks (1m 30s)
  ✗ Run npm run lint:js failed
```

**View error:**

```bash
src/js/main.js
  5:10  error  'x' is not defined  no-undef

✗ ESLint found 1 error
```

**Fix:**

```bash
# Fix locally
npm run lint:js -- --fix

# Commit and push
git add .
git commit -m "fix: undefined variable"
git push

# Pipeline re-runs automatically
```

---

### Failure 2: Build Failed

**Symptom:**

```
✓ quality-checks (1m 23s)
✗ build (30s)
  ✗ Run npm run build failed
```

**View error:**

```bash
[11ty] Problem writing Eleventy templates:
[11ty] Template render error: (src/index.md)
  Error: layout not found: base.njk
```

**Fix:**

```bash
# Check layout exists
ls src/_includes/base.njk

# Fix layout reference in Markdown front matter
# Commit and push
```

---

### Failure 3: Lighthouse Threshold Not Met

**Note:** With `continue-on-error: true`, this won't fail pipeline

**Symptom:**

```
✓ lighthouse (2m 10s)
  ⚠️ Performance score: 45 (threshold: 50)
```

**Fix:**

- Optimize images (compress, resize)
- Minify CSS/JS
- Remove unused code
- Use CDN for assets

---

## 💡 Pro Tips

### Tip 1: Check Actions Before Deploying

```bash
# Before creating PR
npm run lint
npm run build

# If passing locally, will pass in CI/CD
```

---

### Tip 2: Use Draft PRs

```bash
# Create draft PR for work in progress
gh pr create --draft --title "WIP: new feature"

# CI/CD runs, but doesn't deploy
# Mark "Ready for review" when done
```

---

### Tip 3: Monitor Email Notifications

GitHub emails you when:

- ✓ Pipeline succeeds
- ✗ Pipeline fails
- 🎉 Deployment completes

**Enable:** GitHub Settings → Notifications → Actions

---

### Tip 4: Understand Job Dependencies

```yaml
build:
  needs: quality-checks # Waits for quality-checks

deploy:
  needs: [build, lighthouse] # Waits for BOTH
```

**Result:** Jobs run in order, failures stop pipeline early

---

## 🔍 Understanding Artifacts

### What Are Artifacts?

**Artifacts** = Files produced by jobs, used by later jobs

**Our artifacts:**

- `site` = Built website from build job

**Usage:**

1. `build` job uploads `_site/` as artifact
2. `lighthouse` job downloads artifact to test
3. `deploy` job downloads artifact to publish

---

### Viewing Artifacts:

1. Go to workflow run
2. Scroll to bottom
3. See "Artifacts" section
4. Download `site` to inspect

**Use case:** Debug what gets deployed

---

## 🎮 Quick Practice Activity (3 minutes)

### Challenge: Trigger and Monitor Pipeline

**1. Make a change:**

```bash
# Edit homepage
echo "New content!" >> src/index.md

# Commit and push
git add src/index.md
git commit -m "docs: update homepage"
git push origin main
```

**2. Watch pipeline:**

1. Go to GitHub → Actions
2. Click latest workflow run
3. Watch jobs execute in real-time
4. See green checkmarks ✓

**3. Verify deployment:**

1. Wait for deploy job to finish
2. Visit: `https://YOUR_USERNAME.github.io/is117_ai_test_practice/`
3. See your changes live!

**✅ Success!** You've deployed with CI/CD!

---

## 📊 GitHub Actions Checklist

Before moving to the next lesson, verify:

- [ ] Understand CI = testing, CD = deployment
- [ ] Know the 4 jobs: quality-checks, build, lighthouse, deploy
- [ ] Can view workflow runs in Actions tab
- [ ] Can read job logs and errors
- [ ] Know how to fix failed pipelines
- [ ] Understand job dependencies (`needs`)
- [ ] Know artifacts pass files between jobs
- [ ] Can monitor pipeline execution
- [ ] Verified deployment to GitHub Pages works
- [ ] Understand `continue-on-error` for lighthouse

**All checked?** Ready for Lesson 9! 🎉

---

## 📚 Key Takeaways

### ✅ DO:

- Test locally before pushing (`npm run lint`, `npm test`)
- Monitor Actions tab after pushing
- Read job logs when failures occur
- Fix errors and re-push
- Use draft PRs for work in progress
- Understand job dependencies

### ❌ DON'T:

- Push without running tests locally
- Ignore failed pipelines
- Edit workflow file without understanding YAML
- Remove `continue-on-error` from lighthouse (blocks deploys)
- Commit to main without tests passing

---

## 🎯 Pipeline Flow Summary

```
1. Developer pushes code
      ↓
2. Quality checks run (ESLint, Stylelint, etc.)
   - ✓ Pass → Continue
   - ✗ Fail → Stop
      ↓
3. Build site (Eleventy)
   - ✓ Build succeeds → Continue
   - ✗ Build fails → Stop
      ↓
4. Lighthouse tests (Performance, A11y, SEO)
   - Scores reported (doesn't block)
      ↓
5. Deploy to GitHub Pages
   - Only if: main branch + push event
   - Only if: all previous jobs passed
      ↓
6. Live website! 🎉
```

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
- [ ] Lesson 9: Lighthouse CI
- [ ] Lesson 10: Troubleshooting

---

## 🚀 Next Steps

Now let's dive deeper into Lighthouse performance testing!

### [👉 Continue to Lesson 9: Lighthouse CI](/lessons/09-lighthouse-ci/)

---

## 🔗 Quick Links

- [🏠 Back to Course Index](/lessons/)
- [📝 Configuration Prompts](/resources/#prompts)
- [📚 NPM Scripts Reference](/resources/#reference)
- [🔧 GitHub Actions Docs](https://docs.github.com/en/actions)

---

**Your deployments are now fully automated!** 🚀✨
