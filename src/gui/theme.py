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


    def apply_theme(self, app, theme_name) -> None:
        """Applies the specified theme to the GUI."""
        theme = self.theme_config[theme_name]

        app.configure(bg=theme['bg'])
        app.top_frame.configure(bg=theme['bg'])
        app.search_button.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])
        app.delete_button.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])
        app.theme_button.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])

        app.left_frame.configure(bg=theme['bg'])
        app.middle_frame.configure(bg=theme['bg'])
        app.right_frame.configure(bg=theme['bg'])

        app.left_listbox.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])
        app.right_listbox.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])
        app.result_listbox.configure(bg=theme['widget_bg'], fg=theme['widget_fg'])


    def toggle_themes(self, app) -> None:
        """Toggles between themes and saves the current one."""
        # Get the next theme using the get_next_theme method
        new_theme = self.get_next_theme()
        # Update the theme configuration
        self.theme_config['theme'] = new_theme
        self.theme_config = save_config(self.theme_config, CONFIG_FILE)
        # Apply the new theme to the app
        self.apply_theme(app, new_theme)
        # Update the button text based on the new theme
        app.theme_button.config(
            text=self.get_button_text()
        )


    def get_next_theme(self) -> str:
        current_theme: str = self.theme_config["theme"]
        theme_keys: list[str] = [key for key in self.theme_config.keys() if key != "theme"]

        try:
            # Find the index of the current theme in the list of themes
            current_index: int = theme_keys.index(current_theme)
            # Get the next theme, or wrap around to the first one if at the end
            next_theme: str = theme_keys[(current_index + 1) % len(theme_keys)]
        except ValueError:
            # If the current theme is not in the theme_keys list, return the first theme
            next_theme = theme_keys[0]
        return next_theme


    def get_available_themes(self) -> List[str]:
        """Returns a list of available theme names from the configuration."""
        return [theme for theme in self.theme_config.keys() if theme != 'theme']


    def get_button_text(self) -> str:
        """Returns the appropriate button text based on the new theme."""
        return f"Switch to {self.get_next_theme().capitalize()} Mode"