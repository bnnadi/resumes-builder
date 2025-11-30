"""
Markdown Resume Parser

Parses markdown-formatted resumes into structured data for export.
"""

import re
from typing import Dict, List, Any, Optional
from pathlib import Path


class ResumeParser:
    """Parse markdown resume into structured data."""
    
    def __init__(self, markdown_path: Path):
        """
        Initialize parser with markdown file.
        
        Args:
            markdown_path: Path to markdown resume file
        """
        self.markdown_path = Path(markdown_path)
        self.content = self._read_file()
        self.lines = self.content.split('\n')
        self.current_line = 0
        
    def _read_file(self) -> str:
        """Read markdown file content."""
        if not self.markdown_path.exists():
            raise FileNotFoundError(f"Resume file not found: {self.markdown_path}")
        
        with open(self.markdown_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def parse(self) -> Dict[str, Any]:
        """
        Parse markdown resume into structured data.
        
        Returns:
            Dictionary with structured resume data
        """
        data = {
            "name": "",
            "contact": {},
            "summary": "",
            "skills": {},
            "experience": [],
            "education": [],
            "certifications": [],
            "raw_sections": {}  # Store any other sections
        }
        
        # Parse name (first H1)
        data["name"] = self._extract_name()
        
        # Parse contact info (lines after name, before first H2)
        data["contact"] = self._extract_contact()
        
        # Parse sections
        sections = self._split_into_sections()
        
        for section_name, section_content in sections.items():
            section_lower = section_name.lower()
            
            if "summary" in section_lower:
                data["summary"] = self._parse_summary(section_content)
            
            elif "skill" in section_lower:
                data["skills"] = self._parse_skills(section_content)
            
            elif "experience" in section_lower:
                data["experience"] = self._parse_experience(section_content)
            
            elif "education" in section_lower:
                data["education"] = self._parse_education(section_content)
            
            elif "certification" in section_lower:
                data["certifications"] = self._parse_certifications(section_content)
            
            else:
                # Store other sections as-is
                data["raw_sections"][section_name] = section_content
        
        return data
    
    def _extract_name(self) -> str:
        """Extract name from first H1."""
        for line in self.lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
        return "Resume"
    
    def _extract_contact(self) -> Dict[str, str]:
        """Extract contact information from lines after name."""
        contact = {
            "location": "",
            "email": "",
            "phone": "",
            "linkedin": "",
            "github": "",
            "website": ""
        }
        
        # Find lines between first H1 and first H2
        in_contact_section = False
        contact_lines = []
        
        for line in self.lines:
            line = line.strip()
            
            if line.startswith('# '):
                in_contact_section = True
                continue
            
            if line.startswith('## '):
                break
            
            if in_contact_section and line:
                contact_lines.append(line)
        
        # Parse contact lines
        contact_text = ' '.join(contact_lines)
        
        # Extract email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', contact_text)
        if email_match:
            contact["email"] = email_match.group(0)
        
        # Extract phone
        phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', contact_text)
        if phone_match:
            contact["phone"] = phone_match.group(0)
        
        # Extract LinkedIn
        linkedin_match = re.search(r'[Ll]inked[Ii]n:\s*([\w\.\-/]+)', contact_text)
        if linkedin_match:
            contact["linkedin"] = linkedin_match.group(1)
        
        # Extract GitHub
        github_match = re.search(r'[Gg]it[Hh]ub:\s*([\w\.\-/]+)', contact_text)
        if github_match:
            contact["github"] = github_match.group(1)
        
        # Extract location (first line that's not email/phone/linkedin/github)
        for line in contact_lines:
            line_clean = line.strip()
            # Check if line doesn't contain other contact info
            if (line_clean and 
                not '@' in line_clean and 
                not 'linkedin' in line_clean.lower() and 
                not 'github' in line_clean.lower() and
                not re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', line_clean)):
                # Remove pipe separators and extra text
                location = re.split(r'\|', line_clean)[0].strip()
                if location:
                    contact["location"] = location
                    break
        
        return contact
    
    def _split_into_sections(self) -> Dict[str, str]:
        """Split markdown into major sections (H2)."""
        sections = {}
        current_section = None
        section_content = []
        
        for line in self.lines:
            # Check for H2 section header
            if line.startswith('## '):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(section_content)
                
                # Start new section
                current_section = line[3:].strip()
                section_content = []
            
            elif current_section:
                section_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(section_content)
        
        return sections
    
    def _parse_summary(self, content: str) -> str:
        """Parse summary section."""
        # Remove empty lines and return clean text
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        return ' '.join(lines)
    
    def _parse_skills(self, content: str) -> Dict[str, List[str]]:
        """Parse skills section."""
        skills = {}
        current_category = "General"
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Check for category heading (### or **bold**)
            if line.startswith('### '):
                current_category = line[4:].strip()
                skills[current_category] = []
            
            elif line.startswith('**') and line.endswith('**'):
                # Bold category without H3
                current_category = line.strip('*').strip()
                skills[current_category] = []
            
            elif '**' in line and ':' in line:
                # Format: **Category**: skill1, skill2
                match = re.match(r'\*\*([^*]+)\*\*:\s*(.+)', line)
                if match:
                    category = match.group(1).strip()
                    skills_text = match.group(2).strip()
                    skills[category] = [s.strip() for s in skills_text.split(',')]
            
            else:
                # Regular skill item
                if current_category not in skills:
                    skills[current_category] = []
                
                # Split by comma if multiple skills
                if ',' in line:
                    skills[current_category].extend([s.strip() for s in line.split(',')])
                else:
                    skills[current_category].append(line)
        
        return skills
    
    def _parse_experience(self, content: str) -> List[Dict[str, Any]]:
        """Parse experience section."""
        experiences = []
        current_job = None
        
        for line in content.split('\n'):
            line_stripped = line.strip()
            
            # Check for job heading (### Title | Company | Dates)
            if line_stripped.startswith('### '):
                # Save previous job
                if current_job:
                    experiences.append(current_job)
                
                # Parse job title line
                job_line = line_stripped[4:]  # Remove ###
                current_job = self._parse_job_header(job_line)
                current_job["achievements"] = []
            
            # Check for dates line (italic)
            elif line_stripped.startswith('*') and line_stripped.endswith('*'):
                if current_job and not current_job.get("dates"):
                    current_job["dates"] = line_stripped.strip('*').strip()
            
            # Check for description paragraph (before bullets)
            elif (current_job and 
                  line_stripped and 
                  not line_stripped.startswith('-') and 
                  not line_stripped.startswith('*') and
                  not current_job.get("description")):
                current_job["description"] = line_stripped
            
            # Check for achievement bullet
            elif line_stripped.startswith('- '):
                if current_job:
                    achievement = line_stripped[2:].strip()
                    current_job["achievements"].append(achievement)
        
        # Save last job
        if current_job:
            experiences.append(current_job)
        
        return experiences
    
    def _parse_job_header(self, header_line: str) -> Dict[str, str]:
        """Parse job header line (Title | Company | Dates)."""
        job = {
            "title": "",
            "company": "",
            "location": "",
            "dates": "",
            "description": ""
        }
        
        # Split by pipe
        parts = [p.strip() for p in header_line.split('|')]
        
        if len(parts) >= 1:
            job["title"] = parts[0]
        
        if len(parts) >= 2:
            job["company"] = parts[1]
        
        if len(parts) >= 3:
            # Could be location or dates
            third_part = parts[2]
            # Check if it looks like dates
            if re.search(r'\d{4}|[Jj]an|[Ff]eb|[Mm]ar|[Aa]pr|[Mm]ay|[Jj]un|[Jj]ul|[Aa]ug|[Ss]ep|[Oo]ct|[Nn]ov|[Dd]ec', third_part):
                job["dates"] = third_part
            else:
                job["location"] = third_part
        
        if len(parts) >= 4:
            job["dates"] = parts[3]
        
        return job
    
    def _parse_education(self, content: str) -> List[Dict[str, str]]:
        """Parse education section."""
        education = []
        current_edu = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Check for degree line (starts with **)
            if line.startswith('**') and '**' in line[2:]:
                # Save previous entry
                if current_edu:
                    education.append(current_edu)
                
                # Parse: **Degree** | University | Year
                degree_match = re.match(r'\*\*([^*]+)\*\*(.+)?', line)
                if degree_match:
                    degree = degree_match.group(1).strip()
                    rest = degree_match.group(2).strip() if degree_match.group(2) else ""
                    
                    current_edu = {
                        "degree": degree,
                        "school": "",
                        "year": "",
                        "details": []
                    }
                    
                    # Parse rest of line
                    if rest:
                        rest = rest.lstrip('|-').strip()
                        # Split by pipe or dash
                        parts = re.split(r'\s*[|\-]\s*', rest)
                        if len(parts) >= 1:
                            current_edu["school"] = parts[0].strip()
                        if len(parts) >= 2:
                            # Extract year
                            year_match = re.search(r'\d{4}', parts[1])
                            if year_match:
                                current_edu["year"] = year_match.group(0)
                            else:
                                current_edu["year"] = parts[1].strip()
            
            # Additional details
            elif current_edu:
                current_edu["details"].append(line)
        
        # Save last entry
        if current_edu:
            education.append(current_edu)
        
        return education
    
    def _parse_certifications(self, content: str) -> List[str]:
        """Parse certifications section."""
        certifications = []
        
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Remove bullet points
                if line.startswith('- '):
                    line = line[2:]
                certifications.append(line)
        
        return certifications


def parse_resume(markdown_path: Path) -> Dict[str, Any]:
    """
    Convenience function to parse a markdown resume.
    
    Args:
        markdown_path: Path to markdown resume file
    
    Returns:
        Structured resume data
    """
    parser = ResumeParser(markdown_path)
    return parser.parse()

