# AI-Powered Resume Builder

Complete job application workflow with AI analysis, customization, and ATS-optimized export.

## Overview

Transform your job application process with AI-powered resume analysis and customization. This tool scores job fit, customizes resumes for specific roles, and exports to ATS-compliant .docx format - all in one command.

**Features:**
- 🤖 **AI Job Matching** - Score resume fit (0-100) and predict interview probability
- 🎯 **Smart Threshold** - Auto-stops on poor matches (< 70% score) to save time
- ✍️ **AI Customization** - Tailor resumes to specific jobs with keyword optimization
- 🎨 **Skills Inventory** - Maintain all your skills and intelligently add matching ones (NEW!)
- ✅ **ATS Export** - Generate properly formatted .docx files (Calibri 11pt, 1" margins)
- 📦 **Complete Package** - Resume, analysis, cover letter points, and checklist
- 🔒 **Private & Offline** - Uses local Ollama (no cloud, no API costs)

**Time Savings:** 28 minutes → 5 minutes per application (82% reduction)

## Quick Start

### Prerequisites

1. **Install Ollama:**
   ```bash
   brew install ollama  # macOS
   ```

2. **Pull AI model:**
   ```bash
   ollama pull llama3.1
   ```

3. **Start Ollama:**
   ```bash
   ollama serve &
   ```

### Installation

```bash
cd resumes-builder  # or your project directory
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

**Verify:**
```bash
resume-builder --version
# Output: resume-builder 0.3.0
```

**First-Time Setup:**
```bash
# Interactive setup wizard
resume-builder setup

# This will configure:
#  - Where your resumes are stored
#  - Where to save customized resumes
#  - Your base/master resume location
```

See [docs/INSTALL.md](docs/INSTALL.md) for detailed setup and troubleshooting.

## Usage

### Complete Workflow (Recommended)

```bash
# Analyze job, customize resume, export to .docx
resume-builder workflow job-posting.txt
```

**What happens:**
1. AI analyzes job match (~60 seconds)
2. Threshold check - stops if score < 70%
3. AI customizes resume (~3 minutes)
4. Exports to ATS-compliant .docx (~3 seconds)

**Output:**
```
applications/Company/
├── Company_Resume.docx           ⭐ SUBMIT THIS
├── Company_Analysis.md
├── Company_Cover_Letter_Points.md
└── Company_Application_Checklist.md
```

### Individual Commands

```bash
# Analyze job match only
resume-builder job-match job-posting.txt

# Customize resume only
resume-builder customize job-posting.txt --company Google

# Export only (traditional, no AI)
resume-builder export resume.md --validate --package

# Evaluate existing resumes
resume-builder eval
```

### Advanced Options

```bash
# Custom threshold
resume-builder workflow job.txt --min-score 80

# Force through regardless of score
resume-builder workflow job.txt --force

# Use different AI model
resume-builder workflow job.txt --model mistral
```

## Understanding Match Scores

| Score | Meaning | Action |
|-------|---------|--------|
| 85-100 | Excellent match | Definitely apply |
| 70-84 | Good match | Strong candidate |
| 60-69 | Borderline | Worth trying for reach companies |
| < 60 | Poor match | Focus elsewhere |

**Default 70% threshold** prevents wasting time on poor-fit jobs.

## Features in Detail

### AI Job Matching
- Analyzes resume against job requirements
- Scores technical skills, experience level, and seniority alignment
- Calculates ATS keyword match and pass probability
- Predicts interview likelihood based on fit

### Smart Threshold Gate
- Auto-stops on poor matches (< 70% by default)
- Asks on borderline matches (60-69%)
- Saves 20+ minutes per rejected application
- Configurable threshold in settings

### AI Customization
- Reorders sections for relevance
- Emphasizes matching skills and experience
- Optimizes keywords for ATS systems
- **Never fabricates** - only reorders existing content
- Keeps resume to 1-2 pages

### ATS-Compliant Export
- Proper fonts: Calibri/Arial 11pt
- Standard margins: 1 inch all sides
- No tables, images, or complex formatting
- Simple bullets and sections
- File size under 1MB
- Automatic validation

## Configuration

### Interactive Setup (Recommended)

```bash
# Run the setup wizard
resume-builder setup

# View current configuration
resume-builder config list

# Change specific settings
resume-builder config set resume-path ~/my-resumes
resume-builder config set base-resume ~/my-resumes/master.md
resume-builder config set output-dir ~/my-resumes/applications
resume-builder config set model mistral

# Validate paths
resume-builder config validate
```

### Manual Configuration

Edit `~/.config/resume-builder/config.yaml` or `config/settings.yaml`:

```yaml
# Resume paths
resume_paths:
  primary: "~/Documents/resumes"  # Where you keep resumes
  applications: "~/Documents/resumes/applications"  # Customized resumes
  base_resume: "~/Documents/resumes/master.md"  # Your master resume

# Ollama configuration
ollama:
  model: "llama3.1"  # or "mistral", "mixtral"
  temperature: 0.7

# Threshold settings
thresholds:
  minimum_overall: 70  # Match score minimum
  ask_on_borderline: true

# Output directory
output:
  base_dir: "~/Documents/resumes/applications"
```

## Commands Reference

### Main Commands
| Command | Description |
|---------|-------------|
| `workflow` | Complete workflow (match → customize → export) |
| `job-match` | Analyze job fit and score |
| `customize` | Customize resume for job |
| `eval` | Evaluate and compare resumes |
| `export` | Export to .docx (no AI) |
| `setup` | Interactive configuration wizard |
| `config` | Manage settings (list/set/get/validate) |

### Legacy Commands
| Command | Description |
|---------|-------------|
| `export-resume` | Traditional export (backward compatible) |

### Common Options
- `--min-score N` - Set minimum match score (default: 70)
- `--force` - Skip threshold check
- `--model NAME` - Choose Ollama model
- `--quiet` - Minimal output
- `--help` - Show help

## Performance

**Typical Times:**
- Job match analysis: 30-60 seconds
- Resume customization: 2-4 minutes
- Export to .docx: 2-3 seconds
- **Total workflow: 3-5 minutes**

**System Requirements:**
- Python 3.12+
- RAM: 8GB recommended (4GB for Ollama)
- Disk: ~5GB (4GB model + code)
- Ollama with llama3.1 model

## Troubleshooting

### "Cannot connect to Ollama"
```bash
# Check if running
ps aux | grep ollama

# Start Ollama
ollama serve &
```

### "Model not found"
```bash
ollama pull llama3.1
```

### Slow generation
```bash
# Use smaller/faster model
resume-builder workflow job.txt --model llama3.1:8b
```

See [docs/INSTALL.md](docs/INSTALL.md) for complete troubleshooting guide.

## Documentation

- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Quick start guide with examples
- **[docs/INSTALL.md](docs/INSTALL.md)** - Detailed installation and setup
- **[docs/NEXT_STEPS.md](docs/NEXT_STEPS.md)** - Getting started guide
- **[docs/DOCS.md](docs/DOCS.md)** - Complete documentation index
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

## Development

```bash
# Setup development environment
make install

# Run tests
make test

# Format code
make format

# Lint code
make lint
```

## Project Structure

```
resumes-builder/
├── src/
│   ├── resume_ai/          # AI-powered features
│   │   ├── ollama_client.py
│   │   ├── job_match.py
│   │   ├── resume_customize.py
│   │   ├── threshold_gate.py
│   │   └── prompts/
│   ├── resume_export/      # Traditional export
│   │   ├── parser.py
│   │   ├── docx_builder.py
│   │   └── exporters/
│   └── resume_builder_cli.py
├── config/
│   └── settings.yaml
└── memory-bank/            # Project documentation
```

## Examples

### Basic Workflow
```bash
resume-builder workflow google-swe.txt
```

### Batch Processing
```bash
for job in jobs/*.txt; do
    resume-builder workflow "$job" --min-score 70
done
```

### Skills Inventory Management (NEW!)

Maintain a central database of all your skills and let the AI intelligently suggest relevant ones:

```bash
# List all your skills
resume-skills list

# Check which skills match a job
resume-skills match job_posting.txt

# Add new skills
resume-skills add programming_languages "Rust"

# Find a specific skill
resume-skills find "Docker"
```

The skills are automatically integrated during resume customization - the AI will suggest relevant skills from your inventory and add them ONLY if there's evidence in your work experience.

**Conditional Skills**: Add notes for skills that should only appear in specific contexts (e.g., React Native only for mobile roles).

**Documentation**: See [docs/SKILLS_FEATURE.md](docs/SKILLS_FEATURE.md) for complete guide including setup, usage, and conditional skills examples.

### Custom Company and Threshold
```bash
resume-builder workflow job.txt \
    --company "Google" \
    --min-score 75 \
    --base-resume master-resume.md
```

## Why This Tool?

**Before (Manual):**
- 28 minutes per application
- Subjective job fit assessment
- Manual keyword optimization
- Tedious formatting

**After (AI-Powered):**
- 5 minutes per application
- Objective match scoring
- Automatic customization
- ATS-compliant export

**Result:** Focus on high-quality applications, not busy work.

## License

MIT License - See [LICENSE](LICENSE)

## Version

**Current Version:** 0.2.0
- Added AI-powered job matching
- Added smart threshold gating (70% default)
- Added AI resume customization
- Added resume evaluation
- Added complete workflow orchestration

See [CHANGELOG.md](CHANGELOG.md) for full history.

---

**Status:** ✅ Production Ready
**Last Updated:** November 27, 2025

For questions or issues, see [troubleshooting](#troubleshooting) or check [docs/INSTALL.md](docs/INSTALL.md).
