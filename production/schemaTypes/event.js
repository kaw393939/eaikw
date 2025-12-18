// Schema for Job Club events
// Events guide students toward career readiness through workshops, mentoring, and networking
export default {
  name: 'event',
  title: 'Job Club Event',
  type: 'document',
  description: 'Career development events: workshops, office hours, networking, and skill-building sessions',
  fields: [
    {
      name: 'title',
      title: 'Event Title',
      type: 'string',
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'description',
      title: 'Event Description',
      type: 'text',
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'eventType',
      title: 'Event Type',
      type: 'string',
      options: {
        list: [
          { title: 'Workshop', value: 'workshop' },
          { title: 'Office Hours', value: 'office-hours' },
          { title: 'Networking', value: 'networking' },
          { title: 'Hack Night', value: 'hack-night' },
          { title: 'Guest Speaker', value: 'speaker' },
          { title: 'Meetup', value: 'meetup' },
        ],
      },
    },
    {
      name: 'date',
      title: 'Event Date & Time',
      type: 'datetime',
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'endTime',
      title: 'End Time',
      type: 'datetime',
    },
    {
      name: 'location',
      title: 'Location / Venue',
      type: 'string',
      description: 'Physical location or "Zoom" for virtual events',
    },
    {
      name: 'zoomLink',
      title: 'Zoom Link (if applicable)',
      type: 'url',
    },
    {
      name: 'capacity',
      title: 'Event Capacity',
      type: 'number',
      description: 'Max attendees (optional)',
    },
    {
      name: 'speakers',
      title: 'Speakers / Hosts',
      type: 'array',
      of: [
        {
          type: 'reference',
          to: [{ type: 'speaker' }],
        },
      ],
    },
    {
      name: 'registrationLink',
      title: 'Registration Link',
      type: 'url',
      description: 'Link to Calendly, Eventbrite, or form',
    },
    {
      name: 'tags',
      title: 'Tags',
      type: 'array',
      of: [{ type: 'string' }],
      options: {
        list: [
          { title: 'AI', value: 'ai' },
          { title: 'Portfolio', value: 'portfolio' },
          { title: 'Networking', value: 'networking' },
          { title: 'Interview Prep', value: 'interview' },
          { title: 'Career', value: 'career' },
        ],
      },
    },
    {
      name: 'status',
      title: 'Status',
      type: 'string',
      options: {
        list: [
          { title: 'Upcoming', value: 'upcoming' },
          { title: 'Live', value: 'live' },
          { title: 'Completed', value: 'completed' },
          { title: 'Cancelled', value: 'cancelled' },
        ],
      },
      initialValue: 'upcoming',
    },
    {
      name: 'publishedAt',
      title: 'Published At',
      type: 'datetime',
    },
  ],
  preview: {
    select: {
      title: 'title',
      date: 'date',
    },
    prepare(selection) {
      const { title, date } = selection;
      return {
        title,
        subtitle: date ? new Date(date).toLocaleDateString() : 'No date set',
      };
    },
  },
};
