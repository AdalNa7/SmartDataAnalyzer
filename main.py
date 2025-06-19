import os
import glob
import subprocess

# Set comprehensive library path before importing app to fix numpy dependencies
def setup_library_environment():
    """Configure LD_LIBRARY_PATH to include all necessary C++ libraries"""
    lib_paths = []
    
    # Priority 1: Find GCC library paths which contain libstdc++
    try:
        result = subprocess.run(['find', '/nix/store', '-path', '*gcc*', '-name', '*libstdc*', '-type', 'f'], 
                              capture_output=True, text=True, timeout=15)
        if result.stdout.strip():
            for lib_file in result.stdout.strip().split('\n')[:5]:  # Limit to first 5 results
                lib_dir = os.path.dirname(lib_file)
                if lib_dir not in lib_paths:
                    lib_paths.append(lib_dir)
    except:
        pass
    
    # Priority 2: Find any libstdc++.so files
    try:
        result = subprocess.run(['find', '/nix/store', '-name', '*libstdc++*', '-type', 'f'], 
                              capture_output=True, text=True, timeout=10)
        if result.stdout.strip():
            for lib_file in result.stdout.strip().split('\n')[:3]:
                lib_dir = os.path.dirname(lib_file)
                if lib_dir not in lib_paths:
                    lib_paths.append(lib_dir)
    except:
        pass
    
    # Priority 3: Add standard lib directories
    for pattern in ["/nix/store/*/lib", "/nix/store/*/lib64"]:
        additional_paths = glob.glob(pattern)
        for path in additional_paths[:20]:  # Limit to prevent timeout
            if path not in lib_paths and os.path.exists(path):
                lib_paths.append(path)
    
    # Set environment if we found paths
    if lib_paths:
        current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
        new_ld_path = ':'.join(lib_paths)
        if current_ld_path:
            new_ld_path = f"{new_ld_path}:{current_ld_path}"
        os.environ['LD_LIBRARY_PATH'] = new_ld_path
        return len(lib_paths)
    return 0

# Setup environment before any imports
lib_count = setup_library_environment()
print(f"Configured {lib_count} library paths for NumPy/Pandas")

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
