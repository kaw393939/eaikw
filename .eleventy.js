module.exports = function (eleventyConfig) {
  // ===============================
  // PASSTHROUGH COPIES
  // ===============================
  // NOTE: Do NOT passthrough src/css
  // Tailwind builds CSS into _site/css
  eleventyConfig.addPassthroughCopy("src/images");
  eleventyConfig.addPassthroughCopy("src/fonts");

  // ===============================
  // FILTERS
  // ===============================
  // Handles subdirectory hosting (/jobclub)
  eleventyConfig.addFilter("baseUrl", function (url) {
    const pathPrefix = process.env.PATH_PREFIX || "";
    return pathPrefix ? `${pathPrefix}${url}` : url;
  });

  // Returns current year for copyright footer
  eleventyConfig.addFilter("currentYear", function () {
    return new Date().getFullYear();
  });

  // Common filters used throughout templates
  eleventyConfig.addFilter("dateFormat", function (date) {
    if (!date) return "Date not available";
    const d = new Date(date);
    if (isNaN(d.getTime())) return "Invalid date";
    return d.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  });

  eleventyConfig.addFilter("readableDate", function (date) {
    if (!date) return "Date not available";
    const d = new Date(date);
    if (isNaN(d.getTime())) return "Invalid date";
    return d.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  });

  eleventyConfig.addFilter("dateToISO", function (date) {
    if (!date) return new Date().toISOString();
    const d = new Date(date);
    if (isNaN(d.getTime())) return new Date().toISOString();
    return d.toISOString();
  });

  eleventyConfig.addFilter("excerpt", function (content) {
    if (!content) return "";
    const text = String(content).replace(/(<([^>]+)>)/gi, "");
    const excerpt = text.substring(0, 200);
    return excerpt + (text.length > 200 ? "..." : "");
  });

  eleventyConfig.addFilter("limit", function (array, limit) {
    if (!array || !array.slice) return array;
    return array.slice(0, limit);
  });

  eleventyConfig.addFilter("getPreviousCollectionItem", function (collection, page) {
    if (!collection || !page) return null;
    const index = collection.findIndex((item) => item.url === page.url);
    return index > 0 ? collection[index - 1] : null;
  });

  eleventyConfig.addFilter("getNextCollectionItem", function (collection, page) {
    if (!collection || !page) return null;
    const index = collection.findIndex((item) => item.url === page.url);
    return index < collection.length - 1 ? collection[index + 1] : null;
  });

  eleventyConfig.addFilter("dateToRfc3339", function (date) {
    if (!date) return new Date().toISOString();
    const d = new Date(date);
    if (isNaN(d.getTime())) return new Date().toISOString();
    return d.toISOString();
  });

  eleventyConfig.addFilter("getNewestCollectionItemDate", function (collection) {
    if (!collection || collection.length === 0) return new Date();
    return collection[0].date || new Date();
  });

  eleventyConfig.addFilter("absoluteUrl", function (url, baseUrl) {
    if (!baseUrl) return url;
    return new URL(url, baseUrl).href;
  });

  // ===============================
  // WATCH TARGETS
  // ===============================
  // Rebuild when Tailwind source changes
  eleventyConfig.addWatchTarget("./src/css/");

  // ===============================
  // ELEVENTY CONFIG
  // ===============================
  return {
    dir: {
      input: "src",
      includes: "_includes",
      layouts: "_includes",
      output: "_site",
    },
    templateFormats: ["njk", "md", "html"],

    // IMPORTANT: required for /jobclub on GitHub Pages
    pathPrefix: process.env.PATH_PREFIX || "/",
  };
};
