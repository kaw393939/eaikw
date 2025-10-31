# RISD-Inspired Educational Design System

## Design Philosophy

This design system embodies the principles taught at Rhode Island School of
Design (RISD), integrating Swiss/International Typographic Style with modern
educational needs.

### Core Principles

1. **Clarity Through Hierarchy**
   - Information architecture reflects learning progression
   - Visual weight guides attention strategically
   - Typography creates natural reading rhythm

2. **Generous Whitespace**
   - Cognitive breathing room for complex concepts
   - Swiss-style asymmetric balance
   - Empty space as active design element

3. **Functional Elegance**
   - Every design choice serves pedagogy
   - Restraint over decoration
   - Timeless over trendy

4. **Modular Consistency**
   - Reusable components for scalability
   - Predictable patterns reduce cognitive load
   - System thinking enables rapid prototyping

---

## Typography System

### Font Hierarchy

```
Display (Hero Titles): 67px → 51px → 38px
Headlines (Section Titles): 28px → 21px
Body Text (Content): 18px → 16px → 14px
Captions/Meta: 12px (minimum)
```

### Usage Guidelines

**Headings (`.heading-1` through `.heading-6`):**

- Bold weights for primary hierarchy
- Tight line-height (1.1-1.25) for visual impact
- Negative letter-spacing for display sizes
- Always use semantic HTML (`<h1>`, `<h2>`, etc.)

**Body Text (`.text-body`, `.text-intro`):**

- Base size: 16px with 1.6 line-height
- Intro paragraphs: 18px with 1.75 line-height
- Max-width: 65 characters for optimal readability

**Small Text (`.text-small`, `.text-caption`):**

- Minimum 12px for accessibility
- Use for metadata, timestamps, footnotes
- Upper-case + letterspacing for labels

### Font Pairing

- **Sans-serif (Inter):** UI, headings, body text
- **Serif (Merriweather):** Optional for long-form content
- **Monospace (JetBrains Mono):** Code examples

---

## Color System

### Primary Palette (Trust & Intelligence)

```css
Primary Blue:
- 600 (Main Brand): #2563eb
- Used for: Links, CTAs, primary actions
- Psychology: Trust, professionalism, clarity
```

### Secondary Palette (Energy & Action)

```css
Accent Orange:
- 500 (Accent): #f97316
- Used for: Highlights, progress, success states
- Psychology: Creativity, enthusiasm, warmth
```

### Neutrals (Swiss-Style Grays)

```css
Text Hierarchy:
- Primary (900): #171717 - Headings
- Secondary (600): #525252 - Body text
- Tertiary (500): #737373 - Captions

Background Hierarchy:
- Canvas (White): #ffffff
- Surface (50): #fafafa
- Secondary Surface (100): #f5f5f5
```

### Semantic Colors

```css
Success: #10b981 (Green)
Warning: #f59e0b (Amber)
Error: #ef4444 (Red)
Info: #3b82f6 (Blue)
```

### Usage Guidelines

**Color Restraint:**

- Use color purposefully, not decoratively
- Limit to 2-3 colors per component
- Reserve bright colors for calls-to-action

**Accessibility:**

- All text meets WCAG AA (4.5:1 contrast minimum)
- Interactive elements have 3:1 contrast borders
- Focus states use 3px outlines

---

## Spacing System

### 8px Base Grid

```
--space-1: 4px
--space-2: 8px
--space-4: 16px
--space-6: 24px
--space-8: 32px
--space-12: 48px
--space-16: 64px
--space-24: 96px
```

### Application

**Component Padding:**

- Small: `--space-4` to `--space-6`
- Medium: `--space-8`
- Large: `--space-12` to `--space-16`

**Vertical Rhythm:**

- Paragraph spacing: `--space-4`
- Section spacing: `--space-16` to `--space-24`
- Heading margins: `--space-8` to `--space-12`

**Swiss-Style Asymmetry:**

- Don't center everything
- Use grid for structural alignment
- Whitespace creates visual hierarchy

---

## Educational Components

### Learning Objective Box

```html
<div class="learning-objective">
  <div class="learning-objective__title">Learning Objectives</div>
  <ul class="learning-objective__list">
    <li>Understand Swiss design principles</li>
    <li>Apply typographic hierarchy</li>
    <li>Create modular systems</li>
  </ul>
</div>
```

**When to use:**

- Start of lessons to set expectations
- Before complex concepts
- In assignment briefs

### Callout Boxes

```html
<div class="callout callout--info">
  <p>This is an informational callout</p>
</div>
```

**Variants:**

- `callout--info`: Neutral information
- `callout--success`: Positive reinforcement
- `callout--warning`: Important notices
- `callout--error`: Critical warnings

### Key Concept Highlight

```html
<div class="key-concept">
  <span class="key-concept__label">Key Concept</span>
  <h3 class="key-concept__title">Visual Hierarchy</h3>
  <p class="key-concept__text">
    Visual hierarchy guides the eye through intentional contrast in size,
    weight, and position.
  </p>
</div>
```

**When to use:**

- Core principles students must remember
- Definitions of critical terms
- Breakthrough insights

### Step-by-Step Instructions

```html
<ol class="steps">
  <li class="step">
    <h4 class="step__title">Open VS Code</h4>
    <p class="step__description">
      Launch Visual Studio Code from your Applications folder.
    </p>
  </li>
  <li class="step">
    <h4 class="step__title">Create New File</h4>
    <p class="step__description">Use File > New File or press Cmd+N.</p>
  </li>
</ol>
```

**When to use:**

