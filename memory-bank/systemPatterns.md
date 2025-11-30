# System Patterns

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI Interface (export_resume.py)         │
│                   • Argument parsing                         │
│                   • Workflow orchestration                   │
└────────────────┬────────────────────────────────────────────┘
                 │
       ┌─────────┼──────────┬──────────────┬─────────────┐
       │         │          │              │             │
┌──────▼─────┐ ┌▼─────────┐ ┌▼───────────┐ ┌▼──────────┐ ┌▼───────────┐
│  Markdown  │ │  DOCX    │ │ Validator  │ │  Package  │ │  Multi-    │
│  Parser    │ │ Builder  │ │           │ │  Builder  │ │  Format    │
│            │ │          │ │ • ATS     │ │           │ │  Exporter  │
│ • Extract  │ │ • Apply  │ │   Rules   │ │ • Bundle  │ │            │
│   sections │ │   styles │ │ • Checks  │ │   files   │ │ • PDF      │
│ • Parse    │ │ • Format │ │ • Report  │ │ • Summary │ │ • HTML     │
│   content  │ │   resume │ │           │ │           │ │ • TXT      │
└────────────┘ └──────────┘ └───────────┘ └───────────┘ └────────────┘
```

## Core Components

### 1. Markdown Parser (`resume_export/parser.py`)
**Responsibility**: Transform markdown structure into structured data

**Pattern**: Parser pattern with section extractors

```python
{
  "name": "Bisike Nnadi",
  "contact": {
    "location": "Charlotte, NC",
    "email": "email@example.com",
    "phone": "(123) 456-7890",
    "linkedin": "linkedin.com/in/profile",
    "github": "github.com/username"
  },
  "summary": "Engineering leader with...",
  "skills": {
    "Leadership": ["Team building", "..."],
    "Technical": ["Python", "..."]
  },
  "experience": [
    {
      "title": "Engineering Manager",
      "company": "Company Name",
      "dates": "Jan 2020 - Present",
      "location": "City, ST",
      "achievements": ["Led team of...", "..."]
    }
  ],
  "education": [...]
}
```

**Key Decision**: Use structured data format as intermediate representation. This allows:
- Easy validation of required sections
- Simple transformation to any output format
- Clear separation of parsing and formatting

### 2. DOCX Builder (`resume_export/docx_builder.py`)
**Responsibility**: Generate ATS-compliant .docx from structured data

**Pattern**: Builder pattern with style templates

**ATS Formatting Rules**:
```python
STYLES = {
    "fonts": {
        "body": {"name": "Calibri", "size": 11},
        "name": {"name": "Calibri", "size": 16, "bold": True},
        "section_header": {"name": "Calibri", "size": 12, "bold": True},
        "job_title": {"name": "Calibri", "size": 11, "bold": True}
    },
    "margins": {"top": 1.0, "bottom": 1.0, "left": 1.0, "right": 1.0},
    "spacing": {
        "line": 1.0,           # Single spacing
        "paragraph": 6,         # 6pt between paragraphs
        "section": 12          # 12pt between sections
    },
    "bullets": {
        "style": "simple_round",  # No fancy symbols
        "indent": 0.25            # 0.25" indent
    }
}
```

**Key Decision**: No tables, headers, footers, or complex formatting. ATS systems often fail to parse these correctly.

### 3. ATS Validator (`resume_export/validators/ats_checker.py`)
**Responsibility**: Verify ATS compliance and report issues

**Pattern**: Rule-based validation with severity levels

**Validation Rules**:
```python
CRITICAL = [
    "file_size_under_1mb",
    "no_images",
    "no_tables",
    "readable_fonts"
]

WARNING = [
    "consistent_date_format",
    "standard_section_headers",
    "no_special_characters_in_bullets"
]

