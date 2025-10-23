# Blog Post Template

Use this template for writing new blog posts. Save as `your-post-slug.md` in the `blog/` folder.

---

**Title:** Your Post Title Here

**Date:** October 21, 2025

**Slug:** your-post-slug

**Excerpt:** A short 1-2 sentence description that will appear on the blog listing page.

---

## Introduction

Start with a hook. What problem are you addressing? Why should they care?

Example:
> I've seen three companies burn $50K+ on the wrong AI architecture in the last six months. Here's what they got wrong and how to avoid the same mistake.

## The Problem

Describe the problem in detail. Use specific examples if possible.

## The Solution

Walk through your solution. Use:
- Code examples (if relevant)
- Architecture diagrams (describe them if you can't embed images yet)
- Step-by-step explanations
- Real-world examples from your experience

## Key Takeaways

Summarize in 3-5 bullet points:
- Takeaway #1
- Takeaway #2
- Takeaway #3

## What This Means For You

Connect it back to the reader's situation. How can they apply this?

## Want Help With This?

End with a soft CTA:
> If you're facing similar challenges with [specific problem], let's talk. I help teams [specific outcome] through [your service].

---

## How To Publish

1. Write your post using this template
2. Save as `your-post-slug.md` in `website/blog/`
3. Convert to HTML using the template below
4. Test locally
5. Deploy

## Converting Markdown to HTML

For now, manually convert using this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Your excerpt here">
    <title>Your Post Title - Keith Williams</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <nav class="nav">
        <div class="container">
            <div class="nav-content">
                <a href="../index.html" class="logo">Keith Williams</a>
                <div class="nav-links">
                    <a href="../index.html">Home</a>
                    <a href="../about.html">About</a>
                    <a href="../system.html">The System</a>
                    <a href="../blog.html">Blog</a>
                    <a href="../index.html#contact" class="cta-button">Work With Me</a>
                </div>
            </div>
        </div>
    </nav>

    <article style="max-width: 800px; margin: 0 auto; padding: 5rem 2rem;">
        <div style="text-align: center; margin-bottom: 3rem;">
            <span style="color: var(--primary); font-weight: 600;">October 21, 2025</span>
            <h1 style="font-size: 2.5rem; color: var(--secondary); margin: 1rem 0;">Your Post Title</h1>
        </div>

        <!-- Your content here -->
        <p>Paragraph text...</p>
        <h2>Subheading</h2>
        <p>More content...</p>

        <!-- CTA at bottom -->
        <div style="background: var(--gray-100); padding: 2rem; border-radius: var(--radius); margin-top: 3rem; text-align: center;">
            <h3>Need Help With This?</h3>
            <p>If you're facing similar challenges, let's talk.</p>
            <a href="../index.html#contact" class="btn-primary">Get In Touch →</a>
        </div>

        <!-- Share buttons -->
        <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--gray-200); text-align: center;">
            <p style="margin-bottom: 1rem;">Share this post:</p>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=YOUR_URL" target="_blank" 
               style="color: var(--primary); margin: 0 1rem;">LinkedIn</a>
            <a href="https://twitter.com/intent/tweet?url=YOUR_URL&text=YOUR_TITLE" target="_blank"
               style="color: var(--primary); margin: 0 1rem;">Twitter</a>
        </div>
    </article>

    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-left">
                    <p>&copy; 2025 Keith Williams. Builder. Creator. Magician. Sage. Explorer.</p>
                </div>
                <div class="footer-right">
                    <a href="https://github.com/kaw393939" target="_blank">GitHub</a>
                    <a href="https://linkedin.com/in/keithwilliams5" target="_blank">LinkedIn</a>
                    <a href="../blog.html">Blog</a>
                </div>
            </div>
        </div>
    </footer>

    <script src="../script.js"></script>
</body>
</html>
```

## Blog Post Ideas (From Your Strategy)

1. **Why RAG Systems Fail in Production** (technical deep-dive)
2. **The $50K Mistake: Choosing The Wrong AI Architecture** (decision framework)
3. **Practice Builds Theory: 43 Years of Shipping Code** (philosophy)
4. **Knowledge Graphs + Vector DBs: When You Need Both** (architecture)
5. **Training AI Teams: What Actually Works** (teaching)
6. **Multi-Agent Systems: Beyond The Tutorial** (advanced implementation)
7. **Test Coverage for AI Systems: Yes, You Need It** (quality)
8. **The CTO's Guide to AI Strategy** (leadership)
9. **Teaching in Zambia: What I Learned** (personal story)

Pick one and start writing!
