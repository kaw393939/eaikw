# 9. Deployment Requirement

## Overview
Job Club must be deployed to a live, publicly accessible URL with automated CI/CD pipelines and full accessibility/mobile support.

---

## Deployment Platforms (Choose One)

### Option 1: GitHub Pages (Recommended - Free)
- Free hosting on `https://joshua31324324.github.io/eaikw`
- Automatic deployment via GitHub Actions
- Custom domain support available
- Perfect for static Eleventy sites

### Option 2: Netlify
- Free tier with git integration
- Automatic deployments on push
- Built-in form handling
- CDN included

### Option 3: Vercel
- Optimized for Next.js but works with static sites
- Automatic deployments
- Edge functions for serverless logic
- CDN with automatic optimization

---

## Automated CI/CD Requirements

### GitHub Actions Workflow
Must include:

```yaml
- Linting (ESLint, Stylelint, Markdownlint)
- Eleventy build test
- Playwright tests (homepage, onboarding form)
- Lighthouse CI (performance, accessibility, best practices, SEO)
- Bundle size checks (CSS < 10KB gzipped)
- Deploy to GitHub Pages on success
```

### Pre-Deployment Checks
- ✅ All tests passing
- ✅ No console errors
- ✅ Lighthouse score ≥ 90 for all categories
- ✅ Bundle size within limits
- ✅ All links valid (internal + external)

---

## Analytics & Consent

### GDPR-Compliant Analytics Loading
- Analytics scripts MUST NOT load until user consents
- Use consent banner (Accept/Reject/Preferences)
- Store consent preference in localStorage
- Load analytics only after consent given

### Implementation
```javascript
// Only load analytics if user consented
if (localStorage.getItem('analyticsConsent') === 'accepted') {
  loadAnalytics();
}
```

---

## Accessibility Requirements

### Mobile-First Responsive Design
- Must work on all screen sizes (320px - 4K)
- Touch-friendly buttons (min 44px)
- Readable text at all breakpoints
- No horizontal scrolling

### WCAG AA Compliance
- ✅ Color contrast ≥ 4.5:1 for text
- ✅ Keyboard navigation (tab through all elements)
- ✅ ARIA labels on form inputs
- ✅ Screen reader tested
- ✅ Semantic HTML (proper heading hierarchy, landmarks)
- ✅ Image alt text on all images
- ✅ Video captions

### Accessibility Testing
- Lighthouse Accessibility score ≥ 90
- Manual testing with keyboard navigation
- Screen reader testing (NVDA/JAWS on Windows, VoiceOver on Mac)

---

## Public URL & Domain

### Domain Configuration
- GitHub Pages: `https://joshua31324324.github.io/eaikw`
- Custom domain (optional): Set up CNAME in DNS
- Ensure HTTPS is enabled (automatic on GitHub Pages)

### URL Requirements
- Must be publicly accessible (no login required)
- Must load in < 3 seconds
- Must handle 404 pages gracefully
- Must have sitemap.xml and robots.txt

---

## Pre-Deployment Checklist

- [ ] GitHub Actions workflow configured and tested
- [ ] All CI checks passing (lint, build, tests)
- [ ] Lighthouse scores ≥ 90 across all categories
- [ ] Bundle size < 10KB gzipped for CSS
- [ ] Analytics consent banner implemented
- [ ] GDPR-compliant analytics loaded only after consent
- [ ] Mobile responsiveness tested on multiple devices
- [ ] WCAG AA accessibility compliance verified
- [ ] Public URL accessible and working
- [ ] 404 page implemented
- [ ] Sitemap and robots.txt in place
- [ ] SSL/HTTPS working
- [ ] Performance metrics baseline established

---

## Deployment Commands

```bash
# Build for production
npm run build

# Test build locally
npm run serve

# Push to GitHub (triggers GitHub Actions)
git push origin main

# View deployment status
# Go to: https://github.com/joshua31324324/eaikw/actions
```

---

## Monitoring & Maintenance

### Post-Deployment
- Monitor Lighthouse scores monthly
- Check analytics for errors
- Review user feedback
- Update content as needed
- Keep dependencies current

### Performance Targets
- Lighthouse Performance: 90+
- Lighthouse Accessibility: 90+
- Lighthouse Best Practices: 90+
- Lighthouse SEO: 90+
- First Contentful Paint (FCP): < 1.8s
- Largest Contentful Paint (LCP): < 2.5s
- Cumulative Layout Shift (CLS): < 0.1
