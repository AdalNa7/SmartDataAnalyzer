import os
import sys

# Set up environment before any imports
os.environ['FLASK_ENV'] = 'development'
os.environ['PYTHONUNBUFFERED'] = '1'

try:
    from app import app
    print("Full Smart Data Analyzer loaded")
except Exception as e:
    print(f"Loading minimal app: {e}")
    from minimal_app import app

if __name__ == '__main__':
    print("Starting Smart Data Analyzer on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
