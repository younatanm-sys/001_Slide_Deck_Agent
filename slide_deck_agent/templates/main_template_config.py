"""
Main PowerPoint Template Configuration v2.0
Professional Slide Deck Design System

This configuration implements a complete professional design system including:
- Safe Zone boundaries and grid system
- Typography engine with overflow rules
- Component generation logic
- Slide-specific blueprints

Usage:
    from main_template_config import MAIN_CONFIG

    # Access grid system
    safe_zone = MAIN_CONFIG['grid']['safe_zone']

    # Access layout regions
    title_region = MAIN_CONFIG['grid']['regions']['title']
"""

from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# ============================================================================
# 1.0 GLOBAL CANVAS & GRID SYSTEM
# ============================================================================

# Reference resolution: 1920×1080 at 144 DPI
DPI = 144

def px_to_inches(px):
    """Convert pixels to inches at 144 DPI"""
    return Inches(px / DPI)

CANVAS = {
    'width_px': 1920,
    'height_px': 1080,
    'width': px_to_inches(1920),
    'height': px_to_inches(1080),
    'aspect_ratio': '16:9',
    'background_color': '#FFFFFF',
    'background_color_rgb': (255, 255, 255)
}

# Safe Zone: 5% margins (96px left/right, 54px top/bottom)
SAFE_ZONE = {
    'margin_horizontal_px': 96,
    'margin_vertical_px': 54,
    'margin_horizontal': px_to_inches(96),
    'margin_vertical': px_to_inches(54),

    # Boundaries
    'top_left': {
        'x_px': 96,
        'y_px': 54,
        'x': px_to_inches(96),
        'y': px_to_inches(54)
    },
    'bottom_right': {
        'x_px': 1824,  # 1920 - 96
        'y_px': 1026,  # 1080 - 54
        'x': px_to_inches(1824),
        'y': px_to_inches(1026)
    },

    # Dimensions
    'width_px': 1728,  # 1920 - (96*2)
    'height_px': 972,  # 1080 - (54*2)
    'width': px_to_inches(1728),
    'height': px_to_inches(972)
}

# Vertical Layout Regions
REGIONS = {
    'title': {
        'name': 'Title Area',
        'bounds': {
            'x1_px': 96,
            'y1_px': 54,
            'x2_px': 1824,
            'y2_px': 134,
            'x1': px_to_inches(96),
            'y1': px_to_inches(54),
            'x2': px_to_inches(1824),
            'y2': px_to_inches(134)
        },
        'height_px': 80,
        'height': px_to_inches(80),
        'purpose': 'Exclusively for the main slide title'
    },
    'content': {
        'name': 'Content Area',
        'bounds': {
            'x1_px': 96,
            'y1_px': 154,  # 134 + 20px gutter
            'x2_px': 1824,
            'y2_px': 956,
            'x1': px_to_inches(96),
            'y1': px_to_inches(154),
            'x2': px_to_inches(1824),
            'y2': px_to_inches(956)
        },
        'height_px': 802,
        'height': px_to_inches(802),
        'gutter_from_title_px': 20,
        'gutter_from_title': px_to_inches(20),
        'purpose': 'Main area for charts, text blocks, and visual elements'
    },
    'footer': {
        'name': 'Footer Area',
        'bounds': {
            'x1_px': 96,
            'y1_px': 972,  # 956 + 16px gutter
            'x2_px': 1824,
            'y2_px': 1026,
            'x1': px_to_inches(96),
            'y1': px_to_inches(972),
            'x2': px_to_inches(1824),
            'y2': px_to_inches(1026)
        },
        'height_px': 54,
        'height': px_to_inches(54),
        'gutter_from_content_px': 16,
        'gutter_from_content': px_to_inches(16),
        'purpose': 'Source attribution and slide numbers'
    }
}

GRID_SYSTEM = {
    'canvas': CANVAS,
    'safe_zone': SAFE_ZONE,
    'regions': REGIONS,
    'gutters': {
        'title_to_content_px': 20,
        'content_to_footer_px': 16,
        'horizontal_components_px': 60,  # 60px at 144 DPI = 40px at 96 DPI render
        'vertical_components_px': 30,
        'title_to_content': px_to_inches(20),
        'content_to_footer': px_to_inches(16),
        'horizontal_components': px_to_inches(60),  # 60px at 144 DPI = 40px at 96 DPI render
        'vertical_components': px_to_inches(30)
    }
}

