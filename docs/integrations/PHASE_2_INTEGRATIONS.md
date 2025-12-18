# Phase 2: Integrations Documentation

Complete guide for setting up and managing Job Club's backend integrations with Sanity CMS, Notion DB, and Discord.

## Overview

Phase 2 connects the Job Club front-end forms to three backend services:

1. **Sanity CMS** - Content management and member data storage
2. **Notion DB** - Member tracking and progress management
3. **Discord** - Community engagement and notifications

## Architecture

```
Onboarding Form (front-end)
    ↓
API Endpoint (/api/onboarding)
    ↓
Sanity CMS (create memberProfile doc)
    ↓
Notion DB (sync member record)
    ↓
Discord (post welcome & intro)
    ↓
Confirmation email (future: Zapier)
```

## Sanity CMS Setup

### 1. Environment Variables

Add to `.env.local`:

```bash
# Sanity
SANITY_PROJECT_ID=your_project_id
SANITY_DATASET=production
SANITY_WRITE_TOKEN=your_write_token  # Must have write permissions
```

### 2. Schema Configuration

The following schemas are already created in `production/schemaTypes/`:

- **memberProfile.js** - Student member data and onboarding status
- **event.js** - Workshop, office hours, networking events
- **jobclubSpeaker.js** - Event speakers and mentors
- **resource.js** - Career guides and resource library

### 3. Studio Deployment

```bash
cd production
npm install
npm run dev
```

Access Sanity Studio at `http://localhost:3333`

### 4. Document Type Reference

#### memberProfile
Stores all student information collected during onboarding.

**Fields:**
- `name` (string, required) - Student full name
- `email` (string, required) - NJIT email
- `major` (string, required) - Academic major
- `graduationYear` (number) - Expected graduation year
- `careerGoal` (select) - One of: AI Consultant, AI Startup Founder, AI Engineer, Data Scientist, Product Manager, Other
- `linkedinUrl` (url) - LinkedIn profile link
- `githubUrl` (url) - GitHub profile link
- `portfolioUrl` (url) - Portfolio website
- `calendlyUrl` (url) - Calendly scheduling link
- `onboardingStatus` (select) - new, in-progress, completed
- `missingAssets` (array) - LinkedIn, GitHub, Portfolio, Calendly, etc.
- `discordUsername` (string) - Discord handle (optional)
- `joinedDate` (datetime) - Automatically set when created
- `lastUpdated` (datetime) - Updated when modified
- `notes` (text) - Mentor notes

**Example Query:**
```groq
*[_type == "memberProfile" && onboardingStatus == "new"] | order(joinedDate desc)
```

#### event
Manage workshops, office hours, and networking events.

**Fields:**
- `title` (string, required) - Event name
- `description` (text) - Full event description
- `eventType` (select) - workshop, office-hours, networking, hack-night, speaker, meetup
- `date` (datetime) - Event start time
- `endTime` (datetime) - Event end time
- `location` (string) - Physical or virtual location
- `zoomLink` (url) - Zoom meeting URL (if virtual)
- `capacity` (number) - Max attendees
- `speakers` (array) - References to speaker documents
- `registrationLink` (url) - Link to registration form
- `tags` (array) - Topics covered
- `status` (select) - draft, published, cancelled
- `publishedAt` (datetime) - Publication date

**Example Query:**
```groq
*[_type == "event" && status == "published" && dateTime(date) >= dateTime(now())] | order(date asc)
```

#### resource
Career guides, templates, and educational materials.

**Fields:**
- `title` (string, required) - Resource name
- `slug` (string, auto) - URL-friendly identifier
- `description` (string, max 160) - Short description
- `category` (select) - linkedin, github, portfolio, consulting, startup, interviews, resume, networking
- `blockContent` (array) - Rich text content
- `author` (reference) - Author document reference
- `coverImage` (image) - Featured image
- `publishedAt` (datetime) - Publication date
- `updatedAt` (datetime) - Last update date
- `tags` (array) - Search keywords
- `difficulty` (select) - Beginner, Intermediate, Advanced
- `timeToRead` (number) - Estimated read time in minutes

