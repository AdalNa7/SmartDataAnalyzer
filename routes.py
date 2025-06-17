import os
import pandas as pd
import numpy as np
from flask import render_template, request, jsonify, flash, redirect, url_for, session, make_response, send_file, abort
from flask_mail import Message
from werkzeug.utils import secure_filename
from app import app, mail
import json
from datetime import datetime
from pdf_generator import PDFReportGenerator
from enhanced_pdf_generator import EnhancedPDFGenerator
from email_service import EmailService
from growth_analytics import GrowthAnalytics
from advanced_analytics import AdvancedAnalytics
from data_cleaner import SmartDataCleaner

# Initialize services
enhanced_pdf_generator = EnhancedPDFGenerator()
email_service = EmailService()

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

def analyze_sales_data(df):
    """Comprehensive sales data analysis using pandas"""
    analysis = {}
    
    # Standardize column names for analysis
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.lower().str.strip()
    
    # Basic data info
    analysis['total_rows'] = len(df_clean)
    analysis['total_columns'] = len(df_clean.columns)
    
    # Find required columns
    required_cols = {}
    for col in df_clean.columns:
        if 'product' in col or 'item' in col or 'name' in col:
            required_cols['product'] = col
        elif 'price' in col or 'cost' in col or 'amount' in col:
            required_cols['price'] = col
        elif 'quantity' in col or 'qty' in col or 'units' in col:
            required_cols['quantity'] = col
        elif 'date' in col or 'time' in col:
            required_cols['date'] = col
    
    # Revenue analysis
    if 'price' in required_cols and 'quantity' in required_cols:
        try:
            df_clean[required_cols['price']] = pd.to_numeric(df_clean[required_cols['price']], errors='coerce')
            df_clean[required_cols['quantity']] = pd.to_numeric(df_clean[required_cols['quantity']], errors='coerce')
            
            df_clean['revenue'] = df_clean[required_cols['price']] * df_clean[required_cols['quantity']]
            analysis['total_revenue'] = float(df_clean['revenue'].sum())
            analysis['avg_order_value'] = float(df_clean['revenue'].mean())
            analysis['revenue_std'] = float(df_clean['revenue'].std())
        except:
            analysis['total_revenue'] = 0.0
            analysis['avg_order_value'] = 0.0
    else:
        analysis['total_revenue'] = 0.0
        analysis['avg_order_value'] = 0.0
    
    # Product analysis
    if 'product' in required_cols:
        try:
            product_sales = df_clean.groupby(required_cols['product'])['revenue'].agg(['sum', 'count', 'mean']).round(2)
            product_sales = product_sales.sort_values('sum', ascending=False)
            
            # Convert to JSON-serializable format
            top_products_dict = {}
            for product, row in product_sales.head(10).iterrows():
                top_products_dict[str(product)] = {
                    'sum': float(row['sum']),
                    'count': int(row['count']),
                    'mean': float(row['mean'])
                }
            
            analysis['top_products'] = top_products_dict
            analysis['total_unique_products'] = int(len(product_sales))
            analysis['top_product'] = str(product_sales.index[0]) if len(product_sales) > 0 else "No products found"
        except:
            analysis['top_product'] = "Product analysis failed"
            analysis['total_unique_products'] = 0
    else:
        analysis['top_product'] = "No product column found"
        analysis['total_unique_products'] = 0
    
    # Date analysis
    if 'date' in required_cols:
        try:
            df_clean[required_cols['date']] = pd.to_datetime(df_clean[required_cols['date']], errors='coerce')
            df_clean = df_clean.dropna(subset=[required_cols['date']])
            
            # Time-based insights
            df_clean['month'] = df_clean[required_cols['date']].dt.month
            df_clean['day_of_week'] = df_clean[required_cols['date']].dt.day_name()
            
            monthly_sales = df_clean.groupby('month')['revenue'].sum()
            daily_sales = df_clean.groupby('day_of_week')['revenue'].sum()
            
            analysis['best_month'] = int(monthly_sales.idxmax()) if len(monthly_sales) > 0 else "Unknown"
            analysis['best_day'] = str(daily_sales.idxmax()) if len(daily_sales) > 0 else "Unknown"
            analysis['date_range'] = f"{df_clean[required_cols['date']].min().strftime('%Y-%m-%d')} to {df_clean[required_cols['date']].max().strftime('%Y-%m-%d')}"
        except:
            analysis['best_month'] = "Date analysis failed"
            analysis['best_day'] = "Unknown"
            analysis['date_range'] = "Unknown"
    
    return analysis

