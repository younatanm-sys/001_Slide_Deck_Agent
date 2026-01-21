"""Template management for slide deck generation."""

from .template_registry import TemplateRegistry, get_template, list_templates
from .main_template_config import MAIN_CONFIG

__all__ = [
    "TemplateRegistry",
    "get_template",
    "list_templates",
    "MAIN_CONFIG",
]
