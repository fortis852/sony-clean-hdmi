#!/bin/bash

# Quick build without Android SDK
echo "🚀 Quick build (Java only)..."

# Create build directory
mkdir -p build/quick

# Download minimal Android stub if needed
if [ ! -f "sdk/android-stub.jar" ]; then
    echo "Downloading Android stub..."
    mkdir -p sdk
    curl -L -o sdk/android-stub.jar \
        "https://github.com/Sable/android-platforms/raw/master/android-4/android.jar" \
        2>/dev/null || echo "Download failed, continuing..."
fi

# Compile Java files
echo "Compiling Java..."
find src/main/java -name "*.java" > build/sources.txt

if [ -f "sdk/android-stub.jar" ]; then
    javac -cp "sdk/android-stub.jar" \
          -d build/quick \
          -source 1.7 -target 1.7 \
          -Xlint:-options \
          @build/sources.txt
else
    echo "⚠️ No Android JAR, compilation may fail"
    javac -d build/quick \
          -source 1.7 -target 1.7 \
          @build/sources.txt
fi

echo "Creating JAR..."
cd build/quick
jar cf ../CleanHDMI.jar .
cd ../..

echo "✅ Build complete: build/CleanHDMI.jar"
