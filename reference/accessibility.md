# Accessibility Reference

Quick checklist for pages:

- Heading hierarchy (h1 → h2 → h3) is semantically correct
- All interactive controls have focus states and keyboard access
- Images include `alt` text
- Color contrast meets WCAG AA (use `--swiss-gray-*` tokens as guidance)
- Landmark elements are present (header, main, footer)

Testing commands:

- `npm run dev` then run Lighthouse or use browser devtools accessibility audit
- Consider `axe` integrations for automated tests in CI.
