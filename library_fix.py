#!/usr/bin/env python3
"""
Comprehensive library path fix for NumPy dependencies
"""
import os
import subprocess
import glob

def find_required_libraries():
    """Find libstdc++.so.6 and libz.so.1 in the system"""
    libraries = {}
    
    # Find libstdc++.so.6
    try:
        result = subprocess.run(['find', '/nix/store', '-name', 'libstdc++.so.6', '-type', 'f'], 
                              capture_output=True, text=True, timeout=20)
        if result.stdout.strip():
            lib_path = result.stdout.strip().split('\n')[0]
            libraries['libstdc++'] = os.path.dirname(lib_path)
            print(f"Found libstdc++.so.6 at: {lib_path}")
    except:
        pass
    
    # Find libz.so.1
    try:
        result = subprocess.run(['find', '/nix/store', '-name', 'libz.so.1', '-type', 'f'], 
                              capture_output=True, text=True, timeout=15)
        if result.stdout.strip():
            lib_path = result.stdout.strip().split('\n')[0]
            libraries['libz'] = os.path.dirname(lib_path)
            print(f"Found libz.so.1 at: {lib_path}")
    except:
        pass
    
    return libraries

def setup_complete_environment():
    """Setup comprehensive LD_LIBRARY_PATH"""
    lib_dirs = set()
    
    # Get required libraries
    required_libs = find_required_libraries()
    for lib_name, lib_dir in required_libs.items():
        lib_dirs.add(lib_dir)
    
    # Add standard lib paths
    for pattern in ["/nix/store/*/lib", "/nix/store/*/lib64"]:
        paths = glob.glob(pattern)
        for path in paths[:15]:  # Limit to prevent timeout
            if os.path.exists(path):
                lib_dirs.add(path)
    
    if lib_dirs:
        current_ld = os.environ.get('LD_LIBRARY_PATH', '')
        new_ld_path = ':'.join(sorted(lib_dirs))
        if current_ld:
            new_ld_path = f"{new_ld_path}:{current_ld}"
        
        os.environ['LD_LIBRARY_PATH'] = new_ld_path
        print(f"Set LD_LIBRARY_PATH with {len(lib_dirs)} directories")
        return True
    
    return False

if __name__ == "__main__":
    if setup_complete_environment():
        try:
            import numpy
            import pandas
            print(f"SUCCESS: NumPy {numpy.__version__}, Pandas {pandas.__version__}")
        except Exception as e:
            print(f"Import failed: {e}")
    else:
        print("Failed to setup library environment")