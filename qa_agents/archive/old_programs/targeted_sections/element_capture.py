"""
Element-based screenshot capture
Captures specific DOM elements by CSS selector
"""

import asyncio
import base64
from pathlib import Path
from playwright.async_api import async_playwright
from typing import Dict, Any, Optional
from qa_agents.reliability import retry, validate_screenshot


@retry(max_attempts=3, backoff=2.0)
async def capture_element_screenshot(
    url: str,
    selector: str,
    viewport_config: Dict[str, int] = None,
    output_path: str = None,
    validate: bool = True,
    padding: int = 0
) -> Dict[str, Any]:
    """
    Capture screenshot of specific element by CSS selector

    Args:
        url: URL to load
        selector: CSS selector for target element
        viewport_config: Viewport dimensions {width, height}
        output_path: Optional path to save PNG file
        validate: Validate screenshot is not blank/corrupt
        padding: Extra padding around element (pixels)

    Returns:
        Dict with screenshot data and metadata

    Raises:
        RuntimeError: If element not found or screenshot invalid
    """
    if viewport_config is None:
        viewport_config = {"width": 1920, "height": 1080}

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport=viewport_config,
            device_scale_factor=2  # Retina quality
        )
        page = await context.new_page()

        # Navigate and wait for content
        await page.goto(url, wait_until="networkidle", timeout=30000)

        # Find element
        element = await page.query_selector(selector)
        if not element:
            raise RuntimeError(
                f"Element not found: {selector}. "
                f"Ensure element exists and selector is correct."
            )

        # Check if element is visible
        is_visible = await element.is_visible()
        if not is_visible:
            raise RuntimeError(
                f"Element is not visible: {selector}. "
                f"Check CSS display/visibility properties."
            )

        # Get element bounds
        bounds = await element.bounding_box()
        if not bounds:
            raise RuntimeError(
                f"Could not get bounds for element: {selector}"
            )

        # Scroll element into view
        await element.scroll_into_view_if_needed()
        await page.wait_for_timeout(500)  # Let animations settle

        # Capture element screenshot with optional padding
        if padding > 0:
            # Capture with padding by adjusting clip
            screenshot_bytes = await page.screenshot(
                clip={
                    'x': max(0, bounds['x'] - padding),
                    'y': max(0, bounds['y'] - padding),
                    'width': bounds['width'] + (padding * 2),
                    'height': bounds['height'] + (padding * 2)
                }
            )
        else:
            # Capture element directly
            screenshot_bytes = await element.screenshot()

        await browser.close()

    # Convert to base64
    base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')

    result = {
        "base64": base64_image,
        "selector": selector,
        "bounds": bounds,
        "viewport": viewport_config,
        "method": "element-based"
    }

    # Validate if requested
    if validate:
        is_valid, error_msg = validate_screenshot(result)
        if not is_valid:
            raise RuntimeError(
                f"Screenshot validation failed for {selector}: {error_msg}"
            )

    # Save to file if requested
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(screenshot_bytes)
        result["path"] = output_path

    return result


async def capture_multiple_elements(
    url: str,
    selectors: list[str],
    viewport_config: Dict[str, int] = None,
    output_dir: str = None
) -> Dict[str, Dict[str, Any]]:
    """
    Capture multiple elements from same page in one browser session

    Args:
        url: URL to load
        selectors: List of CSS selectors
        viewport_config: Viewport dimensions
        output_dir: Optional directory to save screenshots

    Returns:
        Dict mapping selector to screenshot data
    """
    if viewport_config is None:
        viewport_config = {"width": 1920, "height": 1080}

    results = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport=viewport_config,
            device_scale_factor=2
        )
        page = await context.new_page()

        # Navigate once
        await page.goto(url, wait_until="networkidle", timeout=30000)

        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if not element:
                    print(f"   ⚠️  Element not found: {selector}")
                    continue

                is_visible = await element.is_visible()
                if not is_visible:
                    print(f"   ⚠️  Element not visible: {selector}")
                    continue

                # Scroll into view and capture
                await element.scroll_into_view_if_needed()
                await page.wait_for_timeout(300)

                screenshot_bytes = await element.screenshot()
                base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')

                bounds = await element.bounding_box()

                result = {
                    "base64": base64_image,
                    "selector": selector,
                    "bounds": bounds,
                    "viewport": viewport_config,
                    "method": "element-based"
                }

                # Validate
                is_valid, error_msg = validate_screenshot(result)
                if not is_valid:
                    print(f"   ⚠️  Invalid screenshot for {selector}: "
                          f"{error_msg}")
                    continue

                # Save if output dir specified
                if output_dir:
                    # Create safe filename from selector
                    safe_name = selector.replace('[', '').replace(']', '')
                    safe_name = safe_name.replace('"', '').replace("'", '')
                    safe_name = safe_name.replace(' ', '_')
                    filename = f"{safe_name}.png"
                    output_path = f"{output_dir}/{filename}"

                    Path(output_dir).mkdir(parents=True, exist_ok=True)
                    Path(output_path).write_bytes(screenshot_bytes)
                    result["path"] = output_path

                results[selector] = result
                print(f"   ✅ Captured: {selector}")

            except Exception as e:
                print(f"   ❌ Error capturing {selector}: {e}")
                continue

        await browser.close()

    return results


