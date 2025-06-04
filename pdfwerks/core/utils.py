import sys
from pathlib import Path
from rich import print as printf

from ..tui.components import ConfirmationMenu
from ..tui.file_dialogs import select_files_dialog, save_file_dialog


def get_files(single_file=False, file_types=[("PDF Files", "*.pdf")]):
    while True:
        files = select_files_dialog(single_file, file_types)
        if files:
            return files
        if ConfirmationMenu("No files were selected. Are you sure you want to cancel?").run():
            sys.exit(1)


def get_save_path(default_file_name="processed.pdf", file_types=[("PDF Files", "*.pdf")]):
    while True:
        save_path = save_file_dialog(default_file_name, file_types)
        if save_path:
            return save_path
        if ConfirmationMenu("Save Path wasn't set. Are you sure you want to cancel?").run():
            sys.exit(1)


def get_default_save_path(default_file_name):
    downloads = Path.home() / "Downloads"
    downloads.mkdir(exist_ok=True)
    return str(downloads / default_file_name)


def validate_files(files, allowed_extensions):
    invalid_files = []
    valid_files = []

    for f in files:
        path = Path(f)
        extension = Path(f).suffix.lower()
        if not path.is_file():
            invalid_files.append(f"{f} (Not found)")
        elif extension not in allowed_extensions:
            invalid_files.append(f"{f} (File type not supported)")
        else:
            valid_files.append(f)

    if invalid_files:
        printf("[bold yellow]⚠  WARNING: Some files were ignored:[/bold yellow]")
        for msg in invalid_files:
            printf(f"   - {msg}")
        print()

    return valid_files


def get_unique_save_path(save_path):
    save_path = Path(save_path)
    if not save_path.exists():
        return save_path
    counter = 1
    while True:
        new_path = save_path.with_name(f"{save_path.stem}_{counter}{save_path.suffix}")
        if not new_path.exists():
            return new_path
        counter += 1


def get_about_text():
    return "\n".join([
        "[bold #FFAA66]PDFwerks[/bold #FFAA66] is a lightweight Python toolkit that offers simple, fast, and private PDF manipulation tools, all running locally.",
        "",
        "[bold #FFD580]✓ Merge PDFs[/bold #FFD580]",
        "[bold #FFD580]✓ Compress PDFs[/bold #FFD580]",
        "[bold #FFD580]✓ Convert Image to PDF[/bold #FFD580]",
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
