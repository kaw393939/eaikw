#!/usr/bin/env python3
"""
LLM-Powered Quality Gate Pre-Commit Hook

This script runs as a git pre-commit hook and uses LLM agents to:
1. Analyze linter output and categorize issues
2. Attempt automatic fixes for critical issues
3. Make final commit decision based on quality standards
"""
import asyncio
import sys
import json
from datetime import datetime
from pathlib import Path

# Add qa_agents directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import from installed openai-agents package
from agents import Runner, trace

# Import from local qa_agents package
from config import ENABLE_COST_TRACKING
from quality_agents import (
    lint_agent,
    auto_fix_agent,
    quality_judge_agent,
    LintAnalysisResult,
    AutoFixResult,
    QualityReport,
)
from utils import (
    run_linters_sync,
    get_changed_files_sync,
)


class CostTracker:
    """Track LLM API costs"""

    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.cost_per_1m_input = 0.15  # gpt-4o-mini
        self.cost_per_1m_output = 0.60  # gpt-4o-mini

    def add_usage(self, input_tokens: int, output_tokens: int):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

    @property
    def total_cost(self) -> float:
        input_cost = (self.total_input_tokens / 1_000_000) * self.cost_per_1m_input
        output_cost = (
            self.total_output_tokens / 1_000_000
        ) * self.cost_per_1m_output
        return input_cost + output_cost

    def report(self) -> str:
        return (
            f"Token Usage: {self.total_input_tokens:,} input, "
            f"{self.total_output_tokens:,} output | "
            f"Cost: ${self.total_cost:.4f}"
        )


