# Visual UX Review System: Research & Strategy

**Date**: October 28, 2025 **Objective**: Make the visual UX review system
bulletproof, reliable, and extensible

---

## 1. CURRENT STATE ANALYSIS

### What's Working ✅

- **Screenshot capture**: Successfully captures 3 viewports
  (desktop/tablet/mobile)
- **GPT-4o Vision integration**: Working with Responses API
- **Persona-based analysis**: 2 personas providing structured feedback
- **Cost tracking**: ~$0.08 per full run (6 analyses)
- **Structured output**: Pydantic models ensure consistent results

### Pain Points 🔴

1. **Port conflicts**: Docker containers + dev servers compete for ports
   8080-8082
2. **CSS/JS 404 errors**: Path prefix mismatch between server setups
3. **Full-page only**: Currently captures entire viewport, not page sections
4. **Single-page limitation**: No support for analyzing multiple pages
5. **Manual server management**: Requires manually starting HTTP server
6. **No reliability safeguards**: No retry logic, connection validation, or
   error recovery

---

## 2. TECHNICAL RESEARCH FINDINGS

### GPT-4o Vision Best Practices

**Token Costs (from OpenAI docs):**

- **Detail level matters**:
  - `low`: 85 tokens (512x512 image)
  - `high`: 170 tokens per 512px tile + 85 base
- **Our screenshots**:
  - Desktop (1920x1080): ~765 tokens with high detail
  - Tablet (768x1024): ~425 tokens with high detail
  - Mobile (375x667): ~255 tokens with high detail

**Limitations to consider**:

- Max 50MB payload per request
- Max 500 images per request
- Struggles with small text (need to capture at 2x scale factor - already doing
  this ✅)
- May give approximate counts
- Best for high-level UX, not pixel-perfect design audits

### Section-Based Analysis Approaches

**Option 1: Element-based screenshots** (RECOMMENDED)

```javascript
// Use Playwright locators to screenshot specific elements
await page.locator('header').screenshot();
await page.locator('main').screenshot();
await page.locator('footer').screenshot();
```

- ✅ Precise section isolation
- ✅ Better focus for LLM analysis
- ✅ Lower token costs (smaller images)
- ❌ Requires HTML structure knowledge

**Option 2: Scroll and crop**

```javascript
// Full page screenshot, then crop in post-processing
await page.screenshot({ fullPage: true });
// Crop: hero (0-800px), content (800-2000px), footer (2000-end)
```

- ✅ Works without HTML knowledge
- ✅ Captures fold-specific issues
- ❌ Higher token costs
- ❌ More complex processing

**Option 3: Viewport scrolling** (HYBRID - BEST)

```javascript
// Capture multiple viewport-sized chunks
await page.evaluate(() => window.scrollTo(0, 0));
await page.screenshot(); // above-fold
await page.evaluate(() => window.scrollTo(0, 800));
await page.screenshot(); // mid-page
```

- ✅ Simulates real user scrolling
- ✅ Catches fold-specific issues
- ✅ Manageable token costs
- ✅ No HTML structure dependency

---

## 3. RECOMMENDED ARCHITECTURE

### Phase 1: Reliability & Infrastructure (IMMEDIATE)

#### A. Port Management System

```python
# qa_agents/server_manager.py
class ServerManager:
    """Manages dev server lifecycle"""

    def find_available_port(self, start=8080, end=8090):
        """Find first available port in range"""

    def start_server(self, directory, port):
        """Start HTTP server, kill conflicts"""

    def stop_server(self, port):
        """Clean shutdown of server"""

    def health_check(self, url, timeout=5):
        """Verify server is responding"""
```

**Benefits**:

- ✅ Auto-find available ports
- ✅ Kill conflicting Docker containers if needed
- ✅ Validate server before screenshots
- ✅ Clean shutdown after analysis

#### B. Retry & Error Recovery

