#!/usr/bin/env python3
"""
Chemical Equipment Parameter Visualizer - Desktop Application
PyQt5 + Matplotlib implementation that consumes Django backend API

This desktop application replicates the functionality of the React web frontend
using PyQt5 for UI and Matplotlib for charts, while consuming the same Django API.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from ui.main_window import MainWindow

class ChemicalEquipmentApp(QApplication):
    """Main application class for the Chemical Equipment Analyzer Desktop App"""
    
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("Chemical Equipment Analyzer")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("Chemical Analysis Corp")
        
        # Set application style
        self.setStyle('Fusion')
        
        # Create and show main window
        self.main_window = MainWindow()
        self.main_window.show()

def main():
    """Entry point for the desktop application"""
    app = ChemicalEquipmentApp(sys.argv)
    
    # Set up exception handling
    sys.excepthook = lambda cls, exception, traceback: print(f"Unhandled exception: {exception}")
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()