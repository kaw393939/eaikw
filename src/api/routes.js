/**
 * API Routes for Job Club
 * Handles form submissions, event registration, etc.
 * 
 * These can be deployed as:
 * - Netlify Functions (functions/ directory)
 * - Vercel Functions
 * - Express routes on a Node.js server
 * - Lambda functions
 */

import SanityClient from '@sanity/client';
import NotionDBIntegration from '../lib/notionIntegration.js';
import DiscordIntegration from '../lib/discordIntegration.js';

const sanity = new SanityClient({
  projectId: process.env.SANITY_PROJECT_ID,
  dataset: process.env.SANITY_DATASET,
  token: process.env.SANITY_WRITE_TOKEN,
  useCdn: false,
});

const notion = new NotionDBIntegration();
const discord = new DiscordIntegration();

/**
 * POST /api/onboarding
 * Receives onboarding form submission and creates member profile
 */
export async function handleOnboarding(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const formData = req.body;

    // Validate required fields
    const errors = validateOnboardingForm(formData);
    if (errors.length > 0) {
      return res.status(400).json({ errors });
    }

    // Create member profile in Sanity
    const memberProfile = await sanity.create({
      _type: 'memberProfile',
      name: formData.name,
      email: formData.email,
      major: formData.major,
      graduationYear: parseInt(formData.graduationYear),
      careerGoal: formData.careerGoal,
      linkedinUrl: formData.linkedinUrl || null,
      githubUrl: formData.githubUrl || null,
      portfolioUrl: formData.portfolioUrl || null,
      calendlyUrl: formData.calendlyUrl || null,
      onboardingStatus: 'new',
      joinedDate: new Date().toISOString(),
      lastUpdated: new Date().toISOString(),
    });

    // Sync to Notion
    await notion.upsertMember(memberProfile);

    // Post to Discord
    await discord.sendWelcomeMessage(memberProfile);
    await discord.postIntroduction(memberProfile);

    return res.status(201).json({
      success: true,
      message: 'Welcome to Job Club! Check your email for next steps.',
      memberId: memberProfile._id,
    });
  } catch (error) {
    console.error('Onboarding error:', error);
    return res.status(500).json({
      error: 'Failed to process onboarding',
      details: error.message,
    });
  }
}

/**
 * GET /api/events
 * Fetch all upcoming Job Club events
 */
export async function handleGetEvents(req, res) {
  try {
    const events = await sanity.fetch(`
      *[_type == "event" && status == "published" && dateTime(date) >= dateTime(now())]
      | order(date asc) {
        _id,
        title,
        description,
        eventType,
        date,
        endTime,
        location,
        zoomLink,
        capacity,
        registrationLink,
        tags,
        "speakers": speakers[]->{ _id, name, title, company, bio },
      }
    `);

    return res.status(200).json(events);
  } catch (error) {
    console.error('Error fetching events:', error);
    return res.status(500).json({
      error: 'Failed to fetch events',
      details: error.message,
    });
  }
}

/**
 * GET /api/resources
 * Fetch career resources by category
 */
export async function handleGetResources(req, res) {
  try {
    const { category } = req.query;

    let query = '*[_type == "resource"]';
    if (category) {
      query += `[category == "${category}"]`;
    }
    query += ' | order(publishedAt desc) { _id, title, slug, description, category, difficulty, timeToRead, publishedAt }';

    const resources = await sanity.fetch(query);

    return res.status(200).json(resources);
  } catch (error) {
    console.error('Error fetching resources:', error);
    return res.status(500).json({
      error: 'Failed to fetch resources',
      details: error.message,
    });
  }
}

/**
 * POST /api/event-registration
 * Register a member for an event
 */
export async function handleEventRegistration(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { memberEmail, eventId } = req.body;

    if (!memberEmail || !eventId) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Find member
    const member = await sanity.fetch(`*[_type == "memberProfile" && email == "${memberEmail}"][0]`);

    if (!member) {
      return res.status(404).json({ error: 'Member not found' });
    }

    // Update member's registered events (if storing registrations)
    // This is a simplified example; you might want a separate registration document type
    console.log(`Member ${memberEmail} registered for event ${eventId}`);

    return res.status(200).json({
      success: true,
      message: 'Successfully registered for event',
    });
  } catch (error) {
    console.error('Event registration error:', error);
    return res.status(500).json({
      error: 'Failed to register for event',
      details: error.message,
    });
  }
}

/**
 * Validate onboarding form data
 */
function validateOnboardingForm(data) {
  const errors = [];

  if (!data.name || data.name.trim() === '') {
    errors.push('Name is required');
  }

  if (!data.email || !isValidEmail(data.email)) {
    errors.push('Valid email is required');
  }

  if (!data.major || data.major.trim() === '') {
    errors.push('Major is required');
  }

  if (!data.graduationYear || isNaN(parseInt(data.graduationYear))) {
    errors.push('Valid graduation year is required');
  }

  if (!data.careerGoal) {
    errors.push('Career goal is required');
  }

  return errors;
}

/**
 * Basic email validation
 */
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export default {
  handleOnboarding,
  handleGetEvents,
  handleGetResources,
  handleEventRegistration,
};