```python
# qa_agents/reliability.py
@retry(max_attempts=3, backoff=2.0)
async def capture_with_retry(url, viewport):
    """Capture screenshot with exponential backoff"""

async def validate_screenshot(screenshot_data):
    """Ensure screenshot isn't blank/corrupt"""

def handle_partial_failure(results):
    """Continue with successful analyses if some fail"""
```

**Benefits**:

- ✅ Resilient to network hiccups
- ✅ Detects blank/corrupted screenshots
- ✅ Graceful degradation

#### C. Configuration Management

```python
# qa_agents/config.py additions
class VisualUXConfig:
    SERVER_PORT_RANGE = (8080, 8090)
    SCREENSHOT_TIMEOUT = 30
    RETRY_ATTEMPTS = 3
    VIEWPORT_PROFILES = {...}
    PAGE_DEFINITIONS = {...}  # New: multi-page support
```

---

### Phase 2: Section-Based Analysis (HIGH PRIORITY)

#### Strategy: Hybrid Viewport Scrolling

**Implementation**:

```python
# qa_agents/screenshot_utils.py additions
async def capture_page_sections(
    url: str,
    viewport_name: str = "desktop",
    sections: list[str] = None  # ["above-fold", "mid-page", "footer"]
) -> dict[str, dict]:
    """
    Capture multiple sections of a page

    Sections defined as:
    - above-fold: First viewport height (0-1080px for desktop)
    - mid-page: Second viewport height (1080-2160px)
    - footer: Last viewport height
    """
    viewport = VIEWPORTS[viewport_name]
    screenshots = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport=viewport)
        await page.goto(url, wait_until="networkidle")

        # Get page height
        page_height = await page.evaluate("document.body.scrollHeight")
        viewport_height = viewport["height"]

        # Calculate scroll positions
        scroll_positions = calculate_scroll_positions(
            page_height,
            viewport_height,
            sections
        )

        for section_name, scroll_y in scroll_positions.items():
            await page.evaluate(f"window.scrollTo(0, {scroll_y})")
            await page.wait_for_timeout(500)  # Let animations settle

            screenshot_bytes = await page.screenshot()
            screenshots[section_name] = {
                "base64": base64.b64encode(screenshot_bytes).decode(),
                "viewport": viewport_name,
                "section": section_name,
                "scroll_position": scroll_y
            }

        await browser.close()

    return screenshots
```

**Updated Agent Prompt**:

```python
# qa_agents/visual_ux_agents.py
def get_section_prompt(section_name: str) -> str:
    prompts = {
        "above-fold": """
            Analyze the ABOVE-THE-FOLD section (first thing users see).
            Focus on:
            - First impressions (3-5 second rule)
            - Clear value proposition
            - Primary CTA visibility
            - Hero section effectiveness
        """,
        "mid-page": """
            Analyze the MID-PAGE content section.
            Focus on:
            - Content hierarchy and readability
            - Visual breaks and whitespace
            - Section transitions
            - Engagement elements
        """,
        "footer": """
            Analyze the FOOTER section.
            Focus on:
            - Essential links accessibility
            - Contact information visibility
            - Social proof elements
            - Legal/compliance info
        """
    }
    return prompts.get(section_name, "Analyze this section...")
```

**Cost Impact**:

- Before: 1 screenshot per viewport = ~765 tokens (desktop high detail)
- After: 3 sections per viewport = ~255 tokens each = ~765 tokens total
- **No cost increase**, but MORE detailed feedback per section!

---

### Phase 3: Multi-Page Support (MEDIUM PRIORITY)

#### Page Configuration System

```python
# qa_agents/page_config.yaml
pages:
  home:
    url: "/"
    priority: high
    sections: ["above-fold", "mid-page", "footer"]
    personas: ["first_year_student", "instructor"]

  lessons:
    url: "/lessons/"
    priority: medium
    sections: ["above-fold", "mid-page"]
    personas: ["first_year_student"]

  resources:
    url: "/resources/"
    priority: medium
    sections: ["above-fold"]
    personas: ["first_year_student"]
```

