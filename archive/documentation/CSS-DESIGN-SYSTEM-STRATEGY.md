# CSS Design System Strategy: Fortune 100-Level Framework
## Post-Mortem Analysis & Next Generation Architecture

**Date:** October 29, 2025
**Project:** EverydayAI Educational Platform
**Scope:** Complete CSS framework redesign with enterprise-grade responsive architecture

---

## Executive Summary

### Current State Analysis
After comprehensive audit of the existing CSS system, critical issues identified:

1. **Typography Scaling Crisis**
   - Viewport units (`vw`) scale infinitely, causing oversized text on large displays
   - No container-aware scaling
   - Breakpoint ranges too broad (375px → 1440px)

2. **Spacing System Failures**
   - Fixed spacing (`var(--space-20)` = 96px always) pushes content below fold
   - No viewport-height consideration
   - Inconsistent application of fluid spacing

3. **Responsive Architecture Gaps**
   - Media queries used as patches, not system foundation
   - No component-level responsive behavior
   - Desktop-first thinking in mobile-first world

4. **Maintenance Complexity**
   - 1990 lines of CSS with high specificity conflicts
   - Repeated patterns not abstracted
   - Design tokens not truly systematic

### Recommended Approach
**Container Query-Based Design System** with **Token-Driven Architecture** and **Composition over Inheritance** principles.

---

## Part 1: Core Architecture Philosophy

### 1.1 Container Queries: The Foundation

**Why Container Queries?**
- Components respond to their **container**, not viewport
- Enables true component reusability
- Eliminates media query hell
- Future-proof (98%+ browser support as of 2024)

**Implementation:**
```css
/* OLD - Viewport-based (breaks on large screens) */
.card {
  font-size: clamp(1rem, 2vw, 1.5rem); /* 2vw = 38px at 1920px! */
}

/* NEW - Container-based (scales with parent) */
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card {
  font-size: clamp(1rem, 3cqi, 1.25rem); /* 3cqi = 3% of container width */
}

@container card (min-width: 400px) {
  .card__title {
    font-size: 1.5rem;
  }
}
```

### 1.2 Fluid Space System: Viewport Height Awareness

**Problem:** Current spacing pushes hero content below fold on laptops.

**Solution:** `vh`-based fluid spacing with `clamp()` safety:

```css
/* CURRENT - Fixed spacing */
--space-20: 6rem; /* Always 96px */
.hero { padding: var(--space-20); } /* Pushes below fold */

/* NEXT-GEN - Fluid viewport-relative */
--space-fluid-xs: clamp(0.5rem, 2vh, 1rem);    /* 8px → 16px */
--space-fluid-sm: clamp(1rem, 3vh, 2rem);      /* 16px → 32px */
--space-fluid-md: clamp(2rem, 5vh, 3rem);      /* 32px → 48px */
--space-fluid-lg: clamp(3rem, 8vh, 5rem);      /* 48px → 80px */
--space-fluid-xl: clamp(4rem, 12vh, 8rem);     /* 64px → 128px */

.hero {
  padding-block: var(--space-fluid-lg); /* Responsive to viewport height */
  min-height: clamp(500px, 70vh, 800px); /* Never too tall or short */
}
```

### 1.3 Typography: Utopia + Container Queries

**Current Issue:** Text scales with viewport width, becoming enormous on large screens.

**Solution:** Hybrid approach with container queries for component-level control:

```css
/* BASE SCALE - Utopia formula between 375px → 1440px */
:root {
  --text-xs: clamp(0.75rem, 0.73rem + 0.11vw, 0.875rem);   /* 12→14px */
  --text-sm: clamp(0.875rem, 0.86rem + 0.08vw, 1rem);      /* 14→16px */
  --text-base: clamp(1rem, 0.98rem + 0.09vw, 1.125rem);    /* 16→18px */
  --text-lg: clamp(1.125rem, 1.09rem + 0.17vw, 1.375rem);  /* 18→22px */
  --text-xl: clamp(1.25rem, 1.18rem + 0.34vw, 1.75rem);    /* 20→28px */

  /* Display sizes - MORE CONSERVATIVE */
  --text-2xl: clamp(1.5rem, 1.39rem + 0.54vw, 2rem);       /* 24→32px */
  --text-3xl: clamp(1.875rem, 1.71rem + 0.82vw, 2.5rem);   /* 30→40px */
  --text-4xl: clamp(2rem, 1.86rem + 0.71vw, 3rem);         /* 32→48px */
  --text-5xl: clamp(2.5rem, 2.14rem + 1.79vw, 4rem);       /* 40→64px */
  --text-6xl: clamp(3rem, 2.57rem + 2.14vw, 5rem);         /* 48→80px */
}

/* COMPONENT LEVEL - Container query overrides */
.hero-container {
  container-type: inline-size;
  container-name: hero;
}

.hero__title {
  font-size: var(--text-6xl); /* Base fluid scale */
}

/* Constrain on very large containers */
@container hero (min-width: 1200px) {
  .hero__title {
    font-size: clamp(3rem, 4vw, 4.5rem); /* Cap at 72px */
  }
}
```

---

