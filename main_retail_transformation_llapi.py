"""
Main Template - Retail Digital Transformation - LLAPI Demo
===========================================================

This demo shows how the LLAPI layer generates slide content from a source
document, then passes it to the Main template engine for rendering.

Architecture:
    Source Document -> LLAPI (LLM) -> SlideContent objects -> MainSlideGeneratorSkill -> PowerPoint

Usage:
    # With API key (real LLM generation):
    ANTHROPIC_API_KEY=your-key python main_retail_transformation_llapi.py

    # Mock mode (no API needed, for testing):
    python main_retail_transformation_llapi.py --mock
"""

import sys
import argparse
sys.path.insert(0, '.')

from slide_deck_agent.llapi import ContentGenerator
from slide_deck_agent.skills.main_slide_generator import MainSlideGeneratorSkill

# ============================================================================
# SOURCE DOCUMENT - Retail Digital Transformation Strategy
# ============================================================================

SOURCE_DOCUMENT = """
Retail Digital Transformation Strategy

Executive Summary

A major European retail company is undergoing digital transformation to shift from
brick-and-mortar to omnichannel excellence. The e-commerce channel is growing at
45% CAGR while store sales decline 8% annually. By 2027, e-commerce will represent
70% of total revenue.

Current Situation

The retail landscape is fundamentally changing:
- Store sales declining 8% annually as customers shift to digital channels
- E-commerce revenue growing 45% CAGR, projected to reach €2.8B by 2027
- Mobile commerce represents 65% of digital sales, up from 42% in 2023
- Omnichannel customers spend 3.2x more than single-channel shoppers

Customer Behavior Shift

Mobile-first shopping behavior is now dominant across all demographics:
- Gen Z and Millennials drive 68% of mobile commerce volume
- Average order value on mobile increased 23% YoY to €87
- Mobile app users show 2.8x higher retention than mobile web users
- Push notifications drive 42% conversion uplift vs. email campaigns

Regional Performance

Digital adoption varies significantly by region:
- Western Europe leads with 58% digital penetration and €1.2B annual revenue
- North America at 56% digital penetration, driven by mobile app adoption
- Eastern Europe at 42% penetration but fastest growth at 62% CAGR
- Asia-Pacific at 38% penetration with significant untapped potential

Customer Acquisition Economics

The digital-first strategy is dramatically reducing customer acquisition costs:
- Traditional marketing CAC: €45 (print, TV, direct mail)
- Digital marketing CAC: €17 (social, search, influencer partnerships)
- Organic social driving 40% of new acquisitions at €3 CAC
- Referral program contributing 25% of acquisitions at €8 CAC
- Target blended CAC: €12 (62% reduction from traditional)

Technology Investment Required

Achieving omnichannel excellence requires €180M technology investment:
- Platform modernization: €65M for cloud-native e-commerce platform
- Mobile apps: €35M for iOS/Android native apps with AR try-on features
- Data & analytics: €40M for CDP, ML personalization, real-time inventory
- Store digitization: €40M for smart fitting rooms, endless aisle, mobile POS

Customer Lifetime Value

Omnichannel customers deliver significantly higher lifetime value:
- Single-channel (store only): €400 LTV with 18-month retention
- Single-channel (online only): €520 LTV with 24-month retention
- Omnichannel (store + online): €1,280 LTV with 42-month retention
- Omnichannel customers shop 2.4x more frequently across all touchpoints

Implementation Roadmap

18-month phased rollout minimizes risk while delivering continuous value:
- Phase 1 (Months 1-6): Platform foundation, mobile app MVP, basic personalization
- Phase 2 (Months 7-12): Omnichannel integration, advanced ML, store digitization pilot
- Phase 3 (Months 13-18): Full store rollout, AR features, real-time inventory optimization

Financial Impact

The transformation delivers compelling financial returns:
- Year 1: €80M incremental revenue at 18% EBITDA margin
- Year 2: €240M incremental revenue at 24% EBITDA margin
- Year 3: €420M incremental revenue at 28% EBITDA margin (steady state)
- Payback period: 16 months
- 3-year NPV: €680M at 10% discount rate

Competitive Positioning

Post-transformation competitive position:
- Current NPS: 42 (industry average: 38)
- Target NPS post-transformation: 68 (best-in-class benchmark)
- Mobile app rated 4.7/5.0 stars (top 5% in retail category)
- Omnichannel capabilities exceed 85% of direct competitors

Recommendation

Proceed with the €180M digital transformation investment. The 16-month payback
period and €680M NPV make this a highly attractive investment. The transformation
will position the company as a category leader with best-in-class customer experience
and operational efficiency.
"""


