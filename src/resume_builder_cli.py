#!/usr/bin/env python3
"""
Resume Builder - Unified CLI with AI-powered features.

Combines AI-powered resume analysis, customization, and traditional export.
"""

import argparse
import sys
from pathlib import Path

# Version
__version__ = "0.4.0"


def create_parser() -> argparse.ArgumentParser:
    """Create main argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog='resume-builder',
        description='AI-powered resume builder with ATS-optimized export',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Complete workflow (recommended)
  resume-builder workflow job-posting.txt
  
  # Individual commands
  resume-builder job-match job-posting.txt
  resume-builder customize job-posting.txt --company Google
  resume-builder export resume.md --package
  
  # Evaluate existing resumes
  resume-builder eval
  
For more information, visit: https://github.com/bisikennadi/resumes-builder
        """
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    # Create subparsers
    subparsers = parser.add_subparsers(
        title='commands',
        dest='command',
        help='Available commands'
    )
    
    # Workflow command (recommended)
    add_workflow_parser(subparsers)
    
    # Individual AI commands
    add_job_match_parser(subparsers)
    add_eval_parser(subparsers)
    add_customize_parser(subparsers)
    
    # Export command
    add_export_parser(subparsers)
    
    # Configuration commands
    add_setup_parser(subparsers)
    add_config_parser(subparsers)
    
    return parser


def add_workflow_parser(subparsers):
    """Add workflow command (complete end-to-end)."""
    parser = subparsers.add_parser(
        'workflow',
        aliases=['process'],
        help='Complete workflow: match → customize → export',
        description='Run complete workflow with threshold gating at 70%'
    )
    
    parser.add_argument(
        'job_posting',
        type=Path,
        help='Path to job posting file (.txt or .md)'
    )
    
    parser.add_argument(
        '--base-resume',
        type=Path,
        help='Base resume to customize (auto-detect if not provided)'
    )
    
    parser.add_argument(
        '--company',
        help='Company name (auto-extract if not provided)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory (auto-create if not provided)'
    )
    
    parser.add_argument(
        '--min-score',
        type=int,
        default=70,
        help='Minimum match score to continue (default: 70)'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Skip threshold check and continue regardless of score'
    )
    
    parser.add_argument(
        '--no-export',
        action='store_true',
        help='Stop after customization, skip export to .docx'
    )
    
    parser.add_argument(
        '--model',
        default='llama3.1',
        help='Ollama model to use (default: llama3.1)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output'
    )
    
    parser.set_defaults(func=workflow_command)


def add_job_match_parser(subparsers):
    """Add job-match command."""
    parser = subparsers.add_parser(
        'job-match',
        aliases=['match'],
        help='Analyze how well resume matches job description',
        description='Score resume fit and predict interview probability'
    )
    
    parser.add_argument(
        'job_posting',
        type=Path,
        help='Path to job posting file'
    )
    
    parser.add_argument(
        '--resume',
        type=Path,
        help='Resume to analyze (auto-detect if not provided)'
    )
    
    parser.add_argument(
        '--model',
        default='llama3.1',
        help='Ollama model to use (default: llama3.1)'
    )
    
    parser.add_argument(
        '--save',
        type=Path,
        help='Save analysis to file'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output'
    )
    
    parser.set_defaults(func=job_match_command)


def add_eval_parser(subparsers):
    """Add resume-eval command."""
    parser = subparsers.add_parser(
        'resume-eval',
        aliases=['eval'],
        help='Evaluate and compare multiple resumes',
        description='Analyze resumes and generate master resume'
    )
    
    parser.add_argument(
        '--search',
        type=Path,
        help='Directory to search for resumes'
    )
    
    parser.add_argument(
        '--resume-text',
        help='Paste resume text directly'
    )
    
    parser.add_argument(
        '--model',
        default='llama3.1',
        help='Ollama model to use (default: llama3.1)'
    )
    
    parser.add_argument(
        '--save',
        type=Path,
        help='Save evaluation to file'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output'
    )
    
    parser.set_defaults(func=eval_command)


def add_customize_parser(subparsers):
    """Add resume-customize command."""
    parser = subparsers.add_parser(
        'resume-customize',
        aliases=['customize'],
        help='Customize resume for specific job',
        description='AI-powered resume customization with keyword optimization'
    )
    
    parser.add_argument(
        'job_posting',
        type=Path,
        help='Path to job posting file'
    )
    
    parser.add_argument(
        '--base-resume',
        type=Path,
        help='Base resume to customize (auto-detect if not provided)'
    )
    
    parser.add_argument(
        '--company',
        help='Company name (auto-extract if not provided)'
    )
    
    parser.add_argument(
        '--role',
        help='Role title (auto-extract if not provided)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory (auto-create if not provided)'
    )
    
    parser.add_argument(
        '--model',
        default='llama3.1',
        help='Ollama model to use (default: llama3.1)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output'
    )
    
    parser.set_defaults(func=customize_command)


