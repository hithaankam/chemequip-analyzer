"""
Overview Charts - Professional card-based layout
Clean, modern analytics dashboard design
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGridLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import numpy as np

from ..design_system import (COLORS, SPACING, DIMENSIONS, CARD_STYLE,
                            get_section_title_style, get_card_title_style, 
                            get_body_text_style, get_caption_style)

class OverviewCharts(QWidget):
    """Professional overview charts with card-based layout"""
    
    def __init__(self):
        super().__init__()
        self.analysis_data = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize overview UI with professional layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        layout.setSpacing(SPACING['lg'])
        
        # Section header
        self.create_section_header(layout)
        
        # Key metrics cards
        self.create_metrics_section(layout)
        
        # Charts section
        self.create_charts_section(layout)
        
        # Equipment details section
        self.create_equipment_details_section(layout)
        
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
        title_label = QLabel("Dataset Overview")
        title_label.setStyleSheet(get_section_title_style())
        
        # Description
        desc_label = QLabel("Key metrics and equipment distribution analysis")
        desc_label.setStyleSheet(get_body_text_style())
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        
        layout.addWidget(header_frame)
        
    def create_metrics_section(self, layout):
        """Create key metrics cards"""
        metrics_frame = QFrame()
        metrics_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        
        metrics_layout = QHBoxLayout(metrics_frame)
        metrics_layout.setSpacing(SPACING['md'])
        metrics_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create metric cards
        self.total_equipment_card = self.create_metric_card("Total Equipment", "0", COLORS['primary'])
        self.equipment_types_card = self.create_metric_card("Equipment Types", "0", COLORS['info'])
        self.avg_flowrate_card = self.create_metric_card("Avg Flowrate", "0.0", COLORS['success'])
        self.avg_temperature_card = self.create_metric_card("Avg Temperature", "0.0°C", COLORS['warning'])
        
        metrics_layout.addWidget(self.total_equipment_card)
        metrics_layout.addWidget(self.equipment_types_card)
        metrics_layout.addWidget(self.avg_flowrate_card)
        metrics_layout.addWidget(self.avg_temperature_card)
        
        layout.addWidget(metrics_frame)
        
    def create_metric_card(self, title, value, color):
        """Create a professional metric card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: {SPACING['lg']}px;
                min-height: 100px;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(SPACING['sm'])
        
        # Value (large number)
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 28px;
                font-weight: bold;
                color: {color};
                margin: 0;
            }}
        """)
        
        # Title (smaller text)
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(get_body_text_style())
        
        card_layout.addWidget(value_label)
        card_layout.addWidget(title_label)
        
        # Store value label for updates
        setattr(card, 'value_label', value_label)
        
        return card
        
    def create_charts_section(self, layout):
        """Create charts section with proper cards"""
        charts_frame = QFrame()
        charts_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        
        charts_layout = QHBoxLayout(charts_frame)
        charts_layout.setSpacing(SPACING['md'])
        charts_layout.setContentsMargins(0, 0, 0, 0)
        
        # Bar chart card
        self.bar_chart_card = self.create_chart_card(
            "Equipment Distribution", 
            "Distribution of equipment types in the dataset"
        )
        
        # Pie chart card
        self.pie_chart_card = self.create_chart_card(
            "Type Breakdown", 
            "Percentage breakdown by equipment type"
        )
        
        charts_layout.addWidget(self.bar_chart_card)
        charts_layout.addWidget(self.pie_chart_card)
        
        layout.addWidget(charts_frame)
        
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
        figure = Figure(figsize=(6, 4), dpi=100)
        figure.patch.set_facecolor('white')
        canvas = FigureCanvas(figure)
        canvas.setMinimumSize(DIMENSIONS['chart_min_width'], DIMENSIONS['chart_min_height'])
        
        card_layout.addLayout(header_layout)
        card_layout.addWidget(canvas)
        
        # Store figure and canvas
        card.figure = figure
        card.canvas = canvas
        
        return card
        
    def create_equipment_details_section(self, layout):
        """Create equipment type details section"""
        details_frame = QFrame()
        details_frame.setStyleSheet(CARD_STYLE)
        
        details_layout = QVBoxLayout(details_frame)
        details_layout.setSpacing(SPACING['md'])
        
        # Section header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(SPACING['xs'])
        
        title_label = QLabel("Equipment Type Details")
        title_label.setStyleSheet(get_card_title_style())
        
        desc_label = QLabel("Detailed breakdown of each equipment type")
        desc_label.setStyleSheet(get_caption_style())
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        
        # Types container
        self.types_container = QFrame()
        self.types_container.setStyleSheet("QFrame { background: transparent; border: none; }")
        self.types_layout = QHBoxLayout(self.types_container)
        self.types_layout.setSpacing(SPACING['md'])
        self.types_layout.setContentsMargins(0, 0, 0, 0)
        
        details_layout.addLayout(header_layout)
        details_layout.addWidget(self.types_container)
        
        layout.addWidget(details_frame)
        
    def update_data(self, analysis_results):
        """Update overview with new analysis data"""
        self.analysis_data = analysis_results
        
        # Update metrics
        self.update_metrics(analysis_results)
        
        # Update charts
        self.update_charts(analysis_results)
        
        # Update equipment details
        self.update_equipment_details(analysis_results)
        
    def update_metrics(self, analysis_results):
        """Update metric cards"""
        dataset_overview = analysis_results.get('summary_metrics', {}).get('dataset_overview', {})
        overall_stats = analysis_results.get('summary_metrics', {}).get('overall_stats', {})
        
        total_equipment = dataset_overview.get('total_equipment_count', 0)
        equipment_types_count = dataset_overview.get('equipment_types_count', 0)
        avg_flowrate = overall_stats.get('Flowrate', {}).get('mean', 0)
        avg_temperature = overall_stats.get('Temperature', {}).get('mean', 0)
        
        self.total_equipment_card.value_label.setText(str(total_equipment))
        self.equipment_types_card.value_label.setText(str(equipment_types_count))
        self.avg_flowrate_card.value_label.setText(f"{avg_flowrate:.1f}")
        self.avg_temperature_card.value_label.setText(f"{avg_temperature:.1f}°C")
        
    def update_charts(self, analysis_results):
        """Update chart visualizations"""
        distributions = analysis_results.get('distributions', {})
        equipment_types = distributions.get('equipment_types', {})
        
        if not equipment_types:
            return
            
        # Update bar chart
        self.update_bar_chart(equipment_types)
        
        # Update pie chart
        self.update_pie_chart(equipment_types)
        
    def update_bar_chart(self, equipment_types):
        """Update equipment distribution bar chart"""
        figure = self.bar_chart_card.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        
        types = list(equipment_types.keys())
        counts = list(equipment_types.values())
        
        # Use professional color scheme
        bars = ax.bar(types, counts, color=COLORS['primary'], alpha=0.8, edgecolor=COLORS['border'])
        
        # Styling
        ax.set_ylabel('Count', fontsize=12, color=COLORS['text_secondary'])
        ax.tick_params(axis='x', rotation=45, labelsize=10, colors=COLORS['text_secondary'])
        ax.tick_params(axis='y', labelsize=10, colors=COLORS['text_secondary'])
        ax.grid(True, alpha=0.3, color=COLORS['border'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['border'])
        ax.spines['bottom'].set_color(COLORS['border'])
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{int(height)}', ha='center', va='bottom', 
                   fontsize=10, color=COLORS['text_primary'])
        
        figure.tight_layout()
        self.bar_chart_card.canvas.draw()
        
    def update_pie_chart(self, equipment_types):
        """Update equipment type pie chart"""
        figure = self.pie_chart_card.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        
        types = list(equipment_types.keys())
        counts = list(equipment_types.values())
        
        # Professional color palette
        colors = [COLORS['primary'], COLORS['info'], COLORS['success'], 
                 COLORS['warning'], '#9c27b0', '#ff5722']
        
        wedges, texts, autotexts = ax.pie(counts, labels=types, autopct='%1.1f%%',
                                         colors=colors[:len(types)], startangle=90,
                                         textprops={'fontsize': 10, 'color': COLORS['text_primary']})
        
        # Style the percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        figure.tight_layout()
        self.pie_chart_card.canvas.draw()
        
    def update_equipment_details(self, analysis_results):
        """Update equipment type detail cards"""
        # Clear existing cards
        for i in reversed(range(self.types_layout.count())): 
            child = self.types_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
                
        distributions = analysis_results.get('distributions', {})
        equipment_types = distributions.get('equipment_types', {})
        
        if not equipment_types:
            return
            
        total_count = sum(equipment_types.values())
        
        for equipment_type, count in equipment_types.items():
            percentage = (count / total_count * 100) if total_count > 0 else 0
            type_card = self.create_type_detail_card(equipment_type, count, percentage)
            self.types_layout.addWidget(type_card)
            
    def create_type_detail_card(self, type_name, count, percentage):
        """Create professional equipment type detail card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: {SPACING['md']}px;
                min-width: 140px;
                min-height: 80px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(SPACING['xs'])
        
        # Type name
        type_label = QLabel(type_name)
        type_label.setAlignment(Qt.AlignCenter)
        type_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: 600;
                color: {COLORS['text_primary']};
                margin: 0;
            }}
        """)
        type_label.setWordWrap(True)
        
        # Count
        count_label = QLabel(f"{count} units")
        count_label.setAlignment(Qt.AlignCenter)
        count_label.setStyleSheet(get_body_text_style())
        
        # Percentage
        percentage_label = QLabel(f"{percentage:.1f}%")
        percentage_label.setAlignment(Qt.AlignCenter)
        percentage_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {COLORS['primary']};
                margin: 0;
            }}
        """)
        
        layout.addWidget(type_label)
        layout.addWidget(count_label)
        layout.addWidget(percentage_label)
        
        return card