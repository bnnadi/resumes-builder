#!/usr/bin/env python3
"""
ATS Resume Export System - Command Line Interface

Main CLI entry point for the resume export application.
"""

import argparse
import sys
import logging
from pathlib import Path
from typing import Optional

from . import __version__
from .exporter import ResumeExporter
from .package_builder import PackageBuilder
from .validators.ats_checker import ATSValidator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


class ResumeCLI:
    """Command-line interface for resume export application."""
    
    def __init__(self):
        """Initialize CLI."""
        self.parser = self._create_parser()
        self.exporter = None
        self.validator = None
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            prog='export-resume',
            description='Export markdown resumes to ATS-optimized .docx files',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Simple export
  export-resume resume.md
  
  # With validation
  export-resume resume.md --validate
  
  # Create complete package
  export-resume resume.md --package
  
  # Multi-format export
  export-resume resume.md --formats docx pdf
  
  # Batch export
  export-resume --batch applications/
  
  # Validate existing file
  export-resume --validate-only resume.docx

For more information, visit: https://github.com/bisikennadi/resumes-builder
            """
        )
        
        parser.add_argument('input', nargs='?', help='Input markdown resume file')
        
        parser.add_argument(
            '-o', '--output',
            help='Output directory (default: same as input)'
        )
        
        parser.add_argument(
            '-f', '--formats',
            nargs='+',
            choices=['docx', 'pdf', 'html', 'txt'],
            default=['docx'],
            help='Export formats (default: docx)'
        )
        
        parser.add_argument(
            '--validate',
            action='store_true',
            help='Validate ATS compliance after export'
        )
        
        parser.add_argument(
            '--package',
            action='store_true',
            help='Create complete application package'
        )
        
        parser.add_argument(
            '--template',
            type=Path,
            help='Custom .docx template file'
        )
        
        parser.add_argument(
            '--validate-only',
            type=Path,
            metavar='FILE',
            help='Only validate existing .docx file'
        )
        
        parser.add_argument(
            '--batch',
            type=Path,
            metavar='DIR',
            help='Batch process all resumes in directory'
        )
        
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Verbose output'
        )
        
        parser.add_argument(
            '--version',
            action='version',
            version=f'ats-resume-export {__version__}'
        )
        
        return parser
    
    def setup_logging(self, verbose: bool = False):
        """Configure logging level."""
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
    
    def export_resume(self, args) -> int:
        """Export markdown resume to .docx."""
        input_path = Path(args.input)
        
        # Validate input file
        if not input_path.exists():
            logger.error(f"❌ Error: Input file not found: {input_path}")
            return 1
        
        if input_path.suffix != '.md':
            logger.error(f"❌ Error: Input file must be a markdown (.md) file")
            return 1
        
        # Determine output directory
        if args.output:
            output_dir = Path(args.output)
        else:
            output_dir = input_path.parent
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize exporter
        self.exporter = ResumeExporter(template_path=args.template)
        
        logger.info(f"\n📝 Exporting resume: {input_path.name}")
        logger.info("="*70)
        
        # Export requested formats
        formats = args.formats if args.formats else ['docx']
        results = self.exporter.export_multi_format(input_path, output_dir, formats)
        
        # Display results
        all_success = True
        for fmt, result in results.items():
            if result.get('success'):
                output_file = result.get('output_file')
                logger.info(f"\n✅ {fmt.upper()} created: {Path(output_file).name}")
            else:
                all_success = False
                logger.error(f"\n❌ {fmt.upper()} export failed:")
                for error in result.get('errors', []):
                    logger.error(f"   {error}")
        
        # Validate if requested
        if args.validate and 'docx' in results and results['docx'].get('success'):
            logger.info("\n🔍 Validating ATS compliance...")
            logger.info("-"*70)
            
            docx_path = Path(results['docx']['output_file'])
            self.validator = ATSValidator()
            is_valid, validation_results = self.validator.validate(docx_path)
            
            # Display validation report
            report = self.validator.generate_report(validation_results)
            logger.info(report)
            
            if not is_valid:
                all_success = False
        
        # Create package if requested
        if args.package:
            logger.info("\n📦 Building application package...")
            logger.info("-"*70)
            
            builder = PackageBuilder()
            package_files = builder.create_package(output_dir)
            
            logger.info(f"\n✅ Application package complete!")
            logger.info(f"\n📁 Package contents ({len(package_files)} files):")
            
            # Group files by type
            resume_files = [f for f in package_files if f.endswith(('.docx', '.pdf'))]
            guide_files = [f for f in package_files if f in ['00_START_HERE.md', 'README.md']]
            support_files = [f for f in package_files if f.endswith('.md') and f not in guide_files]
            
            if resume_files:
                logger.info("\n  📄 Submission Files:")
                for f in resume_files:
                    logger.info(f"     - {f} {'[SUBMIT THIS]' if f.endswith('.docx') else ''}")
            
            if guide_files:
                logger.info("\n  📋 Quick Start:")
                for f in guide_files:
                    logger.info(f"     - {f}")
            
            if support_files:
                logger.info("\n  📚 Preparation Materials:")
                for f in support_files:
                    logger.info(f"     - {f}")
        
        # Final summary
        logger.info("\n" + "="*70)
        if all_success:
            logger.info("🎉 Export complete!")
            logger.info(f"📍 Location: {output_dir}")
            
            if args.package:
                logger.info(f"\n👉 Next: Review 00_START_HERE.md in {output_dir}")
        else:
            logger.error("⚠️  Export completed with errors. Please review messages above.")
        
        logger.info("="*70 + "\n")
        
        return 0 if all_success else 1
    
    def validate_only(self, args) -> int:
        """Validate existing .docx file."""
        docx_path = Path(args.validate_only)
        
        if not docx_path.exists():
            logger.error(f"❌ Error: File not found: {docx_path}")
            return 1
        
        logger.info(f"\n🔍 Validating: {docx_path.name}")
        logger.info("="*70)
        
        self.validator = ATSValidator()
        is_valid, results = self.validator.validate(docx_path)
        
        report = self.validator.generate_report(results)
        logger.info(report)
        
        return 0 if is_valid else 1
    
    def batch_export(self, args) -> int:
        """Batch export all resumes in directory."""
        batch_dir = Path(args.batch)
        
        if not batch_dir.exists() or not batch_dir.is_dir():
            logger.error(f"❌ Error: Directory not found: {batch_dir}")
            return 1
        
        # Find all markdown files
        markdown_files = list(batch_dir.rglob("*.md"))
        resume_files = [f for f in markdown_files if 'Resume' in f.name or 'resume' in f.name]
        
        if not resume_files:
            logger.error(f"❌ Error: No resume markdown files found in {batch_dir}")
            return 1
        
        logger.info(f"\n📦 Batch Export")
        logger.info("="*70)
        logger.info(f"Found {len(resume_files)} resume file(s)\n")
        
        self.exporter = ResumeExporter()
        results = []
        
        for resume_file in resume_files:
            logger.info(f"\n📝 Exporting: {resume_file.name}")
            logger.info("-"*70)
            
            output_path = resume_file.parent / f"{resume_file.stem}.docx"
            result = self.exporter.export(resume_file, output_path, validate=args.validate)
            
            if result['success']:
                logger.info(f"✅ Success: {output_path.name}")
            else:
                logger.error(f"❌ Failed: {resume_file.name}")
                for error in result.get('errors', []):
                    logger.error(f"   {error}")
            
            results.append(result)
        
        # Summary
        success_count = sum(1 for r in results if r['success'])
        logger.info("\n" + "="*70)
        logger.info(f"✅ Completed: {success_count}/{len(results)} successful")
        logger.info("="*70 + "\n")
        
        return 0 if success_count == len(results) else 1
    
    def run(self, argv: Optional[list] = None) -> int:
        """
        Run the CLI application.
        
        Args:
            argv: Command line arguments (defaults to sys.argv[1:])
        
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        args = self.parser.parse_args(argv)
        
        # Setup logging
        self.setup_logging(args.verbose)
        
        # Determine mode and execute
        try:
            if args.validate_only:
                return self.validate_only(args)
            
            elif args.batch:
                return self.batch_export(args)
            
            elif args.input:
                return self.export_resume(args)
            
            else:
                self.parser.print_help()
                return 0
        
        except KeyboardInterrupt:
            logger.info("\n\n⚠️  Operation cancelled by user")
            return 130
        
        except Exception as e:
            logger.error(f"\n❌ Unexpected error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1


def main(argv: Optional[list] = None) -> int:
    """
    Main entry point for the CLI application.
    
    Args:
        argv: Command line arguments (defaults to sys.argv[1:])
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    cli = ResumeCLI()
    return cli.run(argv)


if __name__ == '__main__':
    sys.exit(main())

