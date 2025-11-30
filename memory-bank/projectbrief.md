# Project Brief: AI-Powered Resume Builder

## Project Name
**resume-builder** - AI-Powered Resume Builder with ATS-Optimized Export

## Problem Statement
Job applications are time-consuming and often result in poor-fit applications:
- Manual resume customization takes 20-30 minutes per job
- Hard to objectively assess job fit before investing time
- Difficult to optimize keywords and content for specific roles
- Tedious conversion to ATS-compliant formats

## Solution
An AI-powered workflow that:
1. Analyzes job fit with objective scoring (0-100)
2. Gates workflow at 70% threshold (prevents wasting time on poor fits)
3. Customizes resumes using AI for specific jobs
4. Exports to ATS-optimized .docx format
- All running locally with Ollama (offline, private, free)

## Core Goals
1. **AI Analysis**: Objective job fit scoring to guide application decisions
2. **Smart Gating**: 70% threshold prevents time waste on poor-fit jobs
3. **AI Customization**: Tailor resumes to specific jobs with keyword optimization
4. **ATS Compliance**: Ensure 100% ATS-friendly formatting (fonts, spacing, structure)
5. **Complete Workflow**: Single command from job posting to submission-ready .docx
6. **Offline & Private**: All AI processing runs locally (no cloud, no API costs)

## Key Requirements
- Python 3.12+ (matches existing automation environment)
- Integrate with existing workflow at `/Users/bisikennadi/Research/`
- Process existing markdown resumes from `/Users/bisikennadi/Research/resumes/applications/`
- CLI-first interface (matches current automation workflow)
- ATS formatting rules: Calibri/Arial 11pt, 1" margins, no tables/images
- File size under 1MB limit

## Success Criteria
- Analyze job fit in 30-60 seconds with objective scoring
- Auto-stop on poor matches (< 70%) to save time
- Generate customized resume in 2-4 minutes
- Export to ATS-compliant .docx in <3 seconds
- Reduce total application time from 28 minutes to 5 minutes (82% reduction)
- 100% offline operation (no internet required after setup)
- Zero manual formatting required

## Target Users
- Primary: Bisike (resume customization automation)
- Future: Could be generalized for other job seekers

## Out of Scope (v1.0)
- Web interface (CLI only for now)
- Resume content generation (only formatting/export)
- Cover letter generation (future enhancement)
- Direct job application submission

## Project Timeline
- Phase 1: Core Converter (Week 1)
- Phase 2: Validation (Week 2)
- Phase 3: Package Builder (Week 3)
- Phase 4: Integration & Testing (Week 4)

## Related Systems
- `/Users/bisikennadi/Research/automation/` - Job search automation
- `/Users/bisikennadi/Research/resumes/` - Resume storage and customization

