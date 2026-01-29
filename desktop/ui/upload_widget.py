"""
File Upload Widget - Replicates React frontend file upload functionality
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QProgressBar, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
import os

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
        """Initialize upload widget UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Upload Chemical Equipment Data")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #333;
                margin: 20px;
                padding: 15px;
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }
        """)
        layout.addWidget(title_label)
        
        # Upload area
        self.create_upload_area(layout)
        
        # File info
        self.file_info_label = QLabel("No file selected")
        self.file_info_label.setAlignment(Qt.AlignCenter)
        self.file_info_label.setStyleSheet("""
            QLabel {
                color: #666; 
                font-style: italic; 
                font-size: 14px;
                margin: 15px;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.file_info_label)
        
        # Upload button - Make it more visible and always show
        button_container = QFrame()
        button_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
            }
        """)
        button_layout = QVBoxLayout(button_container)
        
        self.upload_button = QPushButton("🚀 Upload & Analyze Dataset")
        self.upload_button.setEnabled(False)
        self.upload_button.setMinimumHeight(60)  # Make it taller
        self.upload_button.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: 2px solid #5a6fd8;
                padding: 20px 40px;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover:enabled {
                background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
                border-color: #4c63d2;
                transform: translateY(-2px);
            }
            QPushButton:disabled {
                background: #e9ecef;
                color: #6c757d;
                border: 2px solid #dee2e6;
            }
            QPushButton:pressed:enabled {
                background: linear-gradient(135deg, #4c63d2 0%, #5a4180 100%);
            }
        """)
        self.upload_button.clicked.connect(self.handle_upload)
        button_layout.addWidget(self.upload_button)
        
        # Add a label to show button status
        self.button_status_label = QLabel("Select a CSV file to enable the analyze button")
        self.button_status_label.setAlignment(Qt.AlignCenter)
        self.button_status_label.setStyleSheet("""
            QLabel {
                color: #666; 
                font-style: italic; 
                font-size: 14px;
                margin: 10px;
                padding: 10px;
            }
        """)
        button_layout.addWidget(self.button_status_label)
        
        layout.addWidget(button_container)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #667eea;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
    def create_upload_area(self, layout):
        """Create drag-and-drop upload area"""
        upload_frame = QFrame()
        upload_frame.setFrameStyle(QFrame.Box)
        upload_frame.setStyleSheet("""
            QFrame {
                border: 2px dashed #ddd;
                border-radius: 10px;
                background-color: #f8f9fa;
                min-height: 200px;
            }
            QFrame:hover {
                border-color: #667eea;
                background-color: #f0f4ff;
            }
        """)
        upload_frame.setAcceptDrops(True)
        
        frame_layout = QVBoxLayout(upload_frame)
        frame_layout.setAlignment(Qt.AlignCenter)
        
        # Upload icon (text-based)
        icon_label = QLabel("📁")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px; margin-bottom: 10px;")
        frame_layout.addWidget(icon_label)
        
        # Instructions
        instruction_label = QLabel("Drop CSV file here or click to browse")
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("font-size: 16px; color: #666; margin-bottom: 10px;")
        frame_layout.addWidget(instruction_label)
        
        # Browse button
        browse_button = QPushButton("Browse Files")
        browse_button.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 2px solid #667eea;
                color: #667eea;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #667eea;
                color: white;
            }
        """)
        browse_button.clicked.connect(self.browse_file)
        frame_layout.addWidget(browse_button)
        
        # File requirements
        req_label = QLabel("Supported: CSV files up to 10MB")
        req_label.setAlignment(Qt.AlignCenter)
        req_label.setStyleSheet("font-size: 12px; color: #999; margin-top: 10px;")
        frame_layout.addWidget(req_label)
        
        layout.addWidget(upload_frame)
        
        # Enable drag and drop
        upload_frame.dragEnterEvent = self.drag_enter_event
        upload_frame.dropEvent = self.drop_event
        
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
        """Set the selected file and update UI"""
        print(f"DEBUG: Setting selected file: {file_path}")  # Debug line
        self.selected_file = file_path
        
        # Get file info
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_size_kb = file_size / 1024
        
        # Update UI
        self.file_info_label.setText(f"✅ Selected: {file_name} ({file_size_kb:.1f} KB)")
        self.file_info_label.setStyleSheet("color: #28a745; font-weight: bold; margin: 10px;")
        self.upload_button.setEnabled(True)
        self.button_status_label.setText("✅ Ready to analyze! Click the button above.")
        self.button_status_label.setStyleSheet("color: #28a745; font-weight: bold; margin: 5px;")
        print(f"DEBUG: Upload button enabled: {self.upload_button.isEnabled()}")  # Debug line
        
        # Validate file size
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            self.show_error("File size exceeds 10MB limit")
            self.upload_button.setEnabled(False)
            self.button_status_label.setText("❌ File too large (max 10MB)")
            self.button_status_label.setStyleSheet("color: #dc3545; font-weight: bold; margin: 5px;")
            print("DEBUG: Upload button disabled due to file size")  # Debug line
            
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
        """Handle successful upload"""
        self.set_uploading(False)
        self.status_label.setText("Analysis completed successfully!")
        self.status_label.setStyleSheet("color: #28a745; font-weight: bold;")
        self.status_message.emit("Analysis completed successfully")
        
        # Emit analysis completed signal
        self.analysis_completed.emit(result)
        
        # Reset for next upload
        self.reset_upload()
        
    def on_upload_error(self, error_message):
        """Handle upload error"""
        self.set_uploading(False)
        self.show_error(f"Upload failed: {error_message}")
        self.status_message.emit("Upload failed")
        
    def show_error(self, message):
        """Show error message"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: #dc3545; font-weight: bold;")
        
    def set_uploading(self, uploading):
        """Set uploading state"""
        self.upload_button.setEnabled(not uploading)
        self.progress_bar.setVisible(uploading)
        
        if uploading:
            self.progress_bar.setValue(0)
        else:
            self.progress_bar.setVisible(False)
            
    def reset_upload(self):
        """Reset upload widget for next file"""
        self.selected_file = None
        self.file_info_label.setText("No file selected")
        self.file_info_label.setStyleSheet("color: #666; font-style: italic; margin: 10px;")
        self.upload_button.setEnabled(False)
        self.button_status_label.setText("Select a CSV file to enable the analyze button")
        self.button_status_label.setStyleSheet("color: #666; font-style: italic; margin: 5px;")