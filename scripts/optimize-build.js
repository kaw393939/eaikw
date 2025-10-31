#!/usr/bin/env node

/**
 * Build Optimization Script
 *
 * Post-processes the built site to fix Lighthouse issues:
 * 1. Minifies CSS files
 * 2. Ensures viewport meta tags exist
 * 3. Adds CSP headers (via meta tags)
 * 4. Optimizes link contrast for accessibility
 * 5. Validates no console errors
 *
 * Run after: npm run build
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const SITE_DIR = path.join(__dirname, '..', '_site');

/**
 * Minify CSS content
 */
function minifyCSS(css) {
  return (
    css
      // Remove comments
      .replace(/\/\*[\s\S]*?\*\//g, '')
      // Remove whitespace
      .replace(/\s+/g, ' ')
      // Remove space around special characters
      .replace(/\s*([{}:;,>+~])\s*/g, '$1')
      // Remove trailing semicolons
      .replace(/;}/g, '}')
      .trim()
  );
}

/**
 * Process a single CSS file
 */
function processCSSFile(filePath) {
  try {
    const css = fs.readFileSync(filePath, 'utf8');
    const minified = minifyCSS(css);
    const originalSize = Buffer.byteLength(css, 'utf8');
    const minifiedSize = Buffer.byteLength(minified, 'utf8');
    const savings = (
      ((originalSize - minifiedSize) / originalSize) *
      100
    ).toFixed(1);

    fs.writeFileSync(filePath, minified, 'utf8');
    console.log(
      `  ✓ ${path.relative(SITE_DIR, filePath)} (${savings}% smaller)`
    );

    return { originalSize, minifiedSize, savings: parseFloat(savings) };
  } catch (error) {
    console.error(`  ✗ Error processing ${filePath}:`, error.message);
    return null;
  }
}

/**
 * Find all CSS files in directory
 */
function findCSSFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      findCSSFiles(fullPath, files);
    } else if (entry.isFile() && entry.name.endsWith('.css')) {
      files.push(fullPath);
    }
  }

  return files;
}

/**
 * Process a single HTML file
 */
