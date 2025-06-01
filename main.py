import os
import pyperclip
from tabulate import tabulate
from termcolor import colored

from gui import select_files_ui, save_file_ui
from utils import display_file_order, reorder_files
from tools import merge, export

def clear_screen():
    os.system('cls')
    print("-----------------------------------------------------------------------------------------------------------")
    print("PDF MERGER")
    print("-----------------------------------------------------------------------------------------------------------")

def main():
    try:
        clear_screen()
        while True:
            print(tabulate([["1", "Merge PDFs"]], tablefmt="rounded_grid"))
            select_tool = input("Choose the tool \n>> ").lower().strip()
            if select_tool in ["1", "Merge  PDFs"]:
                clear_screen()
                files = select_files_ui()
                if files is None:
                    print(colored(f"\nPROGRAM WAS TERMINATED by the User.", "red", attrs=["bold"]))
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

        merge(files)

        save_path = export(save_file_ui())
        pyperclip.copy(str(save_path))
        print(colored(f"SUCCESS! The Merged PDF File has been saved to {save_path}", "green", attrs=["bold"]))

    except KeyboardInterrupt:
        print(colored(f"\nPROGRAM WAS TERMINATED due to KeyboardInterrupt!\n", "red", attrs=["bold"]))


if __name__ == "__main__":
    main()