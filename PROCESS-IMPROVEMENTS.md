# Development & Deployment Process Improvements

**Date:** October 30, 2025 **Context:** Lessons learned from link checker
failures, CI/CD issues, and path prefix migration

---

## 🎯 Executive Summary

Our recent deployment to GitHub Pages with custom domain (eaikw.com) revealed
several process gaps:

- Link checker failures only caught in CI, not locally
- Path prefix confusion (`/is117_ai_test_practice/` → `/`)
- Multiple iterations to fix linting issues
- Manual detection of broken links across 13+ files

**Recommendation:** Implement automated checks earlier in the development
workflow.

---

## 📊 Current Process Analysis

### What Works Well ✅

1. **Pre-commit Hooks** - Auto-formatting with Prettier prevents style issues
2. **Comprehensive Linting** - ESLint, Stylelint, Markdownlint, JSCPD all
   integrated
3. **GitHub Actions CI** - Catches issues before deployment
4. **Local Development Server** - Fast feedback loop with Eleventy watch mode

### Pain Points 🔴

1. **Link Checking Happens Too Late**
   - Only runs in CI, not pre-commit
   - Broken links discovered after push
   - Requires multiple fix-commit-push cycles

2. **Path Prefix Management**
   - No validation that paths match config
   - Manual search-and-replace across 13 files
   - Easy to miss hardcoded URLs

3. **Environment Configuration**
   - `pathPrefix` not dynamically enforced
   - Template files don't validate against config
   - Documentation can get out of sync

4. **CI Feedback Loop**
   - 3-5 minutes to discover link issues
   - No local preview of CI checks
   - Manual interpretation of link checker output

---

## 🚀 Proposed Improvements

### 1. Pre-Commit Link Validation

**Problem:** Broken links only caught in CI after push.

**Solution:** Add link checking to pre-commit hooks with smart scoping.

```javascript
// .husky/pre-commit (add after linters)
# Quick link check on staged files only
npm run lint:links:staged
```

```json
// package.json
{
  "scripts": {
    "lint:links:staged": "node scripts/check-staged-links.js"
  }
}
```

**Implementation:**

```javascript
// scripts/check-staged-links.js
const { execSync } = require('child_process');
const path = require('path');

// Get staged markdown files
const staged = execSync('git diff --cached --name-only --diff-filter=ACMR')
  .toString()
  .split('\n')
  .filter((f) => f.endsWith('.md') && f.includes('docs/lessons'));

if (staged.length === 0) {
  console.log('✓ No lesson files staged for commit');
  process.exit(0);
}

// Quick check only on changed files
try {
  execSync(
    `markdown-link-check ${staged.join(' ')} --config .markdown-link-check.json --quiet`,
    {
      stdio: 'inherit',
    }
  );
  console.log(`✓ Checked ${staged.length} staged markdown files`);
} catch (error) {
  console.error('✗ Broken links detected in staged files');
  process.exit(1);
}
```

**Benefits:**

- Catches broken links before push
- Only checks changed files (fast)
- Provides immediate feedback
- Prevents broken main branch

**Trade-offs:**

- Slightly slower commits (~2-3 seconds)
- May need `--no-verify` for urgent fixes
- Requires network access for external links

---

### 2. Path Prefix Configuration Management

**Problem:** Hardcoded paths scattered across templates.

**Solution:** Centralize path configuration and validate at build time.

```javascript
// .eleventy.js
const config = {
  pathPrefix: process.env.ELEVENTY_ENV === 'production' ? '/' : '/',
  domain:
    process.env.ELEVENTY_ENV === 'production'
      ? 'https://eaikw.com'
      : 'http://localhost:8080',
};

// Validate templates don't have hardcoded paths
module.exports = function (eleventyConfig) {
  // Add global data
  eleventyConfig.addGlobalData('site', {
    url: config.domain,
    pathPrefix: config.pathPrefix,
  });

  // Validate on build
  eleventyConfig.on('eleventy.after', async () => {
    const validatePaths = require('./scripts/validate-paths');
    await validatePaths(config.pathPrefix);
  });

  return {
    pathPrefix: config.pathPrefix,
    // ... rest of config
  };
};
```

```javascript
// scripts/validate-paths.js
const fs = require('fs');
const path = require('path');
const glob = require('glob');

module.exports = async function validatePaths(expectedPrefix) {
  const files = glob.sync('src/**/*.{njk,md}');
  const forbidden = [
    '/is117_ai_test_practice/',
    'https://kaw393939.github.io/is117_ai_test_practice',
  ];

  let errors = [];

  for (const file of files) {
    const content = fs.readFileSync(file, 'utf8');
    for (const pattern of forbidden) {
      if (content.includes(pattern)) {
        errors.push(`${file}: Found hardcoded path "${pattern}"`);
      }
    }
  }

  if (errors.length > 0) {
    console.error('❌ Path validation failed:');
    errors.forEach((e) => console.error(`  ${e}`));
    process.exit(1);
  }

  console.log('✓ All paths validated');
};
```

