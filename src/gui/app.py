import tkinter as tk
from tkinterdnd2 import TkinterDnD
from gui.dragdrop import setup_drag_and_drop
from gui.search import search_files

import os
import subprocess

class FolderDrop(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Folder and File Search GUI")
        self.geometry("800x400")  # Increased width to accommodate the result column

        # Create frames for the left and right columns
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=20, fill=tk.BOTH, expand=True)

        self.middle_frame = tk.Frame(self)
        self.middle_frame.pack(side=tk.LEFT, padx=10, pady=20, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.LEFT, padx=10, pady=20, fill=tk.BOTH, expand=True)

        # Listbox for left column (files or folders)
        self.left_listbox = tk.Listbox(self.left_frame, selectmode=tk.SINGLE)
        self.left_listbox.pack(fill=tk.BOTH, expand=True)
        self.left_listbox.bind('<Delete>', self.delete_selected_left)

        # Listbox for middle column (folders)
        self.right_listbox = tk.Listbox(self.middle_frame, selectmode=tk.SINGLE)
        self.right_listbox.pack(fill=tk.BOTH, expand=True)
        self.right_listbox.bind('<Delete>', self.delete_selected_right)

        # Listbox for the result column
        self.result_listbox = tk.Listbox(self.right_frame, selectmode=tk.SINGLE)
        self.result_listbox.pack(fill=tk.BOTH, expand=True)
        self.result_listbox.bind('<Double-Button-1>', self.open_selected_file)  # Bind double-click event

        # Search button
        self.search_button = tk.Button(self, text="Search", command=self.search_files)
        self.search_button.pack(pady=10)

        # Initialize drag-and-drop functionality
        setup_drag_and_drop(self)

    def search_files(self):
        self.result_listbox.delete(0, tk.END)  # Clear previous results
        search_files(self.left_listbox, self.right_listbox, self.result_listbox)

    def delete_selected_left(self, event=None):
        selection = self.left_listbox.curselection()
        if selection:
            self.left_listbox.delete(selection)

    def delete_selected_right(self, event=None):
        selection = self.right_listbox.curselection()
        if selection:
            self.right_listbox.delete(selection)

    def open_selected_file(self, event=None):
        selection = self.result_listbox.curselection()
        if selection:
            selected_file = self.result_listbox.get(selection[0])
            self.open_file_explorer(selected_file)

    def open_file_explorer(self, filepath):
        if os.name == 'nt':  # Windows
            subprocess.run(['explorer', '/select,', filepath])
        elif os.name == 'posix':  # Linux
            subprocess.run(['xdg-open', os.path.dirname(filepath)])
