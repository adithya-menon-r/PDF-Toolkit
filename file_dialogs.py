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

def select_files_dialog():
    root = tk.Tk()
    root.withdraw()
    try:
        files = list(filedialog.askopenfilenames(
            title="Select PDF Files to Merge",
            filetypes=[("PDF Files", "*.pdf")]
        ))
        if not files:
            return None
        return files
    except Exception as e:
        print(f"Error during file selection: {e}")
        return None

def save_file_dialog():
    root = tk.Tk()
    root.withdraw()
    try:
        save_dir = filedialog.asksaveasfilename(
            title="Save PDF as",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="Merged.pdf",
            defaultextension=".pdf",
            confirmoverwrite=True
        )
        if not save_dir:
            return None
        return save_dir
    except Exception as e:
        print(f"Error during save dialog: {e}")
        return None
