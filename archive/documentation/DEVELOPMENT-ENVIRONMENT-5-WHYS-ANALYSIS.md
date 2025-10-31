# Development Environment 5 Whys Root Cause Analysis
**Date:** October 30, 2025
**Issue:** Development environment is unreliable, CSS doesn't load, servers fail randomly

---

## 🔴 Problem Statement

**Symptom:** The application is extremely difficult to start correctly. CSS doesn't load, the server setup is fragile, and we're constantly troubleshooting basic infrastructure instead of doing actual work.

**Evidence:**
1. Screenshot shows unstyled page (CSS 404 errors)
2. Multiple server start failures across terminals
3. Path prefix confusion (`/is117_ai_test_practice/` vs `/`)
4. API keys not loading despite .env file existing
5. 10+ failed terminal commands trying to start the damn thing

---

## 🔍 5 WHYS ANALYSIS

### **WHY #1: Why is the CSS not loading?**

**Answer:** The HTML references `/is117_ai_test_practice/assets/css/main.css` but the Python HTTP server serves from `_site/` root, making it look for `_site/is117_ai_test_practice/assets/css/main.css` which doesn't exist.

**Evidence from terminal:**
```
::1 - - [30/Oct/2025 00:12:30] code 404, message File not found
::1 - - [30/Oct/2025 00:12:30] "GET /is117_ai_test_practice/assets/css/main.css HTTP/1.1" 404 -
```

**Root Issue:** Path prefix mismatch between build config and dev server

---

### **WHY #2: Why is there a path prefix mismatch?**

**Answer:** Eleventy config uses different path prefixes for dev vs production:
```javascript
pathPrefix: process.env.ELEVENTY_ENV === 'development' ? '/' : '/is117_ai_test_practice/',
```

But `npm start` doesn't set `ELEVENTY_ENV=development`, so it builds with production paths even in dev.

**Root Issue:** Environment variables not configured for local development

---

### **WHY #3: Why are we using different servers (eleventy --serve vs Python http.server)?**

**Answer:** Because eleventy's dev server mysteriously fails to bind to port 8080 despite saying "Server at http://localhost:8080/", forcing us to use Python's http.server as a workaround.

**Evidence:**
```bash
[11ty] Server at http://localhost:8080/is117_ai_test_practice/
# But then:
curl: (7) Failed to connect to localhost port 8080 after 0 ms: Couldn't connect to server
```

**Root Issue:** Eleventy dev server doesn't actually work, so we cobbled together a workaround that has different path behaviors

---

### **WHY #4: Why doesn't the Eleventy dev server work?**

**Answer:** Unknown. But rather than fixing it properly, we keep trying different hacks:
- npm start (fails)
- Python http.server (different paths)
- Background processes that die randomly
- Multiple terminals fighting over port 8080

**Root Issue:** No proper dev environment setup - just ad-hoc terminal commands

---

### **WHY #5: Why don't we have a proper dev environment setup?**

