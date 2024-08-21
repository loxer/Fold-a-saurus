import os
import fnmatch
import tkinter as tk
from tkinter import messagebox

def search_files(left_listbox, right_listbox):
    results = []
    left_items = left_listbox.get(0, tk.END)
    right_folders = right_listbox.get(0, tk.END)

    for folder in right_folders:
        for root, dirs, files in os.walk(folder):
            for left_item in left_items:
                # Search for both files and folders
                if left_item in dirs or left_item in files:
                    full_path = os.path.normpath(os.path.join(root, left_item))
                    results.append(full_path)

    if results:
        result_message = "Found the following matches:\n" + "\n".join(results)
        messagebox.showinfo("Search Results", result_message)
    else:
        messagebox.showinfo("Search Results", "No matches found.")