## Part 2: Token Architecture

### 2.1 Design Token Layers

**Tier 1: Primitive Tokens** (Never used directly in components)
```css
:root {
  /* Color primitives */
  --color-blue-50: #eff6ff;
  --color-blue-500: #3b82f6;
  --color-blue-900: #1e3a8a;

  --color-emerald-500: #10b981;
  --color-emerald-600: #059669;

  /* Size primitives */
  --size-1: 0.25rem;  /* 4px */
  --size-2: 0.5rem;   /* 8px */
  --size-4: 1rem;     /* 16px */
  --size-8: 2rem;     /* 32px */
}
```

**Tier 2: Semantic Tokens** (Component-agnostic meanings)
```css
:root {
  /* Semantic colors */
  --color-primary: var(--color-blue-500);
  --color-primary-hover: var(--color-blue-600);
  --color-success: var(--color-emerald-500);
  --color-text: var(--color-slate-900);
  --color-text-subtle: var(--color-slate-600);

  /* Semantic spacing (fluid) */
  --space-section-block: clamp(4rem, 10vh, 8rem);
  --space-component-gap: clamp(1rem, 2vw, 2rem);
  --space-inline-tight: clamp(0.5rem, 1vw, 1rem);
}
```

**Tier 3: Component Tokens** (Component-specific)
```css
:root {
  /* Hero component */
  --hero-title-size: var(--text-6xl);
  --hero-title-weight: 800;
  --hero-title-line-height: 1.1;
  --hero-padding-block: var(--space-section-block);
  --hero-min-height: clamp(500px, 70vh, 800px);

  /* Card component */
  --card-padding: clamp(1.5rem, 3vw, 2.5rem);
  --card-gap: clamp(1rem, 2vw, 1.5rem);
  --card-radius: 0.75rem;
}
```

### 2.2 Responsive Token Strategy

**Use CSS Custom Properties with Media Query Overrides:**

```css
:root {
  /* Base (mobile-first) */
  --section-padding: clamp(3rem, 8vh, 4rem);
  --heading-size: var(--text-4xl);
  --grid-columns: 1;
}

@media (width >= 768px) {
  :root {
    --section-padding: clamp(4rem, 10vh, 6rem);
    --heading-size: var(--text-5xl);
    --grid-columns: 2;
  }
}

@media (width >= 1024px) {
  :root {
    --grid-columns: 3;
  }
}

/* Components automatically respond */
.section {
  padding-block: var(--section-padding);
}

.grid {
  grid-template-columns: repeat(var(--grid-columns), 1fr);
}
```

---

## Part 3: Component Architecture

### 3.1 Atomic Design Structure

**File Organization:**
```
src/assets/css/
├── tokens/
│   ├── primitives.css      # Raw values
│   ├── semantic.css        # Semantic mappings
│   └── component.css       # Component tokens
├── base/
│   ├── reset.css           # Modern CSS reset
│   └── typography.css      # Base type styles
├── layout/
│   ├── container.css       # Container queries
│   ├── grid.css            # Grid systems
│   └── stack.css           # Spacing utilities
├── components/
│   ├── button.css          # Button component
│   ├── card.css            # Card component
│   ├── hero.css            # Hero component
│   └── navigation.css      # Nav component
└── utilities/
    └── utilities.css       # Utility classes
```

### 3.2 Container Query Pattern

**Every major component gets a container:**

```css
/* Component wrapper establishes container */
.hero-wrapper {
  container-type: inline-size;
  container-name: hero;
}

/* Component uses container queries */
.hero {
  padding: var(--space-fluid-md);
  min-height: var(--hero-min-height);
}

.hero__title {
  font-size: var(--text-5xl);
}

/* Responsive behavior based on CONTAINER width */
@container hero (min-width: 600px) {
  .hero__title {
    font-size: var(--text-6xl);
  }

  .hero__stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
  }
}

@container hero (min-width: 900px) {
  .hero {
    padding: var(--space-fluid-lg);
  }
}
```

### 3.3 Composition Utilities (Not Utility-First)

**Layout primitives for composition:**

```css
/* STACK - Vertical rhythm */
.stack {
  display: flex;
  flex-direction: column;
}

.stack > * + * {
  margin-block-start: var(--stack-space, 1rem);
}

.stack[data-space="sm"] {
  --stack-space: clamp(0.5rem, 2vh, 1rem);
}

.stack[data-space="lg"] {
  --stack-space: clamp(2rem, 5vh, 3rem);
}

/* CLUSTER - Horizontal grouping */
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--cluster-gap, 1rem);
  align-items: var(--cluster-align, flex-start);
}

/* GRID - Responsive auto-grid */
.grid {
  display: grid;
  grid-template-columns: repeat(
    auto-fit,
    minmax(min(var(--grid-min, 250px), 100%), 1fr)
  );
  gap: var(--grid-gap, clamp(1rem, 3vw, 2rem));
}

/* SIDEBAR - Content + sidebar layout */
.sidebar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sidebar-gap, 2rem);
}

.sidebar > :first-child {
  flex-basis: var(--sidebar-width, 250px);
  flex-grow: 1;
}

.sidebar > :last-child {
  flex-basis: 0;
  flex-grow: 999;
  min-inline-size: var(--sidebar-content-min, 50%);
}
```

