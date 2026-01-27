"""
Claude Code Skills Presentation Generator
==========================================

Generates a presentation about Claude Code Skills using the LLAPI layer.
"""

import sys
sys.path.insert(0, '.')

from slide_deck_agent.models import SlideContent, SlideType, PresentationRequest
from slide_deck_agent.skills.main_slide_generator import MainSlideGeneratorSkill


def create_claude_code_skills_presentation():
    """Create the Claude Code Skills presentation with pre-defined content."""

    slides = []

    # Slide 1: Title Slide
    slides.append(SlideContent(
        slide_type=SlideType.TITLE,
        title="Claude Code Skills: AI-Driven Transformation of Presentation Generation",
        subtitle=""
    ))

    # Slide 2: The Problem - The Hidden Cost of Presentations
    slides.append(SlideContent(
        slide_type=SlideType.STANDARD_CONTENT,
        title="The Problem - The Hidden Cost of Presentations",
        bullet_points=[
            "Consultants spend 2-4 hours daily on presentation formatting",
            "10-person team: 7,500+ hours/year = 3-4 full-time employees",
            "Opportunity cost: $900,000-$1,200,000 annually",
            "Highly paid consultants formatting slides instead of solving client problems."
        ],
        source="Industry research on consulting productivity"
    ))

    # Slide 3: The "Last-Mile Problem" - Why Existing AI Tools Fail
    slides.append(SlideContent(
        slide_type=SlideType.STANDARD_CONTENT,
        title="The 'Last-Mile Problem' - Why Existing AI Tools Fail",
        bullet_points=[
            "The Challenge: Template-based tools (Gamma, Beautiful.ai) produce generic outputs requiring extensive manual rework. 80-90% of time savings lost to brand alignment corrections.",
            "Cannot enforce brand-specific rules",
            "Cannot translate brand guidelines into design decisions",
            "Output quality is unpredictable",
            "Users manually fix every slide",
            "Result: Teams spend almost as much time fixing AI slides as creating them manually."
        ],
        source="Analysis of AI presentation tool effectiveness"
    ))

    # Slide 4: The Solution - Claude Code Skills Architecture
    slides.append(SlideContent(
        slide_type=SlideType.STANDARD_CONTENT,
        title="The Solution - Claude Code Skills Architecture",
        bullet_points=[
            "Rule-Based Design System (871 lines of unbreakable design rules)",
            "Content Generation: Claude API generates insight-driven content",
            "Design Rule Engine: Enforces professional standards and brand consistency",
            "PowerPoint Rendering: Generates native, fully-editable files",
            "Result: Complete, professional decks ready to present immediately."
        ],
        chart_data={
            "type": "column",
            "title": "Three-Layer Architecture",
            "categories": ["Content\nGeneration", "Design\nRule Engine", "PowerPoint\nRendering"],
            "series": [
                {"name": "Lines of Code", "values": [800, 871, 450]}
            ]
        },
        source="Claude Code Skills Architecture v2.1"
    ))

    # Slide 5: Core Innovation #1 - Intelligent Annotation System
    # Demonstrate the annotation system with a sample chart showing CAGR arrow and difference line
    slides.append(SlideContent(
        slide_type=SlideType.STANDARD_CONTENT,
        title="Core Innovation #1 - Intelligent Annotation System",
        bullet_points=[
            "Automatically generates annotations that tell the data story:",
            "CAGR Arrows (growth trends)",
            "Difference Lines (changes between points)",
            "Leader Lines (key data points)",
            "Callouts (important insights)",
            "Why It Matters: Consultants spend hours manually adding annotations. Claude Code Skills automates this completely. Template-based tools have zero annotation capability."
        ],
        chart_data={
            "type": "column",
            "title": "E-Commerce Revenue Growth ($M)",
            "categories": ["2021", "2022", "2023", "2024", "2025"],
            "series": [
                {"name": "Revenue", "values": [120, 156, 203, 264, 343]}
            ],
            "annotations": [
                {
                    "type": "cagr_arrow",
                    "series_index": 0,
                    "from_category": 0,
                    "to_category": 4,
                    "cagr_value": 0.30,
                    "label_generation_request": {
                        "task": "generate_cagr_label",
                        "data_series": [120, 156, 203, 264, 343],
                        "cagr_value": 0.30
                    }
                },
                {
                    "type": "difference_line",
                    "series_index": 0,
                    "from_category": 0,
                    "to_category": 4,
                    "label": "+$223M growth\n(186% increase)"
                }
            ]
        },
        source="Sample: Auto-generated annotations"
    ))

    # Slide 6: Core Innovation #2 - Story-Driven Color Engine
    # Demonstrate with a waterfall chart showing color-coded increases/decreases
    slides.append(SlideContent(
        slide_type=SlideType.STANDARD_CONTENT,
        title="Core Innovation #2 - Story-Driven Color Engine",
        bullet_points=[
            "Default state: grey (neutral)",
            "Story is in color (highlight important data)",
            "Comparisons: sequential colors",
            "Never random colors",
            "Example: Waterfall chart shows increases in green, decreases in red. Viewer immediately understands the narrative without reading a legend."
        ],
        chart_data={
            "type": "waterfall",
            "title": "Profit Bridge Analysis ($M)",
            "categories": ["Starting\nProfit", "New\nCustomers", "Price\nIncrease", "Cost\nReduction", "Marketing\nSpend", "Ending\nProfit"],
            "values": [100, 45, 28, 18, -32, 159],
            "types": ["start", "increase", "increase", "increase", "decrease", "end"]
        },
        source="Sample: Story-driven color automatically applied"
    ))

    # Slide 7: Core Innovation #3 - LLM-Powered Label Engine
    # Demonstrate with a waterfall chart showing LLM-generated labels for each contribution
    slides.append(SlideContent(
        slide_type=SlideType.STANDARD_CONTENT,
        title="Core Innovation #3 - LLM-Powered Label Engine",
        bullet_points=[
            "Automatically generates polished annotation labels from raw data:",
            "Instead of manually writing '€28 savings (62% reduction)'",
            "System generates this automatically from structured data",
            "Ensures consistency and saves time",
            "Resilience: Falls back to local calculation if API fails. Production-ready engineering."
        ],
        chart_data={
            "type": "waterfall",
            "title": "Marketing Budget Optimization ($K)",
            "categories": ["Initial\nBudget", "Automation\nSavings", "Channel\nShift", "Agency\nReduction", "Tool\nInvestment", "Final\nBudget"],
            "values": [500, 120, 85, 65, -45, 275],
            "types": ["start", "increase", "increase", "increase", "decrease", "end"],
            "annotations": [
                {
                    "type": "difference_line",
                    "series_index": 0,
                    "from_category": 0,
                    "to_category": 5,
                    "label_generation_request": {
                        "task": "generate_difference_label",
                        "start_value": 500,
                        "end_value": 275,
                        "currency": "$",
                        "direction": "reduction"
                    }
                }
            ]
        },
        source="Sample: LLM-generated label from raw data"
    ))

    # Slide 8: Competitive Differentiation
    slides.append(SlideContent(
        slide_type=SlideType.STANDARD_CONTENT,
        title="Competitive Differentiation",
        bullet_points=[
            "Template-Based Tools (Gamma, Beautiful.ai): Manual layout, decorative colors, no governance. Consistency: Low, user-dependent. Output: Variable, unpredictable",
            "Rule-Based System (Claude Code Skills): Automatic layout, story-driven colors, strict rules. Consistency: High, system-guaranteed. Output: Predictable, professional-grade",
            "Fundamental Difference: Template tools delegate design to users. Rule-based systems enforce design through code."
        ],
        chart_data={
            "type": "column",
            "title": "Brand Compliance Rate (%)",
            "categories": ["Template-Based\nAI Tools", "Claude Code\nSkills"],
            "series": [
                {"name": "Compliance", "values": [72, 99]}
            ],
            "annotations": [
                {
                    "type": "difference_line",
                    "series_index": 0,
                    "from_category": 0,
                    "to_category": 1,
                    "label": "+27 pts\n(38% improvement)"
                }
            ]
        },
        source="Implementation case study analysis"
    ))

    # Slide 9: The Value Proposition - Financial Impact
    slides.append(SlideContent(
        slide_type=SlideType.STANDARD_CONTENT,
        title="The Value Proposition - Financial Impact",
        bullet_points=[
            "Current State (10-person team): 20 hours/week per consultant. Annual cost: $900,000-$1,200,000",
            "Post-Implementation (Projected): 4 hours/week per consultant (80-90% reduction). Annual cost: $180,000-$240,000. Savings: $720,000-$960,000/year",
            "Implementation Costs: $130,000-$200,000",
            "Payback Period: 1.5-3 months",
            "Three-Year ROI: $1,860,000-$2,640,000"
        ],
        chart_data={
            "type": "column",
            "title": "Annual Presentation Costs ($K)",
            "categories": ["Current State", "Post-Implementation"],
            "series": [
                {"name": "Annual Cost", "values": [1050, 210]}
            ],
            "annotations": [
                {
                    "type": "difference_line",
                    "series_index": 0,
                    "from_category": 0,
                    "to_category": 1,
                    "label": "$840K savings\n(80% reduction)"
                }
            ]
        },
        source="ROI analysis for 10-person consulting team"
    ))

    # Slide 10: Implementation Challenges - The Real Hurdles
    slides.append(SlideContent(
        slide_type=SlideType.STANDARD_CONTENT,
        title="Implementation Challenges - The Real Hurdles",
        bullet_points=[
            "Technical & Organizational: Translating brand guidelines to code (2-4 weeks), System integration (Jira, Salesforce, SharePoint), Executive sponsorship and governance",
            "Cultural & Operational: Resistance to change, Mindset shift: 'content provider' vs. 'slide designer', Training and onboarding at scale, Ongoing support and KPI measurement",
            "Key to Success: Executive sponsorship, phased rollout, training, change management."
        ],
        source="Implementation best practices"
    ))

    # Slide 11: Case Study - Global Strategy Partners
    slides.append(SlideContent(
        slide_type=SlideType.STANDARD_CONTENT,
        title="Case Study - Global Strategy Partners",
        bullet_points=[
            "Before: 18 hours/week on formatting, 72% brand compliance, 8 hours senior review per deck",
            "After (Year 1): 1.5 hours per 25-slide deck (92% reduction), 99% brand compliance, 1 hour senior review per deck, Client satisfaction: 7.2 → 9.1/10",
            "Financial Impact: Savings: $1,872,000, Implementation: $205,000, Net benefit: $1,667,000, Payback: 1.3 months",
            "Challenges: Initial resistance, Salesforce integration delays, training costs. Overcome with executive sponsorship and change management."
        ],
        chart_data={
            "type": "column",
            "title": "Time Per 25-Slide Deck (Hours)",
            "categories": ["Before", "After"],
            "series": [
                {"name": "Hours", "values": [18, 1.5]}
            ],
            "annotations": [
                {
                    "type": "difference_line",
                    "series_index": 0,
                    "from_category": 0,
                    "to_category": 1,
                    "label": "16.5 hrs saved\n(92% reduction)"
                }
            ]
        },
        source="Global Strategy Partners implementation case study"
    ))

    # Slide 12: Key Takeaways
    slides.append(SlideContent(
        slide_type=SlideType.STANDARD_CONTENT,
        title="Key Takeaways",
        bullet_points=[
            "The Problem is Real: 7,500+ hours/year per team = 3-4 FTE ($900K-$1.2M opportunity cost)",
            "Existing Tools Fall Short: Template-based AI loses 80-90% of time savings to manual corrections",
            "Rule-Based Systems Win: Design rules in code = predictable, professional output at scale",
            "Implementation Requires Planning: Executive sponsorship, phased rollout, training, change management",
            "ROI is Compelling: 1.5-3 month payback, $720K-$960K annual savings",
            "Real Value: Brand consistency, governance, professional standards at scale"
        ],
        source="Claude Code Skills Value Proposition"
    ))

    # Slide 13: Questions and Discussion
    slides.append(SlideContent(
        slide_type=SlideType.STANDARD_CONTENT,
        title="Questions and Discussion",
        bullet_points=[
            "Ready for your questions."
        ],
        source=""
    ))

    # Create presentation request
    request = PresentationRequest(
        topic="Claude Code Skills",
        slides=slides,
        output_path="claude_code_skills_presentation.pptx",
        author="Strategy Team",
        company="Claude Code Skills"
    )

    return request


