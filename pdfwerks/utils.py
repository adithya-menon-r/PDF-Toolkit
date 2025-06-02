import sys
from .tui import SelectionMenu
from .file_dialogs import select_files_dialog, save_file_dialog


def get_files(single_file=False):
    while True:
        files = select_files_dialog(single_file)
        if files:
            return files
        if SelectionMenu("No files were selected. Are you sure you want to cancel?", ["No", "Yes"]).run() == "Yes":
            sys.exit(1)


def get_save_path():
    while True:
        save_path = save_file_dialog()
        if save_path:
            return save_path
        if SelectionMenu("Save Path wasn't set. Are you sure you want to cancel?", ["No", "Yes"]).run() == "Yes":
            sys.exit(1)
