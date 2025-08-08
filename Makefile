.PHONY: all setup icons build apk clean test install help

help:
	@echo "Clean HDMI Build System"
	@echo "======================"
	@echo "  make setup  - Install dependencies"
	@echo "  make icons  - Generate app icons"
	@echo "  make build  - Compile Java sources"
	@echo "  make apk    - Create APK file"
	@echo "  make test   - Run tests"
	@echo "  make clean  - Clean build files"
	@echo "  make all    - Full build (icons + apk)"

all: icons apk

setup:
	@echo "📦 Installing dependencies..."
	pip3 install --user Pillow pyusb requests pytest
	@echo "✅ Setup complete"

icons:
	@echo "🎨 Generating icons..."
	python3 scripts/generate_icons.py

build:
	@echo "🔨 Building Java sources..."
	mkdir -p build/classes
	find src/main/java -name "*.java" | xargs javac -d build/classes -source 1.7 -target 1.7

apk: build
	@echo "📱 Creating APK..."
	chmod +x scripts/build_apk.sh
	./scripts/build_apk.sh

clean:
	@echo "🧹 Cleaning..."
	rm -rf build/ gen/ out/ keys/

test:
	@echo "🧪 Running tests..."
	python3 -m pytest tests/ -v

install: apk
	@echo "📲 Installing to device..."
	adb install -r build/apk/CleanHDMI.apk || echo "No device connected"
