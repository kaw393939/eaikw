#!/usr/bin/env node

/**
 * Local CI Runner
 *
 * Runs the same checks as GitHub Actions CI locally before pushing.
 * This provides fast feedback and prevents broken builds from reaching CI.
 *
 * Usage:
 *   npm run ci:local           # Run all checks
 *   npm run ci:fast            # Run quick checks only
 *   node scripts/run-local-ci.js --fast
 */

const { execSync } = require('child_process');
const process = require('process');

// Parse command line arguments
const args = process.argv.slice(2);
const isFast = args.includes('--fast') || args.includes('-f');

// CI Steps to run
const CI_STEPS = [
  {
    name: 'JavaScript Linting',
    cmd: 'npm run lint:js',
    required: true,
    fast: true,
  },
  {
    name: 'CSS Linting',
    cmd: 'npm run lint:css',
    required: true,
    fast: true,
  },
  {
    name: 'Markdown Linting',
    cmd: 'npm run lint:md',
    required: true,
    fast: true,
  },
  {
    name: 'Code Formatting Check',
    cmd: 'npm run lint:format',
    required: true,
    fast: true,
  },
  {
    name: 'Code Duplication Check',
    cmd: 'npm run lint:duplication',
    required: true,
    fast: false,
  },
  {
    name: 'Markdown Link Check',
    cmd: 'npm run lint:links:md',
    required: true,
    fast: false,
  },
  {
    name: 'Build Site',
    cmd: 'npm run build',
    required: true,
    fast: true,
  },
  {
    name: 'HTML Link Check',
    cmd: 'npm run lint:links:html',
    required: false, // Allow to fail (external links)
    fast: false,
  },
];

/**
 * Run a command and capture output
 */
function runCommand(cmd, verbose = false) {
  try {
    const output = execSync(cmd, {
      stdio: verbose ? 'inherit' : 'pipe',
      encoding: 'utf8',
    });
    return { success: true, output };
  } catch (error) {
    return {
      success: false,
      output: error.stdout || error.stderr || error.message,
    };
  }
}

/**
 * Format duration in human-readable format
 */
function formatDuration(ms) {
  if (ms < 1000) return `${ms}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
}

/**
 * Main CI runner
 */
async function runLocalCI() {
  console.log('🔍 Running Local CI Checks\n');
  console.log(
    `Mode: ${isFast ? 'FAST (critical checks only)' : 'FULL (all checks)'}\n`
  );

  const startTime = Date.now();
  const results = [];
  const failed = [];
  const warnings = [];

  // Filter steps based on mode
  const stepsToRun = isFast ? CI_STEPS.filter((step) => step.fast) : CI_STEPS;

  // Run each CI step
  for (const step of stepsToRun) {
    const stepStart = Date.now();
    process.stdout.write(`⏳ ${step.name}... `);

    const result = runCommand(step.cmd);
    const duration = Date.now() - stepStart;

    if (result.success) {
      console.log(`✅ (${formatDuration(duration)})`);
      results.push({ ...step, passed: true, duration });
    } else {
      if (step.required) {
        console.log(`❌ (${formatDuration(duration)})`);
        failed.push(step.name);
        results.push({
          ...step,
          passed: false,
          duration,
          output: result.output,
        });
      } else {
        console.log(`⚠️  (${formatDuration(duration)})`);
        warnings.push(step.name);
        results.push({ ...step, passed: false, warning: true, duration });
      }
    }
  }

  const totalDuration = Date.now() - startTime;

  // Print summary
  console.log('\n' + '='.repeat(60));
  console.log('CI CHECK SUMMARY');
  console.log('='.repeat(60) + '\n');

  const passed = results.filter((r) => r.passed).length;
  const total = results.length;

  console.log(`✅ Passed:   ${passed}/${total}`);
  if (warnings.length > 0) {
    console.log(`⚠️  Warnings: ${warnings.length}`);
  }
  if (failed.length > 0) {
    console.log(`❌ Failed:   ${failed.length}`);
  }
  console.log(`⏱️  Duration: ${formatDuration(totalDuration)}\n`);

  // Show failures
  if (failed.length > 0) {
    console.log('FAILED CHECKS:\n');
    for (const failedStep of failed) {
      const result = results.find((r) => r.name === failedStep);
      console.log(`❌ ${failedStep}`);
      if (result.output) {
        // Show first 10 lines of error output
        const lines = result.output.split('\n').slice(0, 10);
        lines.forEach((line) => console.log(`   ${line}`));
        if (result.output.split('\n').length > 10) {
          console.log(
            `   ... (${result.output.split('\n').length - 10} more lines)`
          );
        }
      }
      console.log('');
    }
  }

  // Show warnings
  if (warnings.length > 0) {
    console.log('WARNINGS (non-critical):\n');
    warnings.forEach((warning) => {
      console.log(`⚠️  ${warning}`);
    });
    console.log('');
  }

  // Final status
  if (failed.length === 0) {
    console.log('✅ All required CI checks passed!\n');
    console.log('💡 Safe to push to GitHub\n');
    return 0;
  } else {
    console.log(`❌ ${failed.length} required check(s) failed\n`);
    console.log('💡 Fix the issues above before pushing\n');
    return 1;
  }
}

// Run if called directly
if (require.main === module) {
  runLocalCI()
    .then((exitCode) => process.exit(exitCode))
    .catch((error) => {
      console.error('\n❌ CI runner error:', error.message);
      process.exit(1);
    });
}

module.exports = runLocalCI;
