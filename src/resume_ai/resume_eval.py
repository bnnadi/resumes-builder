"""
Resume Eval - Evaluate and compare multiple resumes, generate master resume.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from .ollama_client import OllamaClient
from .prompts import load_prompt


@dataclass
class ResumeEvaluation:
    """Evaluation results for a single resume."""
    
    resume_id: str
    interview_probability: float
    ats_pass_probability: float
    technical_versatility: str
    strengths: list[str]
    weaknesses: list[str]
    ats_formatting_issues: list[str]
    keyword_gaps: list[str]
    raw_analysis: str


@dataclass
class ResumeEvalResult:
    """Complete resume evaluation results."""
    
    evaluations: list[ResumeEvaluation]
    cross_comparison: str
    master_resume_md: str
    implementation_notes: str
    raw_output: str


class ResumeEvaluator:
    """Evaluate resumes and generate master resume using AI."""
    
    def __init__(self, ollama_client: OllamaClient):
        """
        Initialize resume evaluator.
        
        Args:
            ollama_client: Configured Ollama client
        """
        self.ollama = ollama_client
    
    def evaluate(
        self,
        resume_text: Optional[str] = None,
        search_scope: Optional[str | Path] = None,
        verbose: bool = False
    ) -> ResumeEvalResult:
        """
        Evaluate resumes and generate master resume.
        
        Args:
            resume_text: Optional resume text to evaluate
            search_scope: Optional directory to search for resumes
            verbose: Show progress
            
        Returns:
            ResumeEvalResult with complete analysis
        """
        # Find resumes
        if verbose:
            print("🔍 Discovering resumes...")
        
        resumes = self._discover_resumes(search_scope, verbose)
        
        # Add pasted resume if provided
        if resume_text:
            resumes.append(("Pasted Resume", resume_text))
        
        if not resumes:
            raise ValueError(
                "No resumes found.\n"
                "Either paste a resume or ensure resume files exist in search locations."
            )
        
        if verbose:
            print(f"   Found {len(resumes)} resume(s)")
            for i, (name, _) in enumerate(resumes, 1):
                print(f"   {i}. {name}")
        
        # Build prompt
        prompt = self._build_prompt(resumes)
        
        # Call Ollama
        if verbose:
            print("\n🤖 Evaluating resumes with AI...")
            print("   This may take 2-3 minutes for multiple resumes...\n")
        
        response = self.ollama.generate(
            prompt=prompt,
            system="You are an expert resume consultant and ATS specialist. "
                   "Provide detailed, actionable analysis in clean Markdown format.",
            stream=verbose,
            verbose=verbose
        )
        
        # Parse response
        result = self._parse_response(response, resumes)
        
        if verbose:
            print("\n✅ Evaluation complete")
        
        return result
    
    def _discover_resumes(
        self,
        search_scope: Optional[str | Path],
        verbose: bool
    ) -> list[tuple[str, str]]:
        """
        Discover resume files in file system.
        
        Args:
            search_scope: Optional directory to search
            verbose: Show progress
            
        Returns:
            List of (resume_name, resume_text) tuples
        """
        if search_scope:
            search_dirs = [Path(search_scope)]
        else:
            search_dirs = [
                Path.home() / "Research" / "resumes",
                Path.home() / "Research" / "resumes" / "applications",
                Path.home() / "Documents",
                Path.cwd()
            ]
        
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
                    if search_scope:
                        # Use glob for single directory
                        resume_files.extend(dir_path.glob(pattern))
                    else:
                        # Use rglob for recursive search
                        resume_files.extend(list(dir_path.rglob(pattern))[:5])  # Limit to 5
        
        # Remove duplicates
        resume_files = list(set(resume_files))
        
        # Load and return
        resumes = []
        for i, path in enumerate(resume_files[:5], 1):  # Max 5 resumes
            try:
                if path.suffix == ".md":
                    text = path.read_text()
                elif path.suffix == ".docx":
                    from docx import Document
                    doc = Document(path)
                    text = "\n".join(p.text for p in doc.paragraphs)
                else:
                    text = path.read_text()
                
                resumes.append((f"Resume {chr(64+i)} ({path.name})", text))
            except Exception as e:
                if verbose:
                    print(f"   ⚠️  Skipped {path.name}: {e}")
        
        return resumes
    
    def _build_prompt(self, resumes: list[tuple[str, str]]) -> str:
        """
        Build prompt for Ollama.
        
        Args:
            resumes: List of (name, text) tuples
            
        Returns:
            Formatted prompt
        """
        template = load_prompt("resume_eval")
        
        # Format resumes section
        resumes_section = ""
        for name, text in resumes:
            resumes_section += f"\n\n## {name}\n\n{text}\n\n{'='*80}"
        
        prompt = template.format(
            resumes_count=len(resumes),
            resumes_section=resumes_section
        )
        
        return prompt
    
    def _parse_response(
        self,
        response: str,
        resumes: list[tuple[str, str]]
    ) -> ResumeEvalResult:
        """
        Parse Ollama response.
        
        Args:
            response: Raw response
            resumes: Original resumes list
            
        Returns:
            ResumeEvalResult
        """
        # For now, return simple structure
        # In practice, you'd parse sections more carefully
        
        evaluations = []
        for i, (name, _) in enumerate(resumes, 1):
            evaluations.append(ResumeEvaluation(
                resume_id=name,
                interview_probability=0.0,  # Would parse from response
                ats_pass_probability=0.0,
                technical_versatility="Unknown",
                strengths=[],
                weaknesses=[],
                ats_formatting_issues=[],
                keyword_gaps=[],
                raw_analysis=""
            ))
        
        # Extract master resume if present
        import re
        master_match = re.search(
            r'```markdown\n(.*?)\n```',
            response,
            re.DOTALL
        )
        master_resume = master_match.group(1) if master_match else ""
        
        return ResumeEvalResult(
            evaluations=evaluations,
            cross_comparison="",
            master_resume_md=master_resume,
            implementation_notes="",
            raw_output=response
        )

