"""
Intelligent Column Mapping for Smart Data Analyzer
Automatically detects and maps various column name patterns to standard fields
"""

import pandas as pd
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

class ColumnMapper:
    def __init__(self):
        # Define comprehensive column mapping patterns
        self.column_patterns = {
            'product': [
                'product', 'product_name', 'productname', 'item', 'item_name', 'itemname',
                'description', 'product_description', 'name', 'title', 'sku', 'product_id',
                'productid', 'item_id', 'itemid', 'product_code', 'model', 'part_number',
                'service', 'service_name', 'goods', 'merchandise', 'article'
            ],
            'quantity': [
                'quantity', 'qty', 'amount', 'amount_sold', 'units', 'units_sold',
                'count', 'number', 'sold', 'volume', 'pieces', 'pcs', 'ordered',
                'quantity_sold', 'sales_quantity', 'unit_count', 'total_units'
            ],
            'price': [
                'price', 'unit_price', 'unitprice', 'cost', 'unit_cost', 'unitcost',
                'sale_price', 'saleprice', 'selling_price', 'sellingprice', 'amount',
                'value', 'rate', 'fee', 'charge', 'total', 'subtotal', 'net_price',
                'gross_price', 'list_price', 'retail_price'
            ],
            'date': [
                'date', 'order_date', 'orderdate', 'sale_date', 'saledate', 'timestamp',
                'datetime', 'created_at', 'sold_at', 'purchased_at', 'transaction_date',
                'transactiondate', 'time', 'created', 'modified', 'updated', 'when',
                'delivery_date', 'invoice_date', 'billing_date'
            ]
        }
        
        # Date format patterns to try
        self.date_formats = [
            '%Y-%m-%d',      # ISO: 2023-12-25
            '%Y/%m/%d',      # 2023/12/25
            '%d/%m/%Y',      # UK: 25/12/2023
            '%m/%d/%Y',      # US: 12/25/2023
            '%d-%m-%Y',      # 25-12-2023
            '%m-%d-%Y',      # 12-25-2023
            '%Y-%m-%d %H:%M:%S',  # With time
            '%Y/%m/%d %H:%M:%S',
            '%d/%m/%Y %H:%M:%S',
            '%m/%d/%Y %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',  # ISO with T
        ]
    
    def detect_column_mapping(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Automatically detect column mappings from DataFrame
        Returns mapping result with confidence scores and suggestions
        """
        result = {
            'mappings': {},
            'confidence': {},
            'errors': [],
            'suggestions': {},
            'preview': {}
        }
        
        # Get actual column names from DataFrame
        actual_columns = list(df.columns)
        
        # Handle case where columns are unnamed (like "Unnamed: 0", "Unnamed: 1") or numeric
        if any('Unnamed:' in str(col) or str(col).isdigit() for col in actual_columns):
            print(f"ColumnMapper: Detected problematic columns: {actual_columns}")
            
            # Find the first row with meaningful data to use as headers
            header_row_idx = None
            for i in range(min(10, len(df))):
                row = df.iloc[i]
                non_null_values = row.dropna().astype(str).tolist()
                clean_values = [v.strip() for v in non_null_values if v.strip() and v != 'nan']
                
                if len(clean_values) >= 3 and not all(v.isdigit() for v in clean_values):
                    header_row_idx = i
                    print(f"ColumnMapper: Found potential headers at row {i}: {clean_values}")
                    break
            
            if header_row_idx is not None:
                # Use this row as headers
                header_row = df.iloc[header_row_idx]
                new_columns = [str(col).strip() if str(col) != 'nan' else f'Col_{i}' for i, col in enumerate(header_row)]
                
                # Create new DataFrame starting from the row after headers
                new_df = df.iloc[header_row_idx + 1:].copy()
                new_df.columns = new_columns[:len(new_df.columns)]
                new_df = new_df.reset_index(drop=True)
                
                # Remove completely empty rows and columns
                new_df = new_df.dropna(how='all').dropna(axis=1, how='all')
                
                print(f"ColumnMapper: Created cleaned DataFrame with shape {new_df.shape}")
                print(f"ColumnMapper: New columns: {list(new_df.columns)}")
                
                if len(new_df) > 0 and len(new_df.columns) >= 3:
                    return self.detect_column_mapping(new_df)
            
            # If we can't find good headers, create a meaningful error
            result['errors'].append("Unable to detect proper column headers in the uploaded file")
            result['suggestions'] = {
                'help': 'Please ensure your file has clear column headers and data'
            }
            return result
        
        print(f"ColumnMapper: Processing columns: {actual_columns}")
        
        # Try to map each required field
        for field_type, patterns in self.column_patterns.items():
            best_match, confidence = self._find_best_match(actual_columns, patterns)
            
            if best_match:
                result['mappings'][field_type] = best_match
                result['confidence'][field_type] = confidence
                result['preview'][field_type] = self._get_column_preview(df, best_match)
            else:
                result['errors'].append(f"Could not find '{field_type}' column")
                result['suggestions'][field_type] = self._suggest_alternatives(actual_columns, patterns)
        
        # Validate date column if found
        if 'date' in result['mappings']:
            date_validation = self._validate_date_column(df, result['mappings']['date'])
            result['date_format'] = date_validation
        
        return result
    
    def _find_best_match(self, columns: List[str], patterns: List[str]) -> Tuple[Optional[str], float]:
        """Find the best matching column name with confidence score"""
        best_match = None
        best_score = 0.0
        
        for col in columns:
            col_clean = col.lower().strip().replace(' ', '_').replace('-', '_')
            
            for pattern in patterns:
                # Exact match gets highest score
                if col_clean == pattern:
                    return col, 1.0
                
                # Partial match scoring
                if pattern in col_clean:
                    score = len(pattern) / len(col_clean)
                    if score > best_score:
                        best_score = score
                        best_match = col
                
                # Fuzzy matching for close variations
                similarity = self._calculate_similarity(col_clean, pattern)
                if similarity > 0.8 and similarity > best_score:
                    best_score = similarity
                    best_match = col
        
        # Only return matches with reasonable confidence
        return (best_match, best_score) if best_score > 0.5 else (None, 0.0)
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        # Simple Levenshtein-like similarity
        if len(str1) == 0 or len(str2) == 0:
            return 0.0
        
        # Count common characters
        common = 0
        for char in str1:
            if char in str2:
                common += 1
        
        return common / max(len(str1), len(str2))
    
    def _suggest_alternatives(self, columns: List[str], patterns: List[str]) -> List[str]:
        """Suggest possible alternative column names"""
        suggestions = []
        for col in columns:
            col_clean = col.lower().strip()
            for pattern in patterns[:5]:  # Top 5 patterns only
                if any(word in col_clean for word in pattern.split('_')):
                    suggestions.append(col)
                    break
        return suggestions[:3]  # Return top 3 suggestions
    
    def _get_column_preview(self, df: pd.DataFrame, column_name: str) -> Dict[str, Any]:
        """Get preview of column data"""
        try:
            col_data = df[column_name].dropna()
            if len(col_data) == 0:
                return {'sample': [], 'type': 'empty'}
            
            sample_size = min(5, len(col_data))
            return {
                'sample': col_data.head(sample_size).tolist(),
                'type': str(col_data.dtype),
                'null_count': df[column_name].isnull().sum(),
                'unique_count': col_data.nunique()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _validate_date_column(self, df: pd.DataFrame, date_column: str) -> Dict[str, Any]:
        """Validate and detect date format"""
        try:
            sample_dates = df[date_column].dropna().head(10).astype(str)
            detected_format = None
            success_rate = 0.0
            
            for date_format in self.date_formats:
                try:
                    successful_parses = 0
                    for date_str in sample_dates:
                        try:
                            datetime.strptime(date_str, date_format)
                            successful_parses += 1
                        except:
                            continue
                    
                    current_rate = successful_parses / len(sample_dates)
                    if current_rate > success_rate:
                        success_rate = current_rate
                        detected_format = date_format
                        
                    # If we get high success rate, stop searching
                    if success_rate > 0.8:
                        break
                        
                except Exception:
                    continue
            
            return {
                'format': detected_format,
                'confidence': success_rate,
                'parseable': success_rate > 0.5
            }
            
        except Exception as e:
            return {'error': str(e), 'parseable': False}
    
    def apply_mapping(self, df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
        """Apply the column mapping and return standardized DataFrame"""
        try:
            # Create a copy to avoid modifying original
            result_df = df.copy()
            
            # Rename columns according to mapping
            rename_dict = {original: standard for standard, original in mapping.items()}
            result_df = result_df.rename(columns=rename_dict)
            
            # Process date column if present
            if 'date' in result_df.columns:
                result_df['date'] = self._standardize_dates(result_df['date'])
                # Remove rows with invalid dates
                result_df = result_df.dropna(subset=['date'])
            
            # Ensure numeric columns are properly typed
            for col in ['quantity', 'price']:
                if col in result_df.columns:
                    result_df[col] = pd.to_numeric(result_df[col], errors='coerce')
            
            # Calculate revenue if possible
            if 'quantity' in result_df.columns and 'price' in result_df.columns:
                result_df['revenue'] = result_df['quantity'] * result_df['price']
            
            return result_df
            
        except Exception as e:
            raise ValueError(f"Error applying column mapping: {str(e)}")
    
    def _standardize_dates(self, date_series: pd.Series) -> pd.Series:
        """Convert various date formats to standard datetime"""
        # Try pandas built-in parsing first
        try:
            return pd.to_datetime(date_series, errors='coerce')
        except:
            pass
        
        # Try our custom formats
        for date_format in self.date_formats:
            try:
                return pd.to_datetime(date_series, format=date_format, errors='coerce')
            except:
                continue
        
        # If all else fails, let pandas do its best
        return pd.to_datetime(date_series, errors='coerce')
    
    def validate_required_fields(self, mapping: Dict[str, str]) -> Tuple[bool, List[str]]:
        """Validate that all required fields are mapped"""
        required_fields = ['product', 'quantity', 'price', 'date']
        missing_fields = []
        
        for field in required_fields:
            if field not in mapping or not mapping[field]:
                missing_fields.append(field)
        
        return len(missing_fields) == 0, missing_fields