**Template Usage:**

```njk
{# ❌ OLD - Hardcoded #}
<a href="/is117_ai_test_practice/lessons/">View Lessons</a>

{# ✅ NEW - Dynamic #}
<a href="{{ site.url }}{{ site.pathPrefix }}lessons/">View Lessons</a>
```

**Benefits:**

- Single source of truth for paths
- Prevents hardcoded URLs
- Easy to update for new domains
- Catches issues at build time

---

### 3. Local CI Preview

**Problem:** Can't run full CI checks locally before push.

**Solution:** Add local CI simulation script.

```json
// package.json
{
  "scripts": {
    "ci:local": "node scripts/run-local-ci.js",
    "ci:fast": "npm run lint && npm run build"
  }
}
```

```javascript
// scripts/run-local-ci.js
const { execSync } = require('child_process');

console.log('🔍 Running local CI checks...\n');

const steps = [
  { name: 'Lint JavaScript', cmd: 'npm run lint:js' },
  { name: 'Lint CSS', cmd: 'npm run lint:css' },
  { name: 'Lint Markdown', cmd: 'npm run lint:md' },
  { name: 'Check Formatting', cmd: 'npm run lint:format' },
  { name: 'Check Duplication', cmd: 'npm run lint:duplication' },
  { name: 'Check MD Links', cmd: 'npm run lint:links:md' },
  { name: 'Build Site', cmd: 'npm run build' },
  { name: 'Check HTML Links', cmd: 'npm run lint:links:html' },
];

let failed = [];

for (const step of steps) {
  process.stdout.write(`⏳ ${step.name}... `);
  try {
    execSync(step.cmd, { stdio: 'pipe' });
    console.log('✅');
  } catch (error) {
    console.log('❌');
    failed.push(step.name);
  }
}

if (failed.length > 0) {
  console.error(`\n❌ ${failed.length} checks failed:`);
  failed.forEach((name) => console.error(`   - ${name}`));
  process.exit(1);
}

console.log('\n✅ All CI checks passed locally!');
```

**Benefits:**

- Run full CI suite before push
- Faster feedback than GitHub Actions
- Confidence before commits
- Saves CI minutes

---

### 4. Link Checker Configuration Improvements

**Problem:** Link checker too strict for development, too lenient for
production.

**Solution:** Environment-specific link checking.

```json
// .markdown-link-check.dev.json
{
  "ignorePatterns": [
    { "pattern": "^http://localhost" },
    { "pattern": "^https://example.com" },
    { "pattern": "^/" }
  ],
  "timeout": "5s",
  "retryCount": 1,
  "aliveStatusCodes": [200, 206, 301, 302, 307, 308, 999]
}
```

```json
// .markdown-link-check.prod.json
{
  "ignorePatterns": [{ "pattern": "^http://localhost" }],
  "timeout": "20s",
  "retryCount": 3,
  "retryOn429": true,
  "fallbackRetryDelay": "30s",
  "aliveStatusCodes": [200, 206, 301, 302, 307, 308, 999]
}
```

```json
// package.json
{
  "scripts": {
    "lint:links:md": "markdown-link-check docs/**/*.md README.md --config .markdown-link-check.dev.json --quiet",
    "lint:links:md:prod": "markdown-link-check docs/**/*.md README.md --config .markdown-link-check.prod.json --quiet"
  }
}
```

**Benefits:**

- Fast checks during development
- Thorough checks in CI/production
- Reduces false positives locally

---

### 5. Automated Path Migration Script

**Problem:** Manual find-and-replace across many files is error-prone.

**Solution:** Create migration scripts for path changes.

```javascript
// scripts/migrate-paths.js
const fs = require('fs');
const glob = require('glob');

const migrations = [
  {
    from: '/is117_ai_test_practice/',
    to: '/',
    files: 'src/**/*.{njk,md,html}',
  },
  {
    from: 'https://kaw393939.github.io/is117_ai_test_practice',
    to: 'https://eaikw.com',
    files: '{src,docs}/**/*.{njk,md,html,js}',
  },
  {
    from: 'localhost:8080/is117_ai_test_practice',
    to: 'localhost:8080',
    files: 'docs/**/*.md',
  },
];

console.log('🔄 Starting path migration...\n');

let totalChanges = 0;

for (const migration of migrations) {
  const files = glob.sync(migration.files);
  let changed = 0;

  for (const file of files) {
    const content = fs.readFileSync(file, 'utf8');
    const newContent = content.replaceAll(migration.from, migration.to);

    if (content !== newContent) {
      fs.writeFileSync(file, newContent);
      changed++;
    }
  }

  console.log(`✅ ${migration.from} → ${migration.to}: ${changed} files`);
  totalChanges += changed;
}

console.log(`\n🎉 Migration complete! ${totalChanges} files updated.`);
console.log('⚠️  Please review changes and run: git diff');
```

**Usage:**

```bash
npm run migrate:paths
git diff  # Review changes
git add -A && git commit -m "Migrate to new path prefix"
```

