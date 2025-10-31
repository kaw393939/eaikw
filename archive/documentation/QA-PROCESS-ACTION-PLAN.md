---
title: 'QA Process Improvement - Action Plan'
description:
  'Step-by-step implementation plan for build and QA process improvements'
layout: base.njk
---

# QA Process Improvement - Action Plan

**Date:** October 28, 2025 **Based on:** BUILD-QA-PROCESS-AUDIT.md **Goal:**
Optimize feedback loops for AI coding agents

---

## 🎯 Quick Start (5 Minutes)

### Option 1: Automated Setup (Recommended)

```bash
# Run the automated setup script
./scripts/setup-qa-improvements.sh

# This will install and configure:
# - Vitest (unit testing)
# - html-validate (HTML validation)
# - @axe-core/cli (accessibility)
# - Playwright (E2E & visual regression)
```

### Option 2: Manual Review First

```bash
# Read the audit first
cat BUILD-QA-PROCESS-AUDIT.md | less

# Then run setup when ready
./scripts/setup-qa-improvements.sh
```

---

## 📋 Implementation Checklist

### Week 1: Critical Fixes (HIGH Priority)

#### Day 1: Fix CI/CD Silent Failures ✅

**Current Problem:**

```yaml
# .github/workflows/ci-cd.yml has:
continue-on-error: true # ❌ Hides failures!
```

**Fix:**

```bash
# 1. Edit .github/workflows/ci-cd.yml
code .github/workflows/ci-cd.yml

# 2. Remove these lines:
#   continue-on-error: true  (appears 3 times)

# 3. Make quality gates mandatory
```

**Files to edit:**

- `.github/workflows/ci-cd.yml` (lines with `continue-on-error`)

**Result:** CI/CD will fail properly when issues exist, providing clear
feedback.

---

#### Day 2: Add HTML Validation ✅

**Setup (automated in script):**

```bash
npm install --save-dev html-validate
```

**Manual steps:**

```bash
# 1. Verify .htmlvalidate.json exists
cat .htmlvalidate.json

# 2. Test it
npm run build
npm run validate:html

# 3. Fix any errors found
```

**Expected output:**

```bash
✅ 26 files validated
❌ 3 errors found in 2 files
  _site/index.html:45:12
    error: Missing alt attribute on <img>
```

---

#### Day 3: Improve Error Messages ✅

**Update audit script:**

```bash
# Edit scripts/audit-all-pages.js
code scripts/audit-all-pages.js
```

**Add to error reporting:**

```javascript
// Add line numbers, column numbers, and fix suggestions
function reportError(error) {
  const { file, type, message, line, column, fix, docs } = error;

  console.log(
    `  ${colors.red}✖${colors.reset} ${file}${line ? `:${line}:${column}` : ''}`
  );
  console.log(`    ${type}: ${message}`);

  if (fix) {
    console.log(`    ${colors.blue}💡 Fix:${colors.reset} ${fix}`);
  }

  if (docs) {
    console.log(`    ${colors.blue}📚 Docs:${colors.reset} ${docs}`);
  }

  console.log('');
}
```

---

#### Day 4-5: Add Unit Testing Framework ✅

**Already set up by script!**

**Write your first tests:**

```bash
# 1. Create test for date filter
cat > tests/unit/filters.test.js << 'EOF'
import { describe, it, expect } from 'vitest';

// Import your Eleventy config to test filters
// For now, a simple example:

describe('Date Formatting', () => {
  it('should format dates correctly', () => {
    const date = new Date('2025-10-28');
    // Test your readableDate filter here
    expect(date).toBeInstanceOf(Date);
  });
});
EOF

# 2. Run tests
npm run test:unit

# 3. Watch mode while developing
npm run test:watch
```

**Create tests for:**

- [ ] Eleventy filters (date formatting, etc.)
- [ ] Collection sorting logic
- [ ] Any utility functions
- [ ] Data transformations

---

### Week 2: Accessibility & E2E

#### Day 6-7: Add Accessibility Testing ✅

**Already set up by script!**

**Run accessibility tests:**

```bash
# 1. Build site
npm run build

# 2. Run axe tests
npm run test:a11y

# 3. Fix any violations
```

**Add to CI/CD:**