# ============================================================================
# 2.0 TYPOGRAPHY ENGINE
# ============================================================================

FONTS = {
    'primary': 'Arial',
    'fallback': ['Helvetica', 'Sans-serif']
}

# Typographic Scale
TYPOGRAPHY = {
    'T1': {
        'name': 'Slide Title',
        'font_size_pt': 32,  # Commanding presence
        'font_size': Pt(32),
        'weight': 'bold',
        'color': '#147B58',  # Primary Green
        'color_rgb': (20, 123, 88),
        'bounding_box': 'title_area',
        'overflow_logic': 'reduce_by_2pt_min_20pt',
        'min_font_size_pt': 24,
        'min_font_size': Pt(24)
    },
    'T2': {
        'name': 'Subtitle / Chart Title',
        'font_size_pt': 20,  # Better legibility
        'font_size': Pt(20),
        'weight': 'bold',
        'color': '#4A4A4A',  # Body Text
        'color_rgb': (74, 74, 74),
        'bounding_box': 'content_block',
        'overflow_logic': 'wrap_then_reduce_by_1pt'
    },
    'T3': {
        'name': 'Body Text / Bullets',
        'font_size_pt': 18,  # Client presentation standards
        'font_size': Pt(18),
        'weight': 'regular',
        'color': '#4A4A4A',  # Body Text
        'color_rgb': (74, 74, 74),
        'bounding_box': 'content_block',
        'overflow_logic': 'wrap_within_container',
        'line_spacing_multiplier': 1.5
    },
    'T4': {
        'name': 'Chart Labels',
        'font_size_pt': 12,
        'font_size': Pt(12),
        'weight': 'regular',
        'color': '#4A4A4A',  # Body Text
        'color_rgb': (74, 74, 74),
        'overflow_logic': 'dynamic_position_or_reduce_to_10pt',
        'min_font_size_pt': 10,
        'min_font_size': Pt(10)
    },
    'T4.5': {
        'name': 'Chart Axis / Legend',
        'font_size_pt': 9,
        'font_size': Pt(9),
        'weight': 'regular',
        'color': '#A9A9A9',  # Axis Grey
        'color_rgb': (169, 169, 169)
    },
    'T5': {
        'name': 'Footnotes / Source',
        'font_size_pt': 9,
        'font_size': Pt(9),
        'weight': 'regular',
        'color': '#A9A9A9',  # Axis Grey
        'color_rgb': (169, 169, 169),
        'bounding_box': 'footer_area',
        'overflow_logic': 'truncate_with_ellipsis'
    }
}

# Special Typography Cases
TYPOGRAPHY_SPECIAL = {
    'title_slide_main': {
        'font_size_pt': 60,
        'font_size': Pt(60),
        'weight': 'bold',
        'color': '#FFFFFF',
        'color_rgb': (255, 255, 255),
        'alignment': 'center_both'
    },
    'title_slide_subtitle': {
        'font_size_pt': 24,
        'font_size': Pt(24),
        'weight': 'regular',
        'color': '#FFFFFF',
        'color_rgb': (255, 255, 255),
        'spacing_from_title_px': 40,
        'spacing_from_title': px_to_inches(40)
    },
    'section_divider_title': {
        'font_size_pt': 44,
        'font_size': Pt(44),
        'weight': 'bold',
        'color': '#FFFFFF',
        'color_rgb': (255, 255, 255),
        'alignment': 'center_vertical_left_horizontal',
        'position': {
            'x_px': 96,
            'y_px': 486,
            'x': px_to_inches(96),
            'y': px_to_inches(486)
        }
    }
}

# ============================================================================
# 3.0 COLOR PALETTE
# ============================================================================

