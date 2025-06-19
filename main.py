import os
import sys

# Set up environment
os.environ['FLASK_ENV'] = 'development'
os.environ['PYTHONUNBUFFERED'] = '1'

# Configure complete library path for NumPy
os.environ['LD_LIBRARY_PATH'] = '/nix/store/4w85zw8hd3j2y89fm1j40wgh4kpjgxy7-gcc-12.3.0-lib/lib:/nix/store/k7zgvzp2r31zkg9xqgjim7mbknryv6bs-glibc-2.39-52/lib:/nix/store/3n5j4b4x8ql91srrjwsq0f8x7f4c8jzn-zlib-1.3.1/lib:/nix/store/1ap8g92l5mjbn1z1bw1z0siq1g8fpnqa-openblas-0.3.27/lib'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
print("NumPy library configuration complete")

try:
    from app import app
    print("Full Smart Data Analyzer loaded")
except Exception as e:
    print(f"Loading minimal app: {e}")
    from minimal_app import app

if __name__ == '__main__':
    print("Starting Smart Data Analyzer on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
