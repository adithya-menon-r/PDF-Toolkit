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

def select_files_ui():
    root = tk.Tk()
    root.withdraw()
    files = list(filedialog.askopenfilenames(
        title="Select PDF Files to Merge",
        filetypes=[("PDF Files", "*.pdf")])
    )
    return files

def save_file_ui():
    root = tk.Tk()
    root.withdraw()
    save_dir = filedialog.asksaveasfilename(
        title="Save Merged PDF as",
        filetypes=[("PDF Files", "*.pdf")],
        initialfile="Merged.pdf",
        defaultextension = [("PDF Files", "*.pdf")],
        confirmoverwrite=True
    )
    return save_dir
