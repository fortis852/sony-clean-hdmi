# Makefile for Sony Clean HDMI

.PHONY: help setup build package clean deploy test run-checks

# Default target
help:
	@echo "Sony Clean HDMI - Build System"
	@echo "=============================="
	@echo "Available targets:"
	@echo "  setup      - Set up development environment"
	@echo "  build      - Build the application"
	@echo "  package    - Create APK package"
	@echo "  clean      - Clean build artifacts"
	@echo "  deploy     - Deploy to camera via USB"
	@echo "  test       - Run tests"
	@echo "  run-checks - Run code quality checks"

# Setup development environment
setup:
	@echo "🔧 Setting up development environment..."
	@bash scripts/setup.sh
	@echo "✅ Setup complete!"

# Build application
build: clean
	@echo "🏗️ Building application..."
	@mkdir -p build/classes
	@echo "Compiling Java sources..."
	@javac -cp "lib/*:sdk/lib/*" -d build/classes src/main/java/com/cleanhdmi/*.java
	@echo "✅ Build successful!"

# Create APK package
package: build
	@echo "📦 Creating APK package..."
	@bash scripts/package.sh
	@echo "✅ APK created: build/CleanHDMI.apk"

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/* gen/* out/*
	@echo "✅ Clean complete!"

# Deploy to camera
deploy: package
	@echo "📱 Deploying to camera..."
	@python3 scripts/deploy.py
	@echo "✅ Deployment complete!"

# Run tests
test:
	@echo "🧪 Running tests..."
	@python3 -m pytest tests/ -v
	@echo "✅ All tests passed!"

# Run code quality checks
run-checks:
	@echo "🔍 Running code quality checks..."
	@bash scripts/check-code.sh
	@echo "✅ Code checks passed!"

# Install dependencies
deps:
	@pip3 install -r requirements.txt
