import os
import tkinter as tk
from tkinter import messagebox

def drop_left(event, add_to_listbox_callback):
    # Remove the curly braces and split the paths using a more reliable method
    paths = event.data.strip('{}').split('}')
    paths = [path.strip() for path in paths if path.strip()]

    # Filter paths for files and directories
    valid_paths = [path for path in paths if os.path.isdir(path) or os.path.isfile(path)]
    
    # Use the callback to add the items to the listbox
    add_to_listbox_callback(valid_paths)

def drop_right(event, listbox):
    # Remove the curly braces and split the paths using a more reliable method
    paths = event.data.strip('{}').split('}')
    paths = [path.strip() for path in paths if path.strip()]

    # Filter paths to ensure only directories are added
    valid_paths = [path for path in paths if os.path.isdir(path)]
    
    if not valid_paths:
        tk.messagebox.showerror("Invalid Drop", "Please drop only folders on the right side.")
        return
    
    # Add directories to the listbox
    for path in valid_paths:
        listbox.insert(tk.END, path)
