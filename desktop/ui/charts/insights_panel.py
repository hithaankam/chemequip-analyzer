"""
Insights Panel - Professional card-based layout
Clean, modern analytics dashboard design
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt
import json

from ..design_system import (COLORS, SPACING, DIMENSIONS, CARD_STYLE,
                            get_section_title_style, get_card_title_style, 
                            get_body_text_style, get_caption_style)

class InsightsPanel(QWidget):
    """Professional insights panel with card-based layout"""
    
    def __init__(self):
        super().__init__()
        self.analysis_data = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize insights UI with professional layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        layout.setSpacing(SPACING['lg'])
        
        # Section header
        self.create_section_header(layout)
        
        # Scrollable insights area
        self.create_insights_area(layout)
        
        # Initially show no data message
        self.show_no_data_message()
        
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
        title_label = QLabel("Key Insights & Recommendations")
        title_label.setStyleSheet(get_section_title_style())
        
        # Description
        desc_label = QLabel("Comprehensive analysis findings and actionable recommendations")
        desc_label.setStyleSheet(get_body_text_style())
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        
        layout.addWidget(header_frame)
        
    def create_insights_area(self, layout):
        """Create scrollable insights area"""
        # Scrollable area for insights
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
        
        self.insights_widget = QWidget()
        self.insights_layout = QVBoxLayout(self.insights_widget)
        self.insights_layout.setSpacing(SPACING['lg'])
        
        scroll_area.setWidget(self.insights_widget)
        layout.addWidget(scroll_area)
        
    def update_data(self, analysis_results):
        """Update insights panel with new analysis data"""
        self.analysis_data = analysis_results
        
        # Clear existing widgets
        for i in reversed(range(self.insights_layout.count())): 
            child = self.insights_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Get insights data
        insights = analysis_results.get('comprehensive_insights', {})
        high_temp_analysis = analysis_results.get('high_temperature_analysis', {})
        
        if not insights and not high_temp_analysis:
            self.show_no_data_message()
            return
        
        # Create insight sections
        if insights.get('dataset_overview'):
            self.create_dataset_overview_section(insights['dataset_overview'])
            
        if insights.get('equipment_type_analysis'):
            self.create_equipment_type_analysis_section(insights['equipment_type_analysis'])
            
        if insights.get('high_performance_equipment'):
            self.create_high_performance_section(insights['high_performance_equipment'])
            
        if insights.get('recommendations'):
            self.create_recommendations_section(insights['recommendations'])
            
        if high_temp_analysis:
            self.create_high_temperature_section(high_temp_analysis)
            
        # Add performance insights
        self.create_performance_insights_section(analysis_results)
        
        # Add correlation insights
        self.create_correlation_insights_section(analysis_results)
        
        # Add efficiency insights
        self.create_efficiency_insights_section(analysis_results)
        
        # Add stretch to push content to top
        self.insights_layout.addStretch()
        
    def create_dataset_overview_section(self, dataset_overview):
        """Create dataset overview insight section"""
        section = self.create_insight_section("Dataset Overview", COLORS['primary'])
        
        total_equipment = dataset_overview.get('total_equipment', 0)
        equipment_types = dataset_overview.get('equipment_types', 0)
        
        overview_text = f"""
        <p><strong>Total Equipment:</strong> {total_equipment} units analyzed</p>
        <p><strong>Equipment Types:</strong> {equipment_types} different types identified</p>
        <p>This dataset provides a comprehensive view of chemical equipment performance 
        across multiple parameters including flowrate, pressure, and temperature.</p>
        """
        
        content_label = QLabel(overview_text)
        content_label.setWordWrap(True)
        content_label.setStyleSheet(get_body_text_style())
        section.layout().addWidget(content_label)
        
        self.insights_layout.addWidget(section)
        
    def create_equipment_type_analysis_section(self, type_analysis):
        """Create equipment type analysis section"""
        section = self.create_insight_section("Equipment Type Analysis", COLORS['info'])
        
        for equipment_type, analysis in type_analysis.items():
            if isinstance(analysis, dict):
                count = analysis.get('count', 0)
                performance_summary = analysis.get('performance_summary', 'No summary available')
                
                type_card = QFrame()
                type_card.setStyleSheet(f"""
                    QFrame {{
                        background-color: {COLORS['surface_variant']};
                        border-left: 4px solid {COLORS['info']};
                        padding: {SPACING['md']}px;
                        margin-bottom: {SPACING['sm']}px;
                        border-radius: 6px;
                    }}
                """)
                
                type_layout = QVBoxLayout(type_card)
                type_layout.setSpacing(SPACING['xs'])
                
                type_title = QLabel(f"{equipment_type} ({count} units)")
                type_title.setStyleSheet(f"""
                    QLabel {{
                        font-weight: bold;
                        color: {COLORS['text_primary']};
                        font-size: 14px;
                    }}
                """)
                type_layout.addWidget(type_title)
                
                summary_label = QLabel(performance_summary)
                summary_label.setWordWrap(True)
                summary_label.setStyleSheet(get_body_text_style())
                type_layout.addWidget(summary_label)
                
                section.layout().addWidget(type_card)
        
        self.insights_layout.addWidget(section)
        
    def create_high_performance_section(self, high_performance):
        """Create high performance equipment section"""
        section = self.create_insight_section("High-Performance Equipment", COLORS['success'])
        
        best_performer = high_performance.get('best_performer', {})
        if best_performer:
            equipment_name = best_performer.get('equipment_name', 'Unknown')
            equipment_type = best_performer.get('type', 'Unknown')
            efficiency_score = best_performer.get('efficiency_score', 0)
            
            performance_text = f"""
            <p><strong>Best Performer:</strong> {equipment_name} ({equipment_type})</p>
            <p><strong>Efficiency Score:</strong> {efficiency_score:.3f}</p>
            <p>This equipment demonstrates optimal performance across all measured parameters 
            and serves as a benchmark for similar equipment types.</p>
            """
            
            content_label = QLabel(performance_text)
            content_label.setWordWrap(True)
            content_label.setStyleSheet(get_body_text_style())
            section.layout().addWidget(content_label)
        
        self.insights_layout.addWidget(section)
        
    def create_recommendations_section(self, recommendations):
        """Create recommendations section"""
        section = self.create_insight_section("Recommendations", COLORS['warning'])
        
        if isinstance(recommendations, list):
            for i, recommendation in enumerate(recommendations, 1):
                rec_card = QFrame()
                rec_card.setStyleSheet(f"""
                    QFrame {{
                        background-color: {COLORS['surface_variant']};
                        border: 1px solid {COLORS['border_light']};
                        border-radius: 6px;
                        padding: {SPACING['md']}px;
                        margin-bottom: {SPACING['sm']}px;
                    }}
                """)
                
                rec_layout = QVBoxLayout(rec_card)
                
                rec_label = QLabel(f"{i}. {recommendation}")
                rec_label.setWordWrap(True)
                rec_label.setStyleSheet(get_body_text_style())
                rec_layout.addWidget(rec_label)
                
                section.layout().addWidget(rec_card)
        
        self.insights_layout.addWidget(section)
        
    def create_high_temperature_section(self, high_temp_analysis):
        """Create high temperature analysis section"""
        section = self.create_insight_section("High Temperature Analysis", COLORS['error'])
        
        threshold = high_temp_analysis.get('threshold', 0)
        count = high_temp_analysis.get('count', 0)
        percentage = high_temp_analysis.get('percentage', 0)
        temp_stats = high_temp_analysis.get('temperature_stats', {})
        
        min_temp = temp_stats.get('min', 0)
        max_temp = temp_stats.get('max', 0)
        
        temp_text = f"""
        <p><strong>High Temperature Equipment:</strong> {count} units operating above {threshold}°</p>
        <p><strong>Percentage:</strong> {percentage:.1f}% of total equipment</p>
        <p><strong>Temperature Range:</strong> {min_temp:.1f}° - {max_temp:.1f}°</p>
        <p>Equipment operating at high temperatures may require additional monitoring 
        and maintenance to ensure optimal performance and safety.</p>
        """
        
        content_label = QLabel(temp_text)
        content_label.setWordWrap(True)
        content_label.setStyleSheet(get_body_text_style())
        section.layout().addWidget(content_label)
        
        self.insights_layout.addWidget(section)
        
    def create_performance_insights_section(self, analysis_results):
        """Create performance insights section"""
        section = self.create_insight_section("Performance Insights", COLORS['primary'])
        
        # Get efficiency data
        efficiency = analysis_results.get('efficiency', {})
        rankings = efficiency.get('rankings', {}).get('overall_efficiency', [])
        
        if rankings:
            top_performers = rankings[:3]
            bottom_performers = rankings[-3:]
            
            # Top performers card
            top_card = QFrame()
            top_card.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['surface_variant']};
                    border: 1px solid {COLORS['border_light']};
                    border-radius: 6px;
                    padding: {SPACING['md']}px;
                    margin-bottom: {SPACING['sm']}px;
                }}
            """)
            
            top_layout = QVBoxLayout(top_card)
            
            top_title = QLabel("Top Performers:")
            top_title.setStyleSheet(f"""
                QLabel {{
                    font-weight: bold;
                    color: {COLORS['text_primary']};
                    margin-bottom: {SPACING['xs']}px;
                }}
            """)
            top_layout.addWidget(top_title)
            
            for i, performer in enumerate(top_performers, 1):
                name = performer.get('equipment_name', 'Unknown')
                score = performer.get('efficiency_score', 0)
                perf_label = QLabel(f"{i}. {name}: {score:.3f}")
                perf_label.setStyleSheet(get_body_text_style())
                top_layout.addWidget(perf_label)
            
            section.layout().addWidget(top_card)
            
            # Improvement opportunities
            if bottom_performers:
                improvement_text = f"""
                <p><strong>Areas for Improvement:</strong></p>
                <p>The bottom {len(bottom_performers)} performers show efficiency scores below 
                {bottom_performers[0].get('efficiency_score', 0):.3f}, indicating potential 
                for optimization through maintenance or operational adjustments.</p>
                """
                
                improvement_label = QLabel(improvement_text)
                improvement_label.setWordWrap(True)
                improvement_label.setStyleSheet(get_body_text_style())
                section.layout().addWidget(improvement_label)
        
        self.insights_layout.addWidget(section)
        
    def create_correlation_insights_section(self, analysis_results):
        """Create correlation insights section"""
        section = self.create_insight_section("Parameter Correlations", COLORS['info'])
        
        correlations = analysis_results.get('correlations', {})
        key_correlations = correlations.get('key_correlations', {})
        
        if key_correlations:
            flowrate_temp = key_correlations.get('flowrate_temperature', 0)
            flowrate_pressure = key_correlations.get('flowrate_pressure', 0)
            pressure_temp = key_correlations.get('pressure_temperature', 0)
            
            # Correlations grid
            corr_frame = QFrame()
            corr_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['surface_variant']};
                    border: 1px solid {COLORS['border_light']};
                    border-radius: 6px;
                    padding: {SPACING['md']}px;
                    margin-bottom: {SPACING['sm']}px;
                }}
            """)
            
            corr_layout = QVBoxLayout(corr_frame)
            
            corr_title = QLabel("Key Correlations Identified:")
            corr_title.setStyleSheet(f"""
                QLabel {{
                    font-weight: bold;
                    color: {COLORS['text_primary']};
                    margin-bottom: {SPACING['xs']}px;
                }}
            """)
            corr_layout.addWidget(corr_title)
            
            correlations_text = f"""
            <p>• Flowrate-Temperature: {flowrate_temp:.3f} ({self.interpret_correlation(flowrate_temp)})</p>
            <p>• Flowrate-Pressure: {flowrate_pressure:.3f} ({self.interpret_correlation(flowrate_pressure)})</p>
            <p>• Pressure-Temperature: {pressure_temp:.3f} ({self.interpret_correlation(pressure_temp)})</p>
            """
            
            corr_label = QLabel(correlations_text)
            corr_label.setWordWrap(True)
            corr_label.setStyleSheet(get_body_text_style())
            corr_layout.addWidget(corr_label)
            
            section.layout().addWidget(corr_frame)
            
            # Operational implications
            implications_text = "<p><strong>Operational Implications:</strong></p>"
            
            if abs(flowrate_temp) > 0.5:
                implications_text += "<p>• Strong flowrate-temperature relationship suggests thermal efficiency considerations</p>"
            if abs(flowrate_pressure) > 0.5:
                implications_text += "<p>• Significant flowrate-pressure correlation indicates hydraulic system interdependencies</p>"
            if abs(pressure_temp) > 0.5:
                implications_text += "<p>• Pressure-temperature correlation suggests thermodynamic relationships</p>"
            
            if len(implications_text) > len("<p><strong>Operational Implications:</strong></p>"):
                implications_label = QLabel(implications_text)
                implications_label.setWordWrap(True)
                implications_label.setStyleSheet(get_body_text_style())
                section.layout().addWidget(implications_label)
        
        self.insights_layout.addWidget(section)
        
    def create_efficiency_insights_section(self, analysis_results):
        """Create efficiency insights section"""
        section = self.create_insight_section("Efficiency Analysis", COLORS['success'])
        
        efficiency = analysis_results.get('efficiency', {})
        by_type = efficiency.get('by_type', {})
        
        if by_type:
            # Sort types by mean efficiency
            sorted_types = sorted(by_type.items(), 
                                key=lambda x: x[1].get('efficiency_metrics', {}).get('overall_efficiency', {}).get('mean', 0), 
                                reverse=True)
            
            for equipment_type, stats in sorted_types:
                count = stats.get('count', 0)
                mean_eff = stats.get('efficiency_metrics', {}).get('overall_efficiency', {}).get('mean', 0)
                top_performer = stats.get('top_performer', {})
                
                type_card = QFrame()
                type_card.setStyleSheet(f"""
                    QFrame {{
                        background-color: {COLORS['surface_variant']};
                        border: 1px solid {COLORS['border_light']};
                        border-radius: 6px;
                        padding: {SPACING['md']}px;
                        margin-bottom: {SPACING['sm']}px;
                    }}
                """)
                
                type_layout = QVBoxLayout(type_card)
                
                type_title = QLabel(f"{equipment_type} ({count} units)")
                type_title.setStyleSheet(f"""
                    QLabel {{
                        font-weight: bold;
                        color: {COLORS['text_primary']};
                        font-size: 14px;
                        margin-bottom: {SPACING['xs']}px;
                    }}
                """)
                type_layout.addWidget(type_title)
                
                eff_text = f"Average efficiency: {mean_eff:.3f}"
                if top_performer:
                    top_name = top_performer.get('equipment_name', 'Unknown')
                    top_score = top_performer.get('efficiency_score', 0)
                    eff_text += f"<br>Best performer: {top_name} ({top_score:.3f})"
                
                eff_label = QLabel(eff_text)
                eff_label.setWordWrap(True)
                eff_label.setStyleSheet(get_body_text_style())
                type_layout.addWidget(eff_label)
                
                section.layout().addWidget(type_card)
        
        self.insights_layout.addWidget(section)
        
    def create_insight_section(self, title, accent_color):
        """Create a professional insight section"""
        section = QFrame()
        section.setStyleSheet(CARD_STYLE)
        
        layout = QVBoxLayout(section)
        layout.setSpacing(SPACING['md'])
        
        # Section header with accent color
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: transparent;
                border-bottom: 2px solid {accent_color};
                padding-bottom: {SPACING['sm']}px;
                margin-bottom: {SPACING['md']}px;
            }}
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(get_card_title_style())
        header_layout.addWidget(title_label)
        
        layout.addWidget(header_frame)
        
        return section
        
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
        no_data_frame = QFrame()
        no_data_frame.setStyleSheet(CARD_STYLE)
        
        no_data_layout = QVBoxLayout(no_data_frame)
        no_data_layout.setAlignment(Qt.AlignCenter)
        
        no_data_label = QLabel("No insights data available")
        no_data_label.setAlignment(Qt.AlignCenter)
        no_data_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_disabled']};
                font-size: 18px;
                font-weight: 500;
                margin: {SPACING['xl']}px;
            }}
        """)
        
        desc_label = QLabel("Please upload and analyze a dataset to view comprehensive insights.")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(get_body_text_style())
        
        no_data_layout.addWidget(no_data_label)
        no_data_layout.addWidget(desc_label)
        
        self.insights_layout.addWidget(no_data_frame)