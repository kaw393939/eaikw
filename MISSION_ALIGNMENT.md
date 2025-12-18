# Mission Alignment Framework

## Core Mission

**Turn students into career-ready AI professionals with a guided, automated onboarding experience.**

This document explains how every component of Job Club aligns with and supports this mission.

---

## Phase 1: Guided Experience Foundation

### Pages & Content

**Onboarding Page** → Entry Point to Career Pipeline
- Collects career goals and professional asset URLs
- Initiates the guided journey toward career readiness
- Required fields: name, email, major, graduation year, career goal
- Profile assets: LinkedIn, GitHub, portfolio, Calendly

**Events Page** → Career Development Pathway
- Workshops build essential skills
- Office hours provide mentoring
- Networking events develop professional networks
- Hack nights demonstrate AI capabilities
- All events structured to move students toward career readiness

**Resources Page** → Professional Portfolio Building
- LinkedIn optimization for AI careers
- GitHub profile setup for showcasing AI projects
- Personal portfolio site creation
- Interview preparation for AI roles
- Resume optimization for technical roles
- All resources guide students to "career-ready" professional presence

**About Page** → Mission Communication
- Clearly states: "Turn students into career-ready AI professionals"
- Explains guided pipeline structure
- Defines what "career-ready" means for AI professionals
- Builds trust through team transparency

### Site Configuration (`site.json`)
- **Tagline:** "Turn Students Into Career-Ready AI Professionals"
- **Mission:** Describes the guided, automated pipeline
- **Value Props:** All six focus on career readiness
  1. Structured career pipeline (guidance)
  2. Discord community & mentoring (guidance)
  3. Professional portfolio guidance (career readiness)
  4. Events & workshops (career readiness)
  5. AI career resources (career readiness)
  6. CRM & automation (automation)

---

## Phase 2: Automated Career Pipeline

### Sanity CMS Schemas

**memberProfile** → Individual Career Journey Tracking
- Purpose: Track each student's progress toward career readiness
- Key fields track career readiness status:
  - `careerGoal`: What they want to become
  - `onboardingStatus`: Progress (new → in-progress → completed)
  - `missingAssets`: Gaps in their professional portfolio
  - `linkedinUrl`, `githubUrl`, `portfolioUrl`, `calendlyUrl`: Career-ready asset checklist
- Connects students to: Notion DB for tracking, Discord for community

**event** → Career Development Milestones
- Purpose: Guide students through career skill development
- Event types align with career stages:
  - **workshop**: Skill development
  - **office-hours**: One-on-one mentoring
  - **networking**: Professional relationship building
  - **hack-night**: Portfolio building
  - **speaker**: Industry insights
  - **meetup**: Community connection
- Links to speakers who model career-ready professionals

**resource** → Career Asset Building Guides
- Purpose: Teach how to build the portfolio assets that make you career-ready
- Categories directly support career readiness:
  - **linkedin**: Professional branding
  - **github**: Technical portfolio
  - **portfolio**: Showcase work
  - **consulting**: AI consultant pathway
  - **startup**: Founder pathway
  - **interviews**: Getting the job
  - **resume**: Getting past screening
  - **networking**: Building opportunities

**jobclubSpeaker** → Career Models
- Purpose: Connect students with career-ready professionals they can learn from
- Field: `title` and `company` show real career examples
- Links to mentor relationships

### Integration Services

**Notion DB Sync** → Progress Tracking & Accountability
- Automated sync of memberProfile → Notion
- Purpose: Keep students' progress visible and trackable
- Notion database fields align with "career readiness checklist":
  - Major and graduation year (timeline awareness)
  - Career goal (destination clarity)
  - LinkedIn, GitHub, Portfolio, Calendly (asset checklist)
  - Status (progress tracking)
  - Notes (mentor guidance)
- Supports the "guided" aspect: transparent progress tracking

**Discord Integration** → Mentoring Community
- Welcome messages reinforce career goal clarity
- Introduction posts introduce students to mentors and peers
- Career goal emoji make aspirations visible and supported
- Channels organized by career path
- Supports the "guided" aspect: peer and mentor support

### API Endpoints

**POST /api/onboarding** → Career Pipeline Enrollment
- Validates that all required career readiness elements are collected
- Creates memberProfile in Sanity
- Syncs to Notion (career tracking)
- Posts to Discord (community welcome)
- Entire flow is automated and guided

**GET /api/events** → Accessible Career Development
- Returns published, upcoming events
- All events are milestones on the career pipeline
- Supports discoverability of career development opportunities

**GET /api/resources** → On-Demand Career Guidance
- Returns career-building resources by category
- Students can access guidance whenever they need it
- Categories match the career readiness checklist

**POST /api/event-registration** → Commitment to Career Path
- Records that students are actively participating in career development
- Enables follow-up and progress tracking

---

## How Each Component Serves the Mission

### Guided Experience

| Component | How It Guides | Evidence |
|-----------|---------------|----------|
| Onboarding form | Clarifies career goal | Required `careerGoal` field |
| Career path questions | Narrows focus | 6 specific AI career options |
| Resource guides | Step-by-step instruction | Organized by career asset |
| Events progression | Structured skill building | Workshop → Office hours → Networking |
| Mentor community | Live guidance | Discord integration with speakers |
| Progress tracking | Visibility into next steps | Notion DB tracking missing assets |

