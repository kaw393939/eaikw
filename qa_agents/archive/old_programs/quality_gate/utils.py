"""Utility functions for running linters and git commands"""
import subprocess
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).parent.parent


def run_linters_sync(changed_files: List[str]) -> Dict[str, dict]:
    """
    Run linters only on relevant changed files.
    Filters out Python files, venv, node_modules, etc.

    Args:
        changed_files: List of changed file paths

    Returns:
        Dictionary with linter names as keys and output as values
    """
    results = {}

    # Filter files by type
    js_files = [f for f in changed_files if f.endswith(('.js', '.mjs', '.cjs'))
                and not f.startswith(('qa_agents/', 'node_modules/', 'venv/'))]
    css_files = [f for f in changed_files if f.endswith('.css')
                 and not f.startswith(('qa_agents/', 'node_modules/', 'venv/'))]
    md_files = [f for f in changed_files if f.endswith('.md')
                and not f.startswith(('qa_agents/', 'node_modules/', 'venv/', 'references/'))]

    # Only run ESLint if there are JS files
    if js_files:
        eslint = subprocess.run(
            ["npx", "eslint"] + js_files,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        results["eslint"] = {
            "stdout": eslint.stdout,
            "stderr": eslint.stderr,
            "exit_code": eslint.returncode,
            "passed": eslint.returncode == 0,
            "files_checked": len(js_files)
        }
    else:
        results["eslint"] = {
            "stdout": "",
            "stderr": "",
            "exit_code": 0,
            "passed": True,
            "files_checked": 0,
            "skipped": "No JavaScript files changed"
        }

    # Only run Stylelint if there are CSS files
    if css_files:
        stylelint = subprocess.run(
            ["npx", "stylelint"] + css_files,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        results["stylelint"] = {
            "stdout": stylelint.stdout,
            "stderr": stylelint.stderr,
            "exit_code": stylelint.returncode,
            "passed": stylelint.returncode == 0,
            "files_checked": len(css_files)
        }
    else:
        results["stylelint"] = {
            "stdout": "",
            "stderr": "",
            "exit_code": 0,
            "passed": True,
            "files_checked": 0,
            "skipped": "No CSS files changed"
        }

    # Only run Markdownlint if there are MD files (excluding qa_agents and references)
    if md_files:
        markdownlint = subprocess.run(
            ["npx", "markdownlint"] + md_files,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        results["markdownlint"] = {
            "stdout": markdownlint.stdout,
            "stderr": markdownlint.stderr,
            "exit_code": markdownlint.returncode,
            "passed": markdownlint.returncode == 0,
            "files_checked": len(md_files)
        }
    else:
        results["markdownlint"] = {
            "stdout": "",
            "stderr": "",
            "exit_code": 0,
            "passed": True,
            "files_checked": 0,
            "skipped": "No Markdown files changed (or all in excluded dirs)"
        }

    return results


def get_changed_files_sync() -> List[str]:
    """
    Get list of files in staging area, excluding Python/venv/node_modules.

    Returns:
        List of file paths relative to project root (website files only)
    """
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    if not result.stdout:
        return []

    all_files = result.stdout.strip().split("\n")

    # Filter out Python files, venv, node_modules, and references
    website_files = [
        f for f in all_files
        if not f.startswith(('qa_agents/', 'node_modules/', 'venv/', 'references/'))
        and not f.endswith('.pyc')
        and '/__pycache__/' not in f
    ]

    return website_files
