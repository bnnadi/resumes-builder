# Makefile for ATS Resume Export System

.PHONY: help install clean test lint format run uninstall

# Default target
help:
	@echo "ATS Resume Export System - Available Commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install     Install the application and dependencies"
	@echo "  make uninstall   Remove installation"
	@echo ""
	@echo "Development:"
	@echo "  make clean       Remove build artifacts and cache"
	@echo "  make test        Run tests (when available)"
	@echo "  make lint        Run linters"
	@echo "  make format      Format code with black and isort"
	@echo ""
	@echo "Usage:"
	@echo "  make run FILE=resume.md     Export a resume"
	@echo "  make validate FILE=file.docx  Validate a .docx file"
	@echo ""

# Install application
install:
	@echo "🚀 Installing ATS Resume Export System..."
	@bash install.sh

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.coverage" -delete
	@find . -type d -name "*.pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned"

# Deep clean (including venv)
clean-all: clean
	@echo "🧹 Deep cleaning (including virtual environment)..."
	@rm -rf venv/
	@echo "✅ Deep clean complete"

# Run tests
test:
	@echo "🧪 Running tests..."
	@. venv/bin/activate && pytest tests/ -v

# Run linters
lint:
	@echo "🔍 Running linters..."
	@. venv/bin/activate && pylint resume_export/
	@. venv/bin/activate && mypy resume_export/

# Format code
format:
	@echo "✨ Formatting code..."
	@. venv/bin/activate && black resume_export/
	@. venv/bin/activate && isort resume_export/
	@echo "✅ Code formatted"

# Export a resume (usage: make run FILE=path/to/resume.md)
run:
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Error: FILE parameter required"; \
		echo "Usage: make run FILE=path/to/resume.md"; \
		exit 1; \
	fi
	@. venv/bin/activate && export-resume $(FILE) --validate --package

# Validate a file (usage: make validate FILE=path/to/file.docx)
validate:
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Error: FILE parameter required"; \
		echo "Usage: make validate FILE=path/to/file.docx"; \
		exit 1; \
	fi
	@. venv/bin/activate && export-resume --validate-only $(FILE)

# Uninstall
uninstall:
	@echo "🗑️  Uninstalling ATS Resume Export System..."
	@. venv/bin/activate && pip uninstall -y ats-resume-export || true
	@echo "✅ Uninstalled"

# Quick test with sample resume
demo:
	@echo "🎬 Running demo with Hillpointe resume..."
	@. venv/bin/activate && export-resume \
		/Users/bisikennadi/Research/resumes/applications/Hillpointe/Hillpointe_Bisike_Nnadi_Resume_2025.md \
		--validate --package

# Show version
version:
	@. venv/bin/activate && export-resume --version

# Show status
status:
	@echo "📊 ATS Resume Export System Status"
	@echo ""
	@if [ -d "venv" ]; then \
		echo "✅ Virtual environment: Installed"; \
	else \
		echo "❌ Virtual environment: Not installed"; \
	fi
	@if command -v export-resume &> /dev/null; then \
		echo "✅ CLI command: Available"; \
		. venv/bin/activate && export-resume --version; \
	else \
		echo "❌ CLI command: Not available"; \
	fi
	@echo ""

# Build distribution
build:
	@echo "🏗️  Building distribution packages..."
	@python -m build
	@echo "✅ Distribution packages created in dist/"

# Upload to PyPI
publish: build
	@echo "📦 Uploading to PyPI..."
	@twine upload dist/*
	@echo "✅ Published to PyPI"

# Test distribution
test-dist: build
	@echo "🧪 Testing distribution..."
	@python -m pip install --force-reinstall dist/*.whl
	@resume-builder --version
	@echo "✅ Distribution works"
