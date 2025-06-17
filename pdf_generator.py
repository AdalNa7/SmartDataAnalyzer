"""
PDF Report Generator for Smart Data Analyzer
Creates professional PDF reports with analysis results
"""

import os
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from io import BytesIO

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Define custom styles for the PDF report"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#0d6efd')
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.HexColor('#6c757d'),
            alignment=TA_CENTER
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=12,
            textColor=colors.HexColor('#0d6efd'),
            borderWidth=1,
            borderColor=colors.HexColor('#dee2e6'),
            borderPadding=8,
            backColor=colors.HexColor('#f8f9fa')
        ))
        
        # Insight item style
        self.styles.add(ParagraphStyle(
            name='InsightItem',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leftIndent=20,
            bulletIndent=10
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#6c757d')
        ))

    def generate_report(self, report_data, filename=None, sample_data=None):
        """Generate PDF report with analysis results"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"smart_data_analyzer_report_{timestamp}.pdf"
        
        # Create PDF buffer
        buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build story (content)
        story = []
        
        # Header
        story.append(Paragraph("Smart Data Analyzer Report", self.styles['CustomTitle']))
        story.append(Paragraph("Smart Sales Decisions", self.styles['Subtitle']))
        story.append(Spacer(1, 20))
        
        # Generation info
        generation_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"<b>Generated:</b> {generation_time}", self.styles['Normal']))
        story.append(Spacer(1, 30))
        
        # Executive Summary
        if 'report' in report_data:
            story.append(Paragraph("📊 Executive Summary", self.styles['SectionHeader']))
            
            report_info = report_data['report']
            story.append(Paragraph(f"<b>Analysis Title:</b> {report_info.get('title', 'N/A')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Summary:</b> {report_info.get('summary', 'N/A')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Total Revenue:</b> {report_info.get('total_revenue', 'N/A')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Top Product:</b> {report_info.get('top_product', 'N/A')}", self.styles['Normal']))
            story.append(Paragraph(f"<b>Data Quality:</b> {report_info.get('data_quality', 'N/A')}", self.styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Key Insights
        if 'insights' in report_data and report_data['insights']:
            story.append(Paragraph("💡 Key Insights", self.styles['SectionHeader']))
            
            for i, insight in enumerate(report_data['insights'], 1):
                story.append(Paragraph(f"• {insight}", self.styles['InsightItem']))
            story.append(Spacer(1, 20))
        
        # Data Cleaning Analysis
        if 'cleaning' in report_data:
            story.append(Paragraph("🧹 Data Quality Analysis", self.styles['SectionHeader']))
            
            cleaning_info = report_data['cleaning']
            
            # Create cleaning summary table
            cleaning_data = [
                ['Data Quality Metric', 'Count', 'Status'],
                ['Missing Values', str(cleaning_info.get('missing_values', 0)), 'Detected' if cleaning_info.get('missing_values', 0) > 0 else 'Clean'],
                ['Duplicate Records', str(cleaning_info.get('duplicates', 0)), 'Detected' if cleaning_info.get('duplicates', 0) > 0 else 'Clean'],
                ['Outliers', str(cleaning_info.get('outliers', 0)), 'Detected' if cleaning_info.get('outliers', 0) > 0 else 'Clean'],
                ['Data Types', cleaning_info.get('data_types', 'N/A'), 'Optimized']
            ]
            
            cleaning_table = Table(cleaning_data, colWidths=[2.5*inch, 1*inch, 1.5*inch])
            cleaning_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
            ]))
            
            story.append(cleaning_table)
            story.append(Spacer(1, 20))
        
        # Personalized Recommendations
        if 'personalized' in report_data and report_data['personalized']:
            story.append(Paragraph("⭐ Personalized Recommendations", self.styles['SectionHeader']))
            
            for i, recommendation in enumerate(report_data['personalized'], 1):
                story.append(Paragraph(f"{i}. {recommendation}", self.styles['InsightItem']))
            story.append(Spacer(1, 20))
        
        # Sample Data Preview
        if sample_data is not None and not sample_data.empty:
            story.append(Paragraph("📋 Data Sample Preview", self.styles['SectionHeader']))
            story.append(Paragraph("First 5 rows of your uploaded data:", self.styles['Normal']))
            story.append(Spacer(1, 10))
            
            # Convert sample data to table
            sample_preview = sample_data.head(5)
            table_data = [list(sample_preview.columns)]
            
            for _, row in sample_preview.iterrows():
                table_data.append([str(val) for val in row.values])
            
            # Create table with dynamic column widths
            available_width = 6.5 * inch
            col_width = available_width / len(sample_preview.columns)
            col_widths = [col_width] * len(sample_preview.columns)
            
            sample_table = Table(table_data, colWidths=col_widths)
            sample_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#198754')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(sample_table)
            story.append(Spacer(1, 30))
        
        # Footer
        story.append(Spacer(1, 50))
        story.append(Paragraph("Generated by Smart Data Analyzer | Smart Sales Decisions", self.styles['Footer']))
        story.append(Paragraph("Transforming your data into actionable insights", self.styles['Footer']))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF content
        pdf_content = buffer.getvalue()
        buffer.close()
        
        return pdf_content, filename

    def create_report_from_session_data(self, session_data, report_data):
        """Create PDF report using session data and report analysis"""
        
        sample_data = None
        
        # Load sample data if available
        if 'filepath' in session_data:
            try:
                filepath = session_data['filepath']
                if filepath.lower().endswith('.csv'):
                    sample_data = pd.read_csv(filepath)
                else:
                    sample_data = pd.read_excel(filepath)
            except Exception as e:
                print(f"Error loading sample data: {e}")
                sample_data = None
        
        return self.generate_report(
            report_data=report_data,
            sample_data=sample_data
        )