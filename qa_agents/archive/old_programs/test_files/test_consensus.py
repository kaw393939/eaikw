#!/usr/bin/env python3
"""Test single screenshot with multi-expert review"""

import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

from qa_agents.consensus_review import ConsensusReviewSystem


async def main():
    load_dotenv()

    # Test with just hero screenshot
    hero_screenshot = "qa_agents/screenshots/homepage-review/hero_desktop.png"

    if not Path(hero_screenshot).exists():
        print(f"❌ Screenshot not found: {hero_screenshot}")
        return 1

    print("🧪 Testing multi-expert review on hero section...")

    system = ConsensusReviewSystem()

    try:
        reviews = await system.run_parallel_reviews(
            hero_screenshot,
            "hero"
        )

        print("\n✅ Reviews completed!")
        for expert, review in reviews.items():
            if review:
                print(f"\n👤 {expert}:")
                print(f"   Confidence: {review.confidence_score}%")
                print(f"   Critical: {len(review.critical_issues)}")
                print(f"   Major: {len(review.major_issues)}")
                print(f"   Minor: {len(review.minor_issues)}")

        return 0

    except Exception as e:
        print(f"\n❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
