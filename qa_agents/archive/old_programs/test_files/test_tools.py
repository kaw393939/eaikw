#!/usr/bin/env python3
"""
Quick test of LLM Quality Gate without git integration
"""
import asyncio
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


async def test():
    print("🧪 Testing LLM Quality Gate Tools\n")

    # Test 1: Run linters directly
    print("1️⃣ Testing linters...")

    linters = [
        ("ESLint", ["npm", "run", "lint:js"]),
        ("Stylelint", ["npm", "run", "lint:css"]),
        ("Markdownlint", ["npm", "run", "lint:md"]),
    ]

    for name, cmd in linters:
        result = subprocess.run(cmd, capture_output=True, text=True)
        status = "✅ PASS" if result.returncode == 0 else "❌ FAIL"
        print(f"   {name}: {status}")
        if result.returncode != 0 and result.stdout:
            # Show first 2 lines of output
            lines = result.stdout.split("\n")[:2]
            for line in lines:
                if line.strip():
                    print(f"      {line[:70]}")

    # Test 2: Check git status
    print("\n2️⃣ Testing git integration...")
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True
    )

    changed = result.stdout.strip().split("\n") if result.stdout else []

    if changed and changed != [""]:
        print(f"   Found {len(changed)} staged files:")
        for f in changed[:5]:
            print(f"      - {f}")
    else:
        print("   No files staged")

    print("\n✅ Tool tests complete!")
    print("\n📋 Next steps:")
    print("   1. Stage some files: git add <files>")
    print("   2. Run full quality gate: qa_agents/venv/bin/python3 qa_agents/quality_gate.py")


if __name__ == "__main__":
    asyncio.run(test())
