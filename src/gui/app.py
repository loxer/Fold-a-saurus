import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from gui.search import search_files
from gui.dragdrop import drop_left, drop_right
from gui.theme import ThemeManager
from gui.utils import save_config, load_config
from typing import Dict, List, Optional
import os
import subprocess
import json


CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'configs', 'profile1', 'gui.json')
DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'configs', 'defaults', 'default_gui.json')


class FolderDrop(TkinterDnD.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.setup_environment()
        self.set_window_position()        
        self.set_gui_parameters()
        self.setup_top_frame()
        self.setup_columns()
        self.set_theme()
        self.set_bindings()
        self.setup_drag_and_drop()


    def setup_environment(self) -> None:
        # Dictionary to store full paths for items in the left listbox
        self.left_items_paths: Dict[str, str] = {}

        # Load GUI settings from config file
        self.gui_config: dict = load_config(DEFAULT_CONFIG_FILE, CONFIG_FILE)
        self.title("Fold-A-Saurus")

        # Initialize the theme manager
        self.theme_manager = ThemeManager()


    def set_window_position(self) -> None:
        """Sets the window position based on the loaded configuration."""
        window_width = self.gui_config['window_size'].get('width', 800)
        window_height = self.gui_config['window_size'].get('height', 400)
        window_x = self.gui_config['window_size'].get('x', 100)
        window_y = self.gui_config['window_size'].get('y', 100)
        self.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")


    def set_gui_parameters(self) -> None:
        # Load column sizes from config file
        self.column_sizes = self.gui_config.get('column_sizes', {'left': 200, 'middle': 200, 'right': 200})


    def setup_top_frame(self) -> None:
        """Sets up the top frame with buttons, e.g., search, delete, and theme toggle."""
        # Create the top frame for buttons
        self.top_frame: tk.Frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Search button
        self.search_button: tk.Button = tk.Button(self.top_frame, text="Search", command=self.search_files)
        self.search_button.pack(side=tk.LEFT)

        # Delete button
        self.delete_button: tk.Button = tk.Button(self.top_frame, text="Delete", command=self.delete_selected_items)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        # Toggle Themes button
        button_text = self.theme_manager.get_button_text()
        self.theme_button: tk.Button = tk.Button(
            self.top_frame, 
            text=button_text, 
            command=lambda: self.theme_manager.toggle_themes(self)
        )
        self.theme_button.pack(side=tk.LEFT, padx=10)


    def setup_columns(self) -> None:
        # Create a paned window for resizable columns
        self.paned_window: tk.PanedWindow = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Create frames for the left, middle, and right columns
        self.left_frame: tk.Frame = tk.Frame(self.paned_window, width=self.column_sizes.get('left', 200))
        self.middle_frame: tk.Frame = tk.Frame(self.paned_window, width=self.column_sizes.get('middle', 200))
        self.right_frame: tk.Frame = tk.Frame(self.paned_window, width=self.column_sizes.get('right', 200))

        self.paned_window.add(self.left_frame)
        self.paned_window.add(self.middle_frame)
        self.paned_window.add(self.right_frame)

        # Explicitly set the widths of the panes after adding them
        self.after(100, self.apply_column_sizes)

        # Listbox for left column (files or folders) - enable multi-selection
        self.left_listbox: tk.Listbox = tk.Listbox(self.left_frame, selectmode=tk.EXTENDED)
        self.left_listbox.pack(fill=tk.BOTH, expand=True)
        self.left_listbox.bind('<Double-Button-1>', self.open_selected_file_from_left)

        # Listbox for middle column (folders) - enable multi-selection
        self.right_listbox: tk.Listbox = tk.Listbox(self.middle_frame, selectmode=tk.EXTENDED)
        self.right_listbox.pack(fill=tk.BOTH, expand=True)
        self.right_listbox.bind('<Double-Button-1>', self.open_selected_file_from_right)

        # Listbox for the result column
        self.result_listbox: tk.Listbox = tk.Listbox(self.right_frame, selectmode=tk.SINGLE)
        self.result_listbox.pack(fill=tk.BOTH, expand=True)
        self.result_listbox.bind('<Double-Button-1>', self.open_selected_file_from_result)


    def set_theme(self):
        self.theme_manager.set_theme(self)


    def set_bindings(self) -> None:
        # Bind resizing event for window
        self.bind("<Configure>", self.on_window_resize)

        # Bind resizing event for columns
        self.paned_window.bind("<B1-Motion>", self.on_resize)


    def apply_column_sizes(self) -> None:
        """Applies the column sizes based on the loaded configuration."""
        total_width = self.left_frame.winfo_width() + self.middle_frame.winfo_width() + self.right_frame.winfo_width()
        self.paned_window.paneconfig(self.left_frame, width=self.column_sizes['left'])
        self.paned_window.paneconfig(self.middle_frame, width=self.column_sizes['middle'])
        self.paned_window.paneconfig(self.right_frame, width=total_width - self.column_sizes['left'] - self.column_sizes['middle'])


    def setup_drag_and_drop(self) -> None:
        """Sets up drag-and-drop functionality for the left and right listboxes."""
        self.left_listbox.drop_target_register(DND_FILES)
        self.left_listbox.dnd_bind('<<Drop>>', lambda event: drop_left(event, self.add_to_left_listbox))

        self.right_listbox.drop_target_register(DND_FILES)
        self.right_listbox.dnd_bind('<<Drop>>', lambda event: drop_right(event, self.right_listbox))


    def search_files(self) -> None:
        self.result_listbox.delete(0, tk.END)  # Clear previous results
        search_files(self.left_listbox, self.right_listbox, self.result_listbox)

    def delete_selected_items(self) -> None:
        """Handles deletion of selected items from the left and middle columns."""
        # Delete from left listbox
        left_selection: List[int] = self.left_listbox.curselection()
        for index in reversed(left_selection):  # Iterate in reverse to avoid index issues
            selected_item: str = self.left_listbox.get(index)
            self.left_listbox.delete(index)
            del self.left_items_paths[selected_item]  # Remove the corresponding full path

        # Delete from right listbox
        right_selection: List[int] = self.right_listbox.curselection()
        for index in reversed(right_selection):  # Iterate in reverse to avoid index issues
            self.right_listbox.delete(index)

    def open_selected_file_from_left(self, event: Optional[tk.Event] = None) -> None:
        selection: List[int] = self.left_listbox.curselection()
        for index in selection:
            selected_item: str = self.left_listbox.get(index)
            full_path: Optional[str] = self.left_items_paths.get(selected_item)
            if full_path:
                self.open_file_explorer(full_path)

    def open_selected_file_from_right(self, event: Optional[tk.Event] = None) -> None:
        selection: List[int] = self.right_listbox.curselection()
        for index in selection:
            selected_item: str = self.right_listbox.get(index)
            self.open_file_explorer(selected_item)

    def open_selected_file_from_result(self, event: Optional[tk.Event] = None) -> None:
        selection: List[int] = self.result_listbox.curselection()
        if selection:
            selected_file: str = self.result_listbox.get(selection[0])
            self.open_file_explorer(selected_file)

    def open_file_explorer(self, filepath: str) -> None:
        if os.path.isdir(filepath) or os.path.isfile(filepath):
            if os.name == 'nt':  # Windows
                subprocess.run(['explorer', '/select,', os.path.normpath(filepath)])
            elif os.name == 'posix':  # Linux
                subprocess.run(['xdg-open', os.path.dirname(filepath)])

    def add_to_left_listbox(self, paths: List[str]) -> None:
        """ Adds multiple items to the left listbox, showing only the name but storing the full path. """
        for path in paths:
            file_name: str = os.path.basename(path)
            self.left_listbox.insert(tk.END, file_name)
            self.left_items_paths[file_name] = path

    def on_resize(self, event: tk.Event) -> None:
        """Handles the resizing of columns and saves the sizes to the config file."""
        self.gui_config['column_sizes']['left'] = self.left_frame.winfo_width()
        self.gui_config['column_sizes']['middle'] = self.middle_frame.winfo_width()
        self.gui_config['column_sizes']['right'] = self.right_frame.winfo_width()
        self.gui_config = save_config(self.gui_config, CONFIG_FILE)

    def on_window_resize(self, event: tk.Event) -> None:
        """Handles the resizing and movement of the window and saves the new size and position to the config file."""
        if event.widget == self:
            self.gui_config['window_size']['width'] = self.winfo_width()
            self.gui_config['window_size']['height'] = self.winfo_height()
            self.gui_config['window_size']['x'] = self.winfo_x()
            self.gui_config['window_size']['y'] = self.winfo_y()
            self.gui_config = save_config(self.gui_config, CONFIG_FILE)