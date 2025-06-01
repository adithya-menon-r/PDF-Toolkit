import os
import sys
import shutil
from rich import print as printf

from pdf_tools import PDFTools
from tui import SelectionMenu, ReorderMenu
from file_dialogs import select_files_dialog, save_file_dialog

TOOL_OPTIONS = ["Merge PDFs", "Exit"]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    title = "PDF Toolkit"
    centered_title = title.center(terminal_width)
    printf(f"[bold #FFAA66  ]{centered_title}[/bold #FFAA66  ]")
    underline = "─" * terminal_width
    printf(f"[#FFECB3]{underline}[/#FFECB3]")


def main():
    try:
        clear_screen()
        tool = PDFTools()

        menu_choice = SelectionMenu("Please select one of the tools:", TOOL_OPTIONS).run()

        if menu_choice == "Merge PDFs":
            while True:
                files = select_files_dialog()
                if files is not None:
                    break
                if SelectionMenu("Are you sure you want to cancel?", ["No", "Yes"]).run() == "Yes":
                    sys.exit(1)

        elif menu_choice == "Exit":
            sys.exit(0)

        files = ReorderMenu(
            "Reorder the files if required: ",
            files
        ).run()

        tool.merge(files)

        while True:
            save_path = save_file_dialog()
            if save_path is not None:
                break
            if SelectionMenu("Are you sure you want to cancel?", ["No", "Yes"]).run() == "Yes":
                sys.exit(1)
        
        tool.export(save_path)
        printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580]Merged PDF saved to {save_path}")

    except KeyboardInterrupt:
        printf(f"[bold red]PROGRAM WAS TERMINATED due to KeyboardInterrupt!\n")

    finally:
        printf(f"[bold #A3BE8C]Goodbye!")


if __name__ == "__main__":
    main()
