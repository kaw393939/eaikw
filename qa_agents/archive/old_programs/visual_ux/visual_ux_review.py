#!/usr/bin/env python3
"""
Visual UX Review Gate
Analyzes built website with GPT-4o Vision using persona-based reviews
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import Runner
from qa_agents.visual_ux_agents import get_agent_for_persona, VisualUXReview
from qa_agents.screenshot_utils import capture_all_viewports_sync
from qa_agents.config import OPENAI_API_KEY
from qa_agents.server_manager import ServerManager
from qa_agents.reliability import (
    estimate_cost,
    print_cost_estimate,
    format_troubleshooting_message,
    validate_all_screenshots
)


def format_review_output(review: VisualUXReview) -> str:
    """Format a single review for readable output"""
    output = []
    output.append(f"\n{'=' * 70}")
    output.append(f"🎭 Persona: {review.persona.upper()}")
    output.append(f"📱 Viewport: {review.viewport.upper()}")
    output.append(f"⭐ Rating: {review.recommendation.upper()}")
    output.append(f"{'=' * 70}\n")

    output.append(f"Overall Impression:\n{review.overall_impression}\n")

    if review.specific_observations:
        output.append("🔍 Specific Observations:")
        for obs in review.specific_observations:
            output.append(f"  • {obs}")
        output.append("")

    if review.usability_concerns:
        output.append("⚠️  Usability Concerns:")
        for concern in review.usability_concerns:
            output.append(f"  • {concern}")
        output.append("")

    if review.accessibility_notes:
        output.append("♿ Accessibility Notes:")
        for note in review.accessibility_notes:
            output.append(f"  • {note}")
        output.append("")

    if review.design_feedback:
        output.append("🎨 Design Feedback:")
        for feedback in review.design_feedback:
            output.append(f"  • {feedback}")
        output.append("")

    output.append(f"💭 Reasoning:\n{review.reasoning}\n")

    return "\n".join(output)


def run_visual_ux_review(
    site_url: str = None,
    personas: list[str] = None,
    viewports: list[str] = None,
    save_screenshots: bool = True,
    use_server_manager: bool = True
) -> dict:
    """
    Run visual UX review with GPT-4o Vision

    Args:
        site_url: URL of the built site (None = auto-start server)
        personas: List of personas to use (default: all)
        viewports: List of viewports to test (default: all)
        save_screenshots: Whether to save screenshot files
        use_server_manager: Auto-start server if True

    Returns:
        dict with reviews and overall assessment
    """

    if personas is None:
        personas = ["first_year_student", "instructor"]

    if viewports is None:
        viewports = ["desktop", "tablet", "mobile"]

    print("\n" + "=" * 70)
    print("🎨 VISUAL UX REVIEW - GPT-4o Vision Analysis")
    print("=" * 70)

    # Estimate and display cost
    num_analyses = len(personas) * len(viewports)
    cost_info = estimate_cost(num_analyses, detail_level="high")
    print_cost_estimate(cost_info)

    # Server management
    server = None
    if use_server_manager and site_url is None:
        print("\n🔧 Starting server...")
        try:
            server = ServerManager()
            site_url = server.start_server(kill_conflicts=True)
        except Exception as e:
            error_msg = format_troubleshooting_message(
                e,
                {"url": site_url or "unknown", "port": "8080-8090"}
            )
            print(error_msg)
            sys.exit(1)

    # Use provided URL or default
    if site_url is None:
        site_url = "http://localhost:8082"

    # Step 1: Capture screenshots
    print(f"\n📸 Capturing screenshots from {site_url}...")
    output_dir = "qa_agents/screenshots" if save_screenshots else None

    try:
        screenshots = capture_all_viewports_sync(site_url, output_dir)
        print(f"   ✅ Captured {len(screenshots)} screenshots")
        if save_screenshots:
            print(f"   💾 Saved to {output_dir}/")

        # Validate screenshots
        all_valid, errors = validate_all_screenshots(screenshots)
        if not all_valid:
            print("   ⚠️  Screenshot validation warnings:")
            for error in errors:
                print(f"      - {error}")

    except Exception as e:
        error_msg = format_troubleshooting_message(
            e,
            {"url": site_url,
             "port": site_url.split(":")[-1] if ":" in site_url else "unknown"}
        )
        print(error_msg)
        if server:
            server.stop_server()
        sys.exit(1)

    # Step 2: Run visual analysis with each persona
    all_reviews = []
    total_cost = 0.0

    for persona in personas:
        agent = get_agent_for_persona(persona)

        for viewport in viewports:
            if viewport not in screenshots:
                continue

            screenshot = screenshots[viewport]
            print(
                f"\n🤔 Analyzing with {persona} "
                f"at {viewport} ({screenshot['dimensions']['width']}x"
                f"{screenshot['dimensions']['height']})..."
            )

            try:
                # Create prompt with image using proper format
                prompt_text = f"""Analyze this screenshot of the course website
