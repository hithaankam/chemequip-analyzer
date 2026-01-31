# Chemical Equipment Analyzer - Setup Guide

A comprehensive setup guide for the Chemical Equipment Analyzer project, which includes a Django REST API backend, React frontend, and PyQt5 desktop application.

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Backend Setup (Django)](#backend-setup-django)
- [Frontend Setup (React)](#frontend-setup-react)
- [Desktop Application Setup (PyQt5)](#desktop-application-setup-pyqt5)
- [Running All Applications](#running-all-applications)
- [Test Credentials](#test-credentials)
- [Sample Data](#sample-data)
- [Troubleshooting](#troubleshooting)
- [Features](#features)

## Project Overview

The Chemical Equipment Analyzer is a multi-platform application that provides comprehensive analysis of chemical equipment data including:

- **Backend**: Django REST API with data analysis capabilities
- **Frontend**: React web application with interactive dashboards
- **Desktop**: PyQt5 native application with the same functionality
- **Analysis Features**: Statistical analysis, efficiency rankings, correlation analysis, outlier detection, and PDF report generation

## Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **npm**: 8.0 or higher (comes with Node.js)
- **Git**: For cloning the repository

### Operating System Support

- **Windows**: Fully supported
- **macOS**: Supported (may require additional PyQt5 setup)
- **Linux**: Supported (may require additional system packages)

## Project Structure

```
chemequip-analyzer/
├── backend/                 # Django REST API
│   ├── analysis/           # Data analysis modules
│   ├── api/               # API endpoints and views
│   ├── config/            # Django settings
│   ├── manage.py          # Django management script
│   └── requirements.txt   # Python dependencies
├── frontend/              # React web application
│   ├── src/              # React source code
│   ├── public/           # Static assets
│   ├── package.json      # Node.js dependencies
│   └── package-lock.json # Dependency lock file
├── desktop/              # PyQt5 desktop application
│   ├── ui/              # UI components
│   ├── api/             # API client
│   ├── main.py          # Application entry point
│   └── requirements.txt # Python dependencies
├── datasets/            # Sample data files
├── data-analysis/       # Jupyter notebooks
└── findings/           # Analysis documentation
```

## Backend Setup (Django)

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

First, update the requirements.txt file with all necessary dependencies:

```bash
# Install all required packages
pip install Django==6.0.1
pip install djangorestframework==3.16.1
pip install pandas==2.3.3
pip install numpy==2.3.5
pip install scikit-learn==1.6.0
pip install scipy==1.15.0
pip install django-cors-headers==4.6.0
pip install reportlab==4.0.7
pip install Pillow==10.1.0
pip install matplotlib==3.8.2
```

Or create a complete requirements.txt:

```txt
Django==6.0.1
djangorestframework==3.16.1
pandas==2.3.3
numpy==2.3.5
scikit-learn==1.6.0
scipy==1.15.0
django-cors-headers==4.6.0
reportlab==4.0.7
Pillow==10.1.0
matplotlib==3.8.2
```

Then install:

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 5. Create Test User

```bash
# Start Django shell
python manage.py shell

# Create test user
from django.contrib.auth.models import User
user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
user.save()
exit()
```

### 6. Start Backend Server

```bash
python manage.py runserver
```

The backend will be available at: `http://127.0.0.1:8000`

## Frontend Setup (React)

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start Development Server

```bash
npm start
```

The frontend will be available at: `http://localhost:3000`

**Note**: If port 3000 is already in use, React will prompt you to use another port (usually 3001).

## Desktop Application Setup (PyQt5)

### 1. Navigate to Desktop Directory

```bash
cd desktop
```

### 2. Install Dependencies

```bash
# Install PyQt5 and other dependencies
pip install PyQt5>=5.15.0
pip install matplotlib>=3.5.0
pip install requests>=2.25.0
pip install numpy>=1.21.0

# Or install from requirements file
pip install -r requirements.txt
```

### 3. Run Desktop Application

```bash
python main.py
```

**Note**: Make sure the backend server is running before starting the desktop application.

## Running All Applications

To run all three applications simultaneously:

### Terminal 1 - Backend
```bash
cd backend
python manage.py runserver
```

### Terminal 2 - Frontend
```bash
cd frontend
npm start
```

### Terminal 3 - Desktop (Optional)
```bash
cd desktop
python main.py
```

## Test Credentials

Use these credentials to log into both the web and desktop applications:

- **Username**: `testuser`
- **Password**: `testpass123`

## Sample Data

The project includes sample data for testing:

- **File**: `datasets/sample_equipment_data.csv`
- **Contains**: Chemical equipment data with parameters like flowrate, pressure, and temperature
- **Usage**: Upload this file through either the web or desktop application to test the analysis features

## Features

### Analysis Capabilities

1. **Dataset Overview**
   - Equipment count and types
   - Parameter distributions
   - Data quality metrics

2. **Statistical Analysis**
   - Descriptive statistics
   - Parameter correlations
   - Distribution analysis

3. **Efficiency Analysis**
   - Equipment performance rankings
   - Efficiency scoring
   - Type-based comparisons

4. **Outlier Detection**
   - Statistical outlier identification
   - Parameter-specific analysis
   - Equipment flagging

5. **PDF Report Generation**
   - Comprehensive analysis reports
   - Professional formatting
   - Charts and insights

### User Interface Features

- **Web Application**: Modern React interface with Chart.js visualizations
- **Desktop Application**: Native PyQt5 interface with Matplotlib charts
- **Authentication**: Secure login system
- **File Upload**: CSV data import
- **History**: Previous analysis tracking
- **Export**: PDF report generation

## Troubleshooting

### Common Issues

#### Backend Issues

**Issue**: Database errors
**Solution**: Run migrations: `python manage.py migrate`

#### Frontend Issues

**Issue**: `Module not found: Error: Cannot find file` with case sensitivity errors
**Solution**: This is a Git case-sensitivity issue. The imports have been fixed to use lowercase folder names (`auth`, `dashboard`) instead of uppercase (`Auth`, `Dashboard`).

**Issue**: `npm start` fails
**Solution**: Delete `node_modules` and run `npm install` again

**Issue**: CORS errors
**Solution**: Ensure `django-cors-headers` is installed and configured in Django settings

**Issue**: Port 3000 already in use
**Solution**: Use the alternative port suggested by React, or stop other processes using port 3000

#### Desktop Application Issues

**Issue**: Backend connection failed
**Solution**: Ensure Django server is running on `http://127.0.0.1:8000`

**Issue**: Charts not displaying
**Solution**: Install matplotlib: `pip install matplotlib>=3.5.0`

### Environment Issues

**Issue**: Virtual environment conflicts
**Solution**: Create separate virtual environments for backend and desktop:

```bash
# For backend
cd backend
python -m venv backend_env
backend_env\Scripts\activate  # Windows
pip install -r requirements.txt

# For desktop
cd desktop
python -m venv desktop_env
desktop_env\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Development Notes

### API Endpoints

- `POST /api/analyze/` - Upload and analyze CSV data
- `GET /api/history/` - Get user's analysis history
- `GET /api/dataset/<id>/` - Get specific dataset analysis
- `POST /api/generate-pdf/` - Generate PDF report
- `POST /api/login/` - User authentication
- `POST /api/register/` - User registration

### Technology Stack

- **Backend**: Django 6.0.1, Django REST Framework, Pandas, NumPy, Scikit-learn, ReportLab
- **Frontend**: React 19.2.3, Chart.js, Axios
- **Desktop**: PyQt5, Matplotlib, Requests
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)

### Code Structure

- **Backend Analysis**: Modular analysis pipeline in `backend/analysis/`
- **API Views**: RESTful endpoints in `backend/api/views.py`
- **React Components**: Modular UI components in `frontend/src/components/`
- **Desktop UI**: PyQt5 widgets in `desktop/ui/`

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review the error logs in the terminal
3. Ensure all dependencies are properly installed
4. Verify that all services are running on the correct ports

## Next Steps

After successful setup:

1. Upload the sample dataset (`datasets/sample_equipment_data.csv`)
2. Explore the analysis features
3. Generate PDF reports
4. Try both web and desktop interfaces
5. Review the analysis insights and recommendations