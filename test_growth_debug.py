#!/usr/bin/env python3
"""
Debug script for Growth Analytics issues
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from growth_analytics import GrowthAnalytics
    print("✓ GrowthAnalytics imported successfully")
except Exception as e:
    print(f"✗ Error importing GrowthAnalytics: {e}")
    sys.exit(1)

def create_sample_data():
    """Create sample data for testing"""
    dates = [datetime.now() - timedelta(days=30-i) for i in range(30)]
    data = []
    
    for i, date in enumerate(dates):
        data.append({
            'product': f'Product_{i % 5 + 1}',
            'quantity': np.random.randint(10, 100),
            'price': round(np.random.uniform(10, 100), 2),
            'date': date.strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(data)

def test_growth_analytics():
    """Test growth analytics with sample data"""
    print("\n=== Testing Growth Analytics ===")
    
    # Create sample data
    print("Creating sample data...")
    df = create_sample_data()
    print(f"Sample data created: {len(df)} rows, {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")
    print(f"Sample data:\n{df.head()}")
    
    try:
        # Initialize GrowthAnalytics
        print("\nInitializing GrowthAnalytics...")
        analytics = GrowthAnalytics(df)
        print("✓ GrowthAnalytics initialized successfully")
        
        # Test revenue prediction
        print("\nTesting revenue prediction...")
        revenue_result = analytics.predict_revenue_trend()
        print("✓ Revenue prediction successful")
        print(f"Growth rate: {revenue_result['growth_rate']}%")
        
        # Test top products
        print("\nTesting top products...")
        top_products = analytics.get_top_products()
        print("✓ Top products analysis successful")
        
        # Test best times
        print("\nTesting best times...")
        best_times = analytics.analyze_best_selling_times()
        print("✓ Best times analysis successful")
        
        # Test missed opportunities
        print("\nTesting missed opportunities...")
        missed_opps = analytics.find_missed_opportunities()
        print("✓ Missed opportunities analysis successful")
        
        # Test data quality
        print("\nTesting data quality...")
        data_quality = analytics.get_data_quality_summary()
        print("✓ Data quality analysis successful")
        
        # Test recommendations
        print("\nTesting AI recommendations...")
        recommendations = analytics.generate_ai_recommendations()
        print("✓ AI recommendations successful")
        
        print("\n=== All tests passed! ===")
        return True
        
    except Exception as e:
        print(f"\n✗ Error in growth analytics: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_real_data():
    """Test with real uploaded data if available"""
    print("\n=== Testing with Real Data ===")
    
    # Check for uploaded files
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        print("No uploads directory found")
        return False
    
    # Try with the valid sample file first
    test_file = os.path.join(uploads_dir, "sda_valid_sample.csv")
    if not os.path.exists(test_file):
        print(f"Valid sample file not found: {test_file}")
        return False
    
    print(f"Testing with file: {test_file}")
    
    try:
        df = pd.read_csv(test_file)
        
        print(f"Loaded data: {len(df)} rows, {len(df.columns)} columns")
        print(f"Columns: {list(df.columns)}")
        print(f"Sample data:\n{df.head()}")
        
        if df.empty:
            print("File is empty")
            return False
        
        # Test with real data
        analytics = GrowthAnalytics(df)
        revenue_result = analytics.predict_revenue_trend()
        print("✓ Real data test successful")
        return True
        
    except Exception as e:
        print(f"✗ Error with real data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Growth Analytics Debug Script")
    print("=" * 40)
    
    # Test with sample data
    sample_success = test_growth_analytics()
    
    # Test with real data
    real_success = test_with_real_data()
    
    print("\n" + "=" * 40)
    print("SUMMARY:")
    print(f"Sample data test: {'✓ PASSED' if sample_success else '✗ FAILED'}")
    print(f"Real data test: {'✓ PASSED' if real_success else '✗ FAILED'}")
    
    if not sample_success:
        print("\nThe issue is likely in the GrowthAnalytics class itself.")
    elif not real_success:
        print("\nThe issue is likely with the uploaded data format or content.")
    else:
        print("\nBoth tests passed. The issue might be in the web interface or session handling.") 