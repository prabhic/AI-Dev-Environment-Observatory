"""
Configuration Loader

Loads and validates steering configuration.
"""

import yaml
from pathlib import Path
from typing import Dict


def load_config(config_path: str = "steering/config.yaml") -> Dict:
    """
    Load configuration from YAML file

    Returns validated configuration dictionary
    """
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    # Validate required sections
    required_sections = ["analysis", "registry", "intelligence", "storage", "web"]
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required config section: {section}")

    return config


def get_growth_status(config: Dict) -> Dict:
    """
    Check which growth features are enabled

    Returns dictionary of feature statuses
    """
    return {
        "auto_discovery": config.get("experimental", {}).get("auto_discovery", False),
        "monitoring": config.get("monitoring", {}).get("enabled", False),
        "ml_patterns": config.get("experimental", {}).get("ml_pattern_detection", False),
        "webhooks": config.get("experimental", {}).get("github_webhooks", False),
        "community": config.get("experimental", {}).get("community_contributions", False)
    }
