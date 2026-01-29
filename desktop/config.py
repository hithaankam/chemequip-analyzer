"""
Configuration settings for the desktop application
Matches the API endpoints used by the React frontend
"""

# Backend API Configuration
API_BASE_URL = "http://127.0.0.1:8000"
API_ENDPOINTS = {
    'root': f"{API_BASE_URL}/",
    'register': f"{API_BASE_URL}/api/register/",
    'login': f"{API_BASE_URL}/api/login/",
    'analyze': f"{API_BASE_URL}/api/analyze/",
    'history': f"{API_BASE_URL}/api/history/",
    'dataset': f"{API_BASE_URL}/api/dataset/{{id}}/",
}

# Application Settings
APP_TITLE = "Chemical Equipment Parameter Visualizer"
APP_VERSION = "1.0.0"
WINDOW_SIZE = (1400, 900)
MIN_WINDOW_SIZE = (1000, 700)

# Chart Settings (matching React frontend styling)
CHART_COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#28a745',
    'info': '#17a2b8',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'equipment_types': [
        '#FF6384',  # Red
        '#36A2EB',  # Blue  
        '#FFCE56',  # Yellow
        '#4BC0C0',  # Teal
        '#9966FF',  # Purple
        '#FF9F40',  # Orange
    ]
}

# File Settings
SUPPORTED_FILE_TYPES = ['.csv']
MAX_FILE_SIZE_MB = 10