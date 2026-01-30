"""
File Upload Widget - Replicates React frontend file upload functionality
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QProgressBar, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
import os

from .design_system import COLORS, SPACING, TYPOGRAPHY

class UploadWorker(QThread):
    """Worker thread for file upload to prevent UI blocking"""
    progress = pyqtSignal(int)
    success = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
        
    def run(self):
        try:
            self.progress.emit(25)
            result = self.api_client.upload_and_analyze(self.file_path)
            self.progress.emit(100)
            self.success.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class UploadWidget(QWidget):
    """File upload widget matching React frontend upload functionality"""
    
    analysis_completed = pyqtSignal(dict)
    status_message = pyqtSignal(str)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.selected_file = None
        self.upload_worker = None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize upload widget UI with professional styling"""
        layout = QVBoxLayout(self)
        layout.setSpacing(SPACING['lg'])
        layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        
        # Title - Fix typo and improve typography
        title_label = QLabel("Upload Chemical Equipment Data")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_primary']};
                font-size: 20px;
                font-weight: 600;
                margin: {SPACING['md']}px 0;
                padding: {SPACING['lg']}px;
                background-color: {COLORS['surface']};
                border-radius: 8px;
                border-left: 4px solid {COLORS['primary']};
            }}
        """)
        layout.addWidget(title_label)
        
        # Upload area
        self.create_upload_area(layout)
        
        # File info with better styling
        self.file_info_label = QLabel("No file selected")
        self.file_info_label.setAlignment(Qt.AlignCenter)
        self.file_info_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_disabled']};
                font-style: italic;
                font-size: {TYPOGRAPHY['body']['size']}px;
                margin: {SPACING['md']}px 0;
                padding: {SPACING['md']}px;
                background-color: {COLORS['surface_variant']};
                border-radius: 6px;
            }}
        """)
        layout.addWidget(self.file_info_label)
        
        # Upload button container with improved styling
        self.create_upload_button_section(layout)
        
        # Progress bar with professional styling
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {COLORS['border']};
                border-radius: 6px;
                text-align: center;
                font-weight: 500;
                color: {COLORS['text_primary']};
                background-color: {COLORS['surface']};
                min-height: 24px;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['primary']};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.progress_bar)
        
        # Status label with better styling
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(f"""
            QLabel {{
                font-size: {TYPOGRAPHY['body']['size']}px;
                font-weight: 500;
                margin: {SPACING['sm']}px 0;
                padding: {SPACING['sm']}px;
            }}
        """)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
    def create_upload_area(self, layout):
        """Create professional drag-and-drop upload area"""
        upload_frame = QFrame()
        upload_frame.setFrameStyle(QFrame.Box)
        upload_frame.setStyleSheet(f"""
            QFrame {{
                border: 2px dashed {COLORS['border']};
                border-radius: 8px;
                background-color: {COLORS['surface_variant']};
                min-height: 180px;
            }}
            QFrame:hover {{
                border-color: {COLORS['primary']};
                background-color: {COLORS['surface']};
            }}
        """)
        upload_frame.setAcceptDrops(True)
        
        frame_layout = QVBoxLayout(upload_frame)
        frame_layout.setAlignment(Qt.AlignCenter)
        frame_layout.setSpacing(SPACING['md'])
        
        # Upload icon
        icon_label = QLabel("📁")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 42px; margin-bottom: 8px;")
        frame_layout.addWidget(icon_label)
        
        # Instructions with better typography
        instruction_label = QLabel("Drop CSV file here or click to browse")
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet(f"""
            QLabel {{
                font-size: {TYPOGRAPHY['body']['size']}px;
                color: {COLORS['text_secondary']};
                font-weight: 500;
                margin-bottom: {SPACING['sm']}px;
            }}
        """)
        frame_layout.addWidget(instruction_label)
        
        # Browse button with professional styling
        browse_button = QPushButton("Browse Files")
        browse_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['surface']};
                border: 2px solid {COLORS['primary']};
                color: {COLORS['primary']};
                padding: {SPACING['sm']}px {SPACING['lg']}px;
                border-radius: 6px;
                font-weight: 600;
                font-size: {TYPOGRAPHY['body']['size']}px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary']};
                color: white;
            }}
            QPushButton:pressed {{
                background-color: {COLORS['primary_dark']};
                color: white;
            }}
        """)
        browse_button.clicked.connect(self.browse_file)
        frame_layout.addWidget(browse_button)
        
        # File requirements with better styling
        req_label = QLabel("Supported: CSV files up to 10MB")
        req_label.setAlignment(Qt.AlignCenter)
        req_label.setStyleSheet(f"""
            QLabel {{
                font-size: {TYPOGRAPHY['caption']['size']}px;
                color: {COLORS['text_disabled']};
                margin-top: {SPACING['sm']}px;
            }}
        """)
        frame_layout.addWidget(req_label)
        
        layout.addWidget(upload_frame)
        
        # Enable drag and drop
        upload_frame.dragEnterEvent = self.drag_enter_event
        upload_frame.dropEvent = self.drop_event
        
    def create_upload_button_section(self, layout):
        """Create professional upload button section"""
        button_container = QFrame()
        button_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: {SPACING['lg']}px;
                margin: {SPACING['sm']}px 0;
            }}
        """)
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(SPACING['md'])
        
        # Upload button with professional styling
        self.upload_button = QPushButton("🚀 Upload & Analyze Dataset")
        self.upload_button.setEnabled(False)
        self.upload_button.setMinimumHeight(50)
        self.upload_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                padding: {SPACING['lg']}px {SPACING['xl']}px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                margin: {SPACING['xs']}px 0;
            }}
            QPushButton:hover:enabled {{
                background-color: {COLORS['primary_light']};
            }}
            QPushButton:pressed:enabled {{
                background-color: {COLORS['primary_dark']};
            }}
            QPushButton:disabled {{
                background-color: {COLORS['border']};
                color: {COLORS['text_disabled']};
            }}
        """)
        self.upload_button.clicked.connect(self.handle_upload)
        button_layout.addWidget(self.upload_button)
        
        # Status label with better styling
        self.button_status_label = QLabel("Select a CSV file to enable the analyze button")
        self.button_status_label.setAlignment(Qt.AlignCenter)
        self.button_status_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_disabled']};
                font-style: italic;
                font-size: {TYPOGRAPHY['caption']['size']}px;
                margin: {SPACING['sm']}px 0;
                padding: {SPACING['sm']}px;
            }}
        """)
        button_layout.addWidget(self.button_status_label)
        
        layout.addWidget(button_container)
        
    def browse_file(self):
        """Open file browser dialog"""
        print("DEBUG: Opening file dialog...")  # Debug line
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select CSV File", 
            "", 
            "CSV Files (*.csv);;All Files (*)"
        )
        
        print(f"DEBUG: File dialog returned: {file_path}")  # Debug line
        if file_path:
            self.set_selected_file(file_path)
            
    def drag_enter_event(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) == 1 and urls[0].toLocalFile().endswith('.csv'):
                event.acceptProposedAction()
                
    def drop_event(self, event: QDropEvent):
        """Handle file drop event"""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.endswith('.csv'):
                self.set_selected_file(file_path)
                event.acceptProposedAction()
                
    def set_selected_file(self, file_path):
        """Set the selected file and update UI with professional styling"""
        print(f"DEBUG: Setting selected file: {file_path}")
        self.selected_file = file_path
        
        # Get file info
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_size_kb = file_size / 1024
        
        # Update UI with success styling
        self.file_info_label.setText(f"✅ Selected: {file_name} ({file_size_kb:.1f} KB)")
        self.file_info_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['success']};
                font-weight: 600;
                font-style: normal;
                font-size: {TYPOGRAPHY['body']['size']}px;
                margin: {SPACING['md']}px 0;
                padding: {SPACING['md']}px;
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['success']};
                border-radius: 6px;
            }}
        """)
        
        self.upload_button.setEnabled(True)
        self.button_status_label.setText("✅ Ready to analyze! Click the button above.")
        self.button_status_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['success']};
                font-weight: 600;
                font-style: normal;
                font-size: {TYPOGRAPHY['caption']['size']}px;
                margin: {SPACING['sm']}px 0;
                padding: {SPACING['sm']}px;
            }}
        """)
        print(f"DEBUG: Upload button enabled: {self.upload_button.isEnabled()}")
        
        # Validate file size
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            self.show_error("File size exceeds 10MB limit")
            self.upload_button.setEnabled(False)
            self.button_status_label.setText("❌ File too large (max 10MB)")
            self.button_status_label.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['error']};
                    font-weight: 600;
                    font-style: normal;
                    font-size: {TYPOGRAPHY['caption']['size']}px;
                    margin: {SPACING['sm']}px 0;
                    padding: {SPACING['sm']}px;
                }}
            """)
            print("DEBUG: Upload button disabled due to file size")
            
    def handle_upload(self):
        """Handle file upload and analysis"""
        print("DEBUG: Handle upload called")  # Debug line
        if not self.selected_file:
            self.show_error("Please select a file first")
            print("DEBUG: No file selected")  # Debug line
            return
            
        if not self.api_client.token:
            self.show_error("Please login first")
            print("DEBUG: No authentication token")  # Debug line
            return
            
        print(f"DEBUG: Starting upload of {self.selected_file}")  # Debug line
        # Start upload
        self.set_uploading(True)
        self.status_label.setText("Uploading and analyzing file...")
        self.status_message.emit("Processing file upload...")
        
        self.upload_worker = UploadWorker(self.api_client, self.selected_file)
        self.upload_worker.progress.connect(self.progress_bar.setValue)
        self.upload_worker.success.connect(self.on_upload_success)
        self.upload_worker.error.connect(self.on_upload_error)
        self.upload_worker.start()
        print("DEBUG: Upload worker started")  # Debug line
        
    def on_upload_success(self, result):
        """Handle successful upload with professional feedback"""
        self.set_uploading(False)
        self.status_label.setText("✅ Analysis completed successfully!")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['success']};
                font-weight: 600;
                font-size: {TYPOGRAPHY['body']['size']}px;
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['success']};
                border-radius: 6px;
                padding: {SPACING['md']}px;
            }}
        """)
        self.status_message.emit("Analysis completed successfully")
        
        # Emit analysis completed signal
        self.analysis_completed.emit(result)
        
        # Reset for next upload after a brief delay
        self.reset_upload()
        
    def on_upload_error(self, error_message):
        """Handle upload error with professional feedback"""
        self.set_uploading(False)
        self.show_error(f"Upload failed: {error_message}")
        self.status_message.emit("Upload failed")
        
    def show_error(self, message):
        """Show error message with professional styling"""
        self.status_label.setText(f"❌ {message}")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['error']};
                font-weight: 600;
                font-size: {TYPOGRAPHY['body']['size']}px;
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['error']};
                border-radius: 6px;
                padding: {SPACING['md']}px;
            }}
        """)
        
    def reset_upload(self):
        """Reset upload widget for next file with professional styling"""
        self.selected_file = None
        self.file_info_label.setText("No file selected")
        self.file_info_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_disabled']};
                font-style: italic;
                font-size: {TYPOGRAPHY['body']['size']}px;
                margin: {SPACING['md']}px 0;
                padding: {SPACING['md']}px;
                background-color: {COLORS['surface_variant']};
                border-radius: 6px;
            }}
        """)
        self.upload_button.setEnabled(False)
        self.button_status_label.setText("Select a CSV file to enable the analyze button")
        self.button_status_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_disabled']};
                font-style: italic;
                font-size: {TYPOGRAPHY['caption']['size']}px;
                margin: {SPACING['sm']}px 0;
                padding: {SPACING['sm']}px;
            }}
        """)
        
        # Clear status message
        self.status_label.setText("")
        
    def set_uploading(self, uploading):
        """Set uploading state and update UI accordingly"""
        self.upload_button.setEnabled(not uploading)
        self.progress_bar.setVisible(uploading)
        
        if uploading:
            self.upload_button.setText("🔄 Analyzing...")
        else:
            self.upload_button.setText("🚀 Upload & Analyze Dataset")
            self.progress_bar.setValue(0)