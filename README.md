# Chemical Equipment Analyzer

<div align="center">
  <h3 align="center">Chemical Equipment Analyzer</h3>
  <p align="center">
    A comprehensive multi-platform application for analyzing chemical equipment performance data
    <br />
    <a href="#about-the-project"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    
    <a href="https://github.com/hithaankam/chemequip-analyzer/issues">Report Bug</a>
    ·
    <a href="https://github.com/hithaankam/chemequip-analyzer/issues">Request Feature</a>
  </p>
</div>

## About The Project

The Chemical Equipment Analyzer is a sophisticated data analysis platform designed for chemical engineers and plant operators to analyze equipment performance data. The application provides comprehensive insights into equipment efficiency, parameter correlations, and operational recommendations.

### Key Features

* **Multi-Platform Support**: Web application (React), Desktop application (PyQt5), and REST API (Django)
* **Comprehensive Analysis**: Statistical analysis, efficiency rankings, correlation analysis, and outlier detection
* **Interactive Visualizations**: Dynamic charts and graphs using Chart.js and Matplotlib
* **PDF Report Generation**: Professional analysis reports with insights and recommendations
* **User Authentication**: Secure login system with user-specific data management
* **File Upload & History**: CSV data import with analysis history tracking

### Built With

* [![React][React.js]][React-url]
* [![Django][Django.py]][Django-url]
* [![Python][Python.py]][Python-url]
* [![PyQt5][PyQt5.py]][PyQt5-url]
* [![PostgreSQL][PostgreSQL.db]][PostgreSQL-url]
* [![Chart.js][Chart.js]][Chart-url]

## Getting Started

To get a local copy up and running, follow the detailed setup instructions in [SETUP.md](SETUP.md).

### Prerequisites

* Python 3.8+
* Node.js 16.0+
* npm 8.0+

### Quick Installation

1. Clone the repository
   ```sh
   git clone https://github.com/yourusername/chemequip-analyzer.git
   ```

2. Set up the backend
   ```sh
   cd backend
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. Set up the frontend
   ```sh
   cd frontend
   npm install
   npm start
   ```

4. (Optional) Set up the desktop application
   ```sh
   cd desktop
   pip install -r requirements.txt
   python main.py
   ```

## Usage

### Web Application
1. Navigate to `http://localhost:3000`
2. Login with credentials: `testuser` / `testpass123`
3. Upload a CSV file with equipment data
4. View comprehensive analysis results
5. Generate PDF reports

### Desktop Application
1. Run `python main.py` from the desktop directory
2. Login with the same credentials
3. Access all web features in a native desktop interface

### Sample Data
Use the provided sample dataset at `datasets/sample_equipment_data.csv` to test the application features.

## Project Structure

```
chemequip-analyzer/
├── backend/                 # Django REST API
│   ├── analysis/           # Data analysis modules
│   ├── api/               # API endpoints
│   └── config/            # Django settings
├── frontend/              # React web application
│   └── src/
│       └── components/    # React components
├── desktop/              # PyQt5 desktop application
│   └── ui/              # Desktop UI components
├── datasets/            # Sample data files
└── docs/               # Documentation
```

## Analysis Features

### Statistical Analysis
- Descriptive statistics for all parameters
- Distribution analysis and data quality metrics
- Parameter correlation analysis

### Equipment Performance
- Efficiency scoring and rankings
- Equipment type comparisons
- Performance trend analysis

### Outlier Detection
- Statistical outlier identification
- Parameter-specific anomaly detection
- Equipment maintenance recommendations

### Reporting
- Comprehensive PDF reports
- Executive summaries
- Operational recommendations

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analyze/` | POST | Upload and analyze CSV data |
| `/api/history/` | GET | Get user's analysis history |
| `/api/dataset/<id>/` | GET | Get specific dataset analysis |
| `/api/generate-pdf/` | POST | Generate PDF report |
| `/api/login/` | POST | User authentication |
| `/api/register/` | POST | User registration |


## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Ankam Hitha - hithaankam@gmail.com

Project Link: [https://github.com/hithaankam/chemequip-analyzer](https://github.com/hithaankam/chemequip-analyzer)

## Acknowledgments

* [Django REST Framework](https://www.django-rest-framework.org/)
* [React](https://reactjs.org/)
* [Chart.js](https://www.chartjs.org/)
* [PyQt5](https://pypi.org/project/PyQt5/)
* [ReportLab](https://www.reportlab.com/)
* [Railway](https://railway.app/) for hosting

<!-- MARKDOWN LINKS & IMAGES -->
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Django.py]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[Python.py]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[PyQt5.py]: https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white
[PyQt5-url]: https://pypi.org/project/PyQt5/
[PostgreSQL.db]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Chart.js]: https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white
[Chart-url]: https://www.chartjs.org/
