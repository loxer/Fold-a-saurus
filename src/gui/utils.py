import os
import json
from typing import Dict


def save_config(config_dict: dict, config_file: str) -> dict:
    """Saves the current GUI configuration to a config file."""
    # Ensure the directory exists
    config_dir = os.path.dirname(config_file)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    try:
        with open(config_file, 'w') as f:
            json.dump(config_dict, f, indent=4)
            f.flush()  # Ensure data is written to disk
            return config_dict
    except IOError as e:
        print(f"Failed to save configuration: {e}")


def load_config(default_file: str, config_file: str) -> Dict[str, Dict[str, int]]:
    """Loads GUI configuration from a config file and ensures all parameters are present."""

    # Load default configuration
    with open(default_file, 'r') as f:
        default_config = json.load(f)
    
    # Load configuration from file if it exists
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            loaded_config = json.load(f)
    else:
        loaded_config = {}

    # Ensure all parameters are present
    def update_config(default: Dict, loaded: Dict) -> Dict:
        for key, value in default.items():
            if isinstance(value, dict):
                loaded[key] = update_config(value, loaded.get(key, {}))
            else:
                loaded[key] = loaded.get(key, value)
        return loaded

    # Update the loaded configuration with missing parameters
    final_config = update_config(default_config, loaded_config)
    
    return final_config