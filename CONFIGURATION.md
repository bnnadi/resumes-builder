# Configuration Guide

## Overview

Resume Builder now includes a comprehensive configuration system that allows you to customize paths, settings, and preferences without editing code.

## Quick Start

### First-Time Setup

Run the interactive setup wizard:

```bash
resume-builder setup
```

This will walk you through configuring:
- **Resume directory**: Where you keep your resumes
- **Output directory**: Where customized resumes are saved  
- **Base resume**: Your master/base resume file
- **Skills inventory**: Location of your skills database

### View Current Configuration

```bash
resume-builder config list
```

Output:
```
======================================================================
  Resume Builder Configuration
======================================================================

📁 Resume Paths:
  Primary:      ~/Documents/resumes
  Applications: ~/Documents/resumes/applications
  Fallback:     ~/Documents
  Base Resume:  ~/Documents/resumes/master-resume.md

🤖 Ollama Configuration:
  URL:         http://localhost:11434
  Model:       llama3.1
  Temperature: 0.7

📊 Thresholds:
  Minimum:     70
  Borderline:  60-69

📤 Output:
  Directory:   ~/Documents/resumes/applications

📝 Config File: ~/.config/resume-builder/config.yaml
```

## Configuration Commands

### resume-builder config list

Show all configuration values

```bash
resume-builder config list
# or
resume-builder config show
```

### resume-builder config set

Set a configuration value

```bash
# Set resume directory
resume-builder config set resume-path ~/my-resumes

# Set base resume
resume-builder config set base-resume ~/my-resumes/master-resume.md

# Set output directory
resume-builder config set output-dir ~/my-resumes/applications

# Change AI model
resume-builder config set model mistral

# Change minimum match score
resume-builder config set min-score 75
```

**Available keys:**
- `resume-path` - Primary resume directory
- `base-resume` - Path to your master resume
- `output-dir` - Where to save customized resumes
- `model` - Ollama model name
- `min-score` - Minimum match score threshold

### resume-builder config get

Get a single configuration value

```bash
resume-builder config get model
# Output: llama3.1

resume-builder config get resume-path
# Output: ~/Documents/resumes
```

### resume-builder config validate

Validate that configured paths exist

```bash
resume-builder config validate
```

Output:
```
======================================================================
  Path Validation
======================================================================

✓ resume_primary      ~/Documents/resumes
✓ resume_applications ~/Documents/resumes/applications
✓ output_dir          ~/Documents/resumes/applications
✓ base_resume         ~/Documents/resumes/master-resume.md

✅ All paths valid!
```

### resume-builder config path

Show config file location

```bash
resume-builder config path
# Output: ~/.config/resume-builder/config.yaml
```

## Configuration Files

### Locations (Priority Order)

1. **User config** (highest priority):  
   `~/.config/resume-builder/config.yaml`
   - Your personal settings
   - Created by `resume-builder setup`
   - Overrides project defaults

2. **Project config**:  
   `./config/settings.yaml`
   - Default settings
   - Shared across installations
   - Template for new users

3. **Built-in defaults**:
   - Hardcoded fallbacks if no config exists

### Configuration Structure

```yaml
# ~/.config/resume-builder/config.yaml

# Resume paths
resume_paths:
  primary: "~/Documents/resumes"
  applications: "~/Documents/resumes/applications"
  fallback: "~/Documents"
  base_resume: "~/Documents/resumes/master-resume.md"

# Ollama AI configuration
ollama:
  base_url: "http://localhost:11434"
  model: "llama3.1"
  temperature: 0.7
  timeout: 180

# Threshold settings
thresholds:
  minimum_overall: 70
  borderline_min: 60
  borderline_max: 69
  auto_stop_below: true
  ask_on_borderline: true

# Export settings
export:
  auto_validate: true
  create_package: true
  default_format: "docx"

# Output settings
output:
  base_dir: "~/Documents/resumes/applications"
  create_subdirs: true
  preserve_existing: true

# Skills inventory
skills_inventory: "~/.config/resume-builder/skills_inventory.yaml"

# General
verbose: true
```

## Common Workflows

