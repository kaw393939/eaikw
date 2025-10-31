module.exports = {
  eleventyComputed: {
    permalink: (data) => {
      // Remove 'src/' from the URL
      if (data.page.filePathStem.startsWith('/src/')) {
        const path = data.page.filePathStem.replace('/src/', '/');
        // Don't add trailing slash for index
        if (path === '/index') {
          return '/';
        }
        return path + '/';
      }
      return data.page.filePathStem + '/';
    },
  },
};
