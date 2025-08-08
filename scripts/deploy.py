#!/usr/bin/env python3

"""
Deploy script for installing app to Sony camera
"""

import sys
import os
import subprocess

try:
    import pmca.commands.installer as installer
except ImportError:
    print("❌ pmca-py not installed. Run: pip install pmca-py")
    sys.exit(1)

def main():
    apk_path = "build/CleanHDMI.apk"
    
    if not os.path.exists(apk_path):
        print(f"❌ APK not found: {apk_path}")
        print("Run 'make package' first")
        sys.exit(1)
    
    print("📱 Connecting to camera...")
    print("Make sure camera is connected via USB and in USB mode")
    
    try:
        # Install using pmca
        installer.install(apk_path)
        print("✅ App installed successfully!")
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
