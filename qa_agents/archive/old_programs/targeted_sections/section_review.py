#!/usr/bin/env python3
"""
Section-based visual UX review
Analyzes page sections with targeted personas
"""

import sys
import asyncio
from agents import Runner
from dotenv import load_dotenv

from qa_agents.section_capture import capture_page_sections_sync
from qa_agents.section_personas import (
    get_section_prompt,
    format_section_results,
    SECTION_PERSONAS
)
from qa_agents.visual_ux_agents import create_section_reviewer
from qa_agents.server_manager import ServerManager
from qa_agents.reliability import (
    estimate_cost,
    print_cost_estimate,
    format_troubleshooting_message
)


def run_section_review(
    url: str,
    viewport_name: str = "desktop",
    sections: list[str] = None,
    use_server_manager: bool = True,
    output_dir: str | None = None
) -> int:
    """
    Run section-based visual UX review

    Args:
        url: URL to review (or path if using server manager)
        viewport_name: One of 'desktop', 'tablet', 'mobile'
        sections: List of sections to review
        use_server_manager: Auto-start local server
        output_dir: Optional directory to save screenshots

    Returns:
        Exit code (0 = success)
    """
    load_dotenv()

    if sections is None:
        sections = ["above-fold", "mid-page", "footer"]

    print("\n🔍 SECTION-BASED VISUAL UX REVIEW")
    print(f"📄 URL: {url}")
    print(f"📱 Viewport: {viewport_name}")
    print(f"🎯 Sections: {', '.join(sections)}")
    print()

    # Estimate cost
    num_screenshots = len(sections)
    cost_info = estimate_cost(num_screenshots, detail_level="high")
    print_cost_estimate(cost_info)

    server_manager = None
    exit_code = 0

    try:
        # Start server if needed
        if use_server_manager:
            print("\n⚙️  Starting server manager...")
            server_manager = ServerManager()
            server_url = server_manager.start_server(kill_conflicts=True)
            url = server_url
            print(f"✅ Server running at {server_url}")

        # Capture sections
        print(f"\n📸 Capturing {len(sections)} sections...")
        screenshots = capture_page_sections_sync(
            url,
            viewport_name=viewport_name,
            sections=sections,
            output_dir=output_dir,
            validate=True
        )

        if output_dir:
            print(f"   💾 Screenshots saved to {output_dir}/")

        # Review each section
        results = {}

        print("\n🤖 Analyzing sections with GPT-4o Vision...\n")

        for section_name, screenshot_data in screenshots.items():
            persona = SECTION_PERSONAS[section_name]
            print(f"   🔍 {persona['name']} reviewing "
                  f"{section_name}...")

            # Get section-specific prompt
            prompt = get_section_prompt(section_name, viewport_name)

            # Create reviewer agent
            reviewer = create_section_reviewer(
                section_name,
                viewport_name
            )

            # Run review using Runner API
            result = asyncio.run(Runner.run(
                reviewer,
                [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_image",
                                "detail": "high",
                                "image_url": (
                                    f"data:image/png;base64,"
                                    f"{screenshot_data['base64']}"
                                ),
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": prompt
                    },
                ],
            ))

            # Extract review from response
            if hasattr(result, 'final_output'):
                review_text = str(result.final_output)
            else:
                review_text = str(result)

            results[section_name] = {
                "review": review_text.strip(),
                "scroll_position": screenshot_data["scroll_position"]
            }

            print("      ✅ Complete")

        # Format and display results
        print("\n" + "=" * 70)
        print(format_section_results(results, viewport_name))
        print("=" * 70)

        print("\n✅ Section review complete!")
        print(f"   📊 Analyzed {len(sections)} sections")
        print(f"   💰 Estimated cost: ~${cost_info['estimated_cost']:.4f}")

    except Exception as e:
        print(f"\n❌ Error during section review: {e}")
        print(format_troubleshooting_message(
            e,
            {"url": url, "viewport": viewport_name, "sections": sections}
        ))
        exit_code = 1

    finally:
        # Cleanup
        if server_manager:
            print("\n🧹 Cleaning up server...")
            server_manager.stop_server()

    return exit_code


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = "."

    viewport = sys.argv[2] if len(sys.argv) > 2 else "desktop"

    exit_code = run_section_review(
        url=target_url,
        viewport_name=viewport,
        sections=["above-fold", "mid-page", "footer"],
        use_server_manager=True,
        output_dir="qa_agents/screenshots"
    )

    sys.exit(exit_code)
