## <!-- markdownlint-disable MD046 -->

layout: lesson.njk title: Design System Demo - Visual Language for Education
lessonNumber: 0 description: Demonstration of the RISD-inspired design system
components timeEstimate: 5 minutes level: Reference tags:

- lessons
- design permalink: /lessons/design-system-demo/

---

This lesson demonstrates all components in our RISD-inspired design system.

<div class="key-concept">
  <span class="key-concept__label">Core Philosophy</span>
  <h3 class="key-concept__title">AI Gives You Superpowers</h3>
  <p class="key-concept__text">AI enables you to read and write an <strong>inhuman amount of information</strong>. But this superpower requires three foundations: <strong>vocabulary</strong> (professional terms), <strong>concepts</strong> (mental models), and <strong>strategic thinking</strong> (translating challenges into solutions). This design system teaches you the visual vocabulary needed to leverage AI effectively.</p>
</div>

## Learning Objectives

<div class="learning-objective">
  <div class="learning-objective__title">You Will Learn</div>
  <ul class="learning-objective__list">
    <li>Professional design vocabulary to communicate with AI precisely</li>
    <li>How to use educational components effectively</li>
    <li>When to apply different callout types</li>
    <li>Best practices for visual hierarchy</li>
    <li>How to translate design challenges into AI-actionable solutions</li>
  </ul>
</div>

## Typography Hierarchy

Our typography system follows Swiss design principles with clear hierarchy:

### Display Heading (H1)

This is the page title - reserved for the main lesson title only.

### Section Heading (H2)

Major concept divisions use H2 - notice the generous spacing above.

### Subsection Heading (H3)

Supporting concepts and detailed explanations use H3.

#### Detail Heading (H4)

Minor points and specific examples use H4.

<p class="text-intro">
This is intro text - larger and more inviting for opening paragraphs. Use it sparingly at the start of major sections to draw readers in.
</p>

Regular body text like this paragraph maintains optimal readability at 16-18px
with 1.6 line-height. Notice how the line length is automatically constrained to
65 characters for comfortable reading.

<p class="text-small">This is small text for secondary information, timestamps, or metadata.</p>

<p class="text-caption">THIS IS CAPTION TEXT - UPPER CASE WITH LETTER SPACING FOR LABELS</p>

---

## Callout Components

### Info Callout

<div class="callout callout--info">
  <p><strong>Did you know?</strong> The Swiss/International Typographic Style emerged in the 1950s, emphasizing clarity, objectivity, and grid-based layouts.</p>
</div>

Use info callouts for **interesting context** that enriches understanding but
isn't critical to the main concept.

### Success Callout

<div class="callout callout--success">
  <p><strong>Great work!</strong> You've successfully applied the design principles. Notice how the generous whitespace creates a sense of calm and professionalism.</p>
</div>

Use success callouts for **positive reinforcement**, completed steps, or
validated understanding.

### Warning Callout

<div class="callout callout--warning">
  <p><strong>Important:</strong> Always test your designs at mobile sizes. What looks perfect on desktop may be illegible on small screens.</p>
</div>

Use warning callouts for **important notices**, common pitfalls, or prerequisite
knowledge.

### Error Callout

<div class="callout callout--error">
  <p><strong>Critical:</strong> Never use font sizes below 12px. Accessibility guidelines require minimum readable text sizes for all users.</p>
</div>

Use error callouts for **critical warnings**, accessibility violations, or
serious mistakes to avoid.

---

## Key Concepts

When introducing a **fundamental principle** that students must remember, use
the key concept component:

<div class="key-concept">
  <span class="key-concept__label">Key Concept</span>
  <h3 class="key-concept__title">Whitespace is Not Empty Space</h3>
  <p class="key-concept__text">In Swiss design, whitespace is an active design element. It creates breathing room for complex ideas, establishes visual hierarchy, and guides the eye through intentional contrast. Think of whitespace as "cognitive rest" - giving the brain time to process before moving to the next concept.</p>
</div>

Use this component **sparingly** - reserve it for the 3-5 core principles per
lesson that students will be tested on.

---

## Step-by-Step Instructions

For procedural learning (setup, tutorials, workflows), use the numbered steps
component:

