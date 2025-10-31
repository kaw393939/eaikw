---
layout: lesson.njk
title: 'Troubleshooting & Debugging'
lessonNumber: 10
description:
  'Learn to diagnose and fix common issues in your development workflow'
timeEstimate: '19 minutes'
level: 'All Levels'
tags: ['lessons']
permalink: '/lessons/10-troubleshooting/'
---

⏱️ **Time:** Reading: 9 min | Practice: 10 min | Total: ~19 min 📚 **Level:**
All Levels 🎯 **Goal:** Learn to diagnose and fix common issues in your
development workflow

---

## 🚀 TL;DR

When things break (and they will!), follow this process: **Read the error →
Identify the tool → Check docs → Fix → Verify**. This lesson teaches you how to
debug like a pro.

---

## 🤔 The Debugging Mindset

### Golden Rules:

1. **Read error messages carefully** - They tell you what's wrong!
2. **Check one thing at a time** - Don't change 5 things simultaneously
3. **Google is your friend** - Copy exact error message and search
4. **Ask AI assistants** - GitHub Copilot, ChatGPT, Claude
5. **Version control saves you** - Use `git` to undo mistakes

---

## 📋 Quick Diagnosis Checklist

When something breaks, check in this order:

- [ ] **Step 1:** Read the complete error message
- [ ] **Step 2:** Identify which tool is complaining (ESLint? Eleventy? Git?)
- [ ] **Step 3:** Check if file exists and is in correct location
- [ ] **Step 4:** Check if dependencies are installed (`npm install`)
- [ ] **Step 5:** Check if you're in the right directory (`pwd`)
- [ ] **Step 6:** Try the simplest fix first
- [ ] **Step 7:** Search for the exact error message
- [ ] **Step 8:** Ask for help (with error details)

---

## 🛠️ Common Issues by Tool

### ESLint Errors

#### Error: "'x' is not defined"

**Full error:**

```bash
src/js/main.js
  5:10  error  'x' is not defined  no-undef
```

**Meaning:** Using variable that doesn't exist

**Fixes:**

```javascript
// Option 1: Define the variable
const x = 10;
console.log(x);

// Option 2: Fix typo
const count = 10;
console.log(count); // Was: console.log(conut);

// Option 3: Import it
import { x } from './config.js';
```

---

#### Error: "'x' is assigned but never used"

**Full error:**

```bash
src/js/main.js
  3:7  error  'unused' is assigned a value but never used  no-unused-vars
```

**Meaning:** Variable defined but not used

**Fixes:**

```javascript
// Option 1: Remove it
// const unused = "hello";  ← Delete this line

// Option 2: Use it
const message = 'hello';
console.log(message);

// Option 3: Mark as intentional (rarely needed)
const _unused = 'hello'; // Underscore prefix = intentionally unused
```

---

#### Error: "Unexpected console statement"

**Full error:**

```bash
src/js/main.js
  10:3  warning  Unexpected console statement  no-console
```

**Meaning:** Console.log found (warning, not error)

**Fixes:**

```javascript
// Option 1: Keep it (warnings are OK in our project)
console.log('Debug message');

// Option 2: Remove it
// console.log("Debug message");  ← Delete

// Option 3: Use proper logging
if (process.env.NODE_ENV === 'development') {
  console.log('Debug message');
}
```

---

### Stylelint Errors

#### Error: "Unexpected duplicate selector"

**Full error:**

```bash
src/css/style.css
  5:1  error  Unexpected duplicate selector ".button"  no-duplicate-selectors
```

**Meaning:** Same CSS selector defined twice

**Fixes:**

```css
/* ❌ Bad (duplicate) */
.button {
  color: red;
}
.button {
  background: blue;
} /* ← Duplicate! */

/* ✅ Fix 1: Combine into one rule */
.button {
  color: red;
  background: blue;
}

/* ✅ Fix 2: Use more specific selectors */
.button {
  color: red;
}
.button.primary {
  background: blue;
}
```

---

#### Error: "Unexpected duplicate property"

**Full error:**

```bash
src/css/style.css
  8:3  error  Unexpected duplicate property "color"  declaration-block-no-duplicate-properties
```

**Meaning:** Same property twice in one rule

**Fixes:**

```css
/* ❌ Bad (duplicate property) */
.text {
  color: red;
  color: blue; /* ← Duplicate! Which one wins? */
}

/* ✅ Fix: Keep one */
.text {
  color: blue; /* Keep the one you want */
}
```

---

### Eleventy Errors

#### Error: "Layout not found"

**Full error:**

