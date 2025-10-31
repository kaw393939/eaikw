# 🚀 AI-Assisted Web Development: Quality-First Learning Platform

> **Self-paced course teaching production-ready web development using AI coding
> assistants with automated quality gates and professional DevOps practices.**

[![Deploy Status](https://github.com/kaw393939/is117_ai_test_practice/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/kaw393939/is117_ai_test_practice/actions)
[![Live Site](https://img.shields.io/badge/demo-live-success)](https://kaw393939.github.io/is117_ai_test_practice/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 How This Works

This project uses a **bulletproof development environment** with automated
quality gates that catch issues before they reach production. Here's what makes
it special:

### **Development Environment Options**

**Option 1: Docker (Recommended - Always Works) 🐳**

```bash
docker-compose up
# Opens http://localhost:8080/ with CSS, hot reload, everything just works
```

**Option 2: Local Development Script 🚀**

```bash
./start-dev.sh
# Automated: loads env, kills conflicts, builds, starts server
```

### **What Happens Behind the Scenes**

```
You Edit Code → Auto-Reload → Quality Checks → Git Hooks → CI/CD → Deploy
     ↓              ↓             ↓             ↓          ↓        ↓
   src/         Live in       ESLint       Pre-commit   GitHub    Live
   files      browser       Prettier      Linters     Actions    Site
             (instant)     Stylelint   (stops bad   (tests +   (auto)
                                       code)      deploys)
```

### **Built-In Quality System**

**Automated AI Code Review:**

- 🤖 **7 Expert Agents** - Each specialized (Typography, Layout, Contrast,
  Hierarchy, Accessibility, Conversion, Brand)
- 🔍 **Consensus-Based** - Issues must be confirmed by multiple experts
- 📊 **Quantified Results** - Severity ratings, actionable fixes, priority
  rankings
- 💰 **Cost-Effective** - GPT-4o-mini at ~$0.15 per 1M tokens

**Multi-Device Testing:**

- 📱 **7 Device Sizes** - iPhone portrait/landscape, iPad portrait/landscape,
  MacBook, Desktop, 2K wide
- 📸 **Automated Screenshots** - Playwright captures across all viewports
- 🎯 **Above-the-Fold Analysis** - Ensures hero content visible without
  scrolling
- 🔄 **Responsive Issue Detection** - Identifies mobile-only vs desktop-only
  problems

**Quality Enforcement:**

- ♿ **WCAG AA Compliance** - 186+ accessibility issues caught and fixed
- 🎨 **Design System** - Consistent color tokens, no glassmorphism, proper
  contrast ratios (4.5:1+)
- 📏 **Typography Standards** - 14px minimum, proper hierarchy, balanced text
- 🚫 **Zero Tolerance** - Bad code physically cannot reach production (blocked
  by hooks + CI)

### **Why This Matters**

Traditional dev: Spend 30-60 minutes fighting servers, debugging paths, fixing
CSS 404s **This project: One command. Everything works. Ship features, not bug
fixes.**

📖 **[Full Development Guide](DEVELOPMENT.md)** | 🚀
**[Quick Start](QUICK-START.md)**

---

## 🎯 What You'll Learn

This **self-paced learning platform** teaches you to build production-ready
websites using AI coding assistants while maintaining professional code quality
standards.

**Core Skills:**

- ✅ AI-assisted development with quality assurance
- ✅ Automated quality gates that catch errors before deployment
- ✅ Modern CI/CD workflow (push code → auto-test → auto-deploy)
- ✅ DRY (Don't Repeat Yourself) principles enforced by tooling
- ✅ Professional debugging and troubleshooting

**Time Commitment:**

- Reading: ~2 hours
- Hands-on practice: ~4-6 hours
- Total: 6-8 hours to full project completion

**Prerequisites:** None! Basic HTML/CSS helpful but not required.

---

## 👥 Who This Is For

### 🎓 Students (Self-Paced Learning)

Learn at your own pace with:

- 10 bite-sized lessons (10-40 min each)
- Copy-paste AI prompts for every step
- Built-in knowledge checks to verify understanding
- Comprehensive troubleshooting guide
- Final project for your portfolio

### 👨‍🏫 Instructors (Classroom Integration)

Use as curriculum with:

- **[Instructor Guide](docs/instructor-guide.md)** - Teaching strategies,
  activities, assessments
- Suggested classroom activities and discussion prompts
- Flexible integration (supplement, flipped classroom, or workshop)
- Assessment rubrics and grading guidance
- No instructor interaction required (fully self-serve)

### 💼 Professionals (Skill Upgrading)

Modernize your workflow:

- Learn industry-standard CI/CD practices
- Integrate AI assistants into your development
- Automate quality checks you do manually today
- See real-world examples, not toy projects

---

## 🎓 Course Structure

### **Part 1: Foundation** (~2 hours)

1. [**What Is This Project?**](docs/lessons/01-what-is-this.md) - 3 min _See
   what we're building and why it matters_

2. [**Why Quality Gates?**](docs/lessons/02-why-quality-gates.md) - 3 min _The
   problem with AI-generated code and how to fix it_

3. [**Prompt Engineering Basics**](docs/lessons/03-prompt-engineering-basics.md) -
   5 min _How to talk to AI coding assistants effectively_

4. [**Setup Your Environment**](docs/lessons/04-setup-your-environment.md) -
   30-40 min _Install tools and get the project running locally_

### **Part 2: Building with Quality** (~3 hours)

5. [**Build with Eleventy**](docs/lessons/05-build-with-eleventy.md) - 17 min
   _Create a static website with templates and layouts_

6. [**ESLint & Prettier**](docs/lessons/06-eslint-prettier.md) - 11 min
   _Automatic code quality checking and formatting_

7. [**Pre-commit Hooks**](docs/lessons/07-pre-commit-hooks.md) - 11 min _Stop
   bad code before it's committed to Git_

8. [**GitHub Actions CI/CD**](docs/lessons/08-github-actions.md) - 13 min
   _Automate testing and deployment on every push_

9. [**Lighthouse CI**](docs/lessons/09-lighthouse-ci.md) - 11 min _Ensure your
   site is fast, accessible, and SEO-friendly_

### **Part 3: Professional Skills** (~1 hour)

10. [**Troubleshooting & Debugging**](docs/lessons/10-troubleshooting.md) - 19
    min _Common issues, debugging strategies, and working without automation_

---

## 🚀 Quick Start

### **Docker Setup (Recommended - Always Works)**

```bash
# 1. Fork this repository on GitHub (top right button)
# 2. Clone YOUR fork
git clone https://github.com/YOUR-USERNAME/is117_ai_test_practice.git
cd is117_ai_test_practice

# 3. Copy environment template
cp .env.example .env
# Edit .env and add your API keys (OPENAI_API_KEY, etc.)

# 4. Start everything
docker-compose up

# 5. Visit http://localhost:8080/ in your browser
# ✅ CSS loads, hot reload works, ready to develop
```

**Why Docker?**

- ✅ Consistent environment everywhere
- ✅ No "works on my machine" issues
- ✅ Server always binds correctly
- ✅ One command to start everything

---

### **Local Setup (Alternative)**

```bash
# 1-2. Fork and clone (same as above)

# 3. Install Node.js dependencies
npm install

# 4. Copy environment template
cp .env.example .env
# Edit .env and add your API keys

# 5. Run automated startup script
./start-dev.sh

# 6. Visit http://localhost:8080/ in your browser
```

**The script automatically:**

- Loads environment variables
- Kills port conflicts
- Builds and verifies site
- Starts development server with correct paths

---

### **For Instructors: Read First**

1. Browse the [lessons](docs/lessons/) to understand the flow
2. Check the [Instructor Guide](docs/instructor-guide.md) for teaching
   strategies
3. Review the [Development Guide](DEVELOPMENT.md) to understand infrastructure
4. Then set up your own fork for demonstration

**Note:** Students can complete this entirely self-paced. Your role is context,
troubleshooting, and celebration!

---

## 👨‍🏫 For Instructors

**New to teaching this content?** Start here:

📖 **[Instructor Guide](docs/instructor-guide.md)** - Complete teaching resource

**What's included:**

- ✅ Suggested classroom activities (with time estimates)
- ✅ Assessment rubrics and grading guidance
- ✅ Integration options (flipped classroom, workshop, self-paced)
- ✅ Troubleshooting tips for common student issues
- ✅ External resources and community links

**No prep required** - Content is fully self-serve. Your role is to provide
context, troubleshoot, and celebrate wins!

---

## 📝 Copy-Paste Prompts

Don't want to type? We got you. Pre-written prompts for every step:

- [**Initial Setup Prompts**](docs/prompts/initial-setup.md) - Get started fast
- [**Configuration Prompts**](docs/prompts/configuration.md) - Set up quality
  tools
- [**Building Pages Prompts**](docs/prompts/building-pages.md) - Create content
- [**Debugging Prompts**](docs/prompts/debugging.md) - Fix issues

---

## 📚 Documentation

### **Development Guides**

- 🚀 [**Quick Start Guide**](QUICK-START.md) - TL;DR command reference
- 📖 [**Development Guide**](DEVELOPMENT.md) - Complete development
  documentation
- 🔍
  [**5 Whys Analysis**](archive/documentation/DEVELOPMENT-ENVIRONMENT-5-WHYS-ANALYSIS.md) -
  How we fixed the dev environment
- ✅
  [**What's Fixed**](archive/documentation/DEVELOPMENT-ENVIRONMENT-FIXED.md) -
  Summary of improvements

### **Course Content**

- [**npm Scripts Cheatsheet**](docs/reference/npm-scripts.md) - All available
  commands
- [**File Structure Guide**](docs/reference/file-structure.md) - What each file
  does
- [**Duplication Detection**](docs/reference/duplication-detection.md) -
  Automated code bloat prevention
- [**AI Assistant Guide**](docs/reference/AI-GUIDE.md) - For your AI coding
  assistant

### **Quality Assurance**

- 🤖 **7 AI Expert Agents** - Typography, Layout, Contrast, Hierarchy,
  Accessibility, Conversion, Brand
- 📱 **Multi-Device Testing** - iPhone, iPad, MacBook, Desktop, Wide Desktop
  (portrait + landscape)
- ♿ **WCAG AA Compliance** - Automated accessibility verification
- 🎨 **Design System** - Consistent tokens, no glassmorphism, proper contrast
  ratios

---

## 🎯 Learning Objectives

By the end of this course, you'll be able to:

| Skill                         | What You'll Master                                    |
| ----------------------------- | ----------------------------------------------------- |
| 🤖 **AI Prompting**           | Write effective prompts that generate quality code    |
| 🔍 **Code Quality**           | Use ESLint, Prettier, Stylelint to maintain standards |
| 🪝 **Git Hooks**              | Automate checks before code enters version control    |
| 🚀 **CI/CD**                  | Deploy automatically with GitHub Actions              |
| ⚡ **Performance**            | Build fast, accessible websites with Lighthouse       |
| 🏗️ **Static Site Generators** | Use Eleventy to build modern websites                 |
| 🎨 **Modern Web Dev**         | Work with HTML, CSS, JavaScript professionally        |
| 🐛 **Debugging**              | Troubleshoot issues with AI assistance                |

---

## 🎬 Before You Start

### You'll Need:

- [ ] **A computer** (Mac, Windows, or Linux)
- [ ] **30-60 minutes** of focused time
- [ ] **An AI coding assistant** (GitHub Copilot, ChatGPT, Claude, etc.)
- [ ] **Basic curiosity** about web development

### You DON'T Need:

- ❌ Prior coding experience
- ❌ Deep understanding of web development
- ❌ To memorize anything (we have copy-paste prompts)

---

## 🌐 External Resources & Learning Supplements

### Official Documentation

**Primary Technologies:**

- [Eleventy Docs](https://www.11ty.dev/docs/) - Static site generator we use
- [Node.js Guide](https://nodejs.org/en/docs/) - JavaScript runtime
- [GitHub Actions](https://docs.github.com/en/actions) - CI/CD platform

**Quality Tools:**

- [ESLint Rules](https://eslint.org/docs/rules/) - JavaScript linter
- [Prettier Options](https://prettier.io/docs/en/options.html) - Code formatter
- [Stylelint](https://stylelint.io/) - CSS linter
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/) -
  Performance/accessibility testing

### Video Tutorials (Supplemental)

- [Eleventy Crash Course](https://www.youtube.com/results?search_query=eleventy+crash+course) -
  YouTube
- [Git & GitHub for Beginners](https://www.youtube.com/results?search_query=git+github+for+beginners) -
  YouTube
- [CI/CD Explained Simply](https://www.youtube.com/results?search_query=ci+cd+explained) -
  YouTube

### Interactive Learning

- [Learn Git Branching](https://learngitbranching.js.org/) - Visual Git tutorial
- [GitHub Skills](https://skills.github.com/) - Hands-on GitHub practice
- [MDN Web Docs](https://developer.mozilla.org/) - HTML/CSS/JS reference

### Communities

- [Eleventy Discord](https://www.11ty.dev/blog/discord/) - Ask questions about
  11ty
- [Dev.to](https://dev.to/) - Share your projects and learn from others
- [Stack Overflow](https://stackoverflow.com/) - Technical Q&A

### Related Courses

- [freeCodeCamp](https://www.freecodecamp.org/) - Free web development
  curriculum
- [The Odin Project](https://www.theodinproject.com/) - Full-stack development
  path
- [MDN Learn Web Development](https://developer.mozilla.org/en-US/docs/Learn) -
  Mozilla's web dev guide

---

## 💡 How to Use This Course

### Option 1: **Guided Path** (Recommended for beginners)

Follow lessons 1-10 in order. Each lesson builds on the previous one.

### Option 2: **Reference Mode** (For experienced developers)

Jump to specific topics using the table of contents above.

### Option 3: **Copy-Paste Mode** (For the time-constrained)

Go straight to [prompts](docs/prompts/) and recreate the project.

---

## 🚨 Important Notes

### ⚠️ #1 AI Pitfall: Code Duplication

**AI coding agents LOVE to duplicate code** instead of reusing existing styles,
functions, and components. This creates unmaintainable bloat.

**YOU MUST:**

- ✅ Check existing code BEFORE asking AI to create
- ✅ Explicitly tell AI to REUSE existing styles
- ✅ Review AI output for duplicates

**Read this:**
[Avoiding Duplication Guide](docs/prompts/avoiding-duplication.md)

---

### 🛠️ Technology Stack

**Core:**

- **Eleventy 2.0** - Static site generator
- **Node.js 20** - JavaScript runtime
- **Docker & Docker Compose** - Development environment
- **GitHub Actions** - CI/CD automation

**Quality Tools:**

- **ESLint** - JavaScript linting
- **Prettier** - Code formatting
- **Stylelint** - CSS linting
- **Lighthouse CI** - Performance & accessibility
- **JSCPD** - Duplication detection

**AI Quality System:**

- **OpenAI GPT-4** - AI expert consensus reviews
- **Playwright** - Multi-device screenshot testing
- **Python 3.12** - QA automation scripts

---

### 🔒 Multi-Layer Quality Gates

| Layer              | What It Checks            | When It Runs      | Can Be Bypassed?   |
| ------------------ | ------------------------- | ----------------- | ------------------ |
| 🎨 **Editor**      | Real-time syntax errors   | As you type       | N/A                |
| 💾 **Save**        | Auto-format code          | When you save     | N/A                |
| 🪝 **Pre-commit**  | Lint staged files         | Before Git commit | No (enforced)      |
| 🤖 **CI/CD**       | Full quality check        | On push to GitHub | No (blocks merge)  |
| ⚡ **Lighthouse**  | Performance/accessibility | Before deployment | No (fails CI)      |
| 🚫 **Duplication** | Code/CSS duplication >10% | Pre-commit + CI   | No (blocks commit) |
| 🤖 **AI Review**   | 7-expert consensus        | On-demand         | Yes (manual)       |
| 📱 **Responsive**  | 7-device testing          | On-demand         | Yes (manual)       |

**Key Point:** The first 6 layers are **automatic and enforced**. Bad code
cannot reach production.

---

## 🎓 Who Is This For?

### ✅ Perfect For:

- College students learning web development
- Developers exploring AI-assisted coding
- Anyone wanting to build quality websites fast
- Teams implementing code quality standards

### ⚠️ Not For:

- People looking for no-code solutions
- Those who don't want to learn (just want a website)

---

## 🌟 What Makes This Different?

### Traditional Coding Courses:

❌ Type everything manually ❌ Memorize syntax ❌ Slow feedback loops ❌ No
quality enforcement ❌ Fragile dev environments ❌ "Works on my machine"
problems

### This Course:

✅ Use AI to write code ✅ Focus on prompting skills ✅ Instant quality feedback
✅ Automated quality gates ✅ **Bulletproof Docker environment** ✅
**Professional DevOps from day one** ✅ **Multi-device automated testing** ✅
**AI-powered code review (7 expert agents)**

### **Real-World Ready:**

This isn't a toy project. The development environment and QA system mirror what
you'd find at Fortune 100 companies:

- **Docker containers** for consistency
- **Multi-stage quality gates** (editor → pre-commit → CI/CD)
- **Automated accessibility testing** (WCAG AA compliance)
- **Responsive design verification** (7 device sizes)
- **AI-assisted code review** (GPT-4 powered expert consensus)

**You're not just learning to code. You're learning to ship production-quality
software.**

---

## 📱 TikTok Generation Features

- ⏱️ **Bite-sized lessons** (3-5 minutes each)
- 🎯 **Clear objectives** at the start of each lesson
- 💡 **TL;DR sections** for quick scanning
- 📋 **Copy-paste prompts** for every task
- ✅ **Checkboxes** to track progress
- 🎨 **Visual diagrams** showing workflows
- 🚀 **Instant gratification** with quick wins

---

## 🤖 Running the AI Quality System

### **System Architecture**

```
Responsive Review → 7 Devices → 7 Expert Agents → Consensus Report
     (Entry)        (Capture)     (Analyze)        (Aggregate)
```

**What makes it powerful:**

- 🎯 **49 Perspectives** - 7 devices × 7 experts = comprehensive coverage
- 🤖 **Specialized Experts** - Typography, Layout, Contrast, Hierarchy,
  Accessibility, Conversion, Brand
- 💰 **Cost-Effective** - ~$0.73 per full review (GPT-4o-mini at $0.15/1M
  tokens)
- 📊 **Quantified** - Severity ratings, consensus scoring, actionable fixes
- 🔄 **Iterative** - Re-run consensus without re-capturing screenshots

### **Quick Start**

```bash
# Option 1: Docker (Recommended)
docker-compose up web                                    # Start dev server
docker-compose run --rm qa python run_responsive_review.py  # Run QA

# Option 2: Local Python Environment
cd qa_agents
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python run_responsive_review.py
```

### **What Gets Reviewed**

**7 Device Configurations:**

- 📱 Mobile Portrait (375×812) - iPhone
- 📱 Mobile Landscape (812×375)
- 📱 Tablet Portrait (768×1024) - iPad
- 📱 Tablet Landscape (1024×768)
- 💻 Laptop (1440×900) - MacBook
- 🖥️ Desktop (1920×1080) - Standard monitor
- 🖥️ Wide Desktop (2560×1440) - 2K display

**7 Expert Agents:**

- **Typography Expert** - Font sizes, readability, hierarchy (min 14px, proper
  scale)
- **Layout Expert** - Spacing, alignment, above-the-fold content
- **Contrast Expert** - WCAG AA compliance (4.5:1 minimum), visibility
- **Hierarchy Expert** - Information architecture, hero visibility, visual
  weight
- **Accessibility Expert** - ARIA labels, keyboard navigation, screen readers
- **Conversion Expert** - CTAs, user journey, friction points
- **Brand Expert** - Design system consistency, color tokens, glassmorphism
  violations

### **Output & Reports**

After running, check:

```bash
qa_agents/screenshots/YYYY-MM-DD-HH-MM-SS/
├── mobile-portrait.png              # Screenshots for each device
├── tablet-landscape.png
├── desktop.png
├── responsive-review-report.json    # Machine-readable data
└── RESPONSIVE-REVIEW-REPORT.txt     # Human-readable findings
```

**Report Structure:**

- 🔴 **Critical Issues** - Mentioned by 3+ experts, breaks usability
- 🟡 **Important Issues** - Mentioned by 2 experts, impacts UX
- 🔵 **Minor Issues** - Single expert observations
- 🌐 **Cross-Device Issues** - Problems spanning multiple viewports
- 💡 **Recommendations** - Prioritized action items

### **Advanced Usage**

**Re-analyze existing screenshots (fast, no re-capture):**

```bash
python run_consensus_review.py
```

**Custom viewport sizes:** Edit `responsive_review.py`:

```python
DEVICE_CONFIGS = {
    "custom": {"width": 1024, "height": 768, "name": "Custom Device"}
}
```

**Modify expert behavior:** Edit `expert_agents.py` instructions for any expert
(no restart needed)

**Full documentation:**

- 📖 [QA System Architecture](qa_agents/ARCHITECTURE.md) - System design, data
  flow, best practices
- 🔧 [QA Agents README](qa_agents/README.md) - Setup, configuration,
  troubleshooting
- 📊 [Technical Debt Audit 2024](qa_agents/TECHNICAL-DEBT-AUDIT-2024.md) -
  Recent cleanup details

---

## 🏆 Challenge Yourself

After completing the course, try these extensions:

- [ ] Add a blog with pagination
- [ ] Implement dark mode
- [ ] Add E2E tests with Playwright
- [ ] Create a contact form
- [ ] Add image optimization
- [ ] Implement a search feature
- [ ] **Run responsive review and fix all critical issues**
- [ ] **Achieve 100/100 Lighthouse score on all pages**
- [ ] **Add visual regression testing**

---

## 🤝 Contributing

Found a typo? Have a suggestion? Want to improve a lesson?

1. Fork this repo
2. Make your changes
3. Submit a pull request

All contributions welcome! 🎉

---

## 📄 License

MIT License - Use this for learning, teaching, or building your own projects.

---

## 🚀 Ready to Start?

### [👉 Click Here to Begin Lesson 1: What Is This Project?](docs/lessons/01-what-is-this.md)

---

## 💬 Questions & Troubleshooting

### Common Issues

**"CSS doesn't load / page is unstyled"**

```bash
# Check environment variable
docker-compose run web env | grep ELEVENTY_ENV
# Should show: ELEVENTY_ENV=development

# If not, restart with fresh build
docker-compose down && docker-compose up --build
```

**"Port 8080 already in use"**

```bash
# Kill existing process
lsof -ti:8080 | xargs kill -9
# Then restart
docker-compose up
```

**"Server says running but I can't connect"**

```bash
# This is the Eleventy bug we fixed
# Solution: Use Docker (it always works)
docker-compose up

# Or use the startup script
./start-dev.sh
```

**"API key errors in QA system"**

```bash
# Make sure .env file exists with your key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here
# Restart Docker
docker-compose down && docker-compose up
```

### More Help

- 🐛 **Found a bug?**
  [Open an issue](https://github.com/kaw393939/is117_ai_test_practice/issues)
- 💡 **Have a question?**
  [Open an issue](https://github.com/kaw393939/is117_ai_test_practice/issues)
- 📖 **Read the docs:** [Development Guide](DEVELOPMENT.md) has comprehensive
  troubleshooting
- 🤖 **AI issues?** Check the
  [Troubleshooting Guide](docs/lessons/10-troubleshooting.md)

---

## 🏗️ Project Architecture

```
Development Environment
├── Docker Container (web)
│   ├── Node.js 20 + Eleventy
│   ├── Port 8080
│   ├── Hot reload (file watching)
│   └── Health checks
│
├── Docker Container (qa) [optional]
│   ├── Python 3.12 + Playwright
│   ├── 7 AI Expert Agents
│   ├── Multi-device screenshots
│   └── Responsive review system
│
└── Quality Gates
    ├── Pre-commit hooks
    ├── CI/CD (GitHub Actions)
    ├── Lighthouse CI
    └── Duplication detection
```

**Key Insight:** Docker isolates the entire environment. The Eleventy server bug
that plagued local development? Doesn't exist in Docker. One command, everything
works.

---

## 👥 Credits

**Built with ❤️ by students, for students**

**Infrastructure:** Professional-grade DevOps setup with Docker, multi-layer
quality gates, and AI-powered code review.

**Pedagogy:** Self-paced learning with copy-paste prompts, bite-sized lessons,
and zero prerequisites.

**Philosophy:** Ship production-quality code from day one. No "learn the wrong
way first" compromises.

Last updated: October 30, 2025
