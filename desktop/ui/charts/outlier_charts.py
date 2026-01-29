"""
Outlier Charts - Professional card-based layout
Clean, modern analytics dashboard design
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGridLayout, QFrame, QScrollArea)
from PyQt5.QtCore import Qt
import numpy as np

from ..design_system import (COLORS, SPACING, DIMENSIONS, CARD_STYLE,
                            get_section_title_style, get_card_title_style, 
                            get_body_text_style, get_caption_style)

class OutlierCharts(QWidget):
    """Professional outlier charts with card-based layout"""
    
    def __init__(self):
        super().__init__()
        self.analysis_data = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize outlier UI with professional layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        layout.setSpacing(SPACING['lg'])
        
        # Section header
        self.create_section_header(layout)
        
        # Charts section
        self.create_charts_section(layout)
        
        # Outlier details section
        self.create_details_section(layout)
        
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
        title_label = QLabel("Outlier Detection")
        title_label.setStyleSheet(get_section_title_style())
        
        # Description
        desc_label = QLabel("Identification and analysis of equipment operating outside normal parameters")
        desc_label.setStyleSheet(get_body_text_style())
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        
        layout.addWidget(header_frame)
        
    def create_charts_section(self, layout):
        """Create outlier charts section"""
        charts_frame = QFrame()
        charts_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        
        charts_layout = QHBoxLayout(charts_frame)
        charts_layout.setSpacing(SPACING['md'])
        charts_layout.setContentsMargins(0, 0, 0, 0)
        
        # Outlier summary bar chart
        self.summary_chart_widget = self.create_chart_card(
            "Outlier Detection Summary", 
            "Number of outliers detected per parameter"
        )
        
        # Outlier distribution pie chart
        self.distribution_widget = self.create_chart_card(
            "Outlier Distribution", 
            "Percentage breakdown of outliers by parameter"
        )
        
        charts_layout.addWidget(self.summary_chart_widget)
        charts_layout.addWidget(self.distribution_widget)
        
        layout.addWidget(charts_frame)
        
    def create_details_section(self, layout):
        """Create outlier analysis details section"""
        details_frame = QFrame()
        details_frame.setStyleSheet(CARD_STYLE)
        
        details_layout = QVBoxLayout(details_frame)
        details_layout.setSpacing(SPACING['md'])
        
        # Section header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(SPACING['xs'])
        
        title_label = QLabel("Outlier Analysis Details")
        title_label.setStyleSheet(get_card_title_style())
        
        desc_label = QLabel("Detailed breakdown of outlier detection results")
        desc_label.setStyleSheet(get_caption_style())
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        
        # Scrollable area for outlier details
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background-color: {COLORS['surface_variant']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {COLORS['primary']};
                border-radius: 6px;
                min-height: 20px;
            }}
        """)
        
        self.details_widget = QWidget()
        self.details_layout = QVBoxLayout(self.details_widget)
        self.details_layout.setSpacing(SPACING['md'])
        
        scroll_area.setWidget(self.details_widget)
        
        details_layout.addLayout(header_layout)
        details_layout.addWidget(scroll_area)
        
        layout.addWidget(details_frame)
        
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
        
    def update_data(self, analysis_results):
        """Update outlier charts with new analysis data"""
        self.analysis_data = analysis_results
        
        try:
            print("DEBUG: Starting outlier charts update...")
            # Update outlier charts
            self.update_outlier_charts(analysis_results)
            print("DEBUG: Outlier charts updated successfully")
            
            # Update outlier details
            self.update_outlier_details(analysis_results)
            print("DEBUG: Outlier details updated successfully")
            
        except Exception as e:
            print(f"ERROR: Error in outlier charts update: {e}")
            import traceback
            traceback.print_exc()
            # Show error message in charts
            self.show_no_data_message()
        
    def update_outlier_charts(self, analysis_results):
        """Update outlier charts"""
        outliers = analysis_results.get('outliers', {})
        basic_analysis = outliers.get('basic_analysis', {})
        
        if not basic_analysis:
            self.show_no_data_message()
            return
            
        # Update outlier summary chart
        self.update_summary_chart(basic_analysis)
        
        # Update outlier distribution chart
        self.update_distribution_chart(basic_analysis)
        
    def update_summary_chart(self, basic_analysis):
        """Update outlier summary bar chart"""
        figure = self.summary_chart_widget.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        
        # Prepare outlier count data
        parameters = []
        outlier_counts = []
        
        for parameter, data in basic_analysis.items():
            if isinstance(data, dict) and 'outlier_count' in data:
                parameters.append(parameter)
                outlier_counts.append(data.get('outlier_count', 0))
        
        if not parameters or all(count == 0 for count in outlier_counts):
            ax.text(0.5, 0.5, 'No outlier data available', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=14, color=COLORS['text_disabled'])
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            bars = ax.bar(parameters, outlier_counts, 
                         color=COLORS['warning'], alpha=0.8,
                         edgecolor=COLORS['border'], linewidth=1)
            
            # Professional styling
            ax.set_ylabel('Number of Outliers', fontsize=12, color=COLORS['text_secondary'])
            ax.grid(True, alpha=0.3, color=COLORS['border'])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color(COLORS['border'])
            ax.spines['bottom'].set_color(COLORS['border'])
            ax.tick_params(colors=COLORS['text_secondary'])
            
            # Add value labels on bars
            for bar, count in zip(bars, outlier_counts):
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height + height*0.02,
                           f'{int(count)}', ha='center', va='bottom',
                           fontsize=10, color=COLORS['text_primary'], fontweight='bold')
        
        figure.tight_layout()
        self.summary_chart_widget.canvas.draw()
        
    def update_distribution_chart(self, basic_analysis):
        """Update outlier distribution pie chart"""
        figure = self.distribution_widget.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        
        # Prepare percentage data
        parameters = []
        percentages = []
        
        for parameter, data in basic_analysis.items():
            if isinstance(data, dict) and 'outlier_percentage' in data:
                percentage = data.get('outlier_percentage', 0)
                if percentage > 0:  # Only include parameters with outliers
                    parameters.append(parameter)
                    percentages.append(percentage)
        
        if not parameters or all(p == 0 for p in percentages):
            ax.text(0.5, 0.5, 'No outlier percentage data available', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=14, color=COLORS['text_disabled'])
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            # Professional color palette
            colors = [COLORS['error'], COLORS['warning'], COLORS['info'], 
                     COLORS['success'], COLORS['primary']]
            
            # Ensure we have enough colors
            chart_colors = colors[:len(parameters)] if len(parameters) <= len(colors) else colors * ((len(parameters) // len(colors)) + 1)
            
            wedges, texts, autotexts = ax.pie(percentages, labels=parameters, autopct='%1.1f%%',
                                             colors=chart_colors[:len(parameters)], startangle=90,
                                             textprops={'fontsize': 10, 'color': COLORS['text_primary']})
            
            # Style the percentage text
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
        
        figure.tight_layout()
        self.distribution_widget.canvas.draw()
        
    def update_outlier_details(self, analysis_results):
        """Update outlier details section"""
        # Clear existing widgets
        for i in reversed(range(self.details_layout.count())): 
            child = self.details_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        outliers = analysis_results.get('outliers', {})
        basic_analysis = outliers.get('basic_analysis', {})
        
        if not basic_analysis:
            no_data_label = QLabel("No outlier analysis data available")
            no_data_label.setAlignment(Qt.AlignCenter)
            no_data_label.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['text_disabled']};
                    font-style: italic;
                    padding: {SPACING['xl']}px;
                    font-size: 16px;
                }}
            """)
            self.details_layout.addWidget(no_data_label)
            return
        
        # Create parameter analysis cards
        for parameter, data in basic_analysis.items():
            if isinstance(data, dict):
                parameter_card = self.create_parameter_card(parameter, data)
                self.details_layout.addWidget(parameter_card)
        
        # Add stretch to push cards to top
        self.details_layout.addStretch()
        
    def create_parameter_card(self, parameter, data):
        """Create professional outlier analysis card for a parameter"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface_variant']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: {SPACING['lg']}px;
                margin-bottom: {SPACING['md']}px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(SPACING['md'])
        
        # Parameter title
        title_label = QLabel(f"{parameter} Outlier Analysis")
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {COLORS['text_primary']};
                margin-bottom: {SPACING['sm']}px;
            }}
        """)
        layout.addWidget(title_label)
        
        # Statistics grid
        stats_frame = QFrame()
        stats_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        stats_grid = QGridLayout(stats_frame)
        stats_grid.setSpacing(SPACING['md'])
        
        # Create stat cards
        normal_range = data.get('normal_range', 'N/A')
        outlier_count = data.get('outlier_count', 0)
        outlier_percentage = data.get('outlier_percentage', 0)
        
        normal_card = self.create_stat_card("Normal Range", str(normal_range))
        count_card = self.create_stat_card("Outliers Found", str(outlier_count))
        percentage_card = self.create_stat_card("Percentage", f"{outlier_percentage:.1f}%")
        
        stats_grid.addWidget(normal_card, 0, 0)
        stats_grid.addWidget(count_card, 0, 1)
        stats_grid.addWidget(percentage_card, 0, 2)
        
        # Threshold info
        threshold_info = data.get('threshold_info', {})
        if threshold_info:
            lower_bound = threshold_info.get('lower_bound', 'N/A')
            upper_bound = threshold_info.get('upper_bound', 'N/A')
            threshold_card = self.create_stat_card("Thresholds", f"{lower_bound} - {upper_bound}")
            stats_grid.addWidget(threshold_card, 1, 0, 1, 3)
        
        layout.addWidget(stats_frame)
        
        # Outlier equipment list
        outliers_list = data.get('outliers', [])
        if outliers_list and len(outliers_list) > 0:
            outliers_frame = QFrame()
            outliers_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['surface']};
                    border: 1px solid {COLORS['border_light']};
                    border-radius: 6px;
                    padding: {SPACING['md']}px;
                }}
            """)
            
            outliers_layout = QVBoxLayout(outliers_frame)
            outliers_layout.setSpacing(SPACING['sm'])
            
            outliers_title = QLabel("Outlier Equipment:")
            outliers_title.setStyleSheet(f"""
                QLabel {{
                    font-weight: bold;
                    color: {COLORS['text_primary']};
                    margin-bottom: {SPACING['xs']}px;
                }}
            """)
            outliers_layout.addWidget(outliers_title)
            
            # Show first 5 outliers
            for i, outlier in enumerate(outliers_list[:5]):
                if isinstance(outlier, dict):
                    equipment_name = outlier.get('equipment_name', 'Unknown')
                    equipment_type = outlier.get('type', 'Unknown')
                    value = outlier.get('value', 0)
                    
                    outlier_label = QLabel(f"• {equipment_name} ({equipment_type}): {value:.2f}")
                    outlier_label.setStyleSheet(f"""
                        QLabel {{
                            margin-left: {SPACING['md']}px;
                            color: {COLORS['text_secondary']};
                            font-size: 13px;
                        }}
                    """)
                    outliers_layout.addWidget(outlier_label)
            
            # Show count if more outliers exist
            if len(outliers_list) > 5:
                more_label = QLabel(f"... and {len(outliers_list) - 5} more outliers")
                more_label.setStyleSheet(f"""
                    QLabel {{
                        margin-left: {SPACING['md']}px;
                        color: {COLORS['text_disabled']};
                        font-style: italic;
                        font-size: 12px;
                    }}
                """)
                outliers_layout.addWidget(more_label)
            
            layout.addWidget(outliers_frame)
        
        return card
        
    def create_stat_card(self, title, value):
        """Create a small stat card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border_light']};
                border-radius: 6px;
                padding: {SPACING['sm']}px;
                min-height: 60px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(SPACING['xs'])
        
        # Value
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {COLORS['primary']};
                margin: 0;
            }}
        """)
        
        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: {COLORS['text_secondary']};
                margin: 0;
            }}
        """)
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        return card
        
    def show_no_data_message(self):
        """Show no data available message"""
        for widget in [self.summary_chart_widget, self.distribution_widget]:
            figure = widget.figure
            figure.clear()
            
            ax = figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No outlier data available', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=14, color=COLORS['text_disabled'])
            ax.set_xticks([])
            ax.set_yticks([])
            
            figure.tight_layout()
            widget.canvas.draw()