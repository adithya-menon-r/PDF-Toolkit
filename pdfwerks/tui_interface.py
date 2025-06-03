import os
import sys
import shutil
import pyperclip
from rich import print as printf

from .pdf_tools import PDFTools
from .tui import SelectionMenu, ReorderMenu
from .utils import get_files, get_save_path

OPTIONS = ["Merge PDFs", "Compress PDF", "About", "Exit"]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    title = "PDFwerks"
    centered_title = title.center(terminal_width)
    printf(f"[bold #FFAA66  ]{centered_title}[/bold #FFAA66  ]")
    underline = "─" * terminal_width
    printf(f"[#FFECB3]{underline}[/#FFECB3]")


def run_tui():
    try:
        clear_screen()
        tool = PDFTools()

        menu_choice = SelectionMenu("Please select one of the following:", OPTIONS).run()

        if menu_choice == "Merge PDFs":
            files = get_files()
            files = ReorderMenu(
                "Reorder the files if required: (Use ↑/↓ to navigate, SPACE to select/unselect, ENTER to confirm)",
                files,
            ).run()

            if len(files) < 2:
                printf("[bold red]✗ Merge Failed: At least 2 files are required to merge. Only 1 was selected!\n[/bold red]")
                sys.exit(1)

            tool.merge(files)
            save_path = get_save_path(default_file_name="merged.pdf")
            tool.export(save_path)
            pyperclip.copy(save_path)
            printf("[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Merged PDF saved!\n[/bold #FFD580]")
        
        elif menu_choice == "Compress PDF":
            file = get_files(single_file=True)
            level = SelectionMenu(
                "Select a compression level:",
                ["Low", "Medium", "High"],
                default_select=1
            ).run()

            tool.compress(file[0], level)
            save_path = get_save_path(default_file_name="compressed.pdf")
            tool.export(save_path)
            pyperclip.copy(save_path)
            printf("[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Compressed PDF saved!\n[/bold #FFD580]")

        elif menu_choice == "About":
            clear_screen()
            about_text = "\n".join([
                "[bold #FFAA66]PDFwerks[/bold #FFAA66] is a lightweight Python toolkit that offers simple, fast, and private PDF manipulation tools, all running locally.",
                "",
                "[bold #FFD580]✓ Merge PDFs[/bold #FFD580]",
                "[bold #FFD580]✓ Compress PDFs[/bold #FFD580]",
                "[dim]More tools coming soon![/dim]",
                "",
                "PDFwerks also supports CLI for quick operations - run [bold]pdfwerks --help[/bold] or check the docs to learn more.",
                "",
                "[bold #FFAA66]Developers & Contributions:[/bold #FFAA66]",
                "PDFwerks is open source and welcomes contributions!",
                "Repo: [link=https://github.com/adithya-menon-r/PDFwerks]adithya-menon-r/PDFwerks[/link]",
                "",
                "[bold #FFAA66]Author:[/bold #FFAA66] Adithya Menon R\n",
            ])

            printf(about_text)

        elif menu_choice == "Exit":
            sys.exit(0)

    except KeyboardInterrupt:
        printf("[bold red]PDFwerks was terminated by the user!\n[/bold red]")

    except Exception as e:
        printf(f"[bold red]Unexpected Error: {e}[/bold red]")

    finally:
        printf("[bold #A3BE8C]Goodbye![/bold #A3BE8C]")
