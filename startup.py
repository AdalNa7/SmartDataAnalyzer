#!/usr/bin/env python3
"""
Startup script to fix library path issues and launch Smart Data Analyzer
"""
import os
import sys
import subprocess

# Set library path to include all Nix store libraries
def setup_environment():
    # Find all lib64 and lib directories in nix store
    nix_lib_paths = []
    try:
        # Get all lib directories from nix store
        result = subprocess.run(['find', '/nix/store', '-name', 'lib64', '-type', 'd'], 
                              capture_output=True, text=True, timeout=10)
        nix_lib_paths.extend(result.stdout.strip().split('\n'))
        
        result = subprocess.run(['find', '/nix/store', '-name', 'lib', '-type', 'd'], 
                              capture_output=True, text=True, timeout=10)
        nix_lib_paths.extend(result.stdout.strip().split('\n'))
    except:
        pass
    
    # Filter out empty paths and add to LD_LIBRARY_PATH
    valid_paths = [p for p in nix_lib_paths if p and os.path.exists(p)]
    current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
    
    new_ld_path = ':'.join(valid_paths)
    if current_ld_path:
        new_ld_path = f"{new_ld_path}:{current_ld_path}"
    
    os.environ['LD_LIBRARY_PATH'] = new_ld_path
    print(f"Set LD_LIBRARY_PATH with {len(valid_paths)} paths")

def test_imports():
    """Test if numpy and pandas can be imported"""
    try:
        import numpy
        import pandas
        print(f"✓ NumPy {numpy.__version__} loaded successfully")
        print(f"✓ Pandas {pandas.__version__} loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def main():
    print("Smart Data Analyzer - Setting up environment...")
    setup_environment()
    
    if test_imports():
        print("✓ All dependencies loaded successfully")
        print("Starting Flask application...")
        
        # Import and run the Flask app
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("✗ Dependency loading failed")
        sys.exit(1)

if __name__ == '__main__':
    main()