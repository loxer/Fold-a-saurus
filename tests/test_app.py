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

    # Run search_files and assert it returns no matches
    search_files(left_listbox, right_listbox)
    # Expectation: No matches found, which you might want to verify by capturing the messagebox call


def test_search_files_with_matches(mocker):
    # Create mock listboxes
    left_listbox = tk.Listbox()
    right_listbox = tk.Listbox()

    # Add test data
    left_listbox.insert(tk.END, "example.txt")
    right_listbox.insert(tk.END, "/some/folder")

    # Mock os.walk to return matching results
    mocker.patch("os.walk", return_value=iter([("/some/folder", [], ["example.txt"])]))

    # Run search_files and capture the messagebox output
    mock_messagebox = mocker.patch("tkinter.messagebox.showinfo")
    search_files(left_listbox, right_listbox)
    
    # Normalize the paths for comparison
    expected_path = os.path.normpath("/some/folder/example.txt")
    expected_message = f"Found the following matches:\n{expected_path}"

    # Assert that the mock messagebox was called with the correct normalized path
    mock_messagebox.assert_called_once_with("Search Results", expected_message)