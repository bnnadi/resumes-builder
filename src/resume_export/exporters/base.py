"""Base exporter class for format-specific exporters."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseExporter(ABC):
    """Base class for format-specific exporters."""
    
    @abstractmethod
    def export(self, resume_data: Dict[str, Any], output_path: Path) -> bool:
        """
        Export resume to specific format.
        
        Args:
            resume_data: Structured resume data
            output_path: Path for output file
        
        Returns:
            True if successful, False otherwise
        """
        pass
    
    def validate_input(self, resume_data: Dict[str, Any]) -> bool:
        """Validate input resume data."""
        required_fields = ["name", "contact"]
        return all(field in resume_data for field in required_fields)

