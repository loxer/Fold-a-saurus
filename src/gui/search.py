import os
import tkinter as tk

def search_files(left_listbox, right_listbox, result_listbox):
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
        for result in results:
            # Add the result to the listbox
            result_listbox.insert(tk.END, result)
    else:
        result_listbox.insert(tk.END, "No matches found.")
