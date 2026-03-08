# core/config_manager.py
import json
import yaml
from typing import Any, Dict
from pathlib import Path

class ConfigManager:
    """Advanced configuration management with profiles"""
    
    def __init__(self, config_dir="~/.payload-generator"):
        self.config_dir = Path(config_dir).expanduser()
        self.config_dir.mkdir(exist_ok=True)
        self.profiles_dir = self.config_dir / "profiles"
        self.profiles_dir.mkdir(exist_ok=True)
        self.current_config = self.load_default()
    
    def create_profile(self, name: str, config: Dict[str, Any]):
        """Save configuration profile"""
        profile_path = self.profiles_dir / f"{name}.yaml"
        with open(profile_path, 'w') as f:
            yaml.dump(config, f)
    
    def load_profile(self, name: str) -> Dict[str, Any]:
        """Load configuration profile"""
        profile_path = self.profiles_dir / f"{name}.yaml"
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                return yaml.safe_load(f)
        return self.load_default()
    
    def merge_configs(self, *configs: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge multiple configurations"""
        merged = {}
        for config in configs:
            merged = self._deep_merge(merged, config)
        return merged
