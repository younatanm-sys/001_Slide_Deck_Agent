"""Skill for optimizing presentation design and aesthetics."""

from typing import Dict, Tuple, List
from ..models import PresentationRequest


class DesignOptimizerSkill:
    """Skill for optimizing presentation design and color schemes."""

    # Predefined professional color schemes
    COLOR_SCHEMES = {
        "corporate_blue": {
            "primary": "#1F4788",
            "secondary": "#2E7D32",
            "background": "#FFFFFF",
            "text": "#333333",
            "accent": "#FF6B35",
        },
        "modern_tech": {
            "primary": "#2C3E50",
            "secondary": "#3498DB",
            "background": "#FFFFFF",
            "text": "#2C3E50",
            "accent": "#E74C3C",
        },
        "vibrant_creative": {
            "primary": "#9B59B6",
            "secondary": "#F39C12",
            "background": "#FFFFFF",
            "text": "#34495E",
            "accent": "#1ABC9C",
        },
        "minimalist_gray": {
            "primary": "#455A64",
            "secondary": "#78909C",
            "background": "#FAFAFA",
            "text": "#263238",
            "accent": "#FF7043",
        },
        "earth_tones": {
            "primary": "#5D4037",
            "secondary": "#8D6E63",
            "background": "#FFF8E1",
            "text": "#3E2723",
            "accent": "#43A047",
        },
        "ocean_blue": {
            "primary": "#006064",
            "secondary": "#0097A7",
            "background": "#E0F7FA",
            "text": "#004D40",
            "accent": "#FF6F00",
        },
        "sunset": {
            "primary": "#BF360C",
            "secondary": "#F4511E",
            "background": "#FFF3E0",
            "text": "#3E2723",
            "accent": "#FFB300",
        },
        "professional_green": {
            "primary": "#1B5E20",
            "secondary": "#388E3C",
            "background": "#FFFFFF",
            "text": "#263238",
            "accent": "#FBC02D",
        },
    }

    def apply_color_scheme(
        self, request: PresentationRequest, scheme_name: str = "corporate_blue"
    ) -> PresentationRequest:
        """
        Apply a predefined color scheme to a presentation request.

        Args:
            request: PresentationRequest to modify
            scheme_name: Name of the color scheme to apply

        Returns:
            Modified PresentationRequest
        """
        scheme = self.COLOR_SCHEMES.get(scheme_name, self.COLOR_SCHEMES["corporate_blue"])

        request.primary_color = scheme["primary"]
        request.secondary_color = scheme["secondary"]
        request.background_color = scheme["background"]
        request.text_color = scheme["text"]

        return request

    def suggest_color_scheme(self, topic: str) -> str:
        """
        Suggest an appropriate color scheme based on the presentation topic.

        Args:
            topic: Presentation topic

        Returns:
            Name of suggested color scheme
        """
        topic_lower = topic.lower()

        # Technology/Innovation
        if any(
            word in topic_lower for word in ["tech", "ai", "digital", "software", "innovation"]
        ):
            return "modern_tech"

        # Finance/Business
        if any(
            word in topic_lower for word in ["business", "finance", "corporate", "strategy"]
        ):
            return "corporate_blue"

        # Environment/Sustainability
        if any(
            word in topic_lower
            for word in ["environment", "sustainability", "green", "eco", "nature"]
        ):
            return "professional_green"

        # Creative/Design
        if any(word in topic_lower for word in ["creative", "design", "art", "marketing"]):
            return "vibrant_creative"

        # Education/Research
        if any(word in topic_lower for word in ["education", "research", "academic", "science"]):
            return "minimalist_gray"

        # Default
        return "corporate_blue"

    def optimize_contrast(self, bg_color: str, text_color: str) -> Tuple[str, str]:
        """
        Ensure sufficient contrast between background and text colors.

        Args:
            bg_color: Background color (hex)
            text_color: Text color (hex)

        Returns:
            Tuple of (background_color, text_color) with optimized contrast
        """
        bg_luminance = self._calculate_luminance(bg_color)
        text_luminance = self._calculate_luminance(text_color)

        contrast_ratio = self._contrast_ratio(bg_luminance, text_luminance)

        # WCAG AA standard requires 4.5:1 for normal text
        if contrast_ratio < 4.5:
            # If background is light, make text darker
            if bg_luminance > 0.5:
                text_color = "#000000"
            else:
                text_color = "#FFFFFF"

        return bg_color, text_color

    def _calculate_luminance(self, hex_color: str) -> float:
        """Calculate relative luminance of a color."""
        hex_color = hex_color.lstrip("#")
        r, g, b = [int(hex_color[i : i + 2], 16) / 255.0 for i in (0, 2, 4)]

        # Convert to linear RGB
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4

        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def _contrast_ratio(self, lum1: float, lum2: float) -> float:
        """Calculate contrast ratio between two luminance values."""
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        return (lighter + 0.05) / (darker + 0.05)

    def get_available_schemes(self) -> List[str]:
        """Get list of available color schemes."""
        return list(self.COLOR_SCHEMES.keys())

    def get_scheme_colors(self, scheme_name: str) -> Dict[str, str]:
        """Get colors for a specific scheme."""
        return self.COLOR_SCHEMES.get(scheme_name, self.COLOR_SCHEMES["corporate_blue"])
