# Slide Deck Agent

An AI-powered agent that generates professional PowerPoint presentations using Claude API and Claude Code.

---

## Quick Start with Claude Desktop App

If you're using the **Claude Desktop App** (with Claude Code enabled), follow these steps:

### Step 1: Clone or Download the Project

**Option A — Clone from GitHub (recommended):**
```bash
git clone https://github.com/younatanm-sys/001_Slide_Deck_Agent.git
cd 001_Slide_Deck_Agent
```

**Option B — Download ZIP:**
1. Go to the GitHub repository page and click **Code → Download ZIP**
2. Unzip it to a location on your computer (e.g., Desktop or Documents)
3. You should now have a folder called `001_Slide_Deck_Agent`

### Step 2: Open the Project in Claude

1. Open the **Claude Desktop App**
2. Click the folder icon (bottom left) or use `Cmd+O` (Mac) / `Ctrl+O` (Windows)
3. Navigate to and select the `001_Slide_Deck_Agent` folder
4. Claude will now have access to all the project files

### Step 3: Get Your Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up or log in
3. Navigate to "API Keys" and create a new key
4. Copy the key (starts with `sk-ant-...`)

### Step 4: Ask Claude to Generate a Presentation

In the Claude chat, type something like:

> "Run the main_retail_transformation_llapi.py script. Here is my API key: sk-ant-your-key-here"

Or simply:

> "Generate a presentation about [your topic] using the slide deck agent"

Claude will run the script and create your PowerPoint file.

### Step 5: Find Your Presentation

The generated `.pptx` file will be saved in the project folder. You can ask Claude:

> "Where was the presentation saved?"

---

## Alternative: Command Line Setup

If you prefer running manually from Terminal:

### Step 1: Install Python Dependencies

```bash
cd 001_Slide_Deck_Agent
pip install python-pptx anthropic pydantic pillow
```

### Step 2: Set Your Anthropic API Key

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### Step 3: Run the Main Script

```bash
python main_retail_transformation_llapi.py
```

**No API key? Use mock mode for testing:**
```bash
python main_retail_transformation_llapi.py --mock
```

**Additional options:**
```bash
# Limit number of slides
python main_retail_transformation_llapi.py --max-slides 8

# Custom output file
python main_retail_transformation_llapi.py --output my_presentation.pptx
```

---

## Important: API Key Requirement

| Claude Pro / Max | Anthropic API |
|------------------|---------------|
| Chat subscription at claude.ai | Developer access at console.anthropic.com |
| $20-$100/month fixed | Pay per token (~$3/million input tokens) |
| For personal chat | For running this tool |

**You need an Anthropic API key** from console.anthropic.com — this is separate from your Claude Pro/Max subscription.

> **Tip:** Run with `--mock` flag to test the full pipeline without using any API credits.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│  CLAUDE CODE + CLAUDE API                                                │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  Orchestration Layer (Claude Code)                                 │  │
│  │  SlideDeckAgent orchestrates three specialized skills:             │  │
│  │  ┌──────────────┐  ┌───────────────┐  ┌────────────────┐          │  │
│  │  │ContentAnalyzer│→│DesignOptimizer│→│ SlideGenerator │          │  │
│  │  └──────────────┘  └───────────────┘  └────────────────┘          │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  LLAPI Layer (Claude API - claude-3-5-sonnet)                      │  │
│  │  ContentGenerator: Source Document → Structured SlideContent       │  │
│  │  • Extracts key insights, metrics & executive takeaways            │  │
│  │  • Structures logical narrative flow across slides                 │  │
│  │  • Identifies optimal chart type for each dataset                  │  │
│  │  • Generates compelling headlines & supporting content             │  │
│  │  LLM Label Engine: Insight-driven chart annotation text            │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  DESIGN TEMPLATE ENGINE (Main v2.1)                                      │
│  ┌────────────────────────┐  ┌────────────────────────────────────────┐  │
│  │  Typography System     │  │  Color Intelligence                    │  │
│  │  • T1-T5 (24pt → 9pt)  │  │  • Story-driven modes: comparison,     │  │
│  │  • Dynamic label sizing│  │    highlight, category                 │  │
│  │  • Density-aware scale │  │  • Semantic color meaning              │  │
│  └────────────────────────┘  └────────────────────────────────────────┘  │
│  ┌────────────────────────┐  ┌────────────────────────────────────────┐  │
│  │  Chart Generation      │  │  Smart Layout Engine                   │  │
│  │  • Column, Waterfall,  │  │  • Auto legend redundancy removal      │  │
│  │    Matrix chart types  │  │  • Responsive Split-Screen 60/40       │  │
│  │  • Data-anchored CAGR  │  │  • Full-Width and Hero-Visual modes    │  │
│  │  • Difference Lines    │  │  • Zoned Integrity (Title/Content/     │  │
│  │  • Callout annotations │  │    Footer zones immutable)             │  │
│  └────────────────────────┘  └────────────────────────────────────────┘  │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  POWERPOINT OUTPUT                                                       │
│  • Executive-ready .pptx in seconds  • Fully editable native PowerPoint  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Features