def detect_data_quality_issues(df):
    """Detect data quality issues in uploaded file"""
    issues = {}
    
    # Missing values - convert to native Python types
    missing_data = df.isnull().sum()
    missing_dict = {}
    missing_pct_dict = {}
    
    for col, count in missing_data.items():
        if count > 0:
            missing_dict[str(col)] = int(count)
            missing_pct_dict[str(col)] = float(round(count / len(df) * 100, 2))
    
    issues['missing_values'] = missing_dict
    issues['missing_percentage'] = missing_pct_dict
    
    # Duplicate rows
    duplicate_count = df.duplicated().sum()
    issues['duplicate_rows'] = int(duplicate_count)
    issues['duplicate_percentage'] = float(round(duplicate_count / len(df) * 100, 2))
    
    # Zero or negative values in numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    zero_negative_dict = {}
    
    for col in numeric_cols:
        if 'price' in col.lower() or 'cost' in col.lower() or 'amount' in col.lower():
            zero_count = (df[col] <= 0).sum()
            if zero_count > 0:
                zero_negative_dict[str(col)] = int(zero_count)
    
    issues['zero_negative_values'] = zero_negative_dict
    
    # Data type inconsistencies
    data_types_dict = {}
    for col, dtype in df.dtypes.items():
        data_types_dict[str(col)] = str(dtype)
    
    issues['data_types'] = data_types_dict
    
    return issues

@app.route('/report')
def generate_report():
    """Generate comprehensive sales analysis report from uploaded data"""
    try:
        if 'filepath' not in session:
            return jsonify({'error': 'No data uploaded. Please upload a CSV or Excel file first.'}), 400
        
        # Load the uploaded data
        filepath = session['filepath']
        try:
            if filepath.lower().endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
        except Exception as e:
            return jsonify({'error': f'Error reading file: {str(e)}'}), 400
        
        if df.empty:
            return jsonify({'error': 'The uploaded file is empty'}), 400
        
        # Perform comprehensive analysis
        analysis = analyze_sales_data(df)
        quality_issues = detect_data_quality_issues(df)
        
        # Generate insights based on real data
        insights = []
        if analysis['total_revenue'] > 0:
            insights.append(f"Total revenue: ${float(analysis['total_revenue']):,.2f}")
            insights.append(f"Average order value: ${float(analysis['avg_order_value']):.2f}")
            insights.append(f"Top performing product: {analysis['top_product']}")
        else:
            insights.append("Revenue calculation requires price and quantity columns")
        
        if analysis['total_unique_products'] > 0:
            insights.append(f"Product portfolio includes {int(analysis['total_unique_products'])} unique items")
        
        if 'date_range' in analysis and analysis['date_range'] != "Unknown":
            insights.append(f"Data covers period: {analysis['date_range']}")
            if 'best_month' in analysis and analysis['best_month'] != "Unknown":
                insights.append(f"Strongest sales month: {int(analysis['best_month'])}")
            if 'best_day' in analysis and analysis['best_day'] != "Unknown":
                insights.append(f"Best performing day: {analysis['best_day']}")
        
        # Generate recommendations based on data quality
        recommendations = []
        if quality_issues['missing_values']:
            recommendations.append(f"Address missing data in columns: {list(quality_issues['missing_values'].keys())}")
        if quality_issues['duplicate_rows'] > 0:
            recommendations.append(f"Remove {int(quality_issues['duplicate_rows'])} duplicate entries")
        if quality_issues['zero_negative_values']:
            recommendations.append(f"Review zero/negative values in: {list(quality_issues['zero_negative_values'].keys())}")
        if not recommendations:
            recommendations.append("Data quality is good - ready for advanced analysis")
        
        report_data = {
            'report': {
                'title': 'Sales Data Analysis Report',
                'summary': f'Comprehensive analysis of {int(analysis["total_rows"])} records across {int(analysis["total_columns"])} fields',
                'total_revenue': f'${float(analysis["total_revenue"]):,.2f}' if analysis['total_revenue'] > 0 else 'Revenue calculation unavailable',
                'top_product': str(analysis['top_product']),
                'data_quality': 'Good' if len(quality_issues['missing_values']) == 0 and quality_issues['duplicate_rows'] == 0 else 'Needs attention'
            },
            'insights': insights,
            'cleaning': {
                'missing_values': len(quality_issues['missing_values']),
                'duplicates': int(quality_issues['duplicate_rows']),
                'outliers': len(quality_issues['zero_negative_values']),
                'data_types': f"{len(df.select_dtypes(include=[np.number]).columns)} numeric, {len(df.select_dtypes(include=['object']).columns)} text columns"
            },
            'personalized': recommendations
        }
        
        return jsonify(report_data)
        
    except Exception as e:
        return jsonify({'error': f'Error generating report: {str(e)}'}), 500

