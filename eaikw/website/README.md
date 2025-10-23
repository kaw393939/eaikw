# Keith Williams - AI Consulting Landing Page

A professional landing page for AI consulting, training, and engineering services.

## 🎯 Strategic Positioning

This website positions you as:
- **AI Engineering Consultant** (production systems, architecture, implementation)
- **AI Team Trainer** (workshops, bootcamps, ongoing education)
- **Technical Advisor / Fractional CTO** (strategy, leadership, long-term partnerships)

Your R&D system is shown as **proof of expertise**, not a product for sale.

## 📁 File Structure

```
website/
├── index.html          # Homepage (main landing page)
├── about.html          # About page (your journey/story)
├── blog.html           # Blog landing (posts coming soon)
├── system.html         # The System page (R&D proof)
├── styles.css          # All styling
├── script.js           # JavaScript functionality
└── README.md           # This file
```

## 🚀 How To Use

### Option 1: Local Preview (Simplest)
Just double-click `index.html` to open in your browser. All pages work locally.

### Option 2: Python HTTP Server (Better)
```bash
cd website
python3 -m http.server 8000
```
Then visit: http://localhost:8000

### Option 3: Deploy to Production

**GitHub Pages (Free):**
1. Create a new repo: `keithwilliams-consulting`
2. Upload all files to the repo
3. Go to Settings → Pages → Source: main branch
4. Your site will be live at: `https://kaw393939.github.io/keithwilliams-consulting/`

**Netlify (Free, Custom Domain):**
1. Sign up at netlify.com
2. Drag and drop the `website` folder
3. Done! Custom domain setup available.

**Your Own Domain:**
- Buy domain at Namecheap/Google Domains
- Host on GitHub Pages or Netlify
- Point DNS to hosting provider

## ✏️ Customization Checklist

### Before You Launch:

1. **Add Your Email** (Required)
   - Open `index.html`
   - Find: `your.email@example.com`
   - Replace with your actual email address

2. **Review Content**
   - All pages use info from your CV/LinkedIn strategy
   - Check for accuracy (especially dates, numbers)
   - Adjust tone if needed (currently: direct, confident, no-BS)

3. **Optional: Add Photos**
   - Headshot for About page
   - Screenshots of your system for System page
   - Team training photos if you have them

4. **Test All Links**
   - GitHub links work (kaw393939)
   - LinkedIn link works (keithwilliams5)
   - Email link works

## 🎨 Design Principles (Cialdini + Brand Archetypes)

### Cialdini's 6 Principles Applied:

1. **Authority**
   - 43 years experience, 22+ years teaching, CTO
   - MS Instructional Design (3.9 GPA)
   - NJIT Director credentials
   - Production code proof (20K+ LOC)

2. **Social Proof**
   - GitHub repos with real code
   - Test coverage stats (100%)
   - Years of experience numbers
   - Fortune 500 recognition

3. **Scarcity**
   - "Limited availability"
   - "Small number of clients"
   - "Priority goes to serious teams"

4. **Reciprocity**
   - Blog content (giving value first)
   - Open source code (GitHub)
   - Detailed system explanations

5. **Consistency/Commitment**
   - Three clear service tiers
   - Specific deliverables listed
   - Clear pricing guidance

6. **Liking**
   - Story-driven About page
   - Authentic voice ("I don't write pointless grants")
   - Humor in appropriate places

### Brand Archetypes:

- **The Magician** (transformation, making impossible possible)
- **The Sage** (wisdom, teaching, understanding)
- Supporting: The Explorer (innovation, cutting-edge)

## 📝 Content Strategy

### Homepage Sections:
1. **Hero** - Clear value prop + authority
2. **Problem/Solution** - Pain points you solve
3. **Proof** - Your R&D system as credibility
4. **Credibility** - Your background (concise)
5. **Services** - Three clear offerings
6. **Blog Preview** - Content marketing
7. **CTA** - Clear next steps

### About Page:
- Journey from age 7 to now
- Why no PhD (reframed as strength)
- What makes you different
- Invitation to work together

### Blog Page:
- 9 post ideas ready to write
- Topics: Production AI, architecture, training, philosophy
- CTA: Connect on LinkedIn

### System Page:
- NOT for sale (R&D only)
- Architecture showcase
- Proof of expertise
- Link to GitHub

## 🎯 Next Steps After Launch

### Week 1:
1. Deploy website
2. Update LinkedIn profile with website link
3. Publish LinkedIn Post #1 (introduction)
4. Share website with close contacts for feedback

### Week 2-4:
1. Write first 2-3 blog posts
2. Share blog posts on LinkedIn
3. Add blog posts to website
4. Engage with comments

### Month 2-3:
1. Weekly blog posts
2. LinkedIn content strategy (from LINKEDIN_STRATEGY_KEITH_WILLIAMS.md)
3. Track leads/inquiries
4. Refine messaging based on feedback

## 🔧 Technical Notes

### Performance:
- Static HTML/CSS/JS (super fast)
- No dependencies, no build step
- Mobile responsive
- Works offline after first load

### SEO:
- Meta descriptions on all pages
- Semantic HTML
- Fast load times
- Mobile-friendly

### Browser Support:
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Uses CSS Grid/Flexbox (IE11 not supported, but who cares)

## 📊 Analytics (Optional)

Add Google Analytics or Plausible to track:
- Page views
- Time on site
- Popular content
- Traffic sources

Add before `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
```

## 🎨 Color Scheme

- Primary Blue: `#2563eb` (trust, professionalism)
- Secondary Slate: `#0f172a` (authority, depth)
- Accent Purple: `#8b5cf6` (innovation, creativity)
- Success Green: `#10b981` (achievement)
- Warning Orange: `#f59e0b` (energy, urgency)

## 💡 Tips

1. **Keep It Updated**: Add new blog posts regularly
2. **Track Leads**: Note which content drives inquiries
3. **A/B Test**: Try different headlines/CTAs
4. **Add Testimonials**: As you work with clients
5. **Case Studies**: Write up successful engagements (with permission)

## 🐛 Troubleshooting

**Links not working?**
- Check file paths are correct
- Ensure all files are in same directory
- Use relative paths (not absolute)

**Styles not loading?**
- Check `styles.css` is in same folder as HTML files
- View browser console for errors
- Hard refresh (Cmd+Shift+R on Mac)

**Email link not working?**
- Format: `mailto:your.email@example.com`
- Check for typos

## 📞 Support

If you need help customizing:
1. HTML/CSS basics: https://www.w3schools.com
2. Deployment: https://pages.github.com (GitHub Pages)
3. Custom domains: https://docs.netlify.com/domains-https/

---

**Built with:** HTML5, CSS3, Vanilla JavaScript (no frameworks needed)

**Philosophy:** Fast, simple, effective. Just like your approach to software.

🚀 **Now go ship it.**
