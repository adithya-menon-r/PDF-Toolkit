import os
import sys
import ctypes
import argparse
import tkinter
import pyperclip

from pathlib import Path
from tkinter import filedialog
from pypdf import PdfWriter
from termcolor import colored
from tabulate import tabulate
from multipledispatch import dispatch

writer = PdfWriter()
DEFAULT_SAVE_PATH = Path.home() / "Downloads"


def clr_scr():
    os.system('cls' if os.name == "nt" else 'clear')
    print("-----------------------------------------------------------------------------------------------------------")
    print("PDF MERGER")
    print("-----------------------------------------------------------------------------------------------------------")


def clean_and_validate_path(file_path):
    file_path = file_path.replace("\"", "")
    file_path = file_path.replace("/", "\\")
    if file_path.endswith("\\"):
        file_path = file_path[:-1]
    if not file_path.endswith(".pdf") or not Path(file_path).exists():
        print(colored("ERROR: Invalid file path. File does not exist / Wrong File Type.", "red", attrs=["bold"]))
        return None
    return file_path


def get_files_via_paths():
    files = []
    while True:
        try:
            num_files = int(input("Number of files to Merge: "))
            if num_files > 1:
                print()
                break
            else:
                print(colored("ERROR: Insufficient number of Files. Please enter an integer greater than 1.\n", "red", attrs=["bold"]))
        except ValueError:
            print(colored("ERROR: Invalid input. Please enter a valid integer greater than 1.\n", "red", attrs=["bold"]))
    for i in range(num_files):
        while True:
            if file_path := clean_and_validate_path(input(f"Enter the file path for File {i + 1}: ").strip()):
                break
        files.append(file_path)
    return files


def get_files_via_gui():
    while True:
        root = tkinter.Tk()
        root.withdraw()
        files = list(filedialog.askopenfilenames(title="Select PDFs to Merge", filetypes=[("PDF Files", "*.pdf")]))
        if len(files) > 1:
            break
        else:
            print(colored("ERROR: Insufficient number of Files. Please select at least two PDF files.\n", "red", attrs=["bold"]))
            retry_confirm = input(f"Press {colored("Q", "blue", attrs=["bold"])} to Quit or {colored("Enter", "blue", attrs=["bold"])} to select files again.\n>> ")
            if retry_confirm.lower().strip() in ["q", "quit"]:
                return None
    return files


def display_file_order(files):
    file_order = [
        {"No.": i+1, "File Name": Path(file_path).parts[-1]} for i, file_path in enumerate(files)
    ]
    print(tabulate(file_order, headers="keys", tablefmt="rounded_grid"))


def reorder_files(files):
    while True:
        try:
            new_order = input("\nEnter the file numbers in the required order (seperated by ',' or ' ').\n>> ").strip()
            new_order = new_order.replace("\"", "")
            order_index = new_order.split(",") if "," in new_order else new_order.split()
            if len(order_index) != len(set(order_index)) != len(files):
                raise IndexError
            reordered_files = [files[int(index) - 1] for index in order_index]
            break
        except (ValueError, IndexError):
            print(colored(f"ERROR: Invalid Order. Reordering couldn't be processed. Try typing the order like \"5,2,1,3,4\".", "red", attrs=["bold"]))
    return reordered_files


def merge(files):
    print("\nWorking on it...")
    for i, pdf in enumerate(files):
        writer.append(pdf)
        print(colored(f"{i+1} Done!", "blue", attrs=["bold"]))


@dispatch()
def get_export_path():
    while True:
        if not (export_name := input("\nEnter Name of Merged File: ").strip()):
            print(colored("ERROR: Merged file name cannot be empty.", "red", attrs=["bold"]))
            continue
        if not export_name.endswith(".pdf"):
            export_name = export_name + ".pdf"
        export_path = DEFAULT_SAVE_PATH / export_name
        if Path(export_path).exists():
            overwrite_confirm = input("File with same name already exists! Do you want to overwrite it (yes/no)? ")
            if overwrite_confirm.lower().strip() in ["y", "yes", "overwrite"]:
                return export_path
        else:
            return export_path


@dispatch(str)
def get_export_path(export_name):
    if not export_name.endswith(".pdf"):
        export_name = export_name + ".pdf"
    export_path = DEFAULT_SAVE_PATH / export_name
    if Path(export_path).exists():
        print(colored("Unable to save File! File already exists in destination folder.", "red", attrs=["bold"]))
        sys.exit(1)
    return export_path


def export(export_path):
    if not export_path.parent.exists():
        print("\nCreating Directory...")
        export_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        print()
    print("Saving the Merged File...")
    writer.write(export_path)
    writer.close()
    return export_path


def args_merge(files, export_name="merged files.pdf"):
    for i, file_path in enumerate(files):
        if file_path := clean_and_validate_path(file_path):
            files[i] = file_path
        else:
            sys.exit(1)
    merge(files)
    save_path = export(get_export_path(export_name))
    pyperclip.copy(str(save_path))
    print(colored(f"SUCCESS! The Merged PDF File has been saved to {save_path}", "green", attrs=["bold"]))
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--merge", type=str, nargs=2, help="Provide two file paths (in quotes) to the PDFs you want to merge.")
    parser.add_argument("--fileName", type=str, help="Enter the custom name for the merged PDF. If omitted, 'merged files.pdf' will be used.")
    args = parser.parse_args()
    if args.merge:
        args_merge(args.merge, args.fileName) if args.fileName else args_merge(args.merge)

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    try:
        clr_scr()
        while True:
            print(tabulate([["1", "Command Line Interface (CLI)"], ["2", "Graphical User Interface (GUI)"]], tablefmt="rounded_grid"))
            select_files_ui = input("Choose the preferred UI to select Files. \n>> ").lower().strip()
            if select_files_ui in ["cli", "1", "command", "command line interface"]:
                clr_scr()
                files = get_files_via_paths()
                break
            elif select_files_ui in ["gui", "2", "graphics", "graphical user interface"]:
                files = get_files_via_gui()
                if files is None:
                    print(colored(f"\nPROGRAM WAS TERMINATED by the User.", "red", attrs=["bold"]))
                    return
                break
            else:
                print(colored(f"\nERROR: Invalid choice. Please choose between 1/2.\n", "red", attrs=["bold"]))

        while True:
            clr_scr()
            print(f"The {len(files)} files selected for merging will be merged in the following order: ")
            display_file_order(files)
            reorder_confirm = input(f"Press {colored("R", "blue", attrs=["bold"])} to Reorder the files or {colored("Enter", "blue", attrs=["bold"])} to merge.\n>> ")
            if reorder_confirm.lower().strip() in ["r", "reorder", "re", "y", "yes"]:
                files = reorder_files(files)
            else:
                break

        merge(files)

        save_path = export(get_export_path())
        pyperclip.copy(str(save_path))
        print(colored(f"SUCCESS! The Merged PDF File has been saved to {save_path}", "green", attrs=["bold"]))

    except KeyboardInterrupt:
        print(colored(f"\nPROGRAM WAS TERMINATED due to KeyboardInterrupt!\n", "red", attrs=["bold"]))


if __name__ == '__main__':
    main()
