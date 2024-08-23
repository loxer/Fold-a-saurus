import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from gui.search import search_files
from gui.dragdrop import drop_left, drop_right
import os
import subprocess
from typing import Dict, List, Optional

class FolderDrop(TkinterDnD.Tk):
    def __init__(self) -> None:
        super().__init__()
        
        self.title("Folder and File Search GUI")
        self.geometry("800x400")  # Increased width to accommodate the result column

        # Dictionary to store full paths for items in the left listbox
        self.left_items_paths: Dict[str, str] = {}

        # Create the top frame for buttons
        self.top_frame: tk.Frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Search button
        self.search_button: tk.Button = tk.Button(self.top_frame, text="Search", command=self.search_files)
        self.search_button.pack(side=tk.LEFT)

        # Delete button
        self.delete_button: tk.Button = tk.Button(self.top_frame, text="Delete", command=self.delete_selected_items)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        # Create frames for the left and right columns
        self.left_frame: tk.Frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.middle_frame: tk.Frame = tk.Frame(self)
        self.middle_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.right_frame: tk.Frame = tk.Frame(self)
        self.right_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Listbox for left column (files or folders) - enable multi-selection
        self.left_listbox: tk.Listbox = tk.Listbox(self.left_frame, selectmode=tk.EXTENDED)
        self.left_listbox.pack(fill=tk.BOTH, expand=True)
        self.left_listbox.bind('<Double-Button-1>', self.open_selected_file_from_left)  # Bind double-click event

        # Listbox for middle column (folders) - enable multi-selection
        self.right_listbox: tk.Listbox = tk.Listbox(self.middle_frame, selectmode=tk.EXTENDED)
        self.right_listbox.pack(fill=tk.BOTH, expand=True)
        self.right_listbox.bind('<Double-Button-1>', self.open_selected_file_from_right)  # Bind double-click event

        # Listbox for the result column
        self.result_listbox: tk.Listbox = tk.Listbox(self.right_frame, selectmode=tk.SINGLE)
        self.result_listbox.pack(fill=tk.BOTH, expand=True)
        self.result_listbox.bind('<Double-Button-1>', self.open_selected_file_from_result)  # Bind double-click event

        # Initialize drag-and-drop functionality
        self.setup_drag_and_drop()

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