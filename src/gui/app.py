import tkinter as tk
from tkinterdnd2 import TkinterDnD
from gui.dragdrop import setup_drag_and_drop
from gui.search import search_files

class FolderDrop(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Folder and File Search GUI")
        self.geometry("600x400")

        # Create frames for the left and right columns
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Listbox for left column (files or folders)
        self.left_listbox = tk.Listbox(self.left_frame, selectmode=tk.SINGLE)
        self.left_listbox.pack(fill=tk.BOTH, expand=True)
        self.left_listbox.bind('<Delete>', self.delete_selected_left)

        # Listbox for right column (folders)
        self.right_listbox = tk.Listbox(self.right_frame, selectmode=tk.SINGLE)
        self.right_listbox.pack(fill=tk.BOTH, expand=True)
        self.right_listbox.bind('<Delete>', self.delete_selected_right)

        # Search button
        self.search_button = tk.Button(self, text="Search", command=self.search_files)
        self.search_button.pack(pady=10)

        # Initialize drag-and-drop functionality
        setup_drag_and_drop(self)

    def search_files(self):
        search_files(self.left_listbox, self.right_listbox)

    def delete_selected_left(self, event=None):
        selection = self.left_listbox.curselection()
        if selection:
            self.left_listbox.delete(selection)

    def delete_selected_right(self, event=None):
        selection = self.right_listbox.curselection()
        if selection:
            self.right_listbox.delete(selection)