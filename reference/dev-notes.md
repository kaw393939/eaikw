# Development Notes

Quick commands:

- Install: `npm install`
- Dev server: `npm run dev` (Eleventy serves on `http://localhost:8080`)
- Build: `npm run build` (copies CSS/JS and runs Eleventy)
- Serve built site: `npm run serve`

Local troubleshooting:

- If styles are missing, ensure `src/css/main.css` exists and run
  `npm run build:css`
- For mobile menu issues, confirm `src/js/mobile-menu.bundle.js` is copied to
  `_site/js`

Add more tips as common issues arise.
