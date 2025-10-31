"""
Section-based screenshot capture
Captures page sections for targeted analysis
"""

import asyncio
import base64
from pathlib import Path
from playwright.async_api import async_playwright
from qa_agents.reliability import retry, validate_screenshot


VIEWPORTS = {
    "desktop": {"width": 1920, "height": 1080},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 667}
}


def calculate_scroll_positions(
    page_height: int,
    viewport_height: int,
    sections: list[str] = None
) -> dict[str, int]:
    """
    Calculate scroll positions for page sections

    Args:
        page_height: Total page height in pixels
        viewport_height: Viewport height in pixels
        sections: List of sections to capture

    Returns:
        Dict mapping section name to scroll position (y coordinate)
    """
    if sections is None:
        sections = ["above-fold", "mid-page", "footer"]

    positions = {}

    # Calculate positions based on page geometry
    if "above-fold" in sections:
        positions["above-fold"] = 0  # Top of page

    if "mid-page" in sections:
        # Middle section - one viewport down
        positions["mid-page"] = viewport_height

    if "footer" in sections:
        # Footer - scroll to bottom minus one viewport
        footer_scroll = max(0, page_height - viewport_height)
        positions["footer"] = footer_scroll

    # If page is short, don't duplicate positions
    unique_positions = {}
    seen = set()
    for name, pos in positions.items():
        if pos not in seen:
            unique_positions[name] = pos
            seen.add(pos)

    return unique_positions


@retry(max_attempts=3, backoff=2.0)
async def capture_page_sections(
    url: str,
    viewport_name: str = "desktop",
    sections: list[str] = None,
    output_dir: str | None = None,
    validate: bool = True
) -> dict[str, dict]:
    """
    Capture multiple sections of a page

    Sections:
    - above-fold: First viewport height (what user sees immediately)
    - mid-page: Second viewport height (after scrolling once)
    - footer: Last viewport height (bottom of page)

    Args:
        url: URL to capture
        viewport_name: One of 'desktop', 'tablet', 'mobile'
        sections: List of sections to capture (default: all)
        output_dir: Optional directory to save screenshots
        validate: Validate screenshots are not blank/corrupt

    Returns:
        Dict mapping section name to screenshot data

    Raises:
        RuntimeError: If screenshot validation fails
    """
    if sections is None:
        sections = ["above-fold", "mid-page", "footer"]

    viewport = VIEWPORTS.get(viewport_name, VIEWPORTS["desktop"])
    screenshots = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport=viewport,
            device_scale_factor=2  # Retina/HiDPI for clarity
        )
        page = await context.new_page()

        # Navigate and wait for page to be fully loaded
        await page.goto(url, wait_until="networkidle", timeout=30000)

        # Get page dimensions
        page_height = await page.evaluate("document.body.scrollHeight")
        viewport_height = viewport["height"]

        # Calculate scroll positions
        scroll_positions = calculate_scroll_positions(
            page_height,
            viewport_height,
            sections
        )

        # Capture each section
        for section_name, scroll_y in scroll_positions.items():
            # Scroll to position
            await page.evaluate(f"window.scrollTo(0, {scroll_y})")
            await page.wait_for_timeout(500)  # Let animations settle

            # Take screenshot
            screenshot_bytes = await page.screenshot(full_page=False)

            # Convert to base64
            base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')

            result = {
                "base64": base64_image,
                "viewport": viewport_name,
                "section": section_name,
                "scroll_position": scroll_y,
                "dimensions": viewport
            }

            # Validate if requested
            if validate:
                is_valid, error_msg = validate_screenshot(result)
                if not is_valid:
                    raise RuntimeError(
                        f"Screenshot validation failed for {section_name} "
                        f"at {viewport_name}: {error_msg}"
                    )

            # Optionally save to file
            if output_dir:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                filename = f"{viewport_name}_{section_name}.png"
                output_path = f"{output_dir}/{filename}"
                Path(output_path).write_bytes(screenshot_bytes)
                result["path"] = output_path

            screenshots[section_name] = result

        await browser.close()

    return screenshots


async def capture_all_sections_all_viewports(
    url: str,
    sections: list[str] = None,
    viewports: list[str] = None,
    output_dir: str | None = None
) -> dict[str, dict[str, dict]]:
    """
    Capture all sections for all viewports

    Args:
        url: URL to capture
        sections: List of sections (default: all)
        viewports: List of viewports (default: all)
        output_dir: Optional directory to save screenshots

    Returns:
        Nested dict: viewport -> section -> screenshot data
    """
    if viewports is None:
        viewports = list(VIEWPORTS.keys())

    if sections is None:
        sections = ["above-fold", "mid-page", "footer"]

    all_screenshots = {}

    for viewport_name in viewports:
        screenshots = await capture_page_sections(
            url,
            viewport_name,
            sections,
            output_dir
        )
        all_screenshots[viewport_name] = screenshots

    return all_screenshots


def capture_page_sections_sync(
    url: str,
    viewport_name: str = "desktop",
    sections: list[str] = None,
    output_dir: str | None = None,
    validate: bool = True
) -> dict[str, dict]:
    """Synchronous wrapper for capture_page_sections"""
    return asyncio.run(
        capture_page_sections(
            url, viewport_name, sections, output_dir, validate
        )
    )


def capture_all_sections_all_viewports_sync(
    url: str,
    sections: list[str] = None,
    viewports: list[str] = None,
    output_dir: str | None = None
) -> dict[str, dict[str, dict]]:
    """Synchronous wrapper for capture_all_sections_all_viewports"""
    return asyncio.run(
        capture_all_sections_all_viewports(
            url,
            sections,
            viewports,
            output_dir
        )
    )
