"""
LLM-Powered Label Engine - Data Storyteller
=============================================

Uses LLM intelligence to generate human-readable, insight-driven labels
for chart annotations. The Python code sends structured data, and the LLM
returns polished narrative text.

PRINCIPLE 6 - Insight Over Information:
The LLM acts as a "Data Storyteller," transforming raw numbers into
meaningful insights that communicate the story behind the data.
"""

import json
import os
from typing import Dict, Any, Optional, Union
from pydantic import BaseModel


# =============================================================================
# LABEL ENGINE SYSTEM PROMPT
# =============================================================================

LABEL_ENGINE_SYSTEM_PROMPT = """You are a Data Storyteller AI specialized in creating concise, impactful labels for chart annotations.

Your role is to transform raw data into human-readable insights that tell a story.

RULES FOR LABEL GENERATION:

1. DIFFERENCE LABELS:
   - Primary line: State the absolute difference with currency/unit (e.g., "€28 savings")
   - Secondary line: Show percentage in parentheses (e.g., "(62% reduction)")
   - Use action words: "savings", "reduction", "increase", "growth", "decline"
   - Keep primary line under 15 characters
   - Keep secondary line under 20 characters

2. CAGR LABELS:
   - Format: "X-Year CAGR: +/-Y%"
   - Calculate years from data series length minus 1
   - Use + for positive, - for negative CAGR
   - Round to nearest whole percent

3. GENERAL PRINCIPLES:
   - Be concise - every character counts on a chart
   - Lead with impact - the most important number first
   - Use professional business language
   - Format numbers consistently (e.g., €1.2M not €1,200,000)

Always respond with valid JSON only. No explanations or markdown."""


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class DifferenceLabelRequest(BaseModel):
    """Request for generating a difference line label."""
    task: str = "generate_difference_label"
    start_value: float
    end_value: float
    currency: str = "€"
    direction: str = "reduction"  # "reduction", "increase", "change"


class DifferenceLabelResponse(BaseModel):
    """Response containing difference line label text."""
    primary: str  # e.g., "€28 savings"
    secondary: str  # e.g., "(62% reduction)"


class CAGRLabelRequest(BaseModel):
    """Request for generating a CAGR arrow label."""
    task: str = "generate_cagr_label"
    data_series: list  # e.g., [22, 35, 42, 55, 65]
    cagr_value: float  # e.g., 0.31 for 31%


class CAGRLabelResponse(BaseModel):
    """Response containing CAGR label text."""
    label: str  # e.g., "4-Year CAGR: +31%"


# =============================================================================
# LLM-POWERED LABEL ENGINE
# =============================================================================

