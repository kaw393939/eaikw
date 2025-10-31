# 117 Site

A static site built with Eleventy (11ty) featuring comprehensive code quality
gates and Lighthouse CI.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run all quality checks
npm test
```

## Features

- ✨ **11ty Static Site Generator** - Fast, flexible templating
- 🎨 **Multiple Template Languages** - Nunjucks, Markdown, HTML
- 🔍 **ESLint** - JavaScript linting
- 💅 **Prettier** - Code formatting
- 🎯 **Stylelint** - CSS linting
- 📝 **Markdownlint** - Markdown linting
- 🪝 **Husky + lint-staged** - Pre-commit hooks
- 🚦 **Lighthouse CI** - Performance, accessibility, SEO checks
- 🤖 **GitHub Actions** - Automated CI/CD
- 📚 **VS Code Integration** - Extensions and settings included

## Project Structure

```
117_site/
├── src/
│   ├── _includes/     # Reusable components and partials
│   ├── _layouts/      # Page layout templates
│   ├── _data/         # Global data files
│   ├── assets/        # CSS, JS, images
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── index.md       # Homepage
├── _site/             # Build output (git-ignored)
├── .github/
│   └── workflows/     # CI/CD pipelines
├── docs/
│   └── AI-GUIDE.md    # Guide for AI coding assistants
└── .eleventy.js       # 11ty configuration
```

## Available Scripts

- `npm start` - Start development server with live reload
- `npm run build` - Build site for production
- `npm run clean` - Clean build directory
- `npm test` - Run all linters and build
- `npm run lint` - Run all linters
- `npm run lint:js` - Lint JavaScript files
- `npm run lint:css` - Lint CSS files
- `npm run lint:md` - Lint Markdown files
- `npm run lint:format` - Check code formatting
- `npm run format` - Auto-format all files
- `npm run lighthouse` - Run Lighthouse CI checks

## Code Quality Gates

All code must pass these checks before commit:

1. **ESLint** - No JavaScript errors or warnings
2. **Stylelint** - Valid, formatted CSS
3. **Prettier** - Consistent code formatting
4. **Markdownlint** - Clean markdown files

Pre-commit hooks automatically run these checks on staged files.

## Deployment

The site automatically deploys to GitHub Pages when:

1. Code is pushed to the `main` branch
2. All quality checks pass
3. Lighthouse CI meets performance budgets
4. Build completes successfully

### GitHub Pages Setup

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select **GitHub Actions**
4. The site will deploy automatically on push to `main`

### GitHub Actions Secrets (Optional)

For enhanced Lighthouse CI features, add the following secret:

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `LHCI_GITHUB_APP_TOKEN`
4. Value: Your Lighthouse CI GitHub App token
5. [Learn more about Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)

**Note:** The CI/CD pipeline will work without this secret, but Lighthouse
results won't be posted as GitHub comments.

### Environment Variables

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

Edit `.env` with your site configuration:

- `SITE_TITLE` - Your site title
- `SITE_DESCRIPTION` - Site description for meta tags
- `SITE_URL` - Production URL (update for GitHub Pages)
- `SITE_AUTHOR` - Your name

## VS Code Setup

Recommended extensions are automatically suggested. Accept the prompt to install
them for the best development experience.

## Documentation

See [AI-GUIDE.md](docs/AI-GUIDE.md) for detailed documentation aimed at AI
coding assistants.

## License

MIT
