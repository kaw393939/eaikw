#!/usr/bin/env node

/**
 * Path Migration Utility
 *
 * Automates path migrations when changing domains or path prefixes.
 * Safer than manual find-and-replace across many files.
 *
 * Usage:
 *   node scripts/migrate-paths.js
 *   npm run migrate:paths
 *
 * Always review changes with `git diff` before committing!
 */

const fs = require('fs');
const { glob } = require('glob');
const path = require('path');

/**
 * Path migration configurations
 * Add new migrations here as needed
 */
const MIGRATIONS = [
  {
    name: 'Old GitHub Pages prefix → Root',
    from: '/is117_ai_test_practice/',
    to: '/',
    files: 'src/**/*.{njk,md,html}',
    description: 'Updates old path prefix to root path',
  },
  {
    name: 'Old GitHub Pages domain → eaikw.com',
    from: 'https://kaw393939.github.io/is117_ai_test_practice',
    to: 'https://eaikw.com',
    files: '{src,docs}/**/*.{njk,md,html,js}',
    description: 'Updates old domain to new custom domain',
  },
  {
    name: 'Old localhost path → Root localhost',
    from: 'localhost:8080/is117_ai_test_practice',
    to: 'localhost:8080',
    files: 'docs/**/*.md',
    description: 'Updates old localhost URLs in documentation',
  },
];

/**
 * Apply a single migration
 */
async function applyMigration(migration) {
  console.log(`\n📝 ${migration.name}`);
  console.log(`   ${migration.description}`);
  console.log(`   Pattern: "${migration.from}" → "${migration.to}"\n`);

  const files = await glob(migration.files, {
    ignore: ['node_modules/**', '_site/**', '**/*.backup', '**/*.bak'],
    nodir: true,
  });

  let changedFiles = 0;
  let totalReplacements = 0;

  for (const file of files) {
    const content = fs.readFileSync(file, 'utf8');

    // Count occurrences
    const occurrences = (
      content.match(new RegExp(escapeRegex(migration.from), 'g')) || []
    ).length;

    if (occurrences > 0) {
      const newContent = content.replaceAll(migration.from, migration.to);
      fs.writeFileSync(file, newContent);
      changedFiles++;
      totalReplacements += occurrences;
      console.log(
        `   ✓ ${file} (${occurrences} replacement${occurrences > 1 ? 's' : ''})`
      );
    }
  }

  if (changedFiles === 0) {
    console.log('   ℹ️  No files needed changes');
  } else {
    console.log(
      `\n   📊 Summary: ${totalReplacements} replacement(s) in ${changedFiles} file(s)`
    );
  }

  return { changedFiles, totalReplacements };
}

/**
 * Escape special regex characters
 */
function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Main migration function
 */
async function migratePaths() {
  console.log('🔄 Starting Path Migration\n');
  console.log('='.repeat(60));

  let totalChanged = 0;
  let totalReplacements = 0;

  for (const migration of MIGRATIONS) {
    const result = await applyMigration(migration);
    totalChanged += result.changedFiles;
    totalReplacements += result.totalReplacements;
  }

  console.log('\n' + '='.repeat(60));
  console.log('\n🎉 Migration Complete!\n');
  console.log(
    `📊 Total: ${totalReplacements} replacement(s) in ${totalChanged} file(s)\n`
  );

  if (totalChanged > 0) {
    console.log('⚠️  IMPORTANT: Review changes before committing!\n');
    console.log('   Run: git diff\n');
    console.log(
      '   Then: git add -A && git commit -m "Migrate paths to new structure"\n'
    );
  } else {
    console.log('✅ No migrations needed - paths are already up to date\n');
  }
}

// Run if called directly
if (require.main === module) {
  migratePaths()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error('\n❌ Migration error:', error.message);
      process.exit(1);
    });
}

module.exports = migratePaths;
