"""
Package Builder

Creates complete application packages with resume and supporting documents.
"""

from pathlib import Path
from typing import List, Dict, Any
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class PackageBuilder:
    """Build complete application packages."""
    
    def create_package(self, application_dir: Path) -> List[str]:
        """
        Create complete application package.
        
        Args:
            application_dir: Directory containing resume and application files
        
        Returns:
            List of files in the package
        """
        application_dir = Path(application_dir)
        package_files = []
        
        # Find all files in directory
        for file in application_dir.iterdir():
            if file.is_file():
                package_files.append(file.name)
        
        # Create START_HERE if it doesn't exist
        start_here_path = application_dir / "00_START_HERE.md"
        if not start_here_path.exists():
            self._create_start_here(application_dir)
            package_files.append("00_START_HERE.md")
        
        # Create README if it doesn't exist
        readme_path = application_dir / "README.md"
        if not readme_path.exists():
            self._create_readme(application_dir)
            package_files.append("README.md")
        
        logger.info(f"📦 Package complete with {len(package_files)} files")
        
        return sorted(package_files)
    
    def _create_start_here(self, application_dir: Path):
        """Create 00_START_HERE.md quick reference file."""
        # Extract company name from directory
        company_name = application_dir.name
        
        # Find resume files
        docx_files = list(application_dir.glob("*.docx"))
        pdf_files = list(application_dir.glob("*.pdf"))
        
        content = f"""# 📋 START HERE - Quick Reference

**Company**: {company_name}  
**Generated**: {datetime.now().strftime("%B %d, %Y")}

---

## 📄 Submission Files

### Primary Submission
"""
        
        if docx_files:
            for docx in docx_files:
                content += f"- ✅ **{docx.name}** [SUBMIT THIS - .docx format]\n"
        
        if pdf_files:
            content += "\n### Backup Format\n"
            for pdf in pdf_files:
                content += f"- ✅ **{pdf.name}** [SUBMIT THIS - .pdf format]\n"
        
        content += """
---

## 📚 Preparation Materials

### Before Applying
1. ☐ Review job analysis file
2. ☐ Read through technical gaps
3. ☐ Review cover letter talking points
4. ☐ Complete application checklist

### Files to Review
"""
        
        # Find supporting files
        for file in sorted(application_dir.glob("*.md")):
            if file.name not in ["00_START_HERE.md", "README.md"]:
                if "Analysis" in file.name:
                    content += f"- 📊 **{file.name}** - Job requirements analysis\n"
                elif "Cover_Letter" in file.name:
                    content += f"- ✍️  **{file.name}** - Cover letter key points\n"
                elif "Checklist" in file.name:
                    content += f"- ☑️  **{file.name}** - Application checklist\n"
                elif "Gaps" in file.name:
                    content += f"- ⚠️  **{file.name}** - Technical gaps & preparation\n"
                else:
                    content += f"- 📄 **{file.name}**\n"
        
        content += """
---

## ✅ Submission Checklist

- [ ] Resume file reviewed and error-free
- [ ] Cover letter customized (if required)
- [ ] Contact information current
- [ ] LinkedIn profile updated
- [ ] Application submitted through correct channel
- [ ] Follow-up date noted on calendar

---

## 📝 Notes

### ATS Optimization
Your resume has been:
- ✅ Formatted with ATS-friendly fonts (Calibri)
- ✅ Optimized for keyword matching
- ✅ Validated for compliance
- ✅ Sized appropriately (under 1MB)

### File Format
- Primary format: .docx (most compatible with ATS)
- Backup format: .pdf (if .docx not accepted)

---

**Ready to apply!** 🚀

*If you have questions about the resume format or content, review the README.md file.*
"""
        
        with open(application_dir / "00_START_HERE.md", 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info("✅ Created 00_START_HERE.md")
    
    def _create_readme(self, application_dir: Path):
        """Create README.md package overview."""
        company_name = application_dir.name
        
        content = f"""# {company_name} Application Package

This directory contains your complete application package for {company_name}.

## 📦 Package Contents

### Submission Files
These are the files you'll submit with your application:

- **Resume (.docx)** - Primary submission format, ATS-optimized
- **Resume (.pdf)** - Backup format if .docx not accepted

### Preparation Materials
These files help you prepare for the application and interview:

- **Job Analysis** - Breakdown of job requirements and match score
- **Cover Letter Points** - Key points to include in cover letter
- **Application Checklist** - Steps to complete before submitting
- **Technical Gaps** - Areas to prepare for interviews

## 🎯 How to Use This Package

### 1. Review the Analysis
Start with the job analysis file to understand:
- Key requirements and priorities
- Your match score
- Important keywords to emphasize

### 2. Prepare Your Resume
Your resume is already:
- ✅ ATS-optimized for parsing
- ✅ Formatted with appropriate fonts and spacing
- ✅ Customized for this role
- ✅ Validated for compliance

### 3. Complete the Checklist
Work through the application checklist to ensure you've:
- Reviewed all materials
- Updated your LinkedIn
- Prepared your cover letter
- Double-checked contact information

### 4. Submit
Use the .docx file as your primary submission format. If the application system doesn't accept .docx, use the .pdf version.

## 📋 Submission Guidelines

### File Format
- **Preferred**: .docx (best ATS compatibility)
- **Alternative**: .pdf (if .docx not accepted)
- **Avoid**: Uploading through web forms that might reformat

### Contact Information
Verify your contact information is current:
- Email address is active
- Phone number is correct
- LinkedIn profile is up to date

## 🔍 ATS Optimization

This resume has been optimized for Applicant Tracking Systems:

### Format
- ✅ ATS-friendly font (Calibri 11pt)
- ✅ Standard 1" margins
- ✅ No tables, images, or complex formatting
- ✅ Simple bullet points

### Content
- ✅ Keywords aligned with job description
- ✅ Standard section headers
- ✅ Clear job titles and dates
- ✅ Quantified achievements

### Technical
- ✅ File size under 1MB
- ✅ Clean .docx format
- ✅ No hidden metadata issues

## 💡 Interview Preparation

After submitting:
1. Review the technical gaps file
2. Prepare examples for each requirement
3. Research the company and team
4. Prepare questions to ask
5. Practice explaining your experience

## 📞 Follow-Up

- Wait 1-2 weeks after submission
- Follow up via email if no response
- Connect with recruiter on LinkedIn
- Note follow-up date on calendar

---

**Application Package Generated**: {datetime.now().strftime("%B %d, %Y")}

Good luck with your application! 🚀
"""
        
        with open(application_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info("✅ Created README.md")
    
    def generate_summary(self, application_dir: Path) -> Dict[str, Any]:
        """
        Generate package summary.
        
        Args:
            application_dir: Application directory
        
        Returns:
            Summary dictionary
        """
        application_dir = Path(application_dir)
        
        summary = {
            "company": application_dir.name,
            "files": [],
            "resume_files": [],
            "support_files": [],
            "file_count": 0
        }
        
        for file in application_dir.iterdir():
            if file.is_file():
                summary["files"].append(file.name)
                summary["file_count"] += 1
                
                if file.suffix in ['.docx', '.pdf']:
                    summary["resume_files"].append(file.name)
                elif file.suffix == '.md':
                    summary["support_files"].append(file.name)
        
        return summary