### Core Capabilities

- **AI Content Generation**: Claude API reads your source document and generates a full slide structure — extracting key insights, metrics, and narrative flow automatically
- **Chart Generation**: Column charts, waterfall charts, and matrix charts rendered directly in PowerPoint
- **Chart Annotations**: CAGR arrows, difference lines, and callout labels placed automatically and labeled with AI-generated insight text
- **LLM Label Engine**: AI-powered annotation text that writes insight-driven labels (e.g. "45% CAGR") rather than raw data values
- **Professional Templates**: Multiple slide types including title, content, bullet points, two-column, charts, and more
- **Design Optimization**: 8+ professional color schemes with automatic contrast optimization and story-driven color logic
- **Full Customization**: Complete control over every aspect of your presentation
- **Speaker Notes**: Add presenter notes to any slide
- **Mock Mode**: Run the full pipeline without an API key for testing

### Slide Types

- **Title Slide**: Full-screen title and subtitle with branded background
- **Title & Content**: Standard content slide with title and body text
- **Section Header**: Visual break between presentation sections
- **Bullet Points**: Lists with proper hierarchy and spacing
- **Two Column**: Side-by-side content comparison (60/40 split)
- **Chart + Insight**: Chart on left with AI-generated insight bullets on right
- **Quote**: Highlighted quotations with attribution
- **Thank You**: Closing slide with call-to-action
- **Blank**: Custom layouts

### Chart Capabilities

- **Column Charts**: Grouped and single-series bar/column charts
- **Waterfall Charts**: Cumulative contribution charts for financials
- **Matrix Charts**: Multi-metric comparison grids
- **CAGR Annotations**: Automatically calculated and placed growth rate arrows
- **Difference Lines**: Visual connectors highlighting deltas between data points
- **Callout Labels**: AI-generated insight text anchored to data points

---

## Quick Start

### Example 1: Create from Topic Only

The simplest way to generate a presentation:

```python
from slide_deck_agent import SlideDeckAgent

agent = SlideDeckAgent()

result = agent.create_presentation_from_topic(
    topic="Artificial Intelligence in Healthcare",
    num_slides=10,
    output_path="ai_healthcare.pptx",
    color_scheme="modern_tech",
    author="Your Name"
)

if result.success:
    print(f"Created {result.slide_count} slides!")
```

### Example 2: Create from Structured Content

For more control over content:

```python
content = {
    "title": "Q1 Business Review",
    "subtitle": "2025 Performance",
    "color_scheme": "corporate_blue",
    "sections": [
        {
            "header": "Revenue",
            "title": "Q1 Performance",
            "bullets": [
                "Revenue up 25% YoY",
                "Record customer acquisition",
                "Expansion into new markets"
            ]
        },
        {
            "title": "Key Challenges",
            "content": "Despite strong growth, we face increasing competition..."
        }
    ],
    "closing": {
        "title": "Thank You",
        "subtitle": "Questions?"
    }
}

result = agent.create_presentation_from_content(
    content_dict=content,
    output_path="q1_review.pptx"
)
```

### Example 3: Full Custom Control

Complete control over every slide:

```python
from slide_deck_agent import SlideContent, SlideType, PresentationRequest

slides = [
    SlideContent(
        slide_type=SlideType.TITLE,
        title="My Presentation",
        subtitle="A Custom Approach",
        notes="Welcome and introduction"
    ),
    SlideContent(
        slide_type=SlideType.BULLET_POINTS,
        title="Key Points",
        bullet_points=[
            "First important point",
            "Second critical aspect",
            "Third essential element"
        ],
        notes="Emphasize the second point"
    ),
    SlideContent(
        slide_type=SlideType.QUOTE,
        quote_text="Innovation distinguishes between a leader and a follower",
        quote_author="Steve Jobs"
    )
]

request = PresentationRequest(
    topic="My Presentation",
    slides=slides,
    output_path="custom.pptx",
    primary_color="#1F4788",
    secondary_color="#2E7D32",
    author="Jane Doe"
)

result = agent.create_custom_presentation(request)
```

## Color Schemes

The agent includes 8 professional color schemes:

| Scheme | Best For | Primary Color |
|--------|----------|---------------|
| `corporate_blue` | Business, Finance | #1F4788 |
| `modern_tech` | Technology, Innovation | #2C3E50 |
| `vibrant_creative` | Creative, Marketing | #9B59B6 |
| `minimalist_gray` | Education, Research | #455A64 |
| `earth_tones` | Sustainability, Nature | #5D4037 |
| `ocean_blue` | Healthcare, Wellness | #006064 |
| `sunset` | Energy, Passion | #BF360C |
| `professional_green` | Environment, Growth | #1B5E20 |

### Using Color Schemes

```python
# Let the agent suggest based on topic
result = agent.create_presentation_from_topic(
    topic="Environmental Sustainability",
    color_scheme=None  # Agent will suggest "professional_green"
)

# Or specify explicitly
result = agent.create_presentation_from_topic(
    topic="Any Topic",
    color_scheme="vibrant_creative"
)

# View available schemes
schemes = agent.get_available_color_schemes()
print(schemes)

# Preview a scheme's colors
colors = agent.get_color_scheme_preview("modern_tech")
print(colors)  # {'primary': '#2C3E50', 'secondary': '#3498DB', ...}
```

## Agent Skills

The agent uses three specialized skills:

### 1. MainSlideGeneratorSkill

The primary slide renderer implementing the v2.1 design specification. Handles PowerPoint file creation with proper formatting, chart generation, chart annotations, and layout decisions.

### 2. SlideGeneratorSkill

A general-purpose slide generator for standard slide types without chart support.

### 3. ContentAnalyzerSkill

- Analyzes topics and generates appropriate slide structures
- Structures raw content into logical slides
- Splits long content across multiple slides
- Extracts bullet points from text

### 4. DesignOptimizerSkill

- Applies professional color schemes
- Ensures WCAG AA contrast compliance
- Suggests appropriate schemes based on topic
- Optimizes visual hierarchy

## LLAPI Layer

The `slide_deck_agent/llapi/` module handles all Claude API interactions:

- **ContentGenerator**: Reads a source document and produces structured `SlideContent` objects ready for rendering
- **LLMPoweredLabelEngine**: Generates insight-driven annotation text for chart labels (e.g. turns raw data into "45% CAGR — fastest growing region")
- **DocumentParser**: Parses and preprocesses source documents
- **StructureRecommender**: Recommends slide structure based on content type and audience
- **AnnotationPlacer**: Determines optimal placement for chart annotations

## API Reference

### SlideDeckAgent

#### Methods

**`create_presentation_from_topic(topic, num_slides, output_path, color_scheme, author, company)`**

Create a presentation from just a topic. The agent will generate an appropriate structure.

**`create_presentation_from_content(content_dict, output_path)`**

Create from structured content dictionary.

**`create_custom_presentation(request)`**

Create from a full `PresentationRequest` with complete control.

**`get_available_color_schemes()`**

Returns list of available color scheme names.

**`get_color_scheme_preview(scheme_name)`**

Returns color values for a specific scheme.

**`get_available_templates()`**

Returns list of available company templates.

**`validate_presentation_request(request)`**

Validates a request and returns list of errors (empty if valid).

### Models

#### SlideType (Enum)

- `TITLE` - Title slide
- `TITLE_CONTENT` - Title and content
- `SECTION_HEADER` - Section divider
- `TWO_COLUMN` - Two-column layout
- `BULLET_POINTS` - Bulleted list
- `IMAGE_CAPTION` - Image with caption
- `QUOTE` - Quotation slide
- `THANK_YOU` - Closing slide
- `BLANK` - Blank slide

#### SlideContent

Defines content for a single slide:

```python
SlideContent(
    slide_type: SlideType,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    content: Optional[str] = None,
    bullet_points: Optional[List[str]] = None,
    left_content: Optional[str] = None,  # For two-column
    right_content: Optional[str] = None,  # For two-column
    quote_text: Optional[str] = None,
    quote_author: Optional[str] = None,
    chart_data: Optional[Dict] = None,   # For chart slides
    notes: Optional[str] = None          # Speaker notes
)
```

#### PresentationRequest

Complete presentation specification:

```python
PresentationRequest(
    topic: str,
    slides: List[SlideContent],
    output_path: str = "presentation.pptx",
    template: str = "modern",
    primary_color: str = "#1F4788",
    secondary_color: str = "#2E7D32",
    background_color: str = "#FFFFFF",
    text_color: str = "#333333",
    author: Optional[str] = None,
    company: Optional[str] = None
)
```

#### GenerationResult

Result of presentation generation:

