"""
Statistics Charts - Professional card-based layout
Clean, modern analytics dashboard design
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
import numpy as np

from ..design_system import (COLORS, SPACING, DIMENSIONS, CARD_STYLE,
                            get_section_title_style, get_card_title_style, 
                            get_body_text_style, get_caption_style)

class StatisticsCharts(QWidget):
    """Professional statistics charts with card-based layout"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize statistics UI with professional layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        layout.setSpacing(SPACING['lg'])
        
        # Section header
        self.create_section_header(layout)
        
        # Statistical summary chart
        self.create_summary_section(layout)
        
        # Box plot and variance analysis
        self.create_analysis_section(layout)
        
        # Detailed statistics table
        self.create_table_section(layout)
        
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
        title_label = QLabel("Statistical Analysis")
        title_label.setStyleSheet(get_section_title_style())
        
        # Description
        desc_label = QLabel("Comprehensive statistical summary and distribution analysis")
        desc_label.setStyleSheet(get_body_text_style())
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        
        layout.addWidget(header_frame)
        
    def create_summary_section(self, layout):
        """Create statistical summary chart section"""
        self.stats_chart = self.create_chart_card(
            "Statistical Summary", 
            "Mean, standard deviation, min/max values across parameters"
        )
        layout.addWidget(self.stats_chart)
        
    def create_analysis_section(self, layout):
        """Create box plot and variance analysis section"""
        analysis_frame = QFrame()
        analysis_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
        
        analysis_layout = QHBoxLayout(analysis_frame)
        analysis_layout.setSpacing(SPACING['md'])
        analysis_layout.setContentsMargins(0, 0, 0, 0)
        
        # Box plot analysis card
        self.box_plot_chart = self.create_chart_card(
            "Quartile Analysis", 
            "Distribution quartiles (Q1, Median, Q3) for each parameter"
        )
        
        # Variance analysis card
        self.variance_chart = self.create_chart_card(
            "Variance Analysis", 
            "Variance and coefficient of variation comparison"
        )
        
        analysis_layout.addWidget(self.box_plot_chart)
        analysis_layout.addWidget(self.variance_chart)
        
        layout.addWidget(analysis_frame)
        
    def create_table_section(self, layout):
        """Create detailed statistics table section"""
        table_frame = QFrame()
        table_frame.setStyleSheet(CARD_STYLE)
        
        table_layout = QVBoxLayout(table_frame)
        table_layout.setSpacing(SPACING['md'])
        
        # Section header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(SPACING['xs'])
        
        title_label = QLabel("Detailed Statistical Summary")
        title_label.setStyleSheet(get_card_title_style())
        
        desc_label = QLabel("Complete statistical breakdown for all parameters")
        desc_label.setStyleSheet(get_caption_style())
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        
        # Statistics table
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(9)
        self.stats_table.setHorizontalHeaderLabels([
            'Parameter', 'Count', 'Mean', 'Std Dev', 'Min', 'Q1', 'Median', 'Q3', 'Max'
        ])
        
        # Professional table styling
        self.stats_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                gridline-color: {COLORS['border_light']};
                font-size: {SPACING['md']}px;
            }}
            QTableWidget::item {{
                padding: {SPACING['sm']}px;
                border-bottom: 1px solid {COLORS['border_light']};
            }}
            QTableWidget::item:selected {{
                background-color: {COLORS['primary_light']};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {COLORS['surface_variant']};
                padding: {SPACING['md']}px;
                border: none;
                border-bottom: 2px solid {COLORS['primary']};
                font-weight: 600;
                color: {COLORS['text_primary']};
            }}
        """)
        
        # Configure table behavior
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stats_table.verticalHeader().setVisible(False)
        self.stats_table.setAlternatingRowColors(True)
        self.stats_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        table_layout.addLayout(header_layout)
        table_layout.addWidget(self.stats_table)
        
        layout.addWidget(table_frame)
        
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
        figure = Figure(figsize=(8, 5), dpi=100)
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
        """Update statistics charts with new data"""
        statistical_summary = analysis_results.get('summary_metrics', {}).get('statistical_summary', {})
        overall_stats = analysis_results.get('summary_metrics', {}).get('overall_stats', {})
        
        if statistical_summary:
            self.update_statistical_chart(statistical_summary)
            self.update_box_plot(overall_stats)
            self.update_variance_chart(analysis_results.get('advanced_statistics', {}))
            self.update_stats_table(statistical_summary)
            
    def update_statistical_chart(self, statistical_summary):
        """Update statistical summary bar chart"""
        figure = self.stats_chart.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        stats = ['mean', 'std', 'min', 'max']
        colors = [COLORS['primary'], COLORS['info'], COLORS['warning'], COLORS['error']]
        
        x = np.arange(len(parameters))
        width = 0.2
        
        for i, stat in enumerate(stats):
            values = [statistical_summary.get(param, {}).get(stat, 0) for param in parameters]
            bars = ax.bar(x + i * width, values, width, label=stat.capitalize(), 
                         color=colors[i], alpha=0.8, edgecolor=COLORS['border'])
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                           f'{value:.1f}', ha='center', va='bottom', 
                           fontsize=9, color=COLORS['text_primary'])
            
        # Professional styling
        ax.set_xlabel('Parameters', fontsize=12, color=COLORS['text_secondary'])
        ax.set_ylabel('Values', fontsize=12, color=COLORS['text_secondary'])
        ax.set_xticks(x + width * 1.5)
        ax.set_xticklabels(parameters)
        ax.legend(frameon=True, fancybox=True, shadow=True)
        ax.grid(True, alpha=0.3, color=COLORS['border'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['border'])
        ax.spines['bottom'].set_color(COLORS['border'])
        ax.tick_params(colors=COLORS['text_secondary'])
        
        figure.tight_layout()
        self.stats_chart.canvas.draw()
        
    def update_box_plot(self, overall_stats):
        """Update box plot simulation"""
        figure = self.box_plot_chart.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        colors = [COLORS['primary'], COLORS['info'], COLORS['success']]
        
        x = np.arange(len(parameters))
        width = 0.25
        
        q25_values = [overall_stats.get(param, {}).get('q25', 0) for param in parameters]
        median_values = [overall_stats.get(param, {}).get('median', 0) for param in parameters]
        q75_values = [overall_stats.get(param, {}).get('q75', 0) for param in parameters]
        
        bars1 = ax.bar(x - width, q25_values, width, label='Q1 (25%)', 
                      color=colors[0], alpha=0.7, edgecolor=COLORS['border'])
        bars2 = ax.bar(x, median_values, width, label='Median (50%)', 
                      color=colors[1], alpha=0.7, edgecolor=COLORS['border'])
        bars3 = ax.bar(x + width, q75_values, width, label='Q3 (75%)', 
                      color=colors[2], alpha=0.7, edgecolor=COLORS['border'])
        
        # Add value labels
        for bars, values in [(bars1, q25_values), (bars2, median_values), (bars3, q75_values)]:
            for bar, value in zip(bars, values):
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                           f'{value:.1f}', ha='center', va='bottom', 
                           fontsize=9, color=COLORS['text_primary'])
        
        # Professional styling
        ax.set_xlabel('Parameters', fontsize=12, color=COLORS['text_secondary'])
        ax.set_ylabel('Values', fontsize=12, color=COLORS['text_secondary'])
        ax.set_xticks(x)
        ax.set_xticklabels(parameters)
        ax.legend(frameon=True, fancybox=True, shadow=True)
        ax.grid(True, alpha=0.3, color=COLORS['border'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['border'])
        ax.spines['bottom'].set_color(COLORS['border'])
        ax.tick_params(colors=COLORS['text_secondary'])
        
        figure.tight_layout()
        self.box_plot_chart.canvas.draw()
        
    def update_variance_chart(self, advanced_stats):
        """Update variance analysis chart"""
        figure = self.variance_chart.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        
        variance_analysis = advanced_stats.get('variance_analysis', {})
        if not variance_analysis:
            ax.text(0.5, 0.5, 'No variance data available', ha='center', va='center', 
                   transform=ax.transAxes, fontsize=14, color=COLORS['text_disabled'])
            ax.set_xticks([])
            ax.set_yticks([])
            figure.tight_layout()
            self.variance_chart.canvas.draw()
            return
            
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        variances = [variance_analysis.get(param, {}).get('variance', 0) for param in parameters]
        cvs = [variance_analysis.get(param, {}).get('coefficient_of_variation', 0) for param in parameters]
        
        x = np.arange(len(parameters))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, variances, width, label='Variance', 
                      color=COLORS['primary'], alpha=0.8, edgecolor=COLORS['border'])
        bars2 = ax.bar(x + width/2, cvs, width, label='Coefficient of Variation', 
                      color=COLORS['warning'], alpha=0.8, edgecolor=COLORS['border'])
        
        # Add value labels
        for bars, values in [(bars1, variances), (bars2, cvs)]:
            for bar, value in zip(bars, values):
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                           f'{value:.2f}', ha='center', va='bottom', 
                           fontsize=9, color=COLORS['text_primary'])
        
        # Professional styling
        ax.set_xlabel('Parameters', fontsize=12, color=COLORS['text_secondary'])
        ax.set_ylabel('Values', fontsize=12, color=COLORS['text_secondary'])
        ax.set_xticks(x)
        ax.set_xticklabels(parameters)
        ax.legend(frameon=True, fancybox=True, shadow=True)
        ax.grid(True, alpha=0.3, color=COLORS['border'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['border'])
        ax.spines['bottom'].set_color(COLORS['border'])
        ax.tick_params(colors=COLORS['text_secondary'])
        
        figure.tight_layout()
        self.variance_chart.canvas.draw()
        
    def update_stats_table(self, statistical_summary):
        """Update detailed statistics table"""
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        self.stats_table.setRowCount(len(parameters))
        
        for i, param in enumerate(parameters):
            stats = statistical_summary.get(param, {})
            
            # Create styled table items
            items = [
                QTableWidgetItem(param),
                QTableWidgetItem(f"{stats.get('count', 0):.0f}"),
                QTableWidgetItem(f"{stats.get('mean', 0):.2f}"),
                QTableWidgetItem(f"{stats.get('std', 0):.2f}"),
                QTableWidgetItem(f"{stats.get('min', 0):.2f}"),
                QTableWidgetItem(f"{stats.get('25%', 0):.2f}"),
                QTableWidgetItem(f"{stats.get('50%', 0):.2f}"),
                QTableWidgetItem(f"{stats.get('75%', 0):.2f}"),
                QTableWidgetItem(f"{stats.get('max', 0):.2f}")
            ]
            
            for j, item in enumerate(items):
                if j == 0:  # Parameter name - make it bold
                    item.setData(Qt.FontRole, 600)
                item.setTextAlignment(Qt.AlignCenter)
                self.stats_table.setItem(i, j, item)
            
        self.stats_table.resizeColumnsToContents()