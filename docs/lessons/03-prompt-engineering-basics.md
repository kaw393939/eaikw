---
layout: lesson.njk
title: 'Prompt Engineering Basics'
lessonNumber: 3
description: 'Learn to write effective prompts that generate quality code'
timeEstimate: '5 minutes'
level: 'Beginner'
tags: ['lessons']
permalink: '/lessons/03-prompt-engineering-basics/'
---

⏱️ **Time:** 5 minutes 📚 **Level:** Beginner 🎯 **Goal:** Learn to write
effective prompts that generate quality code

---

## 🚀 TL;DR

**Good prompts** = **Good code**. Learn the framework: Context + Task +
Constraints + Format.

---

## 🎯 What Is Prompt Engineering?

**Prompt engineering** is the skill of communicating with AI coding assistants
to get the results you want.

### Bad Prompt:

```
"Make a website"
```

**Result:** Generic, unusable code

### Good Prompt:

```
"Create an Eleventy layout file named 'base.njk' that includes:
- Semantic HTML5 structure
- Responsive viewport meta tag
- Link to '/styles/main.css'
- Navigation with Home and About links
- Main content block with {{ content | safe }}
- Footer with copyright

Use Nunjucks template syntax."
```

**Result:** Specific, production-ready code

---

## 🏗️ The C-T-C-F Framework

### **C**ontext + **T**ask + **C**onstraints + **F**ormat

This simple framework ensures your AI understands exactly what you need.

### 1. **Context** (What's the situation?)

Tell the AI about your project:

```
"I'm building an Eleventy static site with..."
"This is a Node.js project that uses..."
"Working on a CSS file for responsive design..."
```

### 2. **Task** (What do you want?)

Be specific about the action:

```
"Create a..."
"Fix the bug in..."
"Refactor this code to..."
"Explain how..."
```

### 3. **Constraints** (What are the rules?)

Specify requirements and limitations:

```
"Must follow ESLint rules"
"Should be accessible (WCAG 2.1 AA)"
"Use only vanilla JavaScript (no frameworks)"
"Keep bundle size under 100KB"
```

### 4. **Format** (How should it look?)

Describe the expected output:

```
"Return just the code, no explanations"
"Explain each step with comments"
"Show before and after examples"
"Include error handling"
```

---

## 📚 Real Examples

### Example 1: Creating a Component

#### ❌ Weak Prompt:

```
"I need a button"
```

#### ✅ Strong Prompt:

```
**Context:** Building an Eleventy site with accessible components

**Task:** Create a reusable button component in HTML/CSS

**Constraints:**
- Must meet WCAG 2.1 AA standards
- Should have hover and focus states
- Include disabled state styling
- Use CSS custom properties for colors

**Format:** Provide separate HTML and CSS files with comments
```

### Example 2: Fixing a Bug

#### ❌ Weak Prompt:

```
"This doesn't work"
```

#### ✅ Strong Prompt:

```
**Context:** Eleventy site deployed to GitHub Pages with pathPrefix '/my-repo/'

**Task:** Fix the broken CSS and JS links on deployed site

**Constraints:**
- Links must work in both dev (localhost) and production
- Use Eleventy's url filter
- Don't hardcode the path prefix

**Format:** Show the fix with before/after code examples
```

### Example 3: Configuring Tools

#### ❌ Weak Prompt:

```
"Set up ESLint"
```

#### ✅ Strong Prompt:

```
**Context:** Node.js project using ES6+ modules, browser environment

**Task:** Create .eslintrc.json configuration

**Constraints:**
- Use recommended ESLint rules
- Include browser globals
- Set ECMAScript 2022
- Warn on console.log (not error)

**Format:** Complete JSON file with inline comments explaining key settings
```

---

## 🎨 Prompt Patterns for Common Tasks

### Pattern 1: Creating Files

```
Create a [FILE_TYPE] named [FILENAME] that [PURPOSE].

Requirements:
- [REQUIREMENT_1]
- [REQUIREMENT_2]
- [REQUIREMENT_3]

Use [TECHNOLOGY/FRAMEWORK] syntax.
```

**Example:**

```
Create a Nunjucks layout file named 'post.njk' that displays blog posts.

Requirements:
- Extends base.njk layout
- Shows post title, date, and author
- Includes post content with safe filter
- Has previous/next post navigation

Use Nunjucks template syntax with Eleventy data.
```

