#!/usr/bin/env python3
"""
Quick Homepage QA Check
Captures homepage screenshot and runs basic validation
"""
import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright


async def quick_homepage_check():
    """Run quick visual check on homepage"""

    url = "http://localhost:8080/"
    output_dir = Path("qa_agents/screenshots/quick-check")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 70)
    print("🔍 QUICK HOMEPAGE QA CHECK")
    print("=" * 70)
    print(f"\n📸 Capturing screenshots from {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Test key device sizes
        devices = [
            ("Mobile", 375, 812),
            ("Desktop", 1920, 1080)
        ]

        for device_name, width, height in devices:
            print(f"\n📱 Testing {device_name} ({width}x{height})...")

            await page.set_viewport_size({"width": width, "height": height})
            await page.goto(url, wait_until="networkidle")
            await asyncio.sleep(1)

            # Take screenshot
            screenshot_path = output_dir / f"homepage_{device_name.lower()}_{width}x{height}.png"
            await page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"   ✓ Screenshot saved: {screenshot_path}")

            # Check for common issues
            issues = []

            # Check if hero is visible
            hero = await page.query_selector(".hero-explorer, .hero-wrapper, [data-section-name='hero']")
            if hero:
                box = await hero.bounding_box()
                if box and box['y'] > height:
                    issues.append(f"⚠️  Hero section is below the fold (starts at {box['y']}px)")

            # Check for CSS load
            css_loaded = await page.evaluate("""
                () => {
                    const style = window.getComputedStyle(document.body);
                    return style.fontFamily !== '' && style.fontSize !== '16px';
                }
            """)
            if not css_loaded:
                issues.append("❌ CSS may not be loaded properly")

            # Check for responsive meta tag
            has_viewport = await page.evaluate("""
                () => {
                    const viewport = document.querySelector('meta[name="viewport"]');
                    return viewport !== null;
                }
            """)
            if not has_viewport:
                issues.append("❌ Missing viewport meta tag")

            # Report issues
            if issues:
                print(f"\n   🚨 Issues found on {device_name}:")
                for issue in issues:
                    print(f"      {issue}")
            else:
                print(f"   ✅ No obvious issues detected")

        await browser.close()

    print("\n" + "=" * 70)
    print("✅ Quick check complete!")
    print(f"📁 Screenshots saved to: {output_dir}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(quick_homepage_check())
