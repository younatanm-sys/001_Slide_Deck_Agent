"""Advanced example with custom content structure."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from slide_deck_agent import SlideDeckAgent


def main():
    """Create a presentation with custom structured content."""
    agent = SlideDeckAgent()

    # Define custom content structure
    content = {
        "title": "Product Launch Strategy 2025",
        "subtitle": "Q1 Marketing Plan",
        "author": "Marketing Team",
        "company": "TechCorp",
        "color_scheme": "vibrant_creative",
        "sections": [
            {
                "header": "Market Analysis",
                "title": "Current Market Landscape",
                "content": "The market is experiencing rapid growth with increasing demand "
                "for innovative solutions. Our competitive analysis shows "
                "significant opportunities in the enterprise segment.",
            },
            {
                "title": "Target Audience",
                "bullets": [
                    "Enterprise customers (1000+ employees)",
                    "Tech-savvy decision makers",
                    "Companies seeking digital transformation",
                    "Budget range: $50K - $500K annually",
                ],
            },
            {
                "header": "Strategy & Execution",
                "title": "Go-to-Market Strategy",
                "bullets": [
                    "Phase 1: Soft launch with beta customers (Month 1-2)",
                    "Phase 2: Public launch and PR campaign (Month 3)",
                    "Phase 3: Scale marketing efforts (Month 4-6)",
                    "Phase 4: Evaluate and optimize (Month 7+)",
                ],
            },
            {
                "title": "Marketing Channels",
                "bullets": [
                    "Content Marketing: Blog posts, whitepapers, case studies",
                    "Social Media: LinkedIn, Twitter, YouTube",
                    "Paid Advertising: Google Ads, LinkedIn Ads",
                    "Events: Trade shows, webinars, conferences",
                    "Partner Marketing: Co-marketing with strategic partners",
                ],
            },
            {
                "header": "Metrics & Success",
                "title": "Key Performance Indicators",
                "bullets": [
                    "Lead generation: 500 qualified leads per month",
                    "Conversion rate: 5% from lead to customer",
                    "Customer acquisition cost: < $5,000",
                    "ROI: 3x marketing spend by end of Q2",
                ],
            },
        ],
        "closing": {"title": "Let's Launch Successfully!", "subtitle": "Questions & Discussion"},
    }

    print("Creating product launch presentation...")

    result = agent.create_presentation_from_content(
        content_dict=content, output_path="examples/output/product_launch.pptx"
    )

    if result.success:
        print(f"✓ Success! Created {result.slide_count} slides")
        print(f"✓ Saved to: {result.output_path}")
        print(f"✓ Using color scheme: {content['color_scheme']}")
    else:
        print(f"✗ Error: {result.error}")


if __name__ == "__main__":
    main()
