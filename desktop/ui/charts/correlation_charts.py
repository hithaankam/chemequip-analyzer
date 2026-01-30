"""
Correlation Charts - Professional card-based layout
Clean, modern analytics dashboard design
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGridLayout, QFrame)
from PyQt5.QtCore import Qt
import numpy as np

from ..design_system import (COLORS, SPACING, DIMENSIONS, CARD_STYLE,
                            get_section_title_style, get_card_title_style, 
                            get_body_text_style, get_caption_style)

class CorrelationCharts(QWidget):
    """Professional correlation charts with card-based layout"""
    
    def __init__(self):
        super().__init__()
        self.analysis_data = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize correlation UI with professional layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        layout.setSpacing(SPACING['lg'])
        
        # Section header
        self.create_section_header(layout)
        
        # Charts section
        self.create_charts_section(layout)
        
        # Correlation insights section
        self.create_insights_section(layout)
        
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
        title_label = QLabel("Correlation Analysis")
        title_label.setStyleSheet(get_section_title_style())
        
        # Description
        desc_label = QLabel("Understanding relationships between Flowrate, Pressure, and Temperature")
        desc_label.setStyleSheet(get_body_text_style())
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        
        layout.addWidget(header_frame)
        
    def create_charts_section(self, layout):
        """Create correlation charts section"""
        charts_frame = QFrame()
        charts_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        
        charts_layout = QHBoxLayout(charts_frame)
        charts_layout.setSpacing(SPACING['md'])
        charts_layout.setContentsMargins(0, 0, 0, 0)
        
        # Parameter correlations bar chart
        self.correlation_chart_widget = self.create_chart_card(
            "Parameter Correlations", 
            "Correlation coefficients between equipment parameters"
        )
        
        # Correlation matrix heatmap
        self.heatmap_widget = self.create_chart_card(
            "Correlation Matrix", 
            "Visual correlation matrix showing parameter relationships"
        )
        
        charts_layout.addWidget(self.correlation_chart_widget)
        charts_layout.addWidget(self.heatmap_widget)
        
        layout.addWidget(charts_frame)
        
    def create_insights_section(self, layout):
        """Create correlation insights section"""
        insights_frame = QFrame()
        insights_frame.setStyleSheet(CARD_STYLE)
        
        insights_layout = QVBoxLayout(insights_frame)
        insights_layout.setSpacing(SPACING['md'])
        
        # Section header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(SPACING['xs'])
        
        title_label = QLabel("Correlation Insights")
        title_label.setStyleSheet(get_card_title_style())
        
        desc_label = QLabel("Key correlation findings and their operational implications")
        desc_label.setStyleSheet(get_caption_style())
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        
        # Insights grid
        self.insights_grid = QGridLayout()
        
        # Create insight cards
        self.flowrate_temp_card = self.create_insight_card("Flowrate-Temperature", "-")
        self.flowrate_pressure_card = self.create_insight_card("Flowrate-Pressure", "-")
        self.pressure_temp_card = self.create_insight_card("Pressure-Temperature", "-")
        
        self.insights_grid.addWidget(self.flowrate_temp_card, 0, 0)
        self.insights_grid.addWidget(self.flowrate_pressure_card, 0, 1)
        self.insights_grid.addWidget(self.pressure_temp_card, 1, 0, 1, 2)
        
        insights_layout.addLayout(header_layout)
        insights_layout.addLayout(self.insights_grid)
        
        layout.addWidget(insights_frame)
        
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
        
    def create_insight_card(self, title, value):
        """Create a professional insight card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface_variant']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: {SPACING['md']}px;
                min-height: 80px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(SPACING['xs'])
        
        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: 600;
                color: {COLORS['text_primary']};
                margin: 0;
            }}
        """)
        
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
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        # Store value label for updates
        card.value_label = value_label
        
        return card
        
    def update_data(self, analysis_results):
        """Update correlation charts with new analysis data"""
        self.analysis_data = analysis_results
        
        # Update correlation charts
        self.update_correlation_charts(analysis_results)
        
        # Update correlation insights
        self.update_correlation_insights(analysis_results)
        
    def update_correlation_charts(self, analysis_results):
        """Update correlation charts"""
        correlations = analysis_results.get('correlations', {})
        key_correlations = correlations.get('key_correlations', {})
        
        if not key_correlations:
            self.show_no_data_message()
            return
            
        # Update correlation bar chart
        self.update_correlation_bar_chart(key_correlations)
        
        # Update correlation heatmap
        self.update_correlation_heatmap(key_correlations)
        
    def update_correlation_bar_chart(self, key_correlations):
        """Update parameter correlations bar chart"""
        figure = self.correlation_chart_widget.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        
        # Prepare correlation data
        correlations = {
            'Flowrate-Temperature': float(key_correlations.get('flowrate_temperature', 0)),
            'Flowrate-Pressure': float(key_correlations.get('flowrate_pressure', 0)),
            'Pressure-Temperature': float(key_correlations.get('pressure_temperature', 0))
        }
        
        labels = list(correlations.keys())
        values = list(correlations.values())
        
        # Color bars based on correlation strength
        colors = []
        for val in values:
            if abs(val) > 0.7:
                colors.append(COLORS['error'])  # Strong correlation - red
            elif abs(val) > 0.3:
                colors.append(COLORS['primary'])  # Moderate correlation - blue
            else:
                colors.append(COLORS['warning'])  # Weak correlation - yellow
        
        bars = ax.bar(labels, values, color=colors, alpha=0.8, 
                     edgecolor=COLORS['border'], linewidth=1)
        
        # Professional styling
        ax.set_ylabel('Correlation Coefficient', fontsize=12, color=COLORS['text_secondary'])
        ax.set_ylim(-1, 1)
        ax.axhline(y=0, color=COLORS['text_disabled'], linestyle='-', alpha=0.5)
        ax.grid(True, alpha=0.3, color=COLORS['border'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['border'])
        ax.spines['bottom'].set_color(COLORS['border'])
        ax.tick_params(colors=COLORS['text_secondary'])
        
        # Rotate x-axis labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + (0.02 if height >= 0 else -0.05),
                   f'{value:.3f}', ha='center', va='bottom' if height >= 0 else 'top',
                   fontsize=10, color=COLORS['text_primary'], fontweight='bold')
        
        # Improve layout with better margins to prevent label clipping
        figure.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.25)
        self.correlation_chart_widget.canvas.draw()
        
    def update_correlation_heatmap(self, key_correlations):
        """Update correlation matrix heatmap"""
        figure = self.heatmap_widget.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        
        # Create correlation matrix data
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        correlation_matrix = np.array([
            [1.0, float(key_correlations.get('flowrate_pressure', 0)), float(key_correlations.get('flowrate_temperature', 0))],
            [float(key_correlations.get('flowrate_pressure', 0)), 1.0, float(key_correlations.get('pressure_temperature', 0))],
            [float(key_correlations.get('flowrate_temperature', 0)), float(key_correlations.get('pressure_temperature', 0)), 1.0]
        ])
        
        # Create professional heatmap using RdBu_r colormap
        im = ax.imshow(correlation_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='equal')
        
        # Set ticks and labels
        ax.set_xticks(range(len(parameters)))
        ax.set_yticks(range(len(parameters)))
        ax.set_xticklabels(parameters, fontsize=11, color=COLORS['text_secondary'])
        ax.set_yticklabels(parameters, fontsize=11, color=COLORS['text_secondary'])
        
        # Add correlation values as text
        for i in range(len(parameters)):
            for j in range(len(parameters)):
                text_color = 'white' if abs(correlation_matrix[i, j]) > 0.5 else 'black'
                text = ax.text(j, i, f'{correlation_matrix[i, j]:.3f}',
                             ha="center", va="center", color=text_color, 
                             fontweight='bold', fontsize=10)
        
        # Add colorbar with professional styling
        cbar = figure.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Correlation Coefficient', fontsize=11, color=COLORS['text_secondary'])
        cbar.ax.tick_params(colors=COLORS['text_secondary'])
        
        # Improve layout with better margins
        figure.subplots_adjust(left=0.15, right=0.85, top=0.95, bottom=0.15)
        self.heatmap_widget.canvas.draw()
        
    def update_correlation_insights(self, analysis_results):
        """Update correlation insights cards"""
        correlations = analysis_results.get('correlations', {})
        key_correlations = correlations.get('key_correlations', {})
        
        if not key_correlations:
            return
            
        # Update insight cards with interpretation
        flowrate_temp = float(key_correlations.get('flowrate_temperature', 0))
        flowrate_pressure = float(key_correlations.get('flowrate_pressure', 0))
        pressure_temp = float(key_correlations.get('pressure_temperature', 0))
        
        self.flowrate_temp_card.value_label.setText(
            f"{flowrate_temp:.3f}\n({self.interpret_correlation(flowrate_temp)})"
        )
        self.flowrate_pressure_card.value_label.setText(
            f"{flowrate_pressure:.3f}\n({self.interpret_correlation(flowrate_pressure)})"
        )
        self.pressure_temp_card.value_label.setText(
            f"{pressure_temp:.3f}\n({self.interpret_correlation(pressure_temp)})"
        )
        
    def interpret_correlation(self, correlation):
        """Interpret correlation strength"""
        abs_corr = abs(correlation)
        if abs_corr > 0.8:
            strength = "Very Strong"
        elif abs_corr > 0.6:
            strength = "Strong"
        elif abs_corr > 0.4:
            strength = "Moderate"
        elif abs_corr > 0.2:
            strength = "Weak"
        else:
            strength = "Very Weak"
            
        direction = "Positive" if correlation > 0 else "Negative"
        return f"{strength} {direction}"
        
    def show_no_data_message(self):
        """Show no data available message"""
        for widget in [self.correlation_chart_widget, self.heatmap_widget]:
            figure = widget.figure
            figure.clear()
            
            ax = figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No correlation data available', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=14, color=COLORS['text_disabled'])
            ax.set_xticks([])
            ax.set_yticks([])
            
            figure.tight_layout()
            widget.canvas.draw()