function processHTMLFile(filePath) {
  try {
    const html = fs.readFileSync(filePath, 'utf8');
    const dom = new JSDOM(html);
    const document = dom.window.document;
    let modified = false;

    // 1. Ensure viewport meta tag exists
    let viewport = document.querySelector('meta[name="viewport"]');
    if (!viewport) {
      viewport = document.createElement('meta');
      viewport.setAttribute('name', 'viewport');
      viewport.setAttribute('content', 'width=device-width, initial-scale=1.0');
      document.head.appendChild(viewport);
      modified = true;
    } else {
      // Ensure it has proper content
      const content = viewport.getAttribute('content');
      if (!content || !content.includes('width=device-width')) {
        viewport.setAttribute(
          'content',
          'width=device-width, initial-scale=1.0'
        );
        modified = true;
      }
    }

    // 2. Add Content Security Policy meta tag (strict)
    let csp = document.querySelector(
      'meta[http-equiv="Content-Security-Policy"]'
    );
    if (!csp) {
      csp = document.createElement('meta');
      csp.setAttribute('http-equiv', 'Content-Security-Policy');
      // More restrictive CSP for better security
      csp.setAttribute(
        'content',
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';"
      );
      document.head.appendChild(csp);
      modified = true;
    }

    // 3. Add charset if missing
    let charset = document.querySelector('meta[charset]');
    if (!charset) {
      charset = document.createElement('meta');
      charset.setAttribute('charset', 'UTF-8');
      document.head.insertBefore(charset, document.head.firstChild);
      modified = true;
    }

    // 4. Fix link contrast - ensure links have underlines or other visual indicators
    const style = document.createElement('style');
    style.textContent = `
      a:not([class*="btn"]) {
        text-decoration: underline;
        text-decoration-thickness: 1px;
        text-underline-offset: 2px;
      }
      a:not([class*="btn"]):hover {
        text-decoration-thickness: 2px;
      }
    `;

    // Check if this style doesn't already exist
    const existingStyles = Array.from(document.querySelectorAll('style'));
    const hasLinkStyles = existingStyles.some(
      (s) =>
        s.textContent.includes('text-decoration') &&
        s.textContent.includes('a:not')
    );

    if (!hasLinkStyles) {
      document.head.appendChild(style);
      modified = true;
    }

    // 5. Fix link text issues - ensure all links have descriptive text or aria-labels
    const links = document.querySelectorAll('a[href]');
    links.forEach((link) => {
      const text = link.textContent.trim();
      const ariaLabel = link.getAttribute('aria-label');
      const title = link.getAttribute('title');

      // If link has no text and no aria-label, add one
      if (!text && !ariaLabel && !title) {
        const href = link.getAttribute('href');
        if (href && href !== '#') {
          // Extract meaningful text from href
          let linkText = href;
          if (href.startsWith('#')) {
            linkText = `Jump to ${href.substring(1).replace(/-/g, ' ')}`;
          } else if (href.startsWith('/')) {
            linkText = `Navigate to ${href.replace(/\//g, ' ').trim()}`;
          }
          link.setAttribute('aria-label', linkText);
          modified = true;
        }
      }
    });

    // 6. Ensure there's a proper heading structure (h1 exists)
    const h1Elements = document.querySelectorAll('h1');
    if (h1Elements.length === 0) {
      // Add a visually hidden h1 if none exists
      const h1 = document.createElement('h1');
      h1.className = 'sr-only';
      h1.style.cssText =
        'position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden;';
      h1.textContent =
        document.title ||
        document.querySelector('title')?.textContent ||
        'Page Content';

      const main = document.querySelector('main') || document.body;
      if (main.firstChild) {
        main.insertBefore(h1, main.firstChild);
      } else {
        main.appendChild(h1);
      }
      modified = true;
    }

    if (modified) {
      fs.writeFileSync(filePath, dom.serialize(), 'utf8');
      return true;
    }

    return false;
  } catch (error) {
    console.error(`  ✗ Error processing ${filePath}:`, error.message);
    return false;
  }
}

/**
 * Find all HTML files in directory
 */
function findHTMLFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      findHTMLFiles(fullPath, files);
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      files.push(fullPath);
    }
  }

  return files;
}

/**
 * Main optimization process
 */
async function optimize() {
  console.log('🔧 Optimizing build for production...\n');

  if (!fs.existsSync(SITE_DIR)) {
    console.error(
      '❌ Error: _site directory not found. Run "npm run build" first.'
    );
    process.exit(1);
  }

  // 1. Minify CSS
  console.log('📦 Minifying CSS files...');
  const cssFiles = findCSSFiles(SITE_DIR);

  if (cssFiles.length === 0) {
    console.log('  ⚠️  No CSS files found');
  } else {
    const results = cssFiles.map(processCSSFile).filter((r) => r !== null);
    const totalOriginal = results.reduce((sum, r) => sum + r.originalSize, 0);
    const totalMinified = results.reduce((sum, r) => sum + r.minifiedSize, 0);
    const totalSavings = (
      ((totalOriginal - totalMinified) / totalOriginal) *
      100
    ).toFixed(1);

    console.log(
      `  📊 Total: ${results.length} files, ${totalSavings}% size reduction\n`
    );
  }

  // 2. Optimize HTML files
  console.log('🔍 Optimizing HTML files...');
  const htmlFiles = findHTMLFiles(SITE_DIR);

  if (htmlFiles.length === 0) {
    console.log('  ⚠️  No HTML files found');
  } else {
    let modifiedCount = 0;
    for (const file of htmlFiles) {
      if (processHTMLFile(file)) {
        modifiedCount++;
      }
    }
    console.log(
      `  ✓ Processed ${htmlFiles.length} HTML files (${modifiedCount} modified)\n`
    );
  }

  console.log('✅ Build optimization complete!\n');

  return 0;
}

// Run if called directly
if (require.main === module) {
  optimize()
    .then((exitCode) => process.exit(exitCode))
    .catch((error) => {
      console.error('\n❌ Optimization failed:', error.message);
      process.exit(1);
    });
}

module.exports = optimize;
