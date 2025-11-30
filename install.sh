#!/bin/bash
#
# ATS Resume Export System - Installation Script
#
# This script installs the resume export application and sets up
# the command-line interface.
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Header
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║        ATS Resume Export System - Installation Script        ║"
echo "║                       Version 0.1.0                           ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
print_info "Checking Python installation..."
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD=python3.12
    print_success "Found Python 3.12"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [[ "$PYTHON_VERSION" == "3.12" ]]; then
        PYTHON_CMD=python3
        print_success "Found Python 3.12"
    else
        print_warning "Python 3.12 recommended, found Python $PYTHON_VERSION"
        PYTHON_CMD=python3
    fi
else
    print_error "Python 3.12+ is required but not found"
    echo "Please install Python 3.12 or higher:"
    echo "  macOS: brew install python@3.12"
    echo "  Linux: apt-get install python3.12"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create virtual environment
print_info "Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists, skipping creation"
else
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip -q
print_success "pip upgraded"

# Install dependencies
print_info "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
    print_success "Dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Install package in development mode
print_info "Installing resume_export package..."
pip install -e . -q
print_success "Package installed"

# Make bin scripts executable
if [ -d "bin" ]; then
    print_info "Making scripts executable..."
    chmod +x bin/*
    print_success "Scripts are executable"
fi

# Test installation
print_info "Testing installation..."
if command -v export-resume &> /dev/null; then
    VERSION=$(export-resume --version 2>&1)
    print_success "Installation successful: $VERSION"
else
    print_error "Installation test failed"
    exit 1
fi

# Installation complete
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              ✅ Installation Complete!                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

print_success "ATS Resume Export System is ready to use!"
echo ""
echo "To get started:"
echo ""
echo "  1. Activate the virtual environment:"
echo "     ${BLUE}source venv/bin/activate${NC}"
echo ""
echo "  2. Export a resume:"
echo "     ${BLUE}export-resume your-resume.md --validate --package${NC}"
echo ""
echo "  3. View help:"
echo "     ${BLUE}export-resume --help${NC}"
echo ""
echo "Quick Start Guide: ${BLUE}cat QUICKSTART.md${NC}"
echo "Full Documentation: ${BLUE}cat README.md${NC}"
echo ""
print_info "For updates and issues: https://github.com/bisikennadi/resumes-builder"
echo ""

