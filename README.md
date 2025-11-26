# ATS Resume Export System

Convert markdown resumes to ATS-optimized .docx files with a single command.

## Overview

This tool automates the conversion of markdown-formatted resumes into ATS (Applicant Tracking System) compliant .docx files. It ensures proper formatting, validates ATS compliance, and creates complete application packages.

## Features

- ✅ **Markdown to DOCX**: Convert markdown resumes to properly formatted .docx files
- ✅ **ATS Compliance**: Automatic validation of ATS-friendly formatting
- ✅ **Multi-Format Export**: Generate .docx, .pdf, .html, and .txt versions
- ✅ **Package Builder**: Create complete application packages with supporting documents
- ✅ **Fast**: Export complete packages in under 10 seconds
- ✅ **CLI Interface**: Simple command-line interface for automation

## Installation

### Quick Install (Recommended)

**Option 1: Automated Installation Script**
```bash
cd /Users/bisikennadi/Projects/resumes-builder
./install.sh
```

**Option 2: Using Make**
```bash
make install
```

**Option 3: Manual Installation**
```bash
# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies and package
pip install -r requirements.txt
pip install -e .

# Verify installation
export-resume --version
```

See `INSTALL.md` for detailed installation instructions and troubleshooting.

### Prerequisites

- Python 3.12 or higher
- pip (included with Python)
- ~100MB disk space

## Quick Start

### Basic Usage

Convert a markdown resume to .docx:

```bash
export-resume path/to/resume.md
```

### With Validation

Export and validate ATS compliance:

```bash
export-resume resume.md --validate
```

### Create Complete Package

Generate .docx, .pdf, and supporting documents:

```bash
export-resume resume.md --package
```

### Multi-Format Export

Export to multiple formats:

```bash
export-resume resume.md --formats docx pdf html
```

## ATS Formatting Rules

The tool ensures your resume follows ATS best practices:

- **Font**: Calibri 11pt (or Arial as fallback)
- **Margins**: 1 inch on all sides
- **Spacing**: Single spacing with proper section separation
- **Bullets**: Simple round bullets (no fancy symbols)
- **No**: Tables, images, text boxes, headers, or footers
- **File Size**: Under 1MB

## Command-Line Options

```bash
export-resume [OPTIONS] INPUT_FILE

Options:
  -o, --output DIR          Output directory (default: same as input)
  -f, --formats FORMATS     Export formats: docx, pdf, html, txt (default: docx)
  --validate                Validate ATS compliance after export
  --package                 Create complete application package
  --template FILE           Custom .docx template
  --preview                 Preview formatting without exporting
  --validate-only           Only validate existing .docx file
  --batch DIR               Batch process all resumes in directory
  -v, --verbose             Verbose output
  --version                 Show version
  -h, --help                Show help message
```

## Examples

### Example 1: Simple Export

```bash
export-resume Hillpointe_Resume.md
```

Output:
- `Hillpointe_Resume.docx`

### Example 2: Complete Application Package

```bash
export-resume Hillpointe_Resume.md --package --validate
```

Output:
- `Hillpointe_Resume.docx` ✅ [READY TO SUBMIT]
- `Hillpointe_Resume.pdf` ✅ [READY TO SUBMIT]
- `00_START_HERE.md` [Quick reference]
- `README.md` [Package overview]
- All existing analysis and checklist files preserved

### Example 3: Batch Processing

```bash
export-resume --batch applications/ --validate
```

Exports all markdown resumes in the directory.

### Example 4: Validate Existing File

```bash
export-resume --validate-only existing_resume.docx
```

## Markdown Resume Format

Your markdown resume should follow this structure:

```markdown
# Your Full Name

City, State | email@example.com | (123) 456-7890  
LinkedIn: linkedin.com/in/profile | GitHub: github.com/username

## Summary

Brief professional summary highlighting key achievements and expertise.

## Core Skills

**Leadership**: Team building, Strategy, Agile methodologies  
**Technical**: Python, React, AWS, Docker, Kubernetes

## Experience

### Job Title, Company Name, Location
*Month Year - Month Year*

- Achievement with quantifiable results
- Led initiative that improved X by Y%
- Managed team of Z engineers

### Previous Job Title, Company Name, Location
*Month Year - Month Year*

- More achievements
- More quantifiable results

## Education

**Degree Name** - University Name (Year)  
Relevant coursework, honors, or activities
```

## Integration with Existing Workflow

This tool is designed to integrate seamlessly with existing resume customization workflows:

```bash
# 1. Customize resume (existing workflow)
resume-customize --company "Company Name"

# 2. Export to .docx (new tool)
export-resume applications/Company/Company_Resume.md --package

# 3. Submit application
# → Use Company_Resume.docx from the package
```

## Development

### Setup Development Environment

**Automated Setup**:
```bash
make install
```

**Manual Setup**:
```bash
# Clone or navigate to repository
cd /Users/bisikennadi/Projects/resumes-builder

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .
```

### Development Commands

```bash
make clean         # Clean build artifacts
make test          # Run tests
make lint          # Run linters
make format        # Format code
make demo          # Run demo with sample resume
```

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=resume_export --cov-report=html
```

### Format Code

```bash
black resume_export/
isort resume_export/
```

### Type Check

```bash
mypy resume_export/
```

## Project Structure

```
resumes-builder/
├── resume_export/              # Main package
│   ├── parser.py              # Markdown parsing
│   ├── docx_builder.py        # DOCX generation
│   ├── exporter.py            # Main exporter
│   ├── exporters/             # Format-specific exporters
│   ├── validators/            # ATS validation
│   └── templates/             # Style templates
├── export_resume.py           # CLI entry point
├── tests/                     # Test suite
├── memory-bank/               # Project documentation
├── requirements.txt           # Dependencies
├── setup.py                   # Package setup
└── README.md                  # This file
```

## Troubleshooting

### Font Not Found

If Calibri is not installed:
- Tool automatically falls back to Arial
- Warning will be displayed
- Both fonts are ATS-friendly

### PDF Generation Fails

PDF generation requires LibreOffice or python-docx2pdf:
- Install LibreOffice for best results
- Or: `pip install python-docx2pdf`
- Tool will skip PDF if neither available

### Validation Warnings

If ATS validation shows warnings:
- Review the specific issues reported
- Most warnings are suggestions, not critical
- Critical issues will prevent export

## Support

For issues or questions:
1. Check the Memory Bank documentation in `memory-bank/`
2. Review existing test cases in `tests/`
3. Check project documentation

## License

MIT License - See LICENSE file for details

## Version

Current Version: 0.1.0 (Alpha)

---

**Built for**: Job seekers who want ATS-compliant resumes without manual formatting  
**Optimized for**: Speed, reliability, and seamless workflow integration

