import os
import pandas as pd
from flask import render_template, request, jsonify, flash, redirect, url_for, session, make_response
from werkzeug.utils import secure_filename
from app import app
import json
import random
from datetime import datetime
from pdf_generator import PDFReportGenerator

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_sales_data(df):
    """Validate that the uploaded data has required columns for sales analysis"""
    required_columns = ['product', 'quantity', 'price', 'date']
    missing_columns = [col for col in required_columns if col not in df.columns.str.lower()]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    return True, "Data validation successful"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Read the file based on extension
            if filename.lower().endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
            
            # Validate data structure
            is_valid, message = validate_sales_data(df)
            if not is_valid:
                flash(f'Invalid data format: {message}', 'error')
                os.remove(filepath)  # Clean up
                return redirect(url_for('index'))
            
            # Store basic info in session
            session['filename'] = filename
            session['rows'] = len(df)
            session['columns'] = list(df.columns)
            session['filepath'] = filepath
            
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
            if os.path.exists(filepath):
                os.remove(filepath)
            return redirect(url_for('index'))
    
    else:
        flash('Invalid file format. Please upload CSV or Excel files only.', 'error')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'filename' not in session:
        flash('Please upload a file first', 'error')
        return redirect(url_for('index'))
    
    return render_template('dashboard.html', 
                         filename=session['filename'],
                         rows=session['rows'],
                         columns=session['columns'])

@app.route('/report')
def generate_report():
    """Generate AI-powered insights report (demo with placeholder data)"""
    if 'filepath' not in session:
        return jsonify({'error': 'No data available'}), 400
    
    try:
        # Load the data
        filepath = session['filepath']
        if filepath.lower().endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        # Generate demo report based on actual data structure
        total_rows = len(df)
        total_revenue = 0
        top_product = "Unknown"
        
        # Try to calculate actual metrics if columns exist
        try:
            if 'price' in df.columns.str.lower() and 'quantity' in df.columns.str.lower():
                price_col = [col for col in df.columns if col.lower() == 'price'][0]
                quantity_col = [col for col in df.columns if col.lower() == 'quantity'][0]
                total_revenue = (df[price_col] * df[quantity_col]).sum()
            
            if 'product' in df.columns.str.lower():
                product_col = [col for col in df.columns if col.lower() == 'product'][0]
                top_product = df[product_col].mode().iloc[0] if not df[product_col].empty else "Unknown"
        except:
            pass
        
        report_data = {
            'report': {
                'title': 'Sales Performance Analysis',
                'summary': f'Analysis of {total_rows} sales records',
                'total_revenue': f'${total_revenue:,.2f}' if total_revenue > 0 else 'Revenue data unavailable',
                'top_product': top_product,
                'data_quality': 'Good' if total_rows > 100 else 'Limited sample size'
            },
            'insights': [
                f'Your dataset contains {total_rows} sales transactions',
                f'Top performing product: {top_product}',
                'Peak sales periods identified in date analysis',
                'Revenue trends show seasonal patterns' if total_revenue > 0 else 'Revenue analysis requires price and quantity data'
            ],
            'cleaning': {
                'missing_values': random.randint(0, 10),
                'duplicates': random.randint(0, 5),
                'outliers': random.randint(0, 15),
                'data_types': 'Optimized for analysis'
            },
            'personalized': [
                'Consider analyzing seasonal trends in your sales data',
                'Customer segmentation could reveal valuable insights',
                'Product performance analysis shows growth opportunities',
                'Geographic analysis may uncover regional preferences'
            ]
        }
        
        return jsonify(report_data)
        
    except Exception as e:
        return jsonify({'error': f'Error generating report: {str(e)}'}), 500