```bash
[11ty] Problem writing Eleventy templates:
[11ty] TemplateContentRenderError: Layout not found: base.njk
```

**Meaning:** Referenced layout file doesn't exist

**Fixes:**

```bash
# Check if layout exists
ls -la src/_includes/base.njk

# If missing, create it or fix typo in Markdown:
```

```markdown
## <!-- ❌ Bad (typo) -->

## layout: basse.njk

## <!-- ✅ Good -->

## layout: base.njk
```

---

#### Error: "Input directory doesn't exist"

**Full error:**

```bash
[11ty] Problem processing files:
[11ty] Error: Input directory 'src' doesn't exist
```

**Meaning:** Eleventy can't find source directory

**Fixes:**

```bash
# Check if you're in project root
pwd
# Should show: /path/to/is117_ai_test_practice

# If not, navigate there
cd /path/to/is117_ai_test_practice

# Verify src/ exists
ls -la src/
```

---

### Git Errors

#### Error: "fatal: not a git repository"

**Full error:**

```bash
fatal: not a git repository (or any of the parent directories): .git
```

**Meaning:** Not in a Git repository

**Fixes:**

```bash
# Check if you're in project directory
pwd

# Navigate to project
cd /path/to/is117_ai_test_practice

# Verify .git exists
ls -la .git/
```

---

#### Error: "Changes not staged for commit"

**Full error:**

```bash
Changes not staged for commit:
  modified:   src/index.md
```

**Meaning:** Files changed but not added to staging

**Fixes:**

```bash
# Stage specific files
git add src/index.md

# Or stage all changes
git add .

# Then commit
git commit -m "your message"
```

---

#### Error: "remote: Permission denied"

**Full error:**

```bash
remote: Permission to user/repo.git denied to otheruser.
fatal: unable to access 'https://github.com/user/repo.git/': The requested URL returned error: 403
```

**Meaning:** No permission to push to repository

**Fixes:**

```bash
# Check remote URL
git remote -v

# If wrong fork, change it
git remote set-url origin https://github.com/YOUR_USERNAME/is117_ai_test_practice.git

# Verify
git remote -v

# Try push again
git push
```

---

### npm Errors

#### Error: "Cannot find module"

**Full error:**

```bash
Error: Cannot find module 'eleventy'
    at Function.Module._resolveFilename (node:internal/modules/cjs/loader:1048:15)
```

**Meaning:** Package not installed

**Fixes:**

```bash
# Install all dependencies
npm install

# Verify installation
npm list eleventy

# Try command again
npm start
```

---

#### Error: "ENOENT: no such file or directory"

**Full error:**

```bash
npm ERR! enoent ENOENT: no such file or directory, open '/path/to/package.json'
```

**Meaning:** Not in project directory

**Fixes:**

```bash
# Check location
pwd

# Navigate to project
cd /path/to/is117_ai_test_practice

# Verify package.json exists
ls -la package.json

# Try command again
npm install
```

---

### Pre-commit Hook Errors

#### Error: "Hook failed, commit blocked"

**Full error:**

```bash
✗ eslint --fix found errors:
  src/js/main.js:5:10  error  'x' is not defined

✗ Pre-commit hook failed
```

**Meaning:** Code has errors, commit blocked

**Fixes:**

```bash
# View the error details above
# Fix the specific issue (in this case, define 'x')

# Verify fix
npm run lint:js

# Re-stage fixed files
git add src/js/main.js

# Try commit again
git commit -m "your message"
```

---

## 🔍 Debugging Workflow

### Step-by-Step Process:

```
1. Error occurs
      ↓
2. Don't panic! Read error message
      ↓
3. Copy exact error text
      ↓
4. Identify tool (ESLint? Eleventy? Git?)
      ↓
5. Check this guide for that tool
      ↓
6. Try suggested fix
      ↓
7. Test if fixed
      ↓
8. Still broken? Search error online
      ↓
9. Still stuck? Ask for help with:
   - Exact error message
   - What you were doing
   - What you've tried
```

---

## 💡 Using AI for Debugging

### Prompt Template for AI Assistants:

```
I'm getting this error in my Eleventy project:

[Paste exact error message]

I was trying to: [Describe what you were doing]

Here's my file:
[Paste relevant code]

What's causing this and how do I fix it?
```

---

### Example:

```
I'm getting this error in my Eleventy project:

[11ty] TemplateContentRenderError: variable 'title' is not defined

I was trying to: Build my site after editing index.md

Here's my file (src/index.md):
---
layout: base.njk
---
# Welcome

What's causing this and how do I fix it?
```

