import os
from flask import render_template, request, jsonify, flash, redirect, url_for, session

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xlsx', 'xls'}

def index():
    return render_template('index.html')

def upload_file():
    flash('Data processing temporarily unavailable while fixing system dependencies.', 'warning')
    return redirect(url_for('index'))

def dashboard():
    return render_template('dashboard.html')

def generate_report():
    return jsonify({'error': 'Report generation temporarily disabled during dependency fix'})

def explore_data():
    return jsonify({'response': 'Data exploration temporarily unavailable'})

def clean_data():
    return jsonify({'error': 'Data cleaning temporarily disabled'})

def download_report():
    return jsonify({'error': 'Downloads temporarily disabled'})

def growth_analytics():
    return jsonify({'error': 'Analytics temporarily disabled'})

def advanced_analytics():
    return jsonify({'error': 'Advanced analytics temporarily disabled'})

def send_report():
    return jsonify({'error': 'Report sending temporarily disabled'})

def email_report():
    return jsonify({'error': 'Email reports temporarily disabled'})

def secure_download(report_id):
    return jsonify({'error': 'Secure downloads temporarily disabled'})

def not_found(e):
    return render_template('index.html'), 404

def too_large(e):
    return jsonify({'error': 'File too large'}), 413

def server_error(e):
    return jsonify({'error': 'Server error during maintenance'}), 500