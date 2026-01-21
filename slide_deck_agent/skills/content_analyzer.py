"""Skill for analyzing and structuring content for presentations."""

from typing import List, Dict, Any
from ..models import SlideContent, SlideType


class ContentAnalyzerSkill:
    """Skill for analyzing content and suggesting slide structures."""

    def analyze_topic(self, topic: str, num_slides: int = 10) -> List[SlideContent]:
        """
        Analyze a topic and generate a suggested slide structure.

        This is a template method that provides basic structure.
        In practice, this would be enhanced with AI/LLM integration.

        Args:
            topic: The presentation topic
            num_slides: Desired number of slides

        Returns:
            List of SlideContent objects with suggested structure
        """
        slides = []

        # Title slide
        slides.append(
            SlideContent(
                slide_type=SlideType.TITLE,
                title=topic,
                subtitle="A Comprehensive Overview",
                notes="Introduction slide - set the stage for the presentation",
            )
        )

        # Agenda/Overview
        slides.append(
            SlideContent(
                slide_type=SlideType.BULLET_POINTS,
                title="Agenda",
                bullet_points=[
                    "Introduction and Background",
                    "Key Concepts and Principles",
                    "Current State and Challenges",
                    "Solutions and Recommendations",
                    "Next Steps and Conclusion",
                ],
                notes="Outline what will be covered in the presentation",
            )
        )

        # Section: Introduction
        slides.append(
            SlideContent(
                slide_type=SlideType.SECTION_HEADER, title="Introduction & Background"
            )
        )

        slides.append(
            SlideContent(
                slide_type=SlideType.TITLE_CONTENT,
                title="Background",
                content="Provide context and background information about the topic. "
                "Explain why this topic is important and relevant to the audience.",
                notes="Establish foundation and context for the presentation",
            )
        )

        # Section: Key Concepts
        slides.append(SlideContent(slide_type=SlideType.SECTION_HEADER, title="Key Concepts"))

        slides.append(
            SlideContent(
                slide_type=SlideType.TWO_COLUMN,
                title="Core Principles",
                left_content="Concept 1:\nExplain the first key concept or principle "
                "that is fundamental to understanding this topic.",
                right_content="Concept 2:\nExplain the second key concept or principle "
                "that complements the first one.",
                notes="Break down complex concepts into digestible parts",
            )
        )

        # Main content slides
        slides.append(
            SlideContent(
                slide_type=SlideType.BULLET_POINTS,
                title="Key Points",
                bullet_points=[
                    "First important point about the topic",
                    "Second critical aspect to consider",
                    "Third essential element",
                    "Fourth supporting detail",
                ],
                notes="Main content - adjust based on your specific topic",
            )
        )

        # Quote or insight
        slides.append(
            SlideContent(
                slide_type=SlideType.QUOTE,
                quote_text="Insert a relevant, impactful quote that reinforces your message",
                quote_author="Author Name",
                notes="Use quotes to add credibility and emphasize key messages",
            )
        )

        # Recommendations/Next Steps
        slides.append(
            SlideContent(
                slide_type=SlideType.BULLET_POINTS,
                title="Next Steps",
                bullet_points=[
                    "Immediate action item #1",
                    "Short-term goal #2",
                    "Long-term objective #3",
                ],
                notes="Clear actionable items for the audience",
            )
        )

        # Thank you slide
        slides.append(
            SlideContent(
                slide_type=SlideType.THANK_YOU,
                title="Thank You",
                subtitle="Questions & Discussion",
                notes="Open floor for questions and discussion",
            )
        )

        return slides[:num_slides]

    def structure_content(self, content_dict: Dict[str, Any]) -> List[SlideContent]:
        """
        Structure raw content into slides.

        Args:
            content_dict: Dictionary with content sections and data

        Returns:
            List of SlideContent objects
        """
        slides = []

        # Title
        if "title" in content_dict:
            slides.append(
                SlideContent(
                    slide_type=SlideType.TITLE,
                    title=content_dict["title"],
                    subtitle=content_dict.get("subtitle"),
                )
            )

        # Sections
        if "sections" in content_dict:
            for section in content_dict["sections"]:
                # Section header
                if section.get("header"):
                    slides.append(
                        SlideContent(
                            slide_type=SlideType.SECTION_HEADER, title=section["header"]
                        )
                    )

                # Section content
                if section.get("bullets"):
                    slides.append(
                        SlideContent(
                            slide_type=SlideType.BULLET_POINTS,
                            title=section.get("title"),
                            bullet_points=section["bullets"],
                        )
                    )
                elif section.get("content"):
                    slides.append(
                        SlideContent(
                            slide_type=SlideType.TITLE_CONTENT,
                            title=section.get("title"),
                            content=section["content"],
                        )
                    )

        # Closing
        if content_dict.get("closing"):
            slides.append(
                SlideContent(
                    slide_type=SlideType.THANK_YOU,
                    title=content_dict["closing"].get("title", "Thank You"),
                    subtitle=content_dict["closing"].get("subtitle"),
                )
            )

        return slides

    def split_long_content(self, content: str, max_chars: int = 500) -> List[str]:
        """
        Split long content into multiple slides.

        Args:
            content: Long text content
            max_chars: Maximum characters per slide

        Returns:
            List of content chunks
        """
        sentences = content.split(". ")
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chars:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def extract_bullet_points(self, text: str) -> List[str]:
        """
        Extract bullet points from text.

        Args:
            text: Text containing bullet points or list items

        Returns:
            List of bullet point strings
        """
        lines = text.split("\n")
        bullets = []

        for line in lines:
            line = line.strip()
            # Remove common bullet point markers
            if line.startswith(("- ", "* ", "• ", "→ ")):
                bullets.append(line[2:].strip())
            elif line and line[0].isdigit() and ". " in line:
                # Handle numbered lists
                bullets.append(line.split(". ", 1)[1].strip())
            elif line:
                bullets.append(line)

        return [b for b in bullets if b]  # Remove empty strings
