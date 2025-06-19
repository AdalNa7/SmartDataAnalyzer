import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file, session
from flask_mail import Mail
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
import json

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "fixing_dependencies", "message": "NumPy/Pandas dependency resolution in progress"})

@app.route('/upload', methods=['POST'])
def upload_file():
    flash('Upload functionality temporarily disabled while fixing data processing dependencies.', 'warning')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error during dependency resolution'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)