<ol class="steps">
  <li class="step">
    <h4 class="step__title">Analyze Your Content Hierarchy</h4>
    <p class="step__description">Before applying any design, map out the information structure. What's the main idea? What are supporting points? Which elements need emphasis?</p>
  </li>
  <li class="step">
    <h4 class="step__title">Choose Your Type Scale</h4>
    <p class="step__description">Select sizes from the defined scale (heading-1 through heading-6, body, intro). Don't create custom sizes - the system provides everything you need.</p>
  </li>
  <li class="step">
    <h4 class="step__title">Apply Spacing Consistently</h4>
    <p class="step__description">Use the 8px base grid for all spacing. Choose from space-2 (8px), space-4 (16px), space-6 (24px), space-8 (32px), etc. Consistency reduces cognitive load.</p>
  </li>
  <li class="step">
    <h4 class="step__title">Test Accessibility</h4>
    <p class="step__description">Run Lighthouse audits to verify color contrast meets WCAG AA standards (4.5:1 for body text). Test with keyboard navigation to ensure all interactive elements are accessible.</p>
  </li>
</ol>

Notice how the visual line connects steps to show progression - this is inspired
by timeline diagrams in Swiss educational materials.

---

## Example Boxes

### Basic Example

<div class="example">
  <div class="example__header">Example: Typography Hierarchy</div>
  <div class="example__content">
    <h2 style="margin-top: 0;">This is an H2 heading</h2>
    <p>This is body text that follows. Notice the size relationship: the heading is clearly larger, establishing immediate visual hierarchy.</p>
    <h3>This is an H3 subheading</h3>
    <p>Supporting text continues here with consistent spacing.</p>
  </div>
  <div class="example__caption">
    The size difference between heading levels creates clear structure without relying on color or decoration.
  </div>
</div>

### Side-by-Side Comparison

<div class="example example--comparison">
  <div class="example__side">
    <div class="example__side-label">❌ Avoid</div>
    <div style="background: linear-gradient(90deg, red, yellow, green, blue); padding: 1rem; color: white; text-align: center;">
      TOO MANY COLORS COMPETING FOR ATTENTION
    </div>
  </div>
  <div class="example__side">
    <div class="example__side-label">✓ Better</div>
    <div style="background: #2563eb; padding: 1rem; color: white; text-align: center;">
      Single purposeful color
    </div>
  </div>
</div>

Use comparison examples to **show before/after**, **right vs. wrong**, or **two
valid approaches**.

### The Vocabulary Advantage

<div class="example">
  <div class="example__header">Example: Prompting Without vs. With Design Vocabulary</div>
  <div class="example__content">
    <h4>Without Vocabulary (Vague)</h4>
    <blockquote style="margin: 0 0 1.5rem; padding-left: 1rem; border-left: 3px solid #d4d4d4;">
      "Make this page look better and more professional"
    </blockquote>
    <p style="font-size: 14px; color: #737373; margin-bottom: 2rem;">
      <strong>Result:</strong> AI makes generic changes with no strategic direction. You can't evaluate quality because you don't have the language to critique.
    </p>

    <h4>With Vocabulary (Precise)</h4>
    <blockquote style="margin: 0 0 1rem; padding-left: 1rem; border-left: 3px solid #2563eb;">
      "Analyze this layout's visual hierarchy. The h2 headings appear weak relative to body text. Suggest type scale adjustments following Swiss design principles to create clearer information architecture. Ensure WCAG AA contrast compliance."
    </blockquote>
    <p style="font-size: 14px; color: #737373;">
      <strong>Result:</strong> AI provides specific, principled recommendations you can evaluate and iterate on. You control the outcome through precise language.
    </p>

  </div>
  <div class="example__caption">
    <strong>Key Insight:</strong> Professional vocabulary transforms AI from a random suggestion machine into a strategic design partner. You're not asking for "better" - you're diagnosing specific problems and requesting principled solutions.
  </div>
</div>

---

## Knowledge Checks

At the end of concept sections, test understanding:

<div class="knowledge-check">
  <div class="knowledge-check__header">
    <span class="knowledge-check__icon">?</span>
    <h3 class="knowledge-check__title">Check Your Understanding</h3>
  </div>
  <p class="knowledge-check__question">
    What is the primary purpose of whitespace in educational design?
  </p>
  <ul class="knowledge-check__options">
    <li class="knowledge-check__option">To fill empty areas so the page doesn't look sparse</li>
    <li class="knowledge-check__option knowledge-check__option--correct">To create cognitive breathing room and guide attention</li>
    <li class="knowledge-check__option">To meet minimum page length requirements</li>
    <li class="knowledge-check__option">To save printer ink when students print materials</li>
  </ul>
</div>

_The correct answer is highlighted above. In interactive implementations, you'd
use JavaScript to reveal answers on click._

---

## Glossary Terms

When defining important terminology:

<div class="glossary-term">
  <div class="glossary-term__word">Swiss Design</div>
  <div class="glossary-term__definition">
    A graphic design style that emerged in Switzerland in the 1950s, emphasizing cleanliness, readability, and objectivity. Also known as International Typographic Style. Characterized by grid-based layouts, sans-serif typography, and asymmetric compositions.
  </div>
