// Schema for speakers/event hosts
export default {
  name: 'speaker',
  title: 'Speaker / Host',
  type: 'document',
  fields: [
    {
      name: 'name',
      title: 'Full Name',
      type: 'string',
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'title',
      title: 'Job Title / Role',
      type: 'string',
    },
    {
      name: 'company',
      title: 'Company / Organization',
      type: 'string',
    },
    {
      name: 'bio',
      title: 'Bio',
      type: 'text',
    },
    {
      name: 'photo',
      title: 'Photo',
      type: 'image',
      options: {
        hotspot: true,
      },
    },
    {
      name: 'email',
      title: 'Email Address',
      type: 'string',
    },
    {
      name: 'linkedinUrl',
      title: 'LinkedIn Profile',
      type: 'url',
    },
    {
      name: 'twitterUrl',
      title: 'Twitter / X Profile',
      type: 'url',
    },
    {
      name: 'websiteUrl',
      title: 'Personal Website',
      type: 'url',
    },
  ],
  preview: {
    select: {
      title: 'name',
      subtitle: 'company',
    },
  },
};
