"""
Authentication Dialog for login/register functionality
Matches the React frontend authentication flow
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QPushButton, QLabel, QTabWidget, 
                             QWidget, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

class AuthWorker(QThread):
    """Worker thread for authentication to prevent UI blocking"""
    success = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client, action, username, password, email=None):
        super().__init__()
        self.api_client = api_client
        self.action = action
        self.username = username
        self.password = password
        self.email = email
        
    def run(self):
        try:
            if self.action == 'login':
                result = self.api_client.login(self.username, self.password)
            else:  # register
                result = self.api_client.register(self.username, self.password, self.email)
            self.success.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class AuthDialog(QDialog):
    """Authentication dialog with login and register tabs"""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.auth_worker = None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the authentication dialog UI"""
        self.setWindowTitle("Authentication Required")
        self.setFixedSize(400, 300)
        self.setModal(True)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Chemical Equipment Analyzer")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #667eea; margin-bottom: 20px;")
        layout.addWidget(title_label)
        
        # Tab widget for login/register
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create login tab
        self.create_login_tab()
        
        # Create register tab
        self.create_register_tab()
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red; margin-top: 10px;")
        layout.addWidget(self.status_label)
        
    def create_login_tab(self):
        """Create login tab"""
        login_widget = QWidget()
        layout = QVBoxLayout(login_widget)
        
        # Form layout
        form_layout = QFormLayout()
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter username")
        form_layout.addRow("Username:", self.login_username)
        
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setPlaceholderText("Enter password")
        form_layout.addRow("Password:", self.login_password)
        
        layout.addLayout(form_layout)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
            }
            QPushButton:disabled {
                background: #cccccc;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        # Connect Enter key
        self.login_password.returnPressed.connect(self.handle_login)
        
        self.tab_widget.addTab(login_widget, "Login")
        
    def create_register_tab(self):
        """Create register tab"""
        register_widget = QWidget()
        layout = QVBoxLayout(register_widget)
        
        # Form layout
        form_layout = QFormLayout()
        
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Choose username")
        form_layout.addRow("Username:", self.register_username)
        
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("Enter email address")
        form_layout.addRow("Email:", self.register_email)
        
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password.setPlaceholderText("Choose password")
        form_layout.addRow("Password:", self.register_password)
        
        layout.addLayout(form_layout)
        
        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #218838 0%, #1ea085 100%);
            }
            QPushButton:disabled {
                background: #cccccc;
            }
        """)
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)
        
        # Connect Enter key
        self.register_password.returnPressed.connect(self.handle_register)
        
        self.tab_widget.addTab(register_widget, "Register")
        
    def handle_login(self):
        """Handle login button click"""
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
            
        self.set_loading(True)
        self.status_label.setText("Logging in...")
        
        self.auth_worker = AuthWorker(self.api_client, 'login', username, password)
        self.auth_worker.success.connect(self.on_auth_success)
        self.auth_worker.error.connect(self.on_auth_error)
        self.auth_worker.start()
        
    def handle_register(self):
        """Handle register button click"""
        username = self.register_username.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text().strip()
        
        if not username or not email or not password:
            self.show_error("Please fill in all fields")
            return
            
        if '@' not in email:
            self.show_error("Please enter a valid email address")
            return
            
        self.set_loading(True)
        self.status_label.setText("Creating account...")
        
        self.auth_worker = AuthWorker(self.api_client, 'register', username, password, email)
        self.auth_worker.success.connect(self.on_auth_success)
        self.auth_worker.error.connect(self.on_auth_error)
        self.auth_worker.start()
        
    def on_auth_success(self, result):
        """Handle successful authentication"""
        self.set_loading(False)
        self.status_label.setText("")
        self.accept()  # Close dialog with success
        
    def on_auth_error(self, error_message):
        """Handle authentication error"""
        self.set_loading(False)
        self.show_error(f"Authentication failed: {error_message}")
        
    def show_error(self, message):
        """Show error message"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: red; margin-top: 10px;")
        
    def set_loading(self, loading):
        """Set loading state"""
        self.login_button.setEnabled(not loading)
        self.register_button.setEnabled(not loading)
        
        if not loading:
            self.status_label.setText("")