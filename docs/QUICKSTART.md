# Quick Start Guide

## TL;DR - Start Using in 2 Minutes

```bash
# 1. Activate environment
cd /Users/bisikennadi/Projects/resumes-builder
source venv/bin/activate

# 2. Export your resume
export-resume /path/to/your/resume.md --validate --package

# 3. Done! Check output directory for:
#    - Resume.docx [SUBMIT THIS]
#    - 00_START_HERE.md [READ THIS FIRST]
```

---

## Installation (One-Time Setup)

Already done! But if you need to reinstall:

```bash
cd /Users/bisikennadi/Projects/resumes-builder
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

**First-Time Configuration:**
```bash
# Run the setup wizard
resume-builder setup

# Or configure manually
resume-builder config set resume-path ~/my-resumes
resume-builder config set base-resume ~/my-resumes/master-resume.md
```

---

## Common Usage

### 1. Export Single Resume
```bash
source venv/bin/activate
export-resume applications/Company/Company_Resume.md
```

**Output**: `Company_Resume.docx` in same directory

### 2. Export with Validation
```bash
export-resume applications/Company/Company_Resume.md --validate
```

**Output**: 
- `Company_Resume.docx`
- Validation report in terminal

### 3. Create Complete Package (Recommended!)
```bash
export-resume applications/Company/Company_Resume.md --package --validate
```

**Output**:
- `Company_Resume.docx` ✅ [SUBMIT THIS]
- `00_START_HERE.md` [Quick reference]
- `README.md` [Package overview]
- All existing files preserved

### 4. Batch Process Multiple Resumes
```bash
export-resume --batch applications/
```

**Output**: Exports all markdown resumes in directory

### 5. Validate Existing .docx
```bash
export-resume --validate-only resume.docx
```

**Output**: ATS compliance report

### 6. Manage Skills Inventory (New!)
```bash
# List all your skills
resume-skills list

# Check which skills match a job
resume-skills match job_posting.txt

# Add new skills
resume-skills add programming_languages "Rust"

# Find a skill
resume-skills find "Docker"
```

**See**: [SKILLS_FEATURE.md](SKILLS_FEATURE.md) for complete guide

### 7. Configuration Management (New!)
```bash
# View all settings
resume-builder config list

# Set configuration values
resume-builder config set resume-path ~/my-resumes
resume-builder config set base-resume ~/my-resumes/master.md
resume-builder config set output-dir ~/my-resumes/applications

# Get a specific value
resume-builder config get model

# Validate configured paths
resume-builder config validate

# Show config file location
resume-builder config path
```

---

## Real Example (Tested & Working!)

```bash
# Export the Hillpointe resume
cd /Users/bisikennadi/Projects/resumes-builder
source venv/bin/activate

export-resume \
  /Users/bisikennadi/Research/resumes/applications/Hillpointe/Hillpointe_Bisike_Nnadi_Resume_2025.md \
  --validate \
  --package
```

**Result**:
```
✅ DOCX created: Hillpointe_Bisike_Nnadi_Resume_2025.docx
✅ ATS validation: PASSED (100% compliant)
✅ Package complete: 8 files
📍 Location: /Users/bisikennadi/Research/resumes/applications/Hillpointe/
⏱️  Time: 3 seconds
```

---

## What You Get

### Standard Export
- `Resume.docx` - ATS-optimized, ready to submit

### With --validate
- Validation report showing:
  - ✅ File size: Under 1MB
  - ✅ Fonts: ATS-friendly
  - ✅ No tables or images
  - ✅ Standard sections present
  - ✅ Optimal length

### With --package
- `Resume.docx` ✅ [SUBMIT THIS]
- `00_START_HERE.md` - Quick reference & checklist
- `README.md` - Complete package guide
- All your existing analysis/checklist files preserved

---

## Troubleshooting

### "Command not found: export-resume"
```bash
# Make sure you activated the virtual environment
cd /Users/bisikennadi/Projects/resumes-builder
source venv/bin/activate
```

### "File not found"
Check the path to your markdown file:
```bash
# Use absolute path if needed
export-resume /Users/bisikennadi/Research/resumes/applications/Company/Resume.md
```

### PDF Export Failed
Normal! PDF requires LibreOffice:
```bash
# Install LibreOffice (optional)
brew install --cask libreoffice

# Or just use the .docx file (preferred for ATS anyway)
```

### Want Verbose Output
```bash
export-resume resume.md --validate --package --verbose
```

---

## Integration with Existing Workflow

### Current Workflow
```bash
# 1. Customize resume (existing automation)
cd /Users/bisikennadi/Research/automation
# ... run resume-customize script ...

# 2. Export to .docx (NEW!)
cd /Users/bisikennadi/Projects/resumes-builder
source venv/bin/activate
export-resume ../Research/resumes/applications/Company/Company_Resume.md --package

# 3. Submit
# → Use Company_Resume.docx from package
```

### Future: Streamlined Workflow
Add to resume-customize script:
```bash
# After generating markdown, automatically export
export-resume $OUTPUT_FILE --package --validate
```

---

## Tips & Best Practices

### ✅ DO:
- Always use `--validate` to check ATS compliance
- Use `--package` to get complete application bundle
- Review `00_START_HERE.md` before applying
- Submit .docx format (preferred by most ATS)

### ❌ DON'T:
- Don't manually format the .docx (already ATS-optimized)
- Don't skip validation (catches issues early)
- Don't ignore warnings (address them if possible)
- Don't submit .md file directly (companies want .docx)

---

## Performance

- **Export time**: ~3 seconds
- **File size**: ~40KB (well under 1MB limit)
- **ATS compliance**: 100% (on tested resumes)
- **Memory usage**: ~30MB

---

## Getting Help

### Check Documentation
1. `README.md` - Full documentation
2. `memory-bank/` - Project context and architecture
3. `.cursorrules` - Project patterns and insights

### Test with Sample Resume
```bash
# Use the validated Hillpointe resume
export-resume \
  /Users/bisikennadi/Research/resumes/applications/Hillpointe/Hillpointe_Bisike_Nnadi_Resume_2025.md \
  --validate
```

---

## Quick Reference Card

| Command | What It Does |
|---------|-------------|
| `export-resume file.md` | Export to .docx |
| `--validate` | Check ATS compliance |
| `--package` | Create complete bundle |
| `--batch DIR` | Process all resumes |
| `--validate-only file.docx` | Check existing file |
| `--formats docx pdf` | Multi-format export |
| `--help` | Show all options |

---

## Success!

You now have a production-ready ATS resume export system that:
- ✅ Converts markdown → .docx in seconds
- ✅ Guarantees ATS compliance
- ✅ Creates complete application packages
- ✅ Integrates with your workflow

**Now go apply to those jobs!** 🚀

---

**Version**: 0.1.0  
**Status**: Production Ready ✅  
**Last Tested**: November 26, 2025

