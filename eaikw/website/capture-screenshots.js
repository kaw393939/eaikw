#!/usr/bin/env node

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Define viewport sizes to test
const viewports = [
    { name: 'mobile-small', width: 375, height: 667, description: 'iPhone SE' },
    { name: 'mobile-large', width: 414, height: 896, description: 'iPhone Pro Max' },
    { name: 'tablet', width: 768, height: 1024, description: 'iPad Portrait' },
    { name: 'tablet-landscape', width: 1024, height: 768, description: 'iPad Landscape' },
    { name: 'desktop-small', width: 1280, height: 800, description: 'Small Desktop' },
    { name: 'desktop-large', width: 1920, height: 1080, description: 'Large Desktop' },
];

async function captureScreenshots() {
    console.log('🎯 Starting screenshot capture...\n');
    
    // Create screenshots directory
    const screenshotsDir = path.join(__dirname, 'screenshots');
    if (!fs.existsSync(screenshotsDir)) {
        fs.mkdirSync(screenshotsDir);
    }

    const browser = await puppeteer.launch({
        headless: true,
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    });

    const page = await browser.newPage();
    const url = 'http://localhost:8080';

    for (const viewport of viewports) {
        console.log(`📱 Capturing ${viewport.name} (${viewport.width}x${viewport.height}) - ${viewport.description}`);
        
        await page.setViewport({
            width: viewport.width,
            height: viewport.height,
            deviceScaleFactor: 2, // Retina/High-DPI
        });

        await page.goto(url, { waitUntil: 'networkidle2' });
        
        // Wait a bit for any animations
        await page.waitForTimeout(500);

        // Full page screenshot
        const screenshotPath = path.join(screenshotsDir, `${viewport.name}-full.png`);
        await page.screenshot({
            path: screenshotPath,
            fullPage: true,
        });
        
        console.log(`   ✅ Saved: ${screenshotPath}`);

        // Capture just the hero section
        const heroPath = path.join(screenshotsDir, `${viewport.name}-hero.png`);
        const hero = await page.$('.hero');
        if (hero) {
            await hero.screenshot({ path: heroPath });
            console.log(`   ✅ Saved hero: ${heroPath}`);
        }
    }

    await browser.close();
    
    console.log('\n✨ Screenshot capture complete!');
    console.log(`📂 Screenshots saved to: ${screenshotsDir}`);
    
    // Generate HTML report
    generateReport(screenshotsDir, viewports);
}

function generateReport(screenshotsDir, viewports) {
    const reportPath = path.join(screenshotsDir, 'index.html');
    
    let html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Design Screenshots</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            background: #f5f5f5;
        }
        h1 { color: #1d4035; }
        .viewport-section {
            background: white;
            padding: 2rem;
            margin: 2rem 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .viewport-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #e8e4dc;
        }
        .viewport-name {
            font-size: 1.5rem;
            font-weight: 700;
            color: #2d2d2d;
        }
        .viewport-size {
            color: #5a5a5a;
            font-size: 0.9rem;
        }
        .screenshot-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1rem;
        }
        .screenshot-container {
            background: #fafafa;
            padding: 1rem;
            border-radius: 4px;
        }
        .screenshot-label {
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #333;
        }
        img {
            width: 100%;
            border: 1px solid #ddd;
            border-radius: 4px;
            display: block;
        }
        .notes {
            background: #fff3cd;
            padding: 1rem;
            border-radius: 4px;
            margin: 2rem 0;
            border-left: 4px solid #ffc107;
        }
    </style>
</head>
<body>
    <h1>🎨 Responsive Design Screenshots</h1>
    <p>Generated: ${new Date().toLocaleString()}</p>
    
    <div class="notes">
        <strong>📋 Analysis Checklist:</strong>
        <ul>
            <li>Check navigation usability at each size</li>
            <li>Verify text readability (font sizes, line lengths)</li>
            <li>Ensure buttons/CTAs are easily tappable on mobile (min 44x44px)</li>
            <li>Check image scaling and aspect ratios</li>
            <li>Verify spacing and whitespace at different sizes</li>
            <li>Look for horizontal scrolling issues</li>
            <li>Check that important content is above the fold</li>
        </ul>
    </div>
`;

    viewports.forEach(viewport => {
        html += `
    <div class="viewport-section">
        <div class="viewport-header">
            <div>
                <div class="viewport-name">${viewport.description}</div>
                <div class="viewport-size">${viewport.width}×${viewport.height}px</div>
            </div>
        </div>
        <div class="screenshot-grid">
            <div class="screenshot-container">
                <div class="screenshot-label">Full Page</div>
                <img src="${viewport.name}-full.png" alt="${viewport.description} - Full Page" loading="lazy">
            </div>
            <div class="screenshot-container">
                <div class="screenshot-label">Hero Section</div>
                <img src="${viewport.name}-hero.png" alt="${viewport.description} - Hero" loading="lazy">
            </div>
        </div>
    </div>
`;
    });

    html += `
</body>
</html>`;

    fs.writeFileSync(reportPath, html);
    console.log(`📄 HTML report generated: ${reportPath}`);
}

// Run the capture
captureScreenshots().catch(console.error);
