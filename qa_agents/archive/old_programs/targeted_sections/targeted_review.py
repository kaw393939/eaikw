#!/usr/bin/env python3
"""
Targeted section review using data-attribute discovery
Integrates auto-discovery + element capture + persona reviews
"""

import sys
import asyncio
import argparse
from pathlib import Path
from typing import Dict, Any, Optional
from agents import Runner
from dotenv import load_dotenv

from qa_agents.discover_ux_sections import UXSectionDiscovery
from qa_agents.element_capture import capture_from_config
from qa_agents.section_personas import (
    get_section_prompt,
    format_section_results,
)
from qa_agents.visual_ux_agents import create_section_reviewer
from qa_agents.server_manager import ServerManager
from qa_agents.reliability import (
    estimate_cost,
    print_cost_estimate,
    format_troubleshooting_message
)


async def run_targeted_review(
    url: str,
    viewport_name: str = "desktop",
    config_path: Optional[str] = None,
    auto_discover: bool = False,
    pages: Optional[list[str]] = None,
    use_server_manager: bool = True,
    output_dir: str = "qa_agents/screenshots",
    priority_filter: Optional[str] = None
) -> int:
    """
    Run targeted UX review using data-attribute discovery

    Args:
        url: URL to review (or path if using server manager)
        viewport_name: One of 'desktop', 'tablet', 'mobile'
        config_path: Path to existing YAML config (optional)
        auto_discover: Auto-discover sections from HTML
        pages: Pages to scan if auto-discovering
        use_server_manager: Auto-start local server
        output_dir: Directory to save screenshots
        priority_filter: Only review sections with this priority
                        (critical, high, medium, low)

    Returns:
        Exit code (0 = success)
    """
    load_dotenv()

    print("\n🎯 TARGETED SECTION REVIEW (Data-Attribute Based)")
    print(f"📄 URL: {url}")
    print(f"📱 Viewport: {viewport_name}")
    print()

    server_manager = None
    exit_code = 0
    config = None

    try:
        # Start server if needed
        if use_server_manager:
            print("⚙️  Starting server manager...")
            server_manager = ServerManager()
            server_url = server_manager.start_server(kill_conflicts=True)
            url = server_url
            print(f"✅ Server running at {server_url}\n")

        # Get configuration
        if config_path:
            print(f"📋 Loading config from {config_path}...")
            import yaml
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        elif auto_discover:
            print("🔍 Auto-discovering sections from HTML...")
            discovery = UXSectionDiscovery()

            if pages is None:
                pages = ["/"]

            # Discover sections - use server URL when server is running
            scan_target = url
            results = await discovery.scan_site(scan_target, pages)

            # Generate config
            config = discovery.generate_config(
                results['pages'],
                output_format='dict'
            )

            total_sections = sum(
                len(page_data.get('sections', []))
                for page_data in config['pages']
            )
            print(f"   ✅ Found {total_sections} sections "
                  f"across {len(pages)} page(s)\n")
        else:
            print("❌ Error: Must provide --config or --auto-discover")
            return 1

        # Apply priority filter
        if priority_filter:
            print(f"🔎 Filtering for priority: {priority_filter}")
            config = filter_by_priority(config, priority_filter)

        # Count sections for cost estimate
        total_sections = count_sections(config)

        if total_sections == 0:
            print("⚠️  No sections found to review")
            return 0

        # Estimate cost
        cost_info = estimate_cost(total_sections, detail_level="high")
        print_cost_estimate(cost_info)

        # Capture screenshots
        print(f"\n📸 Capturing {total_sections} section(s)...")
        screenshots = await capture_from_config(
            config,
            url,
            viewport_name=viewport_name,
            output_dir=output_dir
        )

        print(f"   💾 Screenshots saved to {output_dir}/")

        # Review each section
        results = {}

        print("\n🤖 Analyzing sections with GPT-4o Vision...\n")

        for section_name, screenshot_data in screenshots.items():
            # Find section info from config
            section_info = None
            page_url = screenshot_data.get('page_url', '/')

            for page_data in config['pages']:
                if page_data.get('url') == page_url:
                    for section in page_data.get('sections', []):
                        if section.get('name') == section_name:
                            section_info = section
                            break
                if section_info:
                    break

            if not section_info:
                print(f"   ⚠️  Skipping {section_name}: config not found")
                continue

            persona_key = section_info.get('persona', 'content-flow')
            priority = section_info.get('priority', 'medium')

            print(f"   🔍 [{priority.upper()}] Reviewing '{section_name}' "
                  f"({persona_key})...")

            # Get section-specific prompt
            prompt = get_section_prompt(persona_key, viewport_name)

            # Create reviewer agent
            reviewer = create_section_reviewer(
                persona_key,
                viewport_name
            )

            # Run review using Runner API
            result = await Runner.run(
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
            )

            # Extract review from response
            if hasattr(result, 'final_output'):
                review_text = str(result.final_output)
            else:
                review_text = str(result)

            results[f"{page_url}#{section_name}"] = {
                "review": review_text.strip(),
                "persona": persona_key,
                "priority": priority,
                "selector": section_info.get('selector', ''),
                "page": page_url
            }

            print("      ✅ Complete")

        # Format and display results
        print("\n" + "=" * 70)
        print(format_targeted_results(results, viewport_name))
        print("=" * 70)

        print(f"\n✅ Targeted review complete!")
        print(f"   📊 Analyzed {len(results)} section(s)")
        print(f"   💰 Estimated cost: ~${cost_info['estimated_cost']:.4f}")

    except Exception as e:
        print(f"\n❌ Error during targeted review: {e}")
        print(format_troubleshooting_message(
            e,
            {
                "url": url,
                "viewport": viewport_name,
                "config_path": config_path,
                "auto_discover": auto_discover
            }
        ))
        exit_code = 1

    finally:
        # Cleanup
        if server_manager:
            print("\n🧹 Cleaning up server...")
            server_manager.stop_server()

    return exit_code