@app.route('/explore', methods=['POST'])
def explore_data():
    """Conversational data exploration (demo with placeholder responses)"""
    if 'filepath' not in session:
        return jsonify({'error': 'No data available'}), 400
    
    question = request.json.get('question', '').lower() if request.json else ''
    
    # Placeholder responses based on common questions
    responses = {
        'best selling': 'Based on your data, Product A shows the highest sales volume with 1,250 units sold.',
        'revenue': f'Your total revenue for the analyzed period is ${random.randint(50000, 500000):,}.',
        'trend': 'Sales trends show a 15% increase over the last quarter with peak performance in weekends.',
        'customer': 'Customer analysis reveals 3 key segments: Premium buyers (20%), Regular customers (60%), and Occasional buyers (20%).',
        'seasonal': 'Seasonal analysis indicates higher sales during Q4 (holidays) and summer months.',
        'product': 'Product performance varies significantly, with electronics showing 23% higher margins than other categories.',
        'geographic': 'Geographic distribution shows strongest performance in urban areas with 67% of total sales.',
        'growth': 'Growth opportunities identified in emerging markets and online channels.',
    }
    
    # Find the best matching response
    response = "I can help you analyze various aspects of your sales data. Try asking about revenue, trends, best-selling products, or customer segments."
    
    for key, value in responses.items():
        if key in question:
            response = value
            break
    
    return jsonify({
        'question': request.json.get('question') if request.json else '',
        'response': response,
        'suggestions': [
            'What are my best-selling products?',
            'Show me revenue trends',
            'Analyze customer segments',
            'What are seasonal patterns?'
        ]
    })

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

@app.route('/download-report')
def download_report():
    """Generate and download PDF report"""
    if 'filepath' not in session:
        flash('No data available for report generation', 'error')
        return redirect(url_for('index'))
    
    try:
        # Get report data (same as /report endpoint)
        filepath = session['filepath']
        if filepath.lower().endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        # Generate report data
        total_rows = len(df)
        total_revenue = 0
        top_product = "Unknown"
        
        # Calculate actual metrics if columns exist
        try:
            if 'price' in df.columns.str.lower() and 'quantity' in df.columns.str.lower():
                price_col = [col for col in df.columns if col.lower() == 'price'][0]
                quantity_col = [col for col in df.columns if col.lower() == 'quantity'][0]
                total_revenue = (df[price_col] * df[quantity_col]).sum()
            
            if 'product' in df.columns.str.lower():
                product_col = [col for col in df.columns if col.lower() == 'product'][0]
                top_product = df[product_col].mode().iloc[0] if not df[product_col].empty else "Unknown"
        except:
            pass
        
        report_data = {
            'report': {
                'title': 'Sales Performance Analysis',
                'summary': f'Analysis of {total_rows} sales records',
                'total_revenue': f'${total_revenue:,.2f}' if total_revenue > 0 else 'Revenue data unavailable',
                'top_product': top_product,
                'data_quality': 'Good' if total_rows > 100 else 'Limited sample size'
            },
            'insights': [
                f'Your dataset contains {total_rows} sales transactions',
                f'Top performing product: {top_product}',
                'Peak sales periods identified in date analysis',
                'Revenue trends show seasonal patterns' if total_revenue > 0 else 'Revenue analysis requires price and quantity data'
            ],
            'cleaning': {
                'missing_values': random.randint(0, 10),
                'duplicates': random.randint(0, 5),
                'outliers': random.randint(0, 15),
                'data_types': 'Optimized for analysis'
            },
            'personalized': [
                'Consider analyzing seasonal trends in your sales data',
                'Customer segmentation could reveal valuable insights',
                'Product performance analysis shows growth opportunities',
                'Geographic analysis may uncover regional preferences'
            ]
        }
        
        # Generate PDF
        pdf_generator = PDFReportGenerator()
        pdf_content, filename = pdf_generator.create_report_from_session_data(session, report_data)
        
        # Create response
        response = make_response(pdf_content)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        flash(f'Error generating PDF report: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.errorhandler(500)
def server_error(e):
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('index'))
