# GitHub Pages Setup Guide

## ✅ Completed Steps

1. **CNAME File Created**: `src/CNAME` contains `eaikw.com`
2. **.nojekyll File Added**: Prevents Jekyll processing on GitHub Pages
3. **Eleventy Config Updated**: 
   - Sitemap hostname set to `https://eaikw.com`
   - PathPrefix removed (custom domain doesn't need it)
   - CNAME and .nojekyll files copy to `_site/` on build
4. **Code Pushed to GitHub**: Force-pushed to `origin main`

## 🔧 GitHub Repository Settings

Now you need to configure GitHub Pages in your repository:

### 1. Enable GitHub Pages

1. Go to your repository: **https://github.com/kaw393939/eaikw**
2. Click **Settings** (top right)
3. In the left sidebar, click **Pages**
4. Under **Source**, select:
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/ (root)`
5. Click **Save**

### 2. Configure Custom Domain

In the same GitHub Pages settings:

1. Under **Custom domain**, enter: `eaikw.com`
2. Click **Save**
3. ✅ Check **Enforce HTTPS** (wait a few minutes for cert provisioning)

## 🌐 DNS Configuration

You need to configure your domain's DNS settings with your domain registrar:

### For Root Domain (eaikw.com)

Add these **A Records** pointing to GitHub's servers:

```
Type: A
Name: @
Value: 185.199.108.153

Type: A
Name: @
Value: 185.199.109.153

Type: A
Name: @
Value: 185.199.110.153

Type: A
Name: @
Value: 185.199.111.153
```

### For WWW Subdomain (optional)

Add a **CNAME Record**:

```
Type: CNAME
Name: www
Value: kaw393939.github.io
```

## ⏱️ Timeline

- **DNS Propagation**: 15 minutes to 48 hours (usually ~1 hour)
- **SSL Certificate**: 24-48 hours after DNS is configured
- **First Deployment**: 1-5 minutes after enabling Pages

## 🔍 Verification

### Check GitHub Pages Status

1. Go to **Settings > Pages**
2. Look for: "Your site is live at https://eaikw.com"
3. If you see errors, check the Actions tab for build logs

### Test the Site

Once DNS propagates:

```bash
# Check if DNS is configured
nslookup eaikw.com

# Check if site is live
curl -I https://eaikw.com
```

Expected result: HTTP 200 with redirect to HTTPS

### Test Homepage Content

Visit https://eaikw.com and verify:

- ✅ CSS loads properly (styled content, not raw HTML)
- ✅ Hero section displays with macro-economic messaging
- ✅ Two initiatives (NJIT + Project Elevate) are visible
- ✅ January 2026 pilot CTA is present
- ✅ Navigation works (About, Events, Blog, Course links)

## 🚨 Troubleshooting

### "Domain is not properly configured"

- **Wait**: DNS can take up to 48 hours
- **Verify DNS**: Use `nslookup eaikw.com` to check A records
- **Check NS Records**: Ensure nameservers point to your registrar

### "404 - Page Not Found"

- **Check Branch**: Ensure Pages is deploying from `main` branch
- **Check Folder**: Should be `/ (root)`, not `/docs`
- **Rebuild**: Push an empty commit to trigger rebuild:
  ```bash
  git commit --allow-empty -m "Trigger Pages rebuild"
  git push origin main
  ```

### "CSS Not Loading"

- **Check Browser Console**: Look for 404 errors on CSS files
- **Clear Cache**: Hard refresh (Cmd+Shift+R on Mac)
- **Verify Build**: Check that `_site/assets/css/main.css` exists locally

### "SSL Certificate Errors"

- **Wait**: Can take 24-48 hours after DNS configuration
- **Re-save Domain**: Remove and re-add custom domain in Settings
- **Check CAA Records**: Some registrars block Let's Encrypt by default

## 📱 Next Steps After Deployment

1. **Test on Multiple Devices**: Mobile, tablet, desktop
2. **Check Performance**: Run Lighthouse audit
3. **Verify SEO**: Check meta tags, sitemap.xml, robots.txt
4. **Monitor Analytics**: Set up Google Analytics or similar
5. **Share the Link**: Post on LinkedIn with #EverydayAI

## 🎯 Launch Checklist

- [ ] GitHub Pages enabled (Settings > Pages)
- [ ] Custom domain configured (eaikw.com)
- [ ] DNS A records added at domain registrar
- [ ] HTTPS enabled (may take 24-48 hours)
- [ ] Site accessible at https://eaikw.com
- [ ] Homepage displays correctly with CSS
- [ ] Navigation links work
- [ ] Mobile responsive
- [ ] Record LinkedIn video announcing launch
- [ ] Post article with link to site
- [ ] Email 900+ LinkedIn connections
- [ ] Start recruiting January pilot partners

## 📞 Support

- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **Custom Domain Setup**: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

---

**Repository**: https://github.com/kaw393939/eaikw  
**Target URL**: https://eaikw.com  
**Build Tool**: Eleventy v2.0.1  
**Deploy Method**: GitHub Pages (main branch, root folder)
