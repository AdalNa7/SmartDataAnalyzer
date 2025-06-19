import os
import sys

# Set up environment before any imports
os.environ['FLASK_ENV'] = 'development'
os.environ['PYTHONUNBUFFERED'] = '1'

# Clear any conflicting NumPy paths that might cause import issues
sys.path = [p for p in sys.path if 'numpy' not in p.lower() or '.pythonlibs' in p]

# Configure library paths for NumPy compatibility
import subprocess
import glob

# Find GCC library paths specifically
try:
    gcc_lib_path = subprocess.check_output(['find', '/nix/store', '-name', 'libstdc++.so.6', '-type', 'f'], 
                                         stderr=subprocess.DEVNULL, timeout=10).decode().strip().split('\n')[0]
    gcc_dir = os.path.dirname(gcc_lib_path)
    print(f"Found libstdc++.so.6 at: {gcc_dir}")
except:
    gcc_dir = None

# Find actual Nix store paths for libraries
nix_lib_paths = []
for pattern in ['/nix/store/*/lib', '/nix/store/*/lib64']:
    try:
        nix_lib_paths.extend(glob.glob(pattern)[:10])  # Limit to avoid too many paths
    except:
        pass

lib_paths = []
if gcc_dir:
    lib_paths.append(gcc_dir)
lib_paths.extend(nix_lib_paths[:5])  # Only use first 5 to avoid path length issues
lib_paths.extend(['/usr/lib', '/usr/lib64', '/lib', '/lib64'])

# Add existing LD_LIBRARY_PATH if it exists
existing_path = os.environ.get('LD_LIBRARY_PATH', '')
if existing_path:
    lib_paths.append(existing_path)

os.environ['LD_LIBRARY_PATH'] = ':'.join(lib_paths)
print(f"LD_LIBRARY_PATH configured with {len(lib_paths)} paths")

try:
    from app import app
    print("Full Smart Data Analyzer loaded")
except Exception as e:
    print(f"Loading minimal app: {e}")
    from minimal_app import app

if __name__ == '__main__':
    print("Starting Smart Data Analyzer on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
