---
layout: lesson.njk
title: 'Setup Your Environment'
lessonNumber: 4
description: 'Install required tools and get the project running locally'
timeEstimate: '30-40 minutes'
level: 'Beginner'
tags: ['lessons']
permalink: '/lessons/04-setup-your-environment/'
---

⏱️ **Time:** Reading: 8 min | Practice: 20-30 min | Total: ~30-40 min 📚
**Level:** Beginner 🎯 **Goal:** Install required tools and get the project
running locally

---

## 🚀 TL;DR

Install Node.js, Git, and a code editor. Fork the repository, clone it locally,
install dependencies, and verify everything works.

---

## 📋 Prerequisites Checklist

Before you start, you'll need:

- [ ] **A computer** (Mac, Windows, or Linux)
- [ ] **Internet connection** (for downloading tools)
- [ ] **GitHub account** (free at github.com)
- [ ] **30 minutes** of uninterrupted time

---

## 🔧 Required Tools

### 1. Node.js (JavaScript Runtime)

**What it is:** Runs JavaScript outside the browser (needed for Eleventy)

**Required Version:** 20 or higher

**Install:**

**Mac:**

```bash
# Using Homebrew (recommended)
brew install node@20

# Verify installation
node --version  # Should show v20.x.x
npm --version   # Should show 10.x.x
```

**Windows:**

1. Download from <https://nodejs.org/>
2. Choose "20.x.x LTS" version
3. Run installer with default options
4. Open Command Prompt:

```cmd
node --version
npm --version
```

**Linux:**

```bash
# Using nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20

# Verify
node --version
npm --version
```

---

### 2. Git (Version Control)

**What it is:** Tracks changes to your code

**Install:**

**Mac:**

```bash
# Using Homebrew
brew install git

# Verify
git --version
```

**Windows:**

1. Download from <https://git-scm.com/>
2. Run installer
3. Accept default options
4. Verify in Command Prompt:

```cmd
git --version
```

**Linux:**

```bash
sudo apt-get install git  # Debian/Ubuntu
sudo yum install git      # CentOS/RHEL

git --version
```

---

### 3. Code Editor (VS Code Recommended)

**What it is:** Where you write and edit code

**Why VS Code?**

- Free and open source
- Excellent AI assistant integration (GitHub Copilot)
- Built-in terminal
- Great extensions

**Install:**

1. Download from <https://code.visualstudio.com/>
2. Install for your operating system
3. Launch VS Code

**Recommended Extensions:**

Open VS Code and install these extensions:

- **ESLint** - JavaScript linting
- **Prettier** - Code formatting
- **Stylelint** - CSS linting
- **markdownlint** - Markdown linting
- **GitHub Copilot** (optional) - AI coding assistant

**Quick Install:**

```bash
# Open VS Code, then press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows/Linux)
# Type: "Extensions: Install Extensions"
# Search and install each extension
```

---

## 📦 Fork and Clone the Repository

### Step 1: Fork on GitHub

1. Go to: <https://github.com/kaw393939/is117_ai_test_practice>
2. Click "Fork" button (top right)
3. Choose your account
4. Wait for fork to complete

**Result:** You now have your own copy at
`github.com/YOUR_USERNAME/is117_ai_test_practice`

---

### Step 2: Clone Locally

**Using VS Code (Easiest):**

1. Open VS Code
2. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
3. Type: "Git: Clone"
4. Paste: `https://github.com/YOUR_USERNAME/is117_ai_test_practice.git`
5. Choose where to save it
6. Click "Open" when prompted

**Using Terminal:**

```bash
# Navigate to where you want the project
cd ~/Desktop  # Or wherever you prefer

# Clone your fork
git clone https://github.com/YOUR_USERNAME/is117_ai_test_practice.git

# Navigate into the project
cd is117_ai_test_practice

# Open in VS Code
code .
```

---

## 📥 Install Dependencies

**What this does:** Downloads all the tools (Eleventy, ESLint, etc.) the project
needs

**In VS Code Terminal:**

1. Open Terminal: `View → Terminal` or `` Ctrl+` ``
2. Run:

```bash
npm install
```

**What you'll see:**

```bash
added 740 packages, and audited 773 packages in 30s

147 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

**Time:** 30-60 seconds (depending on internet speed)

**If you see errors:**

- Check Node.js version: `node --version` (must be 20+)
- Delete `node_modules/` and `package-lock.json`, try again
- Check internet connection

---

## ✅ Verify Setup

### Test 1: Run Development Server

```bash
npm start
```

**Expected output:**