**AI Response:** "You're missing the `title` field in your front matter. Add it
like this: ..."

---

## 🔧 Testing Your Fixes

### After fixing any issue:

```bash
# 1. Run relevant check
npm run lint:js      # If JS error
npm run lint:css     # If CSS error
npm run build        # If Eleventy error

# 2. Run all checks
npm test

# 3. If all pass, commit
git add .
git commit -m "fix: resolve [issue]"
git push
```

---

## 🚨 Emergency Fixes

### "Everything is broken!"

**Nuclear option (use carefully):**

```bash
# 1. Stash your changes
git stash

# 2. Clean install
rm -rf node_modules package-lock.json
npm install

# 3. Verify clean state works
npm test

# 4. Restore your changes
git stash pop

# 5. Fix any conflicts
npm test
```

---

### "I committed something wrong!"

**Undo last commit:**

```bash
# Undo commit, keep changes
git reset HEAD~1

# Fix the issues
# ...

# Commit again
git add .
git commit -m "corrected commit"
```

---

### "My branch is a mess!"

**Start fresh from main:**

```bash
# Save your work elsewhere (copy files)

# Get clean main branch
git checkout main
git pull origin main

# Create new branch
git checkout -b feature/new-attempt

# Carefully add your changes back
# Test as you go
```

---

## 🎮 Practice Debugging (3 minutes)

### Challenge: Create and Fix Errors

**1. Create syntax error:**

```javascript
// src/js/debug-test.js
const message = 'hello'; // Missing semicolon
console.log(message);
```

**Run check:**

```bash
npm run lint:js
# Should catch missing semicolon
```

**Fix it:**

```bash
npm run lint:js -- --fix
# Auto-fixes!
```

---

**2. Create CSS duplication:**

```css
/* src/css/debug-test.css */
.test {
  color: red;
}
.test {
  color: blue;
} /* Duplicate! */
```

**Run check:**

```bash
npm run lint:css
# Should catch duplicate
```

**Fix it manually:**

```css
.test {
  color: blue;
} /* Keep one */
```

---

**3. Clean up:**

```bash
rm src/js/debug-test.js src/css/debug-test.css
git status  # Should show deleted files
```

---

## 📊 Troubleshooting Checklist

You've mastered troubleshooting when you can:

- [ ] Read and understand error messages
- [ ] Identify which tool is reporting the error
- [ ] Look up errors in this guide
- [ ] Search for errors online effectively
- [ ] Use AI assistants for debugging
- [ ] Test fixes systematically
- [ ] Undo changes with Git when needed
- [ ] Ask for help with proper context
- [ ] Stay calm when errors occur
- [ ] Learn from each bug you fix

**All checked?** You're a debugging pro! 🎉

---

## 📚 Key Takeaways

### ✅ DO:

- Read complete error messages
- Check one thing at a time
- Test after each fix
- Use version control to undo mistakes
- Search for exact error text
- Ask AI assistants for help
- Document fixes for future reference
- Stay patient and methodical

### ❌ DON'T:

- Panic when errors occur
- Change multiple things at once
- Ignore warnings (they become errors later)
- Skip testing after fixes
- Commit broken code
- Give up without asking for help
- Delete files without backing up

---

## 🎯 Error Prevention Checklist

**Before committing:**

- [ ] Run `npm test` locally
- [ ] Check for console errors in browser
- [ ] Verify site builds (`npm run build`)
- [ ] Test site in browser (`npm start`)
- [ ] Review your changes (`git diff`)

**Before pushing:**

- [ ] Pull latest from main (`git pull`)
- [ ] Resolve any conflicts
- [ ] Run `npm test` again
- [ ] Commit message is clear

**Before deploying:**

- [ ] All CI/CD checks pass
- [ ] Review deployment preview
- [ ] Test on mobile
- [ ] Check Lighthouse scores

---

## 📊 Progress Tracker

**🎉 Congratulations! You've completed all lessons!**

- [x] ~~Lesson 1: What Is This Project?~~
- [x] ~~Lesson 2: Why Quality Gates?~~
- [x] ~~Lesson 3: Prompt Engineering Basics~~
- [x] ~~Lesson 4: Setup Your Environment~~
- [x] ~~Lesson 5: Build with Eleventy~~
- [x] ~~Lesson 6: ESLint & Prettier~~
- [x] ~~Lesson 7: Pre-commit Hooks~~
- [x] ~~Lesson 8: GitHub Actions~~
- [x] ~~Lesson 9: Lighthouse CI~~
- [x] ~~Lesson 10: Troubleshooting~~

**✅ Course Complete!**

