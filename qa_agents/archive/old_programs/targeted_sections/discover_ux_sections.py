#!/usr/bin/env python3
"""
UX Section Auto-Discovery Tool
Scans HTML pages for data-ux-section markers and generates config
"""

import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from typing import List, Dict, Any
import yaml


class UXSectionDiscovery:
    """Discovers and catalogs UX review sections from HTML"""

    PERSONA_MAPPING = {
        # Section name patterns -> persona assignments
        'hero': 'first-impression',
        'header': 'first-impression',
        'navigation': 'first-impression',
        'nav': 'first-impression',
        'features': 'content-flow',
        'content': 'content-flow',
        'main': 'content-flow',
        'lessons': 'content-flow',
        'courses': 'content-flow',
        'about': 'content-flow',
        'footer': 'trust-inspector',
        'contact': 'trust-inspector',
        'social': 'trust-inspector',
    }

    PRIORITY_DEFAULTS = {
        'hero': 'critical',
        'header': 'critical',
        'navigation': 'high',
        'nav': 'high',
        'footer': 'medium',
        'features': 'high',
    }

    def __init__(self):
        self.discovered_sections = {}

    async def discover_page(
        self,
        page,
        url: str,
        page_name: str = None
    ) -> Dict[str, Any]:
        """
        Discover all UX review sections on a page

        Args:
            page: Playwright page object
            url: URL to scan
            page_name: Human-readable page name

        Returns:
            Dict with page info and discovered sections
        """
        print(f"\n🔍 Scanning: {url}")
        await page.goto(url, wait_until="networkidle", timeout=30000)

        # JavaScript to find all marked sections
        sections = await page.evaluate("""
            () => {
                const elements = document.querySelectorAll('[data-ux-section]');
                return Array.from(elements).map((el, index) => {
                    const rect = el.getBoundingClientRect();
                    const computedStyle = window.getComputedStyle(el);

                    return {
                        name: el.dataset.uxSection,
                        priority: el.dataset.uxPriority || null,
                        selector: `[data-ux-section="${el.dataset.uxSection}"]`,
                        tagName: el.tagName.toLowerCase(),
                        classes: el.className,
                        bounds: {
                            x: rect.x,
                            y: rect.y,
                            width: rect.width,
                            height: rect.height,
                            top: rect.top,
                            bottom: rect.bottom
                        },
                        isVisible: computedStyle.display !== 'none' &&
                                 computedStyle.visibility !== 'hidden' &&
                                 rect.width > 0 && rect.height > 0,
                        index: index
                    };
                });
            }
        """)

        # Filter visible sections only
        visible_sections = [s for s in sections if s['isVisible']]

        print(f"   ✅ Found {len(visible_sections)} sections")
        for section in visible_sections:
            priority = section['priority'] or 'not set'
            print(f"      - {section['name']} ({priority})")

        return {
            'url': url,
            'name': page_name or url,
            'sections': visible_sections,
            'total_found': len(sections),
            'visible_count': len(visible_sections)
        }

    def infer_persona(self, section_name: str) -> str:
        """
        Infer appropriate persona based on section name

        Args:
            section_name: Name from data-ux-section

        Returns:
            Persona name
        """
        section_lower = section_name.lower()

        for pattern, persona in self.PERSONA_MAPPING.items():
            if pattern in section_lower:
                return persona

        # Default to content-flow for unknown sections
        return 'content-flow'

    def infer_priority(
        self,
        section_name: str,
        explicit_priority: str = None
    ) -> str:
        """
        Infer priority if not explicitly set

        Args:
            section_name: Name from data-ux-section
            explicit_priority: Priority from data-ux-priority

        Returns:
            Priority level (critical/high/medium/low)
        """
        if explicit_priority:
            return explicit_priority

        section_lower = section_name.lower()
        for pattern, priority in self.PRIORITY_DEFAULTS.items():
            if pattern in section_lower:
                return priority

        return 'medium'

    def generate_config(
        self,
        discovered_pages: List[Dict[str, Any]],
        output_format: str = 'yaml'
    ) -> str:
        """
        Generate configuration file from discovered sections

        Args:
            discovered_pages: List of page discovery results
            output_format: 'yaml' or 'json'

        Returns:
            Configuration string
        """
        config = {
            'version': '1.0',
            'description': 'Auto-discovered UX review sections',
            'defaults': {
                'viewports': ['desktop', 'tablet', 'mobile'],
                'capture_method': 'element-based'
            },
            'pages': []
        }

        for page_data in discovered_pages:
            page_config = {
                'url': page_data['url'],
                'name': page_data['name'],
                'sections': []
            }

            for section in page_data['sections']:
                section_config = {
                    'name': section['name'],
                    'selector': section['selector'],
                    'persona': self.infer_persona(section['name']),
                    'priority': self.infer_priority(
                        section['name'],
                        section.get('priority')
                    ),
                    'bounds': section['bounds']
                }

                page_config['sections'].append(section_config)

            config['pages'].append(page_config)

        if output_format == 'yaml':
            return yaml.dump(config, sort_keys=False, default_flow_style=False)
        elif output_format == 'json':
            return json.dumps(config, indent=2)
        else:
            # Return as dict
            return config

    async def scan_site(
        self,
        base_url: str,
        pages: List[str] = None
    ) -> Dict[str, Any]:
        """
        Scan entire site for UX sections

        Args:
            base_url: Base URL or local directory
            pages: List of page paths to scan (e.g., ["/", "/about"])

        Returns:
            Complete site scan results
        """
        if pages is None:
            pages = ["/"]

        discovered_pages = []

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={'width': 1920, 'height': 1080})

            for page_path in pages:
                # Construct full URL
                if base_url.startswith('http'):
                    url = f"{base_url.rstrip('/')}{page_path}"
                else:
                    # Local file
                    url = f"file://{Path(base_url).resolve()}{page_path}/index.html"

                try:
                    result = await self.discover_page(page, url, page_path)
                    discovered_pages.append(result)
                except Exception as e:
                    print(f"   ❌ Error scanning {page_path}: {e}")

            await browser.close()

        return {
            'base_url': base_url,
            'pages': discovered_pages,
            'total_pages': len(discovered_pages),
            'total_sections': sum(p['visible_count'] for p in discovered_pages)
        }


