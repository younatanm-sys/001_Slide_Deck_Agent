"""Data models for slide deck generation."""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SlideType(str, Enum):
    """Types of slides that can be created."""

    TITLE = "title"
    TITLE_CONTENT = "title_content"
    SECTION_HEADER = "section_header"
    TWO_COLUMN = "two_column"
    BULLET_POINTS = "bullet_points"
    IMAGE_CAPTION = "image_caption"
    QUOTE = "quote"
    THANK_YOU = "thank_you"
    BLANK = "blank"


class SlideContent(BaseModel):
    """Content for a single slide."""

    slide_type: SlideType
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None
    bullet_points: Optional[List[str]] = None
    left_content: Optional[str] = None
    right_content: Optional[str] = None
    image_path: Optional[str] = None
    caption: Optional[str] = None
    quote_text: Optional[str] = None
    quote_author: Optional[str] = None
    notes: Optional[str] = Field(default=None, description="Speaker notes")
    chart_data: Optional[Dict[str, Any]] = Field(default=None, description="Chart data with categories and series")
    source: Optional[str] = Field(default=None, description="Source attribution for footer")


class PresentationRequest(BaseModel):
    """Request for creating a presentation."""

    topic: str = Field(description="Main topic or title of the presentation")
    slides: List[SlideContent] = Field(default_factory=list)
    output_path: str = Field(default="presentation.pptx")
    template: str = Field(default="modern", description="Template style to use")

    # Theme settings
    primary_color: Optional[str] = Field(default="#1F4788", description="Primary color (hex)")
    secondary_color: Optional[str] = Field(default="#2E7D32", description="Secondary color (hex)")
    background_color: Optional[str] = Field(default="#FFFFFF", description="Background color (hex)")
    text_color: Optional[str] = Field(default="#333333", description="Text color (hex)")

    # Metadata
    author: Optional[str] = None
    company: Optional[str] = None


class GenerationResult(BaseModel):
    """Result of presentation generation."""

    success: bool
    output_path: Optional[str] = None
    slide_count: int = 0
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
