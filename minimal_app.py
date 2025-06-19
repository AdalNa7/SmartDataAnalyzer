import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
import json
import uuid
from datetime import datetime

# Create Flask app without NumPy dependencies
app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-12345')
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create required directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('reports', exist_ok=True)

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return {"status": "operational", "message": "Smart Data Analyzer running without NumPy dependencies"}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    client_email = request.form.get('client_email', '').strip()
    
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if not client_email:
        flash('Please enter your email address for report delivery', 'warning')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Store file info in session
        session['uploaded_file'] = filepath
        session['client_email'] = client_email
        session['original_filename'] = file.filename
        
        flash('File uploaded successfully! NumPy analysis will be available once dependencies are resolved.', 'success')
        return redirect(url_for('dashboard'))
    
    flash('Invalid file format. Please upload CSV, XLSX, or XLS files.', 'error')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'uploaded_file' not in session:
        flash('Please upload a file first')
        return redirect(url_for('index'))
    
    return render_template('dashboard.html', 
                         filename=session.get('original_filename', 'Unknown'),
                         client_email=session.get('client_email', ''))

@app.route('/api/analyze', methods=['POST'])
def analyze():
    return jsonify({
        "status": "dependency_issue",
        "message": "NumPy/Pandas dependencies are currently being resolved. Analysis will be available shortly.",
        "solution": "The libstdc++.so.6 library is being configured for NumPy support."
    })

@app.route('/api/growth-insights', methods=['POST'])
def growth_insights():
    return jsonify({
        "status": "dependency_issue", 
        "message": "Growth insights require NumPy/Pandas which are currently being resolved."
    })

@app.route('/api/advanced-analytics', methods=['POST'])
def advanced_analytics():
    return jsonify({
        "status": "dependency_issue",
        "message": "Advanced analytics require NumPy/Pandas which are currently being resolved."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)