### Pattern 2: Debugging

```
I'm getting [ERROR_MESSAGE] when [ACTION].

Environment:
- [TOOL_1]: version X
- [TOOL_2]: version Y

Current code:
[PASTE CODE]

Expected: [WHAT SHOULD HAPPEN]
Actual: [WHAT'S HAPPENING]

Help me fix this.
```

### Pattern 1b: Creating Styles (DRY-Focused)

```
I need to style [COMPONENT].

First, check these existing files for similar styles:
- src/styles/main.css

If similar styles exist:
- REUSE them by applying existing classes
- If modification needed, UPDATE the existing rule

Only create NEW styles if:
- No similar styles exist
- The component is truly unique

Follow these rules:
- Use existing CSS custom properties (variables)
- Match existing naming conventions
- Keep specificity low
- Avoid !important

Show me:
1. What existing styles can be reused
2. What (if anything) needs to be created
3. The minimal CSS needed
```

### Pattern 3: Refactoring

```
Refactor this code to [IMPROVEMENT_GOAL]:

Current code:
[PASTE CODE]

Constraints:
- Must maintain [FUNCTIONALITY]
- Should improve [METRIC]
- Keep [REQUIREMENT]

Show before and after with explanation of changes.
```

### Pattern 4: Explaining Concepts

```
Explain [CONCEPT] in the context of [YOUR_PROJECT].

I need to understand:
1. [QUESTION_1]
2. [QUESTION_2]
3. [QUESTION_3]

Use examples from [TECHNOLOGY] and keep it concise.
```

---

## 💡 Pro Tips

### Tip 1: Iterate on Prompts

```
First try:  "Create a navigation menu"
            → Too generic

Second try: "Create a responsive navigation menu with mobile hamburger"
            → Better, but missing details

Third try:  "Create a responsive navigation menu in HTML/CSS that:
             - Shows horizontal links on desktop
             - Collapses to hamburger icon on mobile (<768px)
             - Uses accessible ARIA labels
             - Includes smooth transitions"
            → Perfect! ✅
```

### Tip 2: Include Error Messages

When debugging, ALWAYS include the full error:

```
I'm getting this error:

```

Error: Cannot find module '.eleventy.js' at Module.\_resolveFilename
(node:internal/modules/cjs/loader:1039:15)

```

My .eleventy.js file is in the root directory. What's wrong?
```

### Tip 3: Specify Your Stack

AI needs to know what tools you're using:

```
**My Stack:**
- Eleventy 2.0.1
- Node.js 20
- ESLint 8.x
- Prettier 3.x
- No React/Vue/frameworks

[Your question here]
```

### Tip 4: Ask for Explanations

```
"Create a GitHub Actions workflow that [TASK].

After providing the code, explain:
1. What each step does
2. Why these settings are recommended
3. Common gotchas to watch for"
```

### Tip 5: Request Quality Checks

```
"Create [COMPONENT] and ensure it:
- Passes ESLint with no warnings
- Is formatted with Prettier
- Includes JSDoc comments
- Has error handling"
```

### Tip 6: Enforce DRY (Don't Repeat Yourself) ⚠️

**CRITICAL:** AI coding agents often duplicate existing code instead of reusing
it!

```
"Before creating new CSS, check if styles already exist in:
- src/styles/main.css

If similar styles exist, REUSE them. If modification needed, UPDATE the existing rule.

DO NOT create duplicate CSS rules.
DO NOT copy-paste existing styles with minor changes.

Add new styles ONLY if truly unique."
```

**Why this matters:**

- AI will generate duplicate `.button` classes instead of using existing ones
- AI creates new utility classes that already exist
- Results in bloated, unmaintainable CSS

---

## 🚨 Common Prompt Mistakes

### Mistake 1: Too Vague

❌ "Fix my code" ✅ "Fix the ESLint error 'no-unused-vars' on line 23 of
src/js/main.js"

### Mistake 2: Missing Context

❌ "Add a sitemap" ✅ "Add a sitemap.xml for my Eleventy site deployed at
<https://example.com/my-repo/>"

### Mistake 3: No Constraints

❌ "Style this button" ✅ "Style this button with CSS that works in IE11+, uses
BEM naming, and has 44x44px minimum tap target"

