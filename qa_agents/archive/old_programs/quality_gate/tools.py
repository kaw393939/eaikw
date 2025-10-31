"""Tools for LLM agents to interact with the codebase"""
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

# Import from the installed openai-agents package
from agents import function_tool

from config import PROJECT_ROOT


@function_tool
async def run_linters() -> Dict[str, str]:
    """
    Run all linters (ESLint, Stylelint, Markdownlint) and return results.

    Returns:
        Dictionary with linter names as keys and output as values
    """
    results = {}

    # ESLint
    eslint = subprocess.run(
        ["npm", "run", "lint:js"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    results["eslint"] = {
        "stdout": eslint.stdout,
        "stderr": eslint.stderr,
        "exit_code": eslint.returncode,
        "passed": eslint.returncode == 0
    }

    # Stylelint
    stylelint = subprocess.run(
        ["npm", "run", "lint:css"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    results["stylelint"] = {
        "stdout": stylelint.stdout,
        "stderr": stylelint.stderr,
        "exit_code": stylelint.returncode,
        "passed": stylelint.returncode == 0
    }

    # Markdownlint
    markdownlint = subprocess.run(
        ["npm", "run", "lint:md"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    results["markdownlint"] = {
        "stdout": markdownlint.stdout,
        "stderr": markdownlint.stderr,
        "exit_code": markdownlint.returncode,
        "passed": markdownlint.returncode == 0
    }

    return results


@function_tool
async def get_git_diff() -> str:
    """
    Get the git diff of staged changes.

    Returns:
        The diff output as a string
    """
    result = subprocess.run(
        ["git", "diff", "--cached"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    return result.stdout


@function_tool
async def get_changed_files() -> List[str]:
    """
    Get list of files in staging area.

    Returns:
        List of file paths relative to project root
    """
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    return result.stdout.strip().split("\n") if result.stdout else []


@function_tool
async def read_file_content(file_path: str) -> str:
    """
    Read the content of a file.

    Args:
        file_path: Path to file relative to project root

    Returns:
        File content as string
    """
    full_path = PROJECT_ROOT / file_path
    if not full_path.exists():
        return f"Error: File {file_path} not found"

    try:
        return full_path.read_text()
    except Exception as e:
        return f"Error reading file: {str(e)}"


@function_tool
async def apply_fix(file_path: str, old_code: str, new_code: str, line_number: Optional[int] = None) -> Dict[str, any]:
    """
    Apply a code fix to a file and stage the changes.

    Args:
        file_path: Path to file relative to project root
        old_code: Code to replace (must match exactly)
        new_code: New code to insert
        line_number: Optional line number for reference

    Returns:
        Dictionary with success status and message
    """
    full_path = PROJECT_ROOT / file_path

    if not full_path.exists():
        return {
            "success": False,
            "message": f"File {file_path} not found"
        }

    try:
        content = full_path.read_text()

        if old_code not in content:
            return {
                "success": False,
                "message": f"Old code not found in {file_path}",
                "hint": "Make sure to include exact whitespace and context"
            }

        # Apply the fix
        new_content = content.replace(old_code, new_code, 1)  # Replace only first occurrence
        full_path.write_text(new_content)

        # Stage the file
        subprocess.run(
            ["git", "add", file_path],
            cwd=PROJECT_ROOT,
            check=True
        )

        return {
            "success": True,
            "message": f"Applied fix to {file_path}",
            "line_number": line_number
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error applying fix: {str(e)}"
        }


@function_tool
async def run_prettier_on_file(file_path: str) -> Dict[str, any]:
    """
    Run Prettier on a specific file to auto-format.

    Args:
        file_path: Path to file relative to project root

    Returns:
        Dictionary with success status
    """
    result = subprocess.run(
        ["npx", "prettier", "--write", file_path],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        # Stage the formatted file
        subprocess.run(["git", "add", file_path], cwd=PROJECT_ROOT)

        return {
            "success": True,
            "message": f"Formatted {file_path} with Prettier"
        }
    else:
        return {
            "success": False,
            "message": f"Prettier failed: {result.stderr}"
        }


@function_tool
async def check_bem_compliance(css_content: str) -> Dict[str, any]:
    """
    Check CSS for BEM naming convention compliance.

    Args:
        css_content: CSS file content to check

    Returns:
        Dictionary with violations and suggestions
    """
    violations = []

    # Simple BEM validation patterns
    lines = css_content.split("\n")
    for i, line in enumerate(lines, 1):
        # Check for class selectors
        if line.strip().startswith("."):
            class_name = line.strip().split("{")[0].split()[0].strip(".")

            # Check for common non-BEM patterns
            if "_" in class_name and "__" not in class_name:
                violations.append({
                    "line": i,
                    "class": class_name,
                    "issue": "Uses single underscore instead of double underscore for element",
                    "suggestion": f"Use double underscore: {class_name.replace('_', '__', 1)}"
                })

            # Check for camelCase (should be kebab-case)
            if any(c.isupper() for c in class_name):
                violations.append({
                    "line": i,
                    "class": class_name,
                    "issue": "Uses camelCase instead of kebab-case",
                    "suggestion": "Convert to kebab-case"
                })

    return {
        "compliant": len(violations) == 0,
        "violations": violations,
        "total_violations": len(violations)
    }
