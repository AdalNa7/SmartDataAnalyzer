# Try to load the full app with NumPy dependencies, fallback to minimal app
try:
    import os
    import subprocess
    import glob
    
    # Configure library path before importing NumPy-dependent modules
    def setup_cpp_libraries():
        """Set up LD_LIBRARY_PATH to include C++ standard library"""
        lib_dirs = set()
        
        # Find libstdc++.so.6 specifically
        try:
            result = subprocess.run(['find', '/nix/store', '-name', 'libstdc++.so.6', '-type', 'f'], 
                                  capture_output=True, text=True, timeout=8)
            if result.stdout.strip():
                for lib_path in result.stdout.strip().split('\n')[:3]:
                    if lib_path:
                        lib_dirs.add(os.path.dirname(lib_path))
        except:
            pass
        
        # Add standard library directories
        for pattern in ["/nix/store/*/lib", "/nix/store/*/lib64"]:
            paths = glob.glob(pattern)
            for path in paths[:10]:
                if os.path.exists(path):
                    lib_dirs.add(path)
        
        if lib_dirs:
            current_ld = os.environ.get('LD_LIBRARY_PATH', '')
            new_ld_path = ':'.join(sorted(lib_dirs))
            if current_ld:
                new_ld_path = f"{new_ld_path}:{current_ld}"
            os.environ['LD_LIBRARY_PATH'] = new_ld_path
            return True
        return False

    # Setup libraries
    setup_cpp_libraries()
    
    # Try to import full app
    from app import app
    print("Full Smart Data Analyzer loaded successfully")
    
except ImportError as e:
    print(f"NumPy dependency issue detected, loading minimal app: {e}")
    # Fallback to minimal app without NumPy dependencies
    from minimal_app import app
    print("Minimal Smart Data Analyzer loaded (file upload functional)")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
