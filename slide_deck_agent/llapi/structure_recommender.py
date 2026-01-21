"""
Structure Recommender for LLAPI
===============================

Recommends optimal slide structure based on content analysis.
"""

from typing import List, Dict, Any, Optional
from .prompt_templates import PromptTemplates


class StructureRecommender:
    """Recommend slide structure based on content and presentation type."""

    def __init__(self):
        """Initialize the structure recommender."""
        self.templates = PromptTemplates.STRUCTURE_TEMPLATES

    def get_available_types(self) -> List[str]:
        """Get list of available presentation types."""
        return list(self.templates.keys())

    def get_template(self, presentation_type: str) -> Dict[str, Any]:
        """
        Get structure template for a presentation type.

        Args:
            presentation_type: Type of presentation (e.g., 'investor_pitch')

        Returns:
            Template dictionary with structure information
        """
        return self.templates.get(
            presentation_type,
            self.templates["investor_pitch"]
        )

    def recommend_structure(
        self,
        content_sections: Dict[str, str],
        presentation_type: str = "investor_pitch",
        max_slides: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Recommend slide structure based on available content.

        This is a rule-based recommendation that maps content sections
        to slide types. For AI-powered recommendations, use the LLM
        with get_structure_analysis_prompt().

        Args:
            content_sections: Dictionary of section name -> content
            presentation_type: Type of presentation
            max_slides: Maximum number of slides

        Returns:
            List of recommended slide specifications
        """
        template = self.get_template(presentation_type)
        recommended = []

        # Map content sections to slide types
        section_mapping = self._get_section_mapping(presentation_type)

        for slide_spec in template["structure"]:
            if len(recommended) >= max_slides:
                break

            slide_type = slide_spec["type"]

            # Find matching content
            matching_content = self._find_matching_content(
                slide_type,
                content_sections,
                section_mapping
            )

            if matching_content:
                recommended.append({
                    "slide_type": slide_type,
                    "purpose": slide_spec["purpose"],
                    "source_content": matching_content,
                    "has_content": True
                })
            else:
                # Include in structure but mark as needing content
                recommended.append({
                    "slide_type": slide_type,
                    "purpose": slide_spec["purpose"],
                    "source_content": None,
                    "has_content": False
                })

        return recommended

    def _get_section_mapping(self, presentation_type: str) -> Dict[str, List[str]]:
        """
        Get mapping from slide types to content section keywords.

        Args:
            presentation_type: Type of presentation

        Returns:
            Dictionary mapping slide types to section name patterns
        """
        # Common mappings that work across presentation types
        return {
            "problem": ["problem", "challenge", "pain", "issue", "current_state"],
            "solution": ["solution", "approach", "answer", "product", "offering"],
            "market": ["market", "opportunity", "tam", "sam", "som", "size"],
            "value_proposition": ["value", "proposition", "differentiator", "benefit", "pillar"],
            "product": ["product", "feature", "capability", "platform", "service"],
            "traction": ["traction", "milestone", "achievement", "progress", "roadmap"],
            "business_model": ["business", "model", "revenue", "monetization", "unit_economics"],
            "go_to_market": ["go_to_market", "gtm", "distribution", "channel", "launch"],
            "competition": ["competition", "competitive", "moat", "advantage", "differentiation"],
            "team": ["team", "founder", "leadership", "experience"],
            "financials": ["financial", "projection", "forecast", "revenue", "growth"],
            "ask": ["ask", "raise", "funding", "investment", "use_of_funds"],
            "vision": ["vision", "future", "mission", "long_term"],
            "executive_summary": ["executive", "summary", "overview", "key_points"],
            "situation": ["situation", "context", "background", "current"],
            "challenges": ["challenge", "issue", "problem", "obstacle"],
            "options": ["option", "alternative", "scenario", "approach"],
            "recommendation": ["recommendation", "propose", "suggest", "path"],
            "implementation": ["implementation", "execute", "plan", "action"],
            "timeline": ["timeline", "roadmap", "phase", "schedule"],
            "risks": ["risk", "mitigation", "concern", "challenge"],
            "next_steps": ["next", "step", "action", "follow_up"],
        }

    def _find_matching_content(
        self,
        slide_type: str,
        content_sections: Dict[str, str],
        section_mapping: Dict[str, List[str]]
    ) -> Optional[str]:
        """
        Find content that matches a slide type.

        Args:
            slide_type: Type of slide to match
            content_sections: Available content sections
            section_mapping: Mapping from slide types to keywords

        Returns:
            Matching content string or None
        """
        keywords = section_mapping.get(slide_type, [slide_type])

        for section_name, content in content_sections.items():
            section_lower = section_name.lower()

            for keyword in keywords:
                if keyword in section_lower:
                    return content

        return None

    def validate_structure(
        self,
        recommended_structure: List[Dict[str, Any]],
        min_slides: int = 5
    ) -> Dict[str, Any]:
        """
        Validate a recommended structure.

        Args:
            recommended_structure: List of slide specifications
            min_slides: Minimum required slides

        Returns:
            Validation result with status and issues
        """
        issues = []

        # Check minimum slides
        slides_with_content = [s for s in recommended_structure if s.get("has_content")]
        if len(slides_with_content) < min_slides:
            issues.append(
                f"Only {len(slides_with_content)} slides have content, "
                f"minimum required is {min_slides}"
            )

        # Check for critical missing slides (for investor pitch)
        critical_types = ["problem", "solution"]
        for ctype in critical_types:
            has_type = any(
                s["slide_type"] == ctype and s.get("has_content")
                for s in recommended_structure
            )
            if not has_type:
                issues.append(f"Missing critical slide type: {ctype}")

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "total_slides": len(recommended_structure),
            "slides_with_content": len(slides_with_content)
        }
