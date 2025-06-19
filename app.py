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

# Import routes with fallback for NumPy dependency issues
try:
    from routes import *
    print("Routes imported successfully - NumPy dependencies resolved")
except ImportError as e:
    print(f"NumPy dependency issue detected: {e}")
    # Create minimal routes as fallback
    @app.route('/')
    def index():
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Smart Data Analyzer - Dependency Resolution</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 10px; backdrop-filter: blur(10px);">
                <h1>Smart Data Analyzer</h1>
                <h2>System Dependency Resolution in Progress</h2>
                <p>We're currently resolving a NumPy system dependency issue (libstdc++.so.6).</p>
                <p>The application will be fully operational once the C++ standard library is properly configured.</p>
                <hr style="border: 1px solid rgba(255,255,255,0.3);">
                <h3>Current Status:</h3>
                <ul>
                    <li>✓ Flask application running</li>
                    <li>✓ Gunicorn server operational</li>
                    <li>⚠ NumPy/Pandas dependency resolution needed</li>
                    <li>⚠ Missing libstdc++.so.6 system library</li>
                </ul>
                <p><strong>Solution:</strong> Install libstdc++6 system package to resolve NumPy C extension loading.</p>
            </div>
        </body>
        </html>
        '''
    
    @app.route('/health')
    def health():
        return {"status": "dependency_resolution", "issue": "libstdc++.so.6 missing", "server": "operational"}
    
    print("Fallback routes configured - application accessible with dependency notice")
