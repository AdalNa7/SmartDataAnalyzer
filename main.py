import os
import sys

# Environment setup
os.environ['FLASK_ENV'] = 'development'
os.environ['PYTHONUNBUFFERED'] = '1'

# Test NumPy functionality before app startup  
try:
    import numpy as np
    import pandas as pd
    print(f"NumPy {np.__version__} and Pandas {pd.__version__} working")
    NUMPY_WORKING = True
except Exception:
    print("NumPy not available - using minimal app mode")
    NUMPY_WORKING = False

try:
    from app import app
    print("Full Smart Data Analyzer loaded")
except Exception as e:
    print(f"Loading minimal app: {e}")
    from minimal_app import app

if __name__ == '__main__':
    port = os.getenv('PORT', 3000)
    print("Starting Smart Data Analyzer on port" ,port)
    app.run(host='0.0.0.0', port=port, debug=False)