---

## Part 4: Responsive Strategy

### 4.1 Progressive Enhancement Approach

**Mobile-First Foundation:**
```css
/* BASE - Mobile (0-599px) */
.component {
  --columns: 1;
  --font-size: var(--text-base);
  --padding: var(--space-fluid-sm);
}

/* TABLET - 600px+ */
@media (width >= 600px) {
  .component {
    --columns: 2;
    --font-size: var(--text-lg);
  }
}

/* DESKTOP - 900px+ */
@media (width >= 900px) {
  .component {
    --columns: 3;
  }
}

/* LARGE DESKTOP - 1200px+ */
@media (width >= 1200px) {
  .component {
    --columns: 4;
    --padding: var(--space-fluid-md);
  }
}
```

### 4.2 Breakpoint System

**Standard breakpoints aligned with container queries:**

```css
:root {
  /* Breakpoint tokens */
  --bp-xs: 375px;   /* Small mobile */
  --bp-sm: 600px;   /* Large mobile / Small tablet */
  --bp-md: 900px;   /* Tablet / Small desktop */
  --bp-lg: 1200px;  /* Desktop */
  --bp-xl: 1440px;  /* Large desktop */
  --bp-2xl: 1920px; /* Extra large */
}

/* Corresponding container query breakpoints */
@container (min-width: 600px) { /* sm */ }
@container (min-width: 900px) { /* md */ }
@container (min-width: 1200px) { /* lg */ }
```

### 4.3 Viewport Height Handling

**Critical for above-the-fold content:**

```css
/* HERO - Must fit in viewport */
.hero {
  min-height: clamp(500px, 70vh, 800px);
  padding-block: clamp(2rem, 8vh, 4rem);
}

.hero__content {
  display: flex;
  flex-direction: column;
  gap: clamp(1rem, 3vh, 2rem);
}

/* SECTION - Generous but not excessive */
.section {
  padding-block: clamp(3rem, 10vh, 6rem);
}

/* CARD - Container-relative */
.card {
  padding: clamp(1.5rem, 3cqi, 2.5rem); /* 3% of container */
}
```

---

## Part 5: Implementation Roadmap

### Phase 1: Foundation (Week 1)
**Setup new token system and architecture**

Tasks:
1. Create token hierarchy (primitives → semantic → component)
2. Implement container query base
3. Build layout primitives (stack, cluster, grid, sidebar)
4. Setup new file structure

**Deliverables:**
- `tokens/` folder with complete token system
- `layout/` folder with container-aware primitives
- Base reset and typography

### Phase 2: Component Migration (Week 2)
**Rebuild components with new system**

Priority order:
1. **Hero** - Most visible, highest impact
2. **Navigation** - Present on every page
3. **Cards** - Reused across site
4. **Buttons** - Used everywhere
5. **Typography components** - Headings, paragraphs

**Pattern for each component:**
```css
/* 1. Container wrapper */
.component-wrapper {
  container-type: inline-size;
  container-name: component;
}

/* 2. Base styles (mobile) */
.component {
  /* Use tokens only */
  padding: var(--component-padding);
  gap: var(--component-gap);
}

/* 3. Container queries for responsive behavior */
@container component (min-width: 600px) {
  .component {
    /* Adjustments for medium containers */
  }
}
```

### Phase 3: Testing & Optimization (Week 3)
**Cross-device testing and performance**

Testing matrix:
- Mobile: 375px, 414px (iPhone)
- Tablet: 768px, 834px (iPad)
- Desktop: 1280px, 1440px, 1920px
- Viewport heights: 667px, 800px, 1080px

Performance targets:
- CSS file < 50KB gzipped
- No layout shift (CLS = 0)
- 60fps scroll performance

### Phase 4: Documentation (Week 4)
**Create living style guide**

Components:
1. Storybook-style component showcase
2. Token documentation with visual examples
3. Layout primitive usage guide
4. Responsive behavior documentation

---

## Part 6: Critical Design Decisions

### 6.1 Typography Scale

**REJECTED: Current aggressive scaling**
```css
/* TOO AGGRESSIVE - Causes oversized text */
--text-6xl: clamp(3.75rem, 2.75rem + 5vw, 6.5rem); /* 60→104px */
```

**APPROVED: Conservative with container cap**
```css
/* CONSERVATIVE - Proper scaling */
--text-6xl: clamp(3rem, 2.57rem + 2.14vw, 5rem); /* 48→80px */

/* CONTAINER OVERRIDE - Cap for large containers */
@container hero (min-width: 1200px) {
  .hero__title {
    font-size: clamp(3rem, 4cqi, 4.5rem); /* Max 72px */
  }
}
```

### 6.2 Spacing Philosophy

**REJECTED: Fixed spacing system**
- Predictable but inflexible
- Causes content to push below fold
- Doesn't respond to viewport

