import os
import sys

# Set up environment before any imports
os.environ['FLASK_ENV'] = 'development'
os.environ['PYTHONUNBUFFERED'] = '1'

# Configure library paths for NumPy compatibility
import glob

# Find actual Nix store paths for libraries
nix_lib_paths = []
for pattern in ['/nix/store/*/lib', '/nix/store/*/lib64']:
    nix_lib_paths.extend(glob.glob(pattern))

lib_paths = nix_lib_paths + [
    '/usr/lib',
    '/usr/lib64', 
    '/lib',
    '/lib64'
]

# Add existing LD_LIBRARY_PATH if it exists
existing_path = os.environ.get('LD_LIBRARY_PATH', '')
if existing_path:
    lib_paths.append(existing_path)

os.environ['LD_LIBRARY_PATH'] = ':'.join(lib_paths)

try:
    from app import app
    print("Full Smart Data Analyzer loaded")
except Exception as e:
    print(f"Loading minimal app: {e}")
    from minimal_app import app

if __name__ == '__main__':
    print("Starting Smart Data Analyzer on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