### Scenario 1: New User Setup

```bash
# 1. Install resume builder
pip install -e .

# 2. Run setup
resume-builder setup

# 3. Verify configuration
resume-builder config list

# 4. Test with a job
resume-builder workflow job-posting.txt
```

### Scenario 2: Change Resume Location

```bash
# Update resume path
resume-builder config set resume-path ~/Dropbox/resumes

# Update base resume
resume-builder config set base-resume ~/Dropbox/resumes/master.md

# Validate new paths
resume-builder config validate
```

### Scenario 3: Use Different AI Model

```bash
# Switch to Mistral
resume-builder config set model mistral

# Verify change
resume-builder config get model

# Use in workflow
resume-builder workflow job.txt
```

### Scenario 4: Change Match Threshold

```bash
# Set higher bar (only excellent matches)
resume-builder config set min-score 80

# Or lower bar (more permissive)
resume-builder config set min-score 65

# Verify
resume-builder config list
```

## Troubleshooting

### "No base resume found"

**Problem**: System can't find your master resume

**Solutions**:
```bash
# Option 1: Set it explicitly
resume-builder config set base-resume ~/path/to/your/master-resume.md

# Option 2: Re-run setup
resume-builder setup

# Option 3: Specify on command line
resume-builder workflow job.txt --base-resume ~/path/to/resume.md
```

### "Path validation failed"

**Problem**: Configured paths don't exist

**Solutions**:
```bash
# Check which paths are invalid
resume-builder config validate

# Fix invalid paths
resume-builder config set resume-path ~/correct/path

# Or re-run setup
resume-builder setup
```

### "First time setup required"

**Problem**: No user configuration exists

**Solution**:
```bash
resume-builder setup
```

### Want to reset to defaults?

**Solution**:
```bash
# Delete user config
rm ~/.config/resume-builder/config.yaml

# Re-run setup
resume-builder setup
```

## Advanced Configuration

### Manual Config Editing

You can edit the config file directly:

```bash
# Open in your editor
vim ~/.config/resume-builder/config.yaml
# or
code ~/.config/resume-builder/config.yaml
```

### Multiple Configurations

You can maintain multiple configs for different scenarios:

```bash
# Save current config
cp ~/.config/resume-builder/config.yaml ~/config-work.yaml

# Use different config
cp ~/config-personal.yaml ~/.config/resume-builder/config.yaml

# Resume builder will use the active config
resume-builder config list
```

### Environment-Specific Settings

For different environments (work, personal, etc.):

```yaml
# work-config.yaml
resume_paths:
  primary: "~/work/resumes"
  base_resume: "~/work/resumes/work-resume.md"
output:
  base_dir: "~/work/applications"

# personal-config.yaml
resume_paths:
  primary: "~/personal/resumes"
  base_resume: "~/personal/resumes/personal-resume.md"
output:
  base_dir: "~/personal/applications"
```

## Integration with Existing Workflows

### With resume-skills

Skills inventory location is configurable:

```bash
# Default location
resume-skills list

# Set custom location
resume-builder config set skills-inventory ~/my-skills.yaml
```

### With CI/CD

For automated workflows:

```bash
# Use non-interactive setup
resume-builder setup --non-interactive

# Or set via environment
export RESUME_BASE_DIR=~/resumes
export RESUME_BASE_FILE=~/resumes/master.md
```

## FAQ

**Q: Where is my config file stored?**  
A: Run `resume-builder config path` to see the location (typically `~/.config/resume-builder/config.yaml`)

**Q: Can I use environment variables?**  
A: Yes, paths like `~/Documents` automatically expand to your home directory

**Q: What happens if I don't run setup?**  
A: The system uses project defaults from `config/settings.yaml`, but you'll be prompted to run setup on first use

**Q: Can I share my config with teammates?**  
A: Yes, but adjust paths to their system. Better to share `config/settings.yaml` as a template

**Q: Does changing config affect existing customized resumes?**  
A: No, only affects where new resumes are saved and found

---

**Version**: Added in v0.4.0  
**See also**: [README.md](README.md), [QUICKSTART.md](QUICKSTART.md)

