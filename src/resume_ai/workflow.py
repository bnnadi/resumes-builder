"""
Workflow - Complete end-to-end resume workflow with threshold gating.
"""

from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from .ollama_client import OllamaClient, OllamaConfig
from .job_match import JobMatcher, JobMatchResult
from .resume_customize import ResumeCustomizer, CustomizationResult
from .threshold_gate import ThresholdGate, ThresholdConfig
from .skills_manager import SkillsManager
from ..resume_export.exporter import ResumeExporter


@dataclass
class WorkflowResult:
    """Result from complete workflow."""
    
    status: str  # "completed", "stopped_low_score", "stopped_user"
    match_result: Optional[JobMatchResult] = None
    customization_result: Optional[CustomizationResult] = None
    export_path: Optional[Path] = None
    package_dir: Optional[Path] = None


class ResumeWorkflow:
    """Orchestrates complete resume workflow with AI and threshold gating."""
    
    def __init__(
        self,
        ollama_config: Optional[OllamaConfig] = None,
        threshold_config: Optional[ThresholdConfig] = None,
        skills_manager: Optional[SkillsManager] = None
    ):
        """
        Initialize workflow.
        
        Args:
            ollama_config: Ollama configuration
            threshold_config: Threshold configuration
            skills_manager: Skills manager for inventory-based customization
        """
        self.ollama = OllamaClient(ollama_config)
        self.threshold = ThresholdGate(threshold_config)
        self.job_matcher = JobMatcher(self.ollama)
        self.skills_manager = skills_manager or self._init_skills_manager()
        self.customizer = ResumeCustomizer(self.ollama, self.skills_manager)
    
    def _init_skills_manager(self) -> Optional[SkillsManager]:
        """Initialize skills manager if available."""
        try:
            return SkillsManager()
        except FileNotFoundError:
            return None
    
    def process(
        self,
        job_posting_path: Path,
        base_resume_path: Optional[Path] = None,
        company_name: Optional[str] = None,
        output_dir: Optional[Path] = None,
        force: bool = False,
        skip_export: bool = False,
        verbose: bool = True
    ) -> WorkflowResult:
        """
        Execute complete workflow: match → threshold → customize → export.
        
        Args:
            job_posting_path: Path to job posting file
            base_resume_path: Path to base resume (auto-detect if None)
            company_name: Company name (auto-extract if None)
            output_dir: Output directory (auto-create if None)
            force: Skip threshold check
            skip_export: Stop after customization
            verbose: Show progress
            
        Returns:
            WorkflowResult with all generated files
        """
        # Read job posting
        job_text = job_posting_path.read_text()
        
        # STEP 1: Job Match
        if verbose:
            print("=" * 70)
            print("STEP 1/4: Analyzing Job Match")
            print("=" * 70)
        
        match_result = self.job_matcher.match(
            job_description=job_text,
            resume_path=base_resume_path,
            verbose=verbose
        )
        
        # Print match results
        if verbose:
            self._print_match_summary(match_result)
        
        # STEP 2: Threshold Gate
        if not force:
            decision = self.threshold.evaluate(match_result.overall_fit_score)
            
            self.threshold.print_decision(
                match_result.overall_fit_score,
                decision,
                match_result
            )
            
            if decision == "stop":
                return WorkflowResult(
                    status="stopped_low_score",
                    match_result=match_result
                )
            
            elif decision == "ask":
                if not self.threshold.prompt_user_continue():
                    return WorkflowResult(
                        status="stopped_user",
                        match_result=match_result
                    )
        
        # STEP 3: Customize
        if verbose:
            print("\n" + "=" * 70)
            print("STEP 3/4: Customizing Resume")
            print("=" * 70)
        
        customization_result = self.customizer.customize(
            job_description=job_text,
            base_resume_path=base_resume_path,
            company_name=company_name,
            output_dir=output_dir,
            verbose=verbose
        )
        
        if skip_export:
            return WorkflowResult(
                status="completed",
                match_result=match_result,
                customization_result=customization_result
            )
        
        # STEP 4: Export
        if verbose:
            print("\n" + "=" * 70)
            print("STEP 4/4: Exporting to .docx")
            print("=" * 70)
        
        # Get resume markdown file
        resume_md = customization_result.output_directory / \
                   f"{customization_result.company_name}_Bisike_Nnadi_Resume_2025.md"
        
        # Export using existing export functionality
        exporter = ResumeExporter()
        export_result = exporter.export(
            str(resume_md),
            formats=["docx"],
            validate=True
        )
        
        if verbose:
            print(f"\n✅ Resume exported: {export_result.output_files['docx']}")
        
        # Create package
        from ..resume_export.package_builder import PackageBuilder
        builder = PackageBuilder()
        package_dir = builder.build_package(
            str(customization_result.output_directory)
        )
        
        if verbose:
            print(f"✅ Package complete: {package_dir}")
        
        # Final summary
        if verbose:
            self._print_final_summary(
                match_result,
                customization_result,
                export_result.output_files['docx']
            )
        
        return WorkflowResult(
            status="completed",
            match_result=match_result,
            customization_result=customization_result,
            export_path=Path(export_result.output_files['docx']),
            package_dir=Path(package_dir)
        )
    
    def _print_match_summary(self, result: JobMatchResult) -> None:
        """Print formatted match summary."""
        from rich.console import Console
        from rich.table import Table
        
        console = Console()
        
        table = Table(title="Match Analysis", show_header=False)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold")
        
        table.add_row("Overall Fit Score", f"{result.overall_fit_score}/100")
        table.add_row("Interview Probability", f"{result.interview_probability:.0%}")
        table.add_row("ATS Pass Probability", f"{result.ats_pass_probability:.0%}")
        table.add_row("Seniority Alignment", result.seniority_alignment)
        
        console.print()
        console.print(table)
    
    def _print_final_summary(
        self,
        match_result: JobMatchResult,
        customization_result: CustomizationResult,
        export_path: str
    ) -> None:
        """Print final workflow summary."""
        from rich.console import Console
        from rich.panel import Panel
        
        console = Console()
        
        compensation_line = ""
        if customization_result.compensation_negotiation_guide_md:
            compensation_line = f"  💰 Compensation Guide: {customization_result.company_name}_Compensation_Negotiation_Guide.md\n"
        
        summary = f"""
[bold green]✅ Workflow Complete![/bold green]

[bold]Match Score:[/bold] {match_result.overall_fit_score}/100
[bold]Company:[/bold] {customization_result.company_name}
[bold]Role:[/bold] {customization_result.role_title}

[bold]Files Created:[/bold]
  📄 Resume (.docx): {Path(export_path).name}
  📝 Analysis: {customization_result.company_name}_Analysis.md
  💼 Cover Letter Points: {customization_result.company_name}_Cover_Letter_Points.md
  ✅ Checklist: {customization_result.company_name}_Application_Checklist.md
{compensation_line}[bold]Location:[/bold] {customization_result.output_directory}

[bold cyan]Next Steps:[/bold cyan]
  1. Review the customized .docx resume
  2. Read cover letter points for key talking points
  3. Use checklist before submitting
"""
        
        console.print()
        console.print(Panel(summary, border_style="green"))

