#!/usr/bin/env python3
"""
Optimized Review Runner
Captures screenshots, then runs token-efficient multi-agent pipeline
"""
import asyncio
import sys
from pathlib import Path

# Import existing screenshot capture
from responsive_review import capture_responsive_screenshots

# Import optimized pipeline
from optimized_review_pipeline import run_optimized_review


async def main():
    """
    Complete optimized review workflow:
    1. Capture screenshots (7 devices)
    2. Run optimized multi-agent pipeline
    3. Generate actionable reports
    """

    # Configuration
    url = "http://localhost:8080"
    output_dir = Path("qa_agents/screenshots/optimized_review")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 70)
    print("🚀 STARTING OPTIMIZED REVIEW PROCESS")
    print("=" * 70)
    print(f"\n📸 Step 1: Capturing screenshots from {url}")
    print(f"📁 Output directory: {output_dir}")

    # Cost estimation
    print("\n💰 COST ESTIMATE:")
    print("  - Screenshot capture: Free (Playwright)")
    print("  - Phase 1 Triage (7 devices): ~$0.03")
    print("  - Phase 2-3 Expert Review (3-5 devices): ~$0.10-0.15")
    print("  - Phase 4 Pattern Detection: ~$0.03")
    print("  - Phase 5 Report Generation: Free")
    print("  - TOTAL: ~$0.16-0.21 (vs $0.73 for parallel approach)")
    print("  - SAVINGS: 70-77%")

    # Confirm
    if "--auto-confirm" not in sys.argv:
        response = input("\nProceed with optimized review? (y/n): ")
        if response.lower() != 'y':
            print("Review cancelled.")
            return

    # Step 1: Capture screenshots
    print("\n" + "=" * 70)
    print("📸 CAPTURING SCREENSHOTS")
    print("=" * 70)

    try:
        screenshots = await capture_responsive_screenshots(
            url, str(output_dir)
        )
        print(f"\n✅ Screenshots captured: {len(screenshots)} devices")
    except Exception as e:
        print(f"\n❌ Screenshot capture failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Is the dev server running? (npm start)")
        print("  2. Can you access it? (curl http://localhost:8080)")
        print("  3. Is Playwright installed?")
        print("     (pip install playwright && playwright install)")
        sys.exit(1)

    # Step 2: Run optimized review
    print("\n" + "=" * 70)
    print("🤖 RUNNING OPTIMIZED MULTI-AGENT REVIEW")
    print("=" * 70)

    try:
        report_path = await run_optimized_review(output_dir, url)

        print("\n" + "=" * 70)
        print("✅ OPTIMIZED REVIEW COMPLETE")
        print("=" * 70)
        print("\n📖 Read the report:")
        print(f"  - Human: {report_path}")
        print(f"  - Machine: {report_path.with_suffix('.json')}")
        print("\n🎯 What to do next:")
        print("  1. Review critical issues (top priority)")
        print("  2. Check cross-device patterns (affects multiple devices)")
        print("  3. Fix universal issues first (widest impact)")
        print("  4. Iterate on mobile-specific issues (most users)")

    except Exception as e:
        print(f"\n❌ Review failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
Optimized Multi-Agent Review Runner

USAGE:
  python qa_agents/run_optimized_review.py [--auto-confirm]

OPTIONS:
  --auto-confirm    Skip confirmation prompts
  --help, -h        Show this help message

FEATURES:
  ✅ Token-optimized (70% savings vs parallel approach)
  ✅ Triage-based prioritization (skip similar devices)
  ✅ Sequential expert chain (experts build on each other)
  ✅ Cross-device pattern detection
  ✅ Actionable reports (human + machine readable)

COST:
  ~$0.16-0.21 per review (vs $0.73 for parallel)

OUTPUT:
  - qa_agents/screenshots/optimized_review/REVIEW-{timestamp}.md (human)
  - qa_agents/screenshots/optimized_review/REVIEW-{timestamp}.json (AI)

REQUIREMENTS:
  - Dev server running on http://localhost:8080
  - Playwright installed (playwright install)
  - OpenAI API key in environment
        """)
        sys.exit(0)

    asyncio.run(main())
