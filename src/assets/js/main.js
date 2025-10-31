// Main JavaScript file
document.addEventListener('DOMContentLoaded', () => {
  // Add smooth scrolling to all links
  const links = document.querySelectorAll('a[href^="#"]');

  links.forEach((link) => {
    link.addEventListener('click', (e) => {
      try {
        const href = link.getAttribute('href');

        // Skip empty or just "#" hrefs
        if (!href || href === '#') {
          return;
        }

        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
          });
        }
      } catch (error) {
        // Silently handle any selector errors
        // Note: Error logging available for debugging if needed
      }
    });
  });
});
