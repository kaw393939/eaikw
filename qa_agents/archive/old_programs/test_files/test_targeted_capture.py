#!/usr/bin/env python3
"""
Tests for targeted capture (data-attribute discovery + element capture)
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from qa_agents.discover_ux_sections import UXSectionDiscovery
from qa_agents.element_capture import (
    capture_element_screenshot,
    capture_multiple_elements
)


# Sample HTML for testing
SAMPLE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test Page</title>
    <style>
        body { margin: 0; padding: 0; font-family: sans-serif; }
        .hero {
            height: 400px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .features {
            padding: 40px;
            background: #f7fafc;
        }
        .footer {
            padding: 20px;
            background: #2d3748;
            color: white;
            text-align: center;
        }
    </style>
</head>
<body>
    <header data-ux-section="hero" data-ux-priority="critical" class="hero">
        <h1>Welcome to Test Site</h1>
    </header>

    <main data-ux-section="features" data-ux-priority="high" class="features">
        <h2>Features</h2>
        <p>Amazing features go here</p>
    </main>

    <footer data-ux-section="footer" data-ux-priority="medium" class="footer">
        <p>&copy; 2025 Test Site</p>
    </footer>
</body>
</html>
"""


@pytest.fixture
def temp_html_file():
    """Create temporary HTML file for testing"""
    temp_dir = tempfile.mkdtemp()
    html_file = Path(temp_dir) / "test.html"
    html_file.write_text(SAMPLE_HTML)

    yield html_file

    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_output_dir():
    """Create temporary output directory"""
    temp_dir = tempfile.mkdtemp()

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir)


class TestUXSectionDiscovery:
    """Test auto-discovery functionality"""

    def test_persona_inference(self):
        """Test persona inference from section names"""
        discovery = UXSectionDiscovery()

        test_cases = [
            ("hero", "first-impression"),
            ("header", "first-impression"),
            ("navigation", "first-impression"),
            ("features", "content-flow"),
            ("lessons", "content-flow"),
            ("footer", "trust-inspector"),
            ("contact", "trust-inspector"),
            ("unknown-section", "content-flow")  # default
        ]

        for section_name, expected_persona in test_cases:
            result = discovery.infer_persona(section_name)
            assert result == expected_persona, (
                f"Expected {section_name} -> {expected_persona}, "
                f"got {result}"
            )

    def test_priority_inference(self):
        """Test priority inference from section names"""
        discovery = UXSectionDiscovery()

        test_cases = [
            ("hero", "critical"),
            ("header", "critical"),
            ("navigation", "high"),
            ("nav", "high"),
            ("features", "high"),
            ("footer", "medium"),
            ("sidebar", "medium")
        ]

        for section_name, expected_priority in test_cases:
            result = discovery.infer_priority(section_name)
            assert result == expected_priority, (
                f"Expected {section_name} -> {expected_priority}, "
                f"got {result}"
            )

    @pytest.mark.asyncio
    async def test_discover_from_html(self, temp_html_file):
        """Test discovering sections from HTML file"""
        discovery = UXSectionDiscovery()

        file_url = f"file://{temp_html_file}"

        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(file_url)

                result = await discovery.discover_page(page, file_url)

                await browser.close()

                # Verify discovered sections
                sections = result['sections']
                assert len(sections) == 3, "Should find 3 sections"

                section_names = [s['name'] for s in sections]
                assert 'hero' in section_names
                assert 'features' in section_names
                assert 'footer' in section_names

        except ImportError:
            pytest.skip("Playwright not available")

    def test_config_generation_yaml(self):
        """Test YAML config generation"""
        discovery = UXSectionDiscovery()

        sample_pages = [
            {
                'url': '/',
                'name': 'Home',
                'sections': [
                    {
                        'name': 'hero',
                        'priority': 'critical',
                        'selector': '[data-ux-section="hero"]',
                        'bounds': {}
                    }
                ]
            }
        ]

        config = discovery.generate_config(
            sample_pages,
            output_format='yaml'
        )

        # Verify YAML structure
        assert 'pages:' in config
        assert 'hero' in config


class TestElementCapture:
    """Test element-based screenshot capture"""

    @pytest.mark.asyncio
    async def test_capture_element_basic(
        self,
        temp_html_file,
        temp_output_dir
    ):
        """Test basic element capture"""
        file_url = f"file://{temp_html_file}"
        output_path = Path(temp_output_dir) / "hero.png"

        try:
            screenshot = await capture_element_screenshot(
                file_url,
                '[data-ux-section="hero"]',
                output_path=str(output_path)
            )

            # Verify screenshot was captured
            assert screenshot is not None
            assert 'base64' in screenshot
            assert 'path' in screenshot
            assert output_path.exists()
            assert output_path.stat().st_size > 0

        except ImportError:
            pytest.skip("Playwright not available")


def run_tests():
    """Run all tests"""
    pytest.main([__file__, '-v'])


if __name__ == "__main__":
    run_tests()
