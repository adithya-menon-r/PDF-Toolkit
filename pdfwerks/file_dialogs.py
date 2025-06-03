import ctypes
import tkinter as tk
from tkinter import filedialog

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def select_files_dialog(single_file, file_types):
    root = tk.Tk()
    root.withdraw()
    files = None
    try:
        if single_file:
            file = filedialog.askopenfilename(
                title="Select PDF File",
                filetypes=file_types
            )
            files = [file] if file else []
        else:
            files = list(filedialog.askopenfilenames(
                title="Select PDF Files",
                filetypes=file_types
            ))
    except Exception as e:
        print(f"Error during file selection: {e}")
        files = []
    finally:
        root.destroy()
    return files


def save_file_dialog(default_file_name, file_types):
    root = tk.Tk()
    root.withdraw()
    save_path = None
    try:
        save_path = filedialog.asksaveasfilename(
            title="Save PDF as",
            filetypes=file_types,
            initialfile=default_file_name,
            defaultextension=".pdf",
            confirmoverwrite=True,
        )
    except Exception as e:
        print(f"Error during save dialog: {e}")
    finally:
        root.destroy()
    return save_path if save_path else None
