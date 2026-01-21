"""Demo showing all available color schemes."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from slide_deck_agent import SlideDeckAgent, SlideContent, SlideType, PresentationRequest


def main():
    """Create sample slides demonstrating each color scheme."""
    agent = SlideDeckAgent()

    # Get all available color schemes
    schemes = agent.get_available_color_schemes()

    print(f"Available color schemes ({len(schemes)}):")
    for scheme in schemes:
        colors = agent.get_color_scheme_preview(scheme)
        print(f"\n{scheme}:")
        for key, value in colors.items():
            print(f"  {key}: {value}")

    # Create a presentation showcasing all color schemes
    slides = [
        SlideContent(
            slide_type=SlideType.TITLE,
            title="Color Schemes Gallery",
            subtitle="Professional templates for every occasion",
        )
    ]

    for scheme in schemes:
        colors = agent.get_color_scheme_preview(scheme)

        slides.append(
            SlideContent(slide_type=SlideType.SECTION_HEADER, title=scheme.replace("_", " ").title())
        )

        slides.append(
            SlideContent(
                slide_type=SlideType.BULLET_POINTS,
                title=f"{scheme} Color Palette",
                bullet_points=[
                    f"Primary: {colors['primary']}",
                    f"Secondary: {colors['secondary']}",
                    f"Background: {colors['background']}",
                    f"Text: {colors['text']}",
                    f"Accent: {colors['accent']}",
                ],
            )
        )

    slides.append(
        SlideContent(
            slide_type=SlideType.THANK_YOU, title="Choose Your Style", subtitle="All schemes ready to use"
        )
    )

    # Create presentation for each scheme
    for scheme in schemes:
        request = PresentationRequest(
            topic=f"Color Scheme Demo: {scheme}",
            slides=[
                SlideContent(
                    slide_type=SlideType.TITLE,
                    title=scheme.replace("_", " ").title(),
                    subtitle="Color Scheme Demonstration",
                ),
                SlideContent(
                    slide_type=SlideType.BULLET_POINTS,
                    title="Sample Content",
                    bullet_points=[
                        "This is how bullet points look",
                        "Notice the color harmony",
                        "Professional and readable",
                    ],
                ),
                SlideContent(
                    slide_type=SlideType.THANK_YOU,
                    title="Beautiful Design",
                    subtitle="Ready for your content",
                ),
            ],
            output_path=f"examples/output/schemes/{scheme}_demo.pptx",
        )

        request = agent.design_optimizer.apply_color_scheme(request, scheme)
        result = agent.create_custom_presentation(request)

        if result.success:
            print(f"✓ Created: {scheme}_demo.pptx")


if __name__ == "__main__":
    main()
