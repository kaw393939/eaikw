# Phase 2 Implementation Checklist

Complete checklist for getting Phase 2 working in your environment.

**Mission:** Turn students into career-ready AI professionals with a guided, automated onboarding experience.

This checklist ensures all integrations support the automated onboarding pipeline that guides students toward career readiness.

## ✅ Code Implementation Status

All code is implemented and ready. Check the following:

- [x] Sanity CMS schemas created (4 types)
- [x] Notion integration module created
- [x] Discord integration module created  
- [x] API routes defined (4 endpoints)
- [x] Onboarding form updated
- [x] Deployment wrappers created (Netlify + Vercel)
- [x] GitHub Actions workflow configured
- [x] Documentation written (3 guides)
- [x] Test suite created
- [x] All commits pushed to GitHub

## 📋 Configuration Checklist

Before testing locally, you need to configure external services:

### 1. Sanity CMS Setup ⏳

- [ ] Create account at sanity.io
- [ ] Create new project (or note existing project ID)
- [ ] Copy **Project ID** from sanity.io dashboard
- [ ] Create **Write Token**:
  - Go to API section
  - Click "Add API token"
  - Select "Editor" role
  - Copy the token
- [ ] Save to `.env.local`:
  ```
  SANITY_PROJECT_ID=abc123...
  SANITY_DATASET=production
  SANITY_WRITE_TOKEN=sk_prod_...
  ```

### 2. Notion DB Setup ⏳

- [ ] Create Notion account at notion.so
- [ ] Create new database called "Job Club Members"
- [ ] Copy database ID from URL
- [ ] Create Notion integration:
  - Go to notion.so/my-integrations
  - Create new integration "Job Club Bot"
  - Copy the Internal Integration Token
- [ ] Connect bot to database:
  - Open your Job Club Members database
  - Click "..." (three dots)
  - Add connections → Find "Job Club Bot"
- [ ] Save to `.env.local`:
  ```
  NOTION_API_KEY=ntn_...
  NOTION_DATABASE_ID=abc123...
  ```

### 3. Discord Setup ⏳

- [ ] Open your Discord server
- [ ] Go to channel where you want notifications
- [ ] Click channel settings (⚙️)
- [ ] Integrations → Webhooks → New Webhook
- [ ] Name: "Job Club Bot"
- [ ] Copy the Webhook URL
- [ ] Save to `.env.local`:
  ```
  DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
  ```

## 🧪 Local Testing Checklist

After configuration, test locally:

### Step 1: Start Development Server

```bash
npm install          # Install dependencies
npm run dev          # Start Eleventy dev server
```

Should see:
```
[11ty] Writing _site/index.html from ./src/index.njk
[11ty] Benchmark (in milliseconds):
```

### Step 2: Test Onboarding Form

- [ ] Navigate to http://localhost:8080/jobclub/onboarding
- [ ] Fill in form:
  - Name: Test Student
  - Email: test@njit.edu
  - Major: Computer Science
  - Graduation Year: 2025
  - Career Goal: AI Engineer
  - LinkedIn: https://linkedin.com/in/test
- [ ] Click "Complete Onboarding"

### Step 3: Verify Sanity Creation

- [ ] Login to Sanity Studio: http://localhost:3333
- [ ] Navigate to "memberProfile" collection
- [ ] Should see your test submission with:
  - Name: Test Student
  - Email: test@njit.edu
  - Status: new
  - joinedDate: today

### Step 4: Verify Notion Sync

- [ ] Open Notion database "Job Club Members"
- [ ] Refresh page (F5)
- [ ] Should see new row:
  - Name: Test Student
  - Email: test@njit.edu
  - Major: Computer Science
  - Graduation Year: 2025
  - Status: new

### Step 5: Verify Discord Post

- [ ] Check Discord channel where webhook is configured
- [ ] Should see two messages:
  1. Welcome embed with member details
  2. Introduction post with career goal and links

### Step 6: Check Error Handling

Test error scenarios:

- [ ] Submit form with missing name → Should show error "Name is required"
- [ ] Submit form with invalid email → Should show error "Valid email is required"
- [ ] Try form with Discord webhook disabled → Should still work, just skip Discord
- [ ] Check browser console for any JavaScript errors

## 🚀 Deployment Checklist

### Pre-Deployment

- [ ] All tests passing locally
- [ ] `.env.local` file NOT committed (add to .gitignore)
- [ ] Production URLs configured
- [ ] Sanity dataset set to "production"
- [ ] Notion database is shared and accessible

### Deploy to Netlify

