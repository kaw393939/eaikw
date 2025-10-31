#!/bin/bash
# Quick Start: Implement Critical Audit Recommendations
# Run this to set up the most important missing pieces

set -e

echo "🚀 Implementing Build & QA Process Improvements"
echo "================================================"
echo ""

# 1. Install Testing Framework
echo "📦 Installing Vitest (unit testing)..."
npm install --save-dev vitest @vitest/ui @vitest/coverage-v8 jsdom

# 2. Install HTML Validation
echo "📦 Installing html-validate..."
npm install --save-dev html-validate

# 3. Install Accessibility Testing
echo "📦 Installing axe-core for accessibility..."
npm install --save-dev @axe-core/cli @axe-core/puppeteer

# 4. Install Visual Regression Testing
echo "📦 Installing Playwright for E2E and visual testing..."
npm install --save-dev @playwright/test
npx playwright install --with-deps chromium

# 5. Create test directories
echo "📁 Creating test directory structure..."
mkdir -p tests/{unit,integration,e2e}

# 6. Create Vitest config
echo "⚙️  Creating vitest.config.js..."
cat > vitest.config.js << 'EOF'
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        '_site/',
        'tests/',
        '*.config.js',
      ],
    },
  },
});
EOF

# 7. Create Playwright config
echo "⚙️  Creating playwright.config.js..."
cat > playwright.config.js << 'EOF'
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:8080/is117_ai_test_practice',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'mobile',
      use: { ...devices['iPhone 13'] },
    },
  ],
  webServer: {
    command: 'npm start',
    url: 'http://localhost:8080',
    reuseExistingServer: !process.env.CI,
  },
});
EOF

# 8. Create HTML validation config
echo "⚙️  Creating .htmlvalidate.json..."
cat > .htmlvalidate.json << 'EOF'
{
  "extends": ["html-validate:recommended"],
  "rules": {
    "attr-quotes": "error",
    "doctype-html": "error",
    "void-style": ["error", "selfclose"],
    "no-trailing-whitespace": "off",
    "require-sri": "off",
    "no-inline-style": "off"
  }
}
EOF

# 9. Create example unit test
echo "📝 Creating example unit test..."
cat > tests/unit/example.test.js << 'EOF'
import { describe, it, expect } from 'vitest';

describe('Example Test Suite', () => {
  it('should pass basic assertion', () => {
    expect(1 + 1).toBe(2);
  });

  it('should handle strings', () => {
    const greeting = 'Hello, World!';
    expect(greeting).toContain('World');
  });
});
EOF

# 10. Create example E2E test
echo "📝 Creating example E2E test..."
cat > tests/e2e/homepage.spec.js << 'EOF'
const { test, expect } = require('@playwright/test');

test.describe('Homepage', () => {
  test('should load successfully', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/AI-Assisted Web Development/);
  });

  test('should have working navigation', async ({ page }) => {
    await page.goto('/');
    await page.click('text=Lessons');
    await expect(page).toHaveURL(/\/lessons/);
  });

  test('should be responsive', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    const hero = page.locator('.hero-explorer');
    await expect(hero).toBeVisible();
  });
});
EOF

# 11. Create internal link validator
echo "📝 Creating internal link validator script..."
cat > scripts/validate-internal-links.js << 'EOF'
#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const SITE_DIR = path.join(__dirname, '..', '_site');
const errors = [];

function getAllLinks(html, filePath) {
  const dom = new JSDOM(html);
  const links = dom.window.document.querySelectorAll('a[href]');

  return Array.from(links)
    .map(link => ({
      href: link.getAttribute('href'),
      text: link.textContent.trim(),
      source: filePath
    }))
    .filter(link =>
      // Only internal links
      !link.href.startsWith('http') &&
      !link.href.startsWith('mailto:') &&
      !link.href.startsWith('#')
    );
}

function validateLink(link) {
  let targetPath = link.href;

  // Remove leading slash and add site directory
  if (targetPath.startsWith('/')) {
    targetPath = targetPath.substring(1);
  }

  const fullPath = path.join(SITE_DIR, targetPath);

  // Check if file exists (try with and without index.html)
  const possiblePaths = [
    fullPath,
    path.join(fullPath, 'index.html'),
    fullPath + '.html'
  ];

  const exists = possiblePaths.some(p => fs.existsSync(p));

  if (!exists) {
    errors.push({
      source: link.source.replace(SITE_DIR, ''),
      href: link.href,
      text: link.text
    });
  }
}

