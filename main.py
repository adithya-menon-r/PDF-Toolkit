import os
from tabulate import tabulate
from termcolor import colored

from file_dialogs import select_files_dialog, save_file_dialog
from utils import display_file_order, reorder_files
from pdf_tools import PDFMerger

def clear_screen():
    os.system('cls')
    print("-----------------------------------------------------------------------------------------------------------")
    print("PDF MERGER")
    print("-----------------------------------------------------------------------------------------------------------")

def main():
    try:
        clear_screen()
        merger = PDFMerger()

        while True:
            print(tabulate([["1", "Merge PDFs"]], tablefmt="rounded_grid"))
            select_tool = input("Choose the tool \n>> ").lower().strip()
            if select_tool in ["1", "Merge  PDFs"]:
                clear_screen()
                files = select_files_dialog()
                if files is None:
                    print(colored(f"\nPROGRAM WAS TERMINATED.", "red", attrs=["bold"]))
                    return
                break
            else:
                print(colored(f"\nERROR: Invalid choice. Please choose between 1/2.\n", "red", attrs=["bold"]))

        while True:
            clear_screen()
            print(f"The {len(files)} files selected for merging will be merged in the following order: ")
            display_file_order(files)
            reorder_confirm = input(f"Press {colored("R", "blue", attrs=["bold"])} to Reorder the files or {colored("Enter", "blue", attrs=["bold"])} to merge.\n>> ")
            if reorder_confirm.lower().strip() in ["r", "reorder", "re", "y", "yes"]:
                files = reorder_files(files)
            else:
                break

        merger.merge(files)

        save_path = save_file_dialog()
        if save_path is None:
            cancel_confirm = input(f"No Save Location was selected. Press {colored("R", "blue", attrs=["bold"])} to Retry.\n>> ")
            if cancel_confirm.lower().strip() in ["r", "retry"]:
                save_path = save_file_dialog()
        
        if save_path is not None:
            merger.export(save_path)
            print(colored(f"SUCCESS! The Merged PDF File has been saved to {save_path}", "green", attrs=["bold"]))

    except KeyboardInterrupt:
        print(colored(f"\nPROGRAM WAS TERMINATED due to KeyboardInterrupt!\n", "red", attrs=["bold"]))


if __name__ == "__main__":
    main()