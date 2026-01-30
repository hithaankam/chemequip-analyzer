"""
Main Window for Chemical Equipment Analyzer Desktop Application
Professional dashboard-style interface inspired by Material UI/Ant Design
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QLabel, QStatusBar, QMenuBar, QAction,
                             QMessageBox, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

from .auth_dialog import AuthDialog
from .upload_widget import UploadWidget
from .dashboard_widget import DashboardWidget
from .history_widget import HistoryWidget
from .design_system import COLORS, SPACING, DIMENSIONS, TAB_STYLE, TYPOGRAPHY
from api.client import APIClient
from config import APP_TITLE, WINDOW_SIZE, MIN_WINDOW_SIZE

class MainWindow(QMainWindow):
    """Main application window with professional dashboard design"""
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.current_user = None
        self.current_analysis = None
        
        self.init_ui()
        self.setup_connections()
        self.check_authentication()
        
    def init_ui(self):
        """Initialize the user interface with dashboard design"""
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, *WINDOW_SIZE)
        self.setMinimumSize(*MIN_WINDOW_SIZE)
        
        # Set global application style
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLORS['background']};
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }}
            {TAB_STYLE}
        """)
        
        # Create main container with max width constraint
        main_container = QWidget()
        self.setCentralWidget(main_container)
        
        # Center layout with max width
        center_layout = QHBoxLayout(main_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        
        # Content widget with max width
        content_widget = QWidget()
        content_widget.setMaximumWidth(DIMENSIONS['container_max_width'])
        content_widget.setStyleSheet(f"background-color: {COLORS['background']};")
        
        # Main content layout
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        layout.setSpacing(SPACING['lg'])
        
        # Header
        self.create_header(layout)
        
        # Main tabs
        self.create_main_tabs(layout)
        
        # Center the content widget
        center_layout.addStretch()
        center_layout.addWidget(content_widget)
        center_layout.addStretch()
        
        # Status bar
        self.create_status_bar()
        
        # Menu bar
        self.create_menu_bar()
        
    def create_header(self, layout):
        """Create clean, professional header"""
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: {SPACING['lg']}px;
            }}
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title section
        title_section = QVBoxLayout()
        title_section.setSpacing(SPACING['xs'])
        
        title_label = QLabel(APP_TITLE)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: {TYPOGRAPHY['page_title']['size']}px;
                font-weight: {TYPOGRAPHY['page_title']['weight']};
                color: {TYPOGRAPHY['page_title']['color']};
                margin: 0;
            }}
        """)
        
        subtitle_label = QLabel("Professional Equipment Parameter Analysis")
        subtitle_label.setStyleSheet(f"""
            QLabel {{
                font-size: {TYPOGRAPHY['body']['size']}px;
                color: {TYPOGRAPHY['body']['color']};
                margin: 0;
            }}
        """)
        
        title_section.addWidget(title_label)
        title_section.addWidget(subtitle_label)
        
        # User info with proper padding and margin
        self.user_label = QLabel("Not logged in")
        self.user_label.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['surface_variant']};
                color: {COLORS['text_secondary']};
                padding: {SPACING['md']}px {SPACING['lg']}px;
                margin: 0 {SPACING['md']}px 0 0;
                border-radius: 20px;
                font-size: {TYPOGRAPHY['body']['size']}px;
                font-weight: 500;
                min-width: 120px;
            }}
        """)
        
        header_layout.addLayout(title_section)
        header_layout.addStretch()
        header_layout.addWidget(self.user_label)
        
        layout.addWidget(header_frame)
        
    def create_main_tabs(self, layout):
        """Create main application tabs"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        
        # Create tab widgets
        self.upload_widget = UploadWidget(self.api_client)
        self.dashboard_widget = DashboardWidget()
        self.history_widget = HistoryWidget(self.api_client)
        
        # Add tabs with clean icons
        self.tab_widget.addTab(self.upload_widget, "Upload")
        self.tab_widget.addTab(self.dashboard_widget, "Dashboard")
        self.tab_widget.addTab(self.history_widget, "History")
        
        layout.addWidget(self.tab_widget)
        
    def create_status_bar(self):
        """Create clean status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {COLORS['surface']};
                border-top: 1px solid {COLORS['border']};
                padding: {SPACING['sm']}px;
                color: {COLORS['text_secondary']};
            }}
        """)
        
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {COLORS['surface']};
                border-bottom: 1px solid {COLORS['border']};
                padding: {SPACING['xs']}px;
            }}
            QMenuBar::item {{
                padding: {SPACING['sm']}px {SPACING['md']}px;
                color: {COLORS['text_primary']};
            }}
            QMenuBar::item:selected {{
                background-color: {COLORS['surface_variant']};
            }}
        """)
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        login_action = QAction('Login', self)
        login_action.triggered.connect(self.show_login_dialog)
        file_menu.addAction(login_action)
        
        logout_action = QAction('Logout', self)
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)
        
        file_menu.addSeparator()
        
        # PDF generation action
        self.pdf_action = QAction('Generate PDF Report', self)
        self.pdf_action.triggered.connect(self.generate_pdf_report)
        self.pdf_action.setEnabled(False)  # Initially disabled
        file_menu.addAction(self.pdf_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_connections(self):
        """Setup signal connections between widgets"""
        # Upload widget signals
        self.upload_widget.analysis_completed.connect(self.on_analysis_completed)
        self.upload_widget.status_message.connect(self.status_bar.showMessage)
        
        # History widget signals  
        self.history_widget.dataset_selected.connect(self.on_dataset_selected)
        
        # Dashboard widget signals
        self.dashboard_widget.pdf_generation_requested.connect(self.generate_pdf_report)
        
    def check_authentication(self):
        """Check if user is already authenticated"""
        if not self.api_client.test_connection():
            self.show_styled_message("Connection Error", 
                                   "Cannot connect to backend API. Please ensure the Django server is running.",
                                   "warning")
            return
            
        if not self.current_user:
            self.show_login_dialog()
            
    def show_login_dialog(self):
        """Show login/register dialog"""
        dialog = AuthDialog(self.api_client, self)
        if dialog.exec_() == AuthDialog.Accepted:
            self.current_user = self.api_client.user
            self.update_user_display()
            self.history_widget.refresh_history()
            
    def logout(self):
        """Logout current user"""
        self.api_client.clear_auth()
        self.current_user = None
        self.current_analysis = None
        self.update_user_display()
        self.dashboard_widget.clear_data()
        self.show_login_dialog()
        
    def update_user_display(self):
        """Update user information display with consistent styling"""
        if self.current_user:
            self.user_label.setText(f"Welcome, {self.current_user['username']}")
            self.user_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {COLORS['primary']};
                    color: white;
                    padding: {SPACING['md']}px {SPACING['lg']}px;
                    margin: 0 {SPACING['md']}px 0 0;
                    border-radius: 20px;
                    font-size: {TYPOGRAPHY['body']['size']}px;
                    font-weight: 600;
                    min-width: 120px;
                }}
            """)
        else:
            self.user_label.setText("Not logged in")
            self.user_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {COLORS['surface_variant']};
                    color: {COLORS['text_secondary']};
                    padding: {SPACING['md']}px {SPACING['lg']}px;
                    margin: 0 {SPACING['md']}px 0 0;
                    border-radius: 20px;
                    font-size: {TYPOGRAPHY['body']['size']}px;
                    font-weight: 500;
                    min-width: 120px;
                }}
            """)
            
    def on_analysis_completed(self, analysis_data):
        """Handle completed analysis from upload widget"""
        self.current_analysis = analysis_data
        self.dashboard_widget.update_analysis(analysis_data)
        self.tab_widget.setCurrentIndex(1)  # Switch to dashboard tab
        self.history_widget.refresh_history()
        
        # Enable PDF generation
        self.pdf_action.setEnabled(True)
        
    def on_dataset_selected(self, dataset_data):
        """Handle dataset selection from history"""
        self.current_analysis = dataset_data
        self.dashboard_widget.update_analysis(dataset_data)
        self.tab_widget.setCurrentIndex(1)  # Switch to dashboard tab
        
        # Enable PDF generation
        self.pdf_action.setEnabled(True)
        
    def generate_pdf_report(self):
        """Generate and save PDF report"""
        if not self.current_analysis:
            self.show_styled_message("No Data", "No analysis data available for PDF generation.", "warning")
            return
            
        if not self.api_client.token:
            self.show_styled_message("Authentication Required", "Please login to generate PDF reports.", "warning")
            return
        
        try:
            # Show progress dialog
            from PyQt5.QtWidgets import QProgressDialog
            from PyQt5.QtCore import QTimer
            
            progress = QProgressDialog("Generating PDF report...", "Cancel", 0, 0, self)
            progress.setWindowTitle("PDF Generation")
            progress.setModal(True)
            progress.show()
            
            # Get analysis results
            analysis_results = self.current_analysis.get('analysis_results', {})
            dataset_info = {
                'filename': 'equipment_data.csv',  # You can enhance this to get actual filename
                'upload_date': self.current_analysis.get('upload_date', ''),
                'equipment_count': analysis_results.get('summary_metrics', {}).get('dataset_overview', {}).get('total_equipment_count', 0)
            }
            
            # Generate PDF
            pdf_content = self.api_client.generate_pdf_report(analysis_results, dataset_info)
            
            # Save PDF file
            from PyQt5.QtWidgets import QFileDialog
            import os
            from datetime import datetime
            
            default_filename = f"equipment_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save PDF Report",
                default_filename,
                "PDF Files (*.pdf);;All Files (*)"
            )
            
            progress.close()
            
            if file_path:
                with open(file_path, 'wb') as f:
                    f.write(pdf_content)
                
                self.show_styled_message("Success", f"PDF report saved successfully to:\n{file_path}", "info")
                
                # Ask if user wants to open the PDF
                from PyQt5.QtWidgets import QMessageBox
                reply = QMessageBox.question(
                    self, 
                    'Open PDF', 
                    'Would you like to open the PDF report now?',
                    QMessageBox.Yes | QMessageBox.No, 
                    QMessageBox.Yes
                )
                
                if reply == QMessageBox.Yes:
                    import subprocess
                    import platform
                    
                    if platform.system() == 'Windows':
                        os.startfile(file_path)
                    elif platform.system() == 'Darwin':  # macOS
                        subprocess.call(['open', file_path])
                    else:  # Linux
                        subprocess.call(['xdg-open', file_path])
            
        except Exception as e:
            progress.close() if 'progress' in locals() else None
            self.show_styled_message("Error", f"Failed to generate PDF report:\n{str(e)}", "error")
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About", 
                         f"{APP_TITLE}\n\n"
                         "Professional desktop application for chemical equipment analysis.\n"
                         "Built with PyQt5 + Matplotlib, consuming Django REST API.")
        
    def closeEvent(self, event):
        """Handle application close event"""
        reply = QMessageBox.question(self, 'Exit Application', 
                                   'Are you sure you want to exit?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()