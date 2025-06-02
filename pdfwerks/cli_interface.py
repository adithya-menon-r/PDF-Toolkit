import sys
import argparse
from pathlib import Path
from rich import print as printf
from importlib.metadata import version as get_version

from .pdf_tools import PDFTools

try:
    __version__ = get_version("pdfwerks")
except Exception:
    __version__ = "unknown"


def get_default_save_path():
    downloads = Path.home() / "Downloads"
    downloads.mkdir(exist_ok=True)
    return str(downloads / "merged.pdf")


def validate_pdf_files(files):
    invalid_files = []
    valid_files = []

    for f in files:
        path = Path(f)
        if not path.is_file():
            invalid_files.append(f"{f} (Not Found)")
        elif not f.lower().endswith(".pdf"):
            invalid_files.append(f"{f} (Not a Valid PDF)")
        else:
            valid_files.append(f)

    if invalid_files:
        printf("[bold yellow]⚠  Warning: Some files were ignored:[/bold yellow]")
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


def run_cli():
    parser = argparse.ArgumentParser(
        prog="pdfwerks",
        description="A lightweight Python toolkit with multiple tools for PDF manipulation",
        epilog="License: MIT\nRepo: https://github.com/adithya-menon-r/PDFwerks",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="show the version number and exit"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    merge_parser = subparsers.add_parser(
        "merge",
        help="Merge multiple PDF files into one"
    )

    merge_parser.add_argument(
        "input_files",
        nargs="+",
        help="Paths to input PDF files (at least 2 required)"
    )

    merge_parser.add_argument(
        "-o", "--output",
        help="Optional save path. Defaults to ~/Downloads/merged.pdf"
    )

    args = parser.parse_args()

    if args.command == "merge":
        files = validate_pdf_files(args.input_files)

        if len(files) < 2:
            printf("[bold red]✗ Merge Failed: At least 2 input files are required to merge.[/bold red]")
            sys.exit(1)

        save_path = args.output or get_default_save_path()
        save_path = get_unique_save_path(save_path)

        try:
            tool = PDFTools()
            tool.merge(files)
            tool.export(save_path)
            printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Merged PDF saved to:[/bold #FFD580] [bold]{save_path}[/bold]")
        except Exception as e:
            printf(f"[bold red]✗ Merge Failed: {e}[/bold red]")
            sys.exit(1)
