"""Main agent class for slide deck generation."""

import json
from typing import Optional, List, Dict, Any
from pathlib import Path

from .models import PresentationRequest, SlideContent, GenerationResult
from .skills.slide_generator import SlideGeneratorSkill
from .skills.content_analyzer import ContentAnalyzerSkill
from .skills.design_optimizer import DesignOptimizerSkill
from .skills.main_slide_generator import MainSlideGeneratorSkill
from .templates import list_templates


class SlideDeckAgent:
    """
    AI Agent for creating industry-standard PowerPoint presentations.

    This agent combines multiple skills:
    - Content analysis and structuring
    - Slide generation with professional layouts
    - Design optimization with color schemes
    - Main template for professional presentations
    """

    def __init__(self, template: str = "default"):
        """
        Initialize the slide deck agent with all skills.

        Args:
            template: Template to use ('default', 'main')
        """
        self.template = template.lower()

        # Initialize slide generator (Main template is the default)
        if self.template in ["main", "default"]:
            self.slide_generator = MainSlideGeneratorSkill()
        else:
            self.slide_generator = SlideGeneratorSkill()

        self.content_analyzer = ContentAnalyzerSkill()
        self.design_optimizer = DesignOptimizerSkill()

    def create_presentation_from_topic(
        self,
        topic: str,
        num_slides: int = 10,
        output_path: str = "presentation.pptx",
        color_scheme: Optional[str] = None,
        author: Optional[str] = None,
        company: Optional[str] = None,
        template: Optional[str] = None,
    ) -> GenerationResult:
        """
        Create a presentation from just a topic.

        Args:
            topic: Main presentation topic
            num_slides: Number of slides to generate
            output_path: Where to save the presentation
            color_scheme: Optional color scheme name
            author: Optional author name
            company: Optional company name
            template: Optional template override ('main')

        Returns:
            GenerationResult with success status and metadata
        """
        # Use template override if provided
        if template:
            original_generator = self.slide_generator
            if template.lower() in ["main", "default"]:
                self.slide_generator = MainSlideGeneratorSkill()
            else:
                self.slide_generator = SlideGeneratorSkill()

        try:
            # Analyze topic and generate structure
            slides = self.content_analyzer.analyze_topic(topic, num_slides)

            # Suggest color scheme if not provided (skip for Main template as it has its own colors)
            template_with_colors = ["main"]
            skip_color_scheme = template and template.lower() in template_with_colors

            if not color_scheme and not skip_color_scheme:
                color_scheme = self.design_optimizer.suggest_color_scheme(topic)

            # Create presentation request
            request = PresentationRequest(
                topic=topic, slides=slides, output_path=output_path, author=author, company=company
            )

            # Apply color scheme (skip for templates with their own color systems)
            if not skip_color_scheme:
                request = self.design_optimizer.apply_color_scheme(request, color_scheme)

            # Generate presentation
            return self.slide_generator.create_presentation(request)

        finally:
            # Restore original generator if we swapped it
            if template:
                self.slide_generator = original_generator

    def create_presentation_from_content(
        self, content_dict: Dict[str, Any], output_path: str = "presentation.pptx"
    ) -> GenerationResult:
        """
        Create a presentation from structured content.

        Args:
            content_dict: Dictionary with presentation content
            output_path: Where to save the presentation

        Returns:
            GenerationResult with success status and metadata

        Example content_dict:
        {
            "title": "My Presentation",
            "subtitle": "A comprehensive overview",
            "sections": [
                {
                    "header": "Introduction",
                    "title": "Background",
                    "content": "Some content here..."
                },
                {
                    "title": "Key Points",
                    "bullets": ["Point 1", "Point 2", "Point 3"]
                }
            ],
            "closing": {
                "title": "Thank You",
                "subtitle": "Questions?"
            }
        }
        """
        # Structure content into slides
        slides = self.content_analyzer.structure_content(content_dict)

        # Create presentation request
        topic = content_dict.get("title", "Presentation")
        request = PresentationRequest(
            topic=topic,
            slides=slides,
            output_path=output_path,
            author=content_dict.get("author"),
            company=content_dict.get("company"),
        )

        # Apply color scheme
        color_scheme = content_dict.get("color_scheme", "corporate_blue")
        request = self.design_optimizer.apply_color_scheme(request, color_scheme)

        # Generate presentation
        return self.slide_generator.create_presentation(request)

    def create_custom_presentation(self, request: PresentationRequest) -> GenerationResult:
        """
        Create a presentation from a full PresentationRequest.

        This method gives you complete control over all aspects of the presentation.

        Args:
            request: Complete PresentationRequest with all details

        Returns:
            GenerationResult with success status and metadata
        """
        return self.slide_generator.create_presentation(request)

    def add_slides_to_existing(
        self, existing_path: str, new_slides: List[SlideContent], output_path: Optional[str] = None
    ) -> GenerationResult:
        """
        Add slides to an existing presentation.

        Args:
            existing_path: Path to existing presentation
            new_slides: List of slides to add
            output_path: Where to save (defaults to overwriting existing)

        Returns:
            GenerationResult with success status and metadata
        """
        # This would require loading existing presentation
        # For now, creating new presentation with the slides
        if not output_path:
            output_path = existing_path

        request = PresentationRequest(
            topic="Extended Presentation", slides=new_slides, output_path=output_path
        )

        return self.slide_generator.create_presentation(request)

    def get_available_color_schemes(self) -> List[str]:
        """Get list of available color schemes."""
        return self.design_optimizer.get_available_schemes()

    def get_color_scheme_preview(self, scheme_name: str) -> Dict[str, str]:
        """Get colors for a specific scheme."""
        return self.design_optimizer.get_scheme_colors(scheme_name)

    def get_available_templates(self) -> List[str]:
        """Get list of available company templates."""
        return list_templates()

    def get_current_template(self) -> str:
        """Get the currently active template."""
        return self.template

    def validate_presentation_request(self, request: PresentationRequest) -> List[str]:
        """
        Validate a presentation request and return any issues.

        Args:
            request: PresentationRequest to validate

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        if not request.topic:
            errors.append("Topic is required")

        if not request.slides:
            errors.append("At least one slide is required")

        if not request.output_path:
            errors.append("Output path is required")

        # Validate output path
        output_path = Path(request.output_path)
        if output_path.suffix.lower() != ".pptx":
            errors.append("Output path must have .pptx extension")

        # Validate color formats
        for color_field in ["primary_color", "secondary_color", "background_color", "text_color"]:
            color = getattr(request, color_field)
            if color and not color.startswith("#"):
                errors.append(f"{color_field} must be in hex format (#RRGGBB)")

        return errors

    def save_presentation_template(
        self, request: PresentationRequest, template_path: str
    ) -> bool:
        """
        Save a presentation request as a reusable template.

        Args:
            request: PresentationRequest to save as template
            template_path: Where to save the template JSON

        Returns:
            True if successful
        """
        try:
            template_data = request.model_dump()
            Path(template_path).write_text(json.dumps(template_data, indent=2))
            return True
        except Exception:
            return False

    def load_presentation_template(self, template_path: str) -> Optional[PresentationRequest]:
        """
        Load a presentation template from JSON.

        Args:
            template_path: Path to template JSON file

        Returns:
            PresentationRequest or None if failed
        """
        try:
            template_data = json.loads(Path(template_path).read_text())
            return PresentationRequest(**template_data)
        except Exception:
            return None
