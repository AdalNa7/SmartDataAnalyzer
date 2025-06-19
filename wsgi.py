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
    # Find libstdc++.so.6 specifically
    libstdcxx_found = False
    lib_paths = []
    
    # Check common nix store paths
    for pattern in ["/nix/store/*/lib", "/nix/store/*/lib64"]:
        paths = glob.glob(pattern)
        for path in paths:
            libstdcxx_file = os.path.join(path, "libstdc++.so.6")
            if os.path.exists(libstdcxx_file):
                lib_paths.insert(0, path)  # Prioritize paths with libstdc++
                libstdcxx_found = True
            elif os.path.exists(path):
                lib_paths.append(path)
    
    if lib_paths:
        current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
        new_ld_path = ':'.join(lib_paths)
        
        if current_ld_path:
            new_ld_path = f"{new_ld_path}:{current_ld_path}"
        
        os.environ['LD_LIBRARY_PATH'] = new_ld_path
        return libstdcxx_found
    return False

# Setup library paths immediately
setup_library_paths()

# Now import the Flask app
from app import app

# WSGI application
application = app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)