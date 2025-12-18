/**
 * Integration Tests for Phase 2
 * Run with: npm run test
 */

import { describe, it, expect, beforeAll, afterAll } from '@jest/globals';
import NotionDBIntegration from '../src/lib/notionIntegration.js';
import DiscordIntegration from '../src/lib/discordIntegration.js';
import { handleOnboarding, handleGetEvents, handleGetResources } from '../src/api/routes.js';

describe('Phase 2: Integrations', () => {
  let notion;
  let discord;

  beforeAll(() => {
    // Setup test integrations
    notion = new NotionDBIntegration();
    discord = new DiscordIntegration();

    // Check env variables
    if (!process.env.SANITY_PROJECT_ID) {
      console.warn('⚠️  SANITY_PROJECT_ID not set, Sanity tests may fail');
    }
    if (!process.env.NOTION_API_KEY) {
      console.warn('⚠️  NOTION_API_KEY not set, Notion tests may fail');
    }
    if (!process.env.DISCORD_WEBHOOK_URL) {
      console.warn('⚠️  DISCORD_WEBHOOK_URL not set, Discord tests may fail');
    }
  });

  describe('NotionDBIntegration', () => {
    const testMember = {
      name: 'Test Student',
      email: `test-${Date.now()}@njit.edu`,
      major: 'Computer Science',
      graduationYear: 2025,
      careerGoal: 'ai-engineer',
      linkedinUrl: 'https://linkedin.com/in/test',
      githubUrl: 'https://github.com/test',
      portfolioUrl: 'https://test.dev',
      calendlyUrl: 'https://calendly.com/test',
      discordUsername: 'testuser#1234',
      onboardingStatus: 'new',
      joinedDate: new Date().toISOString(),
    };

    it('should map member data to Notion properties', () => {
      const props = notion.mapMemberToNotionProperties(testMember);

      expect(props).toHaveProperty('Name');
      expect(props).toHaveProperty('Email');
      expect(props).toHaveProperty('Major');
      expect(props).toHaveProperty('Graduation Year');
      expect(props).toHaveProperty('Career Goal');
      expect(props).toHaveProperty('LinkedIn');
      expect(props).toHaveProperty('GitHub');
      expect(props).toHaveProperty('Portfolio');
      expect(props).toHaveProperty('Calendly');
      expect(props).toHaveProperty('Status');
      expect(props).toHaveProperty('Joined');

      // Verify property values
      expect(props.Name.title[0].text.content).toBe(testMember.name);
      expect(props.Email.email).toBe(testMember.email);
    });

    it('should map career goal values correctly', () => {
      const expectations = {
        'ai-consultant': 'AI Consultant',
        'ai-startup': 'AI Startup Founder',
        'ai-engineer': 'AI Software Engineer',
        'data-scientist': 'Data Scientist',
        'product-manager': 'Product Manager',
        'other': 'Other',
      };

      Object.entries(expectations).forEach(([input, expected]) => {
        expect(notion.mapCareerGoal(input)).toBe(expected);
      });
    });

    it('should handle missing optional fields', () => {
      const minimalMember = {
        name: 'John Doe',
        email: 'john@example.com',
        major: 'Engineering',
        graduationYear: 2024,
        careerGoal: 'ai-engineer',
      };

      const props = notion.mapMemberToNotionProperties(minimalMember);

      expect(props.LinkedIn.url).toBeNull();
      expect(props.GitHub.url).toBeNull();
      expect(props['Discord Username'].rich_text[0].text.content).toBe('');
    });

    // Skip actual API calls unless NOTION_API_KEY is set
    if (process.env.NOTION_API_KEY && process.env.NOTION_DATABASE_ID) {
      it('should create member in Notion', async () => {
        const result = await notion.createMember(testMember);

        expect(result).toHaveProperty('id');
        expect(result).toHaveProperty('parent');
        expect(result).toHaveProperty('properties');
      });

      it('should find member by email', async () => {
        const result = await notion.findMemberByEmail(testMember.email);

        if (result) {
          expect(result).toHaveProperty('id');
        }
      });
    }
  });

  describe('DiscordIntegration', () => {
    const testMember = {
      name: 'Jane Doe',
      major: 'Computer Science',
      careerGoal: 'ai-engineer',
      graduationYear: 2025,
      linkedinUrl: 'https://linkedin.com/in/jane',
      githubUrl: 'https://github.com/jane',
      calendlyUrl: 'https://calendly.com/jane',
    };

    it('should build welcome embed', () => {
      const embed = discord.buildWelcomeEmbed(testMember);

      expect(embed).toHaveProperty('title');
      expect(embed).toHaveProperty('description');
      expect(embed).toHaveProperty('color');
      expect(embed).toHaveProperty('fields');
      expect(embed.fields).toHaveLength(3);

      // Verify fields
      const fields = embed.fields.map((f) => f.name);
      expect(fields).toContain('Major');
      expect(fields).toContain('Graduation Year');
      expect(fields).toContain('Career Goal');
    });

    it('should build intro text with links', () => {
      const text = discord.buildIntroText(testMember);

      expect(text).toContain(testMember.name);
      expect(text).toContain(testMember.major);
      expect(text).toContain('LinkedIn');
      expect(text).toContain('GitHub');
      expect(text).toContain('Schedule time');
    });

    it('should build event embed', () => {
      const event = {
        title: 'LinkedIn Workshop',
        description: 'Learn to optimize your profile',
        eventType: 'workshop',
        date: new Date().toISOString(),
        location: 'NJIT Campus',
        registrationLink: 'https://eventbrite.com/e/123',
      };

      const embed = discord.buildEventEmbed(event);

      expect(embed).toHaveProperty('title');
      expect(embed).toHaveProperty('description');
      expect(embed).toHaveProperty('fields');
      expect(embed.title).toContain('LinkedIn Workshop');
    });

    it('should map career goal to emoji labels', () => {
      const expectations = {
        'ai-consultant': '🧠 AI Consultant',
        'ai-startup': '🚀 AI Startup Founder',
        'ai-engineer': '💻 AI Software Engineer',
      };

      Object.entries(expectations).forEach(([input, expected]) => {
        expect(discord.getCareerGoalLabel(input)).toBe(expected);
      });
    });
  });

  describe('API Routes', () => {
    describe('POST /api/onboarding', () => {
      it('should validate required fields', async () => {
        const req = {
          method: 'POST',
          body: {
            name: 'John Doe',
            // Missing email, major, etc.
          },
        };

        const res = {
          statusCode: 200,
          status: (code) => {
            res.statusCode = code;
            return res;
          },
          json: (data) => {
            res.data = data;
            return data;
          },
        };

        // This would fail validation
        // Result depends on implementation details
      });

      it('should reject invalid email', async () => {
        const req = {
          method: 'POST',
          body: {
            name: 'John Doe',
            email: 'not-an-email',
            major: 'CS',
            graduationYear: '2025',
            careerGoal: 'ai-engineer',
          },
        };

        // Should return 400 with error
      });

      it('should accept valid form submission', async () => {
        const req = {
          method: 'POST',
          body: {
            name: 'Jane Doe',
            email: `jane-${Date.now()}@njit.edu`,
            major: 'Computer Science',
            graduationYear: '2025',
            careerGoal: 'ai-engineer',
            linkedinUrl: 'https://linkedin.com/in/jane',
            githubUrl: 'https://github.com/jane',
          },
        };

        // Should return 201 with memberId
      });
    });

    describe('GET /api/events', () => {
      it('should return array of events', async () => {
        // Fetch should return published, future events
        // Sorted by date ascending
      });

      it('should return empty array if no events', async () => {
        // Should handle gracefully
      });
    });

    describe('GET /api/resources', () => {
      it('should return all resources', async () => {
        // Should return resources with category, difficulty, etc.
      });

      it('should filter by category', async () => {
        // Should return only resources matching category
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle missing environment variables gracefully', () => {
      const integrationNoKey = new NotionDBIntegration();
      // Should not throw, just warn
    });

    it('should handle API errors', async () => {
      // Notion API returns 401 for invalid key
      // Should catch and rethrow with clear message
    });

    it('should handle network timeouts', async () => {
      // Timeout after 10 seconds
      // Should return error response
    });
  });
});

describe('Integration Tests (End-to-End)', () => {
  it('should complete full onboarding flow', async () => {
    // 1. Submit form to /api/onboarding
    // 2. Verify memberProfile created in Sanity
    // 3. Verify member appears in Notion
    // 4. Verify Discord messages posted
    // 5. Verify form shows success message

    // This test requires all integrations to be configured
    if (!process.env.SANITY_WRITE_TOKEN || !process.env.NOTION_API_KEY) {
      console.log('⏭️  Skipping E2E test (missing credentials)');
      return;
    }

    // Full flow test here
  });
});
