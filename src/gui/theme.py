import os
import json
from typing import Dict, List
from gui.utils import save_config, load_config

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'configs', 'user', 'profile1', 'theme.json')
DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'configs', 'defaults', 'default_theme.json')


class ThemeManager:
    def __init__(self):
        self.theme_config = load_config(DEFAULT_CONFIG_FILE, CONFIG_FILE)


    def set_theme(self, app) -> None:
        """Sets the theme based on the loaded configuration."""
        theme = self.theme_config['theme']
        self.apply_theme(app, theme)


    def apply_theme(self, app, theme_name: str) -> None:
        """Applies the specified theme to the GUI and saves it as the current theme."""
        # Apply the theme
        theme = self.theme_config[theme_name]

        app.configure(bg=theme['bg'])
        app.top_frame.configure(bg=theme['bg'])
        app.search_button.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])
        app.delete_button.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])

        app.left_frame.configure(bg=theme['bg'])
        app.middle_frame.configure(bg=theme['bg'])
        app.right_frame.configure(bg=theme['bg'])

        app.left_listbox.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])
        app.right_listbox.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])
        app.result_listbox.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])

        # Save the applied theme as the current theme
        self.theme_config['theme'] = theme_name
        save_config(self.theme_config, CONFIG_FILE)


    def get_available_themes(self) -> List[str]:
        """Returns a list of available theme names from the configuration."""
        return [theme for theme in self.theme_config.keys() if theme != 'theme']