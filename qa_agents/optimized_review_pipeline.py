"""
Optimized Multi-Agent Review Pipeline
Token-efficient sequential expert chain with triage
and intelligent summarization
"""
import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from agents import Agent, Runner
from pydantic import BaseModel

from expert_agents import EXPERT_AGENTS


# ============================================================================
# Data Models for Structured Output
# ============================================================================

@dataclass
class Issue:
    """Single actionable issue"""
    id: str  # e.g., "MOBILE-001"
    title: str  # Short description
    severity: str  # CRITICAL | IMPORTANT | MINOR
    confidence: int  # 1-7 (number of experts who agree)
    devices_affected: List[str]  # ["mobile-portrait", "tablet-portrait"]
    description: str  # What's wrong
    why_it_matters: str  # User impact
    how_to_fix: str  # Specific action
    file_locations: List[str]  # ["src/assets/css/main.css:42"]
    expert_consensus: Dict[str, bool]  # Which experts flagged it


class TriageResult(BaseModel):
    """Quick assessment of all devices"""
    device: str
    status: str  # CRITICAL | HAS_ISSUES | MINOR | PERFECT | SKIP_SIMILAR
    estimated_issue_count: int
    needs_deep_review: bool
    similar_to_device: Optional[str]  # If SKIP_SIMILAR


class ExpertFinding(BaseModel):
    """Finding from a single expert"""
    expert_name: str
    severity: str
    finding: str
    agrees_with_previous: List[str]  # IDs of previous findings this validates
    adds_new_insight: bool


class DeviceSummary(BaseModel):
    """Summary for one device after expert review"""
    device: str
    critical_issues: List[str]
    important_issues: List[str]
    minor_issues: List[str]
    expert_agreement: Dict[str, int]  # issue -> num experts who flagged it


# ============================================================================
# Phase 1: Triage Agent
# ============================================================================

TRIAGE_AGENT = Agent(
    name="Triage Screener",
    model="gpt-4o-mini",
    instructions="""You are a UX triage expert who quickly scans
screenshots to prioritize review effort.

**Your Task:**
Quickly assess each device screenshot and categorize its severity:

1. **CRITICAL** - Major usability problems (hero below fold,
   contrast failures, broken layout)
2. **HAS_ISSUES** - Notable problems that need expert review
   (spacing, hierarchy, minor contrast)
3. **MINOR** - Small refinements (could skip if budget-limited)
4. **PERFECT** - Looks good, no obvious issues
5. **SKIP_SIMILAR** - Looks identical to another device (specify which)

**Output Format:**
- status: One of the 5 categories above
- estimated_issue_count: Your rough count of issues (0-10)
- needs_deep_review: true/false
- similar_to_device: If SKIP_SIMILAR, which device does this match?

**Rules:**
- Mobile-portrait is ALWAYS worth deep review (most users)
- Desktop is ALWAYS worth deep review (reference viewport)
- If tablet-landscape looks identical to desktop, mark SKIP_SIMILAR
- Flag CRITICAL if: hero not visible, text unreadable, broken layout
- Be fast - this is a screening pass, not deep analysis
""",
    response_format=TriageResult
)


async def triage_all_devices(
    screenshots: Dict[str, Path]
) -> Dict[str, TriageResult]:
    """
    Phase 1: Quick triage of all devices
    Cost: ~7 reviews × 300 tokens = ~2100 tokens = $0.03
    """
    print("\n🎯 PHASE 1: TRIAGE")
    print("=" * 70)

    results = {}
    for device, screenshot_path in screenshots.items():
        print(f"Screening {device}...", end=" ")

        runner = Runner(agent=TRIAGE_AGENT)
        response = await runner.run(
            f"Assess this {device} screenshot for UX issues",
            attachments=[str(screenshot_path)]
        )

        triage = response.data
        results[device] = triage

        status_emoji = {
            "CRITICAL": "🔴",
            "HAS_ISSUES": "🟡",
            "MINOR": "🔵",
            "PERFECT": "✅",
            "SKIP_SIMILAR": "⏭️"
        }
        print(f"{status_emoji.get(triage.status, '?')} {triage.status}")

    return results


