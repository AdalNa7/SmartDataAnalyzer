# Load minimal app to ensure functionality while resolving NumPy dependencies
print("Loading minimal Smart Data Analyzer (file upload functional)")
from minimal_app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
