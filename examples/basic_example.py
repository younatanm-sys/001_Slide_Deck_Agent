"""Basic example of using the Slide Deck Agent."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from slide_deck_agent import SlideDeckAgent


def main():
    """Create a simple presentation from a topic."""
    # Initialize the agent
    agent = SlideDeckAgent()

    # Create a presentation from just a topic
    print("Creating presentation on 'Artificial Intelligence in Healthcare'...")

    result = agent.create_presentation_from_topic(
        topic="Artificial Intelligence in Healthcare",
        num_slides=10,
        output_path="examples/output/ai_healthcare.pptx",
        color_scheme="modern_tech",
        author="Your Name",
        company="Your Company",
    )

    if result.success:
        print(f"✓ Success! Created {result.slide_count} slides")
        print(f"✓ Saved to: {result.output_path}")
    else:
        print(f"✗ Error: {result.error}")


if __name__ == "__main__":
    main()