**APPROVED: Fluid spacing with vh/vw blend**
```css
/* Vertical spacing - Uses vh for viewport awareness */
--space-section-y: clamp(3rem, 10vh, 6rem);
--space-component-y: clamp(1rem, 3vh, 2rem);

/* Horizontal spacing - Uses vw/cqi for container awareness */
--space-container-x: clamp(1rem, 3vw, 3rem);
--space-card-x: clamp(1rem, 3cqi, 2rem); /* Container query unit */
```

### 6.3 Container vs Viewport Queries

**When to use each:**

**Container Queries (Primary):**
- Component internal layout
- Typography within components
- Component spacing/padding
- Grid column counts

**Viewport Queries (Secondary):**
- Global token adjustments
- Major layout shifts
- Navigation behavior
- Footer layout

**Example:**
```css
/* VIEWPORT - Global token adjustment */
@media (width >= 900px) {
  :root {
    --section-padding: clamp(5rem, 12vh, 8rem);
  }
}

/* CONTAINER - Component-specific */
@container card (min-width: 600px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 2fr;
  }
}
```

---

## Part 7: Migration Strategy

### 7.1 Parallel Development Approach

**Don't rewrite everything at once**

Strategy:
1. Create new CSS alongside existing
2. Wrap new components in `.v2` class
3. Test thoroughly before switching
4. Gradual migration page by page

```html
<!-- OLD SYSTEM -->
<div class="hero-explorer">
  <div class="hero-explorer__content">
    <h1 class="hero-explorer__title">Title</h1>
  </div>
</div>

<!-- NEW SYSTEM (parallel) -->
<div class="v2">
  <div class="hero-wrapper">
    <div class="hero stack" data-space="lg">
      <h1 class="hero__title">Title</h1>
    </div>
  </div>
</div>
```

### 7.2 Component Refactoring Checklist

For each component:
- [ ] Identify all variants and states
- [ ] Extract primitive values to tokens
- [ ] Create semantic token mappings
- [ ] Wrap in container query wrapper
- [ ] Replace breakpoints with container queries
- [ ] Use layout primitives (stack, cluster, etc.)
- [ ] Test at all breakpoints
- [ ] Document in style guide

### 7.3 Quality Gates

**Before merging any component:**
1. ✅ Uses only design tokens (no hardcoded values)
2. ✅ Wrapped in container query
3. ✅ Tested 375px → 1920px
4. ✅ No layout shift on resize
5. ✅ Accessible (keyboard, screen reader)
6. ✅ Performance budget met
7. ✅ Documented with examples

---

## Part 8: HTML Structure Recommendations

### 8.1 Screenshot-Optimized Section Architecture

**CRITICAL REQUIREMENT: Every section must be screenshot-testable**

Each section needs:
1. **Container query wrapper** (for responsive behavior)
2. **Isolation padding** (for clean screenshots)
3. **Data attributes** (for automated testing)
4. **Consistent grid behavior** (no orphaned items)

```html
<!-- SCREENSHOT-OPTIMIZED STRUCTURE -->
<div class="section-isolate"> <!-- Provides screenshot padding -->
  <div class="hero-wrapper" data-testid="hero-section"> <!-- Container query -->
    <section class="hero" data-ux-section="hero">
      <div class="container"> <!-- Max-width constraint -->
        <div class="stack" data-space="lg"> <!-- Layout primitive -->
          <h1 class="hero__title">Title</h1>
        </div>
      </div>
    </section>
  </div>
</div>
```

**Why this structure?**
- `.section-isolate` → Adds viewport padding (200px) for clean screenshots
- `.hero-wrapper` → Container query boundary
- `data-testid` → Playwright can target each section
- `.container` → Prevents content from touching edges
- `.stack` → Consistent vertical rhythm

### 8.2 Grid Consistency Rules (Screenshot-Critical)

**Problem:** Grids that show 2 items when they should show 3 create visual inconsistency in screenshots.

**Solution:** Smart grid with minimum items per row constraint:

```css
/* SMART GRID - Prevents orphaned items */
.grid {
  --grid-min: 280px; /* Minimum card width */
  --grid-gap: clamp(1rem, 3vw, 2rem);
  --grid-items: 3; /* Target items per row */

  display: grid;
  gap: var(--grid-gap);

  /* Formula ensures minimum items per row */
  grid-template-columns: repeat(
    auto-fit,
    minmax(
      max(
        var(--grid-min),
        calc((100% - (var(--grid-gap) * (var(--grid-items) - 1))) / var(--grid-items))
      ),
      1fr
    )
  );
}

/* Responsive grid items target */
@container (max-width: 900px) {
  .grid {
    --grid-items: 2; /* 2 per row on tablet */
  }
}

@container (max-width: 600px) {
  .grid {
    --grid-items: 1; /* 1 per row on mobile */
  }
}
```

**Result:** Grid ALWAYS shows intended number of items per row at each breakpoint.

### 8.3 Section Isolation System (Screenshot Padding)

**CSS for screenshot-perfect sections:**

