---
layout: lesson.njk
title: 'ESLint & Prettier'
lessonNumber: 6
description:
  'Understand how ESLint and Prettier enforce code quality automatically'
timeEstimate: '11 minutes'
level: 'Beginner'
tags: ['lessons']
permalink: '/lessons/06-eslint-prettier/'
---

⏱️ **Time:** Reading: 6 min | Practice: 5 min | Total: ~11 min 📚 **Level:**
Beginner 🎯 **Goal:** Understand how ESLint and Prettier enforce code quality
automatically

---

## 🚀 TL;DR

**ESLint** finds bugs and bad patterns in JavaScript. **Prettier** formats code
consistently. Together they make your code clean, readable, and
bug-free—automatically!

---

## 🤔 What Are These Tools?

### ESLint (The Bug Finder)

**Purpose:** Finds problems in JavaScript code

**Catches:**

- Syntax errors
- Unused variables
- Missing semicolons
- Potential bugs
- Bad practices

**Example:**

```javascript
// ❌ ESLint catches this
function greet(name) {
  const greeting = 'Hello'; // Unused variable!
  console.log('Hi ' + name);
}

// ✅ ESLint approves this
function greet(name) {
  console.log('Hi ' + name);
}
```

---

### Prettier (The Formatter)

**Purpose:** Makes code look consistent

**Formats:**

- Indentation (2 spaces)
- Line length (80 chars)
- Quotes (single vs double)
- Semicolons
- Trailing commas

**Example:**

```javascript
// ❌ Before Prettier (messy)
function calculate(a, b, c) {
  return a + b + c;
}

// ✅ After Prettier (clean)
function calculate(a, b, c) {
  return a + b + c;
}
```

---

## 📁 Configuration Files

### .eslintrc.json (ESLint Rules)

**Location:** Root of project

**What it does:** Defines what ESLint checks for

**Our configuration:**

```json
{
  "env": {
    "browser": true,
    "es2021": true,
    "node": true
  },
  "extends": ["eslint:recommended", "prettier"],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "rules": {
    "no-unused-vars": "warn",
    "no-console": "off"
  }
}
```

**Key parts:**

- `extends: ["eslint:recommended"]` - Use standard best practices
- `extends: ["prettier"]` - Don't conflict with Prettier
- `rules` - Custom rules for our project

---

### .prettierrc (Prettier Settings)

**Location:** Root of project

**What it does:** Defines formatting style

**Our configuration:**

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": false,
  "printWidth": 80,
  "tabWidth": 2
}
```

**What these mean:**

- `semi: true` - Use semicolons
- `trailingComma: "es5"` - Trailing commas where valid
- `singleQuote: false` - Use double quotes
- `printWidth: 80` - Max 80 characters per line
- `tabWidth: 2` - 2 spaces for indentation

---

## 🏃 Running the Tools

### Check JavaScript (ESLint)

```bash
npm run lint:js
```

**What happens:**

```bash
✓ 2 files checked
✓ 0 errors
✓ 1 warning

src/.eleventy.js
  1:1  warning  Unexpected console statement  no-console

✓ ESLint passed (1 warning is acceptable)
```

**✅ Passing:** No errors (warnings are OK in this project)

---

### Check CSS (Stylelint)

```bash
npm run lint:css
```

**What happens:**

```bash
✓ 1 file checked
✓ 0 errors
✓ 0 warnings

✓ Stylelint passed
```

**✅ Passing:** No errors or warnings

---

### Check Formatting (Prettier)

```bash
npm run lint:format
```

**What happens:**

```bash
Checking formatting...
All files formatted correctly!
✓ Prettier passed
```

**✅ Passing:** All files match Prettier rules

---

### Check Everything

```bash
npm run lint
```

**What happens:**

```bash
> npm run lint:js && npm run lint:css && npm run lint:md && npm run lint:format && npm run lint:duplication

