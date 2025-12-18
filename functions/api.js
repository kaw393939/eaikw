/**
 * Netlify Function Wrapper
 * Deploy at: netlify/functions/onboarding.js
 * 
 * This is a Netlify-specific wrapper that handles the conversion
 * from Netlify's event/context format to our standard API routes
 */

import { handleOnboarding, handleGetEvents, handleGetResources } from '../../src/api/routes.js';

// Converts Netlify event to Express-like request object
function createRequest(event) {
  const body = event.body ? JSON.parse(event.body) : {};
  const queryParams = event.queryStringParameters || {};

  return {
    method: event.httpMethod,
    body,
    query: queryParams,
    headers: event.headers || {},
  };
}

// Netlify response object
function createResponse(statusCode, data) {
  return {
    statusCode,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    },
    body: JSON.stringify(data),
  };
}

// Generic handler that routes requests
export async function handler(event, context) {
  // Handle CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return createResponse(200, { message: 'OK' });
  }

  const req = createRequest(event);
  const res = {
    statusCode: 200,
    data: null,
    status: (code) => {
      res.statusCode = code;
      return res;
    },
    json: (data) => {
      res.data = data;
      return createResponse(res.statusCode, data);
    },
  };

  // Route based on path and method
  const path = event.path || event.route || '/api/onboarding';

  if (path.includes('onboarding') && event.httpMethod === 'POST') {
    return handleOnboarding(req, res);
  } else if (path.includes('events') && event.httpMethod === 'GET') {
    return handleGetEvents(req, res);
  } else if (path.includes('resources') && event.httpMethod === 'GET') {
    return handleGetResources(req, res);
  }

  return createResponse(404, { error: 'Not found' });
}
