#!/bin/bash
# Smart Data Analyzer startup script with library path fixes

echo "Setting up library paths for numpy/pandas..."

# Find all library paths in nix store
export LD_LIBRARY_PATH="$(find /nix/store -name "lib" -type d 2>/dev/null | head -20 | tr '\n' ':')$(find /nix/store -name "lib64" -type d 2>/dev/null | head -10 | tr '\n' ':')$LD_LIBRARY_PATH"

echo "Starting Smart Data Analyzer..."
cd /home/runner/workspace

# Start with Python development server
exec python wsgi.py