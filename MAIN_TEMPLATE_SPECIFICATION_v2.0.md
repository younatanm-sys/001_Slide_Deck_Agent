# Main Template Specification v2.0
## Professional Slide Deck Design System - Complete Technical Reference

---

## TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [Canvas & Grid System](#2-canvas--grid-system)
3. [Zone Architecture](#3-zone-architecture)
4. [Typography Engine](#4-typography-engine)
5. [Color Palette](#5-color-palette)
6. [Story-Driven Color Engine](#6-story-driven-color-engine)
7. [Layout Distribution Rules](#7-layout-distribution-rules)
8. [Chart Specifications](#8-chart-specifications)
9. [Annotation Skills](#9-annotation-skills)
10. [Text Components](#10-text-components)
11. [Slide Blueprints](#11-slide-blueprints)
12. [Critical Rendering Rules](#12-critical-rendering-rules)
13. [Design Principles](#13-design-principles)

---

## 1. EXECUTIVE SUMMARY

The Main Template is a professional slide deck design system implementing consulting-grade standards for automated PowerPoint generation. It enforces strict visual consistency through:

- **Fixed 16:9 aspect ratio** (1920×1080px at 144 DPI reference)
- **Immutable zone architecture** (Title/Content/Footer)
- **Hierarchical typography** (T1-T5 scale)
- **Story-driven color logic** (highlight vs. neutral)
- **Dynamic layout engine** (content-aware composition)
- **Professional chart styling** (borderless, no 3D effects)
- **Intelligent annotation system** (CAGR arrows, difference lines, callouts)

---

## 2. CANVAS & GRID SYSTEM

### 2.1 Canvas Dimensions

| Property | Pixels | Inches | Notes |
|----------|--------|--------|-------|
| Width | 1920 | 13.33" | Standard 16:9 |
| Height | 1080 | 7.5" | Standard 16:9 |
| DPI Reference | 144 | - | Design reference |
| Background | - | - | #FFFFFF (White) |

### 2.2 Safe Zone

The Safe Zone defines the boundary within which all content must remain. It provides 5% margins on all sides.

| Property | Pixels | Inches |
|----------|--------|--------|
| Horizontal Margin | 96px | 0.667" |
| Vertical Margin | 54px | 0.375" |
| Top-Left Corner | (96, 54) | (0.667", 0.375") |
| Bottom-Right Corner | (1824, 1026) | (12.667", 7.125") |
| Usable Width | 1728px | 12.0" |
| Usable Height | 972px | 6.75" |

### 2.3 Coordinate Conversion

```
inches = pixels / 144
pixels = inches × 144
```

All specifications use 144 DPI as the reference. When rendered in PowerPoint (typically 96 DPI), elements scale proportionally.

---

## 3. ZONE ARCHITECTURE

The slide is divided into three immutable vertical zones. **No element may cross zone boundaries.**

### 3.1 Title Zone

| Property | Value (px) | Value (inches) |
|----------|------------|----------------|
| X1 (Left) | 96 | 0.667" |
| Y1 (Top) | 54 | 0.375" |
| X2 (Right) | 1824 | 12.667" |
| Y2 (Bottom) | 134 | 0.931" |
| Height | 80 | 0.556" |
| Purpose | Slide title only (T1) |

### 3.2 Content Zone

| Property | Value (px) | Value (inches) |
|----------|------------|----------------|
| X1 (Left) | 96 | 0.667" |
| Y1 (Top) | 154 | 1.069" |
| X2 (Right) | 1824 | 12.667" |
| Y2 (Bottom) | 956 | 6.639" |
| Height | 802 | 5.569" |
| Gutter from Title | 20 | 0.139" |
| Purpose | Charts, text, visuals |

### 3.3 Footer Zone

| Property | Value (px) | Value (inches) |
|----------|------------|----------------|
| X1 (Left) | 96 | 0.667" |
| Y1 (Top) | 972 | 6.75" |
| X2 (Right) | 1824 | 12.667" |
| Y2 (Bottom) | 1026 | 7.125" |
| Height | 54 | 0.375" |
| Gutter from Content | 16 | 0.111" |
| Purpose | Source attribution, slide numbers |

### 3.4 Gutters

| Gutter | Pixels | Inches | Purpose |
|--------|--------|--------|---------|
| Title → Content | 20 | 0.139" | Zone separation |
| Content → Footer | 16 | 0.111" | Zone separation |
| Horizontal Components | 60 | 0.417" | Between side-by-side elements |
| Vertical Components | 30 | 0.208" | Between stacked elements |

---

## 4. TYPOGRAPHY ENGINE

### 4.1 Typography Hierarchy

| Level | Name | Size | Weight | Color | Use Case |
|-------|------|------|--------|-------|----------|
| **T1** | Slide Title | 32pt | Bold | #147B58 (Primary Green) | Main slide title |
| **T2** | Subtitle/Chart Title | 20pt | Bold | #4A4A4A (Body Text) | Chart titles, subtitles |
| **T3** | Body Text/Bullets | 18pt | Regular | #4A4A4A (Body Text) | Bullet points, paragraphs |
| **T4** | Chart Labels | 12pt | Regular | #4A4A4A (Body Text) | Data labels, category labels |
| **T4.5** | Axis/Legend | 9pt | Regular | #A9A9A9 (Axis Grey) | Axis labels, legends |
| **T5** | Footnotes/Source | 9pt | Regular | #A9A9A9 (Axis Grey) | Source attributions |

### 4.2 Primary Font

- **Font Family**: Arial
- **Fallbacks**: Helvetica, Sans-serif

### 4.3 Overflow Logic

| Level | Overflow Handling |
|-------|-------------------|
| T1 | Reduce by 2pt until fits (min 24pt) |
| T2 | Wrap, then reduce by 1pt |
| T3 | Wrap within container |
| T4 | Dynamic position or reduce to 10pt |
| T5 | Truncate with ellipsis |

### 4.4 Special Typography (Title Slide)

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Main Title | 60pt | Bold | #FFFFFF (White) |
| Subtitle | 24pt | Regular | #FFFFFF (White) |
| Spacing (Title→Subtitle) | 40px | - | - |

### 4.5 Special Typography (Section Divider)

| Element | Size | Weight | Color | Position |
|---------|------|--------|-------|----------|
| Section Title | 44pt | Bold | #FFFFFF | (96px, 486px) |

---

## 5. COLOR PALETTE

### 5.1 Primary Brand Colors

| Name | Hex | RGB | Use Case |
|------|-----|-----|----------|
| **Primary Green** | #147B58 | (20, 123, 88) | Titles, highlights, positive values |
| **Accent Blue** | #005EB8 | (0, 94, 184) | Secondary accent (NOT for waterfall charts) |
| **Accent Yellow** | #F3C13A | (243, 193, 58) | Warning, attention |
| **Negative Red** | #E65166 | (230, 81, 102) | Negative values, decreases |

### 5.2 Neutral Colors

| Name | Hex | RGB | Use Case |
|------|-----|-----|----------|
| **Primary Body Text** | #4A4A4A | (74, 74, 74) | Body text, labels |
| **Axis Grey** | #A9A9A9 | (169, 169, 169) | Axis labels, footnotes |
| **Light Grey** | #D3D3D3 | (211, 211, 211) | Default bar color |
| **Gridline Light** | #E0E0E0 | (224, 224, 224) | Chart gridlines |
| **White** | #FFFFFF | (255, 255, 255) | Backgrounds |
| **Light Gray BG** | #F5F5F5 | (245, 245, 245) | Callout backgrounds |

### 5.3 Sequential Palette (Multi-Series)

| Shade | Hex | RGB | Order |
|-------|-----|-----|-------|
| **Shade 1** | #025645 | (2, 86, 69) | Darkest |
| **Shade 2** | #517B70 | (81, 123, 112) | Medium-dark |
| **Shade 3** | #51A3A3 | (81, 163, 163) | Medium-light |
| **Shade 4** | #A2DAD9 | (162, 218, 217) | Lightest |

---

## 6. STORY-DRIVEN COLOR ENGINE

### 6.1 Universal Principle

> **"Color is not for decoration; it is for communication."**

### 6.2 Unbreakable Rules

1. **The Default State is Grey**: All elements default to Light Grey (#D3D3D3)
2. **The Story is in Color**: Use single Highlight Color (Primary Green #147B58) for the most important data
3. **Comparisons Use Sequential Colors**: For equally important comparisons, use Sequential Palette
4. **Never Use Random Colors**: Only use colors from the defined palette

### 6.3 Column Chart Color Modes

| Mode | Description | Colors Used |
|------|-------------|-------------|
| **Highlight Mode** | One bar highlighted, rest neutral | Primary Green (#147B58) + Light Grey (#D3D3D3) |
| **Comparison Mode** | Multiple series compared | Sequential Palette (4 shades) |
| **Single Series** | All bars same series | Primary Green only |

### 6.4 Waterfall Chart Color Rules (UNBREAKABLE)

| Column Type | Color | Hex | RGB |
|-------------|-------|-----|-----|
| **Start** | Primary Green | #147B58 | (20, 123, 88) |
| **End** | Primary Green | #147B58 | (20, 123, 88) |
| **Increase 1** | Sequential Darkest | #025645 | (2, 86, 69) |
| **Increase 2** | Sequential Medium-dark | #517B70 | (81, 123, 112) |
| **Increase 3** | Sequential Medium-light | #51A3A3 | (81, 163, 163) |
| **Increase 4+** | Sequential Lightest | #A2DAD9 | (162, 218, 217) |
| **Decrease** | Negative Red | #E65166 | (230, 81, 102) |

> **Note**: Accent Blue (#005EB8) is **FORBIDDEN** in waterfall charts.

> **Palette Cycling Rule**: If the number of 'Increase' columns exceeds 4, the coloring logic cycles back to Shade 1. For example: 5th increase uses Shade 1 (#025645), 6th uses Shade 2 (#517B70), and so on. This is implemented via modulo operation: `palette[increase_index % 4]`.

---

## 7. LAYOUT DISTRIBUTION RULES

### 7.1 Single Component Layout

- **Rule**: Center in content area
- **Max Scale**: 80% of content area
- **Max Width**: 1382px (9.597")
- **Max Height**: 642px (4.458")
- **Aspect Ratio**: Maintained

### 7.2 Two Components Side-by-Side (50/50 Split)

| Region | X1 (px) | Y1 (px) | X2 (px) | Y2 (px) | Width (px) |
|--------|---------|---------|---------|---------|------------|
| Left Column | 96 | 154 | 906 | 956 | 810 |
| Right Column | 966 | 154 | 1824 | 956 | 858 |
| **Gutter** | - | - | - | - | **60px** |

### 7.3 Chart + Insight Layout (50/50 Split)

| Region | X1 (px) | Y1 (px) | X2 (px) | Y2 (px) | Width (px) | Height (px) |
|--------|---------|---------|---------|---------|------------|-------------|
| Chart Area | 96 | 154 | 834 | 956 | 738 | 802 |
| Text Area | 894 | 154 | 1824 | 956 | 930 | 802 |
| **Gutter** | - | - | - | - | **60px** | - |

> **Vertical Alignment Rule (MANDATORY)**: The Text Area must be vertically centered relative to the geometric center of the Chart Area. This is achieved by setting `vertical_anchor='MIDDLE'` on the text box and calculating alignment based on the chart's vertical center position.

### 7.4 Two Components Top-Bottom

| Region | X1 (px) | Y1 (px) | X2 (px) | Y2 (px) | Height (px) |
|--------|---------|---------|---------|---------|-------------|
| Top Row | 96 | 154 | 1824 | 540 | 386 |
| Bottom Row | 96 | 570 | 1824 | 956 | 386 |
| **Gutter** | - | - | - | - | **30px** |

---

## 8. CHART SPECIFICATIONS

### 8.1 Column Chart

#### Axes

| Element | Style | Thickness | Color |
|---------|-------|-----------|-------|
| X-Axis Line | Solid | 1.5pt | #A9A9A9 |
| Y-Axis Line | None | - | - |
| Horizontal Gridlines | Solid | 1pt | #E0E0E0 |
| Vertical Gridlines | None | - | - |

#### Bars

| Property | Value |
|----------|-------|
| Default Color | #D3D3D3 (Light Grey) |
| Highlight Color | #147B58 (Primary Green) |
| Gap Width | 50% of bar width |
| Border | None |
| 3D Effects | None (FORBIDDEN) |

#### Labels

| Label Type | Position | Typography |
|------------|----------|------------|
| Data Labels | Outside End | T4 (12pt) |
| Category Labels | X-Axis | T4 (12pt) |

### 8.2 Waterfall Chart

#### Columns

| Type | Fill Color | Border | Grounded |
|------|------------|--------|----------|
| Start/End | #147B58 | Same as fill | Yes (touches X-axis) |
| Increase | Sequential Palette | None | No (floats) |
| Decrease | #E65166 | Same as fill | No (floats) |

#### Connector Lines

| Property | Value |
|----------|-------|
| Style | Dashed |
| Thickness | 1pt |
| Color | #A9A9A9 |

### 8.3 Matrix Chart (BCG Matrix)

#### Plot Area

| Property | Value |
|----------|-------|
| Shape | Square |
| Border Thickness | 1.5pt |
| Border Color | #A9A9A9 |

#### Quadrants

| Quadrant | Position | Label |
|----------|----------|-------|
| Top-Left | High Growth, High Share | Stars |
| Top-Right | High Growth, Low Share | Question Marks |
| Bottom-Left | Low Growth, High Share | Cash Cows |
| Bottom-Right | Low Growth, Low Share | Dogs |

#### Axes

| Axis | Direction | Label |
|------|-----------|-------|
| X-Axis | **Reversed** (High → Low) | Relative Market Share |
| Y-Axis | Standard (Low → High) | Market Growth |

#### Bubbles

| Property | Value |
|----------|-------|
| Min Size | 20px (0.139") |
| Max Size | 150px (1.042") |
| Colors | Sequential Palette |
| Border | 1pt, #4A4A4A |

---

## 9. ANNOTATION SKILLS

### 9.1 CAGR Arrow (Compound Annual Growth Rate)

**Purpose**: Show growth rate between two time periods with a curved arrow above the bars.

#### Visual Specifications

| Property | Value |
|----------|-------|
| Line Type | Quadratic Bézier curve |
| Line Color | #A9A9A9 (Axis Grey) |
| Line Thickness | 1pt |
| Fill | None |

#### Curve Logic

1. **Start Point**: Top-center of first bar (from_category)
2. **End Point**: Top-center of last bar (to_category)
3. **Control Point**: Calculated to clear highest obstacle between endpoints
4. **Clearance**: 30px (0.208") above highest bar
5. **Segments**: 20 line segments approximating curve

#### Label Specifications

| Property | Value |
|----------|-------|
| Position | Above curve apex, horizontally centered |
| Width | 0.9" |
| Height | 0.25" |
| Offset Above Apex | 0.08" |
| Font Size | 10pt |
| Font Weight | Regular |
| Font Color | #4A4A4A |
| Alignment | Center |

#### Input Parameters

```json
{
  "type": "cagr_arrow",
  "series_index": 0,
  "from_category": 0,
  "to_category": 4,
  "label": "45% CAGR"
}
```

### 9.2 Difference Line

**Purpose**: Show the difference between two adjacent bars with a vertical line and label.

#### Visual Design AI Rules (UNBREAKABLE)

1. **Calculate the Gutter**: `line.position_x = midpoint between bar1.right_edge_x and bar2.left_edge_x`
2. **Set Line Height**: `line.start_y = bar1.top_edge_y`, `line.end_y = bar2.top_edge_y`
3. **Position Label**: Default to RIGHT of line with 15px padding, vertically centered
4. **Collision Avoidance**: If label overlaps bar2, move to LEFT side

#### Line Specifications

| Property | Value |
|----------|-------|
| Type | Vertical, Dashed |
| Color | #E65166 (Negative Red) |
| Thickness | 1.5pt |
| Start Y | Top of bar1 (EXACTLY) |
| End Y | Top of bar2 (EXACTLY) |

#### Label Specifications (Composed Block)

| Property | Primary Line | Secondary Line |
|----------|--------------|----------------|
| Font Size | 11pt | 10pt |
| Font Weight | Bold | Regular |
| Font Color | #E65166 | #E65166 |
| Alignment | Center | Center |
| Example | "€28 savings" | "(62% reduction)" |

#### Input Parameters

```json
{
  "type": "difference_line",
  "series_index": 0,
  "from_category": 0,
  "to_category": 1,
  "label": "€28 savings\n(62% reduction)"
}
```

### 9.3 Leader Line

**Purpose**: Point from a data point to a label in clean white space.

#### Specifications

| Property | Value |
|----------|-------|
| Line Color | #A9A9A9 (Axis Grey) |
| Line Thickness | 0.75pt |
| Directions | up, down, left, right |
| Default Length | 40px (0.278") |

#### Label Specifications

| Property | Value |
|----------|-------|
| Font Size | 10pt |
| Font Weight | Regular |
| Font Color | #4A4A4A |

#### Input Parameters

```json
{
  "type": "leader_line",
  "x": 0.82,
  "y": 0.92,
  "text": "€1,280 LTV\n3.2x multiplier",
  "direction": "right",
  "line_length": 50
}
```

### 9.4 Callout

**Purpose**: Highlight specific points on a chart with text annotation.

#### Input Parameters

```json
{
  "type": "callout",
  "x": 0.25,
  "y": 0.15,
  "text": "Quick wins:\nMobile app",
  "position": "above"
}
```

---

## 10. TEXT COMPONENTS

### 10.1 Bulleted List

#### Bullet Style

| Property | Value |
|----------|-------|
| Shape | Solid circle |
| Color | #147B58 (Primary Green) |

#### Indentation

| Level | Indent (px) | Indent (inches) |
|-------|-------------|-----------------|
| Level 1 | 0 | 0" |
| Level 2 | 30 | 0.208" |
| Level 3 | 60 | 0.417" |

#### Text Style

| Property | Value |
|----------|-------|
| Typography | T3 (18pt Regular) |
| Line Spacing | 1.5× |
| Hanging Indent | Yes |

#### Dynamic Spacing Rule (Sparse Content)

| Condition | Behavior |
|-----------|----------|
| ≤3 bullets in single-column layout | Increase `space_after` to vertically center content block at 50-60% of Content Zone height |
| >3 bullets | Standard 12pt spacing |

**Calculation Formula**:
```
space_after_pt = (target_height - text_height) / (num_bullets - 1)
```

Where:
- `target_height` = Content Zone height × 0.55 (55% fill target)
- `text_height` = num_bullets × 24pt (approximate line height)
- Minimum: 24pt | Maximum: 48pt

### 10.2 Callout Box

#### Container

| Property | Value |
|----------|-------|
| Background | #F5F5F5 |
| Border Thickness | 2pt |
| Border Color | #147B58 (Primary Green) |
| Padding | 20px (0.139") |
| Max Width | 90% of content area |

#### Header

| Property | Value |
|----------|-------|
| Typography | T2 (20pt Bold) |
| Spacing to Body | 10px (0.069") |

#### Body

| Property | Value |
|----------|-------|
| Typography | T3 (18pt Regular) |
| Line Spacing | 1.5× |

---

## 11. SLIDE BLUEPRINTS

### 11.1 Title Slide

| Property | Value |
|----------|-------|
| Layout | Full bleed |
| Background | #147B58 (Primary Green) |

| Element | Typography | Position |
|---------|------------|----------|
| Main Title | 60pt Bold White | Center both |
| Subtitle | 24pt Regular White | Below title, 40px spacing |

### 11.2 Section Divider

| Property | Value |
|----------|-------|
| Layout | Full bleed |
| Background | #147B58 (Primary Green) |

| Element | Typography | Position |
|---------|------------|----------|
| Section Title | 44pt Bold White | (96px, 486px), left-aligned |
| Bounds | 1728px × 108px | - |

### 11.3 Content: Chart + Insight

| Property | Value |
|----------|-------|
| Layout | chart_plus_insight_50_50 |
| Chart Region | Left 50% |
| Text Region | Right 50% |
| Gutter | 60px |

### 11.4 Content: Single Chart

| Property | Value |
|----------|-------|
| Layout | single_component |
| Scale | 80% max of content area |

### 11.5 Content: Bullets Only

| Property | Value |
|----------|-------|
| Layout | text_only |
| Two-Column Trigger | >5 bullets OR >800 characters |

#### Two-Column Layout (when triggered)

| Column | X1 (px) | Width (px) |
|--------|---------|------------|
| Left | 96 | 834 |
| Right | 990 | 834 |
| Gutter | - | 60 |

---

## 12. CRITICAL RENDERING RULES

### 12.1 Boundary Enforcement

> **ABSOLUTE RULE**: No element may extend beyond the Safe Zone boundaries.

| Boundary | Position |
|----------|----------|
| Left | 96px (0.667") |
| Top | 54px (0.375") |
| Right | 1824px (12.667") |
| Bottom | 1026px (7.125") |

**Exception**: Full-bleed backgrounds only (title slide, section divider).

### 12.2 Overflow Handling

| Content Type | Handling |
|--------------|----------|
| Text Overflow | Follow typography-specific logic |
| Component Overflow | Scale down by 5% increments |

### 12.3 Spacing Consistency

| Spacing Type | Minimum (px) | Minimum (inches) |
|--------------|--------------|------------------|
| Horizontal Gutter | 60 | 0.417" |
| Vertical Gutter | 30 | 0.208" |
| Component Padding | 20 | 0.139" |
| Bullet Indentation | 30 | 0.208" |

### 12.4 Chart Quality Standards

| Rule | Requirement |
|------|-------------|
| 3D Effects | **FORBIDDEN** |
| Chart Borders | **NONE** |
| Bar Spacing | 50% gap width |
| Label Positioning | Outside end, prevent overlap |

### 12.5 Font Handling

| Property | Value |
|----------|-------|
| Primary Font | Arial |
| Fallback Fonts | Helvetica, Sans-serif |
| Substitution | Alert if font unavailable |

---

## 13. DESIGN PRINCIPLES

### PRINCIPLE 1: Zoned Integrity

> Slide is divided into Title, Content, and Footer zones. These zones are immutable—elements cannot violate their boundaries or overlap into adjacent zones.

### PRINCIPLE 2: Content-Driven Layouts

> Layout is determined by content type:
> - **Split-Screen (50/50)**: Chart + explanatory text
> - **Full-Width**: Single large chart or visualization
> - **Text-Only**: Bullet points with optional two-column

### PRINCIPLE 3: Atomic Text Elements

> Each bullet point is a separate paragraph with complete formatting (bullet character, hanging indent, line spacing) to ensure scannability.

### PRINCIPLE 4: Hierarchical Titling

> - **T1 (Slide Title)**: Communicates the "so what" / key insight
> - **T2 (Chart Title)**: Describes "what it is" / data being shown

### PRINCIPLE 5: Consistent Visual Anchoring

> - Titles: Vertically centered in Title zone
> - Content: Top-aligned within Content zone
> - Chart + Text: Cross-aligned to chart's vertical center

### PRINCIPLE 6: Insight Over Information

> The LLM acts as a "Data Storyteller," transforming raw numbers into meaningful insights. Chart annotation labels are generated dynamically by the LLM-Powered Label Engine rather than being hardcoded or pre-formatted.
>
> **Key Concepts:**
> - Python code sends structured data (values, currency, direction)
> - LLM returns polished, human-readable labels
> - Labels communicate the story, not just the numbers

---

## 14. LLM-POWERED LABEL ENGINE

### 14.1 Overview

The Label Engine is a new architectural component that generates annotation labels using LLM intelligence. It implements PRINCIPLE 6 by converting raw data into insight-driven text.

### 14.2 Request/Response Models

#### Difference Line Label

**Request:**
```json
{
  "task": "generate_difference_label",
  "start_value": 45,
  "end_value": 17,
  "currency": "€",
  "direction": "reduction"
}
```

**Response:**
```json
{
  "primary": "€28 savings",
  "secondary": "(62% reduction)"
}
```

#### CAGR Arrow Label

**Request:**
```json
{
  "task": "generate_cagr_label",
  "data_series": [22, 35, 42, 55, 65],
  "cagr_value": 0.31
}
```

**Response:**
```json
{
  "label": "4-Year CAGR: +31%"
}
```

### 14.3 Integration Pattern

```python
# Instead of:
annotation = {
    "type": "difference_line",
    "label": "€28 savings\n(62% reduction)"  # Pre-formatted
}

# Use:
annotation = {
    "type": "difference_line",
    "label_generation_request": {
        "task": "generate_difference_label",
        "start_value": 45,
        "end_value": 17,
        "currency": "€",
        "direction": "reduction"
    }
}
```

### 14.4 Fallback Behavior

If the LLM API call fails, the Label Engine falls back to local calculation using the same rules:
- Difference: Calculate absolute and percentage change, format with action words
- CAGR: Calculate years from series length, format with sign prefix

---

## APPENDIX A: Quick Reference Card

### Colors at a Glance

```
Primary Green:  #147B58  rgb(20, 123, 88)   - Titles, highlights, positive
Accent Blue:    #005EB8  rgb(0, 94, 184)    - Secondary accent
Accent Yellow:  #F3C13A  rgb(243, 193, 58)  - Attention/warning
Negative Red:   #E65166  rgb(230, 81, 102)  - Negative values
Body Text:      #4A4A4A  rgb(74, 74, 74)    - Primary text
Axis Grey:      #A9A9A9  rgb(169, 169, 169) - Axes, footnotes
Light Grey:     #D3D3D3  rgb(211, 211, 211) - Default bars
Gridline:       #E0E0E0  rgb(224, 224, 224) - Chart gridlines
```

### Typography at a Glance

```
T1:   32pt Bold    #147B58  - Slide title
T2:   20pt Bold    #4A4A4A  - Chart title
T3:   18pt Regular #4A4A4A  - Body/bullets
T4:   12pt Regular #4A4A4A  - Chart labels
T4.5:  9pt Regular #A9A9A9  - Axes/legend
T5:    9pt Regular #A9A9A9  - Footnotes
```

### Safe Zone Bounds

```
Top-Left:     (96, 54)px     = (0.667", 0.375")
Bottom-Right: (1824, 1026)px = (12.667", 7.125")
Usable Area:  1728 × 972px   = 12.0" × 6.75"
```

### Gutter Standards

```
Horizontal components: 60px = 0.417"
Vertical components:   30px = 0.208"
Title to content:      20px = 0.139"
Content to footer:     16px = 0.111"
```

---

## APPENDIX B: File References

| File | Purpose |
|------|---------|
| `templates/main_template_config.py` | All configuration constants |
| `skills/main_slide_generator.py` | Rendering logic implementation |
| `llapi/annotation_placer.py` | Visual Design AI for annotations |
| `llapi/label_engine.py` | LLM-Powered Label Engine (PRINCIPLE 6) |
| `models.py` | Data models (SlideContent, PresentationRequest, Label requests/responses) |

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 2.1 | 2026-01-22 | LLM-Powered Label Engine (PRINCIPLE 6), dynamic annotation text generation |
| 2.0 | 2026-01-22 | Sequential palette for waterfall, Visual Design AI for difference lines |
| 1.5 | - | Story-Driven Color Engine, CAGR arrow improvements |
| 1.0 | - | Initial specification |

---

*End of Specification*
