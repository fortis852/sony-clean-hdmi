#!/bin/bash

echo "🔧 Setting up Sony Clean HDMI development environment..."
echo "======================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create project structure
echo -e "${YELLOW}Creating project structure...${NC}"
mkdir -p {sdk,lib,build,gen,docs,tests}
mkdir -p src/main/java/com/cleanhdmi
mkdir -p src/main/resources/{layout,values,drawable}
mkdir -p scripts

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip3 install --user pmca-py pyusb pytest requests

# Clone OpenMemories Framework if not exists
if [ ! -d "sdk/OpenMemories-Framework" ]; then
    echo -e "${YELLOW}Cloning OpenMemories Framework...${NC}"
    git clone https://github.com/ma1co/OpenMemories-Framework.git sdk/OpenMemories-Framework
fi

# Download Android build tools (lightweight version)
if [ ! -d "sdk/android-tools" ]; then
    echo -e "${YELLOW}Setting up Android tools...${NC}"
    mkdir -p sdk/android-tools
    cd sdk/android-tools
    
    # Download necessary tools
    wget -q https://github.com/ma1co/OpenMemories-SDK/raw/master/tools/apktool.jar
    wget -q https://github.com/ma1co/OpenMemories-SDK/raw/master/tools/signapk.jar
    
    cd ../..
fi

# Setup environment variables
echo -e "${YELLOW}Setting up environment variables...${NC}"
echo 'export PROJECT_ROOT=/workspace' >> ~/.bashrc
echo 'export ANDROID_TOOLS=$PROJECT_ROOT/sdk/android-tools' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_TOOLS' >> ~/.bashrc
source ~/.bashrc

# Create initial configuration file
echo -e "${YELLOW}Creating default configuration...${NC}"
cat > config.json << 'EOF'
{
  "camera": {
    "model": "DSC-HX400",
    "apiVersion": "1.0"
  },
  "defaults": {
    "autoFocus": false,
    "exposureLock": true,
    "showGrid": false,
    "hdmiInfo": false,
    "startupMode": "clean"
  },
  "controls": {
    "menuButton": "toggle_ui",
    "fnButton": "focus_lock",
    "upButton": "exposure_plus",
    "downButton": "exposure_minus"
  }
}
EOF

echo -e "${GREEN}✅ Environment setup complete!${NC}"
echo -e "${GREEN}You can now run 'make build' to build the application${NC}"
