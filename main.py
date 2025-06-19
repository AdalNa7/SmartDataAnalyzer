import os
import sys

# Set up clean environment
os.environ['FLASK_ENV'] = 'development'
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['PYTHONPATH'] = ''

# Configure library paths for NumPy
lib_paths = [
    '/nix/store/4w85zw8hd3j2y89fm1j40wgh4kpjgxy7-gcc-12.3.0-lib/lib',
    '/nix/store/k7zgvzp2r31zkg9xqgjim7mbknryv6bs-glibc-2.39-52/lib'
]
current_ld = os.environ.get('LD_LIBRARY_PATH', '')
os.environ['LD_LIBRARY_PATH'] = ':'.join(lib_paths + [current_ld] if current_ld else lib_paths)

try:
    from app import app
    print("Full Smart Data Analyzer loaded")
except Exception as e:
    print(f"Loading minimal app: {e}")
    from minimal_app import app

if __name__ == '__main__':
    print("Starting Smart Data Analyzer on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
