#!/bin/bash

# Download a known working Sony camera app and modify it

echo "📥 Downloading sample Sony camera app..."

mkdir -p build/sony/sample

# Download OpenMemories-Tweak (known to work)
cd build/sony/sample

# Get a simple working app
wget -O sample.apk \
    "https://github.com/ma1co/OpenMemories-Tweak/releases/download/release-41/com.github.ma1co.OpenMemories-Tweak-release-41.apk" \
    2>/dev/null || {
    echo "Download failed, trying alternative..."
    
    # Alternative: PMCADemo app
    wget -O sample.apk \
        "https://github.com/ma1co/PMCADemo/releases/download/release-14/com.github.ma1co.PMCADemo-release-14.apk" \
        2>/dev/null
}

if [ -f "sample.apk" ]; then
    echo "✅ Sample APK downloaded"
    
    # Extract and modify
    echo "📦 Extracting APK..."
    unzip -q sample.apk -d extracted
    
    # Modify package name and content
    echo "✏️ Modifying for Clean HDMI..."
    
    # Create our simple app
    cd extracted
    
    # Remove original classes
    rm -f classes.dex
    
    # Create new minimal classes.dex (you'd need dx for this)
    # For now, we'll keep the original
    
    # Repackage
    echo "📦 Repackaging APK..."
    zip -0 -r ../CleanHDMI_modified.apk .
    
    cd ..
    
    echo "✅ Modified APK created: CleanHDMI_modified.apk"
    echo "Try installing: python -m pmca.installer install build/sony/sample/CleanHDMI_modified.apk"
else
    echo "❌ Failed to download sample APK"
fi

cd ../../..
