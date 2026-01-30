"""
Efficiency Charts - Professional card-based layout
Clean, modern analytics dashboard design
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
import numpy as np

from ..design_system import (COLORS, SPACING, DIMENSIONS, CARD_STYLE,
                            get_section_title_style, get_card_title_style, 
                            get_body_text_style, get_caption_style)

class EfficiencyCharts(QWidget):
    """Professional efficiency charts with card-based layout"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize efficiency UI with professional layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        layout.setSpacing(SPACING['lg'])
        
        # Section header
        self.create_section_header(layout)
        
        # Efficiency ranking chart
        self.create_efficiency_section(layout)
        
    def create_section_header(self, layout):
        """Create section header with title and description"""
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: transparent;
                border: none;
                padding: 0;
                margin-bottom: {SPACING['md']}px;
            }}
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(SPACING['xs'])
        
        # Title
        title_label = QLabel("Efficiency Analysis")
        title_label.setStyleSheet(get_section_title_style())
        
        # Description
        desc_label = QLabel("Equipment performance rankings and efficiency scores")
        desc_label.setStyleSheet(get_body_text_style())
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        
        layout.addWidget(header_frame)
        
    def create_efficiency_section(self, layout):
        """Create efficiency ranking chart section"""
        self.efficiency_chart = self.create_chart_card(
            "Top Equipment by Efficiency Score", 
            "Highest performing equipment ranked by overall efficiency metrics"
        )
        layout.addWidget(self.efficiency_chart)
        
    def create_chart_card(self, title, description):
        """Create a professional chart card"""
        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(SPACING['md'])
        
        # Card header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(SPACING['xs'])
        
        title_label = QLabel(title)
        title_label.setStyleSheet(get_card_title_style())
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet(get_caption_style())
        desc_label.setWordWrap(True)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        
        # Chart area
        figure = Figure(figsize=(10, 6), dpi=100)
        figure.patch.set_facecolor('white')
        canvas = FigureCanvas(figure)
        canvas.setMinimumSize(DIMENSIONS['chart_min_width'], DIMENSIONS['chart_min_height'])
        
        card_layout.addLayout(header_layout)
        card_layout.addWidget(canvas)
        
        # Store figure and canvas
        card.figure = figure
        card.canvas = canvas
        
        return card
        
    def update_data(self, analysis_results):
        """Update efficiency charts with new data"""
        efficiency = analysis_results.get('efficiency', {})
        rankings = efficiency.get('rankings', {}).get('overall_efficiency', [])
        
        if rankings:
            self.update_efficiency_chart(rankings[:10])
            
    def update_efficiency_chart(self, rankings):
        """Update efficiency ranking chart"""
        figure = self.efficiency_chart.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        
        if not rankings:
            # Professional empty state styling
            ax.text(0.5, 0.6, '📊', horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=32, alpha=0.3)
            ax.text(0.5, 0.4, 'No efficiency data available', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=14, color=COLORS['text_disabled'],
                   fontweight='500')
            ax.text(0.5, 0.3, 'Upload equipment data to see efficiency rankings', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12, color=COLORS['text_disabled'],
                   style='italic')
            
            # Clean empty state appearance
            ax.set_xticks([])
            ax.set_yticks([])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.set_facecolor(COLORS['surface_variant'])
            
            figure.patch.set_facecolor('white')
            figure.tight_layout()
            self.efficiency_chart.canvas.draw()
            return
        
        names = [item.get('equipment_name', 'Unknown') for item in rankings]
        scores = [item.get('efficiency_score', 0) for item in rankings]
        
        # Create color gradient based on efficiency scores
        colors = []
        for score in scores:
            if score > 0.8:
                colors.append(COLORS['success'])
            elif score > 0.6:
                colors.append(COLORS['primary'])
            elif score > 0.4:
                colors.append(COLORS['warning'])
            else:
                colors.append(COLORS['error'])
        
        y_pos = np.arange(len(names))
        bars = ax.barh(y_pos, scores, color=colors, alpha=0.8, edgecolor=COLORS['border'])
        
        # Add value labels on bars
        for i, (bar, score) in enumerate(zip(bars, scores)):
            width = bar.get_width()
            ax.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                   f'{score:.3f}', ha='left', va='center', 
                   fontsize=10, color=COLORS['text_primary'], fontweight='bold')
        
        # Professional styling
        ax.set_yticks(y_pos)
        ax.set_yticklabels(names, fontsize=10)
        ax.set_xlabel('Efficiency Score', fontsize=12, color=COLORS['text_secondary'])
        ax.set_xlim(0, max(scores) * 1.15 if scores else 1)
        ax.grid(True, alpha=0.3, color=COLORS['border'], axis='x')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['border'])
        ax.spines['bottom'].set_color(COLORS['border'])
        ax.tick_params(colors=COLORS['text_secondary'])
        
        # Invert y-axis to show highest scores at top
        ax.invert_yaxis()
        
        figure.tight_layout()
        self.efficiency_chart.canvas.draw()