#### Orchestrator

```python
# qa_agents/multi_page_review.py
class MultiPageReviewer:
    """Orchestrate reviews across multiple pages"""

    def __init__(self, config_path: str):
        self.pages = load_page_config(config_path)

    async def review_all_pages(
        self,
        base_url: str,
        filter_priority: str = None
    ) -> dict:
        """
        Review all configured pages

        Returns:
        {
            "home": {
                "above-fold": [...reviews...],
                "mid-page": [...reviews...],
                "footer": [...reviews...]
            },
            "lessons": {...},
            "cost": 0.45,
            "summary": {...}
        }
        """

    def generate_report(self, results: dict) -> str:
        """Generate HTML/Markdown report with all findings"""
```

**Execution Strategies**:

1. **Full Site Audit** (expensive, thorough)

   ```bash
   python qa_agents/multi_page_review.py --mode=full
   # Reviews all pages, all sections, all personas
   # Cost: ~$2-5 depending on site size
   ```

2. **Smart Sampling** (balanced)

   ```bash
   python qa_agents/multi_page_review.py --mode=smart
   # Reviews high-priority pages fully
   # Samples other pages (desktop + student persona only)
   # Cost: ~$0.50-1.00
   ```

3. **Critical Path** (fast, cheap)
   ```bash
   python qa_agents/multi_page_review.py --mode=critical
   # Reviews only: home (above-fold), lessons (above-fold)
   # Cost: ~$0.15
   ```

---

### Phase 4: Advanced Features (FUTURE)

#### A. Visual Regression Testing

```python
# Compare screenshots over time
def detect_visual_changes(before_screenshot, after_screenshot):
    """Use perceptual hashing to detect changes"""
    # Trigger UX review only if >10% visual difference
```

#### B. A/B Testing Support

```python
# Compare two variants
async def compare_variants(url_a, url_b, viewport="desktop"):
    """Analyze both, provide comparative feedback"""
```

#### C. Accessibility Deep Dive

```python
# New persona: accessibility_expert
# Focus: WCAG 2.1 AA compliance, contrast ratios, keyboard nav
```

#### D. Performance Integration

```python
# Combine with Lighthouse
def analyze_ux_and_performance(url):
    """Correlate visual UX with Core Web Vitals"""
```

---

## 4. IMPLEMENTATION PLAN

### Week 1: Bulletproofing (Priority 1)

- [ ] Implement `ServerManager` class
  - Port detection
  - Docker container management
  - Health checks
- [ ] Add retry logic to screenshot capture
- [ ] Add screenshot validation (not blank/corrupt)
- [ ] Update error messages with troubleshooting steps
- [ ] Add `--dry-run` mode for testing without API calls

**Deliverable**: System that "just works" regardless of port conflicts

### Week 2: Section Analysis (Priority 2)

- [ ] Implement `capture_page_sections()` function
- [ ] Add section-specific prompts to agents
- [ ] Update output formatting for sectioned results
- [ ] Test on home page with 3 sections
- [ ] Document section definitions

**Deliverable**: Detailed section-by-section UX analysis

### Week 3: Multi-Page Support (Priority 3)

- [ ] Create `page_config.yaml` structure
- [ ] Implement `MultiPageReviewer` class
- [ ] Add report generation (HTML + Markdown)
- [ ] Create CLI with `--mode` flag
- [ ] Add progress bar for long runs

**Deliverable**: Full-site UX audit capability

### Week 4: Polish & Documentation (Priority 4)

- [ ] Create comprehensive README with examples
- [ ] Add `--help` documentation
- [ ] Create video walkthrough
- [ ] Add cost estimation before running
- [ ] Implement caching for repeated analyses

---

## 5. IMMEDIATE NEXT STEPS

### Quick Wins (Can implement in 1-2 hours):

