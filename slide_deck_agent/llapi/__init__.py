"""
LLAPI - LLM Layer for Slide Deck Generation
============================================

This module provides the AI content generation layer that sits on top of
the template engine. It uses LLMs to generate slide content from source
documents or topic prompts.

Architecture:
    User Input (Document/Topic) → LLAPI → SlideContent objects → Template Engine → PowerPoint

Components:
    - ContentGenerator: Main class for generating slide content via LLM
    - DocumentParser: Parses source documents (text, markdown, PDF)
    - StructureRecommender: Recommends optimal slide structure based on content
    - PromptTemplates: Pre-built prompts for different presentation types

Usage:
    from slide_deck_agent.llapi import ContentGenerator

    generator = ContentGenerator(api_key="your-api-key")
    slides = generator.generate_from_document(
        document_path="source.md",
        presentation_type="investor_pitch",
        max_slides=15
    )
"""

from .content_generator import ContentGenerator
from .document_parser import DocumentParser
from .structure_recommender import StructureRecommender
from .prompt_templates import PromptTemplates

__all__ = [
    "ContentGenerator",
    "DocumentParser",
    "StructureRecommender",
    "PromptTemplates",
]
