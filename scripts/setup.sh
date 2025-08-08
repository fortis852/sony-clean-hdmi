#!/bin/bash

# Setup script for local development

echo "Setting up Sony Clean HDMI development environment..."

# Check Java
if ! command -v java &> /dev/null; then
    echo "❌ Java not found. Please install JDK 11+"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Install Python packages
pip3 install --user pmca-py pyusb pytest

# Create directories
mkdir -p sdk lib build gen docs tests

# Clone required repositories
if [ ! -d "sdk/OpenMemories-Framework" ]; then
    git clone https://github.com/ma1co/OpenMemories-Framework.git sdk/OpenMemories-Framework
fi

echo "✅ Setup complete!"
