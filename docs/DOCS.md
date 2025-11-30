# Documentation Index

Quick guide to all documentation files.

## 🚀 Getting Started (Read These First)

1. **[README.md](../README.md)** - Main overview and quick start
2. **[INSTALL.md](INSTALL.md)** - Complete installation guide
3. **[NEXT_STEPS.md](NEXT_STEPS.md)** - Your first steps after installation
4. **[QUICKSTART.md](QUICKSTART.md)** - Quick reference and examples

## 🎨 Feature Documentation

- **[SKILLS_FEATURE.md](SKILLS_FEATURE.md)** - Skills inventory and conditional skills guide
- **[CONFIGURATION.md](CONFIGURATION.md)** - Configuration system and setup guide (NEW!)

## 📚 Documentation Structure

### For New Users
```
1. README.md          → Overview, features, basic usage
2. INSTALL.md         → Install Ollama, Python, resume-builder
3. NEXT_STEPS.md      → Test installation, first workflow
4. QUICKSTART.md      → Common usage patterns
```

### For Reference
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history and changes
- **[LICENSE](../LICENSE)** - MIT License
- **../config/settings.yaml** - Configuration options
- **../memory-bank/** - Technical documentation (for developers)

## 📖 What Each File Contains

### README.md
- Project overview
- Features list
- Quick install steps
- Basic usage examples
- Command reference
- Troubleshooting basics

### INSTALL.md
- Detailed installation instructions
- Ollama setup
- Python environment setup
- Verification steps
- Complete troubleshooting guide
- Alternative models and configurations

### NEXT_STEPS.md
- Post-installation checklist
- First workflow walkthrough
- Real-world usage examples
- Tips and best practices
- Understanding match scores
- Tracking success

### QUICKSTART.md
- TL;DR - 2 minute start
- Common commands
- Real-world examples
- Integration with existing workflow
- Best practices

### CHANGELOG.md
- Version history
- Feature additions
- Bug fixes
- Breaking changes

### SKILLS_FEATURE.md
- Skills inventory system overview
- CLI commands reference (`resume-skills`)
- Conditional skills (context-dependent skills)
- Real-world examples (React Native scenarios)
- Best practices for skills management

### CONFIGURATION.md
- Setup wizard and first-time configuration
- Config commands (`resume-builder config`)
- File locations and priorities
- Common workflows and troubleshooting
- Advanced configuration topics

## 🎯 Usage Paths

### Path 1: Complete Beginner
```
README.md → docs/INSTALL.md → test_installation.sh → docs/NEXT_STEPS.md
```

### Path 2: Quick Start (Already Have Ollama)
```
docs/INSTALL.md (Step 4 only) → docs/QUICKSTART.md
```

### Path 3: Just Want Commands
```
README.md (Commands Reference section)
```

### Path 4: Setting Up Skills Inventory
```
docs/SKILLS_FEATURE.md → config/skills_inventory.yaml → resume-skills CLI
```

### Path 5: Configuring Resume Paths
```
resume-builder setup → docs/CONFIGURATION.md → resume-builder config
```

## 🔧 Developer Documentation

Located in `../memory-bank/`:
- **projectbrief.md** - Project goals and requirements
- **activeContext.md** - Current implementation status
- **techContext.md** - Technical architecture
- **systemPatterns.md** - Design patterns
- **productContext.md** - Product philosophy
- **progress.md** - Development progress

## 💡 Quick Links

**Installation:**
- [Quick Install](INSTALL.md#quick-install)
- [Troubleshooting](INSTALL.md#troubleshooting)

**Usage:**
- [Complete Workflow](../README.md#complete-workflow-recommended)
- [Individual Commands](../README.md#individual-commands)
- [Match Scores](../README.md#understanding-match-scores)

**Help:**
```bash
resume-builder --help
resume-builder workflow --help
```

## 📝 Documentation Maintenance

Files are organized as:
- **User-facing:** README, INSTALL, QUICKSTART, NEXT_STEPS
- **Reference:** CHANGELOG, LICENSE, config
- **Developer:** memory-bank/

Keep documentation:
- Clear and concise
- Examples-driven
- Up-to-date with code
- Beginner-friendly

---

**Start here:** [README.md](../README.md) → [INSTALL.md](INSTALL.md) → [NEXT_STEPS.md](NEXT_STEPS.md)

