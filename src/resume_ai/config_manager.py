"""
Configuration Manager - Handles user and system configuration.
"""

import yaml
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class ResumeConfig:
    """User configuration for resume builder."""
    
    # Resume paths
    resume_primary_path: str = "~/Documents/resumes"
    resume_applications_path: str = "~/Documents/resumes/applications"
    resume_fallback_path: str = "~/Documents"
    base_resume_path: Optional[str] = None
    
    # Ollama configuration
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    ollama_temperature: float = 0.7
    ollama_timeout: int = 180
    
    # Threshold configuration
    threshold_minimum: int = 70
    threshold_borderline_min: int = 60
    threshold_borderline_max: int = 69
    threshold_auto_stop: bool = True
    threshold_ask_borderline: bool = True
    
    # Export configuration
    export_auto_validate: bool = True
    export_create_package: bool = True
    export_default_format: str = "docx"
    
    # Output configuration
    output_base_dir: str = "~/Documents/resumes/applications"
    output_create_subdirs: bool = True
    output_preserve_existing: bool = True
    
    # Skills inventory
    skills_inventory_path: Optional[str] = None
    
    # General
    verbose: bool = True


class ConfigManager:
    """Manages user configuration for resume builder."""
    
    # Config file locations (checked in order)
    USER_CONFIG_DIR = Path.home() / ".config" / "resume-builder"
    USER_CONFIG_FILE = USER_CONFIG_DIR / "config.yaml"
    PROJECT_CONFIG_FILE = Path(__file__).parent.parent.parent / "config" / "settings.yaml"
    
    def __init__(self):
        """Initialize config manager."""
        self.config = self.load_config()
    
    def load_config(self) -> ResumeConfig:
        """
        Load configuration from available sources.
        
        Priority:
        1. User config (~/.config/resume-builder/config.yaml)
        2. Project config (./config/settings.yaml)
        3. Built-in defaults
        
        Returns:
            ResumeConfig with merged settings
        """
        # Start with defaults
        config = ResumeConfig()
        
        # Try to load project config
        if self.PROJECT_CONFIG_FILE.exists():
            project_config = self._load_yaml_config(self.PROJECT_CONFIG_FILE)
            config = self._merge_config(config, project_config)
        
        # Try to load user config (overrides project config)
        if self.USER_CONFIG_FILE.exists():
            user_config = self._load_yaml_config(self.USER_CONFIG_FILE)
            config = self._merge_config(config, user_config)
        
        return config
    
    def _load_yaml_config(self, path: Path) -> Dict[str, Any]:
        """Load YAML config file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load config from {path}: {e}")
            return {}
    
    def _merge_config(self, config: ResumeConfig, yaml_data: Dict[str, Any]) -> ResumeConfig:
        """Merge YAML data into config object."""
        # Resume paths
        if 'resume_paths' in yaml_data:
            paths = yaml_data['resume_paths']
            if 'primary' in paths:
                config.resume_primary_path = paths['primary']
            if 'applications' in paths:
                config.resume_applications_path = paths['applications']
            if 'fallback' in paths:
                config.resume_fallback_path = paths['fallback']
            if 'base_resume' in paths:
                config.base_resume_path = paths['base_resume']
        
        # Ollama configuration
        if 'ollama' in yaml_data:
            ollama = yaml_data['ollama']
            if 'base_url' in ollama:
                config.ollama_url = ollama['base_url']
            if 'model' in ollama:
                config.ollama_model = ollama['model']
            if 'temperature' in ollama:
                config.ollama_temperature = ollama['temperature']
            if 'timeout' in ollama:
                config.ollama_timeout = ollama['timeout']
        
        # Threshold configuration
        if 'thresholds' in yaml_data:
            thresholds = yaml_data['thresholds']
            if 'minimum_overall' in thresholds:
                config.threshold_minimum = thresholds['minimum_overall']
            if 'borderline_min' in thresholds:
                config.threshold_borderline_min = thresholds['borderline_min']
            if 'borderline_max' in thresholds:
                config.threshold_borderline_max = thresholds['borderline_max']
            if 'auto_stop_below' in thresholds:
                config.threshold_auto_stop = thresholds['auto_stop_below']
            if 'ask_on_borderline' in thresholds:
                config.threshold_ask_borderline = thresholds['ask_on_borderline']
        
        # Export configuration
        if 'export' in yaml_data:
            export = yaml_data['export']
            if 'auto_validate' in export:
                config.export_auto_validate = export['auto_validate']
            if 'create_package' in export:
                config.export_create_package = export['create_package']
            if 'default_format' in export:
                config.export_default_format = export['default_format']
        
        # Output configuration
        if 'output' in yaml_data:
            output = yaml_data['output']
            if 'base_dir' in output:
                config.output_base_dir = output['base_dir']
            if 'create_subdirs' in output:
                config.output_create_subdirs = output['create_subdirs']
            if 'preserve_existing' in output:
                config.output_preserve_existing = output['preserve_existing']
        
        # Skills inventory
        if 'skills_inventory' in yaml_data:
            config.skills_inventory_path = yaml_data['skills_inventory']
        
        # General
        if 'verbose' in yaml_data:
            config.verbose = yaml_data['verbose']
        
        return config
    
    def save_user_config(self, config: Optional[ResumeConfig] = None) -> None:
        """
        Save configuration to user config file.
        
        Args:
            config: Config to save (uses current if None)
        """
        if config is None:
            config = self.config
        
        # Create config directory if it doesn't exist
        self.USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Convert config to YAML format
        yaml_data = {
            'resume_paths': {
                'primary': config.resume_primary_path,
                'applications': config.resume_applications_path,
                'fallback': config.resume_fallback_path,
            },
            'ollama': {
                'base_url': config.ollama_url,
                'model': config.ollama_model,
                'temperature': config.ollama_temperature,
                'timeout': config.ollama_timeout,
            },
            'thresholds': {
                'minimum_overall': config.threshold_minimum,
                'borderline_min': config.threshold_borderline_min,
                'borderline_max': config.threshold_borderline_max,
                'auto_stop_below': config.threshold_auto_stop,
                'ask_on_borderline': config.threshold_ask_borderline,
            },
            'export': {
                'auto_validate': config.export_auto_validate,
                'create_package': config.export_create_package,
                'default_format': config.export_default_format,
            },
            'output': {
                'base_dir': config.output_base_dir,
                'create_subdirs': config.output_create_subdirs,
                'preserve_existing': config.output_preserve_existing,
            },
            'verbose': config.verbose,
        }
        
        # Add optional fields
        if config.base_resume_path:
            yaml_data['resume_paths']['base_resume'] = config.base_resume_path
        
        if config.skills_inventory_path:
            yaml_data['skills_inventory'] = config.skills_inventory_path
        
        # Write to file
        with open(self.USER_CONFIG_FILE, 'w', encoding='utf-8') as f:
            yaml.safe_dump(yaml_data, f, default_flow_style=False, sort_keys=False)
    
    def set_value(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Config key (dot notation supported: 'resume_paths.primary')
            value: Value to set
        """
        # Map common keys
        key_map = {
            'resume-path': 'resume_primary_path',
            'base-resume': 'base_resume_path',
            'output-dir': 'output_base_dir',
            'model': 'ollama_model',
            'min-score': 'threshold_minimum',
        }
        
        attr_name = key_map.get(key, key)
        
        if hasattr(self.config, attr_name):
            # Expand paths
            if 'path' in attr_name or 'dir' in attr_name:
                value = str(Path(value).expanduser())
            
            setattr(self.config, attr_name, value)
            self.save_user_config()
        else:
            raise ValueError(f"Unknown configuration key: {key}")
    
    def get_value(self, key: str) -> Any:
        """Get a configuration value."""
        key_map = {
            'resume-path': 'resume_primary_path',
            'base-resume': 'base_resume_path',
            'output-dir': 'output_base_dir',
            'model': 'ollama_model',
            'min-score': 'threshold_minimum',
        }
        
        attr_name = key_map.get(key, key)
        return getattr(self.config, attr_name, None)
    
    def get_resume_search_paths(self) -> list[Path]:
        """Get list of paths to search for resumes."""
        paths = []
        
        for path_str in [
            self.config.resume_primary_path,
            self.config.resume_applications_path,
            self.config.resume_fallback_path,
        ]:
            path = Path(path_str).expanduser()
            if path.exists():
                paths.append(path)
        
        # Always include current directory as fallback
        paths.append(Path.cwd())
        
        return paths
    
    def get_base_resume_path(self) -> Optional[Path]:
        """Get configured base resume path if set."""
        if self.config.base_resume_path:
            path = Path(self.config.base_resume_path).expanduser()
            if path.exists():
                return path
        return None
    
    def get_output_directory(self) -> Path:
        """Get output directory for applications."""
        return Path(self.config.output_base_dir).expanduser()
    
    def validate_paths(self) -> Dict[str, bool]:
        """
        Validate configured paths exist.
        
        Returns:
            Dictionary of path names and validation status
        """
        validation = {}
        
        paths_to_check = {
            'resume_primary': self.config.resume_primary_path,
            'resume_applications': self.config.resume_applications_path,
            'output_dir': self.config.output_base_dir,
        }
        
        if self.config.base_resume_path:
            paths_to_check['base_resume'] = self.config.base_resume_path
        
        if self.config.skills_inventory_path:
            paths_to_check['skills_inventory'] = self.config.skills_inventory_path
        
        for name, path_str in paths_to_check.items():
            path = Path(path_str).expanduser()
            validation[name] = path.exists()
        
        return validation
    
    def is_first_run(self) -> bool:
        """Check if this is the first run (no user config exists)."""
        return not self.USER_CONFIG_FILE.exists()
    
    def get_config_location(self) -> Path:
        """Get path to user config file."""
        return self.USER_CONFIG_FILE
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return asdict(self.config)


# Global config instance
_config_manager = None


def get_config() -> ConfigManager:
    """Get global config manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

