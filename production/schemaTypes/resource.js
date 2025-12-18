// Schema for Job Club career resources and guides
export default {
  name: 'resource',
  title: 'Career Resource / Guide',
  type: 'document',
  fields: [
    {
      name: 'title',
      title: 'Resource Title',
      type: 'string',
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'slug',
      title: 'URL Slug',
      type: 'slug',
      options: {
        source: 'title',
        maxLength: 96,
      },
    },
    {
      name: 'description',
      title: 'Short Description',
      type: 'string',
      validation: (Rule) => Rule.max(160),
    },
    {
      name: 'category',
      title: 'Category',
      type: 'string',
      options: {
        list: [
          { title: 'LinkedIn', value: 'linkedin' },
          { title: 'GitHub', value: 'github' },
          { title: 'Portfolio', value: 'portfolio' },
          { title: 'Consulting', value: 'consulting' },
          { title: 'Startup', value: 'startup' },
          { title: 'Interviews', value: 'interviews' },
          { title: 'Resume', value: 'resume' },
          { title: 'Networking', value: 'networking' },
        ],
      },
    },
    {
      name: 'content',
      title: 'Content',
      type: 'blockContent',
    },
    {
      name: 'author',
      title: 'Author',
      type: 'reference',
      to: [{ type: 'author' }],
    },
    {
      name: 'coverImage',
      title: 'Cover Image',
      type: 'image',
      options: {
        hotspot: true,
      },
    },
    {
      name: 'publishedAt',
      title: 'Published Date',
      type: 'datetime',
    },
    {
      name: 'updatedAt',
      title: 'Last Updated',
      type: 'datetime',
    },
    {
      name: 'tags',
      title: 'Tags',
      type: 'array',
      of: [{ type: 'string' }],
      options: {
        list: [
          { title: 'AI', value: 'ai' },
          { title: 'Career', value: 'career' },
          { title: 'Interview', value: 'interview' },
          { title: 'Portfolio', value: 'portfolio' },
          { title: 'Guide', value: 'guide' },
          { title: 'Template', value: 'template' },
        ],
      },
    },
    {
      name: 'difficulty',
      title: 'Difficulty Level',
      type: 'string',
      options: {
        list: [
          { title: 'Beginner', value: 'beginner' },
          { title: 'Intermediate', value: 'intermediate' },
          { title: 'Advanced', value: 'advanced' },
        ],
      },
    },
    {
      name: 'timeToRead',
      title: 'Estimated Read Time (minutes)',
      type: 'number',
    },
  ],
  preview: {
    select: {
      title: 'title',
      author: 'author.name',
      media: 'coverImage',
    },
    prepare(selection) {
      const { title, author } = selection;
      return {
        title,
        subtitle: author ? `By ${author}` : 'No author',
      };
    },
  },
};
