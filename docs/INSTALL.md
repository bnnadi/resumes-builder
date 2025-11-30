# Installation Guide

Complete installation instructions for the AI-Powered Resume Builder.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Install](#quick-install)
- [Detailed Install](#detailed-install)  
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Python:** 3.12 or higher
- **RAM:** 8GB recommended (4GB for Ollama + headroom)
- **Disk:** ~5GB (4GB for AI model + code)
- **OS:** macOS, Linux, or Windows

### Required Software

1. **Ollama** - For local AI processing
2. **Python 3.12+** - For running the application
3. **pip** - Python package installer (included with Python)

---

## Quick Install

### Step 1: Install Ollama

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [ollama.ai/download](https://ollama.ai/download)

### Step 2: Pull AI Model

```bash
# Recommended: Llama 3.1 (4GB)
ollama pull llama3.1
```

### Step 3: Start Ollama

```bash
# Start in background
ollama serve &

# Or in separate terminal
ollama serve
```

**Verify Ollama is running:**
```bash
curl http://localhost:11434/api/tags
```

### Step 4: Install Resume Builder

```bash
cd /Users/bisikennadi/Projects/resumes-builder

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

### Step 5: Verify Installation

```bash
resume-builder --version
# Output: resume-builder 0.2.0
```

**Run test:**
```bash
./test_installation.sh
```

---

## Detailed Install

### Option 1: Automated Installation (Recommended)

```bash
cd /Users/bisikennadi/Projects/resumes-builder
./install.sh
```

This will:
- Create virtual environment
- Install all dependencies
- Install the package
- Verify installation

### Option 2: Using Make

```bash
make install
```

### Option 3: Manual Installation

**Step 1: Set up Python environment**
```bash
# Navigate to project
cd /Users/bisikennadi/Projects/resumes-builder

# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify Python version
python --version
# Should show: Python 3.12.x
```

**Step 2: Install dependencies**
```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

**Step 3: Install package**
```bash
# Development install (editable)
pip install -e .

# Or production install
pip install .
```

**Step 4: Verify installation**
```bash
# Check command is available
which resume-builder

# Check version
resume-builder --version

# Check help
resume-builder --help
```

---

## Verification

### Test Ollama Connection

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# List installed models
ollama list

# Test model
ollama run llama3.1 "Hello"
```

### Test Resume Builder

```bash
# Run installation test
./test_installation.sh

# Check all commands
resume-builder --help
resume-builder job-match --help
resume-builder customize --help
resume-builder workflow --help
```

### Test with Sample Job

```bash
# Create test job posting
cat > test-job.txt << 'EOF'
Senior Backend Engineer

Requirements:
- 5+ years Python
- Django/Flask
- PostgreSQL
- AWS
EOF

# Run workflow
resume-builder workflow test-job.txt
```

---

## Troubleshooting

### Ollama Issues

#### "Cannot connect to Ollama"

**Problem:** Ollama not running

**Solution:**
```bash
# Check if running
ps aux | grep ollama

# Start if not running
ollama serve &

# Or in separate terminal
ollama serve
```

#### "Model not found"

**Problem:** Model not downloaded

**Solution:**
```bash
# List models
ollama list

# Pull missing model
ollama pull llama3.1
```

#### "Out of memory"

**Problem:** System running out of RAM

**Solution:**
- Close other applications
- Use smaller model:
  ```bash
  ollama pull llama3.1:8b  # Smaller 8B parameter version
  ```

### Python Issues

#### "resume-builder command not found"

**Problem:** Not in virtual environment or not installed

**Solution:**
```bash
# Activate virtual environment
cd /Users/bisikennadi/Projects/resumes-builder
source venv/bin/activate

# Reinstall if needed
pip install -e .
```

#### "Python version too old"

**Problem:** Python < 3.12

**Solution:**
```bash
# Install Python 3.12
brew install python@3.12  # macOS

# Or use pyenv
pyenv install 3.12.0
pyenv local 3.12.0
```

#### "ModuleNotFoundError"

**Problem:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
```

### Installation Issues

#### "Permission denied"

**Solution:**
```bash
# Don't use sudo - use virtual environment instead
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### "Disk space full"

**Problem:** Not enough space for AI model

**Solution:**
- Free up ~5GB disk space
- AI model is ~4GB
- Or use smaller model

### Performance Issues

#### "Generation is slow"

**Solutions:**
1. Use smaller/faster model:
   ```bash
   resume-builder workflow job.txt --model llama3.1:8b
   ```

2. Increase timeout in config:
   ```yaml
   # config/settings.yaml
   ollama:
     timeout: 300  # 5 minutes
   ```

3. Close other applications to free CPU/RAM

#### "System getting hot"

**Normal behavior:** AI generation is CPU-intensive

**Solutions:**
- Ensure good ventilation
- Close other applications
- Use smaller model
- Run during off-peak times

---

## Alternative Models

### Available Models

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| llama3.1:8b | 4GB | Fast | Good | Recommended for laptops |
| llama3.1 | 4GB | Medium | Better | Default choice |
| mistral | 4GB | Fast | Good | Alternative |
| mixtral | 26GB | Slow | Best | High-end workstations only |

### Installing Alternative Models

```bash
# Faster model for laptops
ollama pull llama3.1:8b

# Alternative model
ollama pull mistral

# High-quality (requires 32GB+ RAM)
ollama pull mixtral
```

### Using Different Models

```bash
# In command
resume-builder workflow job.txt --model mistral

# Or edit config/settings.yaml
ollama:
  model: "mistral"
```

---

## Updating

### Update Ollama

```bash
# macOS
brew upgrade ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

### Update Models

```bash
ollama pull llama3.1
```

### Update Resume Builder

```bash
cd /Users/bisikennadi/Projects/resumes-builder
git pull  # if using git
pip install -r requirements.txt
pip install -e .
```

---

## Uninstalling

### Remove Resume Builder

```bash
pip uninstall ats-resume-builder
```

### Remove Ollama

```bash
# Stop Ollama
pkill ollama

# macOS
brew uninstall ollama

# Linux
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /usr/local/bin/ollama
```

### Remove Models

```bash
# List models
ollama list

# Remove specific model
ollama rm llama3.1

# Remove all models (frees ~4GB per model)
ollama rm llama3.1 mistral mixtral
```

---

## Advanced Configuration

### Custom Ollama Host

If running Ollama on different machine:

```yaml
# config/settings.yaml
ollama:
  base_url: "http://192.168.1.100:11434"
```

### Environment Variables

```bash
# Custom Ollama host
export OLLAMA_HOST=http://localhost:11434

# Custom config path (future)
export RESUME_BUILDER_CONFIG=~/my-config.yaml
```

### Multiple Python Versions

Using pyenv:
```bash
pyenv install 3.12.0
pyenv local 3.12.0
python -m venv venv
source venv/bin/activate
```

---

## Next Steps

After installation:

1. **Read [QUICKSTART.md](QUICKSTART.md)** - Learn basic usage
2. **Read [NEXT_STEPS.md](NEXT_STEPS.md)** - Detailed getting started guide
3. **Test with sample job** - Try the workflow
4. **Configure settings** - Edit `config/settings.yaml`

---

## Support

**Installation issues?**
1. Run `./test_installation.sh` to diagnose
2. Check this troubleshooting section
3. Verify Ollama is running: `ollama list`
4. Check logs if available

**For Ollama-specific issues:** https://ollama.ai/docs

---

**Installation complete!** Ready to use. See [README.md](../README.md) for usage examples.
