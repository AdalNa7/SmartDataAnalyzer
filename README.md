# Smart Data Analyzer

A comprehensive data analysis and visualization web application built with Flask, Python, and modern web technologies.

## Features

- **Data Upload & Processing**: Support for CSV, Excel, and other data formats
- **Advanced Analytics**: Statistical analysis, trend detection, and pattern recognition
- **Interactive Visualizations**: Dynamic charts and graphs using Chart.js
- **PDF Report Generation**: Automated report creation with detailed insights
- **Email Integration**: Send analysis reports via email
- **Growth Analytics**: Specialized tools for business growth analysis
- **Data Cleaning**: Automated data preprocessing and validation

## Tech Stack

- **Backend**: Python, Flask
- **Data Processing**: Pandas, NumPy
- **Visualization**: Chart.js, Plotly
- **PDF Generation**: ReportLab
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with responsive design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AdalNa7/SmartDataAnalyzer.git
cd SmartDataAnalyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
SmartDataAnalyzer/
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── routes.py             # Route definitions
├── data_cleaner.py       # Data preprocessing utilities
├── advanced_analytics.py # Advanced analysis functions
├── growth_analytics.py   # Growth analysis tools
├── pdf_generator.py      # PDF report generation
├── email_service.py      # Email functionality
├── column_mapper.py      # Column mapping utilities
├── templates/            # HTML templates
├── static/              # CSS, JS, and static assets
├── uploads/             # File upload directory
└── reports/             # Generated reports
```

## Usage

1. **Upload Data**: Use the web interface to upload your data files
2. **Preview Data**: Review your data structure and column mappings
3. **Run Analysis**: Select analysis options and generate insights
4. **View Results**: Explore interactive visualizations and statistics
5. **Download Reports**: Generate and download PDF reports
6. **Share Results**: Email reports to stakeholders

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue on GitHub or contact the maintainers. 