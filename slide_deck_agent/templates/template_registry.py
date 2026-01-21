"""
Template Registry for managing company-specific slide deck templates.

This module provides a centralized registry for managing different company
templates (AECOM, BCG, McKinsey, etc.) and allows easy switching between them.

Usage:
    from slide_deck_agent.templates import get_template

    # Get AECOM template
    aecom = get_template('aecom')
    colors = aecom['colors']

    # List all available templates
    from slide_deck_agent.templates import list_templates
    templates = list_templates()
"""

from typing import Dict, Any, Optional, List
from pathlib import Path


class TemplateRegistry:
    """Registry for managing slide deck templates."""

    _templates: Dict[str, Dict[str, Any]] = {}
    _initialized = False

    @classmethod
    def initialize(cls):
        """Initialize the template registry with available templates."""
        if cls._initialized:
            return

        # Register AECOM template
        try:
            from .aecom_template_config import AECOM_CONFIG
            cls.register_template('aecom', AECOM_CONFIG)
        except ImportError:
            pass

        # Register BCG template
        try:
            from .bcg_template_config import BCG_CONFIG
            cls.register_template('bcg', BCG_CONFIG)
        except ImportError:
            pass

        # Register default template
        cls.register_template('default', cls._get_default_template())

        cls._initialized = True

    @classmethod
    def register_template(cls, name: str, config: Dict[str, Any]):
        """
        Register a new template.

        Args:
            name: Template identifier (e.g., 'aecom', 'bcg', 'mckinsey')
            config: Template configuration dictionary
        """
        cls._templates[name.lower()] = config

    @classmethod
    def get_template(cls, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a template by name.

        Args:
            name: Template identifier

        Returns:
            Template configuration or None if not found
        """
        if not cls._initialized:
            cls.initialize()
        return cls._templates.get(name.lower())

    @classmethod
    def list_templates(cls) -> List[str]:
        """
        Get list of available template names.

        Returns:
            List of template identifiers
        """
        if not cls._initialized:
            cls.initialize()
        return list(cls._templates.keys())

    @classmethod
    def template_exists(cls, name: str) -> bool:
        """
        Check if a template exists.

        Args:
            name: Template identifier

        Returns:
            True if template exists
        """
        if not cls._initialized:
            cls.initialize()
        return name.lower() in cls._templates

    @staticmethod
    def _get_default_template() -> Dict[str, Any]:
        """Get the default template configuration."""
        from pptx.util import Inches, Pt
        from pptx.enum.text import PP_ALIGN

        return {
            'template_name': 'Default',
            'version': '1.0',
            'colors': {
                'primary_color': '#2E5090',
                'secondary_color': '#5B9BD5',
                'background_color': '#FFFFFF',
                'text_color': '#000000',
                'accent_color': '#FFC000',
            },
            'fonts': {
                'primary': 'Arial',
                'fallback': ['Helvetica', 'Sans-serif']
            },
            'font_sizes': {
                'cover_title': Pt(54),
                'cover_subtitle': Pt(32),
                'section_header': Pt(44),
                'slide_title': Pt(36),
                'heading': Pt(28),
                'body': Pt(18),
                'bullet_level_1': Pt(20),
                'bullet_level_2': Pt(18),
                'bullet_level_3': Pt(16),
                'caption': Pt(14),
                'footnote': Pt(12)
            },
            'spacing': {
                'margins': {
                    'standard': Inches(0.5),
                },
                'slide_margin_left': Inches(0.5),
                'slide_margin_right': Inches(0.5),
                'slide_margin_top': Inches(0.5),
                'slide_margin_bottom': Inches(0.5)
            }
        }


# Convenience functions
def get_template(name: str = 'default') -> Optional[Dict[str, Any]]:
    """
    Get a template configuration by name.

    Args:
        name: Template identifier (default: 'default')

    Returns:
        Template configuration dictionary
    """
    return TemplateRegistry.get_template(name)


def list_templates() -> List[str]:
    """
    Get list of available templates.

    Returns:
        List of template identifiers
    """
    return TemplateRegistry.list_templates()


def register_template(name: str, config: Dict[str, Any]):
    """
    Register a new template.

    Args:
        name: Template identifier
        config: Template configuration dictionary
    """
    TemplateRegistry.register_template(name, config)
