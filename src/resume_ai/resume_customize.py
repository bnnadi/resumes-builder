"""
Resume Customize - AI-powered resume customization for specific jobs.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import re
from .ollama_client import OllamaClient
from .prompts import load_prompt
from .skills_manager import SkillsManager
from .config_manager import get_config


@dataclass
class CustomizationResult:
    """Result from resume customization."""
    
    company_name: str
    role_title: str
    customized_resume_md: str
    analysis_md: str
    cover_letter_points_md: str
    application_checklist_md: str
    output_directory: Path
    files_created: list[Path]
    compensation_negotiation_guide_md: Optional[str] = None


class ResumeCustomizer:
    """Customize resumes for specific job descriptions using AI."""
    
    def __init__(self, ollama_client: OllamaClient, skills_manager: Optional[SkillsManager] = None):
        """
        Initialize resume customizer.
        
        Args:
            ollama_client: Configured Ollama client
            skills_manager: Optional skills manager (creates default if None)
        """
        self.ollama = ollama_client
        self.skills_manager = skills_manager or self._init_skills_manager()
    
    def _init_skills_manager(self) -> Optional[SkillsManager]:
        """Initialize skills manager if available."""
        try:
            return SkillsManager()
        except FileNotFoundError:
            # Skills inventory not found - will work without it
            return None
    
    def customize(
        self,
        job_description: str,
        base_resume_path: Optional[str | Path] = None,
        company_name: Optional[str] = None,
        role_title: Optional[str] = None,
        output_dir: Optional[str | Path] = None,
        verbose: bool = False
    ) -> CustomizationResult:
        """
        Customize resume for a specific job.
        
        Args:
            job_description: Full job posting text
            base_resume_path: Path to base resume (auto-detect if None)
            company_name: Company name (auto-extract if None)
            role_title: Job title (auto-extract if None)
            output_dir: Where to save files (auto-create if None)
            verbose: Show progress
            
        Returns:
            CustomizationResult with all generated files
        """
        # Load base resume
        if base_resume_path is None:
            if verbose:
                print("🔍 Finding base resume...")
            base_resume_path = self._find_base_resume(verbose)
        
        base_resume = Path(base_resume_path).read_text()
        
        if verbose:
            print(f"   Using: {Path(base_resume_path).name}")
        
        # Extract company and role if not provided
        if company_name is None or role_title is None:
            if verbose:
                print("🏢 Extracting company and role information...")
            extracted = self._extract_job_info(job_description)
            company_name = company_name or extracted["company"]
            role_title = role_title or extracted["role"]
        
        if verbose:
            print(f"   Company: {company_name}")
            print(f"   Role: {role_title}")
        
        # Create output directory
        if output_dir is None:
            output_dir = self._create_output_directory(company_name)
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        if verbose:
            print(f"📁 Output directory: {output_dir}")
        
        # Build prompt
        prompt = self._build_prompt(
            job_description,
            base_resume,
            company_name,
            role_title
        )
        
        # Call Ollama
        if verbose:
            print("\n🤖 Generating customized resume with AI...")
            print("   This may take 2-4 minutes...\n")
        
        response = self.ollama.generate(
            prompt=prompt,
            system="You are an expert resume consultant. Follow instructions precisely. "
                   "Maintain complete accuracy - never fabricate experience. "
                   "Output in clean Markdown format.",
            stream=verbose,
            verbose=verbose
        )
        
        # Parse and save outputs
        if verbose:
            print("\n💾 Saving files...")
        
        result = self._parse_and_save(
            response,
            company_name,
            role_title,
            output_dir,
            verbose
        )
        
        if verbose:
            print(f"\n✅ Complete! Files saved to: {output_dir}")
        
        return result
    
    def _find_base_resume(self, verbose: bool) -> Path:
        """Find base resume to use."""
        config = get_config()
        
        # Check if configured base resume exists
        base_resume = config.get_base_resume_path()
        if base_resume:
            if verbose:
                print(f"   Using configured base resume: {base_resume.name}")
            return base_resume
        
        # Search in configured directories
        search_dirs = config.get_resume_search_paths()
        
        # Look for "master" resume first
        for dir_path in search_dirs:
            if dir_path.exists():
                for pattern in ["*master*.md", "*Master*.md"]:
                    matches = list(dir_path.glob(pattern))
                    if matches:
                        return matches[0]
        
        # Fall back to any resume
        for dir_path in search_dirs:
            if dir_path.exists():
                matches = list(dir_path.glob("*resume*.md"))
                if matches:
                    # Return most recent
                    return max(matches, key=lambda p: p.stat().st_mtime)
        
        raise FileNotFoundError(
            "No base resume found.\n"
            f"Searched in: {', '.join(str(d) for d in search_dirs)}\n"
            "Options:\n"
            "  1. Specify with --base-resume option\n"
            "  2. Set base resume: resume-builder config set base-resume /path/to/resume.md\n"
            "  3. Run setup: resume-builder setup"
        )
    
    def _extract_job_info(self, job_description: str) -> dict:
        """Extract company name and role title from job description."""
        # Simple extraction - could be improved
        lines = job_description.split('\n')
        
        company = "Company"
        role = "Role"
        
        # Try to find common patterns
        for line in lines[:10]:  # Check first 10 lines
            if any(word in line.lower() for word in ["at ", "company", "about us"]):
                # Extract company name
                match = re.search(r'at ([A-Z][A-Za-z\s]+)', line)
                if match:
                    company = match.group(1).strip()
            
            if any(word in line.lower() for word in ["position:", "role:", "hiring"]):
                # Extract role
                role = line.split(':', 1)[-1].strip()
        
        # Sanitize for file names
        company = re.sub(r'[^\w\s-]', '', company).strip()
        company = re.sub(r'\s+', '_', company)
        
        return {"company": company, "role": role}
    
    def _create_output_directory(self, company_name: str) -> Path:
        """Create output directory for company."""
        config = get_config()
        base = config.get_output_directory()
        
        # Create base directory if it doesn't exist
        base.mkdir(parents=True, exist_ok=True)
        
        output_dir = base / company_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        return output_dir
    
    def _build_prompt(
        self,
        job_description: str,
        base_resume: str,
        company_name: str,
        role_title: str
    ) -> str:
        """Build prompt for Ollama."""
        # Extract current skills from resume
        current_skills = self._extract_skills_from_resume(base_resume)
        
        # Find matching skills from inventory
        suggested_skills_text = "Skills inventory not configured."
        
        if self.skills_manager:
            try:
                matching_skills = self.skills_manager.find_matching_skills(
                    job_description,
                    current_skills,
                    max_new_skills=8  # Allow up to 8 suggestions
                )
                
                if matching_skills:
                    suggested_skills_text = self.skills_manager.format_suggestions_for_prompt(
                        matching_skills,
                        include_scores=True
                    )
                else:
                    suggested_skills_text = "No additional skills from inventory match this job description."
            except Exception as e:
                suggested_skills_text = f"Error finding matching skills: {e}"
        
        template = load_prompt("resume_customize")
        
        prompt = template.format(
            job_description=job_description,
            base_resume=base_resume,
            company_name=company_name,
            role_title=role_title,
            suggested_skills=suggested_skills_text
        )
        
        return prompt
    
    def _extract_skills_from_resume(self, resume_text: str) -> dict:
        """
        Extract skills section from resume markdown.
        
        Args:
            resume_text: Full resume markdown text
            
        Returns:
            Dictionary of skills by category
        """
        skills = {}
        
        # Find Core Skills section
        skills_match = re.search(
            r'## Core Skills\s*\n(.*?)(?=\n## |\Z)',
            resume_text,
            re.DOTALL | re.IGNORECASE
        )
        
        if not skills_match:
            return skills
        
        skills_section = skills_match.group(1)
        current_category = "General"
        
        for line in skills_section.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Check for category heading (### or **bold**)
            if line.startswith('### '):
                current_category = line[4:].strip()
                skills[current_category] = []
            
            elif line.startswith('**') and ':' in line:
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
                if ',' in line and not line.startswith('-'):
                    skills[current_category].extend([s.strip() for s in line.split(',')])
                elif line:
                    # Remove bullet if present
                    skill = line.lstrip('- •*').strip()
                    if skill:
                        skills[current_category].append(skill)
        
        return skills
    
    def _parse_and_save(
        self,
        response: str,
        company_name: str,
        role_title: str,
        output_dir: Path,
        verbose: bool
    ) -> CustomizationResult:
        """Parse AI response and save files."""
        # Extract customized resume (between markers or in code block)
        resume_match = re.search(
            r'# CUSTOMIZED RESUME START(.*?)# CUSTOMIZED RESUME END',
            response,
            re.DOTALL
        )
        
        if not resume_match:
            # Try code block
            resume_match = re.search(
                r'```markdown\n(# .*?)\n```',
                response,
                re.DOTALL
            )
        
        customized_resume = resume_match.group(1).strip() if resume_match else ""
        
        # Save resume
        resume_file = output_dir / f"{company_name}_Bisike_Nnadi_Resume_2025.md"
        resume_file.write_text(customized_resume)
        
        # Save full analysis
        analysis_file = output_dir / f"{company_name}_Analysis.md"
        analysis_file.write_text(response)
        
        # Extract cover letter points (if present)
        cl_match = re.search(
            r'# COVER LETTER.*?$(.*?)(?=# |$)',
            response,
            re.MULTILINE | re.DOTALL
        )
        cover_letter = cl_match.group(1).strip() if cl_match else "See full analysis"
        cl_file = output_dir / f"{company_name}_Cover_Letter_Points.md"
        cl_file.write_text(f"# Cover Letter Key Points - {company_name}\n\n{cover_letter}")
        
        # Extract checklist (if present)
        checklist_match = re.search(
            r'# APPLICATION CHECKLIST(.*?)(?=# |$)',
            response,
            re.MULTILINE | re.DOTALL
        )
        checklist = checklist_match.group(1).strip() if checklist_match else "See full analysis"
        checklist_file = output_dir / f"{company_name}_Application_Checklist.md"
        checklist_file.write_text(f"# Application Checklist - {company_name}\n\n{checklist}")
        
        # Extract compensation negotiation guide (if present and relevant)
        # Match the section header and capture until next top-level heading (# ) or end of string
        compensation_match = re.search(
            r'# Compensation Negotiation Guide\s*\n(.*?)(?=\n# [^#]|$)',
            response,
            re.DOTALL | re.IGNORECASE
        )
        compensation_guide = None
        compensation_file = None
        
        if compensation_match:
            compensation_content = compensation_match.group(1).strip()
            # Only create file if content is substantial (not just placeholder)
            if compensation_content and len(compensation_content) > 100:
                compensation_guide = compensation_content
                compensation_file = output_dir / f"{company_name}_Compensation_Negotiation_Guide.md"
                compensation_file.write_text(f"# Compensation Negotiation Guide - {company_name}\n\n{compensation_content}")
        
        files_created = [resume_file, analysis_file, cl_file, checklist_file]
        if compensation_file:
            files_created.append(compensation_file)
        
        if verbose:
            print(f"   ✓ {resume_file.name}")
            print(f"   ✓ {analysis_file.name}")
            print(f"   ✓ {cl_file.name}")
            print(f"   ✓ {checklist_file.name}")
            if compensation_file:
                print(f"   ✓ {compensation_file.name}")
        
        return CustomizationResult(
            company_name=company_name,
            role_title=role_title,
            customized_resume_md=customized_resume,
            analysis_md=response,
            cover_letter_points_md=cover_letter,
            application_checklist_md=checklist,
            compensation_negotiation_guide_md=compensation_guide,
            output_directory=output_dir,
            files_created=files_created
        )