INFO = [
    "optimal_length_1_to_2_pages",
    "action_verbs_in_bullets"
]
```

**Key Decision**: Three severity levels allow users to distinguish between "will break ATS" vs "could be better".

### 4. Package Builder (`resume_export/package_builder.py`)
**Responsibility**: Bundle complete application package

**Pattern**: Composite pattern - assembles multiple artifacts

**Package Contents**:
```
Company_Name/
├── Company_Name_Resume.docx          [PRIMARY SUBMISSION FILE]
├── Company_Name_Resume.pdf           [BACKUP FORMAT]
├── 00_START_HERE.md                  [Quick reference - what to submit]
├── Company_Name_Analysis.md          [Job analysis from customization]
├── Company_Name_Cover_Letter_Points.md [Cover letter talking points]
├── Company_Name_Application_Checklist.md [Submission checklist]
├── Company_Name_Technical_Gaps.md    [Interview prep]
└── README.md                         [Package overview]
```

**Key Decision**: Include both submission files and preparation materials in one package. User never has to hunt for related files.

## Key Technical Decisions

### 1. Python + python-docx
**Why**: 
- Matches existing automation environment (Python 3.12)
- `python-docx` provides programmatic control over formatting
- No dependency on Microsoft Word
- Cross-platform compatibility

**Alternative Considered**: Pandoc
- ❌ Less control over specific formatting details
- ❌ External dependency installation

### 2. Markdown as Source Format
**Why**:
- User already has markdown workflow
- Version control friendly (git)
- Human-readable and editable
- Easy to customize per application

**Key Insight**: Markdown is for humans, .docx is for ATS systems. Keep them separate.

### 3. CLI-First Interface
**Why**:
- Matches existing automation workflow
- Easy to integrate with scripts
- Fast and efficient for power users
- Can be automated/scheduled

**Future**: Web interface could be added without changing core architecture.

### 4. Validation as Separate Step
**Why**:
- Can validate existing .docx files (not just generated ones)
- Useful for debugging
- Clear pass/fail feedback
- Optional (--validate flag) for speed

### 5. Intermediate Data Structure
**Why**:
- Decouples parsing from formatting
- Enables multiple output formats from same parse
- Easy to test each component independently
- Clear data contracts between components

## Design Patterns in Use

### Builder Pattern (DOCX Builder)
Constructs complex .docx document step by step:
```python
builder = DocxBuilder()
builder.set_margins(1.0)
builder.add_header(name, contact)
builder.add_section("Summary", summary)
builder.add_experience(experience_list)
document = builder.build()
```

### Strategy Pattern (Format Exporters)
Different export strategies for different formats:
```python
exporters = {
    "docx": DocxExporter(),
    "pdf": PdfExporter(),
    "html": HtmlExporter(),
    "txt": TxtExporter()
}
exporter = exporters[format_type]
exporter.export(structured_data, output_path)
```

### Chain of Responsibility (Validators)
Multiple validators check different aspects:
```python
validators = [
    FileSizeValidator(),
    FontValidator(),
    StructureValidator(),
    FormattingValidator()
]
for validator in validators:
    result = validator.validate(document)
    if not result.passed:
        issues.append(result)
```

### Template Method (Base Exporter)
Common export workflow with format-specific steps:
```python
class BaseExporter:
    def export(self, data, output_path):
        self.validate_input(data)
        formatted = self.format_data(data)  # Override in subclasses
        self.write_output(formatted, output_path)  # Override in subclasses
        return self.get_metadata()
```

## Integration Points

### Existing Resume Workflow
```
resume-customize command
         ↓
    Markdown Resume Generated
         ↓
    [NEW] export-resume --package
         ↓
    Complete Application Package
         ↓
    Submit to Company
```

### File System Integration
- **Reads from**: `/Users/bisikennadi/Research/resumes/applications/`
- **Writes to**: Same directory as source .md file
- **Preserves**: All existing application preparation files
- **Adds**: .docx and .pdf versions

### Future Integration Opportunities
- CI/CD: Auto-export on git commit
- Email: Auto-attach to application emails
- Portfolio: Sync to personal website
- LinkedIn: Extract sections for profile updates

## Error Handling Strategy

### Graceful Degradation
```python
try:
    export_docx()
    export_pdf()  # If fails, still have .docx
except DocxError:
    # Critical - cannot proceed
    raise
except PdfError:
    # Warning - can still submit .docx
    warn_user()
```

### User-Friendly Errors
- ❌ Bad: "NoneType has no attribute 'text'"
- ✅ Good: "Missing required section: Experience. Add ## Experience section to your markdown."

### Validation Feedback
- Clear indication of what's wrong
- Actionable suggestions for fixing
- Severity levels (critical vs warning)

## Performance Considerations

### Optimization Strategy
1. **Parse once**: Single pass through markdown
2. **Lazy loading**: Only load templates when needed
3. **Parallel exports**: .docx and .pdf can be generated concurrently
4. **Caching**: Cache parsed structure if exporting multiple formats

### Expected Performance
- Parse markdown: <1 second
- Generate .docx: <3 seconds
- Validate ATS: <2 seconds
- Export PDF: <3 seconds
- **Total**: <10 seconds per resume

### Scalability
- Single resume: Optimized for speed
- Batch processing: Parallel processing of multiple resumes
- Not designed for: Real-time web serving (that's different use case)