COLORS = {
    # Primary Brand Colors
    'primary_green': '#147B58',
    'primary_green_rgb': (20, 123, 88),

    'accent_blue': '#005EB8',
    'accent_blue_rgb': (0, 94, 184),

    'accent_yellow': '#F3C13A',
    'accent_yellow_rgb': (243, 193, 58),

    'negative_red': '#E65166',
    'negative_red_rgb': (230, 81, 102),

    # Neutral Colors
    'primary_body_text': '#4A4A4A',
    'primary_body_text_rgb': (74, 74, 74),

    'axis_grey': '#A9A9A9',
    'axis_grey_rgb': (169, 169, 169),

    'light_grey': '#D3D3D3',
    'light_grey_rgb': (211, 211, 211),

    'gridline_light': '#E0E0E0',
    'gridline_light_rgb': (224, 224, 224),

    'white': '#FFFFFF',
    'white_rgb': (255, 255, 255),

    'light_gray_bg': '#F5F5F5',
    'light_gray_bg_rgb': (245, 245, 245),

    # Sequential Palette (for multi-series charts)
    'seq_shade_1': '#025645',  # Darkest
    'seq_shade_1_rgb': (2, 86, 69),

    'seq_shade_2': '#517B70',
    'seq_shade_2_rgb': (81, 123, 112),

    'seq_shade_3': '#51A3A3',
    'seq_shade_3_rgb': (81, 163, 163),

    'seq_shade_4': '#A2DAD9',  # Lightest
    'seq_shade_4_rgb': (162, 218, 217)
}

SEQUENTIAL_PALETTE = [
    COLORS['seq_shade_1'],
    COLORS['seq_shade_2'],
    COLORS['seq_shade_3'],
    COLORS['seq_shade_4']
]

# ============================================================================
# GLOBAL SKILL 1: STORY-DRIVEN COLOR ENGINE
# ============================================================================
"""
Universal Principle: Color is not for decoration; it is for communication.

Unbreakable Rules:
1. The Default State is Grey: All elements default to Light Grey (#D3D3D3)
2. The Story is in Color: Use single Highlight Color (Primary Green #147B58) for the most important data
3. Comparisons Use Sequential Colors: For equally important comparisons, use Sequential Palette (green-based)
4. Never Use Random Colors: Only use colors from the palette
"""

STORY_DRIVEN_COLORS = {
    'default_neutral': COLORS['light_grey'],
    'default_neutral_rgb': COLORS['light_grey_rgb'],

    # UPDATED: Use Primary Green instead of Accent Blue for highlight
    'highlight': COLORS['primary_green'],
    'highlight_rgb': COLORS['primary_green_rgb'],

    'comparison_palette': SEQUENTIAL_PALETTE,
    'comparison_palette_rgb': [
        COLORS['seq_shade_1_rgb'],
        COLORS['seq_shade_2_rgb'],
        COLORS['seq_shade_3_rgb'],
        COLORS['seq_shade_4_rgb']
    ]
}

# ============================================================================
# 4.0 COMPONENT GENERATION LOGIC
# ============================================================================

