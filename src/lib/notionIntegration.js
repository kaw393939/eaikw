/**
 * Notion Database Integration
 * Syncs Job Club member data with Notion DB for tracking
 * Requires NOTION_API_KEY and NOTION_DATABASE_ID env vars
 */

export class NotionDBIntegration {
  constructor() {
    this.apiKey = process.env.NOTION_API_KEY;
    this.databaseId = process.env.NOTION_DATABASE_ID;
    this.baseUrl = 'https://api.notion.com/v1';

    if (!this.apiKey || !this.databaseId) {
      console.warn(
        'Notion integration not configured. Set NOTION_API_KEY and NOTION_DATABASE_ID.'
      );
    }
  }

  /**
   * Add or update a member in the Notion database
   * @param {Object} memberData - Member profile data from Sanity
   * @returns {Promise<Object>} Created/updated page in Notion
   */
  async upsertMember(memberData) {
    if (!this.apiKey || !this.databaseId) {
      console.warn('Notion integration not configured, skipping member sync');
      return null;
    }

    try {
      // First, check if member exists
      const existing = await this.findMemberByEmail(memberData.email);

      if (existing) {
        return await this.updateMember(existing.id, memberData);
      } else {
        return await this.createMember(memberData);
      }
    } catch (error) {
      console.error('Error upserting member to Notion:', error);
      throw error;
    }
  }

  /**
   * Create a new member page in Notion
   * @param {Object} memberData - Member profile data
   * @returns {Promise<Object>} Created page
   */
  async createMember(memberData) {
    const response = await fetch(`${this.baseUrl}/pages`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        parent: { database_id: this.databaseId },
        properties: this.mapMemberToNotionProperties(memberData),
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Notion API error: ${error.message}`);
    }

    return await response.json();
  }

  /**
   * Update an existing member page in Notion
   * @param {string} pageId - Notion page ID
   * @param {Object} memberData - Updated member data
   * @returns {Promise<Object>} Updated page
   */
  async updateMember(pageId, memberData) {
    const response = await fetch(`${this.baseUrl}/pages/${pageId}`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        properties: this.mapMemberToNotionProperties(memberData),
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Notion API error: ${error.message}`);
    }

    return await response.json();
  }

  /**
   * Find a member by email
   * @param {string} email - Member email
   * @returns {Promise<Object|null>} Member page or null
   */
  async findMemberByEmail(email) {
    const response = await fetch(`${this.baseUrl}/databases/${this.databaseId}/query`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        filter: {
          property: 'Email',
          email: {
            equals: email,
          },
        },
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Notion API error: ${error.message}`);
    }

    const data = await response.json();
    return data.results.length > 0 ? data.results[0] : null;
  }

  /**
   * Map member data to Notion database properties
   * @param {Object} memberData - Member profile data
   * @returns {Object} Notion properties object
   */
  mapMemberToNotionProperties(memberData) {
    return {
      Name: {
        title: [
          {
            text: {
              content: memberData.name || '',
            },
          },
        ],
      },
      Email: {
        email: memberData.email || '',
      },
      Major: {
        rich_text: [
          {
            text: {
              content: memberData.major || '',
            },
          },
        ],
      },
      'Graduation Year': {
        number: memberData.graduationYear || null,
      },
      'Career Goal': {
        select: {
          name: this.mapCareerGoal(memberData.careerGoal),
        },
      },
      'LinkedIn': {
        url: memberData.linkedinUrl || null,
      },
      'GitHub': {
        url: memberData.githubUrl || null,
      },
      'Portfolio': {
        url: memberData.portfolioUrl || null,
      },
      'Calendly': {
        url: memberData.calendlyUrl || null,
      },
      'Status': {
        select: {
          name: memberData.onboardingStatus || 'new',
        },
      },
      'Joined': {
        date: {
          start: memberData.joinedDate || new Date().toISOString(),
        },
      },
      'Discord Username': {
        rich_text: [
          {
            text: {
              content: memberData.discordUsername || '',
            },
          },
        ],
      },
    };
  }

  /**
   * Map career goal value to display name
   */
  mapCareerGoal(value) {
    const map = {
      'ai-consultant': 'AI Consultant',
      'ai-startup': 'AI Startup Founder',
      'ai-engineer': 'AI Software Engineer',
      'data-scientist': 'Data Scientist',
      'product-manager': 'Product Manager',
      'other': 'Other',
    };
    return map[value] || 'Undecided';
  }
}

export default NotionDBIntegration;
