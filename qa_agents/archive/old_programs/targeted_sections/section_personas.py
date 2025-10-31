"""
Section-specific review personas
Each section gets a focused review lens
"""

SECTION_PERSONAS = {
    "above-fold": {
        "name": "First Impression Specialist",
        "focus": [
            "Immediate visual hierarchy - can user understand what this "
            "page/site is about in 3 seconds?",
            "Value proposition clarity - is it obvious what the user "
            "gets here?",
            "Primary CTA visibility and appeal - does it stand out?",
            "Hero section effectiveness - compelling imagery or message?",
            "Navigation clarity - can user find what they need?",
            "Trust signals above fold - credibility indicators visible?",
            "Mobile thumb zone optimization (for mobile viewport)",
            "Load time perception - does layout prevent content shift?"
        ],
        "prompt_suffix": (
            "Focus on the FIRST IMPRESSION. This is what users see "
            "immediately without scrolling. Evaluate: Does this grab "
            "attention? Is the value proposition clear? Will users "
            "scroll or bounce?"
        )
    },
    "mid-page": {
        "name": "Content Flow Analyst",
        "focus": [
            "Information architecture - logical content progression?",
            "Scanability - can users skim effectively?",
            "Visual rhythm - good balance of text, images, whitespace?",
            "Section transitions - smooth flow between content blocks?",
            "Secondary CTAs placement and prominence",
            "Engagement elements - interactive components, social proof",
            "Content density - too cramped or too sparse?",
            "Progressive disclosure - complexity revealed gradually?"
        ],
        "prompt_suffix": (
            "Focus on CONTENT FLOW. This is the middle section where "
            "users are exploring. Evaluate: Is information well-organized? "
            "Can users scan easily? Does the layout maintain engagement?"
        )
    },
    "footer": {
        "name": "Utility & Trust Inspector",
        "focus": [
            "Navigation completeness - all key links accessible?",
            "Contact information visibility and accessibility",
            "Legal/compliance links (privacy, terms, etc.)",
            "Social proof elements (testimonials, partners, awards)",
            "Newsletter signup or conversion opportunity",
            "Brand reinforcement - consistent with page design?",
            "Mobile footer optimization - not too overwhelming?",
            "Trust signals - security badges, certifications, etc."
        ],
        "prompt_suffix": (
            "Focus on UTILITY & TRUST. This is the footer where users "
            "look for contact info, legal links, and final conversion "
            "opportunities. Evaluate: Is essential information easy to "
            "find? Does it build trust?"
        )
    }
}


def get_section_prompt(section_name: str, viewport_name: str) -> str:
    """
    Generate section-specific review prompt

    Args:
        section_name: One of 'above-fold', 'mid-page', 'footer'
        viewport_name: One of 'desktop', 'tablet', 'mobile'

    Returns:
        Formatted prompt string for GPT-4o Vision
    """
    persona = SECTION_PERSONAS.get(
        section_name,
        SECTION_PERSONAS["above-fold"]
    )

    viewport_context = {
        "desktop": "Desktop users expect rich information density "
                   "and wider layouts.",
        "tablet": "Tablet users are often in a browsing/research mode, "
                  "prefer scannable content.",
        "mobile": "Mobile users need touch-friendly targets "
                  "(48px+ hit areas) and concise content."
    }

    prompt = f"""You are a **{persona['name']}** reviewing the
**{section_name}** section on **{viewport_name}** viewport.

**Viewport Context**: {viewport_context.get(viewport_name, '')}

**Your Focus Areas**:
"""
    for item in persona['focus']:
        prompt += f"- {item}\n"

    prompt += f"\n**Review Instructions**:\n{persona['prompt_suffix']}\n\n"

    prompt += """
**Provide**:
1. **Strengths** (2-3 specific wins)
2. **Issues** (2-3 specific problems with severity: critical/major/minor)
3. **Quick Wins** (1-2 easy fixes with high impact)

Be specific, actionable, and cite visual evidence from the screenshot.
"""

    return prompt.strip()


def format_section_results(
    results: dict[str, dict],
    viewport_name: str
) -> str:
    """
    Format section review results for display

    Args:
        results: Dict mapping section name to review result
        viewport_name: Viewport being reviewed

    Returns:
        Formatted markdown string
    """
    output = f"\n## 📱 {viewport_name.upper()} - Section Analysis\n\n"

    section_order = ["above-fold", "mid-page", "footer"]

    for section in section_order:
        if section not in results:
            continue

        persona = SECTION_PERSONAS[section]
        result = results[section]

        output += f"### 🔍 {persona['name']} - {section.upper()}\n\n"

        # Add the review content
        if isinstance(result, dict):
            review_text = result.get("review", str(result))
        else:
            review_text = str(result)

        output += f"{review_text}\n\n"
        output += "---\n\n"

    return output
