"""DOCX format exporter."""

from pathlib import Path
from typing import Dict, Any

from .base import BaseExporter
from ..docx_builder import DocxBuilder


class DocxExporter(BaseExporter):
    """Export resume to .docx format."""
    
    def __init__(self, template_path: Path = None):
        """Initialize DOCX exporter."""
        self.template_path = template_path
    
    def export(self, resume_data: Dict[str, Any], output_path: Path) -> bool:
        """
        Export resume to .docx.
        
        Args:
            resume_data: Structured resume data
            output_path: Path for output .docx file
        
        Returns:
            True if successful
        """
        if not self.validate_input(resume_data):
            raise ValueError("Invalid resume data: missing required fields")
        
        builder = DocxBuilder(self.template_path)
        builder.build(resume_data)
        builder.save(output_path)
        
        return True

