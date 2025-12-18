# SEO Reference

Guidance for SEO and meta content:

- Include `title` and `description` front matter for every page
- Use Open Graph tags and Twitter card meta where applicable
- Maintain an up-to-date `sitemap.xml` and `robots.txt`
- Canonical URLs via `{{ page.url | url }}` or site config
- Structured data (JSON-LD) for articles and projects if applicable

Badges & reporting:

- Add Lighthouse badges to README when continuous tests show stable results
- Track search appearance and core web vitals periodically (e.g., Lighthouse CI)
