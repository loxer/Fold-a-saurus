import os
import json
from typing import Dict

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'configs', 'profile1', 'gui.json')
DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'configs', 'defaults', 'default_gui.json')


class ThemeManager:
    def __init__(self):
        self.gui_config = self.load_gui_config()


    def apply_theme(self, app, theme_name: str) -> None:
        """Applies the specified theme to the GUI."""
        theme = self.gui_config['theme'][theme_name]
        
        app.configure(bg=theme['bg'])
        app.top_frame.configure(bg=theme['bg'])
        app.search_button.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])
        app.delete_button.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])
        app.dark_mode_button.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])

        app.left_frame.configure(bg=theme['bg'])
        app.middle_frame.configure(bg=theme['bg'])
        app.right_frame.configure(bg=theme['bg'])
        
        app.left_listbox.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])
        app.right_listbox.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])
        app.result_listbox.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])


    def toggle_dark_mode(self, app) -> None:
        """Toggles between dark and light modes and saves the current mode."""
        current_mode = self.gui_config['theme']['mode']
        new_mode = 'dark' if current_mode == 'light' else 'light'
        self.gui_config['theme']['mode'] = new_mode
        self.save_gui_config()
        self.apply_theme(app, new_mode)
        app.dark_mode_button.config(text="Switch to Light Mode" if new_mode == 'dark' else "Switch to Dark Mode")


    def save_gui_config(self) -> None:
        """Saves the current GUI configuration to a config file."""
        config_dir = os.path.dirname(CONFIG_FILE)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.gui_config, f, indent=4)
                f.flush()  # Ensure data is written to disk
        except IOError as e:
            print(f"Failed to save configuration: {e}")

    def load_gui_config(self) -> Dict[str, Dict[str, int]]:
        """Loads GUI configuration from a config file and ensures all parameters are present."""
        with open(DEFAULT_CONFIG_FILE, 'r') as f:
            default_config = json.load(f)

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                loaded_config = json.load(f)
        else:
            loaded_config = {}

        def update_config(default, loaded):
            for key, value in default.items():
                if isinstance(value, dict):
                    loaded[key] = update_config(value, loaded.get(key, {}))
                else:
                    loaded[key] = loaded.get(key, value)
            return loaded

        return update_config(default_config, loaded_config)