### Mistake 4: Assuming Knowledge

❌ "Use the usual ESLint config" ✅ "Use ESLint with Airbnb style guide,
ECMAScript 2022, and browser environment"

### Mistake 5: One-Size-Fits-All

❌ Using same generic prompt for every task ✅ Customizing prompts based on
specific needs

---

## 🎮 Practice Activity (2 minutes)

### Exercise: Improve These Prompts

#### Prompt A (Weak):

```
"Create a footer"
```

**Your improved version:**

```
[Think about: What goes in a footer? What tech stack? What style?]
```

<details>
<summary>See Suggested Answer</summary>

```
Create a semantic HTML5 footer component for an Eleventy site that includes:
- Copyright notice with current year (use Eleventy date filter)
- Social media links (GitHub, Twitter, LinkedIn)
- Accessible link text (not just icons)
- Flexbox layout: left-aligned copyright, right-aligned social links

Provide HTML and CSS using BEM naming convention.
```

</details>

#### Prompt B (Weak):

```
"GitHub Actions not working"
```

**Your improved version:**

```
[Think about: What's the error? What's it supposed to do? What's your setup?]
```

<details>
<summary>See Suggested Answer</summary>

```
My GitHub Actions deployment workflow is failing with error:
"Error: Process completed with exit code 1"

Workflow should:
1. Run on push to main branch
2. Install Node.js 20
3. Run npm install
4. Build Eleventy site
5. Deploy to GitHub Pages

Current workflow file: [paste workflow YAML]
Repository settings: GitHub Pages source is "GitHub Actions"

What's causing the failure and how do I fix it?
```

</details>

---

## ✅ Knowledge Check

Test your understanding:

- [ ] Can you explain the C-T-C-F framework?
- [ ] Can you identify what's missing in a weak prompt?
- [ ] Do you know when to include error messages?
- [ ] Can you write a prompt for creating a new file?
- [ ] Can you write a prompt for debugging an issue?

---

## 📋 Your Prompt Checklist

Before submitting a prompt, verify:

- [ ] **Context:** Did I explain my project setup?
- [ ] **Task:** Is it clear what I want the AI to do?
- [ ] **Constraints:** Did I specify requirements and limitations?
- [ ] **Format:** Did I describe the expected output format?
- [ ] **Specific:** Could someone else understand what I need?
- [ ] **Error messages:** Did I include full error text if debugging?
- [ ] **Code:** Did I paste relevant existing code if modifying?

---

## 🎯 Quick Reference Card

Save this for later:

```
┌─────────────────────────────────────────┐
│     PROMPT ENGINEERING CHEAT SHEET      │
├─────────────────────────────────────────┤
│ CONTEXT  = Your project setup          │
│ TASK     = What you want done          │
│ CONSTRAINTS = Rules and requirements   │
│ FORMAT   = Expected output structure   │
├─────────────────────────────────────────┤
│ ALWAYS INCLUDE:                         │
│ • Technology stack                      │
│ • Version numbers                       │
│ • Error messages (when debugging)       │
│ • Existing code (when modifying)        │
├─────────────────────────────────────────┤
│ PRO TIPS:                               │
│ • Be specific, not vague                │
│ • Iterate on prompts                    │
│ • Request explanations                  │
│ • Ask for quality checks                │
└─────────────────────────────────────────┘
```

---

## 📊 Progress Tracker

You've completed:

- [x] ~~Lesson 1: What Is This Project?~~
- [x] ~~Lesson 2: Why Quality Gates?~~
- [x] ~~Lesson 3: Prompt Engineering Basics~~
- [ ] Lesson 4: Setup Your Environment
- [ ] Lessons 5-10...

---

## 🚀 Next Steps

Now that you know **how** to communicate with AI, let's get your development
environment ready!

### [👉 Continue to Lesson 4: Setup Your Environment](/lessons/04-setup-your-environment/)

---

## 🔗 Quick Links

- [🏠 Back to Course Index](/lessons/)
- [📝 All Copy-Paste Prompts](/resources/#prompts)
- [📚 Reference: AI Assistant Guide](/resources/#reference)

---

**Pro Tip:** Save your best prompts! Build a personal library of prompts that
work well for your workflow. 📚