# Layout Distribution Rules
LAYOUT_DISTRIBUTION = {
    'single_component': {
        'rule': 'center_in_content_area',
        'max_scale': 0.80,  # 80% of content area
        'maintain_aspect_ratio': True,
        'bounds': {
            'max_width_px': int(1728 * 0.80),  # 1382px
            'max_height_px': int(802 * 0.80),   # 642px
            'max_width': px_to_inches(1382),
            'max_height': px_to_inches(642)
        }
    },
    'two_components_side_by_side': {
        'rule': 'vertical_split_with_gutter',
        'gutter_px': 60,  # 60px at 144 DPI = 40px at 96 DPI render
        'gutter': px_to_inches(60),
        'left_column': {
            'x1_px': 96,
            'y1_px': 154,
            'x2_px': 906,
            'y2_px': 956,
            'width_px': 810,
            'x1': px_to_inches(96),
            'y1': px_to_inches(154),
            'x2': px_to_inches(906),
            'y2': px_to_inches(956),
            'width': px_to_inches(810)
        },
        'right_column': {
            'x1_px': 966,  # 906 + 60
            'y1_px': 154,
            'x2_px': 1824,
            'y2_px': 956,
            'width_px': 858,
            'x1': px_to_inches(966),
            'y1': px_to_inches(154),
            'x2': px_to_inches(1824),
            'y2': px_to_inches(956),
            'width': px_to_inches(858)
        },
        'max_component_scale': 0.95
    },
    'two_components_top_bottom': {
        'rule': 'horizontal_split_with_gutter',
        'gutter_px': 30,
        'gutter': px_to_inches(30),
        'top_row': {
            'x1_px': 96,
            'y1_px': 154,
            'x2_px': 1824,
            'y2_px': 540,
            'height_px': 386,
            'x1': px_to_inches(96),
            'y1': px_to_inches(154),
            'x2': px_to_inches(1824),
            'y2': px_to_inches(540),
            'height': px_to_inches(386)
        },
        'bottom_row': {
            'x1_px': 96,
            'y1_px': 570,  # 540 + 30
            'x2_px': 1824,
            'y2_px': 956,
            'height_px': 386,
            'x1': px_to_inches(96),
            'y1': px_to_inches(570),
            'x2': px_to_inches(1824),
            'y2': px_to_inches(956),
            'height': px_to_inches(386)
        }
    },
    'chart_plus_insight_60_40': {
        'rule': 'left_chart_right_text_50_50',  # 50/50 for better balance
        'chart_area': {
            'x1_px': 96,
            'y1_px': 154,
            'x2_px': 834,  # 50/50 split
            'y2_px': 956,
            'width_px': 738,
            'height_px': 802,
            'x1': px_to_inches(96),
            'y1': px_to_inches(154),
            'x2': px_to_inches(834),
            'y2': px_to_inches(956),
            'width': px_to_inches(738),
            'height': px_to_inches(802)
        },
        'text_area': {
            'x1_px': 894,  # 834 + 60px gutter
            'y1_px': 154,
            'x2_px': 1824,
            'y2_px': 956,
            'width_px': 930,
            'height_px': 802,
            'x1': px_to_inches(894),
            'y1': px_to_inches(154),
            'x2': px_to_inches(1824),
            'y2': px_to_inches(956),
            'width': px_to_inches(930),
            'height': px_to_inches(802)
        },
        'gutter_px': 60,
        'gutter': px_to_inches(60)
    }
}

# Column Chart Specifications
CHART_COLUMN = {
    'axes': {
        'x_axis': {
            'line_style': 'solid',
            'line_thickness_pt': 1.5,
            'line_thickness': Pt(1.5),
            'color': '#A9A9A9',
            'color_rgb': (169, 169, 169)
        },
        'y_axis': {
            'line': None  # No Y-axis line
        }
    },
    'gridlines': {
        'horizontal': {
            'line_style': 'solid',
            'line_thickness_pt': 1,
            'line_thickness': Pt(1),
            'color': '#E0E0E0',
            'color_rgb': (224, 224, 224)
        },
        'vertical': None  # No vertical gridlines
    },
    'bars': {
        'default_color': '#D3D3D3',
        'default_color_rgb': (211, 211, 211),
        'highlight_color': '#147B58',  # Primary Green (updated from Accent Blue)
        'highlight_color_rgb': (20, 123, 88),
        'gap_width_percent': 50,  # 50% of bar width
        'border': None,  # No borders
        'effects': None  # No 3D effects
    },
    'labels': {
        'data_labels': {
            'position': 'outside_end',
            'typography': 'T4'
        },
        'category_labels': {
            'position': 'x_axis',
            'typography': 'T4'
        }
    }
}

