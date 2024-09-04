import os
import tkinter as tk
from typing import List

def search_files(left_listbox: tk.Listbox, right_listbox: tk.Listbox, result_listbox: tk.Listbox) -> None:
    """Search for files or folders listed in the left listbox within the directories listed in the right listbox."""
    result_listbox.delete(0, tk.END)  # Clear previous results
    found_matches: bool = False

    # Get the list of items in the left and right listboxes
    left_items: List[str] = [left_listbox.get(i) for i in range(left_listbox.size())]
    right_dirs: List[str] = [right_listbox.get(i) for i in range(right_listbox.size())]

    # Iterate over each directory in the right listbox
    for right_dir in right_dirs:
        for root, dirs, files in os.walk(right_dir):
            # Check for folder matches
            for left_item in left_items:
                left_item_path: str = os.path.basename(left_item)  # Get just the folder or file name
                if left_item_path in dirs:
                    match_path: str = os.path.join(root, left_item_path)
                    result_listbox.insert(tk.END, match_path)
                    found_matches = True

            # Check for file matches
            for left_item in left_items:
                left_item_path: str = os.path.basename(left_item)  # Get just the file name
                if left_item_path in files:
                    match_path: str = os.path.join(root, left_item_path)
                    result_listbox.insert(tk.END, match_path)
                    found_matches = True

    if not found_matches:
        not_found()


def perform_fast_search(query: str, right_listbox: tk.Listbox, result_listbox: tk.Listbox) -> None:
    """Performs a search based on the input query and directories in the right listbox."""
    found_matches: bool = False
    right_dirs: List[str] = [right_listbox.get(i) for i in range(right_listbox.size())]

    # Iterate over each directory in the right listbox
    for right_dir in right_dirs:
        for root, dirs, files in os.walk(right_dir):
            # Search for matches in files and directories based on the search query
            for name in files + dirs:
                if query.lower() in name.lower():  # Case-insensitive match
                    match_path: str = os.path.join(root, name)
                    result_listbox.insert(tk.END, match_path)
                    found_matches = True

    if not found_matches:
        not_found()


def not_found(result_listbox: tk.Listbox) -> None:
    """Display a 'Not Found' message in the result listbox."""
    result_listbox.delete(0, tk.END)  # Clear previous results
    result_listbox.insert(tk.END, "Not Found")