- [ ] Create Netlify account
- [ ] Connect GitHub repository
- [ ] Add environment variables to Netlify:
  - SANITY_PROJECT_ID
  - SANITY_DATASET
  - SANITY_WRITE_TOKEN
  - NOTION_API_KEY
  - NOTION_DATABASE_ID
  - DISCORD_WEBHOOK_URL
- [ ] Deploy:
  ```bash
  netlify deploy --prod
  ```
- [ ] Test deployed form at https://yourdomain.com/jobclub/onboarding

### Deploy to Vercel (Alternative)

- [ ] Create Vercel account
- [ ] Import GitHub repository
- [ ] Add environment variables
- [ ] Deploy:
  ```bash
  vercel deploy --prod
  ```

### Setup Custom Domain

- [ ] Purchase domain (e.g., jobclub.njit.edu)
- [ ] Configure DNS settings
- [ ] Point to Netlify/Vercel
- [ ] Setup HTTPS (automatic with Netlify/Vercel)

## 📊 Monitoring Checklist

After deployment:

- [ ] Form submissions tracked in Sanity
- [ ] Members appearing in Notion DB
- [ ] Discord messages posting
- [ ] Response times < 2 seconds
- [ ] No console errors in browser
- [ ] Mobile form works on phones
- [ ] Email field validates correctly

## 🐛 Troubleshooting Checklist

If something doesn't work:

### Form won't submit
- [ ] Check browser console (F12) for errors
- [ ] Verify API endpoint is accessible: /api/onboarding
- [ ] Check that SANITY_WRITE_TOKEN is correct
- [ ] Test with curl: `curl -X POST http://localhost:8080/api/onboarding -d "{...}"`

### Sanity not creating document
- [ ] Verify SANITY_PROJECT_ID is correct (not project name)
- [ ] Verify SANITY_WRITE_TOKEN has write permissions
- [ ] Check Sanity Studio for schema errors
- [ ] Verify dataset "production" exists

### Notion not syncing
- [ ] Test Notion API key: `curl -H "Authorization: Bearer $NOTION_API_KEY" https://api.notion.com/v1/users/me`
- [ ] Verify database ID format (remove hyphens if needed)
- [ ] Check Bot is connected to database
- [ ] Verify database has correct property names

### Discord not posting
- [ ] Test webhook URL manually:
  ```bash
  curl -X POST -H 'Content-Type: application/json' \
    -d '{"content":"test"}' \
    [YOUR_WEBHOOK_URL]
  ```
- [ ] Verify webhook channel is correct
- [ ] Check Discord bot permissions

## 📱 Accessibility Checklist

Test accessibility:

- [ ] Form works with keyboard only (Tab through fields)
- [ ] Color contrast is sufficient (use WebAIM tool)
- [ ] Labels are associated with inputs
- [ ] Error messages are clear
- [ ] Mobile layout is readable (no text overflow)
- [ ] Links have underlines or visible distinction

## 🔒 Security Checklist

Before production:

- [ ] .env.local is in .gitignore
- [ ] No credentials in code comments
- [ ] API validates all inputs
- [ ] CORS headers are configured
- [ ] HTTPS is enforced
- [ ] Form has CSRF protection (if applicable)
- [ ] Rate limiting configured (if high volume expected)

## 📚 Documentation Checklist

- [ ] Team has access to PHASE_2_INTEGRATIONS.md
- [ ] Team has access to PHASE_2_QUICKSTART.md
- [ ] Team knows how to update environment variables
- [ ] Team knows how to add new events
- [ ] Team knows how to add new resources
- [ ] Troubleshooting guide is available

## ✨ Final Sign-Off

- [ ] All code deployed to production
- [ ] All integrations working
- [ ] Documentation complete
- [ ] Team trained on usage
- [ ] Ready for Phase 3

---

## Next Phase Preparation

When everything is working in Phase 2, prepare for Phase 3:

### Phase 3A: Email Integration
- [ ] Create Zapier account
- [ ] Setup onboarding email workflow
- [ ] Test email delivery

### Phase 3B: Analytics
- [ ] Choose analytics platform (Plausible/Fathom)
- [ ] Add tracking code to site
- [ ] Setup dashboards

### Phase 3C: GDPR
- [ ] Review privacy policy
- [ ] Add consent banner
- [ ] Setup data export
- [ ] Configure GDPR-compliant analytics

### Phase 3D: CI/CD
- [ ] Verify GitHub Actions workflow
- [ ] Setup staging environment
- [ ] Configure automated deployments

---

**Last Updated:** 2024-01-XX  
**Status:** Ready for implementation  
**Estimated Time:** 2-3 hours for complete setup