# Matrix Chart Specifications
CHART_MATRIX = {
    'plot_area': {
        'shape': 'square',
        'border': {
            'line_thickness_pt': 1.5,
            'line_thickness': Pt(1.5),
            'color': '#A9A9A9',
            'color_rgb': (169, 169, 169)
        }
    },
    'quadrants': {
        'dividing_lines': {
            'line_thickness_pt': 1.5,
            'line_thickness': Pt(1.5),
            'color': '#A9A9A9',
            'color_rgb': (169, 169, 169)
        },
        'label_names': {
            'top_left': 'Stars',
            'top_right': 'Question Marks',
            'bottom_left': 'Cash Cows',
            'bottom_right': 'Dogs'
        },
        'label_style': {
            'typography': 'T3',
            'color': '#E0E0E0',
            'color_rgb': (224, 224, 224),
            'opacity': 0.70,
            'position': 'top_right_corner'
        }
    },
    'axes': {
        'x_axis': {
            'name': 'Relative Market Share',
            'direction': 'reverse',  # High to low
            'typography': 'T4'
        },
        'y_axis': {
            'name': 'Market Growth',
            'direction': 'standard',  # Low to high
            'typography': 'T4'
        }
    },
    'bubbles': {
        'size_range': {
            'min_px': 20,
            'max_px': 150,
            'min': px_to_inches(20),
            'max': px_to_inches(150)
        },
        'colors': SEQUENTIAL_PALETTE,
        'border': {
            'line_thickness_pt': 1,
            'line_thickness': Pt(1),
            'color': '#4A4A4A',
            'color_rgb': (74, 74, 74)
        }
    },
    'bubble_labels': {
        'typography': 'T4',
        'color': '#FFFFFF',
        'color_rgb': (255, 255, 255),
        'weight': 'bold',
        'position': 'center',
        'overflow_logic': 'reduce_font_until_fits'
    }
}

# Waterfall Chart Specifications
CHART_WATERFALL = {
    'columns': {
        'start_end': {
            'fill_color': '#147B58',  # Primary Green
            'fill_color_rgb': (20, 123, 88),
            'border': {
                'line_thickness_pt': 1,
                'line_thickness': Pt(1),
                'color': '#147B58',
                'color_rgb': (20, 123, 88)
            },
            'grounded': True  # Touch X-axis
        },
        'increase': {
            'fill_color': '#147B58',  # Primary Green (updated from Accent Blue)
            'fill_color_rgb': (20, 123, 88),
            'border': {
                'line_thickness_pt': 1,
                'line_thickness': Pt(1),
                'color': '#147B58',
                'color_rgb': (20, 123, 88)
            },
            'grounded': False  # Float
        },
        'decrease': {
            'fill_color': '#E65166',  # Negative Red
            'fill_color_rgb': (230, 81, 102),
            'border': {
                'line_thickness_pt': 1,
                'line_thickness': Pt(1),
                'color': '#E65166',
                'color_rgb': (230, 81, 102)
            },
            'grounded': False  # Float
        }
    },
    'connector_lines': {
        'line_style': 'dashed',
        'line_thickness_pt': 1,
        'line_thickness': Pt(1),
        'color': '#A9A9A9',
        'color_rgb': (169, 169, 169)
    },
    'labels': {
        'data_labels': {
            'position': 'outside_end',
            'typography': 'T4'
        },
        'category_labels': {
            'position': 'below_x_axis',
            'typography': 'T4'
        }
    }
}

# Bulleted List Specifications
TEXT_BULLETED_LIST = {
    'bullet_style': {
        'shape': 'solid_circle',
        'color': '#147B58',  # Primary Green
        'color_rgb': (20, 123, 88)
    },
    'indentation': {
        'level_1_px': 0,
        'level_2_px': 30,
        'level_3_px': 60,
        'level_1': px_to_inches(0),
        'level_2': px_to_inches(30),
        'level_3': px_to_inches(60)
    },
    'hanging_indent': True,
    'typography': 'T3',
    'line_spacing_multiplier': 1.5
}

# Callout Box Specifications
CALLOUT_BOX = {
    'container': {
        'background_color': '#F5F5F5',
        'background_color_rgb': (245, 245, 245),
        'border': {
            'line_thickness_pt': 2,
            'line_thickness': Pt(2),
            'color': '#147B58',  # Primary Green
            'color_rgb': (20, 123, 88)
        },
        'padding_px': 20,
        'padding': px_to_inches(20),
        'max_width_percent': 0.90  # 90% of content area
    },
    'header': {
        'typography': 'T2',
        'spacing_to_body_px': 10,
        'spacing_to_body': px_to_inches(10)
    },
    'body': {
        'typography': 'T3',
        'line_spacing_multiplier': 1.5
    }
}

# ============================================================================
# 5.0 SLIDE BLUEPRINTS
# ============================================================================

