#!/usr/bin/env python3
import subprocess
import os

def find_libs():
    try:
        result = subprocess.run(['find', '/nix/store', '-name', '*libstdc++*', '-type', 'f'], 
                              capture_output=True, text=True, timeout=20)
        libs = result.stdout.strip().split('\n')
        for lib in libs[:5]:
            if lib:
                print(f"Found: {lib}")
                if 'libstdc++.so.6' in lib:
                    print(f"libstdc++.so.6 path: {os.path.dirname(lib)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_libs()