```css
/* SECTION ISOLATION - Adds padding for screenshots */
.section-isolate {
  padding: var(--screenshot-padding, 200px) 0;
  scroll-margin-top: 200px; /* For anchor links */
}

/* Disable isolation in production */
@media (prefers-reduced-data: reduce) {
  .section-isolate {
    padding: 0;
  }
}

/* Environment-aware padding */
:root {
  --screenshot-padding: 0; /* Default: no padding */
}

/* Enable via data attribute for testing */
[data-screenshot-mode="true"] {
  --screenshot-padding: 200px;
}

/* Or via URL parameter */
@supports selector(:has(*)) {
  :root:has(body[data-test-env="screenshot"]) {
    --screenshot-padding: 200px;
  }
}
```

**Usage in Playwright:**

```javascript
// Enable screenshot mode
await page.addStyleTag({
  content: ':root { --screenshot-padding: 200px; }'
});

// Or via data attribute
await page.evaluate(() => {
  document.documentElement.setAttribute('data-screenshot-mode', 'true');
});

// Take section screenshot
const section = await page.locator('[data-testid="hero-section"]');
await section.screenshot({ path: 'hero.png' });
```

---

## Part 13: Screenshot System Integration

### 13.1 Design Principles for Screenshot Testing

**Core Requirements:**
1. **Viewport-perfect sizing** - Each section fits cleanly in viewport
2. **Consistent grid behavior** - No orphaned items (2 when should be 3)
3. **Isolation padding** - Clean boundaries for screenshots
4. **Data attribute targeting** - Automated test discovery
5. **Multi-device consistency** - Same layout logic across breakpoints

### 13.2 Screenshot-Optimized HTML Pattern

**Every section follows this structure:**

```html
<!-- LAYER 1: Isolation (screenshot padding) -->
<div class="section-isolate" data-section-name="hero">

  <!-- LAYER 2: Container Query Wrapper -->
  <div class="hero-wrapper" data-testid="hero-section">

    <!-- LAYER 3: Semantic Section -->
    <section class="hero" data-ux-section="hero" data-ux-priority="critical">

      <!-- LAYER 4: Content Container (max-width) -->
      <div class="container">

        <!-- LAYER 5: Layout Primitive -->
        <div class="stack" data-space="lg">
          <h1>Content here</h1>
        </div>

      </div>
    </section>
  </div>
</div>
```

**Layer Responsibilities:**
- **Isolation**: Screenshot padding (200px), scroll anchors
- **Wrapper**: Container query boundary, test targeting
- **Section**: Semantic meaning, UX tracking
- **Container**: Max-width constraint, horizontal padding
- **Primitive**: Vertical rhythm, component spacing

### 13.3 Viewport-Perfect Section Sizing

**Each section must fit cleanly in viewport with padding:**

```css
/* SECTION SIZING FORMULA */
.section-content {
  /* Available height = viewport height - isolation padding */
  min-height: clamp(
    400px,                           /* Minimum readable height */
    calc(100vh - 400px),            /* Viewport minus padding */
    1200px                          /* Maximum for ultra-wide */
  );

  /* Ensure content doesn't overflow */
  max-height: calc(100vh - 400px);
  overflow: visible; /* Allow natural flow, not scroll */
}

/* HERO - Always above fold with padding */
.hero {
  min-height: clamp(500px, calc(70vh - 200px), 700px);
  padding-block: clamp(2rem, 8vh, 4rem);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* CARD SECTION - Grid fits viewport */
.card-section {
  padding-block: clamp(3rem, 8vh, 5rem);
}

.card-section .grid {
  /* Grid height shouldn't exceed viewport */
  max-height: calc(100vh - 600px); /* Room for padding + header */
}
```

### 13.4 Consistent Grid System (No Orphans)

**Problem:** Auto-fit grids can show 2 items when you want 3, causing visual inconsistency.

**Solution: Breakpoint-Aware Grid with Item Count Control**

```css
/* BASE GRID SYSTEM */
.grid {
  --grid-min-width: 280px;      /* Minimum card width */
  --grid-max-width: 400px;      /* Maximum card width */
  --grid-gap: clamp(1.5rem, 3vw, 2rem);
  --grid-target-columns: 3;     /* Desired columns */

  display: grid;
  gap: var(--grid-gap);

  /* Smart auto-fit with minimum items */
  grid-template-columns: repeat(
    auto-fit,
    minmax(
      clamp(
        var(--grid-min-width),
        calc((100% - (var(--grid-gap) * (var(--grid-target-columns) - 1))) / var(--grid-target-columns)),
        var(--grid-max-width)
      ),
      1fr
    )
  );
}

/* CONTAINER QUERY OVERRIDES - Explicit column control */
@container section (max-width: 900px) {
  .grid {
    --grid-target-columns: 2;
    grid-template-columns: repeat(2, 1fr); /* Force 2 columns */
  }
}

@container section (max-width: 600px) {
  .grid {
    --grid-target-columns: 1;
    grid-template-columns: 1fr; /* Force 1 column */
  }
}

/* ITEM COUNT VARIANTS - Explicit grid definitions */
.grid[data-columns="3"] {
  grid-template-columns: repeat(3, 1fr);
}

.grid[data-columns="2"] {
  grid-template-columns: repeat(2, 1fr);
}

.grid[data-columns="1"] {
  grid-template-columns: 1fr;
}
```

