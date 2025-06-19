import os
import subprocess
import glob

# Configure library path before importing NumPy-dependent modules
def setup_cpp_libraries():
    """Set up LD_LIBRARY_PATH to include C++ standard library"""
    lib_dirs = set()
    
    # Priority 1: Find libstdc++.so.6 specifically
    try:
        result = subprocess.run(['find', '/nix/store', '-name', 'libstdc++.so.6', '-type', 'f'], 
                              capture_output=True, text=True, timeout=8)
        if result.stdout.strip():
            for lib_path in result.stdout.strip().split('\n')[:3]:
                if lib_path:
                    lib_dirs.add(os.path.dirname(lib_path))
    except:
        pass
    
    # Priority 2: Find zlib library
    try:
        result = subprocess.run(['find', '/nix/store', '-name', 'libz.so*', '-type', 'f'], 
                              capture_output=True, text=True, timeout=5)
        if result.stdout.strip():
            for lib_path in result.stdout.strip().split('\n')[:2]:
                if lib_path and 'libz.so' in lib_path:
                    lib_dirs.add(os.path.dirname(lib_path))
    except:
        pass
    
    # Priority 3: Add gcc library paths
    for pattern in ["/nix/store/*gcc*/lib", "/nix/store/*gcc*/lib64"]:
        paths = glob.glob(pattern)
        for path in paths[:5]:
            if os.path.exists(path):
                lib_dirs.add(path)
    
    # Priority 4: Add standard system library directories
    for pattern in ["/nix/store/*/lib", "/nix/store/*/lib64"]:
        paths = glob.glob(pattern)
        for path in paths[:10]:  # Limit to prevent timeout
            if os.path.exists(path):
                lib_dirs.add(path)
    
    if lib_dirs:
        current_ld = os.environ.get('LD_LIBRARY_PATH', '')
        new_ld_path = ':'.join(sorted(lib_dirs))
        if current_ld:
            new_ld_path = f"{new_ld_path}:{current_ld}"
        os.environ['LD_LIBRARY_PATH'] = new_ld_path
        print(f"Configured {len(lib_dirs)} library paths for NumPy")
        return True
    
    print("No library paths found")
    return False

# Setup libraries before any imports
setup_cpp_libraries()

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
