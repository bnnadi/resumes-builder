# Product Context

## Why This Project Exists

### The Problem
Job seekers using markdown-based resume workflows face a critical bottleneck: converting customized resumes to ATS (Applicant Tracking System) compliant .docx files. While markdown is excellent for version control and customization, most companies require .docx format and many use ATS software that fails to parse improperly formatted documents.

### Current Pain Points
1. **Manual Conversion**: Copy-pasting from .md to Word
2. **Formatting Hell**: Manually setting fonts, margins, spacing for each application
3. **ATS Uncertainty**: No way to verify if formatting will pass ATS parsing
4. **Time Waste**: 15-20 minutes per application on mechanical tasks
5. **Error Risk**: Easy to miss formatting details that break ATS parsing

### Impact
- Resume never reaches human reviewers if ATS rejects it
- Wasted time on formatting instead of content refinement
- Inconsistent presentation across applications

## How It Should Work

### User Experience Goal
**Single command from markdown to submission-ready package**

```bash
# Current workflow
1. Write customized resume in markdown ✓ (automated)
2. Open .md file
3. Copy to Word
4. Format manually (font, margins, bullets, spacing)
5. Save as .docx
6. Export PDF
7. Verify ATS compliance manually
8. Gather supporting documents
9. Submit

# Target workflow
1. Write customized resume in markdown ✓ (automated)
2. Run: export-resume applications/Company/Company_Resume.md --package
3. Submit .docx from package ✓
```

### Core User Flow

**Input**: Markdown resume file (e.g., `Hillpointe_Bisike_Nnadi_Resume_2025.md`)

**Process**:
1. Parse markdown structure (sections, bullets, formatting)
2. Apply ATS-approved formatting rules
3. Generate .docx with proper styling
4. Validate ATS compliance
5. Create application package with supporting documents
6. Provide submission checklist

**Output**: Complete application package ready to submit

### Key Features Users Need

#### 1. Format Confidence
Users must trust the output is ATS-compliant. Provide:
- ✅ Validation checks with clear pass/fail
- ✅ Specific warnings if issues detected
- ✅ Formatting summary (fonts, margins, file size)

#### 2. Speed
- Export should complete in seconds
- No manual intervention required
- Batch processing for multiple companies

#### 3. Integration
- Works seamlessly with existing markdown resumes
- Fits into current automation workflow
- No need to change existing processes

#### 4. Package Completeness
Beyond just the resume, include:
- Cover letter talking points
- Job analysis
- Technical gaps prep
- Application checklist
- Quick reference guide

## User Workflows

### Primary Workflow: Single Company Application
```bash
cd /Users/bisikennadi/Research/resumes/applications/Hillpointe/
export-resume Hillpointe_Bisike_Nnadi_Resume_2025.md --package --validate
# → Opens 00_START_HERE.md
# → User reviews checklist and submits .docx
```

### Secondary Workflow: Batch Export
```bash
export-resume --batch applications/ --validate
# → Exports all company resumes at once
# → Useful for updating multiple applications
```

### Validation Workflow
```bash
export-resume --validate-only existing_resume.docx
# → Check if an existing .docx is ATS-compliant
# → Useful for testing or auditing
```

## Problems It Solves

### For Job Applications
- ✅ Eliminates manual formatting time
- ✅ Guarantees ATS compliance
- ✅ Reduces application preparation stress
- ✅ Ensures consistent professional presentation

### For Resume Iteration
- ✅ Makes it easy to update and re-export
- ✅ Version control friendly (markdown source)
- ✅ Quick A/B testing of resume variations

### For Peace of Mind
- ✅ Know your resume will be parsed correctly
- ✅ Confidence in professional formatting
- ✅ Focus energy on content, not formatting

## What Success Looks Like

### Quantitative
- Export time: <10 seconds per resume
- Application prep time: <2 minutes (down from 20)
- ATS compliance rate: 100%
- Zero manual formatting steps

### Qualitative
- User never thinks about formatting
- Seamless part of application workflow
- "Just works" reliability
- Reduces application anxiety