# ============================================================================
# Phase 2: Sequential Expert Chain
# ============================================================================

async def sequential_expert_review(
    device: str,
    screenshot_path: Path,
    previous_findings: List[ExpertFinding] = None
) -> List[ExpertFinding]:
    """
    Phase 2: Run experts sequentially, each building on previous findings
    Cost per device: ~7 experts × 800 tokens = ~5600 tokens = $0.08
    """
    if previous_findings is None:
        previous_findings = []

    findings = []

    # Order experts by dependency:
    # Layout → Typography → Contrast → Hierarchy
    # → Accessibility → Conversion → Brand
    expert_order = [
        "layout_expert",
        "typography_expert",
        "contrast_expert",
        "hierarchy_expert",
        "accessibility_expert",
        "conversion_expert",
        "brand_expert"
    ]

    for expert_name in expert_order:
        expert = EXPERT_AGENTS[expert_name]

        # Build context from previous experts
        context = ""
        if findings:
            context = "\n\n**Previous Expert Findings:**\n"
            # Last 3 to keep prompt short
            for i, finding in enumerate(findings[-3:], 1):
                context += (
                    f"{i}. {finding.expert_name}: {finding.finding}\n"
                )
            context += (
                "\n**Your task:** Build on these findings. "
                "If you agree with a previous finding, "
                "reference it (e.g., 'Agrees with #1'). "
                "Focus on NEW insights from your specialty."
            )

        prompt = (
            f"Analyze this {device} screenshot from your "
            f"expert perspective.\n\n{context}\n\n"
            "Provide your specialized analysis. Be concise - "
            "other experts have already covered some issues."
        )

        runner = Runner(agent=expert)
        response = await runner.run(prompt, attachments=[str(screenshot_path)])

        finding = ExpertFinding(
            expert_name=expert.name,
            severity=response.data.severity,
            finding=response.data.summary,
            agrees_with_previous=[],  # Could parse from response
            adds_new_insight=True
        )
        findings.append(finding)

        print(f"  ✓ {expert.name}")

    return findings


# ============================================================================
# Phase 3: Consensus Summarization
# ============================================================================

SUMMARIZER_AGENT = Agent(
    name="Consensus Summarizer",
    model="gpt-4o-mini",
    instructions="""You are an expert at extracting actionable issues
from multiple expert reviews.

**Your Task:**
Given findings from 7 UX experts, identify the UNIQUE, ACTIONABLE issues.

**Rules:**
1. **Deduplicate:** "Hero below fold" from 3 experts
   = ONE issue with confidence=3
2. **Merge similar:** "CTA too small" + "Button undersized"
   = SAME ISSUE
3. **Prioritize by consensus:** 3+ experts = CRITICAL,
   2 experts = IMPORTANT, 1 expert = MINOR
4. **Be specific:** Not "fix spacing" but "Increase .hero padding
   from 20px to 40px"
5. **Include WHY:** Explain user impact, not just what's wrong
6. **Include HOW:** Specific CSS/HTML changes needed
7. **Include WHERE:** File paths and line numbers if possible

**Output Format:**
Return a list of issues with:
- severity (CRITICAL/IMPORTANT/MINOR)
- title (short, actionable)
- description (what's wrong)
- why_it_matters (user impact)
- how_to_fix (specific action)
- confidence (1-7, how many experts flagged it)

**Focus:**
- 3-5 critical issues maximum (most important)
- 5-10 important issues
- Can skip minor issues to save tokens
""",
    response_format=DeviceSummary
)


async def summarize_device_findings(
    device: str,
    expert_findings: List[ExpertFinding]
) -> DeviceSummary:
    """
    Phase 3: Extract unique actionable issues from expert findings
    Cost per device: ~1000 tokens = $0.015
    """
    findings_text = "\n\n".join([
        f"**{f.expert_name}** (Severity: {f.severity}):\n{f.finding}"
        for f in expert_findings
    ])

    runner = Runner(agent=SUMMARIZER_AGENT)
    response = await runner.run(
        f"Extract unique actionable issues for {device}:\n\n{findings_text}"
    )

    return response.data


