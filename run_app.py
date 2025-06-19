#!/usr/bin/env python3
"""
Smart Data Analyzer startup with comprehensive library path fixes
"""
import os
import subprocess
import sys
import ctypes
import ctypes.util

def find_and_set_library_path():
    """Find libstdc++.so.6 and set proper library path"""
    # Try to find libstdc++.so.6 using find command
    try:
        result = subprocess.run(['find', '/nix/store', '-name', 'libstdc++.so.6', '-type', 'f'], 
                              capture_output=True, text=True, timeout=30)
        if result.stdout.strip():
            libstdcxx_path = result.stdout.strip().split('\n')[0]
            lib_dir = os.path.dirname(libstdcxx_path)
            
            # Set LD_LIBRARY_PATH
            current_ld = os.environ.get('LD_LIBRARY_PATH', '')
            new_ld = f"{lib_dir}:{current_ld}" if current_ld else lib_dir
            os.environ['LD_LIBRARY_PATH'] = new_ld
            
            print(f"Found libstdc++.so.6 at: {libstdcxx_path}")
            print(f"Set LD_LIBRARY_PATH: {lib_dir}")
            return True
    except:
        pass
    
    # Fallback: try to use ctypes to find the library
    try:
        libstdcxx = ctypes.util.find_library('stdc++')
        if libstdcxx:
            lib_dir = os.path.dirname(libstdcxx)
            current_ld = os.environ.get('LD_LIBRARY_PATH', '')
            new_ld = f"{lib_dir}:{current_ld}" if current_ld else lib_dir
            os.environ['LD_LIBRARY_PATH'] = new_ld
            print(f"Found libstdc++ via ctypes at: {libstdcxx}")
            return True
    except:
        pass
    
    return False

def test_numpy_import():
    """Test if numpy can be imported successfully"""
    try:
        import numpy
        import pandas
        print(f"Success: NumPy {numpy.__version__}, Pandas {pandas.__version__}")
        return True
    except Exception as e:
        print(f"Import failed: {e}")
        return False

def main():
    print("Smart Data Analyzer - Fixing dependencies...")
    
    # Set library path
    if find_and_set_library_path():
        print("Library path configured successfully")
    else:
        print("Warning: Could not configure optimal library path")
    
    # Test imports
    if test_numpy_import():
        print("Starting Flask application...")
        
        # Import and run Flask app
        try:
            from app import app
            app.run(host='0.0.0.0', port=5000, debug=True)
        except Exception as e:
            print(f"Failed to start Flask app: {e}")
            return 1
    else:
        print("Failed to import numpy/pandas dependencies")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())