import os
import sys

# Set up environment before any imports
os.environ['FLASK_ENV'] = 'development'
os.environ['PYTHONUNBUFFERED'] = '1'

# Critical: Remove any numpy-related directories from current working directory
import shutil
for item in os.listdir('.'):
    if 'numpy' in item.lower() and os.path.isdir(item):
        try:
            shutil.rmtree(item)
            print(f"Removed numpy conflict: {item}")
        except:
            pass

# Temporarily change to /tmp during imports to avoid source directory conflicts
original_cwd = os.getcwd()
os.chdir('/tmp')

# Clean and configure environment
sys.path = [p for p in sys.path if not ('numpy' in p and 'site-packages' not in p)]
os.environ['OPENBLAS_NUM_THREADS'] = '1'

try:
    from app import app
    print("Full Smart Data Analyzer loaded")
except Exception as e:
    print(f"Loading minimal app: {e}")
    from minimal_app import app

if __name__ == '__main__':
    print("Starting Smart Data Analyzer on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
