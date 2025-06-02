import sys
from .tui import SelectionMenu
from .file_dialogs import select_files_dialog, save_file_dialog


def get_files():
    while True:
        files = select_files_dialog()
        if files is not None:
            break
        if SelectionMenu("No files were selected. Are you sure you want to cancel?", ["No", "Yes"]).run() == "Yes":
            sys.exit(1)
    return files


def get_save_path():
    while True:
        save_path = save_file_dialog()
        if save_path is not None:
            break
        if SelectionMenu("Save Path wasn't set. Are you sure you want to cancel?", ["No", "Yes"]).run() == "Yes":
            sys.exit(1)
    return save_path
