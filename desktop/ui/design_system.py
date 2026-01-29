"""
Design System Constants for Professional Dashboard UI
Inspired by Material UI / Ant Design analytics dashboards
"""

# Color Palette - Neutral with single accent
COLORS = {
    # Primary Colors
    'primary': '#1976d2',
    'primary_light': '#42a5f5',
    'primary_dark': '#1565c0',
    
    # Neutral Colors
    'background': '#fafafa',
    'surface': '#ffffff',
    'surface_variant': '#f5f5f5',
    'border': '#e0e0e0',
    'border_light': '#f0f0f0',
    
    # Text Colors
    'text_primary': '#212121',
    'text_secondary': '#757575',
    'text_disabled': '#bdbdbd',
    
    # Status Colors
    'success': '#4caf50',
    'warning': '#ff9800',
    'error': '#f44336',
    'info': '#2196f3',
}

# Typography Scale
TYPOGRAPHY = {
    'page_title': {
        'size': 24,
        'weight': 'bold',
        'color': COLORS['text_primary']
    },
    'section_title': {
        'size': 18,
        'weight': '600',
        'color': COLORS['text_primary']
    },
    'card_title': {
        'size': 16,
        'weight': '500',
        'color': COLORS['text_primary']
    },
    'body': {
        'size': 14,
        'weight': 'normal',
        'color': COLORS['text_secondary']
    },
    'caption': {
        'size': 12,
        'weight': 'normal',
        'color': COLORS['text_disabled']
    }
}

# Spacing System (8px grid)
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32,
    'xxl': 48
}

# Component Dimensions
DIMENSIONS = {
    'card_min_height': 300,
    'chart_aspect_ratio': 1.6,  # 16:10
    'chart_min_width': 400,
    'chart_min_height': 250,
    'container_max_width': 1200,
    'sidebar_width': 280
}

# Card Styling
CARD_STYLE = f"""
QFrame {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: {SPACING['lg']}px;
    margin: {SPACING['sm']}px;
}}
"""

# Button Styling
BUTTON_PRIMARY = f"""
QPushButton {{
    background-color: {COLORS['primary']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: {SPACING['md']}px {SPACING['lg']}px;
    font-size: {TYPOGRAPHY['body']['size']}px;
    font-weight: 500;
    min-height: 36px;
}}
QPushButton:hover {{
    background-color: {COLORS['primary_light']};
}}
QPushButton:pressed {{
    background-color: {COLORS['primary_dark']};
}}
QPushButton:disabled {{
    background-color: {COLORS['border']};
    color: {COLORS['text_disabled']};
}}
"""

# Tab Styling
TAB_STYLE = f"""
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    background-color: {COLORS['surface']};
    border-radius: 8px;
    margin-top: 2px;
}}
QTabBar::tab {{
    background-color: {COLORS['surface_variant']};
    padding: {SPACING['md']}px {SPACING['lg']}px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-size: {TYPOGRAPHY['body']['size']}px;
    color: {COLORS['text_secondary']};
    min-width: 100px;
}}
QTabBar::tab:selected {{
    background-color: {COLORS['surface']};
    color: {COLORS['primary']};
    border-bottom: 2px solid {COLORS['primary']};
    font-weight: 500;
}}
QTabBar::tab:hover:!selected {{
    background-color: {COLORS['border_light']};
    color: {COLORS['text_primary']};
}}
"""

def get_section_title_style():
    """Get section title styling"""
    return f"""
    QLabel {{
        font-size: {TYPOGRAPHY['section_title']['size']}px;
        font-weight: {TYPOGRAPHY['section_title']['weight']};
        color: {TYPOGRAPHY['section_title']['color']};
        margin-bottom: {SPACING['sm']}px;
        padding: 0;
    }}
    """

def get_card_title_style():
    """Get card title styling"""
    return f"""
    QLabel {{
        font-size: {TYPOGRAPHY['card_title']['size']}px;
        font-weight: {TYPOGRAPHY['card_title']['weight']};
        color: {TYPOGRAPHY['card_title']['color']};
        margin-bottom: {SPACING['md']}px;
        padding: 0;
    }}
    """

def get_body_text_style():
    """Get body text styling"""
    return f"""
    QLabel {{
        font-size: {TYPOGRAPHY['body']['size']}px;
        color: {TYPOGRAPHY['body']['color']};
        line-height: 1.5;
    }}
    """

def get_caption_style():
    """Get caption text styling"""
    return f"""
    QLabel {{
        font-size: {TYPOGRAPHY['caption']['size']}px;
        color: {TYPOGRAPHY['caption']['color']};
        font-style: italic;
    }}
    """