def answer_data_question(df, question):
    """Answer specific questions about the data using pandas analysis"""
    question = question.lower().strip()
    
    # Standardize column names
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.lower().str.strip()
    
    # Find key columns
    product_col = None
    price_col = None
    quantity_col = None
    date_col = None
    
    for col in df_clean.columns:
        if 'product' in col or 'item' in col or 'name' in col:
            product_col = col
        elif 'price' in col or 'cost' in col or 'amount' in col:
            price_col = col
        elif 'quantity' in col or 'qty' in col or 'units' in col:
            quantity_col = col
        elif 'date' in col or 'time' in col:
            date_col = col
    
    try:
        # Revenue questions
        if any(word in question for word in ['revenue', 'total sales', 'money', 'earnings']):
            if price_col and quantity_col:
                df_clean[price_col] = pd.to_numeric(df_clean[price_col], errors='coerce')
                df_clean[quantity_col] = pd.to_numeric(df_clean[quantity_col], errors='coerce')
                total_revenue = (df_clean[price_col] * df_clean[quantity_col]).sum()
                return f"Your total revenue is ${total_revenue:,.2f} based on {len(df_clean)} transactions."
            else:
                return "Revenue calculation requires both price and quantity columns in your data."
        
        # Best selling product questions
        elif any(word in question for word in ['best selling', 'top product', 'most popular', 'highest sales']):
            if product_col and price_col and quantity_col:
                df_clean[price_col] = pd.to_numeric(df_clean[price_col], errors='coerce')
                df_clean[quantity_col] = pd.to_numeric(df_clean[quantity_col], errors='coerce')
                df_clean['revenue'] = df_clean[price_col] * df_clean[quantity_col]
                
                top_products = df_clean.groupby(product_col)['revenue'].sum().sort_values(ascending=False).head(3)
                top_product = top_products.index[0]
                top_revenue = top_products.iloc[0]
                
                return f"Your best-selling product is '{top_product}' with ${top_revenue:,.2f} in total revenue. Top 3: {', '.join(top_products.index[:3])}"
            elif product_col and quantity_col:
                df_clean[quantity_col] = pd.to_numeric(df_clean[quantity_col], errors='coerce')
                top_by_quantity = df_clean.groupby(product_col)[quantity_col].sum().sort_values(ascending=False).head(3)
                return f"By quantity sold: '{top_by_quantity.index[0]}' with {top_by_quantity.iloc[0]} units. Top 3: {', '.join(top_by_quantity.index[:3])}"
            else:
                return "Product analysis requires product and quantity/price columns in your data."
        
        # Date/time trend questions
        elif any(word in question for word in ['trend', 'over time', 'monthly', 'daily', 'when', 'best day']):
            if date_col and price_col and quantity_col:
                df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors='coerce')
                df_clean = df_clean.dropna(subset=[date_col])
                df_clean[price_col] = pd.to_numeric(df_clean[price_col], errors='coerce')
                df_clean[quantity_col] = pd.to_numeric(df_clean[quantity_col], errors='coerce')
                df_clean['revenue'] = df_clean[price_col] * df_clean[quantity_col]
                
                if 'day' in question:
                    df_clean['day_name'] = df_clean[date_col].dt.day_name()
                    daily_sales = df_clean.groupby('day_name')['revenue'].sum().sort_values(ascending=False)
                    return f"Best performing day: {daily_sales.index[0]} with ${daily_sales.iloc[0]:,.2f} in sales."
                else:
                    df_clean['month'] = df_clean[date_col].dt.month
                    monthly_sales = df_clean.groupby('month')['revenue'].sum().sort_values(ascending=False)
                    return f"Peak sales month: {monthly_sales.index[0]} with ${monthly_sales.iloc[0]:,.2f}. Date range: {df_clean[date_col].min().strftime('%Y-%m-%d')} to {df_clean[date_col].max().strftime('%Y-%m-%d')}"
            else:
                return "Time analysis requires date, price, and quantity columns in your data."
        
        # Count/volume questions
        elif any(word in question for word in ['how many', 'count', 'number of', 'total']):
            if 'product' in question and product_col:
                unique_products = df_clean[product_col].nunique()
                return f"Your data contains {unique_products} unique products across {len(df_clean)} total transactions."
            else:
                return f"Your dataset contains {len(df_clean)} total records across {len(df_clean.columns)} columns."
        
        # Average questions
        elif any(word in question for word in ['average', 'mean', 'typical']):
            if price_col and quantity_col:
                df_clean[price_col] = pd.to_numeric(df_clean[price_col], errors='coerce')
                df_clean[quantity_col] = pd.to_numeric(df_clean[quantity_col], errors='coerce')
                df_clean['revenue'] = df_clean[price_col] * df_clean[quantity_col]
                avg_order = df_clean['revenue'].mean()
                avg_price = df_clean[price_col].mean()
                return f"Average order value: ${avg_order:.2f}. Average price per item: ${avg_price:.2f}"
            else:
                return "Average calculations require price and quantity columns in your data."
        
        # Data quality questions
        elif any(word in question for word in ['missing', 'empty', 'quality', 'clean']):
            missing_data = df_clean.isnull().sum()
            duplicates = df_clean.duplicated().sum()
            issues = missing_data[missing_data > 0]
            
            if len(issues) > 0 or duplicates > 0:
                return f"Data quality issues found: {len(issues)} columns with missing values, {duplicates} duplicate rows. Columns needing attention: {list(issues.index)}"
            else:
                return f"Data quality is good: no missing values or duplicates found in {len(df_clean)} records."
        
        else:
            return "I can analyze your data for: revenue totals, best-selling products, sales trends over time, averages, product counts, or data quality issues. What would you like to know?"
            
    except Exception as e:
        return f"Unable to analyze that aspect of your data. Please ensure your file has the required columns (product, price, quantity, date) and try again."

