/**
 * Vercel Function Wrapper
 * Deploy at: api/onboarding.js (or api/events.js, api/resources.js, etc.)
 * 
 * This is a Vercel-specific wrapper for serverless functions
 */

import { handleOnboarding } from '../../src/api/routes.js';

export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Only allow POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Call the shared route handler
    return await handleOnboarding(req, res);
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({
      error: 'Internal server error',
      details: error.message,
    });
  }
}
