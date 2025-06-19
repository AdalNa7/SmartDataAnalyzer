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

# Configure environment for NumPy before importing routes
import os
import glob

# Set up comprehensive library paths
lib_dirs = []
for pattern in ["/nix/store/*/lib", "/nix/store/*/lib64"]:
    lib_dirs.extend(glob.glob(pattern))

if lib_dirs:
    current_ld = os.environ.get('LD_LIBRARY_PATH', '')
    new_ld_path = ':'.join(lib_dirs[:30])  # Limit paths
    if current_ld:
        new_ld_path = f"{new_ld_path}:{current_ld}"
    os.environ['LD_LIBRARY_PATH'] = new_ld_path

# Import routes
from routes import *
