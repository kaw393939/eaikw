module.exports = async function (eleventyConfig) {
  const { EleventyHtmlBasePlugin } = await import('@11ty/eleventy');

  // Copy static files
  eleventyConfig.addPassthroughCopy({ 'src/css': 'css' });
  eleventyConfig.addPassthroughCopy({ 'src/js': 'js' });
  eleventyConfig.addPassthroughCopy({ 'src/images': 'images' });
  eleventyConfig.addPassthroughCopy('src/assets');

  // Add plugins
  eleventyConfig.addPlugin(EleventyHtmlBasePlugin);

  // Watch targets
  eleventyConfig.addWatchTarget('src/css/');
  eleventyConfig.addWatchTarget('src/js/');

  // Collections
  eleventyConfig.addCollection('blog', function (collectionApi) {
    return collectionApi.getFilteredByGlob('src/blog/*.md').reverse();
  });

  eleventyConfig.addCollection('projects', function (collectionApi) {
    return collectionApi.getFilteredByGlob('src/projects/*.md').reverse();
  });

  // Filters
  eleventyConfig.addFilter('dateFormat', function (date) {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  });

  eleventyConfig.addFilter('excerpt', function (content) {
    const excerpt = content.replace(/(<([^>]+)>)/gi, '').substring(0, 200);
    return excerpt + (excerpt.length >= 200 ? '...' : '');
  });

  eleventyConfig.addFilter('limit', function (array, limit) {
    return array.slice(0, limit);
  });

  eleventyConfig.addFilter('currentYear', function () {
    return new Date().getFullYear();
  });

  // Custom filter for GitHub Pages path prefix
  eleventyConfig.addFilter('baseUrl', function (url) {
    // Only apply path prefix if explicitly enabled (for GitHub Pages)
    const pathPrefix = process.env.PATH_PREFIX || '';
    return pathPrefix ? `${pathPrefix}${url}` : url;
  });

  // Markdown config
  const markdownIt = await import('markdown-it');
  eleventyConfig.setLibrary(
    'md',
    markdownIt.default({
      html: true,
      breaks: true,
      linkify: true,
    })
  );

  return {
    dir: {
      input: 'src',
      output: '_site',
      includes: '_layouts',
      data: '_data',
    },
    templateFormats: ['md', 'njk', 'html'],
    markdownTemplateEngine: 'njk',
    htmlTemplateEngine: 'njk',
    dataTemplateEngine: 'njk',
  };
};