hero section. Provide your honest, detailed UX review following your
persona's perspective and the think-aloud protocol.

Screenshot viewport: {viewport}
({screenshot['dimensions']['width']}x{screenshot['dimensions']['height']})

Think aloud as you examine the image, sharing your immediate reactions
and observations."""

                # Run agent with vision input using Responses API format
                import asyncio
                result = asyncio.run(Runner.run(
                    agent,
                    [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_image",
                                    "detail": "high",
                                    "image_url": (
                                        f"data:image/png;base64,"
                                        f"{screenshot['base64']}"
                                    ),
                                }
                            ],
                        },
                        {
                            "role": "user",
                            "content": prompt_text,
                        },
                    ],
                ))

                review = result.final_output
                all_reviews.append(review)

                # Print formatted review
                print(format_review_output(review))

                # Estimate cost (GPT-4o vision: ~$10/1M input tokens)
                # Rough estimate: 1 image ≈ 765 tokens, prompt ≈ 500 tokens
                estimated_tokens = 1265
                estimated_cost = (estimated_tokens / 1_000_000) * 10
                total_cost += estimated_cost

            except Exception as e:
                print(f"   ❌ Analysis failed: {e}")
                continue

    # Step 3: Generate overall assessment
    print("\n" + "=" * 70)
    print("📊 OVERALL ASSESSMENT")
    print("=" * 70)

    # Count recommendations
    excellent = sum(1 for r in all_reviews if r.recommendation == "excellent")
    good = sum(1 for r in all_reviews if r.recommendation == "good")
    needs_improvement = sum(
        1 for r in all_reviews if r.recommendation == "needs_improvement"
    )
    poor = sum(1 for r in all_reviews if r.recommendation == "poor")

    print(f"\n📈 Results ({len(all_reviews)} total reviews):")
    print(f"   ⭐⭐⭐⭐ Excellent: {excellent}")
    print(f"   ⭐⭐⭐   Good: {good}")
    print(f"   ⚠️     Needs Improvement: {needs_improvement}")
    print(f"   ❌     Poor: {poor}")

    # Determine overall verdict
    if poor > 0 or needs_improvement >= len(all_reviews) / 2:
        verdict = "NEEDS_IMPROVEMENT"
        print(f"\n{'=' * 70}")
        print("⚠️  VISUAL UX GATE: NEEDS IMPROVEMENT")
        print("=" * 70)
        print(
            "\nSignificant UX concerns identified. "
            "Review feedback above and address issues."
        )
    elif excellent >= len(all_reviews) / 2:
        verdict = "EXCELLENT"
        print(f"\n{'=' * 70}")
        print("✅ VISUAL UX GATE: EXCELLENT")
        print("=" * 70)
    else:
        verdict = "GOOD"
        print(f"\n{'=' * 70}")
        print("✅ VISUAL UX GATE: GOOD")
        print("=" * 70)

    print(f"\n💰 Estimated cost: ${total_cost:.4f}")

    # Cleanup server if we started it
    if server:
        server.stop_server()

    return {
        "verdict": verdict,
        "reviews": all_reviews,
        "cost": total_cost,
        "screenshots": screenshots
    }


if __name__ == "__main__":
    # Check environment
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not set in .env file")
        sys.exit(1)

    # Run review with auto server management
    # The ServerManager will:
    # 1. Find an available port (8080-8090)
    # 2. Kill any conflicting processes
    # 3. Start HTTP server
    # 4. Validate server is responding
    # 5. Clean up on exit
    result = run_visual_ux_review(
        site_url=None,  # Auto-start server
        personas=["first_year_student", "instructor"],
        viewports=["desktop", "tablet", "mobile"],
        use_server_manager=True
    )

    # Exit with appropriate code
    if result["verdict"] == "NEEDS_IMPROVEMENT":
        sys.exit(1)
    else:
        sys.exit(0)
