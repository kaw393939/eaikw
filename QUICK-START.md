# 🚀 Quick Reference: Development Commands

## Start Development (Pick One)

```bash
# RECOMMENDED: Docker (always works)
docker-compose up

# ALTERNATIVE: Local script
./start-dev.sh
```

Site available at: **http://localhost:8080/**

---

## Stop Development

```bash
# Docker
Ctrl+C or docker-compose down

# Local
Ctrl+C
```

---

## Run QA Analysis

```bash
# Full responsive review (7 devices × 7 experts)
docker-compose --profile qa up

# Or manually
docker-compose up web  # Start server first
docker-compose run qa python3 qa_agents/run_responsive_review.py
```

---

## Common Tasks

```bash
# Clean build
docker-compose run web npm run clean && docker-compose run web npm run build

# Run linters
docker-compose run web npm run lint

# Format code
docker-compose run web npm run format

# Full reset (nuclear option)
docker-compose down -v
docker system prune -f
rm -rf _site node_modules
docker-compose up --build
```

---

## Troubleshooting

### CSS not loading?

```bash
# Check environment
docker-compose run web env | grep ELEVENTY_ENV
# Should show: ELEVENTY_ENV=development

# Restart with fresh build
docker-compose down && docker-compose up --build
```

### Port 8080 in use?

```bash
# Kill existing process
lsof -ti:8080 | xargs kill -9

# Then restart
docker-compose up
```

### Server won't start?

```bash
# Full reset
docker-compose down -v
docker-compose up --build
```

---

## File Locations

- **Source:** `src/`
- **Built site:** `_site/`
- **CSS:** `src/assets/css/main.css`
- **QA Scripts:** `qa_agents/`
- **Screenshots:** `qa_agents/screenshots/`
- **Docs:** `DEVELOPMENT.md`

---

## URLs

- **Dev site:** http://localhost:8080/
- **CSS:** http://localhost:8080/assets/css/main.css
- **JS:** http://localhost:8080/assets/js/main.js

---

## Environment Variables

Create `.env` file:

```bash
OPENAI_API_KEY=sk-proj-your-key-here
ELEVENTY_ENV=development
```

---

## Best Practices

✅ Always use Docker for consistency ✅ Run `npm run lint` before committing ✅
Test CSS loading after changes ✅ Use `./start-dev.sh` if Docker unavailable

❌ Don't edit `_site/` directly (it's generated) ❌ Don't commit `.env` file ❌
Don't run multiple servers on port 8080

---

**Need Help?** Read `DEVELOPMENT.md`
