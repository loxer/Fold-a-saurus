# import tkinter as tk
# from tkinterdnd2 import TkinterDnD, DND_FILES
# import os
# import fnmatch
# from tkinter import messagebox

# class FolderDrop(TkinterDnD.Tk):
#     def __init__(self):
#         super().__init__()
        
#         self.title("Folder and File Search GUI")
#         self.geometry("600x400")

#         # Create frames for the left and right columns
#         self.left_frame = tk.Frame(self)
#         self.left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

#         self.right_frame = tk.Frame(self)
#         self.right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

#         # Listbox for left column (files or folders)
#         self.left_listbox = tk.Listbox(self.left_frame, selectmode=tk.SINGLE)
#         self.left_listbox.pack(fill=tk.BOTH, expand=True)
#         self.left_listbox.bind('<Delete>', self.delete_selected_left)

#         # Listbox for right column (folders)
#         self.right_listbox = tk.Listbox(self.right_frame, selectmode=tk.SINGLE)
#         self.right_listbox.pack(fill=tk.BOTH, expand=True)
#         self.right_listbox.bind('<Delete>', self.delete_selected_right)

#         # Search button
#         self.search_button = tk.Button(self, text="Search", command=self.search_files)
#         self.search_button.pack(pady=10)

#         # Registering left and right columns for drag and drop
#         self.left_listbox.drop_target_register(DND_FILES)
#         self.left_listbox.dnd_bind('<<Drop>>', self.drop_left)

#         self.right_listbox.drop_target_register(DND_FILES)
#         self.right_listbox.dnd_bind('<<Drop>>', self.drop_right)

#     def drop_left(self, event):
#         path = event.data.strip('{}')
#         if os.path.isdir(path) or os.path.isfile(path):
#             file_name = os.path.basename(path)
#             self.left_listbox.insert(tk.END, file_name)

#     def drop_right(self, event):
#         path = event.data.strip('{}')
#         if os.path.isdir(path):
#             self.right_listbox.insert(tk.END, path)
#         else:
#             tk.messagebox.showerror("Invalid Drop", "Please drop only folders on the right side.")

#     def delete_selected(self):
#         # Delete from left listbox
#         left_selection = self.left_listbox.curselection()
#         if left_selection:
#             self.left_listbox.delete(left_selection)

#         # Delete from right listbox
#         right_selection = self.right_listbox.curselection()
#         if right_selection:
#             self.right_listbox.delete(right_selection)

#     def delete_selected_left(self, event=None):
#         selection = self.left_listbox.curselection()
#         if selection:
#             self.left_listbox.delete(selection)

#     def delete_selected_right(self, event=None):
#         selection = self.right_listbox.curselection()
#         if selection:
#             self.right_listbox.delete(selection)

#     def search_files(self):
#         results = []
#         left_items = self.left_listbox.get(0, tk.END)
#         right_folders = self.right_listbox.get(0, tk.END)

#         for folder in right_folders:
#             for root, dirs, files in os.walk(folder):
#                 for left_item in left_items:
#                     # Search for both files and folders
#                     if left_item in dirs or left_item in files:
#                         full_path = os.path.join(root, left_item)
#                         results.append(full_path)

#         if results:
#             result_message = "Found the following matches:\n" + "\n".join(results)
#             messagebox.showinfo("Search Results", result_message)
#         else:
#             messagebox.showinfo("Search Results", "No matches found.")

#     def process_folder(self, folder_path):
#         # Placeholder for your folder processing code
#         print(f"Processing folder: {folder_path}")
#         # Add your processing logic here

# if __name__ == "__main__":
#     app = FolderDrop()
#     app.mainloop()