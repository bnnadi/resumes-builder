# Technical Context

## Technology Stack

### Core Dependencies
```python
# requirements.txt
python-docx>=1.1.0      # .docx file generation and manipulation
markdown>=3.5.0         # Markdown parsing
pyyaml>=6.0.0           # Configuration and style files
jinja2>=3.1.0           # Template rendering
```

### Optional Dependencies
```python
# For additional features
pypdf>=3.17.0           # PDF generation from .docx
beautifulsoup4>=4.12.0  # HTML export
pillow>=10.0.0          # Image handling (validation only)
```

### Development Dependencies
```python
pytest>=7.4.0           # Testing framework
black>=23.0.0           # Code formatting
mypy>=1.7.0             # Type checking
pylint>=3.0.0           # Linting
```

## Development Environment

### Python Version
- **Required**: Python 3.12+
- **Reason**: Matches existing automation environment at `/Users/bisikennadi/Research/automation/`
- **Feature usage**: Type hints, pattern matching, improved error messages

### Operating System
- **Primary**: macOS (darwin 25.0.0)
- **Compatibility**: Should work on Linux and Windows (python-docx is cross-platform)
- **Shell**: zsh

### File Paths
- **Project Root**: `/Users/bisikennadi/Projects/resumes-builder/`
- **Integration Point**: `/Users/bisikennadi/Research/resumes/`
- **Automation Scripts**: `/Users/bisikennadi/Research/automation/`

## Project Structure

```
resumes-builder/
├── resume_export/                 # Main package
│   ├── __init__.py
│   ├── parser.py                 # Markdown parsing
│   ├── docx_builder.py           # .docx generation
│   ├── formatter.py              # Formatting utilities
│   ├── package_builder.py        # Application package creation
│   ├── exporters/                # Format-specific exporters
│   │   ├── __init__.py
│   │   ├── base.py              # Base exporter class
│   │   ├── docx_exporter.py     # .docx export
│   │   ├── pdf_exporter.py      # .pdf export
│   │   ├── html_exporter.py     # .html export
│   │   └── txt_exporter.py      # .txt export
│   ├── validators/               # ATS compliance checking
│   │   ├── __init__.py
│   │   ├── ats_checker.py       # Main ATS validator
│   │   ├── format_validator.py  # Format checking
│   │   └── rules.py             # Validation rules
│   └── templates/                # Style templates
│       ├── styles.yaml          # ATS formatting rules
│       ├── resume_template.docx # Base .docx template
│       └── package_template/    # Package file templates
├── export_resume.py              # CLI entry point
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_docx_builder.py
│   ├── test_validators.py
│   └── fixtures/                # Test data
│       ├── sample_resume.md
│       └── expected_output.docx
├── memory-bank/                  # Project documentation
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── systemPatterns.md
│   ├── techContext.md
│   ├── activeContext.md
│   └── progress.md
├── requirements.txt              # Dependencies
├── requirements-dev.txt          # Dev dependencies
├── setup.py                      # Package setup
├── .cursorrules                  # Project-specific patterns
├── .gitignore
└── README.md
```

## Key Technical Constraints

### 1. ATS Formatting Requirements
These are non-negotiable for ATS systems to parse correctly:

```yaml
# templates/styles.yaml
fonts:
  allowed: ["Calibri", "Arial", "Times New Roman", "Georgia"]
  body_size: 10-12pt
  name_size: 14-18pt
  
margins:
  all_sides: 1.0 inch (minimum 0.5 inch)
  
forbidden_elements:
  - tables
  - text_boxes
  - headers_footers
  - images
  - columns
  - shapes
  - fancy_bullets
  - special_characters (⚡ ★ ●)
  
file_requirements:
  max_size: 1MB
  format: .docx (preferred) or .pdf
  pages: 1-2 recommended
```

### 2. Markdown Input Format
The parser expects markdown files structured as:

```markdown
# Full Name

Location | Email | Phone  
LinkedIn: url | GitHub: url

## Summary
Brief professional summary...

## Core Skills
**Category Name**: Skill 1, Skill 2, Skill 3

## Experience

### Job Title, Company Name, Location
*Month Year - Month Year*

- Achievement bullet point
- Quantified result bullet point

### Next Job...

## Education

**Degree Name** - University Name (Year)
```

**Key Decision**: This format matches existing resume files. Parser must be flexible enough to handle variations.

### 3. python-docx Limitations

**Known Limitations**:
- Cannot edit .docx headers/footers easily (we avoid them)
- Limited style manipulation compared to Word VBA
- No built-in PDF export (need separate tool)
- Font installation on system required (Calibri on macOS)

**Workarounds**:
- Use simple formatting only
- Include template .docx with pre-configured styles
- Use external tool (LibreOffice) for PDF conversion
- Fallback to Arial if Calibri not available

### 4. File System Dependencies

**Assumptions**:
- Resume files exist at `/Users/bisikennadi/Research/resumes/applications/Company/`
- Each company folder contains customized markdown resume
- Supporting files (analysis, cover letter points) already exist
- Script has read/write permissions to application folders

**Error Handling**:
- Check file existence before processing
- Validate markdown structure
- Handle permission errors gracefully
- Preserve existing files (never overwrite without confirmation)