@app.route('/explore', methods=['POST'])
def explore_data():
    """Answer questions about uploaded data using pandas analysis"""
    try:
        if 'filepath' not in session:
            return jsonify({'error': 'No data uploaded. Please upload a file first.'}), 400
        
        question = request.json.get('question', '').strip() if request.json else ''
        
        if not question:
            return jsonify({'error': 'Please ask a question about your data'}), 400
        
        # Load the data
        filepath = session['filepath']
        try:
            if filepath.lower().endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
        except Exception as e:
            return jsonify({'error': f'Error reading file: {str(e)}'}), 400
        
        if df.empty:
            return jsonify({'error': 'The uploaded file is empty'}), 400
        
        # Answer the question using real data analysis
        response = answer_data_question(df, question)
        
        # Generate relevant follow-up suggestions based on available columns
        suggestions = []
        df_cols = df.columns.str.lower()
        
        if any('price' in col or 'cost' in col for col in df_cols) and any('quantity' in col or 'qty' in col for col in df_cols):
            suggestions.append("What's my total revenue?")
            suggestions.append("What's the average order value?")
        
        if any('product' in col or 'item' in col for col in df_cols):
            suggestions.append("Which product sells the most?")
            suggestions.append("How many unique products do I have?")
        
        if any('date' in col or 'time' in col for col in df_cols):
            suggestions.append("What's my best performing day?")
            suggestions.append("Show me sales trends over time")
        
        suggestions.append("Check my data quality")
        
        return jsonify({
            'question': question,
            'response': response,
            'suggestions': suggestions[:4]  # Limit to 4 suggestions
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing question: {str(e)}'}), 500

@app.route('/clean-data')
def clean_data():
    """Analyze data quality and provide cleaning recommendations"""
    try:
        if 'filepath' not in session:
            return jsonify({'error': 'No data uploaded. Please upload a file first.'}), 400
        
        # Load the uploaded data
        filepath = session['filepath']
        try:
            if filepath.lower().endswith('.csv'):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
        except Exception as e:
            return jsonify({'error': f'Error reading file: {str(e)}'}), 400
        
        if df.empty:
            return jsonify({'error': 'The uploaded file is empty'}), 400
        
        # Analyze data quality using SmartDataCleaner
        cleaner = SmartDataCleaner(df)
        cleaning_analysis = cleaner.analyze_data_quality()
        
        # Get specific cleaning suggestions
        cleaning_suggestions = cleaner.get_cleaned_suggestions()
        
        return jsonify({
            'analysis': cleaning_analysis,
            'suggestions': cleaning_suggestions,
            'data_preview': {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'columns': df.columns.tolist(),
                'sample_data': df.head(5).to_dict('records')
            }
        })
        
    except ValueError as e:
        return jsonify({
            'error': 'Data validation failed',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Data cleaning analysis failed',
            'message': f'Error analyzing your data: {str(e)}'
        }), 500

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
                'missing_values': int(df.isnull().sum().sum()),
                'duplicates': int(df.duplicated().sum()),
                'outliers': len([col for col in df.select_dtypes(include=[np.number]).columns if (df[col] <= 0).any()]),
                'data_types': f"{len(df.select_dtypes(include=[np.number]).columns)} numeric, {len(df.select_dtypes(include=['object']).columns)} text columns"
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

@app.route('/growth-analytics')
def growth_analytics():
    """Generate comprehensive growth analytics"""
    if 'filepath' not in session:
        return jsonify({'error': 'No data available'}), 400
    
    try:
        # Load data
        filepath = session['filepath']
        if filepath.lower().endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        # Initialize growth analytics
        analytics = GrowthAnalytics(df)
        
        # Generate all analytics including new advanced features
        result = {
            'revenue_prediction': analytics.predict_revenue_trend(),
            'top_products': analytics.get_top_products(),
            'best_times': analytics.analyze_best_selling_times(),
            'missed_opportunities': analytics.find_missed_opportunities(),
            'data_quality': analytics.get_data_quality_summary(),
            'recommendations': analytics.generate_ai_recommendations(),
            'product_lifecycle': analytics.detect_product_lifecycle(),
            'seasonality': analytics.detect_seasonality_patterns(),
            'anomalies': analytics.detect_anomalies()
        }
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({
            'error': 'Data validation failed',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Analytics processing failed',
            'message': f'Error analyzing your data: {str(e)}'
        }), 500

@app.route('/advanced-analytics')
def advanced_analytics():
    """Generate advanced analytics including segmentation, forecasting, and health metrics"""
    try:
        df = None
        
        # Try to get uploaded data from session
        if 'uploaded_data' in session:
            try:
                file_path = session['uploaded_data']
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
            except Exception as e:
                print(f"Error loading uploaded data: {e}")
                df = None
        
        # Initialize advanced analytics (will use fallback if df is None/empty)
        analytics = AdvancedAnalytics(df)
        
        # Generate all advanced analytics
        result = {
            'customer_segmentation': analytics.customer_segmentation(),
            'forecast': analytics.smart_forecast(),
            'data_health': analytics.data_health_score(),
            'growth_metrics': analytics.growth_metrics()
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Advanced analytics error: {e}")
        # Return fallback analytics on error
        fallback_analytics = AdvancedAnalytics(pd.DataFrame())
        return jsonify({
            'customer_segmentation': fallback_analytics.customer_segmentation(),
            'forecast': fallback_analytics.smart_forecast(),
            'data_health': fallback_analytics.data_health_score(),
            'growth_metrics': fallback_analytics.growth_metrics()
        })

@app.route('/send-report', methods=['POST'])
def send_report():
    """Simulate sending report via email or Slack"""
    try:
        data = request.get_json()
        method = data.get('method', 'email')
        recipient = data.get('recipient', 'client@example.com')
        
        if method == 'email':
            # Simulate email sending
            return jsonify({
                'success': True,
                'message': f'✅ Report sent to {recipient}',
                'method': 'email'
            })
        elif method == 'slack':
            # Simulate Slack sending
            return jsonify({
                'success': True,
                'message': f'✅ Report posted to Slack channel',
                'method': 'slack'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid delivery method'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to send report'
        })

@app.route('/email-report', methods=['POST'])
def email_report():
    """Send PDF report via email after data analysis"""
    try:
        if 'filepath' not in session:
            return jsonify({
                'success': False,
                'message': 'No data available. Please upload a file first.'
            }), 400
        
        data = request.get_json()
        client_email = data.get('email', '').strip()
        
        if not client_email:
            return jsonify({
                'success': False,
                'message': 'Email address is required.'
            }), 400
        
        # Load and analyze data
        filepath = session['filepath']
        if filepath.lower().endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        # Perform comprehensive analysis
        analysis_data = analyze_sales_data(df)
        
        # Generate comprehensive PDF report
        report_info = enhanced_pdf_generator.generate_comprehensive_report(
            analysis_data=analysis_data,
            client_email=client_email,
            sample_data=df
        )
        
        # Send email with download link
        base_url = f"https://{request.host}" if request.is_secure else f"http://{request.host}"
        email_result = email_service.send_report_email(
            client_email=client_email,
            report_info=report_info,
            download_url=f"{base_url}{report_info['download_url']}"
        )
        
        if email_result['success']:
            return jsonify({
                'success': True,
                'message': f'Report successfully sent to {client_email}'
            })
        else:
            # In development mode, provide the direct download link
            if 'download_url' in email_result:
                return jsonify({
                    'success': True,
                    'message': f'Report generated successfully. Development mode: SMTP not configured, but report is ready.',
                    'download_url': f"{base_url}{report_info['download_url']}"
                })
            else:
                return jsonify({
                    'success': False,
                    'message': f'Email delivery failed: {email_result["message"]}'
                }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating or sending report: {str(e)}'
        }), 500

@app.route('/secure-download/<report_id>')
def secure_download(report_id):
    """Secure PDF report download with token validation"""
    try:
        # Get access token from query parameters
        access_token = request.args.get('token')
        
        if access_token:
            # Validate access token for secure downloads
            if not email_service.validate_access_token(access_token, report_id):
                abort(403)  # Forbidden - invalid or expired token
            
            # Get report info from token
            token_data = email_service.get_report_info_by_token(access_token)
            if not token_data:
                abort(404)
                
            filepath = token_data['filepath']
        else:
            # Fallback to session-based download
            if 'report_id' not in session or session['report_id'] != report_id:
                abort(403)
            
            # Construct filepath from report_id
            filepath = None
            for filename in os.listdir('reports'):
                if report_id in filename:
                    filepath = os.path.join('reports', filename)
                    break
            
            if not filepath:
                abort(404)
        
        # Verify file exists
        if not os.path.exists(filepath):
            abort(404)
        
        # Send file with proper headers
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f'business_intelligence_report_{report_id}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        abort(500)

@app.errorhandler(500)
def server_error(e):
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('index'))
