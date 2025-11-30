#!/bin/bash
# Test Installation Script for AI-Powered Resume Builder

set -e

echo "============================================"
echo "Testing Resume Builder Installation"
echo "============================================"
echo

# Check Python version
echo "✓ Checking Python version..."
python3 --version
echo

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Not in virtual environment"
    echo "   Run: source venv/bin/activate"
    exit 1
fi
echo "✓ Virtual environment active"
echo

# Check Ollama is running
echo "✓ Checking Ollama connection..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama is running"
else
    echo "❌ Ollama not running"
    echo "   Run: ollama serve"
    exit 1
fi
echo

# Check model is available
echo "✓ Checking for llama3.1 model..."
if ollama list | grep -q "llama3.1"; then
    echo "✓ llama3.1 model found"
else
    echo "⚠️  llama3.1 not found"
    echo "   Run: ollama pull llama3.1"
fi
echo

# Check package is installed
echo "✓ Checking package installation..."
if command -v resume-builder &> /dev/null; then
    echo "✓ resume-builder command available"
    resume-builder --version
else
    echo "❌ resume-builder not installed"
    echo "   Run: pip install -e ."
    exit 1
fi
echo

# Check dependencies
echo "✓ Checking dependencies..."
python3 -c "import ollama" 2>/dev/null && echo "✓ ollama package installed" || echo "❌ ollama package missing"
python3 -c "import rich" 2>/dev/null && echo "✓ rich package installed" || echo "❌ rich package missing"
python3 -c "import docx" 2>/dev/null && echo "✓ python-docx package installed" || echo "❌ python-docx package missing"
echo

# Check file structure
echo "✓ Checking file structure..."
[ -d "src/resume_ai" ] && echo "✓ resume_ai/ directory exists" || echo "❌ resume_ai/ missing"
[ -f "src/resume_ai/ollama_client.py" ] && echo "✓ ollama_client.py exists" || echo "❌ ollama_client.py missing"
[ -f "src/resume_ai/prompts/job_match.txt" ] && echo "✓ prompt templates exist" || echo "❌ prompts missing"
[ -f "src/resume_builder_cli.py" ] && echo "✓ CLI exists" || echo "❌ CLI missing"
echo

# Check config
echo "✓ Checking configuration..."
[ -f "config/settings.yaml" ] && echo "✓ settings.yaml exists" || echo "⚠️  settings.yaml missing (optional)"
echo

echo "============================================"
echo "✅ Installation Test Complete!"
echo "============================================"
echo
echo "Ready to use! Try:"
echo "  resume-builder --help"
echo "  resume-builder job-match --help"
echo "  resume-builder workflow --help"
echo
