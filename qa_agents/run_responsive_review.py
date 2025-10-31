#!/usr/bin/env python3
"""
Run Responsive Multi-Device UX Review
Captures and analyzes UI across 7 device sizes with 7 expert reviewers = 49 total reviews
"""

import asyncio
import sys
from responsive_review import ResponsiveReviewSystem


async def main():
    print("=" * 80)
    print("🎯 RESPONSIVE MULTI-DEVICE UX REVIEW")
    print("7 Devices × 7 Experts = 49 Comprehensive Reviews")
    print("=" * 80)
    print("")

    # Configuration
    base_url = "http://localhost:8080/"
    output_dir = "qa_agents/screenshots/responsive-review"

    print(f"URL: {base_url}")
    print(f"Output Directory: {output_dir}")
    print("")
    print("DEVICES TO TEST:")
    print("  1. 📱 iPhone Portrait (375×812)")
    print("  2. 📱 iPhone Landscape (812×375)")
    print("  3. 📱 iPad Portrait (768×1024)")
    print("  4. 📱 iPad Landscape (1024×768)")
    print("  5. 💻 MacBook Pro (1440×900)")
    print("  6. 🖥️  Full HD Desktop (1920×1080)")
    print("  7. 🖥️  2K Wide Desktop (2560×1440)")
    print("")
    print("EXPERT REVIEWERS:")
    print("  1. Typography & Readability")
    print("  2. Layout & Spacing")
    print("  3. Contrast & WCAG")
    print("  4. Visual Hierarchy")
    print("  5. Accessibility")
    print("  6. Conversion Optimization")
    print("  7. Brand Consistency")
    print("")

    # Cost estimate
    total_reviews = 7 * 7  # 7 devices × 7 experts
    cost_per_review = 0.015  # GPT-5 estimate
    estimated_cost = total_reviews * cost_per_review

    print(f"💰 Estimated Cost: ${estimated_cost:.2f} ({total_reviews} reviews × ${cost_per_review} each)")
    print("")

    # Confirmation
    confirm = input("🚀 Ready to start? This will take 5-10 minutes. (y/n): ")
    if confirm.lower() != 'y':
        print("❌ Canceled")
        return

    print("")

    # Run the review
    system = ResponsiveReviewSystem(base_url, output_dir)
    results = await system.run_full_responsive_review()

    print("")
    print("=" * 80)
    print("✅ REVIEW COMPLETE!")
    print("=" * 80)
    print(f"📄 Report: {output_dir}/RESPONSIVE-REVIEW-REPORT.txt")
    print(f"📊 Data: {output_dir}/RESPONSIVE-REVIEW-DATA.json")
    print(f"📸 Screenshots: {output_dir}/*.png")
    print("")
    print("🎯 KEY FINDINGS:")

    # Show top issues
    responsive_issues = results['responsive_issues']
    if responsive_issues:
        for issue_group in responsive_issues[:3]:
            print(f"   • {issue_group['type'].replace('_', ' ').title()}: {issue_group['count']} issues")

    # Show device with most issues
    device_reviews = results['device_reviews']
    max_issues_device = max(
        device_reviews.items(),
        key=lambda x: len(x[1]['aggregated'].get('critical_issues', []))
    )
    device_name, device_data = max_issues_device
    critical_count = len(device_data['aggregated'].get('critical_issues', []))

    print(f"   • Most Issues: {device_name} ({critical_count} critical)")
    print("")
    print("📖 Read the full report for detailed findings and recommendations.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ Review interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