✓ ESLint passed
✓ Stylelint passed
✓ Markdownlint passed
✓ Prettier passed
✓ Duplication check passed (0.0%)
```

**✅ All checks passed!**

---

## 🔧 Fixing Issues Automatically

### Auto-Fix JavaScript

```bash
npm run lint:js -- --fix
```

**Fixes:**

- Unused variables (removes them)
- Missing semicolons (adds them)
- Extra spaces (removes them)

**Example:**

```javascript
// Before --fix
let x = 1;
const unused = 'hello';
console.log(x);

// After --fix
let x = 1;
console.log(x);
```

---

### Auto-Format All Files

```bash
npm run format
```

**Formats:**

- JavaScript (`.js`)
- CSS (`.css`)
- Markdown (`.md`)
- JSON (`.json`)
- HTML (`.html`)

**What it does:**

1. Reads file
2. Parses content
3. Reformats according to `.prettierrc`
4. Saves file

**Run this:** Before committing code!

---

## 🎨 How They Work Together

### The Workflow:

```
You Write Code
      ↓
ESLint Checks Logic (catches bugs)
      ↓
Prettier Formats Style (makes it pretty)
      ↓
Clean, Bug-Free Code ✅
```

### Why Both?

- **ESLint** = "Your code has a bug" ❌
- **Prettier** = "Your code should look like this" 🎨
- **Together** = Bug-free AND beautiful ✨

---

## 🚨 Common Errors & Fixes

### Error: "Unexpected var, use let or const"

**Problem:**

```javascript
var name = 'John'; // ❌ Old way
```

**Fix:**

```javascript
const name = 'John'; // ✅ Modern way
```

**Why:** `let`/`const` are safer than `var`

---

### Error: "'x' is assigned but never used"

**Problem:**

```javascript
function calculate() {
  const result = 5 + 5; // ❌ Unused!
  return 10;
}
```

**Fix:**

```javascript
function calculate() {
  const result = 5 + 5;
  return result; // ✅ Used!
}
```

**Why:** Unused variables waste memory

---

### Error: "Missing semicolon"

**Problem:**

```javascript
const x = 5; // ❌ No semicolon
```

**Fix:**

```javascript
const x = 5; // ✅ Semicolon added
```

**Why:** Semicolons prevent weird bugs

---

### Error: "Unexpected console statement"

**Problem:**

```javascript
console.log('Debug message'); // ⚠️ Warning
```

**Fix:**

```javascript
// Remove console.logs before production
// OR keep them (warning is acceptable in our project)
```

**Why:** Console logs clutter production code (but we allow them)

---

### Error: "Expected indentation of 2 spaces"

**Problem:**

```javascript
function test() {
  return true; // ❌ 4 spaces
}
```

**Fix (Run Prettier):**

```bash
npm run format
```

**Result:**

```javascript
function test() {
  return true; // ✅ 2 spaces
}
```

---

## 💡 Pro Tips

### Tip 1: Format on Save (VS Code)

**Enable auto-formatting:**

1. Open VS Code settings (`Cmd+,` or `Ctrl+,`)
2. Search: "format on save"
3. Check: "Editor: Format On Save"
4. Set: "Default Formatter" to "Prettier"

**Result:** Code auto-formats when you save! ✨

---

### Tip 2: Install Extensions

**VS Code Extensions:**

- **ESLint** - Shows errors in editor
- **Prettier** - Formats on save
- **Error Lens** - Shows errors inline

**Install:**

```bash
# Open VS Code
# Press Cmd+Shift+X (Mac) or Ctrl+Shift+X (Windows)
# Search and install each
```

---

### Tip 3: Run Before Commit

**Always run before committing:**

```bash
npm run lint
npm run format
git add .
git commit -m "your message"
```

**Or use pre-commit hooks (covered in Lesson 7!)**

---

### Tip 4: Understand Warnings vs Errors

**Error (🔴):** Must fix (build fails)

```bash
src/main.js
  5:10  error  'x' is not defined  no-undef
