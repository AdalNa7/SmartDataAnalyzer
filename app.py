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

# Try to import routes with NumPy dependencies, fallback if needed
try:
    from routes import *
    print("Full routes with NumPy loaded successfully")
except ImportError as e:
    print(f"NumPy dependency issue: {e}")
    # Fallback routes without NumPy
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/upload', methods=['POST'])
    def upload_file():
        from werkzeug.utils import secure_filename
        from datetime import datetime
        
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
        
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'csv', 'xlsx', 'xls'}:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            session['uploaded_file'] = filepath
            session['client_email'] = client_email
            session['original_filename'] = file.filename
            
            flash('File uploaded successfully! Analysis available once NumPy dependencies resolve.', 'success')
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
            "message": "NumPy/Pandas dependencies are being resolved. Analysis will be available shortly."
        })
    
    print("Fallback routes configured for NumPy dependency resolution")
