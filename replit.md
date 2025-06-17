# Smart Data Analyzer (SDA) - Replit Configuration

## Overview

Smart Data Analyzer is a Flask-based web application that provides AI-powered analysis of sales data through file uploads. The platform features a modern SaaS-style interface with multi-tab analysis capabilities, file validation, and conversational exploration features.

## System Architecture

### Backend Architecture
- **Framework**: Flask 3.1.1 with Python 3.11
- **Web Server**: Gunicorn for production deployment
- **File Processing**: Pandas for data manipulation and analysis
- **File Storage**: Local filesystem with secure filename handling
- **Session Management**: Flask sessions with configurable secret key

### Frontend Architecture
- **UI Framework**: Bootstrap 5 for responsive design
- **Icons**: Font Awesome 6.4.0 for consistent iconography
- **JavaScript**: Vanilla JS for file upload interactions and dynamic content
- **CSS**: Custom CSS variables and modern styling with gradient backgrounds

### Application Structure
```
├── main.py (Entry point)
├── app.py (Flask app configuration)
├── routes.py (Route handlers and business logic)
├── templates/ (Jinja2 templates)
├── static/ (CSS, JS, and assets)
└── uploads/ (Temporary file storage)
```

## Key Components

### File Upload System
- **Supported Formats**: CSV, XLSX, XLS files up to 16MB
- **Validation**: Server-side file type validation and secure filename handling
- **Storage**: Temporary upload directory with automatic cleanup
- **Processing**: Pandas-based data reading with error handling

### Data Analysis Dashboard
- **Multi-tab Interface**: AI Report, Smart Data Cleaning, and Conversational tabs
- **Responsive Design**: Mobile-first approach with Bootstrap grid system
- **Interactive Elements**: Tab navigation and dynamic content loading

### AI Analysis Features (Demo Ready)
- **Report Generation**: Structured JSON responses for insights and analysis
- **Data Cleaning**: Automated detection of missing data and outliers
- **Conversational Interface**: Chat-style interaction for data exploration

## Data Flow

1. **File Upload**: User uploads CSV/Excel file through drag-drop or file picker
2. **Validation**: Server validates file format and required columns (product, quantity, price, date)
3. **Processing**: Pandas reads and processes the data into DataFrame
4. **Dashboard**: User redirected to multi-tab analysis interface
5. **Analysis**: Demo AI features provide structured insights and recommendations

## External Dependencies

### Python Packages
- **Core**: Flask, Werkzeug, Gunicorn
- **Data Processing**: Pandas, OpenPyXL, XLRD
- **Database**: Flask-SQLAlchemy, psycopg2-binary (prepared for future use)
- **Validation**: email-validator for future user features

### Frontend Libraries
- **Bootstrap 5**: Responsive UI components and grid system
- **Font Awesome**: Icon library for consistent visual elements
- **Custom CSS**: Modern styling with CSS variables and gradients

### System Packages (Nix)
- **glibc**: Localization support
- **OpenSSL**: Secure communications
- **PostgreSQL**: Database server (prepared for future use)

## Deployment Strategy

### Replit Configuration
- **Runtime**: Python 3.11 with Nix package manager
- **Process Manager**: Gunicorn with auto-scaling deployment
- **Port Configuration**: Flask app runs on port 5000 with proxy support
- **File Permissions**: Proper upload directory creation and permissions

### Environment Configuration
- **Session Security**: Configurable secret key with environment variable fallback
- **File Limits**: 16MB maximum upload size with proper error handling
- **Logging**: Debug-level logging for development and troubleshooting

### Production Readiness
- **Proxy Support**: Werkzeug ProxyFix for proper header handling
- **Process Management**: Gunicorn with reload capabilities for development
- **Error Handling**: Comprehensive error handling for file operations and data processing

## Changelog
- June 17, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.

---

**Note**: The application is structured to easily integrate with AI services (OpenAI, etc.) and PostgreSQL database in future iterations. Current implementation uses demo data and placeholder functions that can be replaced with real AI analysis and database operations without major architectural changes.