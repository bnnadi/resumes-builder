"""
Job Match - Analyze how well a resume matches a job description.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import re
from .ollama_client import OllamaClient
from .prompts import load_prompt
from .config_manager import get_config


@dataclass
class JobMatchResult:
    """Result from job-match analysis."""
    
    overall_fit_score: int
    interview_probability: float
    matching_strengths: list[str]
    gaps: list[str]
    seniority_alignment: str
    ats_keyword_match: int
    ats_structural_readiness: int
    ats_pass_probability: float
    highest_impact_improvements: list[str]
    final_verdict: str
    raw_output: str


class JobMatcher:
    """Analyze resume fit against job description using AI."""
    
    def __init__(self, ollama_client: OllamaClient):
        """
        Initialize job matcher.
        
        Args:
            ollama_client: Configured Ollama client
        """
        self.ollama = ollama_client
    
    def match(
        self,
        job_description: str,
        resume_text: Optional[str] = None,
        resume_path: Optional[str | Path] = None,
        verbose: bool = False
    ) -> JobMatchResult:
        """
        Analyze how well resume matches job description.
        
        Args:
            job_description: Job posting text
            resume_text: Resume text (if pasting directly)
            resume_path: Path to resume file or "auto" to search
            verbose: Show progress
            
        Returns:
            JobMatchResult with detailed analysis
            
        Raises:
            ValueError: If neither resume_text nor resume_path provided
            FileNotFoundError: If resume file not found
        """
        # Load resume
        if resume_text is None:
            if resume_path is None:
                resume_path = "auto"
            resume_text = self._load_resume(resume_path, verbose)
        
        # Build prompt
        prompt = self._build_prompt(job_description, resume_text)
        
        # Call Ollama
        if verbose:
            print("\n🤖 Analyzing job match with AI...")
            print("   This may take 30-60 seconds...\n")
        
        response = self.ollama.generate(
            prompt=prompt,
            system="You are an expert technical recruiter and ATS specialist. "
                   "Provide realistic, unbiased analysis. No optimism bias.",
            stream=verbose,
            verbose=verbose
        )
        
        # Parse response
        result = self._parse_response(response)
        
        if verbose:
            print("\n✅ Analysis complete")
        
        return result
    
    def _load_resume(self, resume_path: str | Path, verbose: bool) -> str:
        """
        Load resume from file system.
        
        Args:
            resume_path: Path to resume or "auto" to search
            verbose: Show progress
            
        Returns:
            Resume text
        """
        if resume_path == "auto":
            if verbose:
                print("🔍 Searching for most recent resume...")
            resume_path = self._find_latest_resume()
            if verbose:
                print(f"   Found: {resume_path}")
        
        path = Path(resume_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Resume not found: {path}")
        
        if path.suffix == ".md":
            return path.read_text()
        elif path.suffix == ".docx":
            # Use python-docx to extract text
            from docx import Document
            doc = Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
        elif path.suffix in [".txt", ".rtf"]:
            return path.read_text()
        else:
            # Try to read as text anyway
            return path.read_text()
    
    def _find_latest_resume(self) -> Path:
        """
        Find most recent resume file in configured locations.
        
        Returns:
            Path to most recent resume
            
        Raises:
            FileNotFoundError: If no resume found
        """
        config = get_config()
        
        # Check configured base resume first
        base_resume = config.get_base_resume_path()
        if base_resume:
            return base_resume
        
        # Search in configured directories
        search_dirs = config.get_resume_search_paths()
        
        resume_files = []
        patterns = [
            "*resume*.md",
            "*resume*.docx",
            "*cv*.md",
            "*cv*.docx",
            "*Resume*.md",
            "*Resume*.docx"
        ]
        
        for dir_path in search_dirs:
            if dir_path.exists():
                for pattern in patterns:
                    resume_files.extend(dir_path.rglob(pattern))
        
        if not resume_files:
            raise FileNotFoundError(
                "No resume found in configured locations.\n"
                f"Searched in: {', '.join(str(d) for d in search_dirs)}\n"
                "Options:\n"
                "  1. Use --resume-path to specify resume file\n"
                "  2. Set base resume: resume-builder config set base-resume /path/to/resume.md\n"
                "  3. Run setup: resume-builder setup"
            )
        
        # Return most recently modified
        return max(resume_files, key=lambda p: p.stat().st_mtime)
    
    def _build_prompt(self, job_description: str, resume_text: str) -> str:
        """
        Build prompt for Ollama based on job-match spec.
        
        Args:
            job_description: Job posting
            resume_text: Resume content
            
        Returns:
            Formatted prompt
        """
        template = load_prompt("job_match")
        
        prompt = template.format(
            job_description=job_description,
            resume_text=resume_text
        )
        
        return prompt
    
    def _parse_response(self, response: str) -> JobMatchResult:
        """
        Parse Ollama response into structured result.
        
        Args:
            response: Raw response from Ollama
            
        Returns:
            JobMatchResult with parsed data
        """
        # Extract scores and data using regex
        overall_match = re.search(r'Overall Fit Score[:\s]+(\d+)', response, re.IGNORECASE)
        interview_prob = re.search(r'Interview Probability[:\s]+(\d+)%?', response, re.IGNORECASE)
        keyword_match = re.search(r'Keyword Match Score[:\s]+(\d+)', response, re.IGNORECASE)
        structural = re.search(r'Structural.*?Readiness[:\s]+(\d+)', response, re.IGNORECASE)
        ats_pass = re.search(r'ATS Pass Probability[:\s]+(\d+)%?', response, re.IGNORECASE)
        
        # Extract seniority alignment
        seniority_match = re.search(
            r'Seniority Alignment[:\s]+([\w\s-]+?)(?:\n|$)',
            response,
            re.IGNORECASE
        )
        seniority = seniority_match.group(1).strip() if seniority_match else "Unknown"
        
        # Extract lists (strengths, gaps, improvements)
        strengths = self._extract_list_section(response, "Matching Strengths")
        gaps = self._extract_list_section(response, "Gaps")
        improvements = self._extract_list_section(response, "Highest Impact Improvements")
        
        # Extract verdict
        verdict_match = re.search(
            r'Final Verdict[:\s]+(.*?)(?:\n\n|$)',
            response,
            re.IGNORECASE | re.DOTALL
        )
        verdict = verdict_match.group(1).strip() if verdict_match else ""
        
        return JobMatchResult(
            overall_fit_score=int(overall_match.group(1)) if overall_match else 0,
            interview_probability=float(interview_prob.group(1))/100 if interview_prob else 0.0,
            matching_strengths=strengths,
            gaps=gaps,
            seniority_alignment=seniority,
            ats_keyword_match=int(keyword_match.group(1)) if keyword_match else 0,
            ats_structural_readiness=int(structural.group(1)) if structural else 0,
            ats_pass_probability=float(ats_pass.group(1))/100 if ats_pass else 0.0,
            highest_impact_improvements=improvements,
            final_verdict=verdict,
            raw_output=response
        )
    
    def _extract_list_section(self, text: str, section_name: str) -> list[str]:
        """
        Extract bullet points from a section.
        
        Args:
            text: Full response text
            section_name: Section to extract
            
        Returns:
            List of items
        """
        # Find section
        pattern = rf'{section_name}[:\s]+(.*?)(?=\n\n|\n#|$)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        
        if not match:
            return []
        
        section_text = match.group(1)
        
        # Extract bullet points
        items = []
        for line in section_text.split('\n'):
            line = line.strip()
            # Remove bullet markers
            line = re.sub(r'^[-*•]\s*', '', line)
            line = re.sub(r'^\d+\.\s*', '', line)
            if line:
                items.append(line)
        
        return items[:5]  # Return top 5