- Technical tutorials
- Setup instructions
- Multi-stage processes

### Example Boxes

```html
<div class="example">
  <div class="example__header">Example: Swiss Grid System</div>
  <div class="example__content">
    <!-- Your example content -->
  </div>
  <div class="example__caption">
    Notice how the grid creates alignment without rigidity
  </div>
</div>
```

**When to use:**

- Code demonstrations
- Design comparisons (before/after)
- Visual explanations

### Knowledge Checks

```html
<div class="knowledge-check">
  <div class="knowledge-check__header">
    <span class="knowledge-check__icon">?</span>
    <h3 class="knowledge-check__title">Check Your Understanding</h3>
  </div>
  <p class="knowledge-check__question">
    What is the optimal line length for body text?
  </p>
  <ul class="knowledge-check__options">
    <li class="knowledge-check__option">45-75 characters</li>
    <li class="knowledge-check__option">80-100 characters</li>
  </ul>
</div>
```

**When to use:**

- End of concept sections
- Before moving to next lesson
- After code examples

### Assignment Briefs

```html
<div class="assignment">
  <div class="assignment__header">
    <span class="assignment__badge">📝</span>
    <h2 class="assignment__title">Project 1: Personal Portfolio</h2>
  </div>
  <div class="assignment__meta">
    <div class="assignment__meta-item">
      <span class="assignment__meta-label">Due Date</span>
      <span class="assignment__meta-value">Week 10</span>
    </div>
    <div class="assignment__meta-item">
      <span class="assignment__meta-label">Weight</span>
      <span class="assignment__meta-value">40%</span>
    </div>
  </div>
  <div class="assignment__objectives">
    <h3 class="assignment__objectives-title">Objectives</h3>
    <ul>
      <li>Apply design system principles</li>
      <li>Demonstrate responsive design</li>
    </ul>
  </div>
</div>
```

---

## Layout System

### Container Widths

```css
--max-width-prose: 65ch (reading content) --max-width-narrow: 640px
  (forms, focused content) --max-width-reading: 720px (blog posts, lessons)
  --max-width-content: 960px (standard pages) --max-width-wide: 1280px
  (dashboards, galleries);
```

### Grid System

```html
<div class="grid grid--3">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

**Options:**

- `grid--2`: Two columns
- `grid--3`: Three columns
- `grid--4`: Four columns
- Automatically responsive (mobile = 1 column)

### Section Spacing

```html
<section class="section">
  <!-- Standard section padding -->
</section>

<section class="section section--spacious">
  <!-- Extra padding for important sections -->
</section>
```

---

## Best Practices

### For Educational Content

1. **Start with Structure:**
   - Use semantic HTML (`<h1>`, `<p>`, `<section>`)
   - Let design system handle styling
   - Don't fight the typography scale

2. **Guide Attention:**
   - One primary action per section
   - Use callouts sparingly (max 1-2 per page)
   - White space = importance

3. **Maintain Consistency:**
   - Use components as designed
   - Don't create one-off styles
   - Follow the spacing scale

4. **Think Modularly:**
   - Components should work independently
   - Mix and match for variety
   - Test mobile responsiveness

### Swiss Design Principles in Practice

**Grid-Based Layout:**

```html
<div class="container">
  <div class="prose">
    <!-- Content automatically constrained to readable width -->
  </div>
</div>
```

**Asymmetric Balance:**

- Don't center everything
- Use whitespace to create tension
- Align to grid, not to center

**Functional Typography:**

- Size indicates hierarchy
- Weight indicates emphasis
- Spacing indicates relationships

**Restrained Color:**

- Color has meaning (not decoration)
- Gray scale does heavy lifting
- Accent colors for action only

---

## Implementation Examples

### Lesson Page Template

```html
<article class="container container--reading">
  <header class="mt-12 mb-8">
    <h1>Lesson Title</h1>
    <p class="text-intro">Brief lesson introduction</p>
  </header>

  <div class="learning-objective">
    <div class="learning-objective__title">Learning Objectives</div>
    <ul class="learning-objective__list">
      <li>Objective 1</li>
      <li>Objective 2</li>
    </ul>
  </div>

  <h2>Main Concept</h2>
  <p>Explanation of concept...</p>

  <div class="key-concept">
    <span class="key-concept__label">Key Concept</span>
    <h3 class="key-concept__title">Important Principle</h3>
    <p class="key-concept__text">Core principle explanation...</p>
  </div>

  <h3>Step-by-Step Process</h3>
  <ol class="steps">
    <li class="step">
      <h4 class="step__title">Step 1</h4>
      <p class="step__description">Description...</p>
    </li>
  </ol>

  <div class="knowledge-check">
    <!-- Quiz content -->
  </div>
</article>
```

---

## Accessibility Guidelines

### Color Contrast

- All body text: 7:1 minimum (AAA)
- UI text: 4.5:1 minimum (AA)
- Interactive borders: 3:1 minimum

### Focus States

- All interactive elements have visible focus
- 3px outline in primary color
- 3px offset for clarity

### Typography

- Minimum 12px font size (captions only)
- 16px body text minimum
- Line-height 1.5+ for readability

### Keyboard Navigation

- All components keyboard accessible
- Tab order follows visual hierarchy
- Skip links provided for main content

---

## Future Expansion

This system is designed to grow:

- **New components**: Follow existing patterns
- **Color variants**: Use defined palette
- **Spacing adjustments**: Stay on 8px grid
- **Typography tweaks**: Use existing scale

Remember: **Restraint is power.** The best design systems enable creativity
through constraints.