SLIDE_BLUEPRINTS = {
    'title_slide': {
        'layout': 'full_bleed',
        'background': {
            'type': 'solid',
            'color': '#147B58',  # Primary Green
            'color_rgb': (20, 123, 88)
        },
        'elements': {
            'main_title': {
                'typography': 'title_slide_main',
                'position': 'center_both'
            },
            'subtitle': {
                'typography': 'title_slide_subtitle',
                'position': 'below_title',
                'spacing_px': 40,
                'spacing': px_to_inches(40)
            }
        }
    },
    'section_divider': {
        'layout': 'full_bleed',
        'background': {
            'type': 'solid',
            'color': '#147B58',  # Primary Green
            'color_rgb': (20, 123, 88)
        },
        'elements': {
            'section_title': {
                'typography': 'section_divider_title',
                'position': {
                    'x_px': 96,
                    'y_px': 486,
                    'x': px_to_inches(96),
                    'y': px_to_inches(486)
                },
                'bounds': {
                    'width_px': 1728,
                    'height_px': 108,
                    'width': px_to_inches(1728),
                    'height': px_to_inches(108)
                },
                'alignment': 'left_vertical_center'
            }
        }
    },
    'content_chart_insight': {
        'layout': 'chart_plus_insight_60_40',
        'regions': LAYOUT_DISTRIBUTION['chart_plus_insight_60_40'],
        'title': REGIONS['title'],
        'footer': REGIONS['footer']
    },
    'content_single_chart': {
        'layout': 'single_component',
        'regions': {
            'chart': LAYOUT_DISTRIBUTION['single_component']
        },
        'title': REGIONS['title'],
        'footer': REGIONS['footer']
    },
    'content_bullets': {
        'layout': 'text_only',
        'regions': {
            'text': REGIONS['content']
        },
        'title': REGIONS['title'],
        'footer': REGIONS['footer'],
        'two_column_option': {
            'enabled': True,
            'left_column': {
                'x1_px': 96,
                'y1_px': 154,
                'x2_px': 920,
                'y2_px': 956,
                'width_px': 824,
                'x1': px_to_inches(96),
                'y1': px_to_inches(154),
                'x2': px_to_inches(920),
                'y2': px_to_inches(956),
                'width': px_to_inches(824)
            },
            'right_column': {
                'x1_px': 1000,
                'y1_px': 154,
                'x2_px': 1824,
                'y2_px': 956,
                'width_px': 824,
                'x1': px_to_inches(1000),
                'y1': px_to_inches(154),
                'x2': px_to_inches(1824),
                'y2': px_to_inches(956),
                'width': px_to_inches(824)
            },
            'gutter_px': 120,
            'gutter': px_to_inches(120)
        }
    }
}

# ============================================================================
# 6.0 CRITICAL RENDERING RULES
# ============================================================================

RENDERING_RULES = {
    'boundary_enforcement': {
        'absolute_rule': 'no_element_beyond_safe_zone',
        'safe_zone_bounds': SAFE_ZONE,
        'exception': 'full_bleed_backgrounds_only'
    },
    'overflow_handling': {
        'text_overflow': 'follow_typography_logic',
        'component_overflow': 'scale_down_by_5_percent_increments'
    },
    'spacing_consistency': {
        'horizontal_gutter_min_px': 60,
        'vertical_gutter_min_px': 30,
        'component_padding_min_px': 20,
        'bullet_indentation_px': 30,
        'horizontal_gutter_min': px_to_inches(60),
        'vertical_gutter_min': px_to_inches(30),
        'component_padding_min': px_to_inches(20),
        'bullet_indentation': px_to_inches(30)
    },
    'chart_quality': {
        'no_3d_effects': True,
        'no_chart_borders': True,
        'consistent_bar_spacing': '50_percent_gap',
        'label_positioning': 'outside_end_prevent_overlap'
    },
    'font_handling': {
        'primary_font': 'Arial',
        'fallback_fonts': ['Helvetica', 'Sans-serif'],
        'no_substitution_without_alert': True
    }
}

# ============================================================================
# 7.0 COMPLETE CONFIGURATION OBJECT
# ============================================================================

