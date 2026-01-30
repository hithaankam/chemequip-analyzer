"""
Dashboard Widget - Professional card-based analytics dashboard
Inspired by Material UI/Ant Design dashboard layouts
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QLabel, QScrollArea, QFrame, QGridLayout, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from .charts.overview_charts import OverviewCharts
from .charts.statistics_charts import StatisticsCharts
from .charts.efficiency_charts import EfficiencyCharts
from .charts.correlation_charts import CorrelationCharts
from .charts.outlier_charts import OutlierCharts
from .charts.insights_panel import InsightsPanel
from .design_system import (COLORS, SPACING, DIMENSIONS, TAB_STYLE, 
                           get_section_title_style, get_body_text_style)

class DashboardWidget(QWidget):
    """Professional dashboard with card-based layout"""
    
    # Add signal for PDF generation
    pdf_generation_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.current_analysis = None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize dashboard UI with professional layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Dashboard header
        self.create_dashboard_header(layout)
        
        # Analysis tabs
        self.create_analysis_tabs(layout)
        
        # No data state
        self.create_no_data_state(layout)
        
    def create_dashboard_header(self, layout):
        """Create clean dashboard header"""
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border-bottom: 1px solid {COLORS['border']};
                padding: {SPACING['lg']}px;
            }}
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(SPACING['lg'])
        
        # Left side - title and subtitle
        title_section = QVBoxLayout()
        title_section.setSpacing(SPACING['xs'])
        
        # Title
        title_label = QLabel("Analysis Dashboard")
        title_label.setStyleSheet(get_section_title_style())
        
        # Subtitle
        subtitle_label = QLabel("Comprehensive equipment parameter analysis and insights")
        subtitle_label.setStyleSheet(get_body_text_style())
        
        title_section.addWidget(title_label)
        title_section.addWidget(subtitle_label)
        
        # Right side - PDF generation button
        self.pdf_button = QPushButton("📄 Generate PDF Report")
        self.pdf_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color: white;
                border: none;
                padding: {SPACING['md']}px {SPACING['lg']}px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
                min-width: 150px;
            }}
            QPushButton:hover {{
                background-color: #45a049;
            }}
            QPushButton:pressed {{
                background-color: #3d8b40;
            }}
            QPushButton:disabled {{
                background-color: {COLORS['border']};
                color: {COLORS['text_disabled']};
            }}
        """)
        self.pdf_button.setEnabled(False)  # Initially disabled
        self.pdf_button.clicked.connect(self.generate_pdf_report)
        
        header_layout.addLayout(title_section)
        header_layout.addStretch()
        header_layout.addWidget(self.pdf_button)
        
        layout.addWidget(header_frame)
        
    def create_analysis_tabs(self, layout):
        """Create analysis tabs with professional styling"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(TAB_STYLE)
        
        # Create chart widgets
        self.overview_charts = OverviewCharts()
        self.statistics_charts = StatisticsCharts()
        self.efficiency_charts = EfficiencyCharts()
        self.correlation_charts = CorrelationCharts()
        self.outlier_charts = OutlierCharts()
        self.insights_panel = InsightsPanel()
        
        # Add tabs with clean names
        self.tab_widget.addTab(self.create_tab_content(self.overview_charts), "Overview")
        self.tab_widget.addTab(self.create_tab_content(self.statistics_charts), "Statistics")
        self.tab_widget.addTab(self.create_tab_content(self.efficiency_charts), "Efficiency")
        self.tab_widget.addTab(self.create_tab_content(self.correlation_charts), "Correlations")
        self.tab_widget.addTab(self.create_tab_content(self.outlier_charts), "Outliers")
        self.tab_widget.addTab(self.create_tab_content(self.insights_panel), "Insights")
        
        layout.addWidget(self.tab_widget)
        
        # Initially hidden
        self.tab_widget.setVisible(False)
        
    def create_tab_content(self, widget):
        """Create scrollable tab content with proper spacing"""
        scroll_area = QScrollArea()
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {COLORS['background']};
            }}
            QScrollBar:vertical {{
                background-color: {COLORS['surface_variant']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {COLORS['border']};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {COLORS['text_disabled']};
            }}
        """)
        return scroll_area
        
    def create_no_data_state(self, layout):
        """Create professional no data state"""
        self.no_data_frame = QFrame()
        self.no_data_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 2px dashed {COLORS['border']};
                border-radius: 12px;
                margin: {SPACING['xxl']}px;
            }}
        """)
        
        no_data_layout = QVBoxLayout(self.no_data_frame)
        no_data_layout.setAlignment(Qt.AlignCenter)
        no_data_layout.setSpacing(SPACING['lg'])
        
        # Icon placeholder
        icon_label = QLabel("📊")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px; margin: 0;")
        
        # Title
        title_label = QLabel("No Analysis Data")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 20px;
                font-weight: 600;
                color: {COLORS['text_primary']};
                margin: 0;
            }}
        """)
        
        # Description
        self.desc_label = QLabel("Upload a CSV file to begin comprehensive equipment analysis")
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setStyleSheet(get_body_text_style())
        self.desc_label.setWordWrap(True)
        
        no_data_layout.addWidget(icon_label)
        no_data_layout.addWidget(title_label)
        no_data_layout.addWidget(self.desc_label)
        
        layout.addWidget(self.no_data_frame)
        
    def update_analysis(self, analysis_data):
        """Update dashboard with new analysis data"""
        self.current_analysis = analysis_data
        
        if not analysis_data or 'analysis_results' not in analysis_data:
            self.show_no_data()
            return
            
        # Hide no data and show analysis
        self.no_data_frame.setVisible(False)
        self.tab_widget.setVisible(True)
        
        # Enable PDF generation button
        self.pdf_button.setEnabled(True)
        
        # Update all chart widgets
        analysis_results = analysis_data['analysis_results']
        
        try:
            print("DEBUG: Updating dashboard components...")
            
            self.overview_charts.update_data(analysis_results)
            self.statistics_charts.update_data(analysis_results)
            self.efficiency_charts.update_data(analysis_results)
            self.correlation_charts.update_data(analysis_results)
            self.outlier_charts.update_data(analysis_results)
            self.insights_panel.update_data(analysis_results)
            
            # Switch to overview tab
            self.tab_widget.setCurrentIndex(0)
            print("DEBUG: Dashboard update completed successfully")
            
        except Exception as e:
            print(f"ERROR: Dashboard update failed: {e}")
            import traceback
            traceback.print_exc()
            self.show_error(f"Error displaying analysis: {str(e)}")
            
    def generate_pdf_report(self):
        """Generate PDF report - emit signal to main window"""
        self.pdf_generation_requested.emit()
            
    def show_no_data(self):
        """Show no data state"""
        self.no_data_frame.setVisible(True)
        self.tab_widget.setVisible(False)
        
        # Disable PDF generation button
        self.pdf_button.setEnabled(False)
        
        # Reset description
        self.desc_label.setText("Upload a CSV file to begin comprehensive equipment analysis")
        self.desc_label.setStyleSheet(get_body_text_style())
        
    def show_error(self, message):
        """Show error state"""
        self.no_data_frame.setVisible(True)
        self.tab_widget.setVisible(False)
        
        # Update description to show error
        self.desc_label.setText(f"Error: {message}")
        self.desc_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {COLORS['error']};
                text-align: center;
            }}
        """)
        
    def clear_data(self):
        """Clear all dashboard data"""
        self.current_analysis = None
        self.pdf_button.setEnabled(False)
        self.show_no_data()