def run_targeted_review_sync(*args, **kwargs) -> int:
    """Synchronous wrapper for run_targeted_review"""
    return asyncio.run(run_targeted_review(*args, **kwargs))


def filter_by_priority(config: Dict[str, Any], priority: str) -> Dict[str, Any]:
    """Filter config to only include sections with specified priority"""
    filtered_config = {
        'pages': [],
        'defaults': config.get('defaults', {})
    }

    for page_data in config['pages']:
        filtered_sections = [
            section for section in page_data.get('sections', [])
            if section.get('priority', 'medium') == priority
        ]

        if filtered_sections:
            filtered_config['pages'].append({
                **page_data,
                'sections': filtered_sections
            })

    return filtered_config


def count_sections(config: Dict[str, Any]) -> int:
    """Count total sections in config"""
    return sum(
        len(page_data.get('sections', []))
        for page_data in config['pages']
    )


def find_section_info(
    config: Dict[str, Any],
    page_url: str,
    section_name: str
) -> Optional[Dict[str, Any]]:
    """Find section info in config"""
    for page_data in config['pages']:
        if page_data.get('url') == page_url:
            sections = page_data.get('sections', [])
            for section in sections:
                if section.get('name') == section_name:
                    return section
    return None


def format_targeted_results(
    results: Dict[str, Dict[str, Any]],
    viewport_name: str
) -> str:
    """Format targeted review results for display"""
    output = []
    output.append(f"\n🎯 TARGETED SECTION REVIEW RESULTS ({viewport_name})")
    output.append("=" * 70)

    # Group by priority
    by_priority = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': []
    }

    for section_key, data in results.items():
        priority = data.get('priority', 'medium')
        by_priority[priority].append((section_key, data))

    # Display by priority
    for priority in ['critical', 'high', 'medium', 'low']:
        sections = by_priority[priority]
        if not sections:
            continue

        output.append(f"\n{'🔴' if priority == 'critical' else '🟡' if priority == 'high' else '🟢'} {priority.upper()} PRIORITY ({len(sections)} sections)")
        output.append("-" * 70)

        for section_key, data in sections:
            page_url = data.get('page', '')
            section_name = section_key.split('#')[-1]
            persona = data.get('persona', '')
            selector = data.get('selector', '')

            output.append(f"\n📍 {section_name} ({page_url})")
            output.append(f"   Persona: {persona}")
            output.append(f"   Selector: {selector}")
            output.append(f"\n{data['review']}")
            output.append("-" * 70)

    return "\n".join(output)


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Targeted UX review using data-attribute discovery'
    )

    parser.add_argument(
        'url',
        nargs='?',
        default='.',
        help='URL or path to review (default: current directory)'
    )

    parser.add_argument(
        '--viewport',
        '-v',
        default='desktop',
        choices=['desktop', 'tablet', 'mobile'],
        help='Viewport size (default: desktop)'
    )

    parser.add_argument(
        '--config',
        '-c',
        help='Path to YAML config file'
    )

    parser.add_argument(
        '--auto-discover',
        '-a',
        action='store_true',
        help='Auto-discover sections from HTML data attributes'
    )

    parser.add_argument(
        '--pages',
        '-p',
        nargs='+',
        help='Pages to scan (e.g., / /lessons /about)'
    )

    parser.add_argument(
        '--priority',
        choices=['critical', 'high', 'medium', 'low'],
        help='Filter by priority level'
    )

    parser.add_argument(
        '--output',
        '-o',
        default='qa_agents/screenshots',
        help='Output directory for screenshots (default: qa_agents/screenshots)'
    )

    parser.add_argument(
        '--no-server',
        action='store_true',
        help='Disable auto server manager (use existing URL)'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.config and not args.auto_discover:
        parser.error('Must provide either --config or --auto-discover')

    exit_code = run_targeted_review_sync(
        url=args.url,
        viewport_name=args.viewport,
        config_path=args.config,
        auto_discover=args.auto_discover,
        pages=args.pages,
        use_server_manager=not args.no_server,
        output_dir=args.output,
        priority_filter=args.priority
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
