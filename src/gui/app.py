import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from gui.search import search_files
from gui.dragdrop import drop_left, drop_right
import os
import subprocess
from typing import Dict, List, Optional
import json

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'gui_config.json')


class FolderDrop(TkinterDnD.Tk):
    def __init__(self) -> None:
        super().__init__()

        # Dictionary to store full paths for items in the left listbox
        self.left_items_paths: Dict[str, str] = {}

        # Load GUI settings from config file
        self.gui_config = self.load_gui_config()

        # Set window size and position
        window_width = self.gui_config['window_size'].get('width', 800)
        window_height = self.gui_config['window_size'].get('height', 400)
        window_x = self.gui_config['window_size'].get('x', 100)
        window_y = self.gui_config['window_size'].get('y', 100)
        self.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

        self.title("Folder and File Search GUI")

        # Load column sizes from config file
        self.column_sizes = self.gui_config.get('column_sizes', {'left': 200, 'middle': 200, 'right': 200})

        # Create the top frame for buttons
        self.top_frame: tk.Frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Search button
        self.search_button: tk.Button = tk.Button(self.top_frame, text="Search", command=self.search_files)
        self.search_button.pack(side=tk.LEFT)

        # Delete button
        self.delete_button: tk.Button = tk.Button(self.top_frame, text="Delete", command=self.delete_selected_items)
        self.delete_button.pack(side=tk.LEFT, padx=10)

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

        # Bind resizing event for window
        self.bind("<Configure>", self.on_window_resize)

        # Bind resizing event for columns
        self.paned_window.bind("<B1-Motion>", self.on_resize)

        # Initialize drag-and-drop functionality
        self.setup_drag_and_drop()

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
        self.save_gui_config()

    def on_window_resize(self, event: tk.Event) -> None:
        """Handles the resizing and movement of the window and saves the new size and position to the config file."""
        if event.widget == self:
            self.gui_config['window_size']['width'] = self.winfo_width()
            self.gui_config['window_size']['height'] = self.winfo_height()
            self.gui_config['window_size']['x'] = self.winfo_x()
            self.gui_config['window_size']['y'] = self.winfo_y()
            self.save_gui_config()

    def save_gui_config(self) -> None:
        """Saves the current GUI configuration to a config file."""
        # Ensure the directory exists
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
        """Loads GUI configuration from a config file."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {
            'window_size': {'width': 800, 'height': 400, 'x': 100, 'y': 100},
            'column_sizes': {'left': 200, 'middle': 200, 'right': 200}
        }