function scanDirectory(dir) {
  const files = fs.readdirSync(dir);

  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      scanDirectory(filePath);
    } else if (file.endsWith('.html')) {
      const html = fs.readFileSync(filePath, 'utf8');
      const links = getAllLinks(html, filePath);
      links.forEach(validateLink);
    }
  });
}

console.log('🔍 Validating internal links...\n');
scanDirectory(SITE_DIR);

if (errors.length > 0) {
  console.log(`❌ Found ${errors.length} broken internal links:\n`);
  errors.forEach(error => {
    console.log(`  ${error.source}`);
    console.log(`    → ${error.href} (text: "${error.text}")`);
  });
  process.exit(1);
} else {
  console.log('✅ All internal links are valid!');
  process.exit(0);
}
EOF

chmod +x scripts/validate-internal-links.js

# 12. Update package.json scripts
echo "⚙️  Updating package.json scripts..."
node << 'EOF'
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));

// Add new scripts
Object.assign(pkg.scripts, {
  // Testing
  "test": "npm run lint && npm run test:unit && npm run test:integration && npm run build:validate",
  "test:unit": "vitest run tests/unit",
  "test:integration": "vitest run tests/integration",
  "test:e2e": "playwright test",
  "test:visual": "playwright test --update-snapshots",
  "test:watch": "vitest watch",
  "test:coverage": "vitest run --coverage",
  "test:a11y": "axe '_site/**/*.html' --tags wcag2a,wcag2aa --exit",

  // Validation
  "validate:all": "npm run validate:html && npm run validate:links:internal && npm run validate:accessibility",
  "validate:html": "html-validate '_site/**/*.html'",
  "validate:links:internal": "node scripts/validate-internal-links.js",
  "validate:accessibility": "axe '_site/**/*.html' --tags wcag2a,wcag2aa --exit",

  // Build with validation
  "build:validate": "npm run build && npm run validate:all",

  // Quick check (fast feedback)
  "check": "npm run lint && npm run test:unit && npm run build",

  // CI/CD
  "ci": "npm run lint && npm run test && npm run build:validate && npm run test:e2e && npm run lighthouse",
  "ci:pr": "npm run ci && npm audit --audit-level=moderate"
});

// Update lint:js to have max-warnings
pkg.scripts["lint:js"] = "eslint \"src/**/*.js\" \".eleventy.js\" --max-warnings 0";

fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2) + '\n');
console.log('✅ package.json updated');
EOF

# 13. Create pre-push hook for comprehensive checks
echo "⚙️  Creating pre-push hook..."
cat > .husky/pre-push << 'EOF'
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

echo "🔍 Running comprehensive checks before push..."

npm run check || {
  echo "❌ Checks failed! Fix errors before pushing."
  exit 1
}

echo "✅ All checks passed! Pushing to remote..."
EOF

chmod +x .husky/pre-push

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📋 What was installed:"
echo "  - Vitest (unit testing)"
echo "  - html-validate (HTML validation)"
echo "  - @axe-core/cli (accessibility testing)"
echo "  - @playwright/test (E2E & visual regression)"
echo ""
echo "📁 Directories created:"
echo "  - tests/unit/"
echo "  - tests/integration/"
echo "  - tests/e2e/"
echo ""
echo "⚙️  Configs created:"
echo "  - vitest.config.js"
echo "  - playwright.config.js"
echo "  - .htmlvalidate.json"
echo ""
echo "🎯 New npm scripts available:"
echo "  npm run test:unit          - Run unit tests"
echo "  npm run test:e2e           - Run E2E tests"
echo "  npm run test:coverage      - Run tests with coverage"
echo "  npm run validate:html      - Validate HTML"
echo "  npm run validate:all       - Run all validators"
echo "  npm run build:validate     - Build + validate"
echo "  npm run check              - Quick quality check (< 10s)"
echo ""
echo "🚀 Next steps:"
echo "  1. Review BUILD-QA-PROCESS-AUDIT.md"
echo "  2. Run: npm run check"
echo "  3. Write more tests in tests/unit/"
echo "  4. Update CI/CD per audit recommendations"
echo "  5. Remove continue-on-error from .github/workflows/ci-cd.yml"
echo ""
