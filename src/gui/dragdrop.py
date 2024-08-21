import os
import tkinter as tk
from tkinterdnd2 import DND_FILES

def setup_drag_and_drop(app):
    app.left_listbox.drop_target_register(DND_FILES)
    app.left_listbox.dnd_bind('<<Drop>>', lambda e: drop_left(e, app.left_listbox))

    app.right_listbox.drop_target_register(DND_FILES)
    app.right_listbox.dnd_bind('<<Drop>>', lambda e: drop_right(e, app.right_listbox))

def drop_left(event, listbox):
    path = event.data.strip('{}')
    if os.path.isdir(path) or os.path.isfile(path):
        file_name = os.path.basename(path)
        listbox.insert(tk.END, file_name)

def drop_right(event, listbox):
    path = event.data.strip('{}')
    if os.path.isdir(path):
        listbox.insert(tk.END, path)
    else:
        tk.messagebox.showerror("Invalid Drop", "Please drop only folders on the right side.")
