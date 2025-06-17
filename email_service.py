"""
Email Service for Smart Data Analyzer
Handles automated email delivery of PDF reports with secure download links
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
import uuid
from flask import url_for
import logging

class EmailService:
    def __init__(self, app=None):
        self.app = app
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.environ.get('SMTP_EMAIL', 'noreply@smartdataanalyzer.com')
        self.sender_password = os.environ.get('SMTP_PASSWORD', '')
        self.sender_name = "Smart Data Analyzer"
        
        # Report access tokens storage (in production, use Redis or database)
        self.access_tokens = {}
        
    def send_report_email(self, client_email, report_info, download_url, client_name=None):
        """Send professional email with PDF report download link"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = client_email
            msg['Subject'] = "Your Business Intelligence Report is Ready"
            
            # Generate access token for secure download
            access_token = str(uuid.uuid4())
            expiry_date = datetime.now() + timedelta(days=7)
            
            self.access_tokens[access_token] = {
                'report_id': report_info['report_id'],
                'client_email': client_email,
                'expires': expiry_date,
                'filepath': report_info['filepath']
            }
            
            # Create secure download URL
            secure_download_url = f"{download_url}?token={access_token}"
            
            # Create HTML email content
            html_content = self._create_html_email_template(
                client_name or client_email.split('@')[0],
                report_info,
                secure_download_url,
                expiry_date
            )
            
            # Create plain text version
            text_content = self._create_text_email_template(
                client_name or client_email.split('@')[0],
                report_info,
                secure_download_url,
                expiry_date
            )
            
            # Attach both versions
            msg.attach(MIMEText(text_content, 'plain'))
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            if self.sender_password:  # Only send if SMTP credentials are configured
                self._send_smtp_email(msg)
                return {
                    'success': True,
                    'message': 'Report email sent successfully',
                    'access_token': access_token
                }
            else:
                # In development/demo mode, log the email content
                logging.info(f"EMAIL WOULD BE SENT TO: {client_email}")
                logging.info(f"DOWNLOAD URL: {secure_download_url}")
                return {
                    'success': True,
                    'message': 'Email configured (SMTP not set up)',
                    'access_token': access_token,
                    'download_url': secure_download_url
                }
                
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            return {
                'success': False,
                'message': f'Email delivery failed: {str(e)}'
            }
    
    def _send_smtp_email(self, msg):
        """Send email via SMTP"""
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.sender_email, self.sender_password)
        server.send_message(msg)
        server.quit()
    
    def _create_html_email_template(self, client_name, report_info, download_url, expiry_date):
        """Create professional HTML email template"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Business Intelligence Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f8f9fa; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
        .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 300; }}
        .content {{ padding: 40px; }}
        .highlight-box {{ background-color: #eff6ff; border-left: 4px solid #3b82f6; padding: 20px; margin: 25px 0; }}
        .download-button {{ display: inline-block; background-color: #059669; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: 600; margin: 20px 0; }}
        .download-button:hover {{ background-color: #047857; }}
        .report-details {{ background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .footer {{ background-color: #1f2937; color: #9ca3af; padding: 25px; text-align: center; font-size: 14px; }}
        .security-notice {{ background-color: #fef3c7; border: 1px solid #f59e0b; padding: 15px; border-radius: 6px; margin: 20px 0; }}
        ul {{ margin: 15px 0; padding-left: 20px; }}
        li {{ margin: 8px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Smart Data Analyzer</h1>
            <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Your Business Intelligence Report is Ready</p>
        </div>
        
        <div class="content">
            <h2>Hello {client_name},</h2>
            
            <p>Your comprehensive business data analysis has been completed! Our AI-powered system has processed your data and generated actionable insights to help drive your business decisions.</p>
            
            <div class="highlight-box">
                <h3 style="margin-top: 0; color: #1e40af;">📈 What's in Your Report:</h3>
                <ul>
                    <li><strong>Executive Summary</strong> - Key findings and business overview</li>
                    <li><strong>Revenue Analysis</strong> - Financial performance insights</li>
                    <li><strong>Product Performance</strong> - Top-performing products and opportunities</li>
                    <li><strong>Data Quality Assessment</strong> - Data health and optimization recommendations</li>
                    <li><strong>AI-Powered Recommendations</strong> - Strategic actions to boost growth</li>
                    <li><strong>Visual Charts & Tables</strong> - Easy-to-understand data visualizations</li>
                </ul>
            </div>
            
            <div class="report-details">
                <h4 style="margin-top: 0;">📋 Report Details:</h4>
                <p><strong>Report ID:</strong> {report_info['report_id']}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                <p><strong>File Format:</strong> Professional PDF Report</p>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{download_url}" class="download-button">📥 Download Your Report</a>
            </div>
            
            <div class="security-notice">
                <h4 style="margin-top: 0;">🔒 Security Notice:</h4>
                <p>This download link is secure and expires on <strong>{expiry_date.strftime('%B %d, %Y')}</strong> for your data protection. The report contains confidential business information and should be stored securely.</p>
            </div>
            
            <h3>🚀 Next Steps:</h3>
            <ol>
                <li>Download and review your comprehensive analysis report</li>
                <li>Implement the AI-powered recommendations to boost performance</li>
                <li>Schedule regular data analysis for continuous insights</li>
                <li>Contact our team for advanced analytics consultation</li>
            </ol>
            
            <p>Need help interpreting your results or want to schedule a consultation? Our analytics experts are here to help you maximize your data's potential.</p>
            
            <p style="margin-top: 30px;">Best regards,<br>
            <strong>The Smart Data Analyzer Team</strong><br>
            Transforming Data into Decisions</p>
        </div>
        
        <div class="footer">
            <p><strong>Smart Data Analyzer</strong> | Professional Business Intelligence Platform</p>
            <p>© 2025 Smart Sales Decisions. All rights reserved.</p>
            <p style="font-size: 12px; margin-top: 15px;">
                This email contains confidential business intelligence. If you received this in error, please delete it immediately.
            </p>
        </div>
    </div>
</body>
</html>
        """
    
    def _create_text_email_template(self, client_name, report_info, download_url, expiry_date):
        """Create plain text email template"""
        return f"""
SMART DATA ANALYZER - Your Business Intelligence Report is Ready

Hello {client_name},

Your comprehensive business data analysis has been completed! Our AI-powered system has processed your data and generated actionable insights to help drive your business decisions.

WHAT'S IN YOUR REPORT:
• Executive Summary - Key findings and business overview
• Revenue Analysis - Financial performance insights  
• Product Performance - Top-performing products and opportunities
• Data Quality Assessment - Data health and optimization recommendations
• AI-Powered Recommendations - Strategic actions to boost growth
• Visual Charts & Tables - Easy-to-understand data visualizations

REPORT DETAILS:
Report ID: {report_info['report_id']}
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
File Format: Professional PDF Report

DOWNLOAD YOUR REPORT:
{download_url}

SECURITY NOTICE:
This download link is secure and expires on {expiry_date.strftime('%B %d, %Y')} for your data protection. The report contains confidential business information and should be stored securely.

NEXT STEPS:
1. Download and review your comprehensive analysis report
2. Implement the AI-powered recommendations to boost performance
3. Schedule regular data analysis for continuous insights
4. Contact our team for advanced analytics consultation

Need help interpreting your results or want to schedule a consultation? Our analytics experts are here to help you maximize your data's potential.

Best regards,
The Smart Data Analyzer Team
Transforming Data into Decisions

---
Smart Data Analyzer | Professional Business Intelligence Platform
© 2025 Smart Sales Decisions. All rights reserved.

This email contains confidential business intelligence. If you received this in error, please delete it immediately.
        """
    
    def validate_access_token(self, token, report_id):
        """Validate access token for secure download"""
        if token not in self.access_tokens:
            return False
            
        token_data = self.access_tokens[token]
        
        # Check if token is expired
        if datetime.now() > token_data['expires']:
            del self.access_tokens[token]
            return False
            
        # Check if report ID matches
        if token_data['report_id'] != report_id:
            return False
            
        return True
    
    def get_report_info_by_token(self, token):
        """Get report information by access token"""
        return self.access_tokens.get(token)
    
    def cleanup_expired_tokens(self):
        """Clean up expired access tokens"""
        expired_tokens = [
            token for token, data in self.access_tokens.items()
            if datetime.now() > data['expires']
        ]
        
        for token in expired_tokens:
            del self.access_tokens[token]
            
        return len(expired_tokens)