```

**Warning (🟡):** Should fix (build succeeds)

```bash
src/main.js
  5:10  warning  Unexpected console  no-console
```

---

## 🎮 Quick Practice Activity (2 minutes)

### Challenge: Fix Bad Code

**Create:** `src/js/test.js`

```javascript
// This code has problems!
var x = 1;
const unused = 'hello';
function test(a, b) {
  console.log(a + b);
}
test(x, 2);
```

**Run checks:**

```bash
npm run lint:js
```

**Fix automatically:**

```bash
npm run lint:js -- --fix
npm run format
```

**Result:**

```javascript
// Clean code!
let x = 1;
function test(a, b) {
  console.log(a + b);
}
test(x, 2);
```

**✅ Fixed!** Delete test file when done.

---

## 🔍 Checking Existing Code (DRY!)

### Before Writing New JavaScript:

```bash
# Search for similar functions
grep -r "function" src/js/

# Search for similar selectors
grep -r "addEventListener" src/js/

# Search for similar logic
grep -r "querySelector" src/js/
```

**Golden Rule:** Check existing code → Reuse if possible → Only then create new

---

### Before Writing New CSS:

```bash
# Search for similar styles
grep -r "display: flex" src/css/
grep -r "color:" src/css/

# Check for similar classes
grep -r "\.button" src/css/
```

**Duplication checker will catch this too!**

---

## 🆘 Need Help?

### 🤖 AI Assistance (Copy-Paste Prompts)

Stuck? Use these ready-made prompts with AI assistants:

- **[Configuration Prompts](/resources/#prompts)** - Setup ESLint/Prettier
- **[Debugging Prompts](/resources/#prompts)** - Fix linting errors
- **[Building Pages Prompts](/resources/#prompts)** - Write DRY code

### 📖 Documentation

- [ESLint Rules](https://eslint.org/docs/rules/)
- [Prettier Options](https://prettier.io/docs/en/options.html)
- [VS Code ESLint Extension](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)

---

## 📊 ESLint & Prettier Checklist

Before moving to the next lesson, verify:

- [ ] Understand ESLint finds bugs
- [ ] Understand Prettier formats code
- [ ] Can run `npm run lint:js`
- [ ] Can run `npm run lint:css`
- [ ] Can run `npm run lint:format`
- [ ] Can run `npm run format` to auto-fix
- [ ] Know common errors and fixes
- [ ] Installed VS Code extensions
- [ ] Enabled "Format on Save"
- [ ] Understand errors vs warnings

**All checked?** Ready for Lesson 7! 🎉

---

## 📚 Key Takeaways

### ✅ DO:

- Run `npm run lint` before committing
- Run `npm run format` to auto-fix formatting
- Install ESLint and Prettier extensions
- Enable "Format on Save" in VS Code
- Fix errors (🔴) immediately
- Check existing code before writing new

### ❌ DON'T:

- Ignore ESLint errors
- Commit unformatted code
- Disable rules without understanding them
- Write duplicate code
- Skip linting checks

---

## 📊 Progress Tracker

You've completed:

- [x] ~~Lesson 1: What Is This Project?~~
- [x] ~~Lesson 2: Why Quality Gates?~~
- [x] ~~Lesson 3: Prompt Engineering Basics~~
- [x] ~~Lesson 4: Setup Your Environment~~
- [x] ~~Lesson 5: Build with Eleventy~~
- [x] ~~Lesson 6: ESLint & Prettier~~
- [ ] Lesson 7: Pre-commit Hooks
- [ ] Lessons 8-10...

---

## 🚀 Next Steps

Now let's automate these checks with pre-commit hooks!

### [👉 Continue to Lesson 7: Pre-commit Hooks](/lessons/07-pre-commit-hooks/)

---

## 🔗 Quick Links

- [🏠 Back to Course Index](/lessons/)
- [📝 Configuration Prompts](/resources/#prompts)
- [📚 NPM Scripts Reference](/resources/#reference)

---

**Your code is now clean and consistent!** 🎨✨