## Installation & Setup

### Initial Setup
```bash
cd /Users/bisikennadi/Projects/resumes-builder

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install package in development mode
pip install -e .

# Verify installation
export-resume --version
```

### System Requirements
- Python 3.12+
- ~50MB disk space for dependencies
- LibreOffice (optional, for PDF conversion)
- Calibri or Arial font installed

### Configuration
```yaml
# ~/.resume-export/config.yaml (user config)
default_format: docx
auto_validate: true
resumes_directory: /Users/bisikennadi/Research/resumes
template_style: ats-standard
```

## External Dependencies

### python-docx
**Purpose**: Generate and manipulate .docx files  
**Why**: Best Python library for .docx manipulation  
**Docs**: https://python-docx.readthedocs.io/  
**Version**: 1.1.0+

**Key Classes**:
- `Document`: Main document object
- `Paragraph`: Text paragraphs
- `Run`: Formatted text runs
- `Section`: Document sections (for margins)

### markdown
**Purpose**: Parse markdown to AST  
**Why**: Standard Python markdown parser  
**Docs**: https://python-markdown.github.io/  
**Version**: 3.5.0+

**Usage**:
```python
import markdown
md = markdown.Markdown(extensions=['meta', 'tables'])
html = md.convert(markdown_text)
metadata = md.Meta
```

### PyYAML
**Purpose**: Load style configurations  
**Why**: Clean, readable config format  
**Version**: 6.0+

### Jinja2
**Purpose**: Template rendering for package files  
**Why**: Powerful templating for README, checklists  
**Version**: 3.1.0+

## Integration with Existing Systems

### Resume Customization Workflow
```python
# Existing: /Users/bisikennadi/Research/automation/
# Has: resume-customize command (assumed to exist)

# Integration approach:
# 1. User runs existing customization: resume-customize
# 2. Generates markdown: Company_Name_Resume.md
# 3. User runs: export-resume Company_Name_Resume.md --package
# 4. Gets: .docx, .pdf, complete package
```

### File System Integration
- **Reads**: Existing markdown files and supporting docs
- **Writes**: New .docx and .pdf in same directory
- **Preserves**: All existing files unchanged
- **Creates**: README.md and 00_START_HERE.md if missing

### Command-Line Integration
```bash
# Make script available system-wide
# Option 1: Add to PATH
export PATH="/Users/bisikennadi/Projects/resumes-builder:$PATH"

# Option 2: Install as package
pip install -e /Users/bisikennadi/Projects/resumes-builder

# Option 3: Alias in ~/.zshrc
alias export-resume="python /Users/bisikennadi/Projects/resumes-builder/export_resume.py"
```

## Testing Strategy

### Unit Tests
```python
# tests/test_parser.py - Test markdown parsing
# tests/test_docx_builder.py - Test .docx generation
# tests/test_validators.py - Test ATS validation
# tests/test_exporters.py - Test format exporters
```

### Integration Tests
```python
# tests/test_end_to_end.py
# - Load real markdown resume
# - Export to .docx
# - Validate ATS compliance
# - Verify output matches expected
```

### Test Fixtures
- Sample markdown resumes (various structures)
- Expected .docx outputs
- ATS-compliant and non-compliant examples

### Test Execution
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=resume_export --cov-report=html

# Run specific test
pytest tests/test_parser.py::test_parse_experience
```

## Performance Targets

### Speed
- Parse markdown: <1 second
- Generate .docx: <3 seconds
- Validate ATS: <2 seconds
- Total export: <10 seconds

### Memory
- Peak memory: <100MB
- Typical: ~50MB

### File Size
- Output .docx: 50-100KB (well under 1MB limit)
- Output .pdf: 100-200KB

## Security Considerations

### Input Validation
- Sanitize markdown input (no code execution)
- Validate file paths (no directory traversal)
- Check file sizes (prevent DoS)

### File Permissions
- Only read/write in allowed directories
- Never execute user-provided code
- Validate output paths

### Dependencies
- Use pinned versions in requirements.txt
- Regular security updates
- No dependencies on unpinned packages

## Deployment

### Local Installation
Primary deployment method - installed locally on user's machine

```bash
cd /Users/bisikennadi/Projects/resumes-builder
pip install -e .
```

### Distribution (Future)
If generalizing for others:
```bash
# PyPI package
pip install ats-resume-export

# Or GitHub releases
pip install git+https://github.com/user/resumes-builder.git
```

## Monitoring & Logging

### Logging Strategy
```python
import logging

# Log levels
# DEBUG: Detailed parsing/building steps
# INFO: Export progress, file creation
# WARNING: Non-critical ATS issues
# ERROR: Export failures, invalid input
# CRITICAL: System errors

# Log file location
~/.resume-export/logs/export_YYYYMMDD.log
```

### Metrics to Track
- Export success/failure rate
- Average export time
- ATS validation pass rate
- Common error types

## Future Technical Considerations

### Scalability
- Current: Single-user, local execution
- Future: Could support batch processing, web service

### Extensibility
- Plugin system for custom validators
- Custom style templates
- Additional export formats

### Maintenance
- Keep dependencies updated
- Monitor python-docx compatibility
- Test with new ATS systems as they evolve