async def run_quality_gate():
    """Main quality gate orchestration"""

    print("\n" + "=" * 70)
    print("🤖 LLM QUALITY GATE")
    print("=" * 70)

    cost_tracker = CostTracker() if ENABLE_COST_TRACKING else None
    conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Step 0: Get changed files
    print("\n📋 Checking staged files...")
    changed_files_result = get_changed_files_sync()

    if not changed_files_result or changed_files_result == [""]:
        print("✅ No files staged for commit")
        return 0

    print(f"   Files staged: {len(changed_files_result)}")
    for f in changed_files_result[:10]:  # Show first 10
        print(f"   - {f}")
    if len(changed_files_result) > 10:
        print(f"   ... and {len(changed_files_result) - 10} more")

    # Step 1: Run linters (only on changed files)
    print("\n🔍 Running linters...")
    linter_results = run_linters_sync(changed_files_result)

    # Show what was checked
    for tool, result in linter_results.items():
        if "skipped" in result:
            print(f"   {tool}: ⏭️  Skipped ({result['skipped']})")
        elif result.get("files_checked", 0) > 0:
            status = "✅" if result["passed"] else "❌"
            print(f"   {tool}: {status} ({result['files_checked']} files)")

    # Check if all passed
    all_passed = all(result["passed"] for result in linter_results.values())

    if all_passed:
        print("✅ All linters passed!")
        print("\n" + "=" * 70)
        print("✅ QUALITY GATE: PASSED")
        print("=" * 70)
        return 0

    # Step 2: LLM Lint Agent Analysis
    print("\n🤖 Analyzing linter output with LLM...")

    with trace("Lint Analysis", group_id=conversation_id):
        # Prepare input for agent
        lint_input = (
            f"Analyze these linter results and categorize issues:\n\n"
            f"Changed files: {', '.join(changed_files_result)}\n\n"
        )

        for tool, result in linter_results.items():
            lint_input += f"\n{tool.upper()} Results:\n"
            lint_input += f"Exit code: {result['exit_code']}\n"
            if result["stdout"]:
                lint_input += f"Output:\n{result['stdout']}\n"
            if result["stderr"]:
                lint_input += f"Errors:\n{result['stderr']}\n"

        lint_result = await Runner.run(
            lint_agent, [{"content": lint_input, "role": "user"}]
        )

        analysis: LintAnalysisResult = lint_result.final_output_as(
            LintAnalysisResult
        )

    print(f"\n📊 Analysis Results:")
    print(f"   Critical: {len(analysis.critical_issues)}")
    print(f"   Important: {len(analysis.important_issues)}")
    print(f"   Minor: {len(analysis.minor_issues)}")
    print(f"   Fix suggestions: {len(analysis.fix_suggestions)}")

    if analysis.critical_issues:
        print("\n❌ Critical Issues Found:")
        for issue in analysis.critical_issues[:5]:  # Show first 5
            print(
                f"   [{issue.severity.upper()}] {issue.file}:{issue.line or '?'}"
            )
            print(f"      {issue.message}")
        if len(analysis.critical_issues) > 5:
            print(
                f"   ... and {len(analysis.critical_issues) - 5} more"
            )

    # Step 3: Auto-Fix Agent (if fixes suggested)
    if analysis.fix_suggestions:
        print(
            f"\n🔧 Attempting {len(analysis.fix_suggestions)} automatic fixes..."
        )

        with trace("Auto-Fix", group_id=conversation_id):
            fix_input = (
                f"Apply these fixes:\n\n"
                f"Analysis: {json.dumps(analysis.model_dump(), indent=2)}\n\n"
                f"Changed files: {', '.join(changed_files_result)}"
            )

            fix_result = await Runner.run(
                auto_fix_agent, [{"content": fix_input, "role": "user"}]
            )

            auto_fix: AutoFixResult = fix_result.final_output_as(AutoFixResult)

        print(f"\n✨ Auto-Fix Results:")
        print(f"   Fixes applied: {auto_fix.fixes_applied}")
        print(f"   Successful: {len(auto_fix.successful_fixes)}")
        print(f"   Failed: {len(auto_fix.failed_fixes)}")
        print(f"   Recommendation: {auto_fix.recommendation}")

        if auto_fix.successful_fixes:
            print("\n   ✅ Successfully fixed:")
            for f in auto_fix.successful_fixes[:5]:
                print(f"      - {f}")

        if auto_fix.failed_fixes:
            print("\n   ⚠️  Failed to fix:")
            for f in auto_fix.failed_fixes[:5]:
                print(f"      - {f}")

        # If fixes were applied, re-run linters
        if auto_fix.fixes_applied > 0:
            print("\n🔄 Re-running linters after fixes...")
            linter_results = run_linters_sync(changed_files_result)

    # Step 4: Final Quality Judge
    print("\n⚖️  Final quality judgment...")

    with trace("Quality Judge", group_id=conversation_id):
        judge_input = (
            f"Make final commit decision:\n\n"
            f"Lint Analysis:\n{json.dumps(analysis.model_dump(), indent=2)}\n\n"
        )

        if analysis.fix_suggestions:
            judge_input += (
                f"Auto-Fix Results:\n"
                f"{json.dumps(auto_fix.model_dump(), indent=2)}\n\n"
            )

        judge_input += f"Final Linter Results:\n"
        for tool, result in linter_results.items():
            judge_input += f"{tool}: {'✅ PASSED' if result['passed'] else '❌ FAILED'}\n"

        judge_result = await Runner.run(
            quality_judge_agent, [{"content": judge_input, "role": "user"}]
        )

        report: QualityReport = judge_result.final_output_as(QualityReport)

    # Display final report
    print("\n" + "=" * 70)
    print(f"📋 QUALITY REPORT")
    print("=" * 70)
    print(f"Verdict: {report.verdict.upper()}")
    print(f"Score: {report.score}/100")
    print(f"Auto-fixes applied: {report.auto_fixes_applied}")

    if report.critical_issues:
        print(f"\n❌ Critical Issues ({len(report.critical_issues)}):")
        for issue in report.critical_issues:
            print(f"   - {issue}")

    if report.warnings:
        print(f"\n⚠️  Warnings ({len(report.warnings)}):")
        for warning in report.warnings[:5]:
            print(f"   - {warning}")

    print(f"\n💡 Recommendation:")
    print(f"   {report.recommendation}")

    print(f"\n📝 Analysis:")
    print(f"   {report.detailed_analysis}")

    # Cost tracking
    if cost_tracker:
        print(f"\n💰 {cost_tracker.report()}")

    # Final decision
    print("\n" + "=" * 70)
    if report.verdict == "pass":
        print("✅ QUALITY GATE: PASSED")
        print("=" * 70)
        return 0
    elif report.verdict == "needs_improvement":
        print("⚠️  QUALITY GATE: NEEDS IMPROVEMENT")
        print("=" * 70)
        print("\nCommit blocked. Please review and fix the issues above.")
        return 1
    else:  # fail
        print("❌ QUALITY GATE: FAILED")
        print("=" * 70)
        print("\nCommit blocked. Critical issues must be resolved.")
        return 1


def main():
    """Entry point"""
    try:
        exit_code = asyncio.run(run_quality_gate())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Quality gate interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Quality gate error: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
