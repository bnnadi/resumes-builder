"""
Threshold Gate - Determines whether to proceed based on match scores.
"""

from dataclasses import dataclass
from typing import Literal
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Type for decision outcomes
Decision = Literal["continue", "stop", "ask"]


@dataclass
class ThresholdConfig:
    """Configuration for match score thresholds."""
    
    minimum_overall: int = 70
    borderline_min: int = 60
    borderline_max: int = 69
    auto_stop_below: bool = True
    ask_on_borderline: bool = True


class ThresholdGate:
    """Evaluates match scores and determines whether to continue workflow."""
    
    def __init__(self, config: ThresholdConfig | None = None):
        """
        Initialize threshold gate.
        
        Args:
            config: Threshold configuration. Uses defaults if not provided.
        """
        self.config = config or ThresholdConfig()
        self.console = Console()
    
    def evaluate(self, match_score: int) -> Decision:
        """
        Evaluate match score against thresholds.
        
        Args:
            match_score: Overall fit score (0-100)
            
        Returns:
            Decision: "continue", "stop", or "ask"
        """
        if match_score >= self.config.minimum_overall:
            return "continue"
        
        elif self.config.borderline_min <= match_score < self.config.minimum_overall:
            if self.config.ask_on_borderline:
                return "ask"
            else:
                return "stop" if self.config.auto_stop_below else "continue"
        
        else:  # Below borderline_min
            return "stop"
    
    def print_decision(
        self,
        match_score: int,
        decision: Decision,
        match_result
    ) -> None:
        """
        Print formatted decision message.
        
        Args:
            match_score: Overall fit score
            decision: Decision outcome
            match_result: JobMatchResult object with details
        """
        if decision == "continue":
            self._print_good_match(match_score, match_result)
        elif decision == "stop":
            self._print_poor_match(match_score, match_result)
        else:  # ask
            self._print_borderline_match(match_score, match_result)
    
    def _print_good_match(self, score: int, result) -> None:
        """Print good match message."""
        self.console.print()
        self.console.print(Panel.fit(
            f"[bold green]✅ GOOD MATCH[/bold green]\n\n"
            f"Score: {score}/100\n"
            f"Interview Probability: {result.interview_probability:.0%}\n"
            f"ATS Pass Probability: {result.ats_pass_probability:.0%}\n\n"
            f"[green]Continuing with customization...[/green]",
            title="Match Score",
            border_style="green"
        ))
    
    def _print_poor_match(self, score: int, result) -> None:
        """Print poor match warning."""
        self.console.print()
        
        # Build gaps table
        table = Table(show_header=False, box=None)
        table.add_column("", style="red")
        for gap in result.gaps[:5]:
            table.add_row(f"❌ {gap}")
        
        self.console.print(Panel(
            f"[bold red]❌ POOR MATCH[/bold red]\n\n"
            f"Score: {score}/100 (below {self.config.minimum_overall}% threshold)\n"
            f"Interview Probability: {result.interview_probability:.0%}\n\n"
            f"[bold]Key Gaps:[/bold]\n",
            title="Match Score",
            border_style="red"
        ))
        self.console.print(table)
        self.console.print()
        self.console.print(
            "[yellow]💡 RECOMMENDATION:[/yellow] Skip this application.\n"
            "   Focus on better-fit opportunities (70+ score).\n\n"
            "[dim]   To proceed anyway, use --force flag[/dim]"
        )
    
    def _print_borderline_match(self, score: int, result) -> None:
        """Print borderline match prompt."""
        self.console.print()
        
        # Build strengths and gaps
        strengths_text = "\n".join(f"  ✅ {s}" for s in result.matching_strengths[:3])
        gaps_text = "\n".join(f"  ❌ {g}" for g in result.gaps[:3])
        
        self.console.print(Panel(
            f"[bold yellow]⚠️  BORDERLINE MATCH[/bold yellow]\n\n"
            f"Score: {score}/100 (below {self.config.minimum_overall}% threshold)\n"
            f"Interview Probability: {result.interview_probability:.0%}\n\n"
            f"[bold]Strengths:[/bold]\n{strengths_text}\n\n"
            f"[bold]Gaps:[/bold]\n{gaps_text}\n\n"
            f"[yellow]This is close but slightly below recommended threshold.[/yellow]",
            title="Match Score",
            border_style="yellow"
        ))
    
    def prompt_user_continue(self) -> bool:
        """
        Prompt user whether to continue with borderline match.
        
        Returns:
            True if user wants to continue
        """
        from rich.prompt import Confirm
        
        return Confirm.ask(
            "\n[bold]Continue with customization?[/bold]",
            default=False
        )

