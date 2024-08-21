import os
import tkinter as tk
from gui.search import search_files

def test_search_files_no_matches(mocker):
    # Create mock listboxes
    left_listbox = tk.Listbox()
    right_listbox = tk.Listbox()
    result_listbox = tk.Listbox()

    # Add test data
    left_listbox.insert(tk.END, "nonexistent_file.txt")
    right_listbox.insert(tk.END, "/some/folder")

    # Mock os.walk to return empty results
    mocker.patch("os.walk", return_value=iter([]))

    # Run search_files
    search_files(left_listbox, right_listbox, result_listbox)

    # Assert that the result_listbox contains "No matches found."
    assert result_listbox.get(0) == "No matches found."


def test_search_files_with_matches(mocker):
    # Create mock listboxes
    left_listbox = tk.Listbox()
    right_listbox = tk.Listbox()
    result_listbox = tk.Listbox()

    # Add test data
    left_listbox.insert(tk.END, "example.txt")
    right_listbox.insert(tk.END, "/some/folder")

    # Mock os.walk to return matching results
    mocker.patch("os.walk", return_value=iter([("/some/folder", [], ["example.txt"])]))

    # Run search_files
    search_files(left_listbox, right_listbox, result_listbox)

    # Normalize the expected path for comparison
    expected_path = os.path.normpath("/some/folder/example.txt")

    # Assert that the result_listbox contains the correct match
    assert result_listbox.get(0) == expected_path
