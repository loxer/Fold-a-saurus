import os
import tkinter as tk
from typing import List
from moviepy.editor import VideoFileClip  # Requires moviepy library

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
                    display_text = format_file_info(match_path)
                    result_listbox.insert(tk.END, display_text)
                    found_matches = True

    if not found_matches:
        not_found(result_listbox)


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
                    display_text = format_file_info(match_path)
                    result_listbox.insert(tk.END, display_text)
                    found_matches = True

    if not found_matches:
        not_found(result_listbox)


def format_file_info(filepath: str) -> str:
    """Formats file information including size and, if applicable, video length."""
    file_size = os.path.getsize(filepath)
    size_str = f"{file_size} bytes"

    if is_video_file(filepath):
        try:
            clip = VideoFileClip(filepath)
            duration = clip.duration
            clip.close()
            duration_str = f" | Duration: {format_duration(duration)}"
        except Exception as e:
            duration_str = " | Duration: Unknown"
    else:
        duration_str = ""

    return f"{filepath} | Size: {size_str}{duration_str}"


def is_video_file(filepath: str) -> bool:
    """Checks if a file is a video based on its extension."""
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    return os.path.splitext(filepath)[1].lower() in video_extensions


def format_duration(seconds: float) -> str:
    """Formats duration from seconds to a hh:mm:ss string."""
    hrs, rem = divmod(seconds, 3600)
    mins, secs = divmod(rem, 60)
    return f"{int(hrs):02}:{int(mins):02}:{int(secs):02}"


def not_found(result_listbox: tk.Listbox) -> None:
    """Display a 'Not Found' message in the result listbox."""
    result_listbox.delete(0, tk.END)  # Clear previous results
    result_listbox.insert(tk.END, "Not Found")
