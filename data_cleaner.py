"""
Smart Data Cleaner for Sales Data
Detects and reports data quality issues in uploaded Excel/CSV files
"""
import pandas as pd
import numpy as np
from datetime import datetime

class SmartDataCleaner:
    def __init__(self, df):
        """Initialize with uploaded DataFrame"""
        if df is None or df.empty:
            raise ValueError("Data cleaner requires valid uploaded data")
        
        self.df = df.copy()
        self.issues = {}
        self.recommendations = []
        
    def analyze_data_quality(self):
        """Comprehensive data quality analysis"""
        self._detect_missing_values()
        self._detect_duplicates()
        self._detect_outliers()
        self._detect_invalid_formats()
        self._detect_negative_values()
        self._analyze_date_formats()
        self._generate_recommendations()
        
        return {
            'issues': self.issues,
            'recommendations': self.recommendations,
            'summary': self._generate_summary()
        }
    
    def _detect_missing_values(self):
        """Detect missing values in critical columns"""
        missing_data = self.df.isnull().sum()
        missing_pct = (missing_data / len(self.df) * 100).round(2)
        
        critical_missing = {}
        for col in self.df.columns:
            if missing_data[col] > 0:
                col_lower = col.lower()
                if any(keyword in col_lower for keyword in ['price', 'cost', 'amount', 'quantity', 'qty', 'product', 'item']):
                    critical_missing[col] = {
                        'count': int(missing_data[col]),
                        'percentage': float(missing_pct[col])
                    }
        
        if critical_missing:
            self.issues['missing_values'] = critical_missing
    
    def _detect_duplicates(self):
        """Detect duplicate records"""
        duplicate_count = self.df.duplicated().sum()
        if duplicate_count > 0:
            self.issues['duplicates'] = {
                'count': int(duplicate_count),
                'percentage': round(duplicate_count / len(self.df) * 100, 2)
            }
    
    def _detect_outliers(self):
        """Detect outliers in numeric columns using IQR method"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outliers = {}
        
        for col in numeric_cols:
            if 'price' in col.lower() or 'cost' in col.lower() or 'amount' in col.lower() or 'quantity' in col.lower():
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outlier_mask = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
                outlier_count = outlier_mask.sum()
                
                if outlier_count > 0:
                    outliers[col] = {
                        'count': int(outlier_count),
                        'percentage': round(outlier_count / len(self.df) * 100, 2),
                        'min_value': float(self.df[col].min()),
                        'max_value': float(self.df[col].max())
                    }
        
        if outliers:
            self.issues['outliers'] = outliers
    
    def _detect_invalid_formats(self):
        """Detect invalid data formats"""
        format_issues = {}
        
        # Check price/amount columns for non-numeric values
        for col in self.df.columns:
            col_lower = col.lower()
            if 'price' in col_lower or 'cost' in col_lower or 'amount' in col_lower:
                try:
                    numeric_values = pd.to_numeric(self.df[col], errors='coerce')
                    invalid_count = numeric_values.isnull().sum() - self.df[col].isnull().sum()
                    if invalid_count > 0:
                        format_issues[col] = {
                            'issue': 'Non-numeric values in price column',
                            'count': int(invalid_count)
                        }
                except:
                    pass
        
        if format_issues:
            self.issues['invalid_formats'] = format_issues
    
    def _detect_negative_values(self):
        """Detect negative values in price/quantity columns"""
        negative_issues = {}
        
        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['price', 'cost', 'amount', 'quantity', 'qty']):
                try:
                    numeric_col = pd.to_numeric(self.df[col], errors='coerce')
                    negative_count = (numeric_col < 0).sum()
                    zero_count = (numeric_col == 0).sum()
                    
                    if negative_count > 0 or (zero_count > 0 and 'price' in col_lower):
                        negative_issues[col] = {
                            'negative_count': int(negative_count),
                            'zero_count': int(zero_count) if 'price' in col_lower else 0
                        }
                except:
                    pass
        
        if negative_issues:
            self.issues['negative_zero_values'] = negative_issues
    
    def _analyze_date_formats(self):
        """Analyze date column formats"""
        date_issues = {}
        
        for col in self.df.columns:
            col_lower = col.lower()
            if 'date' in col_lower or 'time' in col_lower:
                try:
                    parsed_dates = pd.to_datetime(self.df[col], errors='coerce')
                    invalid_dates = parsed_dates.isnull().sum() - self.df[col].isnull().sum()
                    
                    if invalid_dates > 0:
                        date_issues[col] = {
                            'invalid_count': int(invalid_dates),
                            'sample_invalid': self.df[self.df[col].notna() & parsed_dates.isna()][col].head(3).tolist()
                        }
                except:
                    pass
        
        if date_issues:
            self.issues['date_format_issues'] = date_issues
    
    def _generate_recommendations(self):
        """Generate cleaning recommendations based on detected issues"""
        if 'missing_values' in self.issues:
            for col, data in self.issues['missing_values'].items():
                if data['percentage'] > 20:
                    self.recommendations.append(f"Consider removing column '{col}' - too many missing values ({data['percentage']:.1f}%)")
                else:
                    self.recommendations.append(f"Fill missing values in '{col}' column ({data['count']} missing)")
        
        if 'duplicates' in self.issues:
            self.recommendations.append(f"Remove {self.issues['duplicates']['count']} duplicate records to improve data accuracy")
        
        if 'outliers' in self.issues:
            for col, data in self.issues['outliers'].items():
                self.recommendations.append(f"Review outliers in '{col}' - {data['count']} values outside normal range")
        
        if 'negative_zero_values' in self.issues:
            for col, data in self.issues['negative_zero_values'].items():
                if data['negative_count'] > 0:
                    self.recommendations.append(f"Fix {data['negative_count']} negative values in '{col}' column")
                if data['zero_count'] > 0:
                    self.recommendations.append(f"Review {data['zero_count']} zero prices in '{col}' column")
        
        if 'invalid_formats' in self.issues:
            for col, data in self.issues['invalid_formats'].items():
                self.recommendations.append(f"Fix {data['count']} invalid format values in '{col}' column")
        
        if not self.recommendations:
            self.recommendations.append("Data quality is excellent - no major issues detected")
    
    def _generate_summary(self):
        """Generate overall data quality summary"""
        total_issues = sum(len(issue_data) if isinstance(issue_data, dict) else 1 for issue_data in self.issues.values())
        
        if total_issues == 0:
            quality_score = 100
            status = "Excellent"
        elif total_issues <= 3:
            quality_score = 85
            status = "Good"
        elif total_issues <= 6:
            quality_score = 70
            status = "Fair"
        else:
            quality_score = 50
            status = "Needs Attention"
        
        return {
            'quality_score': quality_score,
            'status': status,
            'total_issues': total_issues,
            'rows_analyzed': len(self.df),
            'columns_analyzed': len(self.df.columns)
        }
    
    def get_cleaned_suggestions(self):
        """Get specific cleaning action suggestions"""
        suggestions = []
        
        # Remove duplicates
        if 'duplicates' in self.issues:
            suggestions.append({
                'action': 'remove_duplicates',
                'description': f"Remove {self.issues['duplicates']['count']} duplicate rows",
                'impact': f"Reduces dataset from {len(self.df)} to {len(self.df) - self.issues['duplicates']['count']} rows"
            })
        
        # Fill missing values
        if 'missing_values' in self.issues:
            for col, data in self.issues['missing_values'].items():
                if data['percentage'] < 20:  # Only suggest filling if less than 20% missing
                    col_lower = col.lower()
                    if 'price' in col_lower or 'cost' in col_lower:
                        suggestions.append({
                            'action': 'fill_missing',
                            'column': col,
                            'description': f"Fill {data['count']} missing values with median price",
                            'method': 'median'
                        })
                    elif 'quantity' in col_lower:
                        suggestions.append({
                            'action': 'fill_missing',
                            'column': col,
                            'description': f"Fill {data['count']} missing quantities with 1",
                            'method': 'constant_1'
                        })
        
        return suggestions