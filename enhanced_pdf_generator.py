"""
Enhanced PDF Report Generator for Smart Data Analyzer
Creates comprehensive professional PDF reports with automated email delivery
"""

import os
import uuid
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import pandas as pd


class EnhancedPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def setup_custom_styles(self):
        """Define custom styles for professional PDF reports"""
        # Main title style
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1E3A8A'),
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#64748B'),
            fontName='Helvetica'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=15,
            spaceBefore=25,
            textColor=colors.HexColor('#1F2937'),
            fontName='Helvetica-Bold'
        ))
        
        # Subsection header style
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            textColor=colors.HexColor('#374151'),
            fontName='Helvetica-Bold'
        ))
        
        # Key insight style
        self.styles.add(ParagraphStyle(
            name='KeyInsight',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=8,
            leftIndent=20,
            textColor=colors.HexColor('#1F2937'),
            fontName='Helvetica'
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#9CA3AF')
        ))

    def generate_comprehensive_report(self, analysis_data, growth_data=None, advanced_data=None, client_email=None, sample_data=None):
        """Generate comprehensive PDF report with all analysis data"""
        # Generate unique report ID and filename
        report_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_report_{timestamp}_{report_id}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        # Create document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        # Build story (content)
        story = []
        
        # Header and title
        self._add_header(story)
        
        # Executive summary
        self._add_executive_summary(story, analysis_data)
        
        # Key metrics dashboard
        self._add_key_metrics(story, analysis_data, growth_data)
        
        # Business insights
        self._add_business_insights(story, analysis_data)
        
        # Data quality analysis
        self._add_data_quality_analysis(story, analysis_data)
        
        # Growth analytics (if available)
        if growth_data:
            self._add_growth_analytics(story, growth_data)
        
        # Advanced analytics (if available)
        if advanced_data:
            self._add_advanced_analytics(story, advanced_data)
        
        # Recommendations
        self._add_recommendations(story, analysis_data)
        
        # Sample data preview
        if sample_data is not None:
            self._add_sample_data(story, sample_data)
        
        # Footer
        self._add_footer(story, report_id, client_email)
        
        # Build PDF
        doc.build(story)
        
        return {
            'filename': filename,
            'filepath': filepath,
            'report_id': report_id,
            'download_url': f'/download-report/{report_id}'
        }

    def _add_header(self, story):
        """Add professional header to the report"""
        story.append(Paragraph("SMART DATA ANALYZER", self.styles['MainTitle']))
        story.append(Paragraph("Comprehensive Business Intelligence Report", self.styles['Subtitle']))
        story.append(Spacer(1, 20))
        
        # Add report metadata
        current_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"Generated on {current_date}", self.styles['Footer']))
        story.append(Spacer(1, 30))

    def _add_executive_summary(self, story, data):
        """Add executive summary section"""
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        # Create summary from analysis data
        if data.get('total_revenue', 0) > 0:
            summary_text = f"This comprehensive analysis reveals key business insights from your dataset. "
            summary_text += f"Total revenue analyzed: ${float(data['total_revenue']):,.2f} "
            if data.get('total_unique_products', 0) > 0:
                summary_text += f"across {int(data['total_unique_products'])} unique products. "
            if data.get('top_product'):
                summary_text += f"Top performing product: {data['top_product']}."
        else:
            summary_text = f"Comprehensive analysis of {data.get('total_rows', 'your')} data records "
            summary_text += f"across {data.get('total_columns', 'multiple')} dimensions reveals key business patterns and opportunities."
        
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(Spacer(1, 15))

    def _add_key_metrics(self, story, analysis_data, growth_data):
        """Add key metrics dashboard"""
        story.append(Paragraph("Key Performance Metrics", self.styles['SectionHeader']))
        
        # Create metrics table
        metrics_data = [['Metric', 'Value', 'Status']]
        
        # Revenue metrics
        if analysis_data.get('total_revenue', 0) > 0:
            metrics_data.append(['Total Revenue', f"${float(analysis_data['total_revenue']):,.2f}", 'Calculated'])
            metrics_data.append(['Average Order Value', f"${float(analysis_data.get('avg_order_value', 0)):.2f}", 'Calculated'])
        
        # Product metrics
        if analysis_data.get('total_unique_products', 0) > 0:
            metrics_data.append(['Unique Products', str(int(analysis_data['total_unique_products'])), 'Analyzed'])
            metrics_data.append(['Top Product', str(analysis_data.get('top_product', 'N/A')), 'Identified'])
        
        # Data quality metrics
        if 'cleaning' in analysis_data:
            cleaning = analysis_data['cleaning']
            quality_score = 100 - (cleaning.get('missing_values', 0) * 2) - (cleaning.get('duplicates', 0))
            quality_score = max(0, min(100, quality_score))
            metrics_data.append(['Data Quality Score', f"{quality_score}%", 'Assessed'])
        
        # Create and style table
        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
            ('TOPPADDING', (0, 0), (-1, 0), 15),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
        ]))
        
        story.append(metrics_table)
        story.append(Spacer(1, 25))

    def _add_business_insights(self, story, data):
        """Add business insights section"""
        story.append(Paragraph("Key Business Insights", self.styles['SectionHeader']))
        
        if 'insights' in data and data['insights']:
            for i, insight in enumerate(data['insights'], 1):
                story.append(Paragraph(f"{i}. {insight}", self.styles['KeyInsight']))
        else:
            story.append(Paragraph("Insights generated based on your specific data patterns.", self.styles['Normal']))
        
        story.append(Spacer(1, 20))

    def _add_data_quality_analysis(self, story, data):
        """Add comprehensive data quality analysis"""
        story.append(Paragraph("Data Quality Analysis", self.styles['SectionHeader']))
        
        if 'cleaning' in data:
            cleaning = data['cleaning']
            
            # Quality overview
            story.append(Paragraph("Quality Assessment Overview", self.styles['SubsectionHeader']))
            
            quality_data = [
                ['Quality Factor', 'Count', 'Impact Level', 'Recommendation'],
                ['Missing Values', str(cleaning.get('missing_values', 0)), 
                 'High' if cleaning.get('missing_values', 0) > 10 else 'Low',
                 'Address missing data' if cleaning.get('missing_values', 0) > 0 else 'Good'],
                ['Duplicate Records', str(cleaning.get('duplicates', 0)),
                 'Medium' if cleaning.get('duplicates', 0) > 5 else 'Low',
                 'Remove duplicates' if cleaning.get('duplicates', 0) > 0 else 'Good'],
                ['Data Outliers', str(cleaning.get('outliers', 0)),
                 'Medium' if cleaning.get('outliers', 0) > 0 else 'Low',
                 'Review outliers' if cleaning.get('outliers', 0) > 0 else 'Good'],
                ['Data Types', cleaning.get('data_types', 'Analyzed'), 'Low', 'Properly formatted']
            ]
            
            quality_table = Table(quality_data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 2.3*inch])
            quality_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC2626')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FEF2F2')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#FECACA')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))
            
            story.append(quality_table)
        
        story.append(Spacer(1, 20))

    def _add_growth_analytics(self, story, growth_data):
        """Add growth analytics section"""
        story.append(Paragraph("Growth Analytics", self.styles['SectionHeader']))
        
        # Revenue prediction
        if 'revenue_prediction' in growth_data:
            story.append(Paragraph("Revenue Trend Analysis", self.styles['SubsectionHeader']))
            prediction = growth_data['revenue_prediction']
            story.append(Paragraph(f"• {prediction.get('summary', 'Revenue analysis completed')}", self.styles['KeyInsight']))
            if 'trend' in prediction:
                story.append(Paragraph(f"• Trend Direction: {prediction['trend']}", self.styles['KeyInsight']))
        
        # Top products
        if 'top_products' in growth_data:
            story.append(Paragraph("Top Performing Products", self.styles['SubsectionHeader']))
            products = growth_data['top_products'].get('products', [])
            for i, product in enumerate(products[:5], 1):
                story.append(Paragraph(f"{i}. {product.get('name', 'Product')} - Revenue: ${product.get('revenue', 0):,.2f}", self.styles['KeyInsight']))
        
        story.append(Spacer(1, 20))

    def _add_advanced_analytics(self, story, advanced_data):
        """Add advanced analytics section"""
        story.append(Paragraph("Advanced Analytics", self.styles['SectionHeader']))
        
        # Customer segmentation
        if 'segmentation' in advanced_data:
            story.append(Paragraph("Customer Segmentation Analysis", self.styles['SubsectionHeader']))
            segments = advanced_data['segmentation'].get('segments', {})
            for segment_name, segment_data in segments.items():
                story.append(Paragraph(f"• {segment_name}: {segment_data.get('percentage', 0):.1f}% of customers", self.styles['KeyInsight']))
        
        # Forecasting
        if 'forecast' in advanced_data:
            story.append(Paragraph("Sales Forecasting", self.styles['SubsectionHeader']))
            forecast = advanced_data['forecast']
            story.append(Paragraph(f"• {forecast.get('summary', 'Forecast analysis completed')}", self.styles['KeyInsight']))
        
        story.append(Spacer(1, 20))

    def _add_recommendations(self, story, data):
        """Add AI-powered recommendations"""
        story.append(Paragraph("Strategic Recommendations", self.styles['SectionHeader']))
        
        if 'personalized' in data and data['personalized']:
            story.append(Paragraph("Based on your data analysis, here are our key recommendations:", self.styles['Normal']))
            story.append(Spacer(1, 10))
            
            for i, recommendation in enumerate(data['personalized'], 1):
                story.append(Paragraph(f"{i}. {recommendation}", self.styles['KeyInsight']))
        else:
            story.append(Paragraph("Personalized recommendations generated based on your specific business data.", self.styles['Normal']))
        
        story.append(Spacer(1, 20))

    def _add_sample_data(self, story, sample_data):
        """Add sample data preview"""
        story.append(Paragraph("Data Preview", self.styles['SectionHeader']))
        story.append(Paragraph("Sample of your analyzed data:", self.styles['Normal']))
        story.append(Spacer(1, 10))
        
        # Create table with first 5 rows
        sample_rows = sample_data.head(5)
        table_data = [list(sample_rows.columns)]
        
        for _, row in sample_rows.iterrows():
            formatted_row = []
            for val in row:
                str_val = str(val)
                if len(str_val) > 20:
                    str_val = str_val[:17] + "..."
                formatted_row.append(str_val)
            table_data.append(formatted_row)
        
        # Adjust column widths based on number of columns
        num_cols = len(table_data[0])
        col_width = 6.5 / num_cols
        
        data_table = Table(table_data, colWidths=[col_width*inch] * num_cols)
        data_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#EFF6FF')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#DBEAFE')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        story.append(data_table)
        story.append(Spacer(1, 20))

    def _add_footer(self, story, report_id, client_email):
        """Add professional footer"""
        story.append(Spacer(1, 30))
        story.append(Paragraph("─" * 80, self.styles['Footer']))
        story.append(Spacer(1, 10))
        
        footer_text = f"Smart Data Analyzer • Professional Business Intelligence Platform<br/>"
        footer_text += f"Report ID: {report_id} • Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
        if client_email:
            footer_text += f"Delivered to: {client_email}<br/>"
        footer_text += "For support or questions, contact our analytics team."
        
        story.append(Paragraph(footer_text, self.styles['Footer']))