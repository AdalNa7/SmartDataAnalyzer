import os
import glob
import subprocess

# Set comprehensive library path before importing app to fix numpy dependencies
def setup_library_environment():
    """Configure LD_LIBRARY_PATH to include all necessary C++ libraries"""
    # Find all lib directories in nix store
    lib_paths = []
    
    # Use find command to locate libstdc++.so.6 specifically
    try:
        result = subprocess.run(['find', '/nix/store', '-name', 'libstdc++.so.6', '-type', 'f'], 
                              capture_output=True, text=True, timeout=10)
        if result.stdout.strip():
            # Add the directory containing libstdc++.so.6
            libstdcxx_path = result.stdout.strip().split('\n')[0]
            lib_paths.append(os.path.dirname(libstdcxx_path))
    except:
        pass
    
    # Add all lib and lib64 directories
    for pattern in ["/nix/store/*/lib", "/nix/store/*/lib64"]:
        lib_paths.extend(glob.glob(pattern))
    
    # Filter existing paths and set environment
    existing_paths = [p for p in lib_paths if os.path.exists(p)]
    if existing_paths:
        current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
        new_ld_path = ':'.join(existing_paths)
        if current_ld_path:
            new_ld_path = f"{new_ld_path}:{current_ld_path}"
        os.environ['LD_LIBRARY_PATH'] = new_ld_path

# Setup environment before any imports
setup_library_environment()

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