# ============================================================================
# Phase 4: Cross-Device Pattern Detection
# ============================================================================

PATTERN_AGENT = Agent(
    name="Pattern Detector",
    model="gpt-4o-mini",
    instructions="""You find patterns across multiple device summaries.

**Your Task:**
Given summaries for multiple devices, identify:

1. **Universal Issues:** Problems on ALL devices
   (fundamental design flaw)
2. **Mobile-Specific:** Only on mobile-portrait/mobile-landscape
   (touch, small screen)
3. **Desktop-Specific:** Only on desktop/wide-desktop
   (large screen, mouse)
4. **Responsive Breakpoints:** Issues that appear/disappear
   at specific sizes

**Focus:**
- Prioritize issues affecting multiple devices (wider impact)
- Flag responsive-specific problems (CSS media query issues)
- Identify root causes (one CSS fix might solve multiple device issues)

**Output:**
- universal_issues: List[str]
- mobile_only: List[str]
- desktop_only: List[str]
- responsive_breakpoint_issues: List[str]
- recommended_fix_order: List[str] (which issues to fix first)
""",
    response_format=dict
)


async def detect_cross_device_patterns(
    device_summaries: Dict[str, DeviceSummary]
) -> Dict:
    """
    Phase 4: Find patterns across devices
    Cost: ~2000 tokens = $0.03
    """
    print("\n🌐 PHASE 4: CROSS-DEVICE PATTERN DETECTION")
    print("=" * 70)

    summaries_text = "\n\n".join([
        (f"**{device}:**\n"
         f"- Critical: {', '.join(summary.critical_issues)}\n"
         f"- Important: {', '.join(summary.important_issues)}")
        for device, summary in device_summaries.items()
    ])

    runner = Runner(agent=PATTERN_AGENT)
    response = await runner.run(
        f"Identify patterns across these device reviews:\n\n{summaries_text}"
    )

    return response.data


# ============================================================================
# Phase 5: Final Report Generation
# ============================================================================

def generate_actionable_report(
    device_summaries: Dict[str, DeviceSummary],
    cross_device_patterns: Dict,
    output_dir: Path
) -> Path:
    """
    Generate human-readable AND AI-parseable final report
    """
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # JSON output (AI-friendly)
    critical_count = sum(
        len(s.critical_issues) for s in device_summaries.values()
    )
    important_count = sum(
        len(s.important_issues) for s in device_summaries.values()
    )

    json_report = {
        "timestamp": timestamp,
        "executive_summary": {
            "total_devices_reviewed": len(device_summaries),
            "critical_issues": critical_count,
            "important_issues": important_count,
        },
        "device_summaries": {
            k: asdict(v) for k, v in device_summaries.items()
        },
        "cross_device_patterns": cross_device_patterns,
    }

    json_path = output_dir / f"REVIEW-{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=2)

    # Markdown output (Human-friendly)
    md_path = output_dir / f"REVIEW-{timestamp}.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"""# UX Review Report
**Generated:** {timestamp}

## 📊 Executive Summary

- **Devices Reviewed:** {len(device_summaries)}
- **Critical Issues:** {critical_count}
- **Important Issues:** {important_count}

---

## 🔴 ACTION REQUIRED: Critical Issues

""")

        # Group critical issues by priority
        all_critical = []
        for device, summary in device_summaries.items():
            for issue in summary.critical_issues:
                confidence = summary.expert_agreement.get(issue, 1)
                all_critical.append((device, issue, confidence))

        # Sort by confidence (most experts agree = highest priority)
        all_critical.sort(key=lambda x: x[2], reverse=True)

        # Top 10
        for i, (device, issue, confidence) in enumerate(
            all_critical[:10], 1
        ):
            f.write(f"""
### {i}. {issue}
- **Device(s):** {device}
- **Confidence:** {confidence}/7 experts agree
- **Why it matters:** [See JSON for full details]
- **How to fix:** [See JSON for full details]

""")

        f.write("""
---

## 🟡 Important Issues

[See JSON file for complete list]

---

## 🌐 Cross-Device Patterns

