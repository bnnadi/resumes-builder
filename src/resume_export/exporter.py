"""
Resume Exporter

Main exporter class that coordinates parsing, building, and validation.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import logging

from .parser import ResumeParser
from .docx_builder import DocxBuilder
from .validators.ats_checker import ATSValidator


logger = logging.getLogger(__name__)


class ResumeExporter:
    """Main resume exporter."""
    
    def __init__(self, template_path: Optional[Path] = None):
        """
        Initialize exporter.
        
        Args:
            template_path: Optional path to .docx template
        """
        self.template_path = template_path
        self.validator = ATSValidator()
    
    def export(
        self, 
        markdown_path: Path, 
        output_path: Path,
        validate: bool = False
    ) -> Dict[str, Any]:
        """
        Export markdown resume to .docx.
        
        Args:
            markdown_path: Path to markdown resume file
            output_path: Path for output .docx file
            validate: Whether to validate ATS compliance
        
        Returns:
            Dictionary with export results
        """
        results = {
            "success": False,
            "input_file": str(markdown_path),
            "output_file": str(output_path),
            "errors": [],
            "warnings": [],
            "validation": None
        }
        
        try:
            # Parse markdown
            logger.info(f"Parsing markdown resume: {markdown_path}")
            parser = ResumeParser(markdown_path)
            resume_data = parser.parse()
            logger.info("✅ Parsing complete")
            
            # Build DOCX
            logger.info("Building .docx file...")
            builder = DocxBuilder(self.template_path)
            document = builder.build(resume_data)
            
            # Save document
            builder.save(output_path)
            logger.info(f"✅ Created: {output_path}")
            
            results["success"] = True
            
            # Validate if requested
            if validate:
                logger.info("Validating ATS compliance...")
                is_valid, validation_results = self.validator.validate(output_path)
                
                results["validation"] = {
                    "is_valid": is_valid,
                    "results": validation_results
                }
                
                # Extract warnings and errors
                for vr in validation_results:
                    if not vr.passed:
                        if vr.severity == "critical":
                            results["errors"].append(vr.message)
                        else:
                            results["warnings"].append(vr.message)
                
                if is_valid:
                    logger.info("✅ ATS validation passed")
                else:
                    logger.warning("⚠️  ATS validation found issues")
            
        except FileNotFoundError as e:
            error_msg = f"File not found: {e}"
            logger.error(error_msg)
            results["errors"].append(error_msg)
        
        except Exception as e:
            error_msg = f"Export failed: {e}"
            logger.error(error_msg)
            results["errors"].append(error_msg)
        
        return results
    
    def export_multi_format(
        self,
        markdown_path: Path,
        output_dir: Path,
        formats: list = None
    ) -> Dict[str, Any]:
        """
        Export to multiple formats.
        
        Args:
            markdown_path: Path to markdown resume file
            output_dir: Output directory
            formats: List of formats (e.g., ['docx', 'pdf'])
        
        Returns:
            Dictionary with results for each format
        """
        if formats is None:
            formats = ['docx']
        
        results = {}
        
        # Get base filename
        base_name = markdown_path.stem
        
        for fmt in formats:
            if fmt == 'docx':
                output_path = output_dir / f"{base_name}.docx"
                results['docx'] = self.export(markdown_path, output_path)
            
            elif fmt == 'pdf':
                # PDF generation (requires docx first)
                docx_path = output_dir / f"{base_name}.docx"
                pdf_path = output_dir / f"{base_name}.pdf"
                
                # First create docx if not already done
                if 'docx' not in results:
                    results['docx'] = self.export(markdown_path, docx_path)
                
                # Then convert to PDF
                try:
                    self._convert_to_pdf(docx_path, pdf_path)
                    results['pdf'] = {
                        "success": True,
                        "output_file": str(pdf_path)
                    }
                except Exception as e:
                    results['pdf'] = {
                        "success": False,
                        "errors": [f"PDF conversion failed: {e}"]
                    }
        
        return results
    
    def _convert_to_pdf(self, docx_path: Path, pdf_path: Path):
        """
        Convert .docx to .pdf.
        
        Args:
            docx_path: Path to .docx file
            pdf_path: Path for output .pdf file
        """
        try:
            # Try using docx2pdf (if available)
            from docx2pdf import convert
            convert(str(docx_path), str(pdf_path))
            logger.info(f"✅ Created: {pdf_path}")
        
        except ImportError:
            # Fallback: Try LibreOffice command line
            import subprocess
            
            try:
                subprocess.run([
                    'soffice',
                    '--headless',
                    '--convert-to', 'pdf',
                    '--outdir', str(pdf_path.parent),
                    str(docx_path)
                ], check=True, capture_output=True)
                logger.info(f"✅ Created: {pdf_path}")
            
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.warning(
                    "⚠️  PDF conversion not available. "
                    "Install LibreOffice or python-docx2pdf for PDF support."
                )
                raise

