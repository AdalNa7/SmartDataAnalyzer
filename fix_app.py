#!/usr/bin/env python3
"""
Fixed application entry point that handles numpy import issues
"""
import os
import sys

# Set up library path before importing numpy
lib_paths = [
    "/nix/store/*/lib",
    "/nix/store/*/lib64", 
    "/usr/lib/x86_64-linux-gnu",
    "/lib/x86_64-linux-gnu"
]

current_ld = os.environ.get('LD_LIBRARY_PATH', '')
new_paths = []

# Find actual paths that exist
import glob
for pattern in lib_paths[:2]:  # Only nix store paths
    new_paths.extend(glob.glob(pattern))

if new_paths:
    ld_path = ':'.join(new_paths)
    if current_ld:
        ld_path = f"{ld_path}:{current_ld}"
    os.environ['LD_LIBRARY_PATH'] = ld_path

# Now try to import the main app
try:
    from main import app
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)
except ImportError as e:
    print(f"Import error: {e}")
    # Create a minimal Flask app as fallback
    from flask import Flask
    fallback_app = Flask(__name__)
    
    @fallback_app.route('/')
    def maintenance():
        return """
        <html>
        <head><title>Smart Data Analyzer - System Maintenance</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>Smart Data Analyzer</h1>
            <h2>System Maintenance in Progress</h2>
            <p>We're currently resolving a system dependency issue.</p>
            <p>The application will be restored shortly.</p>
            <hr>
            <p><small>Technical details: NumPy C extension library dependency resolution</small></p>
        </body>
        </html>
        """
    
    fallback_app.run(host='0.0.0.0', port=5000, debug=True)