---

### 6. Link Health Dashboard

**Problem:** Hard to track link health over time.

**Solution:** Generate link health reports.

```javascript
// scripts/link-health-report.js
const { execSync } = require('child_process');
const fs = require('fs');

function runLinkCheck() {
  try {
    execSync('npm run lint:links:html', { stdio: 'pipe' });
    return { passed: true, broken: 0 };
  } catch (error) {
    const output = error.stdout.toString();
    const match = output.match(/Detected (\d+) broken links/);
    return {
      passed: false,
      broken: match ? parseInt(match[1]) : 0,
      details: output,
    };
  }
}

const result = runLinkCheck();
const report = {
  timestamp: new Date().toISOString(),
  passed: result.passed,
  brokenLinks: result.broken,
  commit: execSync('git rev-parse HEAD').toString().trim(),
  branch: execSync('git branch --show-current').toString().trim(),
};

fs.writeFileSync('link-health-report.json', JSON.stringify(report, null, 2));

console.log(`📊 Link Health Report Generated`);
console.log(`   Status: ${result.passed ? '✅ PASS' : '❌ FAIL'}`);
console.log(`   Broken Links: ${result.broken}`);
console.log(`   Report: link-health-report.json`);

if (!result.passed) process.exit(1);
```

---

## 🎯 Priority Implementation Plan

### Phase 1: Quick Wins (1-2 days)

1. ✅ Add path validation script
2. ✅ Create local CI runner
3. ✅ Add migration script template

### Phase 2: Pre-commit Integration (2-3 days)

1. Add staged file link checking
2. Integrate path validation
3. Test with team workflow

### Phase 3: Configuration Management (3-5 days)

1. Centralize path prefix config
2. Update all templates to use global data
3. Add build-time validation

### Phase 4: Monitoring (Ongoing)

1. Link health dashboard
2. CI performance metrics
3. Regular link audits

---

## 📈 Expected Impact

### Development Velocity

- **Before:** 3-5 CI cycles to fix link issues
- **After:** Catch 90% of issues pre-commit
- **Time Saved:** ~30-45 minutes per deployment

### Code Quality

- **Before:** Manual path management, prone to errors
- **After:** Automated validation, single source of truth
- **Error Reduction:** ~80% fewer path-related bugs

### Developer Experience

- **Before:** Push → wait → fail → fix → repeat
- **After:** Local validation → confident push → clean CI
- **Frustration:** Much lower! 😊

---

## 🔧 Implementation Checklist

- [ ] Create `scripts/check-staged-links.js`
- [ ] Create `scripts/validate-paths.js`
- [ ] Create `scripts/run-local-ci.js`
- [ ] Create `scripts/migrate-paths.js`
- [ ] Update `.husky/pre-commit` hook
- [ ] Add path validation to build process
- [ ] Create environment-specific link configs
- [ ] Update templates to use global site config
- [ ] Document new workflow in DEVELOPMENT.md
- [ ] Train team on new processes

---

## 🤔 Discussion Points

### Should Link Checking Be Mandatory Pre-Commit?

**Pro:**

- Prevents broken links from entering main branch
- Forces developers to fix issues immediately
- Maintains high quality standards

**Con:**

- Slows down commit process (2-5 seconds)
- May block urgent hotfixes
- Requires network access

**Recommendation:** Make it mandatory but allow `--no-verify` bypass for
emergencies.

### Should We Use a Link Checking Service?

Services like **Dead Link Checker** or **Broken Link Checker** offer:

- Scheduled link audits
- Email notifications
- Historical tracking
- No CI time consumption

**Cost:** $10-50/month **Benefit:** Proactive monitoring vs reactive fixing

**Recommendation:** Start with local tools, evaluate service if link issues
persist.

---

## 📚 Additional Resources

- [Eleventy Config Documentation](https://www.11ty.dev/docs/config/)
- [Husky Pre-commit Hooks](https://typicode.github.io/husky/)
- [Markdown Link Check](https://github.com/tcort/markdown-link-check)
- [Linkinator](https://github.com/JustinBeckwith/linkinator)

---

## 🎓 Lessons Learned

1. **Fail Fast, Fail Early** - Validation should happen as close to code
   authoring as possible
2. **Single Source of Truth** - Configuration duplication leads to inconsistency
3. **Automate Everything** - Manual processes will be forgotten or skipped
4. **Test Locally First** - CI should be confirmation, not discovery
5. **Make It Easy to Do Right** - Good processes should feel natural, not
   burdensome

---

## 📝 Next Steps

1. **Team Review** - Discuss proposed changes, gather feedback
2. **Prototype** - Implement Phase 1 in feature branch
3. **Test** - Run through complete development cycle
4. **Document** - Update all relevant documentation
5. **Deploy** - Roll out to team with training session
6. **Monitor** - Track adoption and effectiveness
7. **Iterate** - Refine based on real-world usage

---

**Last Updated:** October 30, 2025 **Author:** Development Team **Status:**
Proposed - Awaiting Review
