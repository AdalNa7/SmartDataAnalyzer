import os
import sys

# Set up environment
os.environ['FLASK_ENV'] = 'development'
os.environ['PYTHONUNBUFFERED'] = '1'

# Configure comprehensive library paths
lib_paths = [
    '/nix/store/4w85zw8hd3j2y89fm1j40wgh4kpjgxy7-gcc-12.3.0-lib/lib',
    '/nix/store/k7zgvzp2r31zkg9xqgjim7mbknryv6bs-glibc-2.39-52/lib',
    '/nix/store/1ap8g92l5mjbn1z1bw1z0siq1g8fpnqa-openblas-0.3.27/lib'
]

# Set library path for NumPy C extensions
existing_ld = os.environ.get('LD_LIBRARY_PATH', '')
all_paths = lib_paths + ([existing_ld] if existing_ld else [])
os.environ['LD_LIBRARY_PATH'] = ':'.join(all_paths)

print(f"NumPy library configuration: {len(lib_paths)} paths configured")

try:
    from app import app
    print("Full Smart Data Analyzer loaded")
except Exception as e:
    print(f"Loading minimal app: {e}")
    from minimal_app import app

if __name__ == '__main__':
    print("Starting Smart Data Analyzer on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
