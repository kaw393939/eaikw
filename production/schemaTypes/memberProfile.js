// Schema for Job Club members/students
export default {
  name: 'memberProfile',
  title: 'Member Profile',
  type: 'document',
  fields: [
    {
      name: 'name',
      title: 'Full Name',
      type: 'string',
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'email',
      title: 'Email Address',
      type: 'string',
      validation: (Rule) => Rule.required().email(),
    },
    {
      name: 'major',
      title: 'Major / Field of Study',
      type: 'string',
    },
    {
      name: 'graduationYear',
      title: 'Expected Graduation Year',
      type: 'number',
    },
    {
      name: 'careerGoal',
      title: 'Primary Career Goal',
      type: 'string',
      options: {
        list: [
          { title: 'AI Consultant', value: 'ai-consultant' },
          { title: 'AI Startup Founder', value: 'ai-startup' },
          { title: 'AI Software Engineer', value: 'ai-engineer' },
          { title: 'Data Scientist', value: 'data-scientist' },
          { title: 'Product Manager (AI)', value: 'product-manager' },
          { title: 'Other', value: 'other' },
        ],
      },
    },
    {
      name: 'linkedinUrl',
      title: 'LinkedIn Profile URL',
      type: 'url',
    },
    {
      name: 'githubUrl',
      title: 'GitHub Profile URL',
      type: 'url',
    },
    {
      name: 'portfolioUrl',
      title: 'Personal Portfolio Website',
      type: 'url',
    },
    {
      name: 'calendlyUrl',
      title: 'Calendly Link',
      type: 'url',
    },
    {
      name: 'onboardingStatus',
      title: 'Onboarding Status',
      type: 'string',
      options: {
        list: [
          { title: 'New', value: 'new' },
          { title: 'In Progress', value: 'in-progress' },
          { title: 'Completed', value: 'completed' },
        ],
      },
      initialValue: 'new',
    },
    {
      name: 'missingAssets',
      title: 'Missing Professional Assets',
      type: 'array',
      of: [{ type: 'string' }],
      options: {
        list: [
          { title: 'LinkedIn', value: 'linkedin' },
          { title: 'GitHub', value: 'github' },
          { title: 'Portfolio Site', value: 'portfolio' },
          { title: 'Calendly', value: 'calendly' },
        ],
      },
    },
    {
      name: 'discordUsername',
      title: 'Discord Username',
      type: 'string',
    },
    {
      name: 'joinedDate',
      title: 'Joined Date',
      type: 'datetime',
      initialValue: () => new Date().toISOString(),
    },
    {
      name: 'lastUpdated',
      title: 'Last Updated',
      type: 'datetime',
    },
    {
      name: 'notes',
      title: 'Mentor Notes',
      type: 'text',
    },
  ],
  preview: {
    select: {
      title: 'name',
      subtitle: 'email',
    },
  },
};
