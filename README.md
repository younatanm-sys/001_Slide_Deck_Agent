# Slide Deck Agent

An AI-powered agent that generates professional PowerPoint presentations using Claude API and Claude Code.

---

## Quick Start with Claude Desktop App

If you're using the **Claude Desktop App** (with Claude Code enabled), follow these steps:

### Step 1: Download and Unzip the Project

1. Download the `Slide_Deck_Agent.zip` file you received
2. Unzip it to a location on your computer (e.g., Desktop or Documents)
3. You should now have a folder called `001_Slide_Deck_Agent`

### Step 2: Open the Project in Claude

1. Open the **Claude Desktop App**
2. Click the folder icon (bottom left) or use `Cmd+O` (Mac) / `Ctrl+O` (Windows)
3. Navigate to and select the `001_Slide_Deck_Agent` folder you just unzipped
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
pip install python-pptx anthropic pydantic
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

### Step 3: Run an Example

```bash
python main_retail_transformation_llapi.py
```

---

## Important: API Key Requirement

| Claude Pro / Max | Anthropic API |
|------------------|---------------|
| Chat subscription at claude.ai | Developer access at console.anthropic.com |
| $20-$100/month fixed | Pay per token (~$3/million input tokens) |
| For personal chat | For running this tool |

**You need an Anthropic API key** from console.anthropic.com - this is separate from your Claude Pro/Max subscription.

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
│  │  Intelligence Layer (Claude API - claude-3-5-sonnet)               │  │
│  │  • Extracts key insights, metrics & executive takeaways            │  │
│  │  • Structures logical narrative flow across slides                 │  │
│  │  • Identifies optimal visualization type for each dataset          │  │
│  │  • Generates compelling headlines & supporting content             │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  DESIGN TEMPLATE ENGINE                                                  │
│  ┌────────────────────────┐  ┌────────────────────────────────────────┐  │
│  │  Typography System     │  │  Color Intelligence                    │  │
│  │  • T1-T5 (24pt → 9pt)  │  │  • Story-driven modes: comparison,     │  │
│  │  • Dynamic label sizing│  │    highlight, category                 │  │
│  │  • Density-aware scale │  │  • Semantic color meaning              │  │
│  └────────────────────────┘  └────────────────────────────────────────┘  │
│  ┌────────────────────────┐  ┌────────────────────────────────────────┐  │
│  │  Chart Formatting      │  │  Smart Layout Engine                   │  │
│  │  • Data-anchored CAGR  │  │  • Auto legend redundancy removal      │  │
│  │  • Callouts & leaders  │  │  • Responsive positioning              │  │
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

- **Content Analysis & Structuring**: Automatically analyze topics and generate appropriate slide structures
- **Professional Templates**: Multiple slide types including title, content, bullet points, two-column, quotes, and more
- **Design Optimization**: 8+ professional color schemes with automatic contrast optimization
- **Full Customization**: Complete control over every aspect of your presentation
- **Speaker Notes**: Add presenter notes to any slide
- **Metadata Support**: Include author, company, and other metadata

### Slide Types

- **Title Slide**: Full-screen title and subtitle with branded background
- **Title & Content**: Standard content slide with title and body text
- **Section Header**: Visual break between presentation sections
- **Bullet Points**: Lists with proper hierarchy and spacing
- **Two Column**: Side-by-side content comparison
- **Quote**: Highlighted quotations with attribution
- **Thank You**: Closing slide with call-to-action
- **Blank**: Custom layouts

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

### 1. SlideGeneratorSkill

Handles the actual PowerPoint file creation with proper formatting, layouts, and styling.

### 2. ContentAnalyzerSkill

- Analyzes topics and generates appropriate slide structures
- Structures raw content into logical slides
- Splits long content across multiple slides
- Extracts bullet points from text

### 3. DesignOptimizerSkill

- Applies professional color schemes
- Ensures WCAG AA contrast compliance
- Suggests appropriate schemes based on topic
- Optimizes visual hierarchy

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
    notes: Optional[str] = None  # Speaker notes
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
│   ├── agent.py              # Main agent class
│   ├── models.py             # Data models
│   └── skills/
│       ├── __init__.py
│       ├── slide_generator.py    # PowerPoint generation
│       ├── content_analyzer.py   # Content structuring
│       └── design_optimizer.py   # Design and colors
├── examples/
│   ├── basic_example.py
│   ├── advanced_example.py
│   ├── custom_slides_example.py
│   └── color_schemes_demo.py
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
- Charts and graphs not yet supported (planned)
- Animation and transitions not supported
- Video embedding not supported
- Master slide editing limited to code-defined templates

## Future Enhancements

- Integration with Claude API for AI-powered content generation
- Chart and graph support (matplotlib integration)
- Image generation and embedding
- Template marketplace
- PowerPoint theme import/export
- Presentation analytics and recommendations

## Contributing

Contributions welcome! Areas for improvement:

- Additional slide layouts
- More color schemes
- Enhanced content analysis
- Better error handling
- Unit tests
- Documentation improvements

## Troubleshooting

**"ANTHROPIC_API_KEY not set" or "AuthenticationError"**
- Make sure you've exported the environment variable
- Restart your terminal after setting it
- Verify your key at https://console.anthropic.com

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

**Presentation not generating / API errors**
- Check your API key has credits at console.anthropic.com
- Ensure you have internet connectivity
- Try a simpler example first (`examples/basic_example.py`)

---

## License

MIT License - See LICENSE file for details

---

Built with Claude Code | Powered by Claude API (claude-3-5-sonnet)
