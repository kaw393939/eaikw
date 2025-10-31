const sitemap = require('@quasibit/eleventy-plugin-sitemap');

module.exports = function (eleventyConfig) {
  // Add sitemap plugin
  eleventyConfig.addPlugin(sitemap, {
    sitemap: {
      hostname: process.env.SITE_URL || 'https://eaikw.com',
    },
  });

  // Copy static assets to output (strip src/ prefix)
  eleventyConfig.addPassthroughCopy({ 'src/assets/css': 'assets/css' });
  eleventyConfig.addPassthroughCopy({ 'src/assets/js': 'assets/js' });
  eleventyConfig.addPassthroughCopy({ 'src/assets/images': 'assets/images' });
  eleventyConfig.addPassthroughCopy({ 'src/robots.txt': 'robots.txt' });
  eleventyConfig.addPassthroughCopy({ 'src/manifest.json': 'manifest.json' });
  eleventyConfig.addPassthroughCopy({ 'src/CNAME': 'CNAME' });
  eleventyConfig.addPassthroughCopy({ 'src/.nojekyll': '.nojekyll' });

  // Watch CSS files for changes
  eleventyConfig.addWatchTarget('src/assets/css/');
  eleventyConfig.addWatchTarget('docs/lessons/');

  // Add a custom date filter for formatting dates
  eleventyConfig.addFilter('readableDate', (dateObj) => {
    return new Date(dateObj).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  });

  // Add a custom filter to get current year
  eleventyConfig.addShortcode('year', () => `${new Date().getFullYear()}`);

  // Add lessons as a collection from docs/lessons
  eleventyConfig.addCollection('lessons', function (collectionApi) {
    return collectionApi.getFilteredByGlob('docs/lessons/*.md').sort((a, b) => {
      // Extract lesson numbers from filenames (e.g., "01-", "02-")
      const aNum = parseInt(a.fileSlug.split('-')[0]);
      const bNum = parseInt(b.fileSlug.split('-')[0]);
      return aNum - bNum;
    });
  });

  return {
    pathPrefix: '/',
    dir: {
      input: '.',
      output: '_site',
      includes: 'src/_includes',
      layouts: 'src/_layouts',
      data: 'src/_data',
    },
    templateFormats: ['md', 'njk', 'html'],
    markdownTemplateEngine: false,
    htmlTemplateEngine: 'njk',
    dataTemplateEngine: 'njk',
    // Ignore patterns
    ignores: ['references/**', 'qa_agents/**', 'node_modules/**'],
  };
};