```yaml
# .github/workflows/ci-cd.yml
- name: Run accessibility tests
  run: |
    npm run build
    npm run test:a11y
  # NO continue-on-error!
```

---

#### Day 8-10: Add E2E Tests ✅

**Already set up by script!**

**Write more E2E tests:**

```bash
# 1. Create lesson navigation test
cat > tests/e2e/lesson-navigation.spec.js << 'EOF'
const { test, expect } = require('@playwright/test');

test.describe('Lesson Navigation', () => {
  test('should navigate through all lessons', async ({ page }) => {
    await page.goto('/lessons/01-what-is-this/');

    // Click next lesson
    await page.click('text=Next Lesson');
    await expect(page).toHaveURL(/02-why-quality-gates/);

    // Verify content loaded
    await expect(page.locator('h1')).toContainText('Why Quality Gates');
  });

  test('should show lesson list', async ({ page }) => {
    await page.goto('/lessons/');

    const lessons = page.locator('.lesson-card');
    await expect(lessons).toHaveCount(10);
  });
});
EOF

# 2. Run E2E tests
npm run test:e2e

# 3. Run with UI for debugging
npx playwright test --ui
```

---

### Week 3: Visual Regression & PR Automation

#### Day 11-12: Visual Regression Testing ✅

**Create baseline screenshots:**

```bash
# 1. Run tests to create baselines
npm run test:visual

# 2. Review screenshots in tests/e2e/screenshots/
```

**Add visual tests:**

```bash
cat > tests/e2e/visual-regression.spec.js << 'EOF'
const { test, expect } = require('@playwright/test');

test.describe('Visual Regression', () => {
  test('homepage matches baseline', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      maxDiffPixels: 100
    });
  });

  test('lesson page matches baseline', async ({ page }) => {
    await page.goto('/lessons/01-what-is-this/');
    await expect(page).toHaveScreenshot('lesson-01.png', {
      fullPage: true
    });
  });

  test('mobile view matches baseline', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage-mobile.png');
  });
});
EOF
```

---

#### Day 13-15: PR Automation

**Add PR comment workflow:**

```bash
# Create new workflow file
cat > .github/workflows/pr-comment.yml << 'EOF'
name: PR Quality Report

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: Run quality checks
        id: checks
        run: |
          npm run ci:pr > report.txt 2>&1 || true

          # Parse results
          LINT_ERRORS=$(grep -c "✖" report.txt || echo "0")
          TEST_FAILURES=$(grep -c "FAIL" report.txt || echo "0")

          echo "lint_errors=$LINT_ERRORS" >> $GITHUB_OUTPUT
          echo "test_failures=$TEST_FAILURES" >> $GITHUB_OUTPUT

      - name: Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            const lintErrors = '${{ steps.checks.outputs.lint_errors }}';
            const testFailures = '${{ steps.checks.outputs.test_failures }}';

            const comment = `
            ## 📊 Quality Check Results

            - **Lint Errors:** ${lintErrors}
            - **Test Failures:** ${testFailures}

            ${lintErrors === '0' && testFailures === '0'
              ? '✅ All checks passed! Ready to merge.'
              : '❌ Please fix issues before merging.'}

            <details>
            <summary>View full report</summary>

            \`\`\`
            $(cat report.txt)
            \`\`\`
            </details>
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
EOF
```

---

### Month 2: Advanced Features

#### Week 4: Dependency Management

**Set up Dependabot:**

```bash
# Create dependabot config
cat > .github/dependabot.yml << 'EOF'
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    reviewers:
      - "kaw393939"
    labels:
      - "dependencies"
      - "automated"
    commit-message:
      prefix: "chore"
      include: "scope"
EOF
```

**Add security audit:**

```bash
# Add to CI/CD
- name: Security audit
  run: npm audit --audit-level=moderate
```

---

#### Week 5-6: Performance Tracking

**Set up persistent Lighthouse storage:**

```javascript
// Update lighthouserc.js
module.exports = {
  ci: {
    collect: {
      // ... existing config
    },
    upload: {
      target: 'temporary-public-storage', // Change this later
      // target: 'lhci',
      // serverBaseUrl: 'https://your-lhci-server.com',
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'categories:performance': ['error', { minScore: 0.95 }],
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'categories:best-practices': ['error', { minScore: 0.95 }],
        'categories:seo': ['error', { minScore: 0.95 }],
      },
    },
  },
};
```

