"""
Responsive Multi-Device UX Review System
Takes screenshots at multiple viewport sizes and runs expert consensus review
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright
from consensus_review import ConsensusReviewSystem


# Device configurations matching real-world usage
DEVICE_CONFIGS = {
    "mobile-portrait": {
        "width": 375,
        "height": 812,
        "device_scale_factor": 3,
        "description": "iPhone 13/14 Pro",
        "priority": "critical"
    },
    "mobile-landscape": {
        "width": 812,
        "height": 375,
        "device_scale_factor": 3,
        "description": "iPhone landscape",
        "priority": "high"
    },
    "tablet-portrait": {
        "width": 768,
        "height": 1024,
        "device_scale_factor": 2,
        "description": "iPad",
        "priority": "high"
    },
    "tablet-landscape": {
        "width": 1024,
        "height": 768,
        "device_scale_factor": 2,
        "description": "iPad landscape",
        "priority": "high"
    },
    "laptop": {
        "width": 1440,
        "height": 900,
        "device_scale_factor": 2,
        "description": "MacBook Pro 14\"",
        "priority": "critical"
    },
    "desktop": {
        "width": 1920,
        "height": 1080,
        "device_scale_factor": 1,
        "description": "Full HD desktop",
        "priority": "critical"
    },
    "wide-desktop": {
        "width": 2560,
        "height": 1440,
        "device_scale_factor": 1,
        "description": "2K wide desktop",
        "priority": "medium"
    }
}


class ResponsiveReviewSystem:
    """Captures and reviews UI across multiple device sizes"""

    def __init__(self, base_url: str, output_dir: str):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.consensus_system = ConsensusReviewSystem()

    async def capture_device_screenshot(
        self,
        page,
        device_name: str,
        config: dict,
        section_name: str = "hero"
    ) -> Path:
        """Capture screenshot at specific device size"""

        # Set viewport
        await page.set_viewport_size({
            "width": config["width"],
            "height": config["height"]
        })

        # Wait for content to stabilize
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(1)  # Allow animations to settle

        # Take screenshot
        filename = f"{section_name}_{device_name}_{config['width']}x{config['height']}.png"
        screenshot_path = self.output_dir / filename

        # Screenshot the hero section (or full page if hero not found)
        try:
            hero_element = await page.query_selector('[data-section-name="hero"]')
            if hero_element:
                await hero_element.screenshot(path=str(screenshot_path))
            else:
                # Fallback to full page
                await page.screenshot(path=str(screenshot_path), full_page=False)
        except Exception as e:
            print(f"⚠️  Error capturing {device_name}: {e}")
            return None

        print(f"📸 Captured {device_name}: {config['description']} ({config['width']}×{config['height']})")
        return screenshot_path

    async def capture_all_devices(self, section_name: str = "hero") -> dict:
        """Capture screenshots across all device configurations"""

        screenshots = {}

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            # Navigate to page
            await page.goto(self.base_url)

            # Capture each device size
            for device_name, config in DEVICE_CONFIGS.items():
                screenshot_path = await self.capture_device_screenshot(
                    page,
                    device_name,
                    config,
                    section_name
                )

                if screenshot_path:
                    screenshots[device_name] = {
                        "path": str(screenshot_path),
                        "config": config,
                        "priority": config["priority"]
                    }

            await browser.close()

        return screenshots

    async def review_device_screenshots(self, screenshots: dict) -> dict:
        """Run expert consensus review on each device screenshot"""

        device_reviews = {}

        for device_name, info in screenshots.items():
            print(f"\n🔍 Reviewing {device_name} ({info['config']['description']})...")

            # Run parallel expert reviews
            reviews = await self.consensus_system.run_parallel_reviews(
                screenshot_path=info['path'],
                section_name=f"hero-{device_name}"
            )

            # Aggregate findings
            aggregated = self.consensus_system.aggregate_findings(reviews)

            device_reviews[device_name] = {
                "device_info": info['config'],
                "priority": info['priority'],
                "reviews": reviews,
                "aggregated": aggregated
            }

        return device_reviews

    def identify_responsive_issues(self, device_reviews: dict) -> list:
        """Cross-analyze device reviews to find responsive-specific issues"""

        responsive_issues = []

        # Compare mobile vs desktop
        mobile_issues = set()
        desktop_issues = set()

        for device_name, review_data in device_reviews.items():
            issues = [
                issue['issue']
                for issue in review_data['aggregated'].get('critical_issues', [])
            ]

            if 'mobile' in device_name:
                mobile_issues.update(issues)
            elif 'desktop' in device_name or 'laptop' in device_name:
                desktop_issues.update(issues)

        # Mobile-only issues
        mobile_only = mobile_issues - desktop_issues
        if mobile_only:
            responsive_issues.append({
                "type": "mobile_only_issues",
                "severity": "critical",
                "count": len(mobile_only),
                "issues": list(mobile_only)
            })

        # Desktop-only issues
        desktop_only = desktop_issues - mobile_issues
        if desktop_only:
            responsive_issues.append({
                "type": "desktop_only_issues",
                "severity": "major",
                "count": len(desktop_only),
                "issues": list(desktop_only)
            })

        return responsive_issues

    def generate_responsive_report(
        self,
        device_reviews: dict,
        responsive_issues: list
    ) -> str:
        """Generate comprehensive responsive design report"""

        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("RESPONSIVE MULTI-DEVICE UX REVIEW")
        report_lines.append("=" * 80)
        report_lines.append(f"Review Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Devices Tested: {len(device_reviews)}")
        report_lines.append("")

        # Device-by-device breakdown
        for device_name, review_data in device_reviews.items():
            config = review_data['device_info']
            aggregated = review_data['aggregated']

            report_lines.append("-" * 80)
            report_lines.append(f"📱 {device_name.upper()}")
            report_lines.append(f"   Device: {config['description']}")
            report_lines.append(f"   Resolution: {config['width']}×{config['height']}")
            report_lines.append(f"   Priority: {review_data['priority'].upper()}")
            report_lines.append("")

            # Critical issues for this device
            critical = aggregated.get('critical_issues', [])
            if critical:
                report_lines.append(f"   🔴 CRITICAL ISSUES: {len(critical)}")
                for idx, issue_data in enumerate(critical[:10], 1):  # Top 10
                    issue = issue_data['issue']
                    consensus = issue_data['consensus']
                    experts = ", ".join(issue_data['experts'])

                    report_lines.append(f"   {idx}. {issue}")
                    report_lines.append(f"      📊 {consensus}% consensus ({experts})")
                    report_lines.append("")

            # Device-specific stats
            expert_totals = aggregated.get('expert_breakdown', {})
            report_lines.append(f"   📊 Expert Findings:")
            for expert, counts in expert_totals.items():
                total = counts['critical'] + counts['major'] + counts['minor']
                report_lines.append(
                    f"      {expert}: {counts['critical']} critical, "
                    f"{counts['major']} major, {counts['minor']} minor (Total: {total})"
                )
            report_lines.append("")

        # Cross-device responsive issues
        if responsive_issues:
            report_lines.append("=" * 80)
            report_lines.append("🔄 RESPONSIVE DESIGN ISSUES")
            report_lines.append("=" * 80)
            report_lines.append("")

            for issue_group in responsive_issues:
                report_lines.append(f"📍 {issue_group['type'].replace('_', ' ').upper()}")
                report_lines.append(f"   Severity: {issue_group['severity']}")
                report_lines.append(f"   Count: {issue_group['count']}")
                report_lines.append("")

                for issue in issue_group['issues'][:10]:  # Top 10
                    report_lines.append(f"   • {issue}")
                report_lines.append("")

        # Summary
        report_lines.append("=" * 80)
        report_lines.append("📊 SUMMARY")
        report_lines.append("=" * 80)

        # Count total issues across all devices
        total_critical = sum(
            len(r['aggregated'].get('critical_issues', []))
            for r in device_reviews.values()
        )
        total_major = sum(
            len(r['aggregated'].get('major_issues', []))
            for r in device_reviews.values()
        )

        report_lines.append(f"Total Devices Tested: {len(device_reviews)}")
        report_lines.append(f"Total Critical Issues: {total_critical}")
        report_lines.append(f"Total Major Issues: {total_major}")
        report_lines.append(f"Responsive-Specific Issues: {len(responsive_issues)}")
        report_lines.append("")

        # Priority recommendations
        report_lines.append("🎯 PRIORITY FIXES:")
        report_lines.append("1. Fix critical issues on mobile-portrait (375×812) first")
        report_lines.append("2. Then fix desktop/laptop (1440×900, 1920×1080)")
        report_lines.append("3. Verify fixes work across all breakpoints")
        report_lines.append("4. Test on real devices, not just emulators")
        report_lines.append("")

        return "\n".join(report_lines)

    async def run_full_responsive_review(self, section_name: str = "hero"):
        """Complete responsive review workflow"""

        print("=" * 80)
        print("🎯 RESPONSIVE MULTI-DEVICE UX REVIEW")
        print("=" * 80)
        print(f"URL: {self.base_url}")
        print(f"Output: {self.output_dir}")
        print(f"Devices: {len(DEVICE_CONFIGS)}")
        print("")

        # Step 1: Capture screenshots
        print("📸 STEP 1: Capturing screenshots across all devices...")
        screenshots = await self.capture_all_devices(section_name)
        print(f"✅ Captured {len(screenshots)} device screenshots")
        print("")

        # Step 2: Review each device
        print("🔍 STEP 2: Running expert consensus review on each device...")
        device_reviews = await self.review_device_screenshots(screenshots)
        print("✅ Completed all device reviews")
        print("")

        # Step 3: Identify responsive issues
        print("🔄 STEP 3: Analyzing cross-device responsive issues...")
        responsive_issues = self.identify_responsive_issues(device_reviews)
        print(f"✅ Identified {len(responsive_issues)} responsive issue groups")
        print("")

        # Step 4: Generate report
        print("📄 STEP 4: Generating comprehensive report...")
        report = self.generate_responsive_report(device_reviews, responsive_issues)

        # Save report
        report_path = self.output_dir / "RESPONSIVE-REVIEW-REPORT.txt"
        with open(report_path, 'w') as f:
            f.write(report)

        # Save JSON data
        json_path = self.output_dir / "RESPONSIVE-REVIEW-DATA.json"
        with open(json_path, 'w') as f:
            # Convert paths to strings for JSON serialization
            json_data = {
                "timestamp": datetime.now().isoformat(),
                "device_reviews": {
                    device: {
                        "config": info['device_info'],
                        "priority": info['priority'],
                        "aggregated": info['aggregated']
                    }
                    for device, info in device_reviews.items()
                },
                "responsive_issues": responsive_issues
            }
            json.dump(json_data, f, indent=2, default=str)

        print(f"✅ Reports saved:")
        print(f"   • {report_path}")
        print(f"   • {json_path}")
        print("")
        print("=" * 80)
        print("🎉 RESPONSIVE REVIEW COMPLETE!")
        print("=" * 80)

        return {
            "screenshots": screenshots,
            "device_reviews": device_reviews,
            "responsive_issues": responsive_issues,
            "report": report
        }


async def main():
    """Run responsive review from command line"""
    import sys

    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080/is117_ai_test_practice/"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "qa_agents/screenshots/responsive-review"

    system = ResponsiveReviewSystem(base_url, output_dir)
    await system.run_full_responsive_review()


if __name__ == "__main__":
    asyncio.run(main())
