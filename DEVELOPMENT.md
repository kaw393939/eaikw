# Development Guide

## Quick Start (Docker - Recommended)

**Prerequisites:** Docker and Docker Compose installed

```bash
# Start the development environment
docker-compose up

# Site will be available at: http://localhost:8080/
```

That's it. CSS works, server works, everything works.

---

## Quick Start (Local - Alternative)

**Prerequisites:** Node.js 20+, npm

```bash
# One-command startup
./start-dev.sh

# Site will be available at: http://localhost:8080/
```

---

## Development Workflows

### Regular Development

```bash
# Docker (recommended)
docker-compose up

# Local
./start-dev.sh
```

### Run QA Analysis

```bash
# With Docker
docker-compose --profile qa up

# Local
cd qa_agents
python3 run_responsive_review.py
```

### Build for Production

```bash
# Docker
docker-compose run web npm run build

# Local
npm run build
```

---

## Project Structure

```
117_site/
├── src/                    # Source files
│   ├── assets/
│   │   ├── css/           # Stylesheets
│   │   ├── js/            # JavaScript
│   │   └── images/        # Images
│   ├── _includes/         # Reusable components
│   ├── _layouts/          # Page layouts
│   ├── _data/             # Data files
│   └── *.njk              # Page templates
├── docs/
│   └── lessons/           # Course lessons
├── qa_agents/             # QA automation system
│   ├── responsive_review.py
│   ├── consensus_review.py
│   └── expert_agents.py
├── _site/                 # Built site (generated)
├── .eleventy.js           # Eleventy config
├── docker-compose.yml     # Docker orchestration
├── Dockerfile             # Web container
└── start-dev.sh           # Local startup script
```

---

## Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
OPENAI_API_KEY=sk-...
ELEVENTY_ENV=development
```

### Path Configuration

- **Development:** Site served at `http://localhost:8080/`
- **Production:** Site served at `https://kaw393939.github.io/is117_ai_test_practice/`

Eleventy automatically handles path prefixes based on `ELEVENTY_ENV`.

---

## Common Tasks

### Clean Build

```bash
# Docker
docker-compose run web npm run clean && docker-compose run web npm run build

# Local
npm run clean && npm run build
```

### Run Linters

```bash
# Docker
docker-compose run web npm run lint

# Local
npm run lint
```

### Format Code

```bash
# Docker
docker-compose run web npm run format

# Local
npm run format
```

### Run Tests

```bash
# Docker
docker-compose run web npm test

# Local
npm test
```

---

## Troubleshooting

### CSS Not Loading

**Problem:** Page displays but has no styling

**Solution:**
1. Check that `ELEVENTY_ENV=development` is set
2. Verify `_site/assets/css/main.css` exists
3. Restart the server: `docker-compose restart web`

### Port 8080 Already in Use

**Problem:** Server fails to start with "address already in use"

**Solution:**
```bash
# Kill existing process
lsof -ti:8080 | xargs kill -9

# Or use different port
docker-compose up --scale web=0 && docker-compose run -p 8081:8080 web
```

### API Key Errors in QA System

**Problem:** "OPENAI_API_KEY not found"

**Solution:**
1. Create `.env` file with your API key
2. Restart Docker: `docker-compose down && docker-compose up`
3. Verify with: `docker-compose run web env | grep OPENAI`

### Server Says Running But Not Accessible

**Problem:** Terminal shows "Server at..." but curl fails

**Solution with Docker (recommended):**
```bash
docker-compose down
docker-compose up --build
```

**Solution without Docker:**
```bash
pkill -f eleventy
./start-dev.sh
```

---

## Architecture

### Development Environment

```
┌─────────────────────────────────────┐
│     Docker Compose                  │
│  ┌──────────────┐  ┌──────────────┐│
│  │              │  │              ││
│  │  Web Server  │  │  QA Agents   ││
│  │  (Node.js)   │  │  (Python)    ││
│  │              │  │              ││
│  │  Port 8080   │  │  API Calls   ││
│  └──────────────┘  └──────────────┘│
│         ▲                  │        │
│         │                  │        │
│    Volume Mount       Screenshots   │
│    (Hot Reload)                     │
└─────────────────────────────────────┘
```

