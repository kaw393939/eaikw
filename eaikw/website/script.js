// Simple JavaScript for the Keith Williams Consulting Website

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add active state to nav links based on scroll position
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');

function setActiveLink() {
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

window.addEventListener('scroll', setActiveLink);

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.problem-card, .credential-card, .service-card, .blog-card, .stat-card').forEach(el => {
    observer.observe(el);
});

// Load blog posts dynamically (if you have a blog.json file)
async function loadBlogPosts() {
    try {
        const response = await fetch('blog/posts.json');
        if (!response.ok) return; // File doesn't exist yet, use placeholder content
        
        const posts = await response.json();
        const blogGrid = document.getElementById('latest-posts');
        
        if (blogGrid && posts.length > 0) {
            blogGrid.innerHTML = posts.slice(0, 3).map(post => `
                <div class="blog-card">
                    <span class="blog-date">${post.date}</span>
                    <h3>${post.title}</h3>
                    <p>${post.excerpt}</p>
                    <a href="blog/${post.slug}.html" class="read-more">Read More →</a>
                </div>
            `).join('');
        }
    } catch (error) {
        console.log('Blog posts not loaded yet');
    }
}

// Load blog posts on page load
if (document.getElementById('latest-posts')) {
    loadBlogPosts();
}

// Email validation for contact form (if you add one later)
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Console Easter egg for developers who view source
console.log('%c👋 Hey Developer!', 'font-size: 20px; font-weight: bold; color: #2563eb;');
console.log('%cIf you\'re reading this, you might be the kind of person I want to work with.', 'font-size: 14px; color: #374151;');
console.log('%cCheck out my GitHub: https://github.com/kaw393939', 'font-size: 12px; color: #8b5cf6;');
console.log('%cView my production AI code: https://github.com/kaw393939/enterprise_ai_demo1_websearch', 'font-size: 12px; color: #10b981;');