""")

        if "universal_issues" in cross_device_patterns:
            f.write("### Universal (All Devices)\n")
            for issue in cross_device_patterns["universal_issues"]:
                f.write(f"- {issue}\n")

        f.write(f"""

---

## 📂 Files

- **Full Details:** `{json_path.name}`
- **Human Summary:** `{md_path.name}`

---

## 🚀 Recommended Fix Order

1. Fix universal issues first (affects all devices)
2. Fix mobile-critical issues (most users)
3. Fix desktop issues
4. Fix minor refinements

**Estimated Development Time:** [Calculate based on issue count]
**Expected Impact:** [High/Medium/Low for each issue]
""")

    print("\n📄 Reports generated:")
    print(f"  - Human-readable: {md_path}")
    print(f"  - Machine-readable: {json_path}")

    return md_path


# ============================================================================
# Main Pipeline
# ============================================================================

async def run_optimized_review(
    screenshots_dir: Path,
    url: str = "http://localhost:8080"
):
    """
    Token-optimized multi-agent review pipeline

    Estimated cost: ~$0.20 (vs $0.73 for parallel approach)
    Estimated time: 3-4 minutes (sequential, but focused)
    """
    print("\n" + "=" * 70)
    print("🤖 OPTIMIZED MULTI-AGENT REVIEW PIPELINE")
    print("=" * 70)

    # Assume screenshots already captured
    screenshots = {
        "mobile-portrait": screenshots_dir / "mobile-portrait.png",
        "mobile-landscape": screenshots_dir / "mobile-landscape.png",
        "tablet-portrait": screenshots_dir / "tablet-portrait.png",
        "tablet-landscape": screenshots_dir / "tablet-landscape.png",
        "laptop": screenshots_dir / "laptop.png",
        "desktop": screenshots_dir / "desktop.png",
        "wide-desktop": screenshots_dir / "wide-desktop.png",
    }

    # Phase 1: Triage (~$0.03, 30 seconds)
    triage_results = await triage_all_devices(screenshots)

    # Determine which devices need deep review
    devices_to_review = [
        device for device, result in triage_results.items()
        if result.needs_deep_review and result.status != "SKIP_SIMILAR"
    ]

    devices_list = ', '.join(devices_to_review)
    print(f"\n📋 Devices selected for deep review: {devices_list}")
    skipped = 7 - len(devices_to_review)
    print(f"💰 Cost savings: Skipping {skipped} devices")

    # Phase 2-3: Sequential review + summarization (~$0.10 per device)
    print("\n🔍 PHASE 2-3: EXPERT REVIEW + SUMMARIZATION")
    print("=" * 70)

    device_summaries = {}
    for device in devices_to_review:
        print(f"\n📱 Reviewing {device}...")

        # Sequential expert chain
        expert_findings = await sequential_expert_review(
            device, screenshots[device]
        )

        # Consensus summarization
        summary = await summarize_device_findings(device, expert_findings)
        device_summaries[device] = summary

        crit = len(summary.critical_issues)
        imp = len(summary.important_issues)
        print(f"  ✅ Found {crit} critical, {imp} important issues")

    # Phase 4: Cross-device patterns (~$0.03)
    cross_device_patterns = await detect_cross_device_patterns(
        device_summaries
    )

    # Phase 5: Generate reports
    print("\n📊 PHASE 5: GENERATING REPORTS")
    print("=" * 70)
    report_path = generate_actionable_report(
        device_summaries,
        cross_device_patterns,
        screenshots_dir
    )

    print("\n" + "=" * 70)
    print("✅ REVIEW COMPLETE")
    print("=" * 70)
    print(f"\n📖 Read the report: {report_path}")
    print("💰 Estimated cost: $0.15-0.25 (vs $0.73 parallel)")
    print("⏱️  Time saved: ~50% fewer tokens, smarter analysis")

    return report_path


# ============================================================================
# CLI Entry Point
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python optimized_review_pipeline.py <screenshots_dir>")
        sys.exit(1)

    screenshots_dir = Path(sys.argv[1])
    if not screenshots_dir.exists():
        print(f"Error: {screenshots_dir} does not exist")
        sys.exit(1)

    asyncio.run(run_optimized_review(screenshots_dir))