**HTML Usage:**

```html
<!-- AUTO - Smart responsive grid -->
<div class="grid">
  <div class="card">1</div>
  <div class="card">2</div>
  <div class="card">3</div>
</div>

<!-- EXPLICIT - Force column count (for screenshots) -->
<div class="grid" data-columns="3">
  <div class="card">1</div>
  <div class="card">2</div>
  <div class="card">3</div>
</div>
```

### 13.5 Playwright Screenshot Configuration

**Updated screenshot helper with isolation support:**

```python
# qa_agents/screenshot_helper.py

async def capture_section_screenshot(
    page,
    section_selector: str,
    output_path: str,
    enable_isolation: bool = True,
    viewport_width: int = 1440,
    viewport_height: int = 900
):
    """
    Capture clean section screenshot with isolation padding.

    Args:
        section_selector: CSS selector or data-testid
        enable_isolation: Add padding around section
        viewport_width: Browser viewport width
        viewport_height: Browser viewport height
    """

    # Set viewport
    await page.set_viewport_size({
        'width': viewport_width,
        'height': viewport_height
    })

    # Enable screenshot mode (adds isolation padding)
    if enable_isolation:
        await page.add_style_tag(content="""
            :root {
                --screenshot-padding: 200px;
            }
            .section-isolate {
                padding: var(--screenshot-padding) 0;
            }
        """)

    # Wait for section to be visible
    section = page.locator(section_selector)
    await section.wait_for(state='visible', timeout=5000)

    # Scroll section into view (with isolation padding)
    await section.scroll_into_view_if_needed()

    # Wait for any animations
    await page.wait_for_timeout(1500)

    # Capture screenshot
    await section.screenshot(
        path=output_path,
        animations='disabled'  # Freeze animations for consistency
    )

# USAGE EXAMPLES

# Desktop screenshot (1440x900)
await capture_section_screenshot(
    page,
    '[data-testid="hero-section"]',
    'screenshots/desktop/hero.png',
    viewport_width=1440,
    viewport_height=900
)

# Tablet screenshot (768x1024)
await capture_section_screenshot(
    page,
    '[data-testid="testimonials-section"]',
    'screenshots/tablet/testimonials.png',
    viewport_width=768,
    viewport_height=1024
)

# Mobile screenshot (375x667)
await capture_section_screenshot(
    page,
    '[data-testid="cta-section"]',
    'screenshots/mobile/cta.png',
    viewport_width=375,
    viewport_height=667
)
```

### 13.6 Multi-Device Screenshot Strategy

**Test matrix for each section:**

```python
# qa_agents/device_matrix.py

DEVICE_MATRIX = {
    'mobile': {
        'iPhone SE': {'width': 375, 'height': 667},
        'iPhone 12 Pro': {'width': 390, 'height': 844},
        'iPhone 14 Pro Max': {'width': 430, 'height': 932}
    },
    'tablet': {
        'iPad Mini': {'width': 768, 'height': 1024},
        'iPad Air': {'width': 820, 'height': 1180},
        'iPad Pro': {'width': 1024, 'height': 1366}
    },
    'desktop': {
        'Laptop': {'width': 1280, 'height': 720},
        'Desktop': {'width': 1440, 'height': 900},
        'Large Desktop': {'width': 1920, 'height': 1080}
    }
}

SECTIONS_TO_TEST = [
    {'id': 'hero-section', 'name': 'Hero', 'priority': 'critical'},
    {'id': 'testimonials-section', 'name': 'Testimonials', 'priority': 'high'},
    {'id': 'methodology-section', 'name': 'Methodology', 'priority': 'high'},
    {'id': 'learning-path-section', 'name': 'Learning Path', 'priority': 'high'},
    {'id': 'explorer-section', 'name': 'Target Audience', 'priority': 'medium'},
    {'id': 'resources-section', 'name': 'Free Resources', 'priority': 'medium'},
    {'id': 'cta-section', 'name': 'Final CTA', 'priority': 'high'}
]

async def test_all_sections_all_devices(page, base_url):
    """
    Comprehensive screenshot test across all sections and devices.
    """
    results = []

    for category, devices in DEVICE_MATRIX.items():
        for device_name, viewport in devices.items():
            for section in SECTIONS_TO_TEST:
                output_path = f"screenshots/{category}/{device_name}/{section['name']}.png"

                try:
                    await capture_section_screenshot(
                        page,
                        f"[data-testid='{section['id']}']",
                        output_path,
                        viewport_width=viewport['width'],
                        viewport_height=viewport['height']
                    )

                    results.append({
                        'section': section['name'],
                        'device': device_name,
                        'status': 'success'
                    })

                except Exception as e:
                    results.append({
                        'section': section['name'],
                        'device': device_name,
                        'status': 'failed',
                        'error': str(e)
                    })

    return results
```

### 13.7 Data Attributes for Test Discovery

**Required attributes for each section:**