## Notion DB Integration

### 1. Setup Notion Database

#### Create Database
1. Open [Notion](https://notion.so)
2. Create new database: "Job Club Members"
3. Copy the database ID from the URL: `notion.so/[workspace]/[databaseId]`

#### Configure Properties
Automatically handled by `NotionDBIntegration.mapMemberToNotionProperties()`:

| Property | Type | Description |
|----------|------|-------------|
| Name | Title | Member name |
| Email | Email | NJIT email |
| Major | Text | Academic major |
| Graduation Year | Number | Expected year |
| Career Goal | Select | Career path |
| LinkedIn | URL | LinkedIn profile |
| GitHub | URL | GitHub profile |
| Portfolio | URL | Portfolio site |
| Calendly | URL | Calendly link |
| Status | Select | new, in-progress, completed |
| Joined | Date | Onboarding date |
| Discord Username | Text | Discord handle |

### 2. Environment Variables

Add to `.env.local`:

```bash
NOTION_API_KEY=ntn_your_api_key
NOTION_DATABASE_ID=your_database_id
```

### 3. Create Notion Integration Token

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Create new integration: "Job Club Bot"
3. Copy the Internal Integration Token
4. In your Notion database, click "..." → "Add connections" → select "Job Club Bot"

### 4. Usage Example

```javascript
import NotionDBIntegration from './src/lib/notionIntegration.js';

const notion = new NotionDBIntegration();

// Sync member to Notion
await notion.upsertMember({
  name: 'Jane Doe',
  email: 'jane.doe@njit.edu',
  major: 'Computer Science',
  graduationYear: 2025,
  careerGoal: 'ai-engineer',
  linkedinUrl: 'https://linkedin.com/in/janedoe',
  githubUrl: 'https://github.com/janedoe',
  portfolioUrl: 'https://janedoe.dev',
  calendlyUrl: 'https://calendly.com/janedoe',
  discordUsername: 'janedoe#1234'
});
```

## Discord Integration

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application: "Job Club Bot"
3. Go to "Bot" section and click "Add Bot"
4. Copy the bot token

### 2. Setup Webhook

Option A - Using Webhook (Recommended for simpler deployments):

1. In Discord server, go to channel settings
2. Integrations → Webhooks → New Webhook
3. Copy the webhook URL
4. Set as `DISCORD_WEBHOOK_URL` environment variable

Option B - Using Bot Token:

1. In Discord server permissions, add "Manage Webhooks" to bot role
2. Use bot token for direct API calls

### 3. Environment Variables

Add to `.env.local`:

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url
DISCORD_INTRO_CHANNEL_ID=123456789  # Optional, for advanced features
```

### 4. Usage Example

```javascript
import DiscordIntegration from './src/lib/discordIntegration.js';

const discord = new DiscordIntegration();

// Send welcome message
await discord.sendWelcomeMessage({
  name: 'Jane Doe',
  major: 'Computer Science',
  careerGoal: 'ai-engineer',
});

// Post introduction
await discord.postIntroduction({
  name: 'Jane Doe',
  major: 'Computer Science',
  graduationYear: 2025,
  careerGoal: 'ai-engineer',
  linkedinUrl: 'https://linkedin.com/in/janedoe',
  githubUrl: 'https://github.com/janedoe',
  calendlyUrl: 'https://calendly.com/janedoe'
});
```

## API Endpoints

### POST /api/onboarding

**Purpose:** Submit onboarding form and create member profile

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane.doe@njit.edu",
  "major": "Computer Science",
  "graduationYear": "2025",
  "careerGoal": "ai-engineer",
  "linkedinUrl": "https://linkedin.com/in/janedoe",
  "githubUrl": "https://github.com/janedoe",
  "portfolioUrl": "https://janedoe.dev",
  "calendlyUrl": "https://calendly.com/janedoe"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Welcome to Job Club! Check your email for next steps.",
  "memberId": "abc123xyz"
}
```

**Error Response (400):**
```json
{
  "errors": ["Name is required", "Valid email is required"]
}
```

### GET /api/events

**Purpose:** Fetch all upcoming published events

**Query Parameters:**
- None (all published future events returned)

**Response:**
```json
[
  {
    "_id": "abc123",
    "title": "LinkedIn Profile Workshop",
    "description": "Learn to optimize your LinkedIn profile...",
    "eventType": "workshop",
    "date": "2024-02-15T18:00:00Z",
    "location": "NJIT Campus",
    "registrationLink": "https://...",
    "speakers": [
      {
        "_id": "speaker1",
        "name": "Keith Williams",
        "title": "AI Career Coach"
      }
    ]
  }
]
```

### GET /api/resources

**Purpose:** Fetch career resources

**Query Parameters:**
- `category` (optional) - Filter by category: linkedin, github, portfolio, consulting, startup, interviews, resume, networking

**Response:**
```json
[
  {
    "_id": "res123",
    "title": "Complete LinkedIn Guide",
    "slug": "complete-linkedin-guide",
    "description": "Step-by-step guide to creating an impressive LinkedIn profile",
    "category": "linkedin",
    "difficulty": "Beginner",
    "timeToRead": 15,
    "publishedAt": "2024-01-10T00:00:00Z"
  }
]
```

### POST /api/event-registration

**Purpose:** Register a member for an event

**Request Body:**
```json
{
  "memberEmail": "jane.doe@njit.edu",
  "eventId": "abc123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Successfully registered for event"
}
```

## Deployment

### Option 1: Netlify Functions

Create `netlify/functions/onboarding.js`:

```javascript
import { handleOnboarding } from '../../src/api/routes.js';

export default async (event, context) => {
  return handleOnboarding(event, context);
};
```

### Option 2: Vercel Functions

Create `api/onboarding.js`:

```javascript
import { handleOnboarding } from '../src/api/routes.js';

export default async (req, res) => {
  return handleOnboarding(req, res);
};
```

### Option 3: Node.js Express Server

```javascript
import express from 'express';
import { handleOnboarding, handleGetEvents, handleGetResources } from './src/api/routes.js';

const app = express();
app.use(express.json());

app.post('/api/onboarding', handleOnboarding);
app.get('/api/events', handleGetEvents);
app.get('/api/resources', handleGetResources);

app.listen(3000, () => console.log('API running on :3000'));
```

## Environment Variables Checklist

```bash
# Sanity CMS
SANITY_PROJECT_ID=
SANITY_DATASET=production
SANITY_WRITE_TOKEN=

# Notion DB
NOTION_API_KEY=
NOTION_DATABASE_ID=

# Discord
DISCORD_WEBHOOK_URL=

# Optional
DISCORD_INTRO_CHANNEL_ID=
```

## Troubleshooting

### Notion Sync Not Working
- Verify API key has database access
- Check database ID format (remove hyphens if needed)
- Ensure webhook integration is connected to database

### Discord Messages Not Posting
- Verify webhook URL is correct
- Check Discord channel permissions
- Test webhook manually: `curl -X POST -H 'Content-Type: application/json' -d '{"content":"test"}' [webhook_url]`

### Sanity Create Failing
- Verify write token has correct permissions
- Check schema field names match exactly
- Ensure dataset name matches environment

### API Endpoints 500 Errors
- Check all environment variables are set
- Verify Sanity client configuration
- Review server logs for specific error messages

## Next Steps (Phase 3)

- [ ] Add email confirmations via Zapier
- [ ] Implement Zapier onboarding workflow automation
- [ ] Setup GDPR consent tracking
- [ ] Configure analytics integration (Plausible/Fathom)
- [ ] Deploy CI/CD pipeline (GitHub Actions)
- [ ] Production deployment to GitHub Pages + Vercel/Netlify
- [ ] Monitor webhook deliveries and error rates
