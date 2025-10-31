module.exports = {
  ci: {
    collect: {
      staticDistDir: './_site',
      // Test all important pages
      url: [
        'http://localhost/index.html',
        'http://localhost/about/index.html',
        'http://localhost/lessons/index.html',
        'http://localhost/resources/index.html',
        'http://localhost/for-instructors/index.html',
        // All lesson pages
        'http://localhost/lessons/01-what-is-this/index.html',
        'http://localhost/lessons/02-why-quality-gates/index.html',
        'http://localhost/lessons/03-prompt-engineering-basics/index.html',
        'http://localhost/lessons/04-setup-your-environment/index.html',
        'http://localhost/lessons/05-build-with-eleventy/index.html',
        'http://localhost/lessons/06-eslint-prettier/index.html',
        'http://localhost/lessons/07-pre-commit-hooks/index.html',
        'http://localhost/lessons/08-github-actions/index.html',
        'http://localhost/lessons/09-lighthouse-ci/index.html',
        'http://localhost/lessons/10-troubleshooting/index.html',
      ],
      numberOfRuns: 1,
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:seo': ['error', { minScore: 0.9 }],
        // Ensure no unrendered markdown (check for common patterns)
        'unsized-images': 'off', // We use responsive images
        'unused-css-rules': 'off', // CSS intentionally shared across pages
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
