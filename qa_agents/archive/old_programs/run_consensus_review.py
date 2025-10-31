#!/usr/bin/env python3
"""
Multi-Expert Consensus UX Review
Run comprehensive review with 7 specialized Fortune 100-level experts
"""

import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

from qa_agents.consensus_review import run_consensus_review


async def main():
    load_dotenv()

    # Get screenshots from the most recent review
    screenshot_dir = Path("qa_agents/screenshots/homepage-review")

    if not screenshot_dir.exists():
        print("❌ No screenshots found. Run targeted_review.py first.")
        return 1

    # Find all desktop screenshots
    screenshots = {}
    for img in screenshot_dir.glob("*_desktop.png"):
        section_name = img.stem.replace("_desktop", "")
        screenshots[section_name] = str(img)

    if not screenshots:
        print("❌ No desktop screenshots found.")
        return 1

    print(f"\n🎯 MULTI-EXPERT CONSENSUS REVIEW")
    print(f"="*70)
    print(f"📸 Found {len(screenshots)} screenshots")
    print(f"👥 Deploying 7 specialized experts:")
    print(f"   1. Typography & Readability Specialist")
    print(f"   2. Layout & Spacing Engineer")
    print(f"   3. Color & Contrast Specialist")
    print(f"   4. Visual Hierarchy Specialist")
    print(f"   5. Accessibility & WCAG Auditor")
    print(f"   6. Conversion & Marketing Strategist")
    print(f"   7. Brand & Style Guide Guardian")
    print(f"="*70)

    # Estimate cost
    total_reviews = len(screenshots) * 7
    estimated_cost = total_reviews * 0.015  # Rough estimate per review
    print(f"\n💰 Estimated cost: ~${estimated_cost:.2f}")
    print(f"   ({total_reviews} reviews × ~$0.015 each)")

    response = input("\n   Continue? (y/n): ")
    if response.lower() != 'y':
        print("\n❌ Cancelled")
        return 0

    # Run the consensus review
    output_file = str(screenshot_dir / "CONSENSUS-REPORT.txt")

    try:
        report = await run_consensus_review(screenshots, output_file)
        print(report)
        print(f"\n✅ Multi-expert review complete!")
        print(f"📊 Check the consensus report for aggregated findings")
        return 0

    except Exception as e:
        print(f"\n❌ Review failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
