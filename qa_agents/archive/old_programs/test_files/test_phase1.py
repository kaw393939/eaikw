#!/usr/bin/env python3
"""
Test Phase 1: Bulletproofing features
"""

import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qa_agents.server_manager import ServerManager
from qa_agents.reliability import (
    estimate_cost,
    print_cost_estimate,
    validate_screenshot
)
from qa_agents.screenshot_utils import capture_screenshot_sync


def test_port_detection():
    """Test auto port detection"""
    print("\n" + "=" * 70)
    print("TEST 1: Port Detection")
    print("=" * 70)

    sm = ServerManager()
    port = sm.find_available_port(start=8080, end=8090)
    print(f"✅ Found available port: {port}")
    assert 8080 <= port <= 8090, "Port out of range"


def test_server_lifecycle():
    """Test server start/stop"""
    print("\n" + "=" * 70)
    print("TEST 2: Server Lifecycle")
    print("=" * 70)

    with ServerManager() as sm:
        url = sm.start_server(kill_conflicts=True)
        print(f"✅ Server started: {url}")

        # Health check
        assert sm.health_check(), "Health check failed"
        print("✅ Health check passed")

    print("✅ Server stopped automatically")


def test_screenshot_capture():
    """Test screenshot with validation"""
    print("\n" + "=" * 70)
    print("TEST 3: Screenshot Capture & Validation")
    print("=" * 70)

    with ServerManager() as sm:
        url = sm.start_server(kill_conflicts=True)

        # Capture screenshot
        screenshot = capture_screenshot_sync(url, "desktop", validate=True)
        print(f"✅ Screenshot captured: {screenshot['viewport']}")

        # Validate
        is_valid, msg = validate_screenshot(screenshot)
        assert is_valid, f"Validation failed: {msg}"
        print(f"✅ Screenshot validated: {msg}")


def test_cost_estimation():
    """Test cost calculation"""
    print("\n" + "=" * 70)
    print("TEST 4: Cost Estimation")
    print("=" * 70)

    cost_info = estimate_cost(6, detail_level="high", model="gpt-4o-mini")
    print_cost_estimate(cost_info)

    assert cost_info["num_screenshots"] == 6
    assert cost_info["estimated_cost"] > 0
    print("✅ Cost estimation working")


def test_port_conflict_resolution():
    """Test killing conflicting processes"""
    print("\n" + "=" * 70)
    print("TEST 5: Port Conflict Resolution")
    print("=" * 70)

    # Start first server
    sm1 = ServerManager()
    sm1.start_server(port=8085, kill_conflicts=False)
    print("✅ First server started on port 8085")

    # Try to start second server on same port with kill_conflicts=True
    sm2 = ServerManager()
    try:
        sm2.start_server(port=8085, kill_conflicts=True)
        print("✅ Second server took over port 8085")
        sm2.stop_server()
    except Exception as e:
        sm1.stop_server()
        raise e

    print("✅ Port conflict resolution working")


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("🧪 PHASE 1 RELIABILITY TESTS")
    print("=" * 70)

    tests = [
        ("Port Detection", test_port_detection),
        ("Server Lifecycle", test_server_lifecycle),
        ("Screenshot Capture", test_screenshot_capture),
        ("Cost Estimation", test_cost_estimation),
        ("Port Conflict Resolution", test_port_conflict_resolution),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ TEST FAILED: {name}")
            print(f"   Error: {e}")
            failed += 1

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"   ✅ Passed: {passed}/{len(tests)}")
    print(f"   ❌ Failed: {failed}/{len(tests)}")
    print("=" * 70 + "\n")

    if failed > 0:
        sys.exit(1)
    else:
        print("🎉 ALL TESTS PASSED!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
