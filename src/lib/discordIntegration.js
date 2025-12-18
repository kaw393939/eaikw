/**
 * Discord Integration
 * Posts welcome messages and handles Job Club member notifications
 */

export class DiscordIntegration {
  constructor() {
    this.webhookUrl = process.env.DISCORD_WEBHOOK_URL;
    this.introChannelId = process.env.DISCORD_INTRO_CHANNEL_ID;

    if (!this.webhookUrl) {
      console.warn('Discord integration not configured. Set DISCORD_WEBHOOK_URL.');
    }
  }

  /**
   * Send welcome message to Discord when member joins
   * @param {Object} memberData - Member profile data from Sanity
   * @returns {Promise<Object>} Discord API response
   */
  async sendWelcomeMessage(memberData) {
    if (!this.webhookUrl) {
      console.warn('Discord integration not configured, skipping message');
      return null;
    }

    try {
      const embed = this.buildWelcomeEmbed(memberData);
      const response = await fetch(this.webhookUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: `🎉 Welcome to Job Club, ${memberData.name}!`,
          embeds: [embed],
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`Discord API error: ${error}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending Discord message:', error);
      throw error;
    }
  }

  /**
   * Build Discord embed for welcome message
   * @param {Object} memberData - Member profile data
   * @returns {Object} Discord embed object
   */
  buildWelcomeEmbed(memberData) {
    const careerGoalLabel = this.getCareerGoalLabel(memberData.careerGoal);

    return {
      title: `${memberData.name} has joined Job Club! 👋`,
      description: `Welcome to the NJIT Job Club community! We're excited to have you here.`,
      color: 0x6366f1,
      fields: [
        {
          name: 'Major',
          value: memberData.major || 'Not specified',
          inline: true,
        },
        {
          name: 'Graduation Year',
          value: memberData.graduationYear ? memberData.graduationYear.toString() : 'Not specified',
          inline: true,
        },
        {
          name: 'Career Goal',
          value: careerGoalLabel,
          inline: false,
        },
      ],
      footer: {
        text: 'Job Club | AI Career Accelerator',
      },
      timestamp: new Date().toISOString(),
    };
  }

  /**
   * Send message to intro channel with member info
   * @param {Object} memberData - Member profile data
   * @returns {Promise<Object>} Discord API response
   */
  async postIntroduction(memberData) {
    if (!this.webhookUrl) {
      console.warn('Discord integration not configured, skipping intro');
      return null;
    }

    try {
      const introText = this.buildIntroText(memberData);
      const response = await fetch(this.webhookUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: introText,
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`Discord API error: ${error}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error posting introduction:', error);
      throw error;
    }
  }

  /**
   * Build intro text for Discord post
   * @param {Object} memberData - Member profile data
   * @returns {string} Formatted intro text
   */
  buildIntroText(memberData) {
    const links = [];
    if (memberData.linkedinUrl) links.push(`[LinkedIn](${memberData.linkedinUrl})`);
    if (memberData.githubUrl) links.push(`[GitHub](${memberData.githubUrl})`);
    if (memberData.portfolioUrl) links.push(`[Portfolio](${memberData.portfolioUrl})`);

    let text = `## ${memberData.name}\n`;
    text += `**Major:** ${memberData.major || 'Not specified'}\n`;
    text += `**Graduation:** ${memberData.graduationYear || 'Not specified'}\n`;
    text += `**Career Goal:** ${this.getCareerGoalLabel(memberData.careerGoal)}\n`;

    if (links.length > 0) {
      text += `\n**Connect:** ${links.join(' • ')}\n`;
    }

    if (memberData.calendlyUrl) {
      text += `\n[Schedule time with ${memberData.name}](${memberData.calendlyUrl})`;
    }

    return text;
  }

  /**
   * Map career goal value to display label
   */
  getCareerGoalLabel(value) {
    const labels = {
      'ai-consultant': '🧠 AI Consultant',
      'ai-startup': '🚀 AI Startup Founder',
      'ai-engineer': '💻 AI Software Engineer',
      'data-scientist': '📊 Data Scientist',
      'product-manager': '🎯 Product Manager',
      'other': '❓ Other/Undecided',
    };
    return labels[value] || 'Undecided';
  }

  /**
   * Send event notification to Discord
   * @param {Object} eventData - Event data from Sanity
   * @returns {Promise<Object>} Discord API response
   */
  async notifyEvent(eventData) {
    if (!this.webhookUrl) {
      console.warn('Discord integration not configured, skipping event notification');
      return null;
    }

    try {
      const embed = this.buildEventEmbed(eventData);
      const response = await fetch(this.webhookUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: `📅 New Job Club Event: ${eventData.title}`,
          embeds: [embed],
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`Discord API error: ${error}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending event notification:', error);
      throw error;
    }
  }

  /**
   * Build Discord embed for event notification
   */
  buildEventEmbed(eventData) {
    const eventTypeEmoji = {
      workshop: '🎓',
      'office-hours': '💼',
      networking: '🤝',
      'hack-night': '🔨',
      speaker: '🎤',
      meetup: '👥',
    };

    return {
      title: `${eventTypeEmoji[eventData.eventType] || '📌'} ${eventData.title}`,
      description: eventData.description || '',
      color: 0x6366f1,
      fields: [
        {
          name: 'Date & Time',
          value: eventData.date ? new Date(eventData.date).toLocaleString() : 'TBD',
          inline: true,
        },
        {
          name: 'Location',
          value: eventData.location || (eventData.zoomLink ? 'Virtual' : 'TBD'),
          inline: true,
        },
        ...(eventData.registrationLink
          ? [
              {
                name: 'Register',
                value: `[Click here](${eventData.registrationLink})`,
                inline: false,
              },
            ]
          : []),
      ],
      footer: {
        text: 'Job Club | AI Career Accelerator',
      },
      timestamp: new Date().toISOString(),
    };
  }
}

export default DiscordIntegration;
