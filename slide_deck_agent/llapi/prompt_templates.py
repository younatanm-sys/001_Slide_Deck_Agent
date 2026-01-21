"""
Prompt Templates for LLM Content Generation
============================================

Pre-built prompts for different presentation types and content generation tasks.
These prompts encode best practices for consulting-quality presentations.
"""

from typing import Dict, Any


class PromptTemplates:
    """Collection of prompt templates for slide content generation."""

    # =========================================================================
    # SYSTEM PROMPTS
    # =========================================================================

    SYSTEM_PROMPT = """You are a senior management consultant with 20 years of experience creating
executive presentations for Fortune 500 companies. You specialize in creating clear,
insight-driven slide decks that communicate complex ideas simply.

Your presentations follow these principles:
1. TITLES ARE INSIGHTS: Every slide title is a complete sentence stating the "so what" - the key takeaway
2. BULLETS SUPPORT THE TITLE: Bullet points provide evidence and detail, not new ideas
3. NO FLUFF: Every word earns its place. Remove filler phrases and redundancy.
4. PARALLEL STRUCTURE: Bullets use consistent grammatical structure
5. QUANTIFY WHEN POSSIBLE: Use specific numbers, percentages, timeframes when available
6. ACTION-ORIENTED: Use active voice and strong verbs

You ONLY use information provided in the source material. You NEVER invent statistics,
numbers, or facts. If the source doesn't contain quantitative data, you create qualitative
slides without fabricated metrics."""

    # =========================================================================
    # PRESENTATION STRUCTURE TEMPLATES
    # =========================================================================

    STRUCTURE_TEMPLATES = {
        "investor_pitch": {
            "name": "Investor Pitch (Sequoia/YC Format)",
            "max_slides": 15,
            "structure": [
                {"type": "problem", "purpose": "Pain point the market faces"},
                {"type": "solution", "purpose": "How you solve it"},
                {"type": "market", "purpose": "Size and growth of opportunity"},
                {"type": "value_proposition", "purpose": "Why customers choose you"},
                {"type": "product", "purpose": "What you've built"},
                {"type": "traction", "purpose": "Evidence of product-market fit"},
                {"type": "business_model", "purpose": "How you make money"},
                {"type": "go_to_market", "purpose": "How you acquire customers"},
                {"type": "competition", "purpose": "Competitive landscape and moat"},
                {"type": "team", "purpose": "Why this team wins"},
                {"type": "financials", "purpose": "Projections and metrics"},
                {"type": "ask", "purpose": "What you're raising and use of funds"},
                {"type": "vision", "purpose": "Where this goes long-term"},
            ]
        },
        "strategy_update": {
            "name": "Strategy Update (McKinsey Format)",
            "max_slides": 20,
            "structure": [
                {"type": "executive_summary", "purpose": "Key findings in 3-5 bullets"},
                {"type": "situation", "purpose": "Current state assessment"},
                {"type": "challenges", "purpose": "Key issues to address"},
                {"type": "options", "purpose": "Strategic alternatives considered"},
                {"type": "recommendation", "purpose": "Proposed path forward"},
                {"type": "implementation", "purpose": "How to execute"},
                {"type": "timeline", "purpose": "Phased roadmap"},
                {"type": "risks", "purpose": "Key risks and mitigations"},
                {"type": "next_steps", "purpose": "Immediate actions required"},
            ]
        },
        "product_overview": {
            "name": "Product Overview",
            "max_slides": 12,
            "structure": [
                {"type": "problem", "purpose": "Customer pain point"},
                {"type": "solution", "purpose": "Product overview"},
                {"type": "features", "purpose": "Key capabilities"},
                {"type": "benefits", "purpose": "Value delivered"},
                {"type": "use_cases", "purpose": "How customers use it"},
                {"type": "differentiation", "purpose": "Why choose us"},
                {"type": "pricing", "purpose": "How it's priced"},
                {"type": "next_steps", "purpose": "Call to action"},
            ]
        },
        "quarterly_review": {
            "name": "Quarterly Business Review",
            "max_slides": 15,
            "structure": [
                {"type": "executive_summary", "purpose": "Quarter highlights"},
                {"type": "kpi_performance", "purpose": "Key metrics vs. targets"},
                {"type": "wins", "purpose": "Major achievements"},
                {"type": "challenges", "purpose": "Issues encountered"},
                {"type": "learnings", "purpose": "What we learned"},
                {"type": "next_quarter", "purpose": "Priorities ahead"},
                {"type": "asks", "purpose": "Support needed"},
            ]
        }
    }

    # =========================================================================
    # CONTENT GENERATION PROMPTS
    # =========================================================================

    @staticmethod
    def get_structure_analysis_prompt(document_content: str, presentation_type: str, max_slides: int) -> str:
        """Generate prompt for analyzing document and recommending slide structure."""

        template = PromptTemplates.STRUCTURE_TEMPLATES.get(
            presentation_type,
            PromptTemplates.STRUCTURE_TEMPLATES["investor_pitch"]
        )

        return f"""Analyze the following source document and recommend a slide structure.

SOURCE DOCUMENT:
{document_content}

PRESENTATION TYPE: {template['name']}
MAXIMUM SLIDES: {max_slides}

REFERENCE STRUCTURE:
{chr(10).join([f"- {s['type']}: {s['purpose']}" for s in template['structure']])}

TASK:
1. Read the source document carefully
2. Identify which sections from the reference structure apply to this content
3. Recommend a slide-by-slide structure
4. For each slide, note what content from the source supports it

OUTPUT FORMAT (JSON):
{{
    "recommended_slides": [
        {{
            "slide_number": 1,
            "type": "problem",
            "working_title": "Brief title idea",
            "source_content": "Relevant quotes/facts from source"
        }},
        ...
    ],
    "omitted_sections": ["section_type1", "section_type2"],
    "reasoning": "Brief explanation of structure choices"
}}

Only include slides that have supporting content in the source document.
Do NOT include slides for topics not covered in the source."""

    @staticmethod
    def get_slide_generation_prompt(
        slide_type: str,
        source_content: str,
        slide_number: int,
        total_slides: int,
        previous_slide_title: str = None
    ) -> str:
        """Generate prompt for creating a single slide's content."""

        context = ""
        if previous_slide_title:
            context = f"\nPREVIOUS SLIDE TITLE: {previous_slide_title}\nEnsure this slide flows logically from the previous one."

        return f"""Create content for slide {slide_number} of {total_slides}.

SLIDE TYPE: {slide_type}
{context}

SOURCE CONTENT TO USE:
{source_content}

REQUIREMENTS:
1. TITLE: Write an insight-driven title (complete sentence, states the "so what")
   - Bad: "Market Overview"
   - Good: "The $4.7T digital banking market is growing 13% annually"

2. BULLET POINTS: Write 3-4 bullets that support the title
   - Each bullet should be a complete thought
   - Use parallel grammatical structure
   - Be specific, not generic
   - Only use information from the source content

3. NO FABRICATION: If specific numbers aren't in the source, don't invent them

OUTPUT FORMAT (JSON):
{{
    "title": "Insight-driven slide title as complete sentence",
    "bullet_points": [
        "First supporting point",
        "Second supporting point",
        "Third supporting point",
        "Fourth supporting point (optional)"
    ],
    "notes": "Any presenter notes or caveats"
}}"""

    @staticmethod
    def get_title_refinement_prompt(draft_title: str, slide_type: str) -> str:
        """Generate prompt for refining a slide title to be more insight-driven."""

        return f"""Refine this slide title to be more insight-driven.

CURRENT TITLE: {draft_title}
SLIDE TYPE: {slide_type}

RULES FOR GOOD TITLES:
1. Complete sentence (subject + verb + object)
2. States the "so what" - the key takeaway
3. Specific, not generic
4. Uses active voice
5. Under 15 words if possible

BAD EXAMPLES:
- "Market Overview" (no insight)
- "Our Solution" (vague)
- "Financial Projections" (descriptive, not insightful)

GOOD EXAMPLES:
- "Digital banking market growing 13% annually creates $4.7T opportunity"
- "Our AI-first platform reduces customer acquisition cost by 75%"
- "Path to profitability in Year 3 with 180% revenue CAGR"

OUTPUT FORMAT (JSON):
{{
    "refined_title": "Your improved title here",
    "reasoning": "Brief explanation of improvement"
}}"""

    @staticmethod
    def get_bullet_refinement_prompt(bullets: list, title: str) -> str:
        """Generate prompt for refining bullet points."""

        bullets_text = "\n".join([f"- {b}" for b in bullets])

        return f"""Refine these bullet points to better support the slide title.

SLIDE TITLE: {title}

CURRENT BULLETS:
{bullets_text}

RULES FOR GOOD BULLETS:
1. Support the title's claim with evidence or detail
2. Use parallel grammatical structure
3. Be specific, not generic
4. Start with strong verbs or key nouns
5. Each bullet is one complete thought
6. 10-20 words per bullet (concise but complete)

OUTPUT FORMAT (JSON):
{{
    "refined_bullets": [
        "Improved bullet 1",
        "Improved bullet 2",
        "Improved bullet 3",
        "Improved bullet 4 (if needed)"
    ],
    "changes_made": "Brief summary of improvements"
}}"""

    @staticmethod
    def get_full_presentation_prompt(
        document_content: str,
        presentation_type: str,
        max_slides: int,
        audience: str = "investors",
        duration_minutes: int = 15
    ) -> str:
        """Generate prompt for creating an entire presentation at once."""

        template = PromptTemplates.STRUCTURE_TEMPLATES.get(
            presentation_type,
            PromptTemplates.STRUCTURE_TEMPLATES["investor_pitch"]
        )

        return f"""Create a {max_slides}-slide presentation from the following source document.

SOURCE DOCUMENT:
{document_content}

PRESENTATION PARAMETERS:
- Type: {template['name']}
- Audience: {audience}
- Duration: {duration_minutes} minutes (~1 minute per slide)
- Maximum slides: {max_slides}

REFERENCE STRUCTURE:
{chr(10).join([f"- {s['type']}: {s['purpose']}" for s in template['structure']])}

CRITICAL RULES:
1. ONLY use information from the source document - NO fabricated statistics or numbers
2. If the source has no numbers, create qualitative slides without metrics
3. Every title must be an insight (complete sentence stating the "so what")
4. 3-4 bullet points per slide that support the title
5. Use parallel structure within each slide's bullets
6. Flow logically from slide to slide

CHART DATA RULES:
When the source document contains QUANTITATIVE DATA (numbers, percentages, trends over time, comparisons),
you MUST include a chart_data object for that slide. Extract the exact numbers from the source.

Available chart types:
- "column": For comparing categories or showing trends over time (most common)
- "waterfall": For showing how components add up to a total (e.g., cost breakdowns, investment allocation)

Chart data structure:
- "type": Chart type ("column" or "waterfall")
- "title": Descriptive chart title (e.g., "Revenue by Channel (€M)")
- "categories": X-axis labels as array
- "series": Array of data series, each with "name" and "values" array (for column charts)
- "values": Single array of values (for waterfall charts)
- "types": Array of "start", "increase", "decrease", "end" (for waterfall charts only)
- "highlight_index": Which series to highlight (0-indexed, for column charts with 2+ series)
- "color_mode": Set to "comparison" when comparing multiple series without a highlight
- "source": Data source attribution (e.g., "Source: Company financials")

Chart annotation types (add to "annotations" array when helpful):
- cagr_arrow: Shows growth rate between two points
  {{"type": "cagr_arrow", "series_index": 0, "from_category": 0, "to_category": 4, "label": "45% CAGR"}}
- difference_line: Shows difference between two bars
  {{"type": "difference_line", "series_index": 0, "from_category": 0, "to_category": 1, "label": "€28 savings"}}
- leader_line: Points to a specific data point with label
  {{"type": "leader_line", "x": 0.8, "y": 0.9, "text": "Key insight", "direction": "right"}}

OUTPUT FORMAT (JSON):
{{
    "presentation_title": "Main title for the deck",
    "subtitle": "Subtitle or company name",
    "slides": [
        {{
            "slide_number": 1,
            "slide_type": "problem",
            "title": "Insight-driven title as complete sentence",
            "bullet_points": [
                "Supporting point 1",
                "Supporting point 2",
                "Supporting point 3"
            ],
            "chart_data": {{
                "type": "column",
                "title": "Chart Title (Units)",
                "categories": ["Cat1", "Cat2", "Cat3"],
                "series": [
                    {{"name": "Series 1", "values": [10, 20, 30]}},
                    {{"name": "Series 2", "values": [15, 25, 35]}}
                ],
                "highlight_index": 1,
                "source": "Source: Data source",
                "annotations": [
                    {{"type": "cagr_arrow", "series_index": 1, "from_category": 0, "to_category": 2, "label": "50% CAGR"}}
                ]
            }}
        }},
        {{
            "slide_number": 2,
            "slide_type": "situation",
            "title": "Another insight-driven title",
            "bullet_points": ["Point 1", "Point 2", "Point 3"]
        }}
    ]
}}

IMPORTANT:
- Include chart_data ONLY when the source document has specific numbers to visualize
- Extract EXACT numbers from the source - do not estimate or fabricate
- Not every slide needs a chart - only include when data visualization adds value
- For qualitative content, omit the chart_data field entirely

Generate exactly {max_slides} content slides (title and closing slides will be added automatically)."""