```python
GenerationResult(
    success: bool,
    output_path: Optional[str],
    slide_count: int,
    error: Optional[str],
    metadata: Dict[str, Any]
)
```

## Examples

See the `examples/` directory for complete working examples:

- `basic_example.py` - Simple topic-based generation
- `advanced_example.py` - Structured content with sections
- `custom_slides_example.py` - Full custom slide control
- `color_schemes_demo.py` - Showcase all color schemes

Run any example:

```bash
python examples/basic_example.py
```

## Project Structure

```
001_Slide_Deck_Agent/
├── slide_deck_agent/
│   ├── __init__.py
│   ├── agent.py                      # Main agent class
│   ├── models.py                     # Data models
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── main_slide_generator.py   # Primary renderer (v2.1 spec)
│   │   ├── slide_generator.py        # General-purpose slide renderer
│   │   ├── content_analyzer.py       # Content structuring
│   │   └── design_optimizer.py       # Design and colors
│   ├── llapi/
│   │   ├── __init__.py
│   │   ├── content_generator.py      # Claude API → SlideContent objects
│   │   ├── label_engine.py           # LLM-powered chart annotation text
│   │   ├── annotation_placer.py      # Chart annotation placement
│   │   ├── document_parser.py        # Source document preprocessing
│   │   ├── structure_recommender.py  # Slide structure recommendations
│   │   └── prompt_templates.py       # Claude prompt templates
│   └── templates/
│       ├── __init__.py
│       ├── template_registry.py      # Template registry
│       └── main_template_config.py   # Main v2.1 design config
├── examples/
│   ├── basic_example.py
│   ├── advanced_example.py
│   ├── custom_slides_example.py
│   └── color_schemes_demo.py
├── main_retail_transformation_llapi.py  # Main entry point / demo
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Best Practices

### Content Structure

1. **Start with a strong title slide** - Include subtitle for context
2. **Add an agenda/overview** - Help audience follow along
3. **Use section headers** - Break content into logical sections
4. **Limit bullet points** - 3-5 bullets per slide maximum
5. **Include speaker notes** - Remember what to say for each slide
6. **End with clear call-to-action** - Thank you slide with next steps

### Design

1. **Choose appropriate color scheme** - Match your topic/industry
2. **Maintain consistency** - Use the same scheme throughout
3. **Ensure readability** - Agent handles contrast automatically
4. **Don't overcrowd slides** - Less is more
5. **Use quotes strategically** - Break up dense content

### Code

1. **Validate requests** - Use `validate_presentation_request()`
2. **Handle errors** - Check `result.success` before proceeding
3. **Reuse templates** - Save/load common structures
4. **Organize content** - Use dictionaries for structured content

## Advanced Usage

### Creating Reusable Templates

```python
# Create a base template
request = PresentationRequest(
    topic="Template",
    slides=your_slides,
    primary_color="#1F4788",
    # ... other settings
)

# Save as template
agent.save_presentation_template(request, "templates/my_template.json")

# Load and reuse
template = agent.load_presentation_template("templates/my_template.json")
template.topic = "New Topic"
template.output_path = "new_presentation.pptx"

result = agent.create_custom_presentation(template)
```

### Custom Color Schemes

```python
request = PresentationRequest(
    topic="Custom Colors",
    slides=slides,
    primary_color="#FF5733",      # Your brand color
    secondary_color="#33FF57",    # Complementary color
    background_color="#FFFFFF",
    text_color="#333333",
    output_path="custom_colors.pptx"
)
```

## Limitations

- Images must be provided as file paths (not embedded)
- Animation and transitions not supported
- Video embedding not supported
- Master slide editing limited to code-defined templates

## Troubleshooting

**"ANTHROPIC_API_KEY not set" or "AuthenticationError"**
- Make sure you've exported the environment variable
- Restart your terminal after setting it
- Verify your key at https://console.anthropic.com
- Or run with `--mock` flag to test without an API key

**"ModuleNotFoundError: No module named 'pptx'"**
```bash
pip install python-pptx
```

**"ModuleNotFoundError: No module named 'anthropic'"**
```bash
pip install anthropic
```

**"ModuleNotFoundError: No module named 'pydantic'"**
```bash
pip install pydantic
```

**"ModuleNotFoundError: No module named 'PIL'"**
```bash
pip install pillow
```

**Presentation not generating / API errors**
- Check your API key has credits at console.anthropic.com
- Ensure you have internet connectivity
- Try mock mode first: `python main_retail_transformation_llapi.py --mock`

---

## License

MIT License - See LICENSE file for details

---

Built with Claude Code | Powered by Claude API (claude-3-5-sonnet)
