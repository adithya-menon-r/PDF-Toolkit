import os
import sys
import shutil
import pyperclip
from rich import print as printf

from ..core.pdf_tools import PDFTools
from .components import SelectionMenu, ReorderMenu, ConfirmationMenu
from ..core.utils import (
    get_files,
    get_save_path,
    get_about_text,
    inputf,
    parse_page_ranges,
    format_page_ranges
)

OPTIONS = [
    "Merge PDFs",
    "Compress PDF",
    "Convert Image to PDF",
    "Extract Text",
    "PDF Security",
    "Delete Pages",
    "About",
    "Exit"
]


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
            files = get_files(file_types=[("Supported Files", "*.pdf *.jpg *.png *.jpeg *.txt")])
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
                "Select a lossy compression level:",
                ["Low", "Medium", "High"],
                choice_messages=[
                    "Quality reduction is approx. 20%",
                    "Quality reduction is approx. 40%",
                    "Quality reduction is approx. 60%"
                ],
                default_select=1,
            ).run()

            tool.compress(file[0], level)
            save_path = get_save_path(default_file_name="compressed.pdf")
            tool.export(save_path)
            pyperclip.copy(save_path)
            printf("[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Compressed PDF saved!\n[/bold #FFD580]")

        elif menu_choice == "Convert Image to PDF":
            file = get_files(single_file=True, file_types=[("Image Files", "*.jpg *.png *.jpeg")])
            tool.convert_img_to_pdf(file[0])
            printf("[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Image Converted to PDF!\n[/bold #FFD580]")
            save_path = get_save_path(default_file_name="converted.pdf")
            tool.export(save_path)
            pyperclip.copy(save_path)
            printf("[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] PDF saved!\n[/bold #FFD580]")
        
        elif menu_choice == "Extract Text":
            file = get_files(single_file=True)
            extract_format = SelectionMenu(
                "Select one of the following output formats:", 
                ["Plain Text", "Markdown", "JSON"],
                choice_messages=[
                    "Extracts raw unformatted text without preserving layout",
                    "Extracts text to markdown (.md) format (experimental)",
                    "Extracts text along with positional metadata"
                ],
                default_select=1
            ).run()
            
            format_methods = {
                "Plain Text": ("extract_to_plain_text", "extracted.txt", [("Text File", "*.txt")]),
                "Markdown": ("extract_to_markdown", "extracted.md", [("Markdown File", "*.md")]),
                "JSON": ("extract_to_json", "extracted.json", [("JSON File", "*.json")])
            }
            method_name, default_file_export, file_types = format_methods[extract_format]
            getattr(tool, method_name)(file[0])
            save_path = get_save_path(default_file_name=default_file_export, file_types=file_types)
            tool.export(save_path)
            pyperclip.copy(save_path)
            printf("[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Extracted Text saved!\n[/bold #FFD580]")
                
        elif menu_choice == "PDF Security":
            file = get_files(single_file=True)
            pwd_operation = SelectionMenu(
                "Select one of the following operations:",
                ["Enable Password Protection", "Disable Password Protection", "Update PDF Password"],
                default_select=1
            ).run()

            if pwd_operation == "Enable Password Protection":
                pwd = inputf("Enter a password for the PDF:")
                tool.enable_pdf_encryption(file[0], pwd)
            elif pwd_operation == "Disable Password Protection":
                pwd = inputf("Enter the password to the PDF:")
                tool.disable_pdf_encryption(file[0], pwd)
            elif pwd_operation == "Update PDF Password":
                old_pwd = inputf("Enter the old password for the PDF:")
                new_pwd = inputf("Enter the new password for the PDF:")
                tool.update_pdf_password(file[0], old_pwd, new_pwd)

            save_path = get_save_path(default_file_name="processed.pdf")
            tool.export(save_path)
            pyperclip.copy(save_path)
            printf("[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Processed File Saved!\n[/bold #FFD580]")
        
        elif menu_choice == "Delete Pages":
            file = get_files(single_file=True)
            pages = inputf("Enter the page numbers to delete (e.g: 2,5-8,21,30):")
            parsed_pages = parse_page_ranges(pages, file[0])
            if not ConfirmationMenu(f"Are you sure you want to delete the pages - {format_page_ranges(parsed_pages)}?").run():
                sys.exit(1)
                
            tool.delete_pages(file[0], parsed_pages)
            save_path = get_save_path(default_file_name="deleted.pdf")
            tool.export(save_path)
            pyperclip.copy(save_path)
            printf("[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Processed PDF Saved!\n[/bold #FFD580]")

        elif menu_choice == "About":
            clear_screen()
            printf(get_about_text())

        elif menu_choice == "Exit":
            sys.exit(0)

    except KeyboardInterrupt:
        printf("[bold red]PDFwerks was terminated by the user!\n[/bold red]")

    except Exception as e:
        printf(f"[bold red]Unexpected Error: {e}[/bold red]")

    finally:
        printf("[bold #A3BE8C]Goodbye![/bold #A3BE8C]")
