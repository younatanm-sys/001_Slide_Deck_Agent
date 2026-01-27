"""Data models for slide deck generation."""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SlideType(str, Enum):
    """
    Types of slides that can be created.

    Note: Layout decisions (50/50, full-width, two-column text) are made
    automatically by the template engine based on content. These types
    define the slide's fundamental purpose, not its layout.
    """

    TITLE = "title"
    STANDARD_CONTENT = "standard_content"  # Universal content slide - layout determined by content
    SECTION_HEADER = "section_header"
    QUOTE = "quote"
    THANK_YOU = "thank_you"
    BLANK = "blank"

    # Legacy aliases for backwards compatibility (map to STANDARD_CONTENT)
    TITLE_CONTENT = "standard_content"
    TWO_COLUMN = "standard_content"
    BULLET_POINTS = "standard_content"
    IMAGE_CAPTION = "standard_content"


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
    """
    Request for creating a presentation.

    Note: Color palette is controlled exclusively by the template engine
    (defined in main_template_config.py). User-configurable colors have been
    removed to protect brand integrity and ensure consistent, professional output.
    """

    topic: str = Field(description="Main topic or title of the presentation")
    slides: List[SlideContent] = Field(default_factory=list)
    output_path: str = Field(default="presentation.pptx")
    template: str = Field(default="main", description="Template to use (main is the only supported template)")

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


# =============================================================================
# LLM-POWERED LABEL ENGINE MODELS
# =============================================================================
# PRINCIPLE 6 - Insight Over Information:
# These models support the LLM's role as a "Data Storyteller," transforming
# raw numbers into meaningful insights.

class LabelGenerationRequest(BaseModel):
    """
    Base request for LLM-powered label generation.

    The LLM Label Engine uses these requests to generate human-readable,
    insight-driven labels for chart annotations.
    """
    task: str = Field(description="The type of label to generate")


class DifferenceLabelRequest(LabelGenerationRequest):
    """
    Request for generating a difference line annotation label.

    Example:
        Input: {"task": "generate_difference_label", "start_value": 45, "end_value": 17, "currency": "€", "direction": "reduction"}
        Output: {"primary": "€28 savings", "secondary": "(62% reduction)"}
    """
    task: str = "generate_difference_label"
    start_value: float = Field(description="The starting value")
    end_value: float = Field(description="The ending value")
    currency: str = Field(default="€", description="Currency symbol")
    direction: str = Field(default="reduction", description="'reduction', 'increase', or 'change'")


class DifferenceLabelResponse(BaseModel):
    """Response containing difference line label text."""
    primary: str = Field(description="Primary label line (e.g., '€28 savings')")
    secondary: str = Field(description="Secondary label line (e.g., '(62% reduction)')")


class CAGRLabelRequest(LabelGenerationRequest):
    """
    Request for generating a CAGR arrow annotation label.

    Example:
        Input: {"task": "generate_cagr_label", "data_series": [22, 35, 42, 55, 65], "cagr_value": 0.31}
        Output: {"label": "4-Year CAGR: +31%"}
    """
    task: str = "generate_cagr_label"
    data_series: List[float] = Field(description="List of values over time")
    cagr_value: float = Field(description="CAGR as a decimal (e.g., 0.31 for 31%)")


class CAGRLabelResponse(BaseModel):
    """Response containing CAGR label text."""
    label: str = Field(description="The CAGR label (e.g., '4-Year CAGR: +31%')")
