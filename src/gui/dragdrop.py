import os
import tkinter as tk
from tkinter import messagebox
from typing import Callable, List

def drop_left(event: tk.Event, add_to_listbox_callback: Callable[[List[str]], None]) -> None:
    """Handles the drop event for the left listbox, adding files or folders."""
    # Remove the curly braces and split the paths using a more reliable method
    paths: List[str] = event.data.strip('{}').split('}')
    paths = [path.strip() for path in paths if path.strip()]

    # Filter paths for files and directories
    valid_paths: List[str] = [path for path in paths if os.path.isdir(path) or os.path.isfile(path)]
    
    # Use the callback to add the items to the listbox
    add_to_listbox_callback(valid_paths)

def drop_right(event: tk.Event, listbox: tk.Listbox) -> None:
    """Handles the drop event for the right listbox, ensuring no duplicate or subfolders."""
    # Remove the curly braces and split the paths using a more reliable method
    paths: List[str] = event.data.strip('{}').split('}')
    paths = [path.strip() for path in paths if path.strip()]

    # Filter paths to ensure only directories are added
    valid_paths: List[str] = [path for path in paths if os.path.isdir(path)]
    
    if not valid_paths:
        tk.messagebox.showerror("Invalid Drop", "Please drop only folders on the right side.")
        return
    
    existing_paths: List[str] = [listbox.get(i) for i in range(listbox.size())]
    
    for path in valid_paths:
        # Check if the path is a subfolder of any existing path
        if any(os.path.commonpath([path, existing_path]) == existing_path for existing_path in existing_paths):
            continue  # Skip adding if the path is a subfolder of an existing path
        
        # Remove any existing subfolders of the new path
        to_remove: List[str] = [existing_path for existing_path in existing_paths if os.path.commonpath([path, existing_path]) == path]
        for subfolder in to_remove:
            index: int = listbox.get(0, tk.END).index(subfolder)
            listbox.delete(index)
            existing_paths.remove(subfolder)

        # Add the new path since it's neither a subfolder nor has a parent folder in the listbox
        listbox.insert(tk.END, path)
        existing_paths.append(path)