```bash
[11ty] Writing _site/404.html from ./src/404.md
[11ty] Writing _site/about/index.html from ./src/about.md
[11ty] Writing _site/index.html from ./src/index.md
[11ty] Wrote 3 files in 0.08 seconds
[11ty] Watching…
[11ty] Server at http://localhost:8080/
```

**✅ Success!** Your development server is running.

---

### Test 2: View in Browser

1. Open browser
2. Go to: <http://localhost:8080/>
3. You should see the website

**See the site?** ✅ Working! **404 Error?** Check the URL includes the repo
name in the path.

**Stop the server:** Press `Ctrl+C` in the terminal

---

### Test 3: Run Quality Checks

```bash
npm test
```

**Expected output:**

```bash
> 117-site@1.0.0 test
> npm run lint && npm run build

✓ ESLint passed
✓ Stylelint passed
✓ Markdownlint passed
✓ Prettier passed
✓ Duplication check passed (0.0%)
✓ Build succeeded
```

**✅ All tests passing!**

---

## 🎨 Configure Git

**Set your name and email** (appears in commits):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Verify:**

```bash
git config --global user.name
git config --global user.email
```

---

## 🚨 Common Issues & Fixes

### Issue: "node: command not found"

**Fix:** Node.js not installed or not in PATH

```bash
# Reinstall Node.js
# Then restart terminal/VS Code
```

---

### Issue: "npm install" fails with permission error

**Fix (Mac/Linux):**

```bash
# Don't use sudo!
# Fix npm permissions:
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

**Fix (Windows):**

Run Command Prompt as Administrator, then `npm install`

---

### Issue: Port 8080 already in use

**Fix:**

```bash
# Find process using port 8080
lsof -i :8080  # Mac/Linux
netstat -ano | findstr :8080  # Windows

# Kill the process
kill -9 [PID]  # Mac/Linux
taskkill /PID [PID] /F  # Windows

# Or use different port
npx eleventy --serve --port=8081
```

---

### Issue: GitHub fork failed

**Fix:**

- Make sure you're logged into GitHub
- Check if you already have a fork (can only have one)
- Try refreshing the page

---

## 📊 Setup Verification Checklist

Before moving to the next lesson, verify:

- [ ] Node.js 20+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Git installed (`git --version`)
- [ ] VS Code installed and opened
- [ ] Repository forked on GitHub
- [ ] Repository cloned locally
- [ ] Dependencies installed (`npm install` succeeded)
- [ ] Dev server runs (`npm start` works)
- [ ] Site loads in browser (<http://localhost:8080/>)
- [ ] Tests pass (`npm test` succeeds)
- [ ] Git configured (name and email set)

**All checked?** You're ready for Lesson 5! 🎉

---

## 💡 Pro Tips

### Tip 1: Use Integrated Terminal

VS Code's built-in terminal is better than external terminal because:

- Automatically in correct directory
- Shares VS Code environment
- Can split into multiple terminals

### Tip 2: Bookmark Local Dev URL

Add <http://localhost:8080/> to bookmarks for quick access

### Tip 3: Keep Dev Server Running

Keep `npm start` running in one terminal tab while you code. Save files and see
changes instantly!

### Tip 4: Learn Git Basics

```bash
git status           # See what changed
git add .            # Stage all changes
git commit -m "msg"  # Commit with message
git push             # Push to GitHub
```

---

## 🎮 Quick Test Activity (1 minute)

**Verify everything works:**

1. Start dev server: `npm start`
2. Open <http://localhost:8080/>
3. Edit `src/index.md` - change the heading
4. Save the file
5. Refresh browser - see your change!
6. Stop server: `Ctrl+C`

**Changes appeared?** ✅ Perfect! You're ready to build!

---

## 📊 Progress Tracker

You've completed:

- [x] ~~Lesson 1: What Is This Project?~~
- [x] ~~Lesson 2: Why Quality Gates?~~
- [x] ~~Lesson 3: Prompt Engineering Basics~~
- [x] ~~Lesson 4: Setup Your Environment~~
- [ ] Lesson 5: Build with Eleventy
- [ ] Lessons 6-10...

---

## 🚀 Next Steps

Now that your environment is set up, let's learn how to build pages with
Eleventy!

### [👉 Continue to Lesson 5: Build with Eleventy](/lessons/05-build-with-eleventy/)

---

## 🔗 Quick Links

- [🏠 Back to Course Index](/lessons/)
- [📝 Initial Setup Prompts](/resources/#prompts)
- [📚 File Structure Guide](/resources/#reference)

---

**Congratulations! Your development environment is ready!** 🎉
