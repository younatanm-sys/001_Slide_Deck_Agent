"""
Content Generator - Main LLAPI Class
=====================================

Uses LLMs to generate slide content from source documents or prompts.
Outputs SlideContent objects that feed directly into the template engine.
"""

import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..models import SlideContent, SlideType, PresentationRequest
from .document_parser import DocumentParser
from .structure_recommender import StructureRecommender
from .prompt_templates import PromptTemplates


class ContentGenerator:
    """
    Generate slide content using LLMs.

    This class sits between user input and the template engine:
    User Input → ContentGenerator → SlideContent objects → Template Engine → PowerPoint

    Supports multiple LLM providers:
    - Anthropic Claude (default)
    - OpenAI GPT
    - Mock mode for testing
    """

    def __init__(
        self,
        provider: str = "anthropic",
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize the content generator.

        Args:
            provider: LLM provider ('anthropic', 'openai', or 'mock')
            api_key: API key (defaults to environment variable)
            model: Model name (defaults based on provider)
        """
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model

        # Initialize components
        self.parser = DocumentParser()
        self.structure_recommender = StructureRecommender()
        self.prompts = PromptTemplates()

        # Set up provider-specific configuration
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
            # No API key needed for mock mode
            pass
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def generate_from_document(
        self,
        source: str,
        presentation_type: str = "investor_pitch",
        max_slides: int = 15,
        audience: str = "investors",
        duration_minutes: int = 15,
        title: Optional[str] = None,
        company: Optional[str] = None
    ) -> PresentationRequest:
        """
        Generate a complete presentation from a source document.

        This is the main entry point for document-based generation.

        Args:
            source: File path or raw text content
            presentation_type: Type of presentation (see PromptTemplates.STRUCTURE_TEMPLATES)
            max_slides: Maximum number of slides to generate
            audience: Target audience description
            duration_minutes: Presentation duration
            title: Override presentation title (default: extracted from content)
            company: Company/subtitle for title slide

        Returns:
            PresentationRequest ready for template engine
        """
        # Parse the source document
        content = self.parser.parse(source)

        # Generate slides using LLM
        slides_data = self._generate_slides_via_llm(
            content=content,
            presentation_type=presentation_type,
            max_slides=max_slides,
            audience=audience,
            duration_minutes=duration_minutes
        )

        # Convert to SlideContent objects
        slides = self._convert_to_slide_content(slides_data)

        # Create presentation request
        return PresentationRequest(
            topic=title or slides_data.get("presentation_title", "Presentation"),
            company=company or slides_data.get("subtitle", ""),
            slides=slides,
            output_path="generated_presentation.pptx"
        )

    def generate_from_prompt(
        self,
        topic: str,
        key_points: List[str],
        presentation_type: str = "investor_pitch",
        max_slides: int = 10,
        audience: str = "general"
    ) -> PresentationRequest:
        """
        Generate a presentation from a topic and key points.

        Args:
            topic: Main topic/title of the presentation
            key_points: List of key points to cover
            presentation_type: Type of presentation
            max_slides: Maximum number of slides
            audience: Target audience

        Returns:
            PresentationRequest ready for template engine
        """
        # Construct pseudo-document from key points
        content = f"Topic: {topic}\n\n"
        content += "Key Points:\n"
        for point in key_points:
            content += f"• {point}\n"

        return self.generate_from_document(
            source=content,
            presentation_type=presentation_type,
            max_slides=max_slides,
            audience=audience,
            title=topic
        )

    def _generate_slides_via_llm(
        self,
        content: str,
        presentation_type: str,
        max_slides: int,
        audience: str,
        duration_minutes: int
    ) -> Dict[str, Any]:
        """
        Call LLM to generate slide content.

        Args:
            content: Source document content
            presentation_type: Type of presentation
            max_slides: Maximum slides
            audience: Target audience
            duration_minutes: Duration

        Returns:
            Dictionary with presentation structure and content
        """
        # Get the prompt
        prompt = PromptTemplates.get_full_presentation_prompt(
            document_content=content,
            presentation_type=presentation_type,
            max_slides=max_slides,
            audience=audience,
            duration_minutes=duration_minutes
        )

        # Call LLM based on provider
        if self.provider == "mock":
            return self._mock_generate(content, max_slides)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt)
        elif self.provider == "openai":
            return self._call_openai(prompt)

    def _call_anthropic(self, prompt: str) -> Dict[str, Any]:
        """Call Anthropic Claude API."""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            message = client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=PromptTemplates.SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Parse JSON response
            response_text = message.content[0].text

            # Extract JSON from response (handle markdown code blocks)
            json_str = self._extract_json(response_text)
            return json.loads(json_str)

        except ImportError:
            raise ImportError(
                "Anthropic package not installed. "
                "Install with: pip install anthropic"
            )
        except Exception as e:
            raise RuntimeError(f"Anthropic API call failed: {str(e)}")

    def _call_openai(self, prompt: str) -> Dict[str, Any]:
        """Call OpenAI API."""
        try:
            import openai

            client = openai.OpenAI(api_key=self.api_key)

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": PromptTemplates.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4096,
                temperature=0.7
            )

            # Parse JSON response
            response_text = response.choices[0].message.content

            # Extract JSON from response
            json_str = self._extract_json(response_text)
            return json.loads(json_str)

        except ImportError:
            raise ImportError(
                "OpenAI package not installed. "
                "Install with: pip install openai"
            )
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {str(e)}")

    def _mock_generate(self, content: str, max_slides: int) -> Dict[str, Any]:
        """
        Generate mock slides for testing without API calls.

        This creates a structured presentation that demonstrates how
        the LLAPI would work with a real LLM. The mock output follows
        consulting best practices with insight-driven titles.
        """
        content_lower = content.lower()

        # Check if this is the Musk Ecosystem Bank content
        if "musk ecosystem bank" in content_lower or ("tesla" in content_lower and "spacex" in content_lower):
            return self._mock_musk_bank_slides(max_slides)

        # Check if this is the Retail Transformation content
        if "retail" in content_lower and ("e-commerce" in content_lower or "digital transformation" in content_lower):
            return self._mock_retail_transformation_slides(max_slides)

        # For other content, use intelligent parsing
        return self._mock_parse_content(content, max_slides)

    def _mock_musk_bank_slides(self, max_slides: int) -> Dict[str, Any]:
        """Generate mock slides specifically for the Musk Ecosystem Bank demo."""
        slides = [
            {
                "slide_number": 1,
                "slide_type": "problem",
                "title": "Traditional banks fail to integrate with modern tech ecosystems",
                "bullet_points": [
                    "Financial services remain siloed from consumers' daily technology experiences",
                    "Banking lacks connection to sustainable transportation and clean energy choices",
                    "No unified financial platform serves users across multiple technology platforms",
                    "Remote and mobile users face connectivity barriers with traditional banking"
                ]
            },
            {
                "slide_number": 2,
                "slide_type": "solution",
                "title": "Musk Ecosystem Bank unifies finance with Tesla, SpaceX, and X platforms",
                "bullet_points": [
                    "Digital-only bank integrating financial services across Musk's technology ecosystem",
                    "Leverages innovation ethos to reimagine banking for the sustainable tech lifestyle",
                    "Initially U.S.-based with plans for global expansion",
                    "Functions as financial 'umbrella' connecting Tesla, SpaceX, and X users"
                ]
            },
            {
                "slide_number": 3,
                "slide_type": "value_proposition",
                "title": "Sustainable Banking ties deposits directly to green initiatives",
                "bullet_points": [
                    "Funds finance electric vehicles, solar projects, and clean technology",
                    "Customers actively help fight climate change through their banking choices",
                    "Carbon credit incentives reward environmentally friendly behaviors",
                    "EV drivers receive rewards for sustainable transportation choices"
                ]
            },
            {
                "slide_number": 4,
                "slide_type": "value_proposition",
                "title": "Ecosystem Synergy delivers unified financial tools across platforms",
                "bullet_points": [
                    "Tesla owners, SpaceX enthusiasts, and X users get exclusive perks",
                    "Digital wallet integrates directly into Tesla vehicle interfaces",
                    "Seamless payment for charging, services, and purchases via car interface",
                    "Similar integration model to Amazon's financial services partnerships"
                ]
            },
            {
                "slide_number": 5,
                "slide_type": "product",
                "title": "AI-first approach powers proactive, personalized banking experiences",
                "bullet_points": [
                    "Advanced algorithms enhance user experience and operational efficiency",
                    "AI-driven credit scoring analyzes alternative data for inclusive lending",
                    "Real-time advice alerts users to optimal charging times and costs",
                    "Intelligent trip planning with optimal Supercharger stop recommendations"
                ]
            },
            {
                "slide_number": 6,
                "slide_type": "market",
                "title": "Starlink enables global banking accessibility anywhere on Earth",
                "bullet_points": [
                    "High-speed satellite internet connects remote users to banking services",
                    "Bank aims to serve customers anywhere on the planet via Starlink",
                    "Positions as 'everything app' for finance that transcends borders",
                    "Mobile and remote users gain unprecedented financial access"
                ]
            },
            {
                "slide_number": 7,
                "slide_type": "differentiation",
                "title": "Four key differentiators set Musk Ecosystem Bank apart",
                "bullet_points": [
                    "Sustainable Banking: Green initiatives and carbon credit rewards",
                    "Ecosystem Synergy: Unified tools across Tesla, SpaceX, and X",
                    "Innovative Tech & AI: Proactive, intelligent financial services",
                    "Global Accessibility: Starlink-powered worldwide reach"
                ]
            },
            {
                "slide_number": 8,
                "slide_type": "vision",
                "title": "The bank enables seamless integration of finance with sustainable tech lifestyle",
                "bullet_points": [
                    "Connects financial life with EV ownership experiences",
                    "Bridges banking to space exploration enthusiasm",
                    "Integrates social media engagement with financial services",
                    "Creates exclusive experiences across the entire Musk ecosystem"
                ]
            }
        ]

        return {
            "presentation_title": "Musk Ecosystem Bank",
            "subtitle": "Integrating Tesla, SpaceX, and X",
            "slides": slides[:max_slides]
        }

    def _mock_retail_transformation_slides(self, max_slides: int) -> Dict[str, Any]:
        """Generate mock slides specifically for the BCG Retail Transformation demo."""
        slides = [
            {
                "slide_number": 1,
                "slide_type": "executive_summary",
                "title": "E-commerce growing 45% CAGR will represent 70% of revenue by 2027",
                "bullet_points": [
                    "Store sales declining 8% annually as customers shift to digital channels",
                    "E-commerce revenue projected to reach €2.8B by 2027",
                    "Mobile commerce now represents 65% of digital sales, up from 42% in 2023",
                    "Omnichannel customers spend 3.2x more than single-channel shoppers"
                ],
                "chart_data": {
                    "type": "column",
                    "title": "Revenue Mix Transformation (€B)",
                    "categories": ["2023", "2024E", "2025E", "2026E", "2027E"],
                    "series": [
                        {"name": "Store Sales", "values": [3.2, 2.9, 2.7, 2.5, 2.3]},
                        {"name": "E-commerce", "values": [1.2, 1.8, 2.2, 2.5, 2.8]}
                    ],
                    "highlight_index": 1,
                    "source": "Source: Company financials, BCG analysis"
                }
            },
            {
                "slide_number": 2,
                "slide_type": "situation",
                "title": "Mobile-first shopping behavior now dominant across all demographics",
                "bullet_points": [
                    "Gen Z and Millennials drive 68% of mobile commerce volume",
                    "Average order value on mobile increased 23% YoY to €87",
                    "Mobile app users show 2.8x higher retention than mobile web",
                    "Push notifications drive 42% conversion uplift vs. email campaigns"
                ],
                "chart_data": {
                    "type": "column",
                    "title": "Mobile vs. Desktop E-commerce (€M)",
                    "categories": ["2023", "2024E", "2025E", "2026E", "2027E"],
                    "series": [
                        {"name": "Desktop", "values": [700, 720, 760, 800, 840]},
                        {"name": "Mobile", "values": [500, 1080, 1440, 1700, 1960]}
                    ],
                    "highlight_index": 1,
                    "annotations": [
                        {
                            "type": "cagr_arrow",
                            "series_index": 1,
                            "from_category": 0,
                            "to_category": 4,
                            "label": "45% CAGR"
                        }
                    ],
                    "source": "Source: Google Analytics, App Annie"
                }
            },
            {
                "slide_number": 3,
                "slide_type": "situation",
                "title": "Western Europe and North America lead with 55%+ digital penetration",
                "bullet_points": [
                    "Western Europe: 58% digital penetration, €1.2B annual revenue",
                    "North America: 56% digital penetration, driven by mobile app adoption",
                    "Eastern Europe: 42% penetration, fastest growth region at 62% CAGR",
                    "Asia-Pacific: 38% penetration, significant untapped potential"
                ],
                "chart_data": {
                    "type": "column",
                    "title": "Digital Revenue by Region (€M)",
                    "categories": ["Western Europe", "North America", "Eastern Europe", "Asia-Pacific"],
                    "series": [
                        {"name": "Q1 2024", "values": [280, 260, 180, 150]},
                        {"name": "Q2 2024", "values": [310, 285, 220, 175]},
                        {"name": "Q3 2024", "values": [340, 295, 260, 190]},
                        {"name": "Q4 2024", "values": [370, 310, 295, 210]}
                    ],
                    "color_mode": "comparison",
                    "source": "Source: Regional sales data"
                }
            },
            {
                "slide_number": 4,
                "slide_type": "challenges",
                "title": "Digital-first strategy reducing CAC by 62%, from €45 to €17",
                "bullet_points": [
                    "Traditional marketing CAC: €45 (print, TV, direct mail)",
                    "Digital marketing CAC: €17 (social, search, influencer partnerships)",
                    "Organic social driving 40% of new acquisitions at €3 CAC",
                    "Referral program contributing 25% of acquisitions at €8 CAC"
                ],
                "chart_data": {
                    "type": "column",
                    "title": "Customer Acquisition Cost Evolution (€)",
                    "categories": ["Traditional\nMarketing", "Paid\nDigital", "Organic\nSocial", "Referral\nProgram", "Target\nBlended"],
                    "series": [
                        {"name": "CAC", "values": [45, 17, 3, 8, 12]}
                    ],
                    "highlight_index": 0,
                    "annotations": [
                        {
                            "type": "difference_line",
                            "series_index": 0,
                            "from_category": 0,
                            "to_category": 1,
                            "label": "€28 savings\n(62% reduction)"
                        }
                    ],
                    "source": "Source: Marketing analytics"
                }
            },
            {
                "slide_number": 5,
                "slide_type": "recommendation",
                "title": "€180M technology investment required for omnichannel excellence",
                "bullet_points": [
                    "Platform modernization: €65M for cloud-native e-commerce platform",
                    "Mobile apps: €35M for iOS/Android native apps with AR try-on",
                    "Data & analytics: €40M for CDP, ML personalization, real-time inventory",
                    "Store digitization: €40M for smart fitting rooms, endless aisle, mobile POS"
                ],
                "chart_data": {
                    "type": "waterfall",
                    "title": "Technology Investment Breakdown (€M)",
                    "categories": ["Current\nState", "E-commerce\nPlatform", "Mobile\nApps", "Data &\nAnalytics", "Store\nDigitization", "Total\nInvestment"],
                    "values": [0, 65, 35, 40, 40, 180],
                    "types": ["start", "increase", "increase", "increase", "increase", "end"]
                }
            },
            {
                "slide_number": 6,
                "slide_type": "recommendation",
                "title": "Omnichannel customers deliver 3.2x higher LTV at €1,280",
                "bullet_points": [
                    "Single-channel (store only): €400 LTV, 18-month retention",
                    "Single-channel (online only): €520 LTV, 24-month retention",
                    "Omnichannel (store + online): €1,280 LTV, 42-month retention",
                    "Omnichannel customers shop 2.4x more frequently across touchpoints"
                ],
                "chart_data": {
                    "type": "column",
                    "title": "Customer Lifetime Value by Channel Preference (€)",
                    "categories": ["Store\nOnly", "Online\nOnly", "Omnichannel"],
                    "series": [
                        {"name": "LTV", "values": [400, 520, 1280]}
                    ],
                    "highlight_index": 0,
                    "annotations": [
                        {
                            "type": "leader_line",
                            "x": 0.82,
                            "y": 0.92,
                            "text": "€1,280 LTV\n3.2x multiplier",
                            "direction": "right",
                            "line_length": 50
                        }
                    ],
                    "source": "Source: CRM analytics, cohort analysis"
                }
            },
            {
                "slide_number": 7,
                "slide_type": "implementation",
                "title": "18-month phased rollout minimizes risk while delivering value",
                "bullet_points": [
                    "Phase 1 (M1-6): Platform foundation, mobile app MVP, basic personalization",
                    "Phase 2 (M7-12): Omnichannel integration, advanced ML, store pilot",
                    "Phase 3 (M13-18): Full store rollout, AR features, inventory optimization",
                    "Quick wins in Phase 1: New mobile app, improved checkout, recommendations"
                ],
                "chart_data": {
                    "type": "column",
                    "title": "Cumulative Revenue Impact (€M)",
                    "categories": ["Phase 1\n(M1-6)", "Phase 2\n(M7-12)", "Phase 3\n(M13-18)", "Steady\nState"],
                    "series": [
                        {"name": "Incremental Revenue", "values": [15, 65, 180, 280]}
                    ],
                    "highlight_index": 0,
                    "annotations": [
                        {
                            "type": "callout",
                            "x": 0.25,
                            "y": 0.15,
                            "text": "Quick wins:\nMobile app",
                            "position": "above"
                        }
                    ]
                }
            },
            {
                "slide_number": 8,
                "slide_type": "risks",
                "title": "Transformation positions company as category leader with 68 NPS",
                "bullet_points": [
                    "Current NPS: 42 (industry average: 38)",
                    "Target NPS post-transformation: 68 (best-in-class benchmark)",
                    "Mobile app rated 4.7/5.0 stars (top 5% in retail category)",
                    "Omnichannel capabilities exceed 85% of direct competitors"
                ]
            },
            {
                "slide_number": 9,
                "slide_type": "next_steps",
                "title": "€420M annual revenue with 28% EBITDA margin by Year 3",
                "bullet_points": [
                    "Year 1: €80M incremental revenue, 18% margin",
                    "Year 2: €240M incremental revenue, 24% margin",
                    "Year 3: €420M incremental revenue, 28% margin (steady state)",
                    "Payback period: 16 months, 3-year NPV: €680M at 10% discount"
                ],
                "chart_data": {
                    "type": "column",
                    "title": "Incremental Annual Revenue & EBITDA (€M)",
                    "categories": ["Year 1", "Year 2", "Year 3"],
                    "series": [
                        {"name": "Revenue", "values": [80, 240, 420]},
                        {"name": "EBITDA", "values": [14, 58, 118]}
                    ],
                    "highlight_index": 0,
                    "source": "Source: Financial model, BCG analysis"
                }
            },
            {
                "slide_number": 10,
                "slide_type": "recommendation",
                "title": "Proceed with €180M investment - 16-month payback, €680M NPV",
                "bullet_points": [
                    "Compelling financial returns: 16-month payback period, €680M 3-year NPV",
                    "Strategic imperative: E-commerce shift is accelerating, not optional",
                    "Competitive necessity: Category leadership requires omnichannel excellence",
                    "Risk mitigation: Phased approach allows course correction and quick wins"
                ]
            }
        ]

        return {
            "presentation_title": "Retail Digital Transformation",
            "subtitle": "BCG Strategy Update",
            "slides": slides[:max_slides]
        }

    def _mock_parse_content(self, content: str, max_slides: int) -> Dict[str, Any]:
        """Parse content intelligently for mock generation."""
        # Parse sections from content
        sections = self.parser.extract_sections(content)

        # Create mock slides
        slides = []
        slide_num = 1

        # Extract key phrases for slide content
        lines = [l.strip() for l in content.split('\n') if l.strip()]

        # Simple heuristic: look for bullet points or key phrases
        current_bullets = []
        current_title = None

        for line in lines:
            # Check for headers (potential slide titles)
            if line.startswith('#') or line.endswith(':'):
                # Save previous slide if exists
                if current_title and current_bullets and slide_num <= max_slides:
                    slides.append({
                        "slide_number": slide_num,
                        "slide_type": "content",
                        "title": current_title,
                        "bullet_points": current_bullets[:4]  # Max 4 bullets
                    })
                    slide_num += 1
                    current_bullets = []

                current_title = line.lstrip('#').rstrip(':').strip()

            # Check for bullet points
            elif line.startswith(('•', '-', '*', '–')):
                bullet = line.lstrip('•-*– ').strip()
                if bullet:
                    current_bullets.append(bullet)

            # Check for key phrases (sentences with important keywords)
            elif any(kw in line.lower() for kw in ['key', 'important', 'main', 'value', 'benefit']):
                if len(current_bullets) < 6:
                    current_bullets.append(line)

        # Save last slide
        if current_title and current_bullets and slide_num <= max_slides:
            slides.append({
                "slide_number": slide_num,
                "slide_type": "content",
                "title": current_title,
                "bullet_points": current_bullets[:4]
            })

        # If we didn't get enough slides, create generic ones
        if len(slides) < 3:
            slides = self._create_generic_slides(content, max_slides)

        return {
            "presentation_title": slides[0]["title"] if slides else "Presentation",
            "subtitle": "",
            "slides": slides[:max_slides]
        }

    def _create_generic_slides(self, content: str, max_slides: int) -> List[Dict]:
        """Create generic slides when parsing doesn't find structure."""
        # Split content into chunks
        words = content.split()
        chunk_size = len(words) // min(max_slides, 10)

        slides = []
        for i in range(min(max_slides, 10)):
            start = i * chunk_size
            end = start + chunk_size
            chunk = ' '.join(words[start:end])

            # Extract sentences for bullets
            sentences = [s.strip() for s in chunk.split('.') if len(s.strip()) > 20]

            slides.append({
                "slide_number": i + 1,
                "slide_type": "content",
                "title": f"Key Points - Part {i + 1}",
                "bullet_points": sentences[:4] if sentences else ["Content from source document"]
            })

        return slides

    def _extract_json(self, text: str) -> str:
        """Extract JSON from LLM response (handles markdown code blocks)."""
        # Try to find JSON in code blocks
        import re

        # Look for ```json ... ``` blocks
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
        if json_match:
            return json_match.group(1).strip()

        # Look for { ... } directly
        brace_match = re.search(r'\{[\s\S]*\}', text)
        if brace_match:
            return brace_match.group(0)

        # Return as-is and hope for the best
        return text

    def _convert_to_slide_content(self, slides_data: Dict[str, Any]) -> List[SlideContent]:
        """
        Convert LLM output to SlideContent objects.

        Args:
            slides_data: Dictionary from LLM with slides array

        Returns:
            List of SlideContent objects ready for template engine
        """
        slides = []

        for slide_dict in slides_data.get("slides", []):
            # Build slide with chart_data if present
            slide = SlideContent(
                slide_type=SlideType.TITLE_CONTENT,
                title=slide_dict.get("title", "Untitled Slide"),
                bullet_points=slide_dict.get("bullet_points", []),
                chart_data=slide_dict.get("chart_data")  # Pass through chart data
            )
            slides.append(slide)

        return slides

    def refine_title(self, draft_title: str, slide_type: str = "content") -> str:
        """
        Use LLM to refine a slide title to be more insight-driven.

        Args:
            draft_title: Current draft title
            slide_type: Type of slide

        Returns:
            Refined title
        """
        prompt = PromptTemplates.get_title_refinement_prompt(draft_title, slide_type)

        if self.provider == "mock":
            # Simple mock refinement
            if not draft_title[0].isupper():
                draft_title = draft_title.capitalize()
            if not any(c in draft_title for c in '.!?'):
                draft_title = draft_title.rstrip() + " - key insight"
            return draft_title

        # Call LLM for refinement
        if self.provider == "anthropic":
            result = self._call_anthropic(prompt)
        elif self.provider == "openai":
            result = self._call_openai(prompt)

        return result.get("refined_title", draft_title)

    def refine_bullets(self, bullets: List[str], title: str) -> List[str]:
        """
        Use LLM to refine bullet points.

        Args:
            bullets: Current bullet points
            title: Slide title for context

        Returns:
            Refined bullet points
        """
        prompt = PromptTemplates.get_bullet_refinement_prompt(bullets, title)

        if self.provider == "mock":
            # Simple mock refinement - ensure parallel structure
            return [b.strip().rstrip('.') for b in bullets]

        # Call LLM for refinement
        if self.provider == "anthropic":
            result = self._call_anthropic(prompt)
        elif self.provider == "openai":
            result = self._call_openai(prompt)

        return result.get("refined_bullets", bullets)
