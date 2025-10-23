# EAIKW - Keith Williams: Fourth Turning + AI Era

**Navigating civilizational transition through education and technology.**

This repository contains the content management system and build tools for Keith Williams' thought leadership platform.

---

## 🎯 The Framework

### Theme 1: The Challenge
Understanding the Fourth Turning + AI convergence, macro-economic forces, and civilizational transition patterns.

### Theme 2: The Response
Rebuilding education and technology culture through Socratic + AI synthesis and ethical development practices.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- OpenAI API key (for image analysis, optional)

### Build Site

```bash
# Install dependencies
pip install -r requirements.txt

# Build site
python build.py

# Or use the build script
./build.sh
```

### Preview Locally

```bash
cd docs && python -m http.server 8000
# Visit http://localhost:8000
```

---

## 📝 Content Management

All content is managed through YAML files in `content/data/`:

- **`townhalls.yaml`** - Town hall events
- **`talks.yaml`** - Individual presentations
- **`themes.yaml`** - The two-theme framework
- **`navigation.yaml`** - Site navigation

To add a new town hall:
1. Edit `content/data/townhalls.yaml`
2. Run `./build.sh`
3. Commit and push

---

## 📁 Repository Structure

```
eaikw/
├── planning/          # 🔒 PRIVATE (gitignored)
├── content/           # 📝 Content (YAML + Markdown)
├── templates/         # 🎨 Jinja2 HTML templates
├── static/            # 📦 CSS, JS, images
├── docs/              # 🌐 Generated site (GitHub Pages)
└── build.py           # Build script
```

---

## 🌐 Deployment

Site deploys to GitHub Pages at **https://eaikw.com**

To deploy:
```bash
./build.sh
git add docs/
git commit -m "Build site"
git push origin main
```

---

## 🔗 Connect

- **Website:** [eaikw.com](https://eaikw.com)
- **LinkedIn:** [Keith Williams](https://linkedin.com/in/keithwilliams)
- **YouTube:** [@keithwilliams](https://youtube.com/@keithwilliams)
- **Discord:** [EAIKW Community](https://discord.gg/eaikw)

---

## 📄 License

Content © 2025 Keith Williams. All rights reserved.

Build system adapted from `legsontheground.com`.

---

**Status:** Build system implemented. Ready for first content.