MAIN_CONFIG = {
    'template_name': 'Main',
    'version': '2.0',
    'grid': GRID_SYSTEM,
    'typography': TYPOGRAPHY,
    'typography_special': TYPOGRAPHY_SPECIAL,
    'colors': COLORS,
    'sequential_palette': SEQUENTIAL_PALETTE,
    'story_driven_colors': STORY_DRIVEN_COLORS,
    'fonts': FONTS,
    'layout_distribution': LAYOUT_DISTRIBUTION,
    'charts': {
        'column': CHART_COLUMN,
        'matrix': CHART_MATRIX,
        'waterfall': CHART_WATERFALL
    },
    'text_components': {
        'bulleted_list': TEXT_BULLETED_LIST,
        'callout_box': CALLOUT_BOX
    },
    'slide_blueprints': SLIDE_BLUEPRINTS,
    'rendering_rules': RENDERING_RULES
}

# ============================================================================
# 8.0 HELPER FUNCTIONS
# ============================================================================

def get_safe_zone_bounds():
    """Get Safe Zone boundary coordinates"""
    return SAFE_ZONE

def get_region(region_name):
    """Get layout region specification by name"""
    return REGIONS.get(region_name)

def get_typography(level):
    """Get typography specification by level"""
    return TYPOGRAPHY.get(level)

def get_chart_spec(chart_type):
    """Get chart specification by type"""
    return MAIN_CONFIG['charts'].get(chart_type)

def get_slide_blueprint(slide_type):
    """Get slide blueprint specification by type"""
    return SLIDE_BLUEPRINTS.get(slide_type)

def validate_bounds(x_px, y_px, width_px=0, height_px=0):
    """
    Validate that element is within Safe Zone bounds.

    Args:
        x_px: X coordinate in pixels
        y_px: Y coordinate in pixels
        width_px: Width in pixels (optional)
        height_px: Height in pixels (optional)

    Returns:
        True if element is fully within Safe Zone, False otherwise
    """
    safe_zone = SAFE_ZONE

    # Check if top-left corner is within bounds
    within_x_start = safe_zone['top_left']['x_px'] <= x_px <= safe_zone['bottom_right']['x_px']
    within_y_start = safe_zone['top_left']['y_px'] <= y_px <= safe_zone['bottom_right']['y_px']

    # Check if bottom-right corner is within bounds (if width/height provided)
    if width_px > 0 and height_px > 0:
        within_x_end = (x_px + width_px) <= safe_zone['bottom_right']['x_px']
        within_y_end = (y_px + height_px) <= safe_zone['bottom_right']['y_px']
        return within_x_start and within_y_start and within_x_end and within_y_end

    return within_x_start and within_y_start

# ============================================================================
# 9.0 USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("Main Template Configuration v2.0")
    print("=" * 80)

    print("\nGrid System:")
    print(f"  Canvas: {CANVAS['width_px']}x{CANVAS['height_px']}px")
    print(f"  Safe Zone: ({SAFE_ZONE['top_left']['x_px']}, {SAFE_ZONE['top_left']['y_px']}) to ({SAFE_ZONE['bottom_right']['x_px']}, {SAFE_ZONE['bottom_right']['y_px']})")
    print(f"  Safe Zone Dimensions: {SAFE_ZONE['width_px']}x{SAFE_ZONE['height_px']}px")

    print("\nLayout Regions:")
    for region_name, region in REGIONS.items():
        print(f"  {region['name']}:")
        print(f"    Height: {region['height_px']}px")
        print(f"    Bounds: ({region['bounds']['x1_px']}, {region['bounds']['y1_px']}) to ({region['bounds']['x2_px']}, {region['bounds']['y2_px']})")

    print("\nTypography Hierarchy:")
    for level, spec in TYPOGRAPHY.items():
        print(f"  {level} ({spec['name']}): {spec['font_size_pt']}pt, {spec['weight']}, {spec['color']}")

    print("\nColor Palette:")
    print(f"  Primary Green: {COLORS['primary_green']}")
    print(f"  Accent Blue: {COLORS['accent_blue']}")
    print(f"  Accent Yellow: {COLORS['accent_yellow']}")
    print(f"  Negative Red: {COLORS['negative_red']}")

    print("\nSlide Blueprints Available:")
    for blueprint_name in SLIDE_BLUEPRINTS.keys():
        print(f"  - {blueprint_name}")
