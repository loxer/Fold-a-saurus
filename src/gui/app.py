import multiprocessing
import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from gui.search import search_files, perform_fast_search, search_files_multiprocessing, perform_fast_search_multiprocessing
from gui.dragdrop import drop_left, drop_right
from gui.theme import ThemeManager
from gui.utils import save_config, load_config, save_listbox_states, load_listbox_states
from gui.paths import CONFIG_LISTBOX_STATE_FILE, CONFIG_GUI_FILE, DEFAULT_CONFIG_GUI_FILE
from typing import Dict, List, Optional
import subprocess
import json
import queue



class FolderDrop(TkinterDnD.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.setup_environment()
        self.set_window_position()
        self.set_gui_parameters()
        self.setup_top_frame()
        self.setup_menu_bar()
        self.setup_buttons()
        self.setup_columns()
        self.set_theme()
        self.set_bindings()
        self.setup_drag_and_drop()
        load_listbox_states(CONFIG_LISTBOX_STATE_FILE, self.left_listbox, self.right_listbox, self.result_listbox)


    def start_search(self) -> None:
        """Starts the search in a separate process."""
        self.result_listbox.delete(0, tk.END)  # Clear previous results

        left_items = [self.left_listbox.get(i) for i in range(self.left_listbox.size())]
        right_dirs = [self.right_listbox.get(i) for i in range(self.right_listbox.size())]

        # Start the search in a new process
        self.search_process = multiprocessing.Process(
            target=search_files_multiprocessing, args=(left_items, right_dirs, self.result_queue)
        )
        self.search_process.start()

        # Start polling for results
        self.after(100, self.process_search_results)


    def process_search_results(self) -> None:
        """Processes search results from the queue and updates the UI."""
        try:
            while not self.result_queue.empty():
                result = self.result_queue.get_nowait()
                if result is None:  # None signals the end of the search
                    if self.search_process.is_alive():
                        self.search_process.terminate()
                    return
                self.result_listbox.insert(tk.END, result)  # Update the listbox with the result
        except queue.Empty:
            pass
        # Continue polling
        self.after(100, self.process_search_results)


    def on_search_entry_change(self, event: Optional[tk.Event] = None) -> None:
        """Starts a fast search when input changes and Fast Search is enabled."""
        if self.fast_search:
            search_query = self.search_entry.get().strip()
            if search_query:
                self.result_listbox.delete(0, tk.END)
                self.search_process = multiprocessing.Process(
                    target=perform_fast_search_multiprocessing, args=(search_query, [self.right_listbox.get(i) for i in range(self.right_listbox.size())], self.result_queue)
                )
                self.search_process.start()
                self.after(100, self.process_search_results)



    def setup_environment(self) -> None:
        # Initialize variables
        self.left_items_paths: Dict[str, str] = {}
        self.fast_search = False
        self.result_queue = multiprocessing.Queue()  # Queue to get results from the process
        self.search_process = None  # To hold the search process

        # Prepare lists for the gui
        self.buttons: List[tk.Button] = []
        self.frames: List[tk.Frame] = []
        self.PanedWindow: List[tk.PanedWindow] = []
        self.left_listbox: List[tk.Listbox] = []

        # Load GUI settings from config file
        self.gui_config: dict = load_config(DEFAULT_CONFIG_GUI_FILE, CONFIG_GUI_FILE)
        self.title("Fold-A-Saurus")

        # Save the state of the GUI on close
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Save state on close

        # Initialize the theme manager
        self.theme_manager = ThemeManager()


    def set_window_position(self) -> None:
        """Sets the window position based on the loaded configuration and current screen resolution."""
        window_width = self.gui_config['window_size'].get('width', 800)
        window_height = self.gui_config['window_size'].get('height', 400)
        window_x = self.gui_config['window_size'].get('x', 100)
        window_y = self.gui_config['window_size'].get('y', 100)

        # Adjust window size and position based on screen resolution difference
        current_resolution = self.get_currenct_resolution()
        saved_resolution = self.gui_config.get('monitor_resolution', current_resolution)
        width_ratio = current_resolution['width'] / saved_resolution['width']
        height_ratio = current_resolution['height'] / saved_resolution['height']

        adjusted_width = int(window_width * width_ratio)
        adjusted_height = int(window_height * height_ratio)
        adjusted_x = int(window_x * width_ratio)
        adjusted_y = int(window_y * height_ratio)

        self.geometry(f"{adjusted_width}x{adjusted_height}+{adjusted_x}+{adjusted_y}")


    def set_gui_parameters(self) -> None:
        """Sets the GUI parameters based on loaded configuration and screen resolution."""        
        current_resolution = self.get_currenct_resolution()
        saved_resolution = self.gui_config.get('monitor_resolution', current_resolution)
        width_ratio = current_resolution['width'] / saved_resolution['width']

        # Adjust column sizes based on screen resolution difference
        self.column_sizes = {
            'left': int(self.gui_config['column_sizes'].get('left', 200) * width_ratio),
            'middle': int(self.gui_config['column_sizes'].get('middle', 200) * width_ratio),
            'right': int(self.gui_config['column_sizes'].get('right', 200) * width_ratio)
        }


    def setup_top_frame(self) -> None:
        """Sets up the top frame with buttons, e.g., search, delete, and theme toggle."""
        # Create the top frame for buttons
        self.top_frame: tk.Frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)


    def setup_menu_bar(self) -> None:
        """Sets up the menu bar with Settings and Themes drop-down menus."""
        menu_bar = tk.Menu(self)

        # Settings menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_checkbutton(
            label="Fast Search",
            command=self.toggle_fast_search,
            variable=tk.BooleanVar(value=self.fast_search)  # Track the fast search state
        )
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # Themes menu
        themes_menu = tk.Menu(menu_bar, tearoff=0)
        
        # Load themes from the theme configuration
        themes = self.theme_manager.get_available_themes()
        current_theme = self.theme_manager.theme_config['theme']  # Get the current theme

        for theme_name in themes:
            # Mark the current theme with a checkmark
            themes_menu.add_command(
                label=theme_name,
                command=lambda theme=theme_name: self.apply_selected_theme(theme),
                background="gray" if theme_name == current_theme else ""
            )

        menu_bar.add_cascade(label="Themes", menu=themes_menu)

        # Add the menu bar to the main window
        self.config(menu=menu_bar)


    def apply_selected_theme(self, theme_name: str) -> None:
        """Applies the selected theme and updates the menu to reflect the current theme."""
        self.theme_manager.apply_theme(self, theme_name)
        self.setup_menu_bar()  # Refresh the menu to highlight the current theme


    def setup_buttons(self) -> None:
        # Create the search entry (search bar)
        self.search_entry: tk.Entry = tk.Entry(self.top_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))  # Add padding to separate from the button
        self.search_entry.bind('<KeyRelease>', self.on_search_entry_change)  # Bind input changes

        # Search button
        self.search_button: tk.Button = tk.Button(self.top_frame, text="Search", command=self.start_search)  # Updated command
        self.search_button.pack(side=tk.LEFT)

        # Delete button
        self.delete_button: tk.Button = tk.Button(self.top_frame, text="Delete", command=self.delete_selected_items)
        self.delete_button.pack(side=tk.LEFT, padx=10)



    def setup_columns(self) -> None:
        # Create a paned window for resizable columns
        self.paned_window: tk.PanedWindow = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Create frames for the left, middle, and right columns
        self.left_frame: tk.Frame = tk.Frame(self.paned_window, width=self.column_sizes.get('left', 200))
        self.middle_frame: tk.Frame = tk.Frame(self.paned_window, width=self.column_sizes.get('middle', 200))
        self.right_frame: tk.Frame = tk.Frame(self.paned_window, width=self.column_sizes.get('right', 200))

        self.paned_window.add(self.left_frame)
        self.paned_window.add(self.middle_frame)
        self.paned_window.add(self.right_frame)

        # Explicitly set the widths of the panes after adding them
        self.after(100, self.apply_column_sizes)

        # Listbox for left column (files or folders) - enable multi-selection
        self.left_listbox: tk.Listbox = tk.Listbox(self.left_frame, selectmode=tk.EXTENDED)
        self.left_listbox.pack(fill=tk.BOTH, expand=True)
        self.left_listbox.bind('<Double-Button-1>', self.open_selected_file_from_left)

        # Listbox for middle column (folders) - enable multi-selection
        self.right_listbox: tk.Listbox = tk.Listbox(self.middle_frame, selectmode=tk.EXTENDED)
        self.right_listbox.pack(fill=tk.BOTH, expand=True)
        self.right_listbox.bind('<Double-Button-1>', self.open_selected_file_from_right)

        # Listbox for the result column
        self.result_listbox: tk.Listbox = tk.Listbox(self.right_frame, selectmode=tk.SINGLE)
        self.result_listbox.pack(fill=tk.BOTH, expand=True)
        self.result_listbox.bind('<Double-Button-1>', self.open_selected_file_from_result)  # Bind the double-click event



    def set_theme(self):
        self.theme_manager.set_theme(self)


    def set_bindings(self) -> None:
        # Bind resizing event for window
        self.bind("<Configure>", self.on_window_resize)

        # Bind resizing event for columns
        self.paned_window.bind("<B1-Motion>", self.on_resize)


    def apply_column_sizes(self) -> None:
        """Applies the column sizes based on the loaded configuration."""
        total_width = self.left_frame.winfo_width() + self.middle_frame.winfo_width() + self.right_frame.winfo_width()
        self.paned_window.paneconfig(self.left_frame, width=self.column_sizes['left'])
        self.paned_window.paneconfig(self.middle_frame, width=self.column_sizes['middle'])
        self.paned_window.paneconfig(self.right_frame, width=total_width - self.column_sizes['left'] - self.column_sizes['middle'])


    def setup_drag_and_drop(self) -> None:
        """Sets up drag-and-drop functionality for the left and right listboxes."""
        self.left_listbox.drop_target_register(DND_FILES)
        self.left_listbox.dnd_bind('<<Drop>>', lambda event: drop_left(event, self.add_to_left_listbox))

        self.right_listbox.drop_target_register(DND_FILES)
        self.right_listbox.dnd_bind('<<Drop>>', lambda event: drop_right(event, self.right_listbox))

    
    def toggle_fast_search(self) -> None:
        """Toggles the fast search functionality on and off."""
        self.fast_search = not self.fast_search
        print(f"Fast Search is now {'enabled' if self.fast_search else 'disabled'}")


    def search_files(self) -> None:
        self.result_listbox.delete(0, tk.END)  # Clear previous results
        search_files(self.left_listbox, self.right_listbox, self.result_listbox)

    def delete_selected_items(self) -> None:
        """Handles deletion of selected items from the left and middle columns."""
        # Delete from left listbox
        left_selection: List[int] = self.left_listbox.curselection()
        for index in reversed(left_selection):  # Iterate in reverse to avoid index issues
            selected_item: str = self.left_listbox.get(index)
            self.left_listbox.delete(index)
            del self.left_items_paths[selected_item]  # Remove the corresponding full path

        # Delete from right listbox
        right_selection: List[int] = self.right_listbox.curselection()
        for index in reversed(right_selection):  # Iterate in reverse to avoid index issues
            self.right_listbox.delete(index)

    def open_selected_file_from_left(self, event: Optional[tk.Event] = None) -> None:
        selection: List[int] = self.left_listbox.curselection()
        for index in selection:
            selected_item: str = self.left_listbox.get(index)
            full_path: Optional[str] = self.left_items_paths.get(selected_item)
            if full_path:
                self.open_file_explorer(full_path)

    def open_selected_file_from_right(self, event: Optional[tk.Event] = None) -> None:
        selection: List[int] = self.right_listbox.curselection()
        for index in selection:
            selected_item: str = self.right_listbox.get(index)
            self.open_file_explorer(selected_item)

    def open_selected_file_from_result(self, event: Optional[tk.Event] = None) -> None:
        """Handles the double-click event on the result listbox to open the selected file or directory in the file explorer."""
        selection: List[int] = self.result_listbox.curselection()
        if selection:
            selected_path: str = self.result_listbox.get(selection[0])
            self.open_file_explorer(selected_path)


    def open_file_explorer(self, filepath: str) -> None:
        """Opens the specified file or directory in the file explorer."""
        try:
            if os.path.isdir(filepath):
                # Open the directory directly
                subprocess.run(['explorer', os.path.normpath(filepath)], check=False)
            elif os.path.isfile(filepath):
                # Open the file in its directory and highlight it
                subprocess.run(['explorer', '/select,', os.path.normpath(filepath)], check=False)
        except Exception as e:
            print(f"Error opening file explorer: {e}")



    def add_to_left_listbox(self, paths: List[str]) -> None:
        """ Adds multiple items to the left listbox, showing only the name but storing the full path. """
        for path in paths:
            file_name: str = os.path.basename(path)
            self.left_listbox.insert(tk.END, file_name)
            self.left_items_paths[file_name] = path

    def on_resize(self, event: tk.Event) -> None:
        """Handles the resizing of columns and saves the sizes to the config file."""
        self.gui_config['monitor_resolution'] = self.get_currenct_resolution()
        self.gui_config['column_sizes']['left'] = self.left_frame.winfo_width()
        self.gui_config['column_sizes']['middle'] = self.middle_frame.winfo_width()
        self.gui_config['column_sizes']['right'] = self.right_frame.winfo_width()
        self.gui_config = save_config(self.gui_config, CONFIG_GUI_FILE)

    def on_search_entry_change(self, event: Optional[tk.Event] = None) -> None:
        """Handles input changes in the search entry when fast search is enabled or a manual search is triggered."""
        search_query = self.search_entry.get().strip()  # Get the input from the search bar
        if search_query:  # Proceed only if there is input
            if self.fast_search:
                # Start fast search using multiprocessing
                self.result_listbox.delete(0, tk.END)
                self.search_process = multiprocessing.Process(
                    target=perform_fast_search_multiprocessing, 
                    args=(search_query, [self.right_listbox.get(i) for i in range(self.right_listbox.size())], self.result_queue)
                )
                self.search_process.start()
                self.after(100, self.process_search_results)
            else:
                # Trigger the standard search
                self.start_search()


    def on_window_resize(self, event: tk.Event) -> None:
        """Handles the resizing and movement of the window and saves the new size and position to the config file."""
        if event.widget == self:
            self.gui_config['monitor_resolution'] = self.get_currenct_resolution()

            # Save window size and position to the configuration
            self.gui_config['window_size']['width'] = self.winfo_width()
            self.gui_config['window_size']['height'] = self.winfo_height()
            self.gui_config['window_size']['x'] = self.winfo_x()
            self.gui_config['window_size']['y'] = self.winfo_y()
            self.gui_config = save_config(self.gui_config, CONFIG_GUI_FILE)


    def on_close(self) -> None:
        """Handles cleanup when the window is closed."""
        save_listbox_states(CONFIG_LISTBOX_STATE_FILE, self.left_listbox, self.right_listbox, self.result_listbox)
        self.destroy()  # Close the application


    def get_currenct_resolution(self) -> Dict[str, int]:
        """Returns the current screen resolution."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        return {'width': screen_width, 'height': screen_height}
    

