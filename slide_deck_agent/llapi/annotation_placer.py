"""
Annotation Placer - Visual Design AI
=====================================

Uses LLM intelligence for precise placement of chart annotations.
Receives chart geometry as JSON and returns coordinates for annotations.

This module handles complex visual layout decisions that programmatic
logic cannot reliably solve, such as:
- Difference line placement between bars
- Label collision avoidance
- Optimal positioning for readability
"""

import json
import os
from typing import Dict, Any, Optional


# Visual Design AI System Prompt
VISUAL_DESIGN_SYSTEM_PROMPT = """You are a Visual Design AI specialized in placing chart annotations.
Your role is to receive chart geometry data and return precise coordinates for annotations.

You must follow these strict rules for Difference Line annotations:

1. CALCULATE THE GUTTER: The line.position_x must be the exact midpoint between bar1.right_edge_x and bar2.left_edge_x.

2. SET LINE HEIGHT: The line.start_y and line.end_y must match the top_edge_y of the respective bars.

3. POSITION THE LABEL:
   - label.vertical_center_y = midpoint between line.start_y and line.end_y
   - label.position_x should be 10 pixels to the right of the line by default

4. COLLISION AVOIDANCE:
   - Estimate label width as approximately 100 pixels
   - If label.position_x + 100 > bar2.left_edge_x, there will be a collision
   - In case of collision, set placement_side to "left" and position label 10 pixels to the LEFT of the line

Always respond with valid JSON only. No explanations or markdown."""


class AnnotationPlacer:
    """
    Visual Design AI for intelligent annotation placement.

    Uses LLM reasoning to calculate precise coordinates for chart annotations,
    handling complex cases like collision avoidance and optimal positioning.
    """

    def __init__(
        self,
        provider: str = "anthropic",
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize the annotation placer.

        Args:
            provider: LLM provider ('anthropic', 'openai', or 'mock')
            api_key: API key (defaults to environment variable)
            model: Model name (defaults based on provider)
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model
        self._setup_provider()

    def _setup_provider(self):
        """Set up provider-specific configuration."""
        if self.provider == "anthropic":
            self.api_key = self.api_key or os.environ.get("ANTHROPIC_API_KEY")
            self.model = self.model or "claude-sonnet-4-20250514"
        elif self.provider == "openai":
            self.api_key = self.api_key or os.environ.get("OPENAI_API_KEY")
            self.model = self.model or "gpt-4"
        elif self.provider == "mock":
            pass

    def place_difference_line(
        self,
        bar1: Dict[str, float],
        bar2: Dict[str, float],
        label_text: str
    ) -> Dict[str, Any]:
        """
        Calculate placement for a difference line annotation.

        Args:
            bar1: Dict with 'left_edge_x', 'right_edge_x', 'top_edge_y' (in pixels)
            bar2: Dict with 'left_edge_x', 'right_edge_x', 'top_edge_y' (in pixels)
            label_text: The label text to display

        Returns:
            Dict with 'line' and 'label' positioning data
        """
        # Build input data structure
        input_data = {
            "chart_type": "column",
            "annotation_type": "difference_line",
            "bar1": bar1,
            "bar2": bar2,
            "label_text": label_text
        }

        if self.provider == "mock":
            return self._calculate_placement_locally(input_data)

        # Build prompt
        prompt = f"""Calculate the precise placement for this annotation.

Input Data:
{json.dumps(input_data, indent=2)}

Apply your Visual Design AI rules and return the annotation object with exact coordinates."""

        # Call LLM
        if self.provider == "anthropic":
            return self._call_anthropic(prompt)
        elif self.provider == "openai":
            return self._call_openai(prompt)
        else:
            return self._calculate_placement_locally(input_data)

    def _calculate_placement_locally(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate placement using local logic (fallback/mock mode).

        This implements the same Visual Design AI rules programmatically.
        """
        bar1 = input_data["bar1"]
        bar2 = input_data["bar2"]
        label_text = input_data["label_text"]

        # RULE 1: Calculate the Gutter
        gutter_centerline = (bar1["right_edge_x"] + bar2["left_edge_x"]) / 2

        # RULE 2: Set Line Height
        line_start_y = bar1["top_edge_y"]
        line_end_y = bar2["top_edge_y"]

        # RULE 3: Position the Label
        vertical_center_y = (line_start_y + line_end_y) / 2
        label_padding = 10  # 10 pixels
        label_width_estimate = 100  # Approximate label width

        # Default: place to the right
        label_x = gutter_centerline + label_padding
        placement_side = "right"

        # RULE 4: Collision Avoidance
        if label_x + label_width_estimate > bar2["left_edge_x"]:
            # Collision detected - move to left
            label_x = gutter_centerline - label_padding - label_width_estimate
            placement_side = "left"

        return {
            "line": {
                "type": "dashed",
                "color": "Negative Red",
                "start_y": line_start_y,
                "end_y": line_end_y,
                "position_x": gutter_centerline
            },
            "label": {
                "text": label_text,
                "position_x": label_x,
                "vertical_center_y": vertical_center_y,
                "placement_side": placement_side
            }
        }

    def _call_anthropic(self, prompt: str) -> Dict[str, Any]:
        """Call Anthropic Claude API for annotation placement."""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            message = client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=VISUAL_DESIGN_SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text
            json_str = self._extract_json(response_text)
            return json.loads(json_str)

        except ImportError:
            # Fall back to local calculation
            return self._calculate_placement_locally(json.loads(prompt.split("Input Data:\n")[1].split("\n\nApply")[0]))
        except Exception as e:
            # Fall back to local calculation on any error
            print(f"LLM call failed, using local calculation: {e}")
            return self._calculate_placement_locally(json.loads(prompt.split("Input Data:\n")[1].split("\n\nApply")[0]))

    def _call_openai(self, prompt: str) -> Dict[str, Any]:
        """Call OpenAI API for annotation placement."""
        try:
            import openai

            client = openai.OpenAI(api_key=self.api_key)

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": VISUAL_DESIGN_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
                temperature=0
            )

            response_text = response.choices[0].message.content
            json_str = self._extract_json(response_text)
            return json.loads(json_str)

        except ImportError:
            return self._calculate_placement_locally(json.loads(prompt.split("Input Data:\n")[1].split("\n\nApply")[0]))
        except Exception as e:
            print(f"LLM call failed, using local calculation: {e}")
            return self._calculate_placement_locally(json.loads(prompt.split("Input Data:\n")[1].split("\n\nApply")[0]))

    def _extract_json(self, text: str) -> str:
        """Extract JSON from response text, handling markdown code blocks."""
        text = text.strip()

        # Remove markdown code blocks
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        return text.strip()