def capture_element_screenshot_sync(
    url: str,
    selector: str,
    viewport_config: Dict[str, int] = None,
    output_path: str = None,
    validate: bool = True
) -> Dict[str, Any]:
    """Synchronous wrapper for capture_element_screenshot"""
    return asyncio.run(
        capture_element_screenshot(
            url,
            selector,
            viewport_config,
            output_path,
            validate
        )
    )


def capture_multiple_elements_sync(
    url: str,
    selectors: list[str],
    viewport_config: Dict[str, int] = None,
    output_dir: str = None
) -> Dict[str, Dict[str, Any]]:
    """Synchronous wrapper for capture_multiple_elements"""
    return asyncio.run(
        capture_multiple_elements(
            url,
            selectors,
            viewport_config,
            output_dir
        )
    )


async def capture_from_config(
    config: Dict[str, Any],
    base_url: str,
    viewport_name: str = "desktop",
    output_dir: str = None
) -> Dict[str, Dict[str, Any]]:
    """
    Capture screenshots based on discovery config

    Args:
        config: Configuration dict from discover_ux_sections
        base_url: Base URL or local server
        viewport_name: Viewport to use
        output_dir: Optional output directory

    Returns:
        Dict mapping section names to screenshot data
    """
    viewport_configs = {
        "desktop": {"width": 1920, "height": 1080},
        "tablet": {"width": 768, "height": 1024},
        "mobile": {"width": 375, "height": 667}
    }

    viewport_config = viewport_configs.get(
        viewport_name,
        viewport_configs["desktop"]
    )

    all_results = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport=viewport_config,
            device_scale_factor=2
        )

        for page_config in config.get('pages', []):
            page_url = page_config['url']
            if not page_url.startswith('http'):
                page_url = f"{base_url.rstrip('/')}{page_url}"

            page = await context.new_page()
            await page.goto(page_url, wait_until="networkidle", timeout=30000)

            # Wait for CSS to fully load and render
            await page.wait_for_load_state("load")
            await page.wait_for_load_state("domcontentloaded")

            # Wait for stylesheets to be fully applied
            await page.evaluate("""
                () => {
                    return document.fonts.ready;
                }
            """)

            # Extended wait to ensure all CSS is parsed and applied
            await page.wait_for_timeout(3000)  # Give CSS/fonts extra time to render

            print(f"\n📸 Capturing sections from: {page_config['name']}")

            for section in page_config.get('sections', []):
                selector = section['selector']
                section_name = section['name']

                try:
                    element = await page.query_selector(selector)
                    if not element or not await element.is_visible():
                        print(f"   ⚠️  Skipping {section_name}: not visible")
                        continue

                    await element.scroll_into_view_if_needed()
                    await page.wait_for_timeout(500)  # Let animations settle

                    # Get element bounds for context padding
                    bounds = await element.bounding_box()
                    if not bounds:
                        print(f"   ⚠️  Skipping {section_name}: no bounds")
                        continue

                    # Capture with padding for visual context (200px above/below)
                    padding_top = 200
                    padding_bottom = 200
                    page_height = await page.evaluate("document.body.scrollHeight")

                    screenshot_bytes = await page.screenshot(
                        clip={
                            'x': 0,  # Full width for context
                            'y': max(0, bounds['y'] - padding_top),
                            'width': viewport_config['width'],
                            'height': min(
                                bounds['height'] + padding_top + padding_bottom,
                                page_height
                            )
                        }
                    )
                    base64_image = base64.b64encode(screenshot_bytes)
                    base64_image = base64_image.decode('utf-8')

                    result = {
                        "base64": base64_image,
                        "section_name": section_name,
                        "selector": selector,
                        "page_url": page_url,
                        "viewport": viewport_name,
                        "persona": section.get('persona', 'content-flow'),
                        "priority": section.get('priority', 'medium')
                    }

                    # Save if output dir specified
                    if output_dir:
                        safe_name = section_name.replace(' ', '_')
                        safe_name = safe_name.replace('/', '_')
                        filename = f"{safe_name}_{viewport_name}.png"
                        output_path = f"{output_dir}/{filename}"

                        Path(output_dir).mkdir(parents=True, exist_ok=True)
                        Path(output_path).write_bytes(screenshot_bytes)
                        result["path"] = output_path

                    all_results[section_name] = result
                    print(f"   ✅ {section_name}")

                except Exception as e:
                    print(f"   ❌ Error with {section_name}: {e}")
                    continue

            await page.close()

        await browser.close()

    return all_results
