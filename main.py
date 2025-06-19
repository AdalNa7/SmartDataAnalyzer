import os
import glob

# Fix numpy library path issue
lib_paths = []
for pattern in ["/nix/store/*/lib", "/nix/store/*/lib64"]:
    lib_paths.extend(glob.glob(pattern))

existing_paths = [p for p in lib_paths if os.path.exists(p)]
if existing_paths:
    current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
    new_ld_path = ':'.join(existing_paths)
    if current_ld_path:
        new_ld_path = f"{new_ld_path}:{current_ld_path}"
    os.environ['LD_LIBRARY_PATH'] = new_ld_path

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