---

## 🔄 New Development Workflow

### For AI Agents (Automated Feedback)

```bash
# 1. Make code changes
# (AI agent writes code)

# 2. Run quick check (< 10 seconds)
npm run check

# 3. If issues found:
#    - Read error messages (now with line numbers!)
#    - Apply suggested fixes
#    - Re-run check

# 4. Commit (pre-commit hooks run automatically)
git add .
git commit -m "feat: add new feature"

# 5. Push (pre-push hooks run comprehensive checks)
git push

# 6. CI/CD runs (now fails properly on issues)
# 7. PR gets automatic quality comment
```

### For Developers (Manual Review)

```bash
# Quick iteration
npm run check         # Fast feedback (< 10s)
npm run test:watch    # Tests in watch mode

# Before commit
npm run lint          # Full linting
npm run test          # All tests

# Before push
npm run ci:pr         # Full CI simulation locally

# Visual testing
npm run test:e2e      # E2E tests
npx playwright test --ui  # Interactive mode
```

---

## 📊 Success Metrics

### Track Weekly

1. **Feedback Speed**
   - [ ] Local validation: < 10 seconds
   - [ ] Pre-commit: < 5 seconds
   - [ ] CI/CD: < 5 minutes

2. **Error Detection**
   - [ ] Catch 95%+ issues locally
   - [ ] < 5% false positives

3. **Test Coverage**
   - [ ] Unit tests: 80%+ coverage
   - [ ] E2E tests: All critical paths
   - [ ] Visual regression: Key pages

4. **Build Health**
   - [ ] CI/CD success rate: 80-90%
   - [ ] Issues caught before merge: 95%+

---

## 🆘 Troubleshooting

### Tests fail with "Cannot find module"

```bash
# Install dependencies
npm ci

# Verify installation
npm run test:unit -- --version
```

### Playwright tests timeout

```bash
# Increase timeout
# In playwright.config.js:
timeout: 30000,  // 30 seconds

# Or use --timeout flag
npx playwright test --timeout=60000
```

### HTML validation too strict

```bash
# Edit .htmlvalidate.json
# Add rules to ignore:
{
  "rules": {
    "specific-rule": "off"
  }
}
```

### Pre-push hook too slow

```bash
# Edit .husky/pre-push
# Remove some checks for faster pushes
# Keep full checks in CI/CD
```

---

## 📚 Documentation

### For Team

- [ ] `BUILD-QA-PROCESS-AUDIT.md` - Full audit
- [ ] `QA-PROCESS-ACTION-PLAN.md` - This file
- [ ] `docs/testing-guide.md` - How to write tests
- [ ] `docs/error-codes.md` - Error reference

### For AI Agents

- [ ] `docs/ai-agent-guide.md` - AI-specific instructions
- [ ] Clear error messages with fixes
- [ ] Example tests to learn from
- [ ] Automated feedback at every step

---

## ✅ Completion Checklist

### Infrastructure

- [ ] Vitest installed and configured
- [ ] Playwright installed and configured
- [ ] html-validate installed and configured
- [ ] axe-core installed and configured
- [ ] Pre-push hook created

### Testing

- [ ] Unit tests written (target: 10+ tests)
- [ ] Integration tests written (target: 5+ tests)
- [ ] E2E tests written (target: 10+ scenarios)
- [ ] Visual regression baselines created
- [ ] Accessibility tests passing

### CI/CD

- [ ] Removed all `continue-on-error: true`
- [ ] Added test jobs to workflow
- [ ] Added validation jobs
- [ ] Added PR comment automation
- [ ] Added Dependabot

### Documentation

- [ ] Testing guide written
- [ ] Error codes documented
- [ ] AI agent guide created
- [ ] README updated with new scripts

---

## 🎯 Final Goal

**A build/QA process that:**

- ✅ Provides immediate feedback (< 10s locally)
- ✅ Catches issues before commit
- ✅ Fails properly in CI/CD (no silent failures)
- ✅ Gives actionable error messages
- ✅ Prevents technical debt accumulation
- ✅ Optimizes AI agent learning loops

**Timeline:** 3-4 weeks to full implementation

**Outcome:** Technical debt score improvement from B+ (86%) to A+ (95%+)

---

_Start with the automated script, then follow this plan for complete
implementation._
