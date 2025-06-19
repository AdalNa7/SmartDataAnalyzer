import os
import sys

# Environment setup
os.environ['FLASK_ENV'] = 'development'
os.environ['PYTHONUNBUFFERED'] = '1'

# Configure C++ library path for NumPy
os.environ['LD_LIBRARY_PATH'] = '/nix/store/4w85zw8hd3j2y89fm1j40wgh4kpjgxy7-gcc-12.3.0-lib/lib:/nix/store/k7zgvzp2r31zkg9xqgjim7mbknryv6bs-glibc-2.39-52/lib:/nix/store/3n5j4b4x8ql91srrjwsq0f8x7f4c8jzn-zlib-1.3.1/lib'

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
    print("Starting Smart Data Analyzer on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
