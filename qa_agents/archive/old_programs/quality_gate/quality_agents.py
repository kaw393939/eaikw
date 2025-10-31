"""LLM Agent definitions for quality enforcement"""
from pydantic import BaseModel
from typing import Literal, List, Optional
from agents import Agent


# ============================================================================
# Output Models
# ============================================================================

class LintIssue(BaseModel):
    """Represents a single linting issue"""
    file: str
    line: Optional[int] = None
    severity: Literal["critical", "important", "minor"]
    tool: str  # eslint, stylelint, markdownlint, etc.
    message: str
    rule: Optional[str] = None


class FixSuggestion(BaseModel):
    """Represents a suggested fix"""
    file: str
    line: Optional[int] = None
    old_code: str
    new_code: str
    reasoning: str
    confidence: float  # 0.0-1.0


class LintAnalysisResult(BaseModel):
    """Output from Lint Agent"""
    critical_issues: List[LintIssue]
    important_issues: List[LintIssue]
    minor_issues: List[LintIssue]
    fix_suggestions: List[FixSuggestion]
    summary: str


class AutoFixResult(BaseModel):
    """Output from Auto-Fix Agent"""
    fixes_applied: int
    successful_fixes: List[str]  # File paths
    failed_fixes: List[str]
    remaining_issues: List[LintIssue]
    recommendation: Literal["commit", "retry", "manual_review"]
    reasoning: str


class QualityReport(BaseModel):
    """Final output from Quality Judge Agent"""
    verdict: Literal["pass", "needs_improvement", "fail"]
    score: int  # 0-100
    critical_issues: List[str]
    warnings: List[str]
    auto_fixes_applied: int
    recommendation: str
    detailed_analysis: str


# ============================================================================
# Agent Definitions
# ============================================================================

# LINT AGENT: Analyzes linter output and categorizes issues
lint_agent = Agent[LintAnalysisResult](
    name="Lint Quality Agent",
    model="gpt-4o-mini",
    instructions="""
    You are a code quality expert analyzing linter output from ESLint, Stylelint, and Markdownlint.

    Your responsibilities:
    1. Parse linter output and categorize issues by severity
    2. Generate specific fix suggestions for critical issues
    3. Provide exact code replacements with line numbers

    Severity Classification:
    - CRITICAL: Syntax errors, BEM violations, accessibility issues, broken functionality
    - IMPORTANT: Best practices, maintainability, performance concerns
    - MINOR: Formatting, comments, optional improvements

    For each CRITICAL issue, you MUST provide:
    - Exact file path
    - Line number (if available)
    - Old code snippet (with context - at least 3 lines)
    - New code with fix applied
    - Clear reasoning for the fix
    - Confidence score (0.0-1.0)

    BEM Compliance Rules:
    - Block: .block-name (lowercase, kebab-case)
    - Element: .block-name__element-name (double underscore)
    - Modifier: .block-name--modifier-name (double dash)
    - NO camelCase, NO single underscores

    Be precise with code snippets - include enough context for exact matching.
    """,
    output_type=LintAnalysisResult,
)


# AUTO-FIX AGENT: Applies fixes iteratively
auto_fix_agent = Agent[AutoFixResult](
    name="Auto-Fix Agent",
    model="gpt-4o-mini",
    instructions="""
    You are an automated code repair agent. Your goal is to fix code quality issues automatically.

    Strategy:
    1. Review fix suggestions from Lint Agent
    2. Apply fixes in order of confidence (highest first)
    3. Only apply fixes with confidence >= 0.8
    4. After each fix, verify the change was successful
    5. Re-run linters to check for new issues
    6. Maximum 3 fix attempts per file

    When applying fixes:
    - Use the apply_fix tool with exact old_code and new_code
    - Include surrounding context in old_code for accurate matching
    - After applying, run run_prettier_on_file to ensure formatting
    - Track which fixes succeeded vs failed

    Decision Logic:
    - If all critical issues fixed → recommend "commit"
    - If some issues fixed but critical remain → recommend "retry" (max 3 total attempts)
    - If can't fix automatically → recommend "manual_review"

    Be cautious: Only apply fixes you're confident about. It's better to recommend manual review than apply incorrect fixes.
    """,
    output_type=AutoFixResult,
)


# QUALITY JUDGE AGENT: Makes final commit decision
quality_judge_agent = Agent[QualityReport](
    name="Quality Judge",
    model="gpt-4o-mini",
    instructions="""
    You are the final arbiter of code quality. Review all analysis and make the commit decision.

    Quality Standards (all must be met for PASS):
    1. Zero critical issues (syntax errors, BEM violations, WCAG failures)
    2. Maximum 5 warnings
    3. All files properly formatted
    4. BEM naming conventions followed 100%
    5. Accessibility standards met (WCAG 2.1 Level AA)

    Scoring (0-100):
    - Start at 100
    - Subtract 20 per critical issue
    - Subtract 5 per important issue
    - Subtract 1 per minor issue
    - Minimum score: 0

    Verdict:
    - PASS (score >= 95, zero critical issues)
      → Clear to commit

    - NEEDS_IMPROVEMENT (score 70-94, 1-3 critical issues)
      → Auto-fix attempted but issues remain
      → Provide specific next steps

    - FAIL (score < 70, >3 critical issues)
      → Block commit completely
      → Detailed remediation plan required

    Your response MUST include:
    1. Clear verdict (pass/needs_improvement/fail)
    2. Numeric quality score
    3. List of remaining critical issues (if any)
    4. Specific actionable recommendations
    5. Detailed analysis of what's good and what needs work

    Be strict but constructive. The goal is maintaining high quality standards while being helpful.
    """,
    output_type=QualityReport,
)