---

## 🚀 What You've Learned

You now know how to:

✅ Build static sites with Eleventy ✅ Write quality code with ESLint & Prettier
✅ Prevent duplication with automated checks ✅ Enforce quality with pre-commit
hooks ✅ Deploy automatically with GitHub Actions ✅ Optimize performance with
Lighthouse ✅ Debug and fix common issues ✅ Work effectively with AI coding
assistants ✅ Maintain DRY, clean codebases ✅ Build production-ready websites

---

## 🎓 Next Steps

### Continue Learning:

1. **Build your own project**
   - Use this template
   - Create portfolio site
   - Add custom features

2. **Deepen knowledge**
   - Advanced Eleventy patterns
   - Complex CSS layouts
   - JavaScript interactivity

3. **Share your work**
   - Deploy to GitHub Pages
   - Share on social media
   - Help others learn

---

## 🔗 Quick Reference Card

**Development Commands:**

```bash
npm start            # Dev server with hot reload
npm run build        # Production build
npm test             # Run all quality checks
npm run format       # Auto-format all files
```

**Debugging Commands:**

```bash
npm run lint:js      # Check JavaScript
npm run lint:css     # Check CSS
npm run lint:md      # Check Markdown
npm run lint:duplication  # Check for duplication
```

**Git Commands:**

```bash
git status           # See what changed
git add .            # Stage all changes
git commit -m "msg"  # Commit with message
git push             # Push to GitHub
git reset HEAD~1     # Undo last commit
```

---

## 🆘 Getting Help

### When stuck:

1. **Check this guide** - Most issues covered here
2. **Check reference docs** - `docs/reference/`
3. **Search online** - Copy exact error message
4. **Ask AI assistant** - Use prompt template above
5. **Ask classmate** - Share error details
6. **Ask instructor** - Provide full context

### When asking for help, include:

- Exact error message (copy-paste)
- What you were trying to do
- What you've already tried
- Relevant code (formatted)
- Screenshots if helpful

---

## � Working Without These Tools?

### What if your team doesn't have automated quality gates?

**Reality Check:** Not every project will have pre-commit hooks, CI/CD, and
duplication detection. Here's how to maintain quality manually:

#### 1. **Internalize the Checklist**

Before every commit, manually verify:

```bash
# Run these commands yourself (no hooks to force you)
npm run lint         # Check for errors
npm run format       # Format code
npm test            # Run tests
git diff            # Review what changed
```

#### 2. **Develop Your Internal Quality Sensor**

Ask yourself before committing:

- ✅ Did I check for existing similar code?
- ✅ Is this code readable in 6 months?
- ✅ Would this pass code review?
- ✅ Did I test this change?
- ✅ Am I solving the root problem or patching symptoms?

#### 3. **Champion Quality on Your Team**

If tools don't exist, introduce them:

- Share this project as an example
- Add ESLint/Prettier (low-hanging fruit)
- Propose pre-commit hooks (easy win)
- Document quality standards
- Lead by example

#### 4. **Use Manual Tools**

Without automation:

- **Browser DevTools** - Test manually in console
- **Code Review Checklist** - Print and use for self-review
- **grep for duplication** - `grep -r "functionName" src/`
- **Markdown preview** - Check docs before pushing
- **Local testing** - Always run site before committing

#### 5. **Build the Habit**

**The tools taught you what to check—now you can check without them.**

Example routine:

```bash
# Your manual quality workflow
1. Write code
2. Run npm run lint (manually remember)
3. Run npm run format (manually remember)
4. Test in browser (manually remember)
5. git diff (review changes)
6. Commit if all looks good
```

**Key Point:** The tools taught you _what quality looks like_. Even without
automation, you now know:

- What ESLint would catch (unused vars, bugs)
- What Prettier would fix (formatting)
- What duplication looks like (DRY violations)
- What Lighthouse would measure (performance)

**You're not dependent on tools—you learned the principles.**

---

## �🔗 Quick Links

- [🏠 Back to Course Index](/lessons/)
- [📝 Debugging Prompts](/resources/#prompts)
- [📚 Reference Documentation](/resources/#reference)
- [🔧 NPM Scripts Guide](/resources/#reference)

---

## 🎉 Congratulations!

**You've completed the Quality-First Web Development Course!**

You're now equipped to:

- Build professional websites
- Maintain high code quality
- Work effectively with AI tools
- Debug issues confidently
- Deploy automatically
- Optimize for performance

**Keep building, keep learning, and most importantly—keep your code DRY!** 🚀✨

---

**Thank you for learning with us!** 💚
