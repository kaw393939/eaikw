"""
Multi-Agent Consensus Review System
Aggregates findings from specialized experts into unified report
"""

import asyncio
from pathlib import Path
from typing import Optional
from agents import Runner
import json
from datetime import datetime

from qa_agents.expert_agents import EXPERT_AGENTS, ExpertReview


class ConsensusReviewSystem:
    """Coordinates multiple expert agents and aggregates their findings"""

    def __init__(self):
        self.experts = EXPERT_AGENTS
        self.reviews = {}

    async def run_expert_review(
        self,
        expert_role: str,
        screenshot_path: str,
        section_name: str,
        context: Optional[str] = None
    ) -> ExpertReview:
        """Run a single expert review"""
        agent = self.experts[expert_role]

        prompt = f"""Review this screenshot of the '{section_name}' section.

{f'Additional Context: {context}' if context else ''}

Analyze from your specialized perspective and provide:
1. Critical issues (must fix - breaks functionality/accessibility)
2. Major issues (should fix - significantly impacts UX)
3. Minor issues (nice to fix - polish items)
4. Quick wins (high impact, low effort fixes)

Be EXTREMELY specific with:
- Exact locations
- Measurements when possible
- CSS property names and values
- Color codes if visible
- Contrast ratios for text

Rate your confidence (0-100) based on screenshot clarity."""

        # Load screenshot as base64
        import base64
        with open(screenshot_path, 'rb') as f:
            screenshot_data = base64.b64encode(f.read()).decode()

        # Run agent with screenshot
        result = await Runner.run(
            agent,
            [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "detail": "high",
                            "image_url": f"data:image/png;base64,{screenshot_data}",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
        )

        # Extract structured output
        if hasattr(result, 'final_output'):
            return result.final_output
        return result

    async def run_parallel_reviews(
        self,
        screenshot_path: str,
        section_name: str,
        context: Optional[str] = None
    ) -> dict[str, ExpertReview]:
        """Run all expert reviews in parallel"""

        print(f"\n🔍 Running multi-expert review of '{section_name}'...")
        print(f"   📸 Screenshot: {screenshot_path}")
        print(f"   👥 Experts: {len(self.experts)}")

        # Create tasks for all experts
        tasks = []
        expert_roles = []

        for role in self.experts.keys():
            task = self.run_expert_review(
                role,
                screenshot_path,
                section_name,
                context
            )
            tasks.append(task)
            expert_roles.append(role)

        # Run all reviews in parallel
        print(f"   ⏳ Analyzing with {len(tasks)} experts...")
        reviews = await asyncio.gather(*tasks, return_exceptions=True)

        # Package results
        results = {}
        for role, review in zip(expert_roles, reviews):
            if isinstance(review, Exception):
                print(f"   ⚠️  {role}: Failed - {review}")
                results[role] = None
            else:
                print(f"   ✅ {role}: Complete (confidence: {review.confidence_score}%)")
                results[role] = review

        return results

    def aggregate_findings(
        self,
        all_reviews: dict[str, dict[str, ExpertReview]]
    ) -> dict:
        """
        Aggregate findings from all experts across all sections

        Creates consensus by:
        1. Counting how many experts flag each issue
        2. Grouping issues by severity
        3. Identifying patterns across sections
        4. Prioritizing by expert consensus
        """

        print("\n" + "="*70)
        print("📊 AGGREGATING EXPERT CONSENSUS")
        print("="*70)

        # Issue tracking with consensus counting
        critical_issues = {}  # issue_text -> {count, experts[], sections[]}
        major_issues = {}
        minor_issues = {}
        quick_wins = {}

        # Track expert agreement
        expert_findings = {role: {
            'critical': 0,
            'major': 0,
            'minor': 0
        } for role in self.experts.keys()}

        # Process each section's reviews
        for section_name, section_reviews in all_reviews.items():
            print(f"\n📍 Processing: {section_name}")

            for expert_role, review in section_reviews.items():
                if review is None:
                    continue

                print(f"   👤 {expert_role}: {len(review.critical_issues)} critical, " +
                      f"{len(review.major_issues)} major, {len(review.minor_issues)} minor")

                # Track critical issues
                for issue in review.critical_issues:
                    key = self._normalize_issue(issue)
                    if key not in critical_issues:
                        critical_issues[key] = {
                            'text': issue,
                            'count': 0,
                            'experts': [],
                            'sections': set()
                        }
                    critical_issues[key]['count'] += 1
                    critical_issues[key]['experts'].append(expert_role)
                    critical_issues[key]['sections'].add(section_name)
                    expert_findings[expert_role]['critical'] += 1

                # Track major issues
                for issue in review.major_issues:
                    key = self._normalize_issue(issue)
                    if key not in major_issues:
                        major_issues[key] = {
                            'text': issue,
                            'count': 0,
                            'experts': [],
                            'sections': set()
                        }
                    major_issues[key]['count'] += 1
                    major_issues[key]['experts'].append(expert_role)
                    major_issues[key]['sections'].add(section_name)
                    expert_findings[expert_role]['major'] += 1

                # Track minor issues
                for issue in review.minor_issues:
                    key = self._normalize_issue(issue)
                    if key not in minor_issues:
                        minor_issues[key] = {
                            'text': issue,
                            'count': 0,
                            'experts': [],
                            'sections': set()
                        }
                    minor_issues[key]['count'] += 1
                    minor_issues[key]['experts'].append(expert_role)
                    minor_issues[key]['sections'].add(section_name)
                    expert_findings[expert_role]['minor'] += 1

                # Track quick wins
                for win in review.quick_wins:
                    key = self._normalize_issue(win)
                    if key not in quick_wins:
                        quick_wins[key] = {
                            'text': win,
                            'count': 0,
                            'experts': [],
                            'sections': set()
                        }
                    quick_wins[key]['count'] += 1
                    quick_wins[key]['experts'].append(expert_role)
                    quick_wins[key]['sections'].add(section_name)

        # Sort by consensus (most experts agreeing)
        critical_sorted = sorted(
            critical_issues.values(),
            key=lambda x: (-x['count'], len(x['sections']))
        )
        major_sorted = sorted(
            major_issues.values(),
            key=lambda x: (-x['count'], len(x['sections']))
        )
        minor_sorted = sorted(
            minor_issues.values(),
            key=lambda x: (-x['count'], len(x['sections']))
        )
        quick_wins_sorted = sorted(
            quick_wins.values(),
            key=lambda x: (-x['count'], len(x['sections']))
        )

        return {
            'critical_issues': critical_sorted,
            'major_issues': major_sorted,
            'minor_issues': minor_sorted,
            'quick_wins': quick_wins_sorted,
            'expert_findings': expert_findings,
            'total_experts': len(self.experts),
            'timestamp': datetime.now().isoformat()
        }

    def _normalize_issue(self, issue_text: str) -> str:
        """Normalize issue text for deduplication"""
        # Remove extra whitespace and lowercase for comparison
        return ' '.join(issue_text.lower().split())

    def format_consensus_report(self, aggregated: dict) -> str:
        """Format aggregated findings into readable report"""

        report = []
        report.append("\n" + "="*70)
        report.append("🎯 CONSENSUS EXPERT REVIEW REPORT")
        report.append("="*70)
        report.append(f"\nReview Date: {aggregated['timestamp']}")
        report.append(f"Experts Consulted: {aggregated['total_experts']}")
        report.append("\n" + "="*70)

        # Critical Issues
        report.append("\n🔴 CRITICAL ISSUES (Expert Consensus)")
        report.append("-" * 70)

        if not aggregated['critical_issues']:
            report.append("\n✅ No critical issues found!")
        else:
            for idx, issue in enumerate(aggregated['critical_issues'], 1):
                consensus_pct = (issue['count'] / aggregated['total_experts']) * 100
                experts_str = ", ".join(set(issue['experts']))
                sections_str = ", ".join(sorted(issue['sections']))

                report.append(f"\n{idx}. {issue['text']}")
                report.append(f"   📊 Consensus: {issue['count']}/{aggregated['total_experts']} " +
                            f"experts ({consensus_pct:.0f}%)")
                report.append(f"   👥 Flagged by: {experts_str}")
                report.append(f"   📍 Affects: {sections_str}")

        # Major Issues
        report.append("\n\n🟠 MAJOR ISSUES (Expert Consensus)")
        report.append("-" * 70)

        for idx, issue in enumerate(aggregated['major_issues'][:10], 1):  # Top 10
            consensus_pct = (issue['count'] / aggregated['total_experts']) * 100
            experts_str = ", ".join(set(issue['experts']))
            sections_str = ", ".join(sorted(issue['sections']))

            report.append(f"\n{idx}. {issue['text']}")
            report.append(f"   📊 Consensus: {issue['count']}/{aggregated['total_experts']} " +
                        f"experts ({consensus_pct:.0f}%)")
            report.append(f"   👥 Flagged by: {experts_str}")
            report.append(f"   📍 Affects: {sections_str}")

        # Quick Wins
        report.append("\n\n🚀 QUICK WINS (High Impact, Low Effort)")
        report.append("-" * 70)

        for idx, win in enumerate(aggregated['quick_wins'][:5], 1):  # Top 5
            consensus_pct = (win['count'] / aggregated['total_experts']) * 100
            experts_str = ", ".join(set(win['experts']))

            report.append(f"\n{idx}. {win['text']}")
            report.append(f"   📊 {win['count']}/{aggregated['total_experts']} experts agree ({consensus_pct:.0f}%)")
            report.append(f"   👥 Recommended by: {experts_str}")

        # Expert Summary
        report.append("\n\n👥 EXPERT BREAKDOWN")
        report.append("-" * 70)

        for expert_role, findings in aggregated['expert_findings'].items():
            total = findings['critical'] + findings['major'] + findings['minor']
            report.append(f"\n{expert_role}:")
            report.append(f"   🔴 {findings['critical']} critical  " +
                        f"🟠 {findings['major']} major  " +
                        f"🟡 {findings['minor']} minor  " +
                        f"(Total: {total})")

        report.append("\n" + "="*70)

        return "\n".join(report)

    def save_report(self, report: str, output_path: str):
        """Save report to file"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"\n💾 Report saved to: {output_path}")


async def run_consensus_review(
    screenshots: dict[str, str],
    output_file: str = "qa_agents/screenshots/CONSENSUS-REPORT.txt"
) -> str:
    """
    Run multi-expert consensus review

    Args:
        screenshots: Dict of {section_name: screenshot_path}
        output_file: Where to save the report

    Returns:
        Formatted consensus report
    """
    system = ConsensusReviewSystem()
    all_reviews = {}

    # Review each section with all experts
    for section_name, screenshot_path in screenshots.items():
        reviews = await system.run_parallel_reviews(
            screenshot_path,
            section_name
        )
        all_reviews[section_name] = reviews

    # Aggregate findings
    aggregated = system.aggregate_findings(all_reviews)

    # Format report
    report = system.format_consensus_report(aggregated)

    # Save report
    system.save_report(report, output_file)

    # Also save raw JSON for programmatic access
    json_path = output_file.replace('.txt', '.json')
    with open(json_path, 'w') as f:
        # Convert sets to lists for JSON serialization
        json_data = aggregated.copy()
        for issue_list_key in ['critical_issues', 'major_issues', 'minor_issues', 'quick_wins']:
            for issue in json_data[issue_list_key]:
                issue['sections'] = list(issue['sections'])
        json.dump(json_data, f, indent=2)
    print(f"💾 JSON data saved to: {json_path}")

    return report