**Answer:** Because the project has accumulated massive technical debt:
- No Docker container for consistent environment
- No dev server configuration file
- No environment variable management
- No startup script that "just works"
- Mixed Python venv paths (sometimes works, sometimes doesn't)
- Repo cluttered with 15+ markdown reports, screenshots, QA tools
- No clear separation between dev/prod builds
- Every session starts with "let me try to start the server 5 different ways"

**ROOT CAUSE:** The project evolved organically without infrastructure planning. We kept adding features (QA agents, responsive review, consensus tools) without maintaining a reliable foundation.

---

## 💀 TECHNICAL DEBT INVENTORY

### **CRITICAL DEBT (Blocks Basic Functionality)**

1. **Eleventy Dev Server Non-Functional**
   - Status: Broken for unknown reason
   - Impact: Forces workarounds, path mismatches
   - Fix Time: 2-4 hours to diagnose and fix OR 1 hour to replace with better solution

2. **Path Prefix Chaos**
   - `/` for dev, `/is117_ai_test_practice/` for prod
   - No environment variable set to control this
   - CSS/JS 404s because server doesn't match build
   - Fix Time: 30 minutes

3. **Environment Variables Not Loading**
   - `.env` exists with `OPENAI_API_KEY`
   - Scripts fail with "API key not set"
   - Dotenv not loaded in some contexts
   - Fix Time: 1 hour

4. **Server Process Management**
   - Background processes die randomly
   - Multiple terminals with conflicting servers
   - No PID management, no restart capability
   - Fix Time: 2 hours (or fix with Docker)

### **HIGH DEBT (Causes Frequent Frustration)**

5. **No Reliable Startup Script**
   - Every session: manually start server, check port, fix paths, restart, debug
   - Should be: `./start-dev.sh` and done
   - Fix Time: 1 hour

6. **Python Venv Path Confusion**
   - `qa_agents/venv/bin/python` sometimes works, sometimes doesn't
   - `which python3` returns venv path, but direct path fails
   - Fix Time: 30 minutes

7. **Repository Clutter**
   - 15+ markdown reports in root
   - Screenshots scattered across directories
   - QA agent scripts mixed with source
   - Makes navigation/debugging harder
   - Fix Time: 1 hour cleanup

### **MEDIUM DEBT (Should Fix Soon)**

8. **No Docker Development Environment**
   - Every machine needs: Node, Python, venv, playwright, dependencies
   - Inconsistent environments
   - Fix Time: 3 hours to create, saves 10 hours of debugging

9. **Build vs Dev Mode Not Clear**
   - `npm run build` vs `npm start` have different behaviors
   - Not obvious which to use when
   - Fix Time: 30 minutes documentation

10. **No Health Check Endpoint**
    - Can't tell if server is actually ready
    - `curl localhost:8080` isn't enough
    - Fix Time: 30 minutes

---

## 🎯 ROOT CAUSE CONCLUSION

**The Real Problem:** We've been building a Fortune 100-level QA system on top of a hobby-project development environment.

**The Contradiction:**
- QA agents: Professional, automated, multi-expert consensus
- Dev environment: Manual, fragile, hope-it-works terminal commands

**Why This Happened:**
We focused on the exciting parts (AI agents, responsive testing) and ignored the boring parts (Docker, startup scripts, path configuration).

**The Fix:** Stop band-aiding. Spend 4-8 hours building proper infrastructure.

---

## ✅ ACTION PLAN: Make This Bulletproof

### **Phase 1: Emergency Stabilization (1 hour)**

1. **Fix Path Prefix Issue NOW**
   ```bash
   # Set env var in package.json
   "start": "ELEVENTY_ENV=development eleventy --serve"
   ```

2. **Create Dead-Simple Startup Script**
   ```bash
   #!/bin/bash
   # start-dev.sh
   export ELEVENTY_ENV=development
   source .env
   npm run build && npm start
   ```

3. **Fix CSS Loading**
   - Verify `_site/assets/css/main.css` exists
   - Verify HTML references match server paths

### **Phase 2: Proper Infrastructure (4 hours)**

4. **Dockerize Development Environment**
   ```dockerfile
   FROM node:20-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   EXPOSE 8080
   CMD ["npm", "start"]
   ```
   - Shared volume for hot reload
   - Server always running
   - Consistent environment everywhere

5. **Docker Compose for Full Stack**
   ```yaml
   services:
     web:
       build: .
       ports: ["8080:8080"]
       volumes: [".:/app"]
     qa:
       build: ./qa_agents
       depends_on: [web]
   ```

6. **Consolidate QA Tools**
   - Move all markdown reports to `docs/reports/`
   - Keep only essential scripts in root
   - Clear README with actual instructions

### **Phase 3: Professional Dev Experience (3 hours)**

7. **Single Command Startup**
   ```bash
   docker-compose up
   # That's it. Server runs. CSS loads. Done.
   ```

8. **Health Checks**
   - Server readiness endpoint
   - Auto-wait for server in tests
   - Clear status indicators

9. **Environment Management**
   - `.env.example` template
   - Validation on startup
   - Clear error messages

10. **Documentation**
    - `DEVELOPMENT.md` with actual setup steps
    - Troubleshooting guide
    - Architecture diagram

---

## 📊 COST-BENEFIT ANALYSIS

### **Current State Cost:**
- 30+ minutes every session fighting with server
- 5-10 sessions per week = 2.5-5 hours/week wasted
- Over 4 weeks = 10-20 hours wasted on infrastructure
- **Plus:** Frustration, context switching, can't focus on real work

### **Fix Cost:**
- Phase 1: 1 hour
- Phase 2: 4 hours
- Phase 3: 3 hours
- **Total: 8 hours investment**

### **ROI:**
- Saves 10-20 hours over next month
- Every future contributor saves setup time
- Can onboard new devs in 5 minutes instead of 2 hours
- **Payback period: 2 weeks**

---

## 🚨 IMMEDIATE NEXT STEPS

**RIGHT NOW (next 30 minutes):**

1. Fix the path prefix in package.json
2. Create working start-dev.sh script
3. Verify CSS loads correctly
4. Document what actually works

**THIS SESSION (next 2 hours):**

5. Clean up repo (move reports, organize structure)
6. Create Docker development setup
7. Test that `docker-compose up` works

**THIS WEEK:**

8. Replace all manual server starts with Docker
9. Update all QA scripts to use Docker endpoint
10. Write proper DEVELOPMENT.md

---

## 💡 LESSONS LEARNED

1. **Infrastructure is not optional** - Even AI agents need a stable foundation
2. **Automate the boring stuff first** - Startup scripts before fancy QA tools
3. **Docker exists for a reason** - "Works on my machine" is not acceptable
4. **Technical debt compounds** - Each workaround makes the next problem worse
5. **Stop and fix properly** - Band-aids create more band-aids

---

## 🎯 SUCCESS CRITERIA

**We're done when:**
- [ ] `docker-compose up` starts everything
- [ ] CSS loads correctly every time
- [ ] All QA scripts work without debugging
- [ ] New contributor can be productive in 10 minutes
- [ ] Zero time wasted on "why isn't the server working"

**Current Score:** 0/5 ❌
**Target Score:** 5/5 ✅

---

**Bottom Line:** We built a race car engine (AI QA system) and installed it in a shopping cart (fragile dev env). Time to build the proper chassis.