def main():
    """Generate the Claude Code Skills presentation."""
    print("=" * 80)
    print("CLAUDE CODE SKILLS PRESENTATION GENERATOR")
    print("=" * 80)
    print()

    # Create the presentation content
    print("Creating presentation content...")
    request = create_claude_code_skills_presentation()
    print(f"  ✓ Created {len(request.slides)} slides")
    print()

    # Display slide structure
    print("Slide Structure:")
    print("-" * 60)
    for i, slide in enumerate(request.slides, 1):
        title_preview = slide.title[:55] + "..." if len(slide.title) > 55 else slide.title
        has_chart = slide.chart_data is not None
        chart_indicator = " [CHART]" if has_chart else ""
        print(f"  {i:2}. {title_preview}{chart_indicator}")
    print("-" * 60)
    print()

    # Render with Main Template Engine (using Anthropic API for label generation)
    print("Rendering with MainSlideGeneratorSkill (Anthropic API)...")

    try:
        generator = MainSlideGeneratorSkill(label_engine_provider="anthropic")
        result = generator.create_presentation(request)

        if result.success:
            print(f"  ✓ Presentation created successfully!")
            print()
            print("  Presentation Details:")
            print(f"    File:     {result.output_path}")
            print(f"    Slides:   {result.slide_count}")
            print(f"    Template: Main v2.1")
            print(f"    Label Engine: Anthropic API")
        else:
            print(f"  ✗ Rendering failed: {result.error}")

    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return

    print()
    print("=" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)
    print()
    print("Design Principles Applied:")
    print("  • PRINCIPLE 1: Zoned Integrity (Title/Content/Footer)")
    print("  • PRINCIPLE 2: Content-Driven Layouts (50/50 split)")
    print("  • PRINCIPLE 3: Atomic Text Elements (separate bullets)")
    print("  • PRINCIPLE 4: Hierarchical Titling (T1-T5)")
    print("  • PRINCIPLE 5: Consistent Visual Anchoring")
    print("  • PRINCIPLE 6: Insight Over Information (LLM Label Engine)")
    print()
    print(f"Open '{request.output_path}' to view the presentation!")
    print("=" * 80)


if __name__ == "__main__":
    main()
