import os
import tkinter as tk
from gui.app import FolderDrop

# def test_open_selected_file_opens_explorer(mocker):
#     # Create a mock FolderDrop instance
#     app = FolderDrop()

#     # Mock the file explorer function
#     mock_open_file_explorer = mocker.patch.object(app, 'open_file_explorer')

#     # Insert a file path into the result listbox
#     file_path = os.path.normpath("/some/path/to/file.txt")
#     app.result_listbox.insert(tk.END, file_path)

#     # Simulate a double-click event
#     app.result_listbox.selection_set(0)
#     app.open_selected_file()

#     # Assert that the open_file_explorer method was called with the correct file path
#     mock_open_file_explorer.assert_called_once_with(file_path)


# def test_double_click_opens_explorer_from_left(mocker):
#     if os.name == 'nt':
#         # Mock the TkinterDnD class to avoid initializing the actual GUI components
#         mocker.patch('tkinterdnd2.TkinterDnD', autospec=True)

#         # Create a mock FolderDrop instance
#         app = FolderDrop()

#         # Mock the subprocess.run function
#         mock_subprocess_run = mocker.patch('subprocess.run')

#         # Insert a file path into the left listbox
#         file_path = "C:\\some\\path\\to\\file.txt"
#         app.left_listbox.insert(tk.END, file_path)

#         # Simulate a double-click event
#         app.left_listbox.selection_set(0)
#         app.left_listbox.event_generate('<Double-Button-1>')

#         # Assert that subprocess.run was called with the correct arguments
#         mock_subprocess_run.assert_called_once_with(['explorer', '/select,', file_path])


# def test_double_click_opens_explorer_from_middle(mocker):
#     if os.name == 'nt':
#         # Mock the TkinterDnD class to avoid initializing the actual GUI components
#         mocker.patch('tkinterdnd2.TkinterDnD', autospec=True)

#         # Create a mock FolderDrop instance
#         app = FolderDrop()

#         # Mock the subprocess.run function
#         mock_subprocess_run = mocker.patch('subprocess.run')

#         # Insert a file path into the right listbox
#         file_path = "C:\\some\\path\\to\\folder"
#         app.right_listbox.insert(tk.END, file_path)

#         # Simulate a double-click event
#         app.right_listbox.selection_set(0)
#         app.right_listbox.event_generate('<Double-Button-1>')

#         # Assert that subprocess.run was called with the correct arguments
#         mock_subprocess_run.assert_called_once_with(['explorer', '/select,', file_path])


# def test_double_click_opens_explorer_from_result(mocker):
#     if os.name == 'nt':
#         # Mock the TkinterDnD class to avoid initializing the actual GUI components
#         mocker.patch('tkinterdnd2.TkinterDnD', autospec=True)

#         # Create a mock FolderDrop instance
#         app = FolderDrop()

#         # Mock the subprocess.run function
#         mock_subprocess_run = mocker.patch('subprocess.run')

#         # Insert a file path into the result listbox
#         file_path = "C:\\some\\path\\to\\file.txt"
#         app.result_listbox.insert(tk.END, file_path)

#         # Simulate a double-click event
#         app.result_listbox.selection_set(0)
#         app.result_listbox.event_generate('<Double-Button-1>')

#         # Assert that subprocess.run was called with the correct arguments
#         mock_subprocess_run.assert_called_once_with(['explorer', '/select,', file_path])