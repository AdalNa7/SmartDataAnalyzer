#!/usr/bin/env python3
"""
Fix library path for numpy/pandas dependencies
"""
import os
import subprocess
import ctypes

def find_libstdcxx():
    """Find libstdc++.so.6 in the system"""
    # Method 1: Use find command
    try:
        result = subprocess.run(['find', '/nix/store', '-name', 'libstdc++.so*', '-type', 'f'], 
                              capture_output=True, text=True, timeout=15)
        if result.stdout.strip():
            for lib_path in result.stdout.strip().split('\n'):
                if 'libstdc++.so' in lib_path:
                    return os.path.dirname(lib_path)
    except:
        pass
    
    # Method 2: Check common gcc lib paths
    gcc_paths = subprocess.run(['find', '/nix/store', '-path', '*/gcc*/lib*', '-type', 'd'], 
                             capture_output=True, text=True, timeout=10)
    if gcc_paths.stdout.strip():
        for path in gcc_paths.stdout.strip().split('\n'):
            if os.path.exists(os.path.join(path, 'libstdc++.so.6')):
                return path
    
    return None

def setup_environment():
    """Setup LD_LIBRARY_PATH"""
    lib_dir = find_libstdcxx()
    if lib_dir:
        current_ld = os.environ.get('LD_LIBRARY_PATH', '')
        new_ld = f"{lib_dir}:{current_ld}" if current_ld else lib_dir
        os.environ['LD_LIBRARY_PATH'] = new_ld
        print(f"Set LD_LIBRARY_PATH: {lib_dir}")
        return True
    return False

if __name__ == "__main__":
    setup_environment()
    
    # Test numpy import
    try:
        import numpy
        import pandas
        print(f"Success: NumPy {numpy.__version__}, Pandas {pandas.__version__}")
    except Exception as e:
        print(f"Import still failing: {e}")