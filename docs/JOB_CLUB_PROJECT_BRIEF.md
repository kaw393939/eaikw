# Job Club - Project Brief
## S373 – Project Brief
### Job Club – AI Career Accelerator
#### Two-Week Production Sprint

---

## 1. Project Overview

Job Club is a student-focused AI career accelerator designed to help NJIT students become:

- AI consultants
- AI startup founders
- AI-savvy developers
- Portfolio-ready job candidates

Your team will build a production-ready Job Club site that:

- Onboards students into a structured career pipeline
- Connects them to Discord, events, mentoring, and learning resources
- Guides them to set up essential professional assets (LinkedIn, GitHub, personal site, Calendly, etc.)
- Automates administrative workflows
- Tracks users in a CRM
- Meets accessibility, SEO, analytics, and GDPR standards

The best implementation may become the official NJIT Job Club site.

---

## 2. Mission of the Site

**Turn students into career-ready AI professionals with a guided, automated onboarding experience.**

The site must:

- Provide a professional onboarding flow
- Offer events, workshops, and resource guides
- Include CRM + Discord integration
- Automate communications and onboarding steps
- Provide clear guidance for building modern professional portfolios
- Operate with real professional-grade UX and technical standards

---

## 3. Functional Requirements

Your team must deliver all of the following functionality:

### A. Student Onboarding Workflow (Core Feature)

This is the heart of the Job Club site.

#### Onboarding Form (Front-end)

Collect the following:

- Name
- Email
- Major / Graduation year
- LinkedIn URL
- GitHub URL
- Personal portfolio site (reference example: https://kaw393939.github.io/117_final_fall_2025/portfolio/)
- Calendly link
- Career goal (consultant, startup founder, SWE, product manager, data scientist, etc.)

#### Sanity CMS Storage (Back-end)

Save onboarding submissions as `memberProfile` documents with fields:

- Personal info
- Career goal
- URLs provided
- Onboarding status (new, in-progress, completed)
- Timestamp
- Flags for missing prerequisites (LinkedIn/GitHub/Site/Calendly)

#### Automated Personalized Checklist

After submission:

- System identifies missing professional assets
- Sends a personalized onboarding email with:
  - Tasks they still need to complete
  - Relevant guides or templates
- Email must be sent via automation (Zapier/Make)

#### Discord Integration

Upon submission:

- Add to CRM
- Post an intro message to a #jobclub-intros channel on Discord
- (Optional) Assign a Discord @Member role

### B. Events System

#### Events Listing Page

Shows all upcoming events stored in Sanity:

- Workshops
- Office hours
- Meetups
- Guest speakers
- Hack nights

#### Event Details Page

Contains:

- Title
- Description
- Date/time
- Location/Zoom link
- "Add to calendar" button

#### Event Management in Sanity

Schemas:

- `event`
- `speaker` (optional)

#### Analytics Integration

Track:

- Page views
- Event clicks
- Registrations

Analytics must be GDPR-compliant (see below).

### C. Resource Library

Job Club must include a curated library of student-friendly AI career tools.

**Minimum:**
At least 2 written guides (stored as Sanity resource docs)

**Recommended examples:**

- "How to Optimize Your LinkedIn for AI Jobs"
- "AI Consulting Portfolio Starter Guide"
- "How to Build a GitHub Profile That Gets You Interviews"
- "How to Set Up Calendly + Zapier for Client Meetings"

Resources must be:

- Well formatted
- Accessible
- Optimized for SEO
- AI-assisted but human-reviewed

### D. Professional Portfolio Guidance

The site must reference or embed:

- A model student portfolio like the sample: https://kaw393939.github.io/117_final_fall_2025/portfolio/

Job Club must provide:

- Guidance on building a personal brand
- A recommended portfolio checklist
- Templates or examples

This is core to the mission.

---

## 4. Technical Requirements

### A. EAiKW Reference Architecture Requirement

You MUST clone and harvest:

https://github.com/kaw393939/eaikw

In `/reference/`, include:

- Eleventy config analysis
- CSS architecture
- Accessibility strategy
- SEO best practices
- Layout patterns

AI-generated `harvest-notes.md` must document the extraction of reusable ideas.

All 3 Job Club pages (home, onboarding, events) must use the EAiKW style and layout patterns, adapted to Job Club branding.

### B. Sanity CMS Requirements

You must implement and connect:

**Schemas:**
- `memberProfile`
- `event`
- `resource`
- `author` (for resource documents)

**CMS Features:**
- Draft → review → publish workflow
- Webhook or API integration
- Ability to list content on the site dynamically
- Ability to store onboarding submissions

### C. Automation Requirements

Your team must build at least two automations using Zapier or Make.

**Required Automation:**

Onboarding Form → CRM + Personalized Email
- Sends personalized onboarding checklist
- Creates/updates CRM entry
- Posts intro to Discord

**Second Automation (choose one):**

- Event created → Announcement to Discord
- Event registration → Add to CRM
- Event registration → Add to Google Calendar
- Resource published → Post to Discord
- MemberProfile updated → Slack/Discord mentor notification

### D. Required Integrations

#### 1. Discord

Dedicated Job Club channels:

- #jobclub-intros
- #events
- #resources

Automation posting required
Optional: role assignment

#### 2. CRM

You must integrate HubSpot, Airtable, or Notion DB to manage:

- Members
- Registration
- Events
- Mentorship pipelines

Sample fields:

- Name
- Email
- Major
- URLs
- Member status
- Mentorship interest

### E. GDPR + Privacy Compliance

All Job Club pages must include:

- GDPR-compliant cookie banner (Accept / Reject / Preferences)
- Analytics scripts only run after consent
- Privacy Policy page describing:
  - What data is collected
  - Use of Zapier/CRM integrations
  - Data storage + deletion policy
  - Cookies + analytics
- Accessible forms & ARIA labeling
- Screen-reader accessible navigation

### F. Web Analytics Requirement

Teams must evaluate at least two analytics options:

- Google Analytics 4
- Plausible
- Fathom
- Matomo
- Cloudflare Web Analytics
- Umami

Deliver:
- `docs/analytics-evaluation.md`

Implement one analytics tool with:

- GDPR consent mode
- Tracking for:
  - Page views
  - Onboarding form views
  - Event clicks

### G. CI/CD Requirements

Your repo must include:

- Linting (JS, CSS, Markdown, formatting)
- Eleventy build test
- Playwright tests
  - Homepage loads
  - Onboarding form works
- Lighthouse CI
  - Performance
  - Accessibility
  - Best Practices
  - SEO
  - Bundle size limits (CSS < ~10KB gzipped recommended)
- GitHub Pages deployment
- No failing CI jobs

---

## 5. UX & Discovery Requirements

### A. Discovery Deliverables

Delivered in `/docs/discovery/`:

- **Personas** (min. 3)
  - Example personas:
    - "AI-curious freshman"
    - "Career-switching senior"
    - "Entrepreneurial student building a startup"
- **Customer journey map**
  - E.g., "Student wants to join Job Club → becomes career-ready"
- **Problem statement & goals**
- **Competitor/comparable analysis**
  - E.g., Replit community, Major League Hacking, university career centers

### B. UX Deliverables

Delivered in `/docs/ux/`:

- **Sitemap & information architecture**
- **Wireframes for:**
  - Homepage
  - Onboarding flow
  - Events page
  - Resource library
- **Brand guide:**
  - Logo
  - Colors
  - Typography
  - Voice & tone
  - Component and button styles

---

## 6. AI Usage Requirement

Teams must maintain a log in:
`docs/ai-usage.md`

Include:

- AI-generated wireframes
- Prompts used for code generation
- AI assistance for Sanity schemas
- AI-assisted QA
- AI-generated forms, content, and checklists

---

## 7. QA Requirements

Delivered in `docs/qa-report.md`:

- Lighthouse scores (screenshots)
- CI test evidence
- Bundle size report
- Results of Playwright tests
- Manual accessibility notes
- Verification of cookie banner

---

## Summary Checklist

- [ ] Onboarding workflow (form, Sanity storage, checklist, Discord integration)
- [ ] Events system (listing, details, management, analytics)
- [ ] Resource library (min. 2 guides, accessible, SEO-optimized)
- [ ] Portfolio guidance (model example, checklist, templates)
- [ ] EAiKW architecture harvested and documented
- [ ] Sanity CMS configured with required schemas
- [ ] At least 2 automations implemented (Zapier/Make)
- [ ] Discord integration working
- [ ] CRM integration (HubSpot/Airtable/Notion)
- [ ] GDPR + Privacy compliance
- [ ] Analytics evaluation + implementation
- [ ] CI/CD pipeline complete
- [ ] Discovery documentation (personas, journey maps, problem statement)
- [ ] UX documentation (wireframes, brand guide, sitemap)
- [ ] AI usage log
- [ ] QA report with evidence