1. **Kill port conflicts automatically**

```python
def kill_port(port):
    os.system(f"lsof -ti:{port} | xargs kill -9")
```

2. **Add connection validation**

```python
def wait_for_server(url, timeout=10):
    for i in range(timeout):
        try:
            requests.get(url, timeout=1)
            return True
        except:
            time.sleep(1)
    return False
```

3. **Better error messages**

```python
except ConnectionError as e:
    print(f"""
    ❌ Cannot connect to {url}

    Troubleshooting:
    1. Is the server running?
       → Run: cd _site && python3 -m http.server 8082

    2. Check for port conflicts:
       → Run: lsof -i :8082

    3. Kill conflicting processes:
       → Run: lsof -ti:8082 | xargs kill -9
    """)
```

---

## 6. COST ANALYSIS

### Current System

- 6 analyses (3 viewports × 2 personas)
- Full-page screenshots
- **Cost**: ~$0.08 per run

### With Section Analysis (3 sections)

- 18 analyses (3 viewports × 3 sections × 2 personas)
- Smaller images per section
- **Cost**: ~$0.20 per page
- **Benefit**: 3x more detailed feedback

### With Multi-Page (5 pages)

- Full audit: 5 pages × $0.20 = **$1.00**
- Smart audit: Home ($0.20) + Others sampled ($0.30) = **$0.50**
- Critical audit: 2 pages above-fold only = **$0.10**

**Budget recommendations**:

- Daily: Run critical path ($0.10/day = $3/month)
- Pre-deploy: Run smart audit ($0.50/deploy)
- Monthly: Run full audit ($1.00/month)

---

## 7. EXTENSIBILITY ARCHITECTURE

### Plugin System

```python
# qa_agents/plugins/
# ├── personas/
# │   ├── first_year_student.py
# │   ├── instructor.py
# │   └── accessibility_expert.py  ← Add new personas
# ├── analyzers/
# │   ├── ux_analyzer.py
# │   ├── performance_analyzer.py  ← Add performance analysis
# │   └── accessibility_analyzer.py
# └── reporters/
#     ├── markdown_reporter.py
#     └── html_reporter.py  ← Add custom report formats
```

### Configuration Inheritance

```yaml
# qa_agents/presets/
# ├── quick.yaml      # Fast, cheap, critical path only
# ├── balanced.yaml   # Good coverage, reasonable cost
# └── thorough.yaml   # Everything, expensive
```

---

## 8. SUCCESS METRICS

### Reliability

- [ ] 99%+ success rate on screenshot capture
- [ ] <5 seconds to detect and fix port conflicts
- [ ] Zero manual intervention required

### Usefulness

- [ ] Identify 10+ actionable UX issues per analysis
- [ ] Reduce false positives to <10%
- [ ] Feedback specific enough to implement directly

### Scalability

- [ ] Analyze 5+ pages in <2 minutes
- [ ] Support 20+ pages without manual config
- [ ] Handle 10+ concurrent analyses

---

## RECOMMENDATION SUMMARY

**Implement in this order:**

1. **TODAY**: Server management + reliability (2-3 hours)
   - Auto port detection
   - Connection validation
   - Better error messages

2. **THIS WEEK**: Section-based analysis (4-6 hours)
   - Above-fold/mid-page/footer capture
   - Section-specific prompts
   - Updated output formatting

3. **NEXT WEEK**: Multi-page support (6-8 hours)
   - Page configuration system
   - Batch orchestration
   - Report generation

4. **FUTURE**: Advanced features (ongoing)
   - Visual regression
   - A/B testing
   - Performance correlation

**Why this order?**

- Reliability issues are blocking current usage → fix first
- Section analysis provides immediate value without new infrastructure
- Multi-page needs reliable foundation → do after #1
- Advanced features are "nice to have" → defer until core is solid

---

**Next**: Shall I implement Phase 1 (Reliability) now?
