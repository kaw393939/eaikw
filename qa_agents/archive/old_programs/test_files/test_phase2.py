#!/usr/bin/env python3
"""
Test Phase 2: Section-based analysis
"""

import sys
from qa_agents.section_capture import (
    capture_page_sections_sync,
    calculate_scroll_positions
)
from qa_agents.section_personas import get_section_prompt


def test_scroll_positions():
    """Test scroll position calculation"""
    print("\n🧪 TEST 1: Scroll Position Calculation")

    # Simulate a long page
    page_height = 3000
    viewport_height = 1080

    positions = calculate_scroll_positions(
        page_height,
        viewport_height,
        ["above-fold", "mid-page", "footer"]
    )

    print(f"   Page height: {page_height}px")
    print(f"   Viewport: {viewport_height}px")
    print(f"   Positions: {positions}")

    # Validate
    assert "above-fold" in positions
    assert positions["above-fold"] == 0
    assert "mid-page" in positions
    assert positions["mid-page"] == viewport_height
    assert "footer" in positions
    assert positions["footer"] == page_height - viewport_height

    print("   ✅ Scroll positions calculated correctly")


def test_section_prompts():
    """Test section-specific prompt generation"""
    print("\n🧪 TEST 2: Section Prompt Generation")

    sections = ["above-fold", "mid-page", "footer"]

    for section in sections:
        prompt = get_section_prompt(section, "desktop")
        assert len(prompt) > 100, f"Prompt too short for {section}"
        assert section in prompt.lower(), f"Section name missing in {section}"
        print(f"   ✅ {section} prompt: {len(prompt)} chars")


def test_section_capture():
    """Test section screenshot capture"""
    print("\n🧪 TEST 3: Section Screenshot Capture")

    # Create a simple test HTML file
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <style>
            body { margin: 0; font-family: Arial, sans-serif; }
            .section { height: 1080px; padding: 50px; }
            .above-fold { background: #e3f2fd; }
            .mid-page { background: #f3e5f5; }
            .footer { background: #e8f5e9; }
        </style>
    </head>
    <body>
        <div class="section above-fold">
            <h1>Above Fold Section</h1>
            <p>This is what users see first</p>
        </div>
        <div class="section mid-page">
            <h2>Mid Page Section</h2>
            <p>This requires scrolling</p>
        </div>
        <div class="section footer">
            <h3>Footer Section</h3>
            <p>Bottom of the page</p>
        </div>
    </body>
    </html>
    """

    # Write test file
    with open("test_sections.html", "w") as f:
        f.write(test_html)

    try:
        # Start a test server manually
        import subprocess
        import time
        import os

        server = subprocess.Popen(
            ["python3", "-m", "http.server", "8085"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(2)  # Wait for server

        # Capture sections
        screenshots = capture_page_sections_sync(
            url="http://localhost:8085/test_sections.html",
            viewport_name="desktop",
            sections=["above-fold", "mid-page", "footer"],
            validate=True
        )

        print(f"   Captured {len(screenshots)} sections")

        # Validate
        assert len(screenshots) == 3
        for section in ["above-fold", "mid-page", "footer"]:
            assert section in screenshots
            assert "base64" in screenshots[section]
            print(f"   ✅ {section}: "
                  f"{len(screenshots[section]['base64'])} chars")

    finally:
        # Cleanup
        server.terminate()
        server.wait()
        os.remove("test_sections.html")


if __name__ == "__main__":
    tests = [
        test_scroll_positions,
        test_section_prompts,
        test_section_capture
    ]

    passed = 0
    failed = 0

    print("=" * 70)
    print("PHASE 2: SECTION-BASED ANALYSIS TESTS")
    print("=" * 70)

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"📊 RESULTS: {passed} passed, {failed} failed")
    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
    print("=" * 70)

    sys.exit(0 if failed == 0 else 1)
