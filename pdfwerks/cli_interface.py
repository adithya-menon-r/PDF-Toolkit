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
        if len(args.input_files) < 2:
            printf("[bold red]✗ Merge Failed: At least 2 input files are required to merge.[/bold red]")
            sys.exit(1)

        save_path = args.output or get_default_save_path()

        try:
            tool = PDFTools()
            tool.merge(args.input_files)
            tool.export(save_path)
            printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Merged PDF saved to:[/bold #FFD580] [bold]{save_path}[/bold]")
        except Exception as e:
            printf(f"[bold red]✗ Merge Failed: {e}[/bold red]")
            sys.exit(1)
