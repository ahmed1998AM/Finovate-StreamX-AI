#!/bin/bash
# Finovate StreamX AI - Build Script for Windows
# ================================================
# Builds standalone executable using Nuitka with UPX compression
#
# Developer: Ahmed Mostafa Ibrahim
# Brand: Finovate – AHMED EG

set -e

echo "=============================================="
echo "  Finovate StreamX AI - Build Script"
echo "  Developer: Ahmed Mostafa Ibrahim"
echo "=============================================="
echo ""

# Configuration
APP_NAME="Finovate_StreamX_AI"
VERSION="1.0.0"
OUTPUT_DIR="dist"
BUILD_DIR="build"
ICON_FILE="assets/icon.ico"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
echo "Python version: $python_version"

# Check required packages
echo -e "${YELLOW}Checking required packages...${NC}"
pip show PySide6 > /dev/null 2>&1 || { echo -e "${RED}PySide6 not installed${NC}"; exit 1; }
pip show python-vlc > /dev/null 2>&1 || { echo -e "${RED}python-vlc not installed${NC}"; exit 1; }
pip show cryptography > /dev/null 2>&1 || { echo -e "${RED}cryptography not installed${NC}"; exit 1; }
echo -e "${GREEN}All required packages found${NC}"

# Create output directory
mkdir -p "$OUTPUT_DIR"
mkdir -p "$BUILD_DIR"

echo ""
echo -e "${YELLOW}Starting Nuitka compilation...${NC}"
echo ""

# Nuitka build command with optimizations
python -m nuitka \
    --standalone \
    --onefile \
    --windows-disable-console \
    --windows-icon-from-ico="$ICON_FILE" \
    --enable-plugin=pyside6 \
    --enable-plugin=upx \
    --upx-cache-compression-level=best \
    --lto=yes \
    --recurse-not-to=tests \
    --recurse-not-to=.git \
    --include-package=core \
    --include-package=ui \
    --include-package=player \
    --include-package=iptv \
    --include-package=database \
    --include-package=ai \
    --include-package=agents \
    --include-package=plugins \
    --include-package=services \
    --include-package=settings \
    --include-package=updater \
    --include-module=aiohttp \
    --include-module=requests \
    --include-module=cryptography \
    --include-module=langchain \
    --output-dir="$OUTPUT_DIR" \
    --output-filename="$APP_NAME.exe" \
    main.py

# Check if build succeeded
if [ -f "$OUTPUT_DIR/$APP_NAME.exe" ]; then
    echo ""
    echo -e "${GREEN}=============================================="
    echo "  Build Successful!"
    echo "==============================================${NC}"
    
    # Get file size
    file_size=$(du -h "$OUTPUT_DIR/$APP_NAME.exe" | cut -f1)
    echo ""
    echo "Output file: $OUTPUT_DIR/$APP_NAME.exe"
    echo "File size: $file_size"
    echo "Version: $VERSION"
    echo ""
    echo -e "${YELLOW}Build completed successfully!${NC}"
else
    echo -e "${RED}Build failed! Output file not found.${NC}"
    exit 1
fi

echo ""
echo "=============================================="
echo "  Build Summary"
echo "=============================================="
echo "Application: $APP_NAME"
echo "Version: $VERSION"
echo "Output: $OUTPUT_DIR/$APP_NAME.exe"
echo "Developer: Ahmed Mostafa Ibrahim"
echo "Brand: Finovate – AHMED EG"
echo "=============================================="