</div>

<div class="glossary-term">
  <div class="glossary-term__word">Visual Hierarchy</div>
  <div class="glossary-term__definition">
    The arrangement and presentation of elements to show their order of importance. Created through variations in size, color, contrast, alignment, repetition, and proximity.
  </div>
</div>

---

## Assignment Brief

For major projects and assignments:

<div class="assignment">
  <div class="assignment__header">
    <span class="assignment__badge">📝</span>
    <h2 class="assignment__title">Project: Redesign a Learning Page</h2>
  </div>

  <div class="assignment__meta">
    <div class="assignment__meta-item">
      <span class="assignment__meta-label">Due Date</span>
      <span class="assignment__meta-value">End of Week</span>
    </div>
    <div class="assignment__meta-item">
      <span class="assignment__meta-label">Weight</span>
      <span class="assignment__meta-value">Practice</span>
    </div>
    <div class="assignment__meta-item">
      <span class="assignment__meta-label">Type</span>
      <span class="assignment__meta-value">Individual</span>
    </div>
  </div>

  <div class="assignment__objectives">
    <h3 class="assignment__objectives-title">Learning Objectives</h3>
    <ul>
      <li>Apply Swiss design principles to educational content</li>
      <li>Create clear visual hierarchy using type scale</li>
      <li>Use whitespace purposefully for cognitive clarity</li>
      <li>Select appropriate components for different content types</li>
    </ul>
  </div>

  <h3>Instructions</h3>
  <p>Choose one of your existing lesson pages or course materials and redesign it using the components from this design system:</p>

  <ol>
    <li>Analyze the content structure and identify key concepts</li>
    <li>Map content to appropriate components (callouts, key concepts, steps, etc.)</li>
    <li>Apply typography hierarchy using the defined scale</li>
    <li>Use the spacing system consistently throughout</li>
    <li>Test for accessibility (color contrast, keyboard navigation)</li>
  </ol>

  <h3>Submission Requirements</h3>
  <ul>
    <li>Before and after comparison</li>
    <li>Written reflection on design choices (200 words)</li>
    <li>Lighthouse accessibility audit results</li>
  </ul>
</div>

---

## Color Usage Guide

Our restrained palette serves pedagogy:

**Primary Blue (#2563eb):** Trust, intelligence, clarity

- Use for: Primary actions, links, important UI elements
- Psychology: Creates sense of professionalism and reliability

**Secondary Orange (#f97316):** Energy, creativity, action

- Use for: Highlights, progress indicators, success states
- Psychology: Draws attention without alarm

**Neutrals (Grays):** Structure and readability

- Use for: Text, backgrounds, borders, subtle distinctions
- Psychology: Creates calm, professional environment for learning

**Semantic Colors:**

- Success Green: Positive reinforcement, correct answers
- Warning Amber: Important notices, proceed with caution
- Error Red: Critical warnings, mistakes to avoid
- Info Blue: Additional context, helpful tips

---

## Best Practices Summary

### Do:

- Use components as designed (they're tested and accessible)
- Follow the spacing scale religiously (8px grid)
- Limit colors to 2-3 per component
- Test at mobile sizes
- Think modularly - mix and match components

### Don't:

- Create custom font sizes (use the scale)
- Center everything (asymmetry is powerful)
- Over-use callouts (max 2-3 per page)
- Fight the system (constraints enable creativity)
- Sacrifice accessibility for aesthetics

---

## Resources

<div class="callout callout--info">
  <p><strong>Want to learn more?</strong> Read the complete <a href="/docs/DESIGN-SYSTEM-GUIDE/">Design System Guide</a> for in-depth documentation, implementation examples, and accessibility guidelines.</p>
</div>

### Further Reading

- Josef Müller-Brockmann: _Grid Systems in Graphic Design_
- Massimo Vignelli: _The Vignelli Canon_
- Edward Tufte: _The Visual Display of Quantitative Information_
- Swiss education design archives:
  [swissdesignawards.ch](https://www.swissdesignawards.ch/)

---

<div class="lesson-nav">
  <a href="/lessons/" class="lesson-nav__link lesson-nav__link--prev">
    <span class="lesson-nav__label">← Back to</span>
    <span class="lesson-nav__title">All Lessons</span>
  </a>
  <a href="/lessons/01-what-is-this/" class="lesson-nav__link lesson-nav__link--next">
    <span class="lesson-nav__label">Next Lesson →</span>
    <span class="lesson-nav__title">What We're Building</span>
  </a>
</div>
