"""Example showing how to create fully custom slides."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from slide_deck_agent import SlideDeckAgent, SlideContent, SlideType, PresentationRequest


def main():
    """Create a presentation with fully custom slide definitions."""
    agent = SlideDeckAgent()

    # Define each slide individually with complete control
    slides = [
        # Title slide
        SlideContent(
            slide_type=SlideType.TITLE,
            title="The Future of Work",
            subtitle="Adapting to the New Normal",
            notes="Welcome everyone and introduce the topic with enthusiasm",
        ),
        # Agenda
        SlideContent(
            slide_type=SlideType.BULLET_POINTS,
            title="What We'll Cover Today",
            bullet_points=[
                "Remote work trends and statistics",
                "Tools and technologies enabling distributed teams",
                "Challenges and solutions",
                "Best practices for productivity",
                "The future outlook",
            ],
            notes="Set expectations for the presentation flow",
        ),
        # Section header
        SlideContent(
            slide_type=SlideType.SECTION_HEADER,
            title="Remote Work Revolution",
            notes="Transition to first major section",
        ),
        # Statistics slide
        SlideContent(
            slide_type=SlideType.TWO_COLUMN,
            title="Remote Work by the Numbers",
            left_content="Before 2020:\n\n"
            "• 5% of workforce remote\n"
            "• Limited tools available\n"
            "• Skepticism from leadership\n"
            "• Office-centric culture",
            right_content="After 2020:\n\n"
            "• 30%+ of workforce remote\n"
            "• Robust ecosystem of tools\n"
            "• Proven productivity gains\n"
            "• Hybrid-first mindset",
            notes="Emphasize the dramatic shift in just a few years",
        ),
        # Tools section
        SlideContent(
            slide_type=SlideType.SECTION_HEADER,
            title="Essential Tools & Technologies",
            notes="Transition to discussing tools that enable remote work",
        ),
        SlideContent(
            slide_type=SlideType.BULLET_POINTS,
            title="The Remote Work Tech Stack",
            bullet_points=[
                "Communication: Slack, Microsoft Teams, Zoom",
                "Project Management: Asana, Jira, Monday.com",
                "Documentation: Notion, Confluence, Google Workspace",
                "Design Collaboration: Figma, Miro, Mural",
                "Development: GitHub, GitLab, VS Code Live Share",
            ],
            notes="Each category is essential for different aspects of collaboration",
        ),
        # Quote slide
        SlideContent(
            slide_type=SlideType.QUOTE,
            quote_text="The future of work is not about location, it's about talent and results",
            quote_author="Sarah Williams, Remote Work Expert",
            notes="Use this quote to reinforce the paradigm shift",
        ),
        # Best practices
        SlideContent(
            slide_type=SlideType.BULLET_POINTS,
            title="Best Practices for Remote Success",
            bullet_points=[
                "Establish clear communication protocols",
                "Set boundaries between work and personal life",
                "Invest in proper home office setup",
                "Regular video check-ins with team",
                "Document everything for async collaboration",
                "Foster social connections virtually",
            ],
            notes="These are based on research and real-world experience",
        ),
        # Closing
        SlideContent(
            slide_type=SlideType.TITLE_CONTENT,
            title="Looking Ahead",
            content="The future of work is flexible, distributed, and empowering. "
            "Organizations that embrace this change will attract top talent, "
            "reduce costs, and build more resilient teams.\n\n"
            "The question is not whether to adapt, but how quickly.",
            notes="End on an inspiring and forward-looking note",
        ),
        # Thank you
        SlideContent(
            slide_type=SlideType.THANK_YOU,
            title="Thank You",
            subtitle="Let's discuss your thoughts and questions",
            notes="Open the floor for Q&A and discussion",
        ),
    ]

    # Create the full presentation request
    request = PresentationRequest(
        topic="The Future of Work",
        slides=slides,
        output_path="examples/output/future_of_work.pptx",
        template="modern",
        primary_color="#2C3E50",
        secondary_color="#3498DB",
        background_color="#FFFFFF",
        text_color="#2C3E50",
        author="Jane Doe",
        company="Future Works Consulting",
    )

    # Validate before generating
    errors = agent.validate_presentation_request(request)
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"  ✗ {error}")
        return

    print("Creating custom presentation...")

    result = agent.create_custom_presentation(request)

    if result.success:
        print(f"✓ Success! Created {result.slide_count} slides")
        print(f"✓ Saved to: {result.output_path}")
        print(f"✓ Author: {result.metadata.get('author')}")
    else:
        print(f"✗ Error: {result.error}")


if __name__ == "__main__":
    main()