```html
<div class="section-isolate"
     data-section-name="hero"          <!-- Human-readable name -->
     data-section-type="hero"          <!-- Section category -->
     data-test-priority="critical">    <!-- Test priority -->

  <div class="hero-wrapper"
       data-testid="hero-section"      <!-- Playwright selector -->
       data-container-type="hero">     <!-- Container query name -->

    <section class="hero"
             data-ux-section="hero"           <!-- UX tracking -->
             data-ux-priority="critical"      <!-- UX priority -->
             data-grid-columns="1"            <!-- Expected layout -->
             data-min-height="500px">         <!-- Minimum height -->
      <!-- Content -->
    </section>
  </div>
</div>
```

**Auto-discovery pattern:**

```python
# Discover all testable sections automatically
sections = await page.locator('[data-testid$="-section"]').all()

for section in sections:
    section_name = await section.get_attribute('data-section-name')
    priority = await section.get_attribute('data-test-priority')

    # Only test high/critical priority
    if priority in ['critical', 'high']:
        await capture_section_screenshot(
            page,
            f'[data-testid="{await section.get_attribute("data-testid")}"]',
            f'screenshots/{section_name}.png'
        )
```

### 13.8 Visual Consistency Rules

**CSS rules to ensure screenshot consistency:**

```css
/* FREEZE ANIMATIONS FOR SCREENSHOTS */
[data-screenshot-mode="true"] * {
  animation-play-state: paused !important;
  transition: none !important;
}

/* CONSISTENT ASPECT RATIOS */
.card-image {
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

.avatar {
  aspect-ratio: 1 / 1;
  object-fit: cover;
}

/* PREVENT CONTENT OVERFLOW */
.section-content {
  overflow: visible; /* Don't clip, let it flow naturally */
  word-wrap: break-word;
  overflow-wrap: break-word;
}

/* CONSISTENT GAPS */
.grid {
  gap: clamp(1.5rem, 3vw, 2rem); /* Never irregular gaps */
}

.stack > * + * {
  margin-block-start: clamp(1rem, 3vh, 2rem); /* Consistent rhythm */
}

/* NO PARTIAL ITEMS IN VIEW */
.scroll-container {
  scroll-snap-type: x mandatory;
  scroll-padding: 2rem;
}

.scroll-container > * {
  scroll-snap-align: start;
}
```

### 13.9 Screenshot Quality Gates

**Automated checks for each screenshot:**

```python
from PIL import Image
import numpy as np

async def validate_screenshot(screenshot_path: str) -> dict:
    """
    Validate screenshot meets quality standards.
    """
    img = Image.open(screenshot_path)
    pixels = np.array(img)

    checks = {
        'has_content': not is_blank(pixels),
        'no_overflow': not has_scrollbar(pixels),
        'proper_padding': check_edge_padding(pixels, min_padding=200),
        'consistent_grid': check_grid_alignment(pixels),
        'readable_text': check_text_contrast(pixels)
    }

    return {
        'path': screenshot_path,
        'passed': all(checks.values()),
        'checks': checks
    }

def is_blank(pixels: np.ndarray) -> bool:
    """Check if screenshot is mostly white/blank."""
    return np.mean(pixels) > 250  # Mostly white

def has_scrollbar(pixels: np.ndarray) -> bool:
    """Detect visible scrollbar (indicates overflow)."""
    # Check right edge for scrollbar pattern
    right_edge = pixels[:, -20:, :]
    return np.std(right_edge) > 10  # Variation indicates scrollbar

def check_edge_padding(pixels: np.ndarray, min_padding: int) -> bool:
    """Verify isolation padding is present."""
    top_padding = pixels[:min_padding, :, :]
    return np.mean(top_padding) > 240  # Mostly empty/white
```

### 13.10 Implementation Checklist

**For each section, ensure:**

- [ ] Wrapped in `.section-isolate` for padding
- [ ] Has `.{section}-wrapper` for container queries
- [ ] Includes `data-testid="{section}-section"` attribute
- [ ] Includes `data-section-name` for discovery
- [ ] Includes `data-test-priority` for filtering
- [ ] Grid uses explicit column count or smart auto-fit
- [ ] Min/max heights constrain to viewport
- [ ] No content overflow (scrollbars)
- [ ] Consistent gaps using design tokens
- [ ] All images have aspect-ratio defined
- [ ] Text contrast meets WCAG standards
- [ ] Animation states are controllable
- [ ] Works on all devices in test matrix

---

### 9.1 CSS Bundle Strategy

**Split CSS by delivery priority:**

```html
<!-- Critical CSS - Inline in <head> -->
<style>
  /* Tokens, reset, above-fold styles */
  /* ~15KB */
</style>

<!-- Main CSS - Async load -->
<link rel="preload" href="main.css" as="style" onload="this.rel='stylesheet'">

<!-- Page-specific CSS - Conditional -->
<link rel="stylesheet" href="homepage.css" media="print" onload="this.media='all'">
```

### 9.2 CSS Optimization Targets

**Performance budget:**
- Critical CSS: < 15KB inline
- Main CSS: < 35KB gzipped
- Page-specific: < 10KB gzipped
- Total CSS: < 50KB gzipped

**Techniques:**
- Use CSS custom properties (no Sass variables)
- Eliminate unused styles
- Scope utility classes
- Minimize specificity
- Use `@layer` for cascade control

