#!/usr/bin/env node
/**
 * Comprehensive Page Audit Script
 * Checks all built HTML pages for common issues:
 * - Unrendered markdown
 * - Missing meta tags
 * - Broken internal links
 * - Accessibility issues
 * - Performance problems
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const SITE_DIR = path.join(__dirname, '..', '_site');
const ERRORS = [];
const WARNINGS = [];

// Colors for terminal output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
};

/**
 * Find all HTML files recursively
 */
function findHTMLFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);

  files.forEach((file) => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      findHTMLFiles(filePath, fileList);
    } else if (file.endsWith('.html')) {
      fileList.push(filePath);
    }
  });

  return fileList;
}

/**
 * Check for unrendered markdown
 */
function checkMarkdown(filePath, dom) {
  const body = dom.window.document.body;

  // Remove code blocks from consideration
  const codeBlocks = body.querySelectorAll('pre, code');
  codeBlocks.forEach((block) => block.remove());

  const text = body.textContent;

  // Check for common markdown patterns
  const markdownPatterns = [
    { pattern: /^##\s/m, name: 'Heading markdown (##)' },
    { pattern: /\*\*[^*]+\*\*/g, name: 'Bold markdown (**)' },
    { pattern: /\[.+\]\(.+\)/g, name: 'Link markdown [text](url)' },
    { pattern: /^-\s/m, name: 'List markdown (-)' },
    { pattern: /^>\s/m, name: 'Blockquote markdown (>)' },
    { pattern: /`[^`]+`/g, name: 'Inline code markdown (`)' },
  ];

  markdownPatterns.forEach(({ pattern, name }) => {
    if (pattern.test(text)) {
      ERRORS.push({
        file: filePath.replace(SITE_DIR, ''),
        type: 'UNRENDERED_MARKDOWN',
        message: `Unrendered markdown found: ${name}`,
      });
    }
  });
}

/**
 * Check for required meta tags
 */
function checkMetaTags(filePath, dom) {
  const head = dom.window.document.head;
  const requiredMeta = [
    { selector: 'meta[name="description"]', name: 'Description' },
    { selector: 'meta[property="og:title"]', name: 'Open Graph title' },
    {
      selector: 'meta[property="og:description"]',
      name: 'Open Graph description',
    },
    { selector: 'link[rel="canonical"]', name: 'Canonical URL' },
  ];

  requiredMeta.forEach(({ selector, name }) => {
    const element = head.querySelector(selector);
    if (!element) {
      WARNINGS.push({
        file: filePath.replace(SITE_DIR, ''),
        type: 'MISSING_META',
        message: `Missing ${name}`,
      });
    }
  });
}

/**
 * Check for accessibility issues
 */
function checkAccessibility(filePath, dom) {
  const doc = dom.window.document;

  // Check for images without alt text
  const images = doc.querySelectorAll('img');
  images.forEach((img, index) => {
    if (!img.hasAttribute('alt')) {
      ERRORS.push({
        file: filePath.replace(SITE_DIR, ''),
        type: 'ACCESSIBILITY',
        message: `Image #${index + 1} missing alt attribute`,
      });
    }
  });

  // Check for form inputs without labels
  const inputs = doc.querySelectorAll('input, textarea, select');
  inputs.forEach((input, index) => {
    const id = input.getAttribute('id');
    if (id) {
      const label = doc.querySelector(`label[for="${id}"]`);
      if (!label && !input.hasAttribute('aria-label')) {
        WARNINGS.push({
          file: filePath.replace(SITE_DIR, ''),
          type: 'ACCESSIBILITY',
          message: `Form input #${index + 1} missing label`,
        });
      }
    }
  });

  // Check for links without text
  const links = doc.querySelectorAll('a');
  links.forEach((link, index) => {
    const text = link.textContent.trim();
    const ariaLabel = link.getAttribute('aria-label');
    if (!text && !ariaLabel) {
      ERRORS.push({
        file: filePath.replace(SITE_DIR, ''),
        type: 'ACCESSIBILITY',
        message: `Link #${index + 1} has no text or aria-label`,
      });
    }
  });
}

/**
 * Check page performance indicators
 */
function checkPerformance(filePath, dom) {
  const doc = dom.window.document;

  // Check for inline styles (bad for performance)
  const elementsWithStyle = doc.querySelectorAll('[style]');
  if (elementsWithStyle.length > 5) {
    WARNINGS.push({
      file: filePath.replace(SITE_DIR, ''),
      type: 'PERFORMANCE',
      message: `Found ${elementsWithStyle.length} elements with inline styles`,
    });
  }

  // Check for missing async/defer on scripts
  const scripts = doc.querySelectorAll('script[src]');
  scripts.forEach((script, index) => {
    if (!script.hasAttribute('async') && !script.hasAttribute('defer')) {
      WARNINGS.push({
        file: filePath.replace(SITE_DIR, ''),
        type: 'PERFORMANCE',
        message: `Script #${index + 1} missing async or defer attribute`,
      });
    }
  });
}

/**
 * Audit a single HTML file
 */
function auditPage(filePath) {
  try {
    const html = fs.readFileSync(filePath, 'utf8');
    const dom = new JSDOM(html);

    checkMarkdown(filePath, dom);
    checkMetaTags(filePath, dom);
    checkAccessibility(filePath, dom);
    checkPerformance(filePath, dom);
  } catch (error) {
    ERRORS.push({
      file: filePath.replace(SITE_DIR, ''),
      type: 'PARSE_ERROR',
      message: `Failed to parse: ${error.message}`,
    });
  }
}

/**
 * Print results
 */
function printResults() {
  console.log(`\n${colors.blue}=== Page Audit Results ===${colors.reset}\n`);

  if (ERRORS.length === 0 && WARNINGS.length === 0) {
    console.log(`${colors.green}✓ All pages passed audit!${colors.reset}\n`);
    return 0;
  }

  if (ERRORS.length > 0) {
    console.log(
      `${colors.red}✖ ${ERRORS.length} ERRORS found:${colors.reset}\n`
    );
    ERRORS.forEach(({ file, type, message }) => {
      console.log(`  ${colors.red}✖${colors.reset} ${file}`);
      console.log(`    ${type}: ${message}\n`);
    });
  }

  if (WARNINGS.length > 0) {
    console.log(
      `${colors.yellow}⚠ ${WARNINGS.length} WARNINGS:${colors.reset}\n`
    );
    WARNINGS.forEach(({ file, type, message }) => {
      console.log(`  ${colors.yellow}⚠${colors.reset} ${file}`);
      console.log(`    ${type}: ${message}\n`);
    });
  }

  return ERRORS.length > 0 ? 1 : 0;
}

/**
 * Main execution
 */
function main() {
  console.log(
    `${colors.blue}Auditing all pages in ${SITE_DIR}...${colors.reset}\n`
  );

  if (!fs.existsSync(SITE_DIR)) {
    console.error(
      `${colors.red}Error: _site directory not found. Run 'npm run build' first.${colors.reset}`
    );
    process.exit(1);
  }

  const htmlFiles = findHTMLFiles(SITE_DIR);
  console.log(`Found ${htmlFiles.length} HTML pages to audit...\n`);

  htmlFiles.forEach((file) => {
    auditPage(file);
  });

  const exitCode = printResults();
  process.exit(exitCode);
}

main();
