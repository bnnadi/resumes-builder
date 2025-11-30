"""
Prompt Templates - Load AI prompts from template files.
"""

from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


def load_prompt(name: str) -> str:
    """
    Load prompt template by name.
    
    Args:
        name: Prompt name (without .txt extension)
        
    Returns:
        Prompt template string
        
    Raises:
        FileNotFoundError: If prompt template not found
    """
    path = PROMPTS_DIR / f"{name}.txt"
    
    if not path.exists():
        raise FileNotFoundError(
            f"Prompt template not found: {name}\n"
            f"Expected at: {path}"
        )
    
    return path.read_text()


def list_prompts() -> list[str]:
    """
    List available prompt templates.
    
    Returns:
        List of prompt names
    """
    return [
        p.stem
        for p in PROMPTS_DIR.glob("*.txt")
    ]

