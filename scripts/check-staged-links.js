#!/usr/bin/env node

/**
 * Staged File Link Checker
 *
 * Checks links in staged markdown files before commit.
 * Runs as part of pre-commit hook for fast feedback.
 *
 * Only checks files that are staged for commit to keep it fast.
 */

const { execSync } = require('child_process');
const fs = require('fs');

/**
 * Get list of staged markdown files
 */
function getStagedMarkdownFiles() {
  try {
    const output = execSync(
      'git diff --cached --name-only --diff-filter=ACMR',
      {
        encoding: 'utf8',
      }
    );

    return output
      .split('\n')
      .filter((f) => f.trim())
      .filter((f) => f.endsWith('.md'))
      .filter((f) => {
        // Only check docs/lessons files (high value, frequently changed)
        return f.includes('docs/lessons/') || f === 'README.md';
      })
      .filter((f) => fs.existsSync(f)); // File must exist
  } catch (error) {
    return [];
  }
}

/**
 * Check links in staged files
 */
function checkStagedLinks() {
  const stagedFiles = getStagedMarkdownFiles();

  if (stagedFiles.length === 0) {
    console.log('✓ No lesson files staged for commit - skipping link check');
    return { passed: true, filesChecked: 0 };
  }

  console.log(`🔗 Checking links in ${stagedFiles.length} staged file(s)...`);
  stagedFiles.forEach((f) => console.log(`   - ${f}`));
  console.log('');

  try {
    // Run markdown-link-check on staged files
    const cmd = `markdown-link-check ${stagedFiles.join(' ')} --config .markdown-link-check.json --quiet`;
    execSync(cmd, { stdio: 'inherit' });

    console.log(`\n✅ All links valid in ${stagedFiles.length} file(s)\n`);
    return { passed: true, filesChecked: stagedFiles.length };
  } catch (error) {
    console.error('\n❌ Broken links detected in staged files\n');
    console.error(
      '💡 Fix the broken links or use --no-verify to skip this check\n'
    );
    return { passed: false, filesChecked: stagedFiles.length };
  }
}

// Run if called directly
if (require.main === module) {
  const result = checkStagedLinks();
  process.exit(result.passed ? 0 : 1);
}

module.exports = checkStagedLinks;
