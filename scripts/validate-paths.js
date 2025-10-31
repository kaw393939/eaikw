#!/usr/bin/env node

/**
 * Path Validation Script
 *
 * Validates that source files don't contain hardcoded paths that should
 * be using the centralized site configuration instead.
 *
 * This runs automatically after each Eleventy build to catch path issues
 * before they reach production.
 */

const fs = require('fs');
const path = require('path');
const { glob } = require('glob');

/**
 * Patterns that should NOT appear in source files
 */
const FORBIDDEN_PATTERNS = [
  {
    pattern: '/is117_ai_test_practice/',
    message:
      'Old path prefix found. Use {{ site.pathPrefix }} or {{ site.url }} instead.',
    severity: 'error',
  },
  {
    pattern: 'https://kaw393939.github.io/is117_ai_test_practice',
    message: 'Old GitHub Pages URL found. Use {{ site.url }} instead.',
    severity: 'error',
  },
  {
    pattern: 'localhost:8080/is117_ai_test_practice',
    message: 'Old localhost path found. Use {{ site.url }} instead.',
    severity: 'error',
  },
  // Warn about potential issues (not errors)
  {
    pattern: /href=["']https?:\/\/localhost/,
    message:
      'Hardcoded localhost URL found. Consider using {{ site.url }} for flexibility.',
    severity: 'warning',
    isRegex: true,
  },
];

/**
 * Files to check for hardcoded paths
 */
const FILE_PATTERNS = [
  'src/**/*.njk',
  'src/**/*.html',
  'src/**/*.md',
  'src/_includes/**/*.njk',
  'src/_layouts/**/*.njk',
];

/**
 * Files to exclude from validation
 */
const EXCLUDE_PATTERNS = [
  'node_modules/**',
  '_site/**',
  'src/robots.txt', // robots.txt needs full URLs
  'src/manifest.json', // manifest needs full URLs
  '**/*.backup',
  '**/*.bak',
  '**/*.broken',
];

/**
 * Check if a file should be excluded
 */
function shouldExclude(filePath) {
  return EXCLUDE_PATTERNS.some((pattern) => {
    if (pattern.includes('*')) {
      const regex = new RegExp(pattern.replace(/\*/g, '.*'));
      return regex.test(filePath);
    }
    return filePath.includes(pattern);
  });
}

/**
 * Validate a single file for forbidden patterns
 */
function validateFile(filePath) {
  if (shouldExclude(filePath)) {
    return { errors: [], warnings: [] };
  }

  const content = fs.readFileSync(filePath, 'utf8');
  const errors = [];
  const warnings = [];

  for (const { pattern, message, severity, isRegex } of FORBIDDEN_PATTERNS) {
    const matches = [];

    if (isRegex) {
      const regex = new RegExp(pattern, 'g');
      let match;
      while ((match = regex.exec(content)) !== null) {
        matches.push({ index: match.index, text: match[0] });
      }
    } else {
      let index = content.indexOf(pattern);
      while (index !== -1) {
        matches.push({ index, text: pattern });
        index = content.indexOf(pattern, index + 1);
      }
    }

    for (const match of matches) {
      // Calculate line number
      const beforeMatch = content.substring(0, match.index);
      const lineNumber = beforeMatch.split('\n').length;

      const issue = {
        file: filePath,
        line: lineNumber,
        pattern: match.text,
        message,
      };

      if (severity === 'error') {
        errors.push(issue);
      } else {
        warnings.push(issue);
      }
    }
  }

  return { errors, warnings };
}

/**
 * Main validation function
 */
async function validatePaths(siteConfig) {
  console.log('  Scanning source files for hardcoded paths...');

  const files = await glob(FILE_PATTERNS, {
    ignore: EXCLUDE_PATTERNS,
    nodir: true,
  });

  let totalErrors = [];
  let totalWarnings = [];
  let filesChecked = 0;

  for (const file of files) {
    const { errors, warnings } = validateFile(file);
    totalErrors = totalErrors.concat(errors);
    totalWarnings = totalWarnings.concat(warnings);
    filesChecked++;
  }

  // Report warnings (don't fail build)
  if (totalWarnings.length > 0) {
    console.log('\n  ⚠️  Path Warnings:');
    totalWarnings.forEach(({ file, line, pattern, message }) => {
      console.log(`    ${file}:${line}`);
      console.log(`      Found: "${pattern}"`);
      console.log(`      ${message}\n`);
    });
  }

  // Report errors (fail build)
  if (totalErrors.length > 0) {
    console.error('\n  ❌ Path Validation Failed!\n');
    console.error(
      `  Found ${totalErrors.length} hardcoded path(s) in ${files.length} file(s):\n`
    );

    totalErrors.forEach(({ file, line, pattern, message }) => {
      console.error(`    ${file}:${line}`);
      console.error(`      Found: "${pattern}"`);
      console.error(`      ${message}\n`);
    });

    console.error('  💡 Fix: Update templates to use centralized config:');
    console.error('     {{ site.url }}           - Full site URL');
    console.error('     {{ site.pathPrefix }}    - Path prefix only');
    console.error(
      '     {{ site.buildUrl(path) }} - Build full URL from path\n'
    );

    throw new Error(
      `Path validation failed: ${totalErrors.length} error(s) found`
    );
  }

  console.log(`  ✓ Checked ${filesChecked} files - no hardcoded paths found`);

  return {
    filesChecked,
    errors: totalErrors,
    warnings: totalWarnings,
  };
}

// Run validation if called directly
if (require.main === module) {
  const siteConfig = {
    url: 'https://eaikw.com',
    pathPrefix: '/',
    domain: 'eaikw.com',
  };

  validatePaths(siteConfig)
    .then(() => {
      console.log('\n✅ Path validation passed!\n');
      process.exit(0);
    })
    .catch((error) => {
      console.error(`\n${error.message}\n`);
      process.exit(1);
    });
}

module.exports = validatePaths;
