#!/usr/bin/env python3
import os
import glob
import sys

# Set up environment for NumPy before any imports
def configure_environment():
    """Configure LD_LIBRARY_PATH for NumPy C extensions"""
    lib_paths = []
    
    # Add all library directories from Nix store
    for pattern in ["/nix/store/*/lib", "/nix/store/*/lib64"]:
        paths = glob.glob(pattern)
        lib_paths.extend(paths[:20])  # Limit to prevent excessive paths
    
    if lib_paths:
        current_ld = os.environ.get('LD_LIBRARY_PATH', '')
        new_ld_path = ':'.join(lib_paths)
        if current_ld:
            new_ld_path = f"{new_ld_path}:{current_ld}"
        os.environ['LD_LIBRARY_PATH'] = new_ld_path
        print(f"Configured {len(lib_paths)} library paths")

# Configure environment
configure_environment()

# Import and run app
try:
    from app import app
    print("Smart Data Analyzer loaded successfully")
    app.run(host='0.0.0.0', port=5000, debug=True)
except Exception as e:
    print(f"Error starting app: {e}")
    # Fallback to minimal app
    from minimal_app import app
    print("Using minimal app fallback")
    app.run(host='0.0.0.0', port=5000, debug=True)