### Automated Experience

| Component | What It Automates | Evidence |
|-----------|-------------------|----------|
| Form submission | Enrollment into all systems | Single form creates Sanity doc + Notion record + Discord post |
| Sanity CMS | Content delivery | Guides automatically served based on career goal |
| Notion sync | Progress tracking | Real-time sync of achievements and gaps |
| Discord posts | Community introduction | Automatic welcome and intro posts |
| Asset checklist | Progress visibility | missingAssets array highlights gaps |
| Email follow-up | Personalized guidance (Phase 3) | Zapier automation sends customized next steps |

### Career-Ready Focus

| Component | How It Measures Readiness | Success Metrics |
|-----------|---------------------------|-----------------|
| memberProfile | Onboarding status progression | new → in-progress → completed |
| missingAssets | Portfolio completeness | LinkedIn ✓ GitHub ✓ Portfolio ✓ Calendly ✓ |
| Career goal options | Clear career path | Selected one of 6 AI careers |
| Event types | Skill acquisition | Attended workshops, office hours, networking |
| Resources | Knowledge gained | Completed guides on essential topics |
| Speaker connections | Mentor relationships | Introduced to career-ready professionals |

---

## Phase 3 Alignment (Planned)

### Email Integration (Phase 3A)
- **Mission support:** Personalized guidance emails keep students on track
- **Automation:** Zapier sends career-stage-appropriate content
- **Example:** "You've completed onboarding. Here's your Week 1 career readiness checklist"

### Analytics (Phase 3B)
- **Mission support:** Measure career readiness progress across cohorts
- **Tracking:** Form completion rates, event attendance, resource engagement
- **Goal:** Identify students needing additional support

### GDPR Compliance (Phase 3C)
- **Mission support:** Build trust with transparent data practices
- **Features:** Data export, deletion, consent tracking
- **Goal:** Ethical, trustworthy career acceleration

### Advanced Features (Phase 3D-E)
- Member onboarding checklist → Track specific career readiness milestones
- Mentor matching → Connect students with career mentors
- AI-powered recommendations → Suggest resources based on career path
- Career dashboard → Visual progress toward goal
- Community leaderboard → Celebrate career achievements

---

## Mission Verification Checklist

**For Each Feature, Ask:**
- [ ] Does this guide students toward a career goal?
- [ ] Does this automate the onboarding process?
- [ ] Does this help measure career readiness?
- [ ] Does this connect students to mentoring or community?
- [ ] Does this build a professional portfolio asset?

**Example: LinkedIn Resource Guide**
- ✅ Guides students to optimize LinkedIn (career goal clarity)
- ✅ Automates the learning (self-serve guide + email prompt)
- ✅ Measures readiness (LinkedIn URL in memberProfile)
- ✅ Connects to community (Discord announcement)
- ✅ Builds portfolio asset (LinkedIn is a career asset)

**Example: Events Page**
- ✅ Guides students through skill progression (workshop → networking → roles)
- ✅ Automates discovery (all events listed, registered via API)
- ✅ Measures readiness (attendance tracked in Notion)
- ✅ Connects to community (live mentoring and networking)
- ✅ Builds relationships (speaker connections, peer network)

---

## Key Principles for Maintaining Mission Alignment

1. **Every feature should answer:** "How does this make students more career-ready?"
2. **Every page should include:** Clear guidance toward the goal
3. **Every integration should:** Track progress or automate a step
4. **Every communication should:** Reinforce the career path
5. **Every resource should:** Build a career asset or skill

---

## Glossary: What "Career-Ready AI Professional" Means

Based on Job Club structure, a career-ready AI professional has:

1. **Clarity of Direction**
   - Chosen a specific AI career path (consultant, startup founder, engineer, product manager, data scientist)
   - Understands what that role requires

2. **Essential Portfolio Assets**
   - Professional LinkedIn profile
   - GitHub account with AI projects
   - Personal portfolio site showcasing work
   - Calendly link for professional scheduling

3. **Professional Skills**
   - Can discuss AI fundamentals in interviews
   - Knows how to optimize for ATS and hiring
   - Can network effectively with professionals
   - Has conducted mock interviews

4. **Active Learning**
   - Engaged with Job Club community and mentors
   - Attending relevant events and workshops
   - Building projects that demonstrate AI capabilities

5. **Accountability & Progress**
   - Tracking progress toward career goals
   - Checking off career readiness milestones
   - Actively seeking mentoring and feedback

---

## Mission Success Outcomes

By the end of Job Club, students should be able to:

- [ ] Articulate their AI career goal confidently
- [ ] Point to professional portfolio assets that showcase readiness
- [ ] Describe how their background aligns with their chosen career path
- [ ] Reference mentors or community members they've learned from
- [ ] Identify next steps toward that career goal
- [ ] Connect with others pursuing similar paths

**The automated onboarding experience removes barriers and provides guidance every step of the way.**
