import os
import tkinter as tk
from gui.dragdrop import drop_left, drop_right

def test_drop_left_inserts_file_name(mocker):
    # Create a mock listbox
    listbox = tk.Listbox()

    # Mock event with a file path
    event = mocker.Mock()
    event.data = "{/some/path/to/file.txt}"

    # Mock os.path.isfile to return True
    mocker.patch("os.path.isfile", return_value=True)

    # Call drop_left with the mock event and listbox
    drop_left(event, listbox)

    # Assert that the file name was inserted into the listbox
    assert listbox.get(0) == "file.txt"


def test_drop_left_inserts_folder_name(mocker):
    # Create a mock listbox
    listbox = tk.Listbox()

    # Mock event with a folder path
    event = mocker.Mock()
    event.data = "{/some/path/to/folder}"

    # Mock os.path.isdir to return True
    mocker.patch("os.path.isdir", return_value=True)

    # Call drop_left with the mock event and listbox
    drop_left(event, listbox)

    # Assert that the folder name was inserted into the listbox
    assert listbox.get(0) == "folder"


# def test_drop_right_inserts_folder_path(mocker):
#     # Create a mock listbox
#     listbox = tk.Listbox()

#     # Mock event with a folder path
#     event = mocker.Mock()
#     event.data = "{/some/path/to/folder}"

#     # Mock os.path.isdir to return True
#     mocker.patch("os.path.isdir", return_value=True)

#     # Call drop_right with the mock event and listbox
#     drop_right(event, listbox)

#     # Normalize the expected path for comparison
#     expected_path = os.path.normpath("/some/path/to/folder")

#     # Assert that the folder path was inserted into the listbox
#     assert listbox.get(0) == expected_path