### Build Process

```
Source Files (src/)
       │
       ├── Nunjucks Templates (.njk)
       ├── Markdown Content (.md)
       ├── CSS (main.css)
       └── JavaScript (main.js)
       │
       ▼
  Eleventy Build
       │
       ├── Template Rendering
       ├── Path Prefix Injection
       ├── Asset Copying
       └── Sitemap Generation
       │
       ▼
Built Site (_site/)
       │
       ├── HTML files
       ├── assets/css/main.css
       ├── assets/js/main.js
       └── assets/images/
```

---

## Development Server Behavior

### Eleventy Dev Server (`npm start`)

- **Live reload** - Changes auto-refresh browser
- **Port:** 8080
- **Path prefix:** `/` (development) or `/is117_ai_test_practice/` (production)
- **Watches:** `src/`, `docs/`, `.eleventy.js`

### Docker Behavior

- **Container isolation** - Consistent environment
- **Volume mounting** - Changes sync to container
- **Health checks** - Auto-wait for server ready
- **Networking** - Services can communicate by name

---

## QA System Integration

The QA agent system runs independently and connects to the dev server:

```bash
# Start web server first
docker-compose up web

# Then run QA analysis (in another terminal)
docker-compose --profile qa up

# Or run specific QA scripts
docker-compose run qa python3 qa_agents/run_responsive_review.py
```

### QA Agent Tools

1. **Responsive Review** - Multi-device screenshot analysis
2. **Consensus Review** - 7-expert collaborative review
3. **Targeted Review** - Section-specific analysis

---

## Best Practices

### DO

✅ Use Docker for development (consistent environment)
✅ Run `./start-dev.sh` if not using Docker
✅ Set `ELEVENTY_ENV=development` for local work
✅ Keep `.env` file with API keys (don't commit it)
✅ Run linters before committing
✅ Test in Docker before pushing

### DON'T

❌ Start server with random terminal commands
❌ Commit `.env` file with API keys
❌ Edit `_site/` directly (it's generated)
❌ Mix production and development paths
❌ Run multiple servers on port 8080
❌ Skip testing after CSS changes

---

## Getting Help

### Check Logs

```bash
# Docker logs
docker-compose logs web
docker-compose logs qa

# Local logs
tail -f /tmp/eleventy.log
```

### Verify Configuration

```bash
# Check environment
docker-compose run web env

# Check build output
docker-compose run web npm run build -- --dryrun
```

### Reset Everything

```bash
# Nuclear option - full reset
docker-compose down -v
docker system prune -f
rm -rf _site node_modules
docker-compose up --build
```

---

## Contributing

Before submitting changes:

1. Run linters: `npm run lint`
2. Run tests: `npm test`
3. Test in Docker: `docker-compose up`
4. Verify CSS loads correctly
5. Run QA review: `docker-compose --profile qa up`

---

## Performance

### Build Times

- **Initial build:** ~5-10 seconds
- **Incremental build:** ~1-2 seconds (hot reload)
- **Docker build:** ~30 seconds (first time), ~5 seconds (cached)

### Dev Server

- **Startup time:** ~3 seconds
- **Live reload latency:** <1 second
- **Memory usage:** ~100MB (Node) + ~500MB (Docker)

---

## FAQ

**Q: Why Docker?**
A: Consistent environment, works the same on every machine, no "works on my machine" issues.

**Q: Can I develop without Docker?**
A: Yes, use `./start-dev.sh` script. But Docker is recommended.

**Q: Why does CSS sometimes 404?**
A: Path prefix mismatch. Make sure `ELEVENTY_ENV=development` is set.

**Q: How do I update dependencies?**
A: `npm update && docker-compose build --no-cache`

**Q: Can I use a different port?**
A: Edit `docker-compose.yml` ports section or use `./start-dev.sh` and change the port in `.eleventy.js`

---

**Last Updated:** October 30, 2025
**Maintained by:** Development Team
