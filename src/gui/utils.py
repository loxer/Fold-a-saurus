import os
import json
import tkinter as tk
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

    # Try to load configuration from the file if it exists
    loaded_config = {}
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                # Check if the file is not empty before loading
                content = f.read().strip()
                if content:
                    loaded_config = json.loads(content)
                else:
                    print("Configuration file is empty, loading defaults.")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading configuration file: {e}. Using defaults.")

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


def save_listbox_states(config_file: str, left_listbox: tk.Listbox, right_listbox: tk.Listbox, result_listbox: tk.Listbox) -> None:
        """Saves the current state of all listboxes to a JSON file."""
        state = {
            "left_listbox": [left_listbox.get(i) for i in range(left_listbox.size())],
            "right_listbox": [right_listbox.get(i) for i in range(right_listbox.size())],
            "result_listbox": [result_listbox.get(i) for i in range(result_listbox.size())]
        }
        save_config(state, config_file)


def load_listbox_states(config_file: str, left_listbox: tk.Listbox, right_listbox: tk.Listbox, result_listbox: tk.Listbox) -> None:
    """Loads the state of the listboxes from a JSON file."""
    try:
        with open(config_file, 'r') as f:
            state = json.load(f)

        left_items = state.get("left_listbox", [])
        right_items = state.get("right_listbox", [])
        result_items = state.get("result_listbox", [])

        # Populate left listbox
        for item in left_items:
            left_listbox.insert(tk.END, item)

        # Populate right listbox
        for item in right_items:
            right_listbox.insert(tk.END, item)

        # Populate result listbox
        for item in result_items:
            result_listbox.insert(tk.END, item)

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading listbox states: {e}")