class LLMPoweredLabelEngine:
    """
    LLM-Powered Label Engine for intelligent annotation text generation.

    PRINCIPLE 6 - Insight Over Information:
    Uses LLM reasoning to transform raw data into meaningful, insight-driven
    labels that tell a story rather than just displaying numbers.
    """

    def __init__(
        self,
        provider: str = "anthropic",
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize the label engine.

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
            pass  # No API key needed for mock mode

    def generate_difference_label(
        self,
        start_value: float,
        end_value: float,
        currency: str = "€",
        direction: str = "reduction"
    ) -> DifferenceLabelResponse:
        """
        Generate a difference line annotation label.

        Args:
            start_value: The starting value (e.g., 45)
            end_value: The ending value (e.g., 17)
            currency: Currency symbol (default "€")
            direction: "reduction", "increase", or "change"

        Returns:
            DifferenceLabelResponse with primary and secondary text
        """
        request = DifferenceLabelRequest(
            start_value=start_value,
            end_value=end_value,
            currency=currency,
            direction=direction
        )

        if self.provider == "mock":
            return self._generate_difference_label_locally(request)

        prompt = f"""Generate a label for this difference annotation.

Input Data:
{json.dumps(request.model_dump(), indent=2)}

Return a JSON object with "primary" and "secondary" fields."""

        try:
            if self.provider == "anthropic":
                result = self._call_anthropic(prompt)
            elif self.provider == "openai":
                result = self._call_openai(prompt)
            else:
                return self._generate_difference_label_locally(request)

            return DifferenceLabelResponse(
                primary=result.get("primary", ""),
                secondary=result.get("secondary", "")
            )
        except Exception as e:
            print(f"LLM call failed, using local calculation: {e}")
            return self._generate_difference_label_locally(request)

    def generate_cagr_label(
        self,
        data_series: list,
        cagr_value: float
    ) -> CAGRLabelResponse:
        """
        Generate a CAGR arrow annotation label.

        Args:
            data_series: List of values over time (e.g., [22, 35, 42, 55, 65])
            cagr_value: The CAGR as a decimal (e.g., 0.31 for 31%)

        Returns:
            CAGRLabelResponse with the label text
        """
        request = CAGRLabelRequest(
            data_series=data_series,
            cagr_value=cagr_value
        )

        if self.provider == "mock":
            return self._generate_cagr_label_locally(request)

        prompt = f"""Generate a label for this CAGR annotation.

Input Data:
{json.dumps(request.model_dump(), indent=2)}

Return a JSON object with a "label" field."""

        try:
            if self.provider == "anthropic":
                result = self._call_anthropic(prompt)
            elif self.provider == "openai":
                result = self._call_openai(prompt)
            else:
                return self._generate_cagr_label_locally(request)

            return CAGRLabelResponse(
                label=result.get("label", "")
            )
        except Exception as e:
            print(f"LLM call failed, using local calculation: {e}")
            return self._generate_cagr_label_locally(request)

    def _generate_difference_label_locally(
        self,
        request: DifferenceLabelRequest
    ) -> DifferenceLabelResponse:
        """
        Generate difference label using local logic (fallback/mock mode).

        Implements the same Data Storyteller rules programmatically.
        """
        start = request.start_value
        end = request.end_value
        currency = request.currency
        direction = request.direction

        # Calculate absolute difference
        diff = abs(start - end)

        # Calculate percentage change
        if start != 0:
            pct_change = abs((start - end) / start) * 100
        else:
            pct_change = 0

        # Format the difference with appropriate magnitude
        if diff >= 1000000:
            diff_formatted = f"{currency}{diff/1000000:.1f}M"
        elif diff >= 1000:
            diff_formatted = f"{currency}{diff/1000:.1f}K"
        else:
            diff_formatted = f"{currency}{diff:.0f}"

        # Determine action word based on direction
        if direction == "reduction":
            action = "savings"
            pct_word = "reduction"
        elif direction == "increase":
            action = "increase"
            pct_word = "increase"
        else:
            action = "change"
            pct_word = "change"

        primary = f"{diff_formatted} {action}"
        secondary = f"({pct_change:.0f}% {pct_word})"

        return DifferenceLabelResponse(primary=primary, secondary=secondary)

    def _generate_cagr_label_locally(
        self,
        request: CAGRLabelRequest
    ) -> CAGRLabelResponse:
        """
        Generate CAGR label using local logic (fallback/mock mode).

        Implements the same Data Storyteller rules programmatically.
        """
        years = len(request.data_series) - 1
        cagr_pct = request.cagr_value * 100

        # Format with sign
        sign = "+" if cagr_pct >= 0 else ""

        label = f"{years}-Year CAGR: {sign}{cagr_pct:.0f}%"

        return CAGRLabelResponse(label=label)

    def _call_anthropic(self, prompt: str) -> Dict[str, Any]:
        """Call Anthropic Claude API for label generation."""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            message = client.messages.create(
                model=self.model,
                max_tokens=256,
                system=LABEL_ENGINE_SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text
            json_str = self._extract_json(response_text)
            return json.loads(json_str)

        except ImportError:
            raise RuntimeError("anthropic package not installed")
        except Exception as e:
            raise RuntimeError(f"Anthropic API call failed: {e}")

    def _call_openai(self, prompt: str) -> Dict[str, Any]:
        """Call OpenAI API for label generation."""
        try:
            import openai

            client = openai.OpenAI(api_key=self.api_key)

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": LABEL_ENGINE_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=256,
                temperature=0
            )

            response_text = response.choices[0].message.content
            json_str = self._extract_json(response_text)
            return json.loads(json_str)

        except ImportError:
            raise RuntimeError("openai package not installed")
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {e}")

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


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_label_engine(
    provider: str = "mock",
    api_key: Optional[str] = None,
    model: Optional[str] = None
) -> LLMPoweredLabelEngine:
    """
    Factory function to create a label engine instance.

    Args:
        provider: 'anthropic', 'openai', or 'mock'
        api_key: Optional API key
        model: Optional model override

    Returns:
        Configured LLMPoweredLabelEngine instance
    """
    return LLMPoweredLabelEngine(
        provider=provider,
        api_key=api_key,
        model=model
    )
