# Phase 2 Quick Start Guide

Get Job Club integrations up and running in 10 minutes.

**Mission:** Turn students into career-ready AI professionals with a guided, automated onboarding experience.

These integrations power the automated career pipeline that starts with onboarding and guides students to professional readiness.

## Checklist

- [ ] Step 1: Configure Sanity CMS
- [ ] Step 2: Setup Notion DB
- [ ] Step 3: Setup Discord Webhook
- [ ] Step 4: Configure Environment Variables
- [ ] Step 5: Test Integrations
- [ ] Step 6: Deploy

## Step 1: Configure Sanity CMS (5 min)

### 1.1 Get Project Credentials

1. Go to [sanity.io](https://sanity.io)
2. Create a new project or use existing: `Job Club`
3. Copy your **Project ID** from project settings
4. Create a **Write Token**:
   - Go to API section
   - Click "Add API token"
   - Select "Editor" role (write permissions)
   - Copy the token

### 1.2 Verify Schemas

```bash
cd production
npm install
npm run dev
```

Visit `http://localhost:3333` to see Sanity Studio with these document types:
- memberProfile
- event
- jobclubSpeaker
- resource

### 1.3 Add Test Data

Create one test member in Sanity Studio:
- Name: "Test Student"
- Email: "test@njit.edu"
- Major: "Computer Science"
- Graduation Year: 2025
- Career Goal: "ai-engineer"

## Step 2: Setup Notion DB (5 min)

### 2.1 Create Notion Database

1. Go to [notion.so](https://notion.so)
2. Create new database: "Job Club Members"
3. Copy database ID from URL: `notion.so/[workspace]/[database_id]`

### 2.2 Create Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Create: "Job Club Bot"
3. Copy the **Internal Integration Token**
4. In your Notion database:
   - Click "..." (three dots)
   - Select "Add connections"
   - Find and add "Job Club Bot"

### 2.3 Verify Properties

The integration will auto-create these properties:
- Name (Title)
- Email
- Major
- Graduation Year
- Career Goal (Select: AI Consultant, AI Startup, AI Engineer, Data Scientist, Product Manager, Other)
- LinkedIn, GitHub, Portfolio, Calendly (URLs)
- Status (Select: new, in-progress, completed)
- Joined (Date)
- Discord Username

## Step 3: Setup Discord Webhook (3 min)

### 3.1 Create Webhook

1. Open your Discord server
2. Go to channel settings (where you want messages)
3. Integrations → Webhooks → New Webhook
4. Name: "Job Club Bot"
5. Copy **Webhook URL**

### 3.2 Test Webhook

```bash
curl -X POST -H 'Content-Type: application/json' \
  -d '{"content":"Test message"}' \
  [YOUR_WEBHOOK_URL]
```

Should post a message in your Discord channel.

## Step 4: Configure Environment Variables (2 min)

Copy `.env.local.template` to `.env.local`:

```bash
cp .env.local.template .env.local
```

Fill in values:

```bash
# Sanity
SANITY_PROJECT_ID=abc123...
SANITY_DATASET=production
SANITY_WRITE_TOKEN=sk_prod_...

# Notion
NOTION_API_KEY=ntn_...
NOTION_DATABASE_ID=abc123...

# Discord
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

## Step 5: Test Integrations

### 5.1 Test API Locally

Start development server:

```bash
npm run dev
```

Test onboarding form:
1. Navigate to `http://localhost:8080/jobclub/onboarding`
2. Fill in form with test data
3. Submit

Should see:
- ✅ Success message in browser
- ✅ New document in Sanity Studio
- ✅ New row in Notion DB
- ✅ Message in Discord channel

### 5.2 Check Results

**Sanity CMS:**
1. Open Sanity Studio at `http://localhost:3333`
2. Go to "memberProfile" collection
3. Should see your test submission

**Notion:**
1. Refresh Notion database
2. Should see new row with your data

**Discord:**
1. Check Discord channel
2. Should see welcome message and introduction post

## Step 6: Deploy

### 6.1 Choose Deployment Platform

Choose one:

**Option A: Netlify Functions**
- Best for: Simple functions + static site
- Setup: Automatic with `netlify.toml`
- Functions at: `functions/api.js`

**Option B: Vercel Functions**
- Best for: Optimized serverless
- Setup: Drop `api/onboarding.js` etc.
- Deploy: `vercel deploy`

**Option C: Express Server**
- Best for: Custom logic + WebSocket
- Setup: Install Express, run server
- Deploy: Railway, Render, Heroku

### 6.2 Set Secrets

Add environment variables to your deployment platform:

**Netlify:**
```
Site settings → Build & deploy → Environment
```

**Vercel:**
```
Settings → Environment Variables
```

### 6.3 Update Form Action

If using Vercel/Express, update form in `src/jobclub/onboarding.njk`:

```html
<!-- Change action to your API URL -->
<form method="POST" action="https://yourdomain.com/api/onboarding">
```

### 6.4 Deploy

```bash
# Build for production
npm run build

# Deploy (platform-specific)
netlify deploy --prod
# or
vercel deploy --prod
```

## Testing Checklist

- [ ] Form submits without errors
- [ ] Data appears in Sanity CMS within 2 seconds
- [ ] Data syncs to Notion within 5 seconds
- [ ] Discord messages post within 3 seconds
- [ ] Success message shows in browser
- [ ] Email field is validated
- [ ] All URL fields accept valid URLs
- [ ] Navigation links work

## Common Issues

### "Failed to create memberProfile"
- Check `SANITY_WRITE_TOKEN` is correct
- Verify token has write permissions
- Check `SANITY_PROJECT_ID` matches

### "Notion sync failed"
- Verify `NOTION_API_KEY` is correct
- Check `NOTION_DATABASE_ID` format
- Confirm Bot is connected to database

### "Discord webhook not working"
- Verify webhook URL is complete
- Check Discord channel permissions
- Ensure webhook hasn't expired

### "CORS errors in browser"
- Add CORS headers to API response:
  ```javascript
  res.setHeader('Access-Control-Allow-Origin', '*');
  ```
- Or use CORS middleware in Express

## Next Steps

After Phase 2 is working:

1. **Phase 3A: Email Integration**
   - Setup Zapier workflow for confirmation emails
   - Send personalized onboarding emails
   - Track email opens

2. **Phase 3B: Analytics**
   - Add Plausible/Fathom tracking
   - Monitor form conversion rate
   - Track event attendance

3. **Phase 3C: GDPR Compliance**
   - Add cookie consent banner
   - Implement data export feature
   - Add data deletion workflow

4. **Phase 3D: CI/CD & Deployment**
   - Setup GitHub Actions for auto-deployment
   - Configure Lighthouse CI for performance
   - Setup error monitoring (Sentry)

## Need Help?

- **Sanity docs**: https://www.sanity.io/docs
- **Notion API**: https://developers.notion.com
- **Discord Webhooks**: https://discord.com/developers/docs/resources/webhook
- **GitHub**: Ask in Discussions or Issues