### 9.3 Runtime Performance

**Avoid layout thrashing:**

```css
/* BAD - Causes layout recalculation */
.component {
  width: calc(100vw - 20px); /* Recalculates on scroll */
}

/* GOOD - Uses container units */
.component-wrapper {
  container-type: inline-size;
}

.component {
  width: 100cqi; /* No recalculation */
  padding-inline: 1rem;
}
```

---

## Part 10: Success Metrics

### 10.1 Technical Metrics

**CSS Health:**
- Lines of code: Target < 1000 LOC (currently 1990)
- Specificity: Avg < 20 (no `!important`)
- Selector depth: Max 3 levels
- Unused CSS: < 5%

**Performance:**
- First Contentful Paint: < 1.5s
- Largest Contentful Paint: < 2.5s
- Cumulative Layout Shift: 0
- Time to Interactive: < 3.5s

### 10.2 UX Metrics

**Responsiveness:**
- Text readable at all viewport sizes
- No horizontal scroll
- Touch targets ≥ 44px
- Content above fold on all devices

**Accessibility:**
- WCAG 2.1 AA compliance
- Contrast ratios ≥ 4.5:1
- Focus indicators visible
- Screen reader friendly

### 10.3 Developer Experience

**Maintainability:**
- New component development time: < 2 hours
- Bug fix time: < 30 minutes
- Documentation coverage: 100%
- Reusability score: > 80%

---

## Part 11: Fortune 100 Best Practices

### 11.1 Enterprise Patterns

**1. Design Token Versioning**
```css
:root {
  /* Version tokens for backward compatibility */
  --v2-color-primary: #0052cc;
  --v2-space-lg: clamp(2rem, 5vh, 3rem);
}

/* Allow gradual migration */
.legacy-component {
  color: var(--brand-primary); /* Old token */
}

.new-component {
  color: var(--v2-color-primary); /* New token */
}
```

**2. Feature Flags**
```css
/* Enable/disable features via tokens */
:root {
  --enable-container-queries: 1;
  --enable-advanced-grid: 1;
}

@supports (container-type: inline-size) {
  .component {
    display: var(--enable-container-queries, 1) > 0 ? grid : block;
  }
}
```

**3. A/B Testing Support**
```css
/* Data attributes for variant testing */
[data-experiment="variant-a"] .hero {
  background: var(--color-primary);
}

[data-experiment="variant-b"] .hero {
  background: var(--color-accent);
}
```

### 11.2 Team Collaboration

**Documentation Requirements:**
- Every component has Storybook story
- Token changes require RFC (Request for Comments)
- Breaking changes need migration guide
- Performance impact documented

**Code Review Checklist:**
- [ ] Uses design tokens exclusively
- [ ] Container query implementation
- [ ] Cross-browser tested
- [ ] Accessibility audit passed
- [ ] Performance budget met
- [ ] Documentation updated

---

## Part 12: Recommended Tools & Resources

### 12.1 Development Tools

**CSS Architecture:**
- **PostCSS** - Modern CSS processing
- **Lightning CSS** - Fast, modern bundler
- **CSS Modules** - Scoped styles
- **@layer** - Cascade control

**Testing:**
- **Playwright** - Cross-browser testing
- **Chromatic** - Visual regression testing
- **Axe DevTools** - Accessibility testing
- **Lighthouse** - Performance auditing

**Documentation:**
- **Storybook** - Component showcase
- **Styleguidist** - Living style guide
- **Zeroheight** - Design system docs

### 12.2 Learning Resources

**Container Queries:**
- MDN: Container Queries Guide
- Ahmad Shadeed: CSS Container Queries
- Una Kravets: Container Query Solutions

**Fluid Typography:**
- Utopia.fyi - Fluid type calculator
- Modern CSS: Fluid Typography
- Type Scale Calculator

**Design Systems:**
- Design Tokens Community Group
- Brad Frost: Atomic Design
- Nathan Curtis: Design Systems Handbook

---

## Conclusion

### Implementation Priority

**Immediate (Week 1):**
1. ✅ Audit complete (done)
2. Setup token system
3. Implement container query base
4. Create layout primitives

**Short-term (Weeks 2-4):**
1. Migrate hero component
2. Migrate navigation
3. Migrate cards & buttons
4. Test at all breakpoints

**Long-term (Months 2-3):**
1. Complete component migration
2. Build style guide
3. Optimize performance
4. Team training

### Expected Outcomes

**Technical:**
- 50% reduction in CSS size
- Zero layout shifts
- Container-based responsive design
- Token-driven architecture

**Business:**
- Faster feature development
- Consistent brand experience
- Better mobile experience
- Improved conversion rates

**User Experience:**
- Text readable at all sizes
- Content above fold on all devices
- Smooth responsive behavior
- Professional appearance

---

**Next Steps:**
1. Present this strategy to stakeholders
2. Get approval for gradual migration
3. Setup new project structure
4. Begin Phase 1 implementation

**Questions for Review:**
- Approval for container query baseline?
- Timeline for full migration?
- Resource allocation for testing?
- Training plan for team?
