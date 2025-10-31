# RISD-Inspired Educational Design System

## Design Philosophy

This design system embodies the principles taught at Rhode Island School of
Design (RISD), integrating Swiss/International Typographic Style with modern
educational needs.

### The AI Superpowers Principle

**AI gives you superpowers:** The ability to read and write an inhuman amount of
information. But these powers require three critical foundations:

1. **Vocabulary** - Professional terminology to communicate precisely with AI
2. **Concepts** - Mental models to structure complex problems
3. **Strategic Thinking** - Framework to translate challenges into solutions

This design system teaches **visual vocabulary** - the professional language of
design that enables you to:

- **Critique effectively:** "The hierarchy is unclear" (not "it looks bad")
- **Prompt precisely:** "Review this as a Fortune 100 marketing executive"
- **Think systematically:** "Apply Swiss grid principles to this layout"

Without vocabulary, AI is like having a Ferrari with no steering wheel. With it,
you can process and create at superhuman scale while maintaining classical
design excellence.

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

5. **Vocabulary-Driven Design**
   - Learn professional terminology to leverage AI effectively
   - Build mental models through named patterns
   - Translate visual problems into precise language

6. **Self-Evident Communication**
   - Design must guide users without external help
   - Every element communicates its purpose visually
   - Users depend on the designer to anticipate their needs
   - No one is there to explain—the interface is the only teacher

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

**Self-Evident Design:**

- Users understand purpose without explanation
- Affordances make interactions obvious
- Visual feedback confirms actions
- Error messages guide toward solutions
- The interface teaches itself

---

## The Designer's Responsibility

### Design Must Communicate Effectively Without You

**The Core Challenge:** Your design must achieve the user's goal when no one is
there to help or provide additional information. The user depends entirely on
you, the designer, to guide them through the process.

**Why This Matters:**

- You won't be there when someone visits your site at 2am
- Users won't read instructions—they'll try things and expect them to work
- Confusion causes abandonment (bounce rate)
- Clear design = conversions; confusing design = lost opportunities

**The Three Communication Layers:**

1. **Visual Affordances** (What can I do here?)
   - Buttons look pressable (shadows, borders, hover states)
   - Links are underlined or distinctly colored
   - Interactive elements respond to hover/focus
   - Disabled elements appear grayed out
   - Forms show what's required before submission

2. **Information Architecture** (Where am I and where can I go?)
   - Clear navigation hierarchy
   - Breadcrumbs show current location
   - Progress indicators for multi-step processes
   - Consistent layout across pages
   - Obvious "back" or "cancel" options

3. **Feedback & Guidance** (Did my action work? What happens next?)
   - Loading states for async actions
   - Success messages after form submission
   - Error messages that explain AND solve ("Email format invalid" vs "Use
     format: name@example.com")
   - Empty states with clear next actions
   - Confirmation dialogs for destructive actions

**Testing for Self-Evidence:**

Ask someone unfamiliar with your site to:

- Find specific information (can they navigate there?)
- Complete a task (can they figure out the steps?)
- Explain what each button does (are affordances clear?)
- Recover from an error (does guidance exist?)

If they struggle, your design isn't communicating effectively.

**Common Failures of Self-Evident Design:**

❌ **Mystery Meat Navigation:** Icons without labels (what does this do?)  
✅ **Clear Labels:** Icons + text, or universally recognized icons only (home,
search, cart)

❌ **Hidden Actions:** Hover-only menus, no visual clue they exist  
✅ **Visible Options:** Show available actions, use progressive disclosure if
complex

❌ **Generic Errors:** "Error occurred" (what do I do now?)  
✅ **Actionable Errors:** "Email already registered. [Log in] or use different
email."

❌ **Assumptive Design:** Assuming users know industry jargon  
✅ **Plain Language:** Write for humans, explain when necessary

❌ **No Feedback:** Button clicked, nothing visible happens  
✅ **Immediate Response:** Loading state, progress indicator, success message

**The Golden Rule:**

> "If you have to explain how to use it, the design has failed."

Your interface is the only teacher. Design accordingly.

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

## AI Superpowers in Practice

### The Vocabulary Advantage

**Without Design Vocabulary:**

```
Student to AI: "Make this look better"
AI: *Makes generic improvements with no clear direction*
Result: Superficial changes, no strategic thinking
```

**With Design Vocabulary:**

```
Student to AI: "Analyze this layout's visual hierarchy.
The h2 headings feel weak relative to body text.
Suggest type scale adjustments following Swiss design principles
to create clearer information architecture."

AI: *Provides specific typographic improvements with rationale*
Result: Strategic, principled design decisions
```

### Translation Framework: Challenge → Solution

This design system teaches you to **translate problems into solutions** by
providing:

1. **Named Patterns** (vocabulary to describe what you see)
   - "Visual hierarchy is unclear"
   - "Whitespace is cramped"
   - "Color contrast fails WCAG AA"

2. **Mental Models** (concepts to structure thinking)
   - Swiss grid systems
   - Typographic scales
   - 8px spacing rhythm

3. **Strategic Frameworks** (methods to solve problems)
   - "Apply modular scale to establish hierarchy"
   - "Use asymmetric balance for visual tension"
   - "Constrain line length to 65 characters for readability"

### Superhuman Scale with Human Excellence

AI enables you to:

- **Read:** Analyze 100 design systems in minutes
- **Write:** Generate 50 layout variations in seconds
- **Iterate:** Test accessibility across all components instantly

But only if you can:

- **Articulate** what makes design good or bad
- **Recognize** patterns and anti-patterns
- **Evaluate** results against classical principles

**The power isn't in the AI. It's in your ability to guide it with professional
vocabulary and strategic thinking.**

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

---

## The Meta-Lesson

This entire design system is itself an example of **vocabulary building for AI
leverage**:

- Every component has a **name** (learning objective, callout, key concept)
- Every principle has **language** (hierarchy, whitespace, functional elegance)
- Every decision has **rationale** (accessibility, cognitive load, Swiss
  tradition)

When you master this vocabulary, you don't just build better websites. You gain
the superpower to translate any visual challenge into AI-actionable solutions at
inhuman speed while maintaining human excellence.

**That's the goal: Classical design thinking + Modern AI tools = Superhuman
creative capacity.**
