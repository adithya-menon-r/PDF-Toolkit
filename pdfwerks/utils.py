import sys
from .tui import ConfirmationMenu
from .file_dialogs import select_files_dialog, save_file_dialog


def get_files(single_file=False, file_types=[("PDF Files", "*.pdf")]):
    while True:
        files = select_files_dialog(single_file, file_types)
        if files:
            return files
        if ConfirmationMenu("No files were selected. Are you sure you want to cancel?").run():
            sys.exit(1)


def get_save_path(default_file_name="processed.pdf", file_types=[("PDF Files", "*.pdf")]):
    while True:
        save_path = save_file_dialog(default_file_name, file_types)
        if save_path:
            return save_path
        if ConfirmationMenu("Save Path wasn't set. Are you sure you want to cancel?").run():
            sys.exit(1)
