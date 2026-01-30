"""
History Widget - Dataset upload history and management
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QPushButton,
                             QFrame, QMessageBox, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QFont
from datetime import datetime
import json

class HistoryLoadThread(QThread):
    """Thread for loading history data"""
    history_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
    def run(self):
        """Load history data in background thread"""
        try:
            history = self.api_client.get_upload_history()
            self.history_loaded.emit(history)
        except Exception as e:
            self.error_occurred.emit(str(e))

class HistoryWidget(QWidget):
    """Widget for managing dataset upload history"""
    
    dataset_selected = pyqtSignal(dict)  # Emitted when user selects a dataset
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.history_data = []
        self.load_thread = None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize history widget UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Header
        self.create_header(layout)
        
        # History table
        self.create_history_table(layout)
        
        # Action buttons
        self.create_action_buttons(layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(self.status_label)
        
    def create_header(self, layout):
        """Create header section"""
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("Dataset History")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6fd8;
            }
            QPushButton:pressed {
                background-color: #4c63d2;
            }
        """)
        self.refresh_button.clicked.connect(self.refresh_history)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_button)
        
        layout.addLayout(header_layout)
        
    def create_history_table(self, layout):
        """Create history table"""
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        table_layout = QVBoxLayout(table_frame)
        
        # Table widget
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels([
            "Dataset Name", "Upload Date", "Equipment Count", "Status", "Actions"
        ])
        
        # Table styling
        self.history_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ddd;
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #e3f2fd;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        
        # Table properties
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.history_table.verticalHeader().setVisible(False)
        
        # Resize columns
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Dataset Name
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Upload Date
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Equipment Count
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Actions
        
        table_layout.addWidget(self.history_table)
        layout.addWidget(table_frame)
        
    def create_action_buttons(self, layout):
        """Create action buttons"""
        button_layout = QHBoxLayout()
        
        # View Analysis button
        self.view_button = QPushButton("View Analysis")
        self.view_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        self.view_button.clicked.connect(self.view_selected_analysis)
        self.view_button.setEnabled(False)
        
        # Delete Dataset button
        self.delete_button = QPushButton("Delete Dataset")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        self.delete_button.clicked.connect(self.delete_selected_dataset)
        self.delete_button.setEnabled(False)
        
        # Export Report button
        self.export_button = QPushButton("Export Report")
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #138496;
            }
            QPushButton:pressed {
                background-color: #117a8b;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        self.export_button.clicked.connect(self.export_selected_report)
        self.export_button.setEnabled(False)
        
        button_layout.addWidget(self.view_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.export_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Connect table selection
        self.history_table.selectionModel().selectionChanged.connect(self.on_selection_changed)
        
    def refresh_history(self):
        """Refresh history data"""
        if self.load_thread and self.load_thread.isRunning():
            return
            
        self.status_label.setText("Loading history...")
        self.refresh_button.setEnabled(False)
        
        # Start loading thread
        self.load_thread = HistoryLoadThread(self.api_client)
        self.load_thread.history_loaded.connect(self.on_history_loaded)
        self.load_thread.error_occurred.connect(self.on_history_error)
        self.load_thread.start()
        
    @pyqtSlot(list)
    def on_history_loaded(self, history):
        """Handle loaded history data"""
        self.history_data = history
        self.populate_history_table()
        self.status_label.setText(f"Loaded {len(history)} datasets")
        self.refresh_button.setEnabled(True)
        
    @pyqtSlot(str)
    def on_history_error(self, error_message):
        """Handle history loading error"""
        self.status_label.setText(f"Error loading history: {error_message}")
        self.refresh_button.setEnabled(True)
        QMessageBox.warning(self, "Error", f"Failed to load history: {error_message}")
        
    def populate_history_table(self):
        """Populate history table with data"""
        self.history_table.setRowCount(len(self.history_data))
        
        for row, dataset in enumerate(self.history_data):
            # Dataset name
            name_item = QTableWidgetItem(dataset.get('filename', 'Unknown'))
            self.history_table.setItem(row, 0, name_item)
            
            # Upload date
            upload_date = dataset.get('upload_date', '')
            if upload_date:
                try:
                    # Parse and format date
                    date_obj = datetime.fromisoformat(upload_date.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
                except:
                    formatted_date = upload_date
            else:
                formatted_date = 'Unknown'
            date_item = QTableWidgetItem(formatted_date)
            self.history_table.setItem(row, 1, date_item)
            
            # Equipment count
            equipment_count = dataset.get('equipment_count', 0)
            count_item = QTableWidgetItem(str(equipment_count))
            count_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 2, count_item)
            
            # Status
            status = "Analyzed" if dataset.get('analysis_results') else "Uploaded"
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignCenter)
            if status == "Analyzed":
                status_item.setBackground(Qt.green)
            else:
                status_item.setBackground(Qt.yellow)
            self.history_table.setItem(row, 3, status_item)
            
            # Actions (placeholder)
            actions_item = QTableWidgetItem("Select row for actions")
            actions_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 4, actions_item)
            
    def on_selection_changed(self):
        """Handle table selection change"""
        selected_rows = self.history_table.selectionModel().selectedRows()
        has_selection = len(selected_rows) > 0
        
        self.view_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        self.export_button.setEnabled(has_selection)
        
        if has_selection:
            row = selected_rows[0].row()
            dataset = self.history_data[row]
            has_analysis = bool(dataset.get('analysis_results'))
            self.view_button.setEnabled(has_analysis)
            self.export_button.setEnabled(has_analysis)
            
    def view_selected_analysis(self):
        """View analysis for selected dataset"""
        selected_rows = self.history_table.selectionModel().selectedRows()
        if not selected_rows:
            return
            
        row = selected_rows[0].row()
        dataset = self.history_data[row]
        
        if not dataset.get('analysis_results'):
            QMessageBox.information(self, "No Analysis", 
                                  "This dataset has not been analyzed yet.")
            return
            
        # Emit signal with dataset data
        self.dataset_selected.emit(dataset)
        
    def delete_selected_dataset(self):
        """Delete selected dataset"""
        selected_rows = self.history_table.selectionModel().selectedRows()
        if not selected_rows:
            return
            
        row = selected_rows[0].row()
        dataset = self.history_data[row]
        dataset_name = dataset.get('filename', 'Unknown')
        
        # Confirm deletion
        reply = QMessageBox.question(self, 'Delete Dataset', 
                                   f'Are you sure you want to delete "{dataset_name}"?',
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                dataset_id = dataset.get('id')
                if dataset_id:
                    success = self.api_client.delete_dataset(dataset_id)
                    if success:
                        QMessageBox.information(self, "Success", "Dataset deleted successfully.")
                        self.refresh_history()
                    else:
                        QMessageBox.warning(self, "Error", "Failed to delete dataset.")
                else:
                    QMessageBox.warning(self, "Error", "Dataset ID not found.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error deleting dataset: {str(e)}")
                
    def export_selected_report(self):
        """Export PDF report for selected dataset"""
        selected_rows = self.history_table.selectionModel().selectedRows()
        if not selected_rows:
            return
            
        row = selected_rows[0].row()
        dataset = self.history_data[row]
        
        if not dataset.get('analysis_results'):
            QMessageBox.information(self, "No Analysis", 
                                  "This dataset has not been analyzed yet.")
            return
        
        try:
            # Show progress dialog
            from PyQt5.QtWidgets import QProgressDialog
            from PyQt5.QtCore import QTimer
            
            progress = QProgressDialog("Generating PDF report...", "Cancel", 0, 0, self)
            progress.setWindowTitle("PDF Generation")
            progress.setModal(True)
            progress.show()
            
            # Generate PDF using dataset ID
            dataset_id = dataset.get('id')
            if dataset_id:
                pdf_content = self.api_client.generate_pdf_from_dataset(dataset_id)
            else:
                # Fallback to using analysis results directly
                analysis_results = dataset.get('analysis_results', {})
                dataset_info = {
                    'filename': dataset.get('filename', 'equipment_data.csv'),
                    'upload_date': dataset.get('upload_date', ''),
                    'equipment_count': dataset.get('equipment_count', 0)
                }
                pdf_content = self.api_client.generate_pdf_report(analysis_results, dataset_info)
            
            # Save PDF file
            from PyQt5.QtWidgets import QFileDialog
            import os
            from datetime import datetime
            
            dataset_name = dataset.get('filename', 'equipment_data').replace('.csv', '')
            default_filename = f"{dataset_name}_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
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
                
                QMessageBox.information(self, "Success", f"PDF report saved successfully to:\n{file_path}")
                
                # Ask if user wants to open the PDF
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
            QMessageBox.critical(self, "Error", f"Failed to generate PDF report:\n{str(e)}")
        
    def showEvent(self, event):
        """Handle widget show event"""
        super().showEvent(event)
        # Auto-refresh when widget is shown
        if not self.history_data:
            self.refresh_history()