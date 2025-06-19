import os
import logging
from flask import Flask
from flask_mail import Mail
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Configure Flask-Mail for automated email delivery
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('SMTP_EMAIL', '')
app.config['MAIL_PASSWORD'] = os.environ.get('SMTP_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = ('Smart Data Analyzer', os.environ.get('SMTP_EMAIL', 'noreply@smartdataanalyzer.com'))

# Initialize Flask-Mail
mail = Mail(app)

# Create required directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('reports', exist_ok=True)

# Import minimal routes (avoiding numpy/pandas dependency issues)
try:
    from routes import *
except ImportError as e:
    print(f"Routes import failed: {e}")
    # Use minimal routes as fallback
    from minimal_routes import *
    
    # Register minimal routes
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/upload', 'upload_file', upload_file, methods=['POST'])
    app.add_url_rule('/dashboard', 'dashboard', dashboard)
    app.add_url_rule('/generate-report', 'generate_report', generate_report, methods=['POST'])
    app.add_url_rule('/explore', 'explore_data', explore_data, methods=['POST'])
    app.add_url_rule('/clean', 'clean_data', clean_data, methods=['POST'])
    app.add_url_rule('/download-report', 'download_report', download_report, methods=['POST'])
    app.add_url_rule('/growth-analytics', 'growth_analytics', growth_analytics, methods=['POST'])
    app.add_url_rule('/advanced-analytics', 'advanced_analytics', advanced_analytics, methods=['POST'])
    app.add_url_rule('/send-report', 'send_report', send_report, methods=['POST'])
    app.add_url_rule('/email-report', 'email_report', email_report, methods=['POST'])
    app.add_url_rule('/secure-download/<report_id>', 'secure_download', secure_download)
    
    app.errorhandler(404)(not_found)
    app.errorhandler(413)(too_large)
    app.errorhandler(500)(server_error)
