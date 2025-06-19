#!/usr/bin/env python3
"""
WSGI entry point with proper library path setup for numpy/pandas
"""
import os
import glob
import sys

# Critical: Set library paths BEFORE any imports that might use numpy
def setup_library_paths():
    """Set up LD_LIBRARY_PATH to include all necessary C++ libraries"""
    lib_patterns = ["/nix/store/*/lib", "/nix/store/*/lib64"]
    lib_paths = []
    
    for pattern in lib_patterns:
        lib_paths.extend(glob.glob(pattern))
    
    # Filter existing paths
    existing_paths = [p for p in lib_paths if os.path.exists(p)]
    
    if existing_paths:
        current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
        new_ld_path = ':'.join(existing_paths)
        
        if current_ld_path:
            new_ld_path = f"{new_ld_path}:{current_ld_path}"
        
        os.environ['LD_LIBRARY_PATH'] = new_ld_path

# Setup library paths immediately
setup_library_paths()

# Now import the Flask app
from app import app

# WSGI application
application = app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)