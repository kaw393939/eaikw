# Professional Portfolio Website

A modern, responsive portfolio website built with Eleventy (11ty) static site generator, featuring clean design, blog functionality, and project showcase capabilities.

## 🚀 Features

- **Static Site Generation** with Eleventy (11ty)
- **Nunjucks Templating** for maintainable layouts
- **Responsive Design** that works on all devices
- **Blog System** with pagination and tagging
- **Project Showcase** with detailed project pages
- **GitHub Pages Deployment** with automated workflows
- **SEO Optimized** with proper meta tags and semantic HTML
- **Performance Focused** with optimized assets and fast loading times

## 🛠️ Tech Stack

- [Eleventy (11ty)](https://www.11ty.dev/) - Static site generator
- [Nunjucks](https://mozilla.github.io/nunjucks/) - Templating engine
- Vanilla CSS with custom properties for styling
- Vanilla JavaScript for interactivity
- GitHub Actions for CI/CD
- GitHub Pages for hosting

## 📁 Project Structure

```
├── .github/
│   ├── workflows/
│   │   └── deploy.yml          # GitHub Actions deployment
│   └── copilot-instructions.md # Copilot configuration
├── .vscode/                    # VS Code workspace settings
├── src/
│   ├── _data/
│   │   └── site.json          # Site metadata
│   ├── _layouts/
│   │   ├── base.njk           # Base template
│   │   ├── post.njk           # Blog post template
│   │   └── project.njk        # Project template
│   ├── blog/
│   │   ├── index.njk          # Blog listing page
│   │   └── *.md               # Blog posts
│   ├── projects/
│   │   ├── index.njk          # Projects listing page
│   │   └── *.md               # Project pages
│   ├── css/
│   │   └── main.css           # Styles
│   ├── js/
│   │   └── main.js            # JavaScript
│   ├── images/                # Images and assets
│   ├── index.njk              # Homepage
│   └── about.njk              # About page
├── .eleventy.js               # Eleventy configuration
├── package.json               # Dependencies and scripts
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and visit `http://localhost:8080`

## 📝 Available Scripts

- `npm run dev` - Start development server with live reload
- `npm run build` - Build the site for production
- `npm run serve` - Serve the built site locally
- `npm run clean` - Clean the build directory

## ✨ Customization

### Site Configuration

Edit `src/_data/site.json` to update:
- Site title and description
- Author information
- Social media links
- Current year

### Adding Blog Posts

Create new Markdown files in `src/blog/` with front matter:

```markdown
---
layout: post.njk
title: "Your Post Title"
description: "Post description"
date: 2025-01-01
tags: ["blog", "tag1", "tag2"]
---

Your blog content here...
```

### Adding Projects

Create new Markdown files in `src/projects/` with front matter:

```markdown
---
layout: project.njk
title: "Project Name"
description: "Project description"
technologies: ["Tech1", "Tech2", "Tech3"]
status: "Completed"
github: "https://github.com/username/repo"
demo: "https://demo-link.com"
date: 2025-01-01
---

Your project description here...
```

### Styling

The site uses CSS custom properties for easy theming. Edit `src/css/main.css` to customize:
- Colors and typography
- Layout and spacing
- Component styles
- Responsive breakpoints

## 🚀 Deployment

The site is configured for automatic deployment to GitHub Pages using GitHub Actions.

### Setup GitHub Pages

1. Go to your repository settings
2. Navigate to "Pages" section
3. Set source to "GitHub Actions"
4. Push to the main branch to trigger deployment

### Custom Domain (Optional)

To use a custom domain:
1. Add a `CNAME` file to the `src/` directory with your domain
2. Configure your DNS settings
3. Update the `url` in `src/_data/site.json`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Eleventy](https://www.11ty.dev/) for the excellent static site generator
- [Nunjucks](https://mozilla.github.io/nunjucks/) for the powerful templating engine
- [GitHub Pages](https://pages.github.com/) for free hosting
- The web development community for inspiration and best practices

---

Built with ❤️ using Eleventy and modern web technologies.