import os
import sys

# Set up environment before any imports
os.environ['FLASK_ENV'] = 'development'
os.environ['PYTHONUNBUFFERED'] = '1'

# Critical: Remove any numpy directories from current working directory
import shutil
for item in os.listdir('.'):
    if 'numpy' in item.lower() and os.path.isdir(item):
        try:
            shutil.rmtree(item)
            print(f"Removed conflicting directory: {item}")
        except:
            pass

# Configure comprehensive library paths for NumPy
lib_paths = []
for path in ['/nix/store/4w85zw8hd3j2y89fm1j40wgh4kpjgxy7-gcc-12.3.0-lib/lib',
             '/nix/store/k7zgvzp2r31zkg9xqgjim7mbknryv6bs-glibc-2.39-52/lib',
             '/nix/store/1ap8g92l5mjbn1z1bw1z0siq1g8fpnqa-openblas-0.3.27/lib',
             '/usr/lib', '/lib']:
    if os.path.exists(path):
        lib_paths.append(path)

if lib_paths:
    os.environ['LD_LIBRARY_PATH'] = ':'.join(lib_paths)
    print(f"Configured {len(lib_paths)} library paths for NumPy")

try:
    from app import app
    print("Full Smart Data Analyzer loaded")
except Exception as e:
    print(f"Loading minimal app: {e}")
    from minimal_app import app

if __name__ == '__main__':
    print("Starting Smart Data Analyzer on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
