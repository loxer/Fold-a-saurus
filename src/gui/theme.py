import os
import json
from typing import Dict
from gui.utils import save_config, load_config

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'configs', 'profile1', 'gui.json')
DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'configs', 'defaults', 'default_gui.json')


class ThemeManager:
    def __init__(self):
        self.theme_config = load_config(DEFAULT_CONFIG_FILE, CONFIG_FILE)


    def apply_theme(self, app, theme_name: str) -> None:
        """Applies the specified theme to the GUI."""
        theme = self.theme_config['theme'][theme_name]

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
        current_mode = self.theme_config['theme']['mode']
        new_mode = 'dark' if current_mode == 'light' else 'light'
        self.theme_config['theme']['mode'] = new_mode
        self.theme_config = save_config(self.theme_config, CONFIG_FILE)
        self.apply_theme(app, new_mode)
        app.dark_mode_button.config(text="Switch to Light Mode" if new_mode == 'dark' else "Switch to Dark Mode")