def add_export_parser(subparsers):
    """Add export command (existing functionality)."""
    parser = subparsers.add_parser(
        'export',
        help='Export markdown resume to .docx (traditional formatting)',
        description='Convert markdown to ATS-optimized .docx without AI'
    )
    
    parser.add_argument(
        'input',
        type=Path,
        help='Input markdown resume file'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output directory (default: same as input)'
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
        '--formats',
        nargs='+',
        choices=['docx', 'pdf'],
        default=['docx'],
        help='Export formats (default: docx)'
    )
    
    parser.set_defaults(func=export_command)


# Command implementations
def workflow_command(args):
    """Execute complete workflow."""
    from resume_ai import OllamaConfig
    from resume_ai.workflow import ResumeWorkflow
    from resume_ai.threshold_gate import ThresholdConfig
    
    try:
        # Configure
        ollama_config = OllamaConfig(model=args.model)
        threshold_config = ThresholdConfig(minimum_overall=args.min_score)
        
        # Initialize workflow
        workflow = ResumeWorkflow(
            ollama_config=ollama_config,
            threshold_config=threshold_config
        )
        
        # Execute
        result = workflow.process(
            job_posting_path=args.job_posting,
            base_resume_path=args.base_resume,
            company_name=args.company,
            output_dir=args.output_dir,
            force=args.force,
            skip_export=args.no_export,
            verbose=not args.quiet
        )
        
        if result.status == "completed":
            sys.exit(0)
        else:
            print(f"\n⏹️  Workflow stopped: {result.status}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def job_match_command(args):
    """Execute job-match command."""
    from resume_ai import OllamaClient, OllamaConfig
    from resume_ai.job_match import JobMatcher
    
    try:
        # Configure
        ollama_config = OllamaConfig(model=args.model)
        ollama = OllamaClient(ollama_config)
        matcher = JobMatcher(ollama)
        
        # Read job posting
        job_text = args.job_posting.read_text()
        
        # Execute
        result = matcher.match(
            job_description=job_text,
            resume_path=args.resume,
            verbose=not args.quiet
        )
        
        # Print results
        if not args.quiet:
            print("\n" + "=" * 70)
            print("JOB MATCH ANALYSIS")
            print("=" * 70)
            print(result.raw_output)
        
        # Save if requested
        if args.save:
            args.save.write_text(result.raw_output)
            print(f"\n💾 Analysis saved to: {args.save}")
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def eval_command(args):
    """Execute resume-eval command."""
    from resume_ai import OllamaClient, OllamaConfig
    from resume_ai.resume_eval import ResumeEvaluator
    
    try:
        # Configure
        ollama_config = OllamaConfig(model=args.model)
        ollama = OllamaClient(ollama_config)
        evaluator = ResumeEvaluator(ollama)
        
        # Execute
        result = evaluator.evaluate(
            resume_text=args.resume_text,
            search_scope=args.search,
            verbose=not args.quiet
        )
        
        # Print results
        if not args.quiet:
            print("\n" + "=" * 70)
            print("RESUME EVALUATION")
            print("=" * 70)
            print(result.raw_output)
        
        # Save if requested
        if args.save:
            args.save.write_text(result.raw_output)
            print(f"\n💾 Evaluation saved to: {args.save}")
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def customize_command(args):
    """Execute resume-customize command."""
    from resume_ai import OllamaClient, OllamaConfig
    from resume_ai.resume_customize import ResumeCustomizer
    
    try:
        # Configure
        ollama_config = OllamaConfig(model=args.model)
        ollama = OllamaClient(ollama_config)
        customizer = ResumeCustomizer(ollama)
        
        # Read job posting
        job_text = args.job_posting.read_text()
        
        # Execute
        result = customizer.customize(
            job_description=job_text,
            base_resume_path=args.base_resume,
            company_name=args.company,
            output_dir=args.output_dir,
            verbose=not args.quiet
        )
        
        print(f"\n✅ Customization complete!")
        print(f"📁 Files saved to: {result.output_directory}")
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def export_command(args):
    """Execute export command."""
    from resume_export.exporter import ResumeExporter
    from resume_export.package_builder import PackageBuilder
    
    try:
        exporter = ResumeExporter()
        
        result = exporter.export(
            str(args.input),
            formats=args.formats,
            output_dir=str(args.output) if args.output else None,
            validate=args.validate
        )
        
        print(f"\n✅ Export complete!")
        for format, path in result.output_files.items():
            print(f"   {format.upper()}: {path}")
        
        if args.package:
            builder = PackageBuilder()
            package_dir = builder.build_package(
                str(args.input.parent)
            )
            print(f"📦 Package: {package_dir}")
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def add_setup_parser(subparsers):
    """Add setup command for initial configuration."""
    parser = subparsers.add_parser(
        'setup',
        help='Interactive setup wizard',
        description='Configure resume builder for first-time use'
    )
    
    parser.add_argument(
        '--non-interactive',
        action='store_true',
        help='Use defaults without prompts'
    )
    
    parser.set_defaults(func=setup_command)


def add_config_parser(subparsers):
    """Add config command for managing configuration."""
    parser = subparsers.add_parser(
        'config',
        help='Manage configuration',
        description='View and modify resume builder configuration'
    )
    
    subparsers_config = parser.add_subparsers(
        dest='config_action',
        help='Config action'
    )
    
    # config list
    list_parser = subparsers_config.add_parser(
        'list',
        aliases=['show'],
        help='Show all configuration values'
    )
    list_parser.set_defaults(func=config_list_command)
    
    # config set
    set_parser = subparsers_config.add_parser(
        'set',
        help='Set a configuration value'
    )
    set_parser.add_argument('key', help='Configuration key')
    set_parser.add_argument('value', help='Value to set')
    set_parser.set_defaults(func=config_set_command)
    
    # config get
    get_parser = subparsers_config.add_parser(
        'get',
        help='Get a configuration value'
    )
    get_parser.add_argument('key', help='Configuration key')
    get_parser.set_defaults(func=config_get_command)
    
    # config validate
    validate_parser = subparsers_config.add_parser(
        'validate',
        help='Validate configured paths'
    )
    validate_parser.set_defaults(func=config_validate_command)
    
    # config path
    path_parser = subparsers_config.add_parser(
        'path',
        help='Show config file location'
    )
    path_parser.set_defaults(func=config_path_command)
    
    parser.set_defaults(func=lambda args: parser.print_help())


def setup_command(args):
    """Run interactive setup wizard."""
    from resume_ai.config_manager import ConfigManager, ResumeConfig
    
    print("\n" + "=" * 70)
    print("  Resume Builder Setup")
    print("=" * 70)
    
    config_manager = ConfigManager()
    
    if not args.non_interactive:
        print("\nLet's configure your resume builder!\n")
        
        # Get resume directory
        default_resume_path = config_manager.config.resume_primary_path
        resume_path = input(f"Where do you keep your resumes? [{default_resume_path}]: ").strip()
        if not resume_path:
            resume_path = default_resume_path
        
        # Expand path
        resume_path = str(Path(resume_path).expanduser())
        
        # Get output directory
        default_output = config_manager.config.output_base_dir
        output_path = input(f"Where should customized resumes go? [{default_output}]: ").strip()
        if not output_path:
            output_path = default_output
        output_path = str(Path(output_path).expanduser())
        
        # Find base resume
        print("\nSearching for base/master resume...")
        resume_dir = Path(resume_path).expanduser()
        
        master_resumes = []
        if resume_dir.exists():
            master_resumes = list(resume_dir.glob("*master*.md")) + list(resume_dir.glob("*Master*.md"))
        
        base_resume_path = None
        if master_resumes:
            print(f"\nFound {len(master_resumes)} master resume(s):")
            for i, resume in enumerate(master_resumes, 1):
                print(f"  {i}. {resume.name}")
            
            choice = input(f"\nSelect base resume [1-{len(master_resumes)}] or enter path: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(master_resumes):
                base_resume_path = str(master_resumes[int(choice) - 1])
            elif choice:
                base_resume_path = str(Path(choice).expanduser())
        else:
            print("  No master resume found.")
            base_resume = input("Enter path to your base resume (or leave blank): ").strip()
            if base_resume:
                base_resume_path = str(Path(base_resume).expanduser())
        
        # Update config
        config_manager.config.resume_primary_path = resume_path
        config_manager.config.output_base_dir = output_path
        if base_resume_path:
            config_manager.config.base_resume_path = base_resume_path
        
        # Check skills inventory
        skills_file = Path(__file__).parent.parent / "config" / "skills_inventory.yaml"
        if skills_file.exists():
            print(f"\n✓ Skills inventory found: {skills_file}")
        else:
            print(f"\n⚠️  Skills inventory not found. You can create one later with resume-skills")
        
        # Save configuration
        config_manager.save_user_config()
        
        print("\n" + "=" * 70)
        print("  Configuration Saved!")
        print("=" * 70)
        print(f"\nConfig location: {config_manager.get_config_location()}")
        print(f"Resume path: {resume_path}")
        print(f"Output path: {output_path}")
        if base_resume_path:
            print(f"Base resume: {base_resume_path}")
        
        print("\n✅ Setup complete!")
        print("\nNext steps:")
        print("  1. Make sure Ollama is running: ollama serve")
        print("  2. Test with: resume-builder workflow job-posting.txt")
        print("  3. Manage skills: resume-skills list")
    else:
        # Non-interactive: save defaults
        config_manager.save_user_config()
        print(f"✓ Configuration saved to: {config_manager.get_config_location()}")
    
    sys.exit(0)


def config_list_command(args):
    """List all configuration values."""
    from resume_ai.config_manager import get_config
    
    config = get_config()
    
    print("\n" + "=" * 70)
    print("  Resume Builder Configuration")
    print("=" * 70)
    
    print("\n📁 Resume Paths:")
    print(f"  Primary:      {config.config.resume_primary_path}")
    print(f"  Applications: {config.config.resume_applications_path}")
    print(f"  Fallback:     {config.config.resume_fallback_path}")
    if config.config.base_resume_path:
        print(f"  Base Resume:  {config.config.base_resume_path}")
    
    print("\n🤖 Ollama Configuration:")
    print(f"  URL:         {config.config.ollama_url}")
    print(f"  Model:       {config.config.ollama_model}")
    print(f"  Temperature: {config.config.ollama_temperature}")
    
    print("\n📊 Thresholds:")
    print(f"  Minimum:     {config.config.threshold_minimum}")
    print(f"  Borderline:  {config.config.threshold_borderline_min}-{config.config.threshold_borderline_max}")
    
    print("\n📤 Output:")
    print(f"  Directory:   {config.config.output_base_dir}")
    
    print(f"\n📝 Config File: {config.get_config_location()}")
    print()
    
    sys.exit(0)


def config_set_command(args):
    """Set a configuration value."""
    from resume_ai.config_manager import get_config
    
    try:
        config = get_config()
        config.set_value(args.key, args.value)
        print(f"✓ Set {args.key} = {args.value}")
        print(f"  Saved to: {config.get_config_location()}")
        sys.exit(0)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def config_get_command(args):
    """Get a configuration value."""
    from resume_ai.config_manager import get_config
    
    config = get_config()
    value = config.get_value(args.key)
    
    if value is not None:
        print(value)
        sys.exit(0)
    else:
        print(f"❌ Unknown configuration key: {args.key}")
        sys.exit(1)


def config_validate_command(args):
    """Validate configured paths."""
    from resume_ai.config_manager import get_config
    
    config = get_config()
    validation = config.validate_paths()
    
    print("\n" + "=" * 70)
    print("  Path Validation")
    print("=" * 70 + "\n")
    
    all_valid = True
    for name, is_valid in validation.items():
        status = "✓" if is_valid else "✗"
        print(f"{status} {name:20} ", end="")
        
        # Get the actual path
        if 'resume_primary' in name:
            path = config.config.resume_primary_path
        elif 'resume_applications' in name:
            path = config.config.resume_applications_path
        elif 'output_dir' in name:
            path = config.config.output_base_dir
        elif 'base_resume' in name:
            path = config.config.base_resume_path
        elif 'skills_inventory' in name:
            path = config.config.skills_inventory_path
        else:
            path = ""
        
        print(f"{path}")
        
        if not is_valid:
            all_valid = False
    
    print()
    
    if all_valid:
        print("✅ All paths valid!")
        sys.exit(0)
    else:
        print("⚠️  Some paths are invalid. Run 'resume-builder setup' to reconfigure.")
        sys.exit(1)


def config_path_command(args):
    """Show config file location."""
    from resume_ai.config_manager import get_config
    
    config = get_config()
    config_path = config.get_config_location()
    
    print(config_path)
    
    if config_path.exists():
        print(f"\n✓ Config file exists ({config_path.stat().st_size} bytes)")
    else:
        print(f"\n⚠️  Config file doesn't exist yet. Run 'resume-builder setup' to create it.")
    
    sys.exit(0)


def main():
    """Main entry point."""
    from resume_ai.config_manager import get_config
    
    parser = create_parser()
    args = parser.parse_args()
    
    # Check for first run (except for setup and config commands)
    if hasattr(args, 'func') and args.func != setup_command and not (hasattr(args, 'config_action')):
        config = get_config()
        if config.is_first_run():
            print("\n⚠️  First time setup required!")
            print("Run: resume-builder setup\n")
            sys.exit(1)
    
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()

