// Initialize all functionality when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
  initMobileNavigation();
  initSmoothScrolling();
  initHeaderScrollEffect();
  initImageLoading();
  initCodeCopyButtons();
  initFormValidation();
  initThemeToggle();
});

// Mobile navigation toggle
function initMobileNavigation() {
  try {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (!hamburger || !navMenu) return;

    hamburger.addEventListener('click', function () {
      hamburger.classList.toggle('active');
      navMenu.classList.toggle('active');
    });

    // Close menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach((link) => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
      });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function (event) {
      const isClickInsideNav = navMenu.contains(event.target);
      const isClickOnHamburger = hamburger.contains(event.target);

      if (!isClickInsideNav && !isClickOnHamburger && navMenu.classList.contains('active')) {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
      }
    });
  } catch (error) {
    console.warn('Mobile navigation initialization failed:', error);
  }
}

// Smooth scrolling for anchor links
function initSmoothScrolling() {
  try {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach((link) => {
      link.addEventListener('click', function (e) {
        const href = this.getAttribute('href');

        if (href === '#') {
          e.preventDefault();
          return;
        }

        const target = document.querySelector(href);

        if (target) {
          e.preventDefault();

          const headerOffset = 80;
          const elementPosition = target.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth',
          });
        }
      });
    });
  } catch (error) {
    console.warn('Smooth scrolling initialization failed:', error);
  }
}

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function () {
  const anchorLinks = document.querySelectorAll('a[href^="#"]');

  anchorLinks.forEach((link) => {
    link.addEventListener('click', function (e) {
      const href = this.getAttribute('href');

      if (href === '#') {
        e.preventDefault();
        return;
      }

      const target = document.querySelector(href);

      if (target) {
        e.preventDefault();

        const headerOffset = 80;
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth',
        });
      }
    });
  });
});

// Add scroll effect to header
function initHeaderScrollEffect() {
  try {
    const header = document.querySelector('.site-header');

    if (!header) return;

    let lastScrollTop = 0;

    window.addEventListener('scroll', function () {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

      if (scrollTop > lastScrollTop && scrollTop > 100) {
        // Scrolling down
        header.style.transform = 'translateY(-100%)';
      } else {
        // Scrolling up
        header.style.transform = 'translateY(0)';
      }

      lastScrollTop = scrollTop;
    });
  } catch (error) {
    console.warn('Header scroll effect initialization failed:', error);
  }
}

// Add loading animation for images
function initImageLoading() {
  try {
    const images = document.querySelectorAll('img[loading="lazy"]');

    images.forEach((img) => {
      img.addEventListener('load', function () {
        this.style.opacity = '1';
      });

      // Add initial styles
      img.style.opacity = '0';
      img.style.transition = 'opacity 0.3s ease';
    });
  } catch (error) {
    console.warn('Image loading initialization failed:', error);
  }
}

// Add copy code functionality
function initCodeCopyButtons() {
  try {
    const codeBlocks = document.querySelectorAll('pre code');

    codeBlocks.forEach((codeBlock) => {
      const pre = codeBlock.parentElement;

      // Create copy button
      const copyButton = document.createElement('button');
      copyButton.className = 'copy-code-btn';
      copyButton.textContent = 'Copy';
      copyButton.setAttribute('aria-label', 'Copy code to clipboard');

      // Position the button
      pre.style.position = 'relative';
      copyButton.style.position = 'absolute';
      copyButton.style.top = '10px';
      copyButton.style.right = '10px';
      copyButton.style.padding = '5px 10px';
      copyButton.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
      copyButton.style.color = 'white';
      copyButton.style.border = '1px solid rgba(255, 255, 255, 0.2)';
      copyButton.style.borderRadius = '4px';
      copyButton.style.fontSize = '12px';
      copyButton.style.cursor = 'pointer';
      copyButton.style.transition = 'all 0.2s ease';

      copyButton.addEventListener('mouseenter', function () {
        this.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';
      });

      copyButton.addEventListener('mouseleave', function () {
        this.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
      });

      copyButton.addEventListener('click', async function () {
        try {
          await navigator.clipboard.writeText(codeBlock.textContent);
          this.textContent = 'Copied!';
          this.style.backgroundColor = '#10b981';

          setTimeout(() => {
            this.textContent = 'Copy';
            this.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
          }, 2000);
        } catch (err) {
          console.error('Failed to copy code: ', err);
          this.textContent = 'Failed';
          this.style.backgroundColor = '#ef4444';

          setTimeout(() => {
            this.textContent = 'Copy';
            this.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
          }, 2000);
        }
      });

      pre.appendChild(copyButton);
    });
  } catch (error) {
    console.warn('Code copy buttons initialization failed:', error);
  }
}

// Add form validation if forms exist
function initFormValidation() {
  try {
    const forms = document.querySelectorAll('form');

    forms.forEach((form) => {
      form.addEventListener('submit', function (e) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;

        requiredFields.forEach((field) => {
          if (!field.value.trim()) {
            isValid = false;
            field.classList.add('error');

            // Remove error class on input
            field.addEventListener(
              'input',
              function () {
                this.classList.remove('error');
              },
              { once: true }
            );
          }
        });

        if (!isValid) {
          e.preventDefault();
        }
      });
    });
  } catch (error) {
    console.warn('Form validation initialization failed:', error);
  }
}

// Add theme toggle functionality (future enhancement)
function initThemeToggle() {
  try {
    const themeToggle = document.querySelector('.theme-toggle');

    if (!themeToggle) return;

    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);

    themeToggle.addEventListener('click', function () {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';

      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
    });
  } catch (error) {
    console.warn('Theme toggle initialization failed:', error);
  }
}
