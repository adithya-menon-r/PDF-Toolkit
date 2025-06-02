import os
import sys
import shutil
import pyperclip
from rich import print as printf

from .pdf_tools import PDFTools
from .tui import SelectionMenu, ReorderMenu
from .utils import get_files, get_save_path

OPTIONS = ["Merge PDFs", "Exit"]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    title = "PDFwerks"
    centered_title = title.center(terminal_width)
    printf(f"[bold #FFAA66  ]{centered_title}[/bold #FFAA66  ]")
    underline = "─" * terminal_width
    printf(f"[#FFECB3]{underline}[/#FFECB3]")


def main():
    try:
        clear_screen()
        tool = PDFTools()

        menu_choice = SelectionMenu("Please select one of the tools:", OPTIONS).run()

        if menu_choice == "Merge PDFs":
            files = get_files()

        elif menu_choice == "Exit":
            sys.exit(0)

        files = ReorderMenu(
            "Reorder the files if required: (Use ↑/↓ to navigate, SPACE to select/unselect, ENTER to confirm)",
            files
        ).run()

        if len(files) < 2:
            printf(f"[red]✗[/red] [bold #FFD580] Merge Tool requires at least 2 PDFs. Only 1 was selected!\n")
            sys.exit(1)

        tool.merge(files)

        save_path = get_save_path()
                
        tool.export(save_path)
        pyperclip.copy(save_path)
        printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Merged PDF saved!\n")

    except KeyboardInterrupt:
        printf(f"[bold red]PDFwerks was terminated due to KeyboardInterrupt!\n")

    finally:
        printf(f"[bold #A3BE8C]Goodbye!")


if __name__ == "__main__":
    main()