async def main():
    """CLI interface for UX section discovery"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Discover UX review sections from HTML pages'
    )
    parser.add_argument(
        'target',
        help='Base URL or local directory (e.g., _site or http://localhost:8080)'
    )
    parser.add_argument(
        '--pages',
        nargs='+',
        default=['/'],
        help='Pages to scan (e.g., / /about /lessons)'
    )
    parser.add_argument(
        '--output',
        '-o',
        default='ux-review-config.yaml',
        help='Output configuration file'
    )
    parser.add_argument(
        '--format',
        choices=['yaml', 'json'],
        default='yaml',
        help='Output format'
    )
    parser.add_argument(
        '--server',
        action='store_true',
        help='Start local HTTP server first'
    )

    args = parser.parse_args()

    # Start server if needed
    server = None
    if args.server:
        from qa_agents.server_manager import ServerManager
        print("\n🚀 Starting local server...")
        server = ServerManager()
        base_url = server.start_server(kill_conflicts=True)
    else:
        base_url = args.target

    # Run discovery
    print("\n" + "=" * 70)
    print("🔍 UX SECTION AUTO-DISCOVERY")
    print("=" * 70)

    discovery = UXSectionDiscovery()
    results = await discovery.scan_site(base_url, args.pages)

    print("\n" + "=" * 70)
    print("📊 DISCOVERY SUMMARY")
    print("=" * 70)
    print(f"   Pages scanned: {results['total_pages']}")
    print(f"   Sections found: {results['total_sections']}")

    # Generate config
    config_str = discovery.generate_config(
        results['pages'],
        args.format
    )

    # Save to file
    output_path = Path(args.output)
    output_path.write_text(config_str)
    print(f"\n✅ Configuration saved to: {output_path}")
    print(f"   Format: {args.format}")

    # Show sample
    print("\n📄 Sample configuration:")
    print("-" * 70)
    lines = config_str.split('\n')[:20]
    print('\n'.join(lines))
    if len(config_str.split('\n')) > 20:
        print("...")

    # Cleanup
    if server:
        print("\n🧹 Stopping server...")
        server.stop_server()

    print("\n✨ Discovery complete!")
    print("\nNext steps:")
    print("1. Review generated config: cat", str(output_path))
    print("2. Add data-ux-section markers to your HTML templates")
    print("3. Run review: python qa_agents/targeted_review.py")


if __name__ == "__main__":
    asyncio.run(main())
