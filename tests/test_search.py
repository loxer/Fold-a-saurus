import os
import tkinter as tk
from gui.search import search_files

def test_search_files_no_matches(mocker):
    # Create mock listboxes
    left_listbox = tk.Listbox()
    right_listbox = tk.Listbox()

    # Add test data
    left_listbox.insert(tk.END, "nonexistent_file.txt")
    right_listbox.insert(tk.END, "/some/folder")

    # Mock os.walk to return empty results
    mocker.patch("os.walk", return_value=iter([]))

    # Mock the messagebox.showinfo function
    mock_messagebox = mocker.patch("tkinter.messagebox.showinfo")

    # Run search_files
    search_files(left_listbox, right_listbox)

    # Assert that the messagebox was called with "No matches found."
    mock_messagebox.assert_called_once_with("Search Results", "No matches found.")


def test_search_files_with_matches(mocker):
    # Create mock listboxes
    left_listbox = tk.Listbox()
    right_listbox = tk.Listbox()

    # Add test data
    left_listbox.insert(tk.END, "example.txt")
    right_listbox.insert(tk.END, "/some/folder")

    # Mock os.walk to return matching results
    mocker.patch("os.walk", return_value=iter([("/some/folder", [], ["example.txt"])]))

    # Mock the messagebox.showinfo function
    mock_messagebox = mocker.patch("tkinter.messagebox.showinfo")

    # Run search_files
    search_files(left_listbox, right_listbox)

    # Normalize the expected path for comparison
    expected_path = os.path.normpath("/some/folder/example.txt")
    expected_message = f"Found the following matches:\n{expected_path}"

    # Assert that the messagebox was called with the correct match message
    mock_messagebox.assert_called_once_with("Search Results", expected_message)