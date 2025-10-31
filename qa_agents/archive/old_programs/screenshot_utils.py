"""
Screenshot capture utilities using Playwright
Captures screenshots at different viewports for visual analysis
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


@retry(max_attempts=3, backoff=2.0)
async def capture_screenshot(
    url: str,
    viewport_name: str = "desktop",
    output_path: str | None = None,
    validate: bool = True
) -> dict:
    """
    Capture screenshot at specified viewport

    Args:
        url: URL to capture
        viewport_name: One of 'desktop', 'tablet', 'mobile'
        output_path: Optional path to save screenshot file
        validate: Validate screenshot is not blank/corrupt

    Returns:
        dict with 'base64' (for GPT-4o) and 'path' (if saved)

    Raises:
        RuntimeError: If screenshot validation fails
    """
    viewport = VIEWPORTS.get(viewport_name, VIEWPORTS["desktop"])

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport=viewport,
            device_scale_factor=2  # Retina/HiDPI for clarity
        )
        page = await context.new_page()

        # Navigate and wait for page to be fully loaded
        await page.goto(url, wait_until="networkidle", timeout=30000)

        # Take screenshot
        screenshot_bytes = await page.screenshot(full_page=False)

        await browser.close()

    # Convert to base64 for GPT-4o Vision API
    base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')

    result = {
        "base64": base64_image,
        "viewport": viewport_name,
        "dimensions": viewport
    }

    # Validate if requested
    if validate:
        is_valid, error_msg = validate_screenshot(result)
        if not is_valid:
            raise RuntimeError(
                f"Screenshot validation failed for {viewport_name}: "
                f"{error_msg}"
            )

    result = {
        "base64": base64_image,
        "viewport": viewport_name,
        "dimensions": viewport
    }

    # Validate if requested
    if validate:
        is_valid, error_msg = validate_screenshot(result)
        if not is_valid:
            raise RuntimeError(
                f"Screenshot validation failed for {viewport_name}: "
                f"{error_msg}"
            )

    # Optionally save to file
    if output_path:
        Path(output_path).write_bytes(screenshot_bytes)
        result["path"] = output_path

    return result


async def capture_all_viewports(
    url: str,
    output_dir: str | None = None
) -> dict[str, dict]:
    """
    Capture screenshots at all viewports

    Args:
        url: URL to capture
        output_dir: Optional directory to save screenshots

    Returns:
        dict mapping viewport name to screenshot data
    """
    screenshots = {}

    for viewport_name in VIEWPORTS.keys():
        output_path = None
        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            output_path = f"{output_dir}/{viewport_name}.png"

        screenshots[viewport_name] = await capture_screenshot(
            url,
            viewport_name,
            output_path
        )

    return screenshots


def capture_screenshot_sync(
    url: str,
    viewport_name: str = "desktop",
    output_path: str | None = None,
    validate: bool = True
) -> dict:
    """Synchronous wrapper for capture_screenshot"""
    return asyncio.run(
        capture_screenshot(url, viewport_name, output_path, validate)
    )


def capture_all_viewports_sync(
    url: str,
    output_dir: str | None = None
) -> dict[str, dict]:
    """Synchronous wrapper for capture_all_viewports"""
    return asyncio.run(capture_all_viewports(url, output_dir))
