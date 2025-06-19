#!/usr/bin/env python3
"""
Smart Data Analyzer startup script with library path fixes
"""
import os
import subprocess
import sys
import glob

def setup_library_path():
    """Setup LD_LIBRARY_PATH to include all necessary libraries"""
    # Find all lib directories in nix store
    lib_paths = []
    
    # Use glob to find lib directories
    nix_lib_patterns = [
        "/nix/store/*/lib",
        "/nix/store/*/lib64"
    ]
    
    for pattern in nix_lib_patterns:
        lib_paths.extend(glob.glob(pattern))
    
    # Filter existing paths
    existing_paths = [p for p in lib_paths if os.path.exists(p)]
    
    if existing_paths:
        current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
        new_ld_path = ':'.join(existing_paths)
        
        if current_ld_path:
            new_ld_path = f"{new_ld_path}:{current_ld_path}"
        
        os.environ['LD_LIBRARY_PATH'] = new_ld_path
        print(f"Set LD_LIBRARY_PATH with {len(existing_paths)} library paths")

def test_numpy_import():
    """Test if numpy can be imported successfully"""
    try:
        import numpy
        import pandas
        print(f"✓ NumPy {numpy.__version__} imported successfully")
        print(f"✓ Pandas {pandas.__version__} imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def main():
    print("Smart Data Analyzer - Starting application...")
    
    # Setup library paths
    setup_library_path()
    
    # Test dependencies
    if test_numpy_import():
        print("✓ All dependencies loaded successfully")
        
        # Import and start the Flask app
        try:
            from app import app
            print("Starting Flask application on 0.0.0.0:5000...")
            app.run(host='0.0.0.0', port=5000, debug=True)
        except Exception as e:
            print(f"Failed to start Flask app: {e}")
            sys.exit(1)
    else:
        print("✗ Dependency import failed")
        sys.exit(1)

if __name__ == '__main__':
    main()