def main():
    """Run the Main Template LLAPI demo."""
    # Parse arguments
    parser = argparse.ArgumentParser(description="Main Template LLAPI Demo - Retail Transformation")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock mode (no API key required)"
    )
    parser.add_argument(
        "--provider",
        choices=["anthropic", "openai", "mock"],
        default="anthropic",
        help="LLM provider to use"
    )
    parser.add_argument(
        "--max-slides",
        type=int,
        default=10,
        help="Maximum number of slides"
    )
    parser.add_argument(
        "--output",
        default="main_retail_transformation_llapi.pptx",
        help="Output file path"
    )
    args = parser.parse_args()

    # Determine provider
    provider = "mock" if args.mock else args.provider

    print("=" * 80)
    print("MAIN TEMPLATE LLAPI DEMO - RETAIL DIGITAL TRANSFORMATION")
    print("=" * 80)
    print()
    print(f"Provider: {provider.upper()}")
    print(f"Max slides: {args.max_slides}")
    print(f"Output: {args.output}")
    print()

    # =========================================================================
    # STEP 1: Initialize LLAPI Content Generator
    # =========================================================================
    print("STEP 1: Initializing LLAPI Content Generator...")

    try:
        generator = ContentGenerator(provider=provider)
        print(f"  ✓ ContentGenerator initialized with {provider} provider")
    except Exception as e:
        print(f"  ✗ Failed to initialize: {e}")
        return

    # =========================================================================
    # STEP 2: Generate Slides from Source Document
    # =========================================================================
    print()
    print("STEP 2: Generating slides from source document...")
    print(f"  Source document: {len(SOURCE_DOCUMENT)} characters")

    try:
        # This is where the LLM magic happens
        presentation_request = generator.generate_from_document(
            source=SOURCE_DOCUMENT,
            presentation_type="strategy_update",  # Strategy presentation
            max_slides=args.max_slides,
            audience="executives",
            duration_minutes=20,
            title="Retail Digital Transformation",
            company="Strategy Team"
        )

        # Update output path
        presentation_request.output_path = args.output
        presentation_request.author = "Digital Strategy Team"

        print(f"  ✓ Generated {len(presentation_request.slides)} slides")
        print()

        # Display generated slides
        print("  Generated Slide Structure:")
        print("  " + "-" * 60)
        charts_count = 0
        for i, slide in enumerate(presentation_request.slides, 1):
            title_preview = slide.title[:55] + "..." if len(slide.title) > 55 else slide.title
            has_chart = hasattr(slide, 'chart_data') and slide.chart_data is not None
            chart_indicator = " [CHART]" if has_chart else ""
            if has_chart:
                charts_count += 1
            print(f"  {i:2}. {title_preview}{chart_indicator}")
            for bullet in slide.bullet_points[:2]:
                bullet_preview = bullet[:45] + "..." if len(bullet) > 45 else bullet
                print(f"      • {bullet_preview}")
            if len(slide.bullet_points) > 2:
                print(f"      ... and {len(slide.bullet_points) - 2} more bullets")
            if has_chart:
                chart_type = slide.chart_data.get('type', 'unknown')
                chart_title = slide.chart_data.get('title', 'Untitled')[:40]
                print(f"      📊 {chart_type}: {chart_title}")
        print("  " + "-" * 60)
        print(f"  Total slides with charts: {charts_count}/{len(presentation_request.slides)}")

    except Exception as e:
        print(f"  ✗ Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # =========================================================================
    # STEP 3: Render with Main Template Engine
    # =========================================================================
    print()
    print("STEP 3: Rendering with MainSlideGeneratorSkill (Main Template Engine)...")

    try:
        # Initialize Main template engine
        main_generator = MainSlideGeneratorSkill()

        # Generate the PowerPoint
        result = main_generator.create_presentation(presentation_request)

        if result.success:
            print(f"  ✓ Presentation created successfully!")
            print()
            print("  Presentation Details:")
            print(f"    File:     {result.output_path}")
            print(f"    Slides:   {result.slide_count}")
            print(f"    Template: {result.metadata.get('template', 'Main v2.0')}")
        else:
            print(f"  ✗ Rendering failed: {result.error}")

    except Exception as e:
        print(f"  ✗ Rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # =========================================================================
    # Summary
    # =========================================================================
    print()
    print("=" * 80)
    print("MAIN TEMPLATE LLAPI DEMO COMPLETE")
    print("=" * 80)
    print()
    print("Architecture Used:")
    print("  Source Document -> LLAPI (ContentGenerator) -> SlideContent objects")
    print("                  -> MainSlideGeneratorSkill (Main Template Engine)")
    print("                  -> PowerPoint File")
    print()
    print("Design Principles Applied:")
    print("  • PRINCIPLE 1: Zoned Integrity (Title/Content/Footer)")
    print("  • PRINCIPLE 2: Content-Driven Layouts (50/50 split)")
    print("  • PRINCIPLE 3: Atomic Text Elements (separate bullets)")
    print("  • PRINCIPLE 4: Hierarchical Titling (T1-T5)")
    print("  • PRINCIPLE 5: Consistent Visual Anchoring")
    print()
    print("Global Skills Applied by Template Engine:")
    print("  • Story-Driven Color Engine (Green Palette)")
    print("  • Legend-to-Data Integrity")
    print("  • Visual Annotation System")
    print("  • Dynamic Text Resizing")
    print("  • Professional Bullet Formatting")
    print()
    print(f"Open '{args.output}' to view the AI-generated presentation!")
    print("=" * 80)


if __name__ == "__main__":
    main()
