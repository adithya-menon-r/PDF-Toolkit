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


def get_default_save_path(file_name):
    downloads = Path.home() / "Downloads"
    downloads.mkdir(exist_ok=True)
    return str(downloads / file_name)


def validate_pdf_files(files):
    invalid_files = []
    valid_files = []

    for f in files:
        path = Path(f)
        if not path.is_file():
            invalid_files.append(f"{f} (Not found)")
        elif not f.lower().endswith(".pdf"):
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


def run_cli():
    try:
        parser = argparse.ArgumentParser(
            prog="pdfwerks",
            description="A lightweight Python toolkit with multiple tools for PDF manipulation",
            epilog="License: MIT\nRepo: https://github.com/adithya-menon-r/PDFwerks",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        parser.add_argument(
            "-v", "--version",
            action="version",
            version=f"%(prog)s {__version__}",
            help="show the version number and exit",
        )

        subparsers = parser.add_subparsers(dest="command", required=True)

        merge_parser = subparsers.add_parser(
            "merge",
            help="Merge multiple PDF files into one"
        )

        merge_parser.add_argument(
            "files",
            nargs="+",
            help="Paths to input PDF files (at least 2 required)"
        )

        merge_parser.add_argument(
            "-o", "--output",
            help="Optional save path. Defaults to ~/Downloads/merged.pdf"
        )

        compress_parser = subparsers.add_parser(
            "compress",
            help="Compress and reduce the size of a PDF file"
        )

        compress_parser.add_argument(
            "file",
            nargs=1,
            help="Path to input PDF file"
        )

        compress_parser.add_argument(
            "--level",
            choices=["low", "medium", "high"],
            default="medium",
            help="Optional level of compression. Choices are: low, medium, high. Defaults to medium"
        )

        compress_parser.add_argument(
            "-o", "--output",
            help="Optional save path. Defaults to ~/Downloads/compressed.pdf"
        )

        args = parser.parse_args()

        if args.command == "merge":
            files = validate_pdf_files(args.files)

            if len(files) < 2:
                printf("[bold red]✗ Merge Failed: At least 2 input files are required to merge.[/bold red]")
                sys.exit(1)

            save_path = get_unique_save_path(args.output or get_default_save_path("merged.pdf"))

            try:
                tool = PDFTools()
                tool.merge(files)
                tool.export(save_path)
                printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Merged PDF saved to:[/bold #FFD580] [bold]{save_path}[/bold]\n")
            except Exception as e:
                printf(f"[bold red]✗ Merge Failed: {e}[/bold red]")
                sys.exit(1)

        elif args.command == "compress":
            files = validate_pdf_files(args.file)

            if len(files) < 1:
                printf("[bold red]✗ Compression Failed: 1 input file is required to compress.[/bold red]")
                sys.exit(1)

            save_path = get_unique_save_path(args.output or get_default_save_path("compressed.pdf"))

            try:
                tool = PDFTools()
                tool.compress(files[0], args.level)
                tool.export(save_path)
                printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Compressed PDF saved to:[/bold #FFD580] [bold]{save_path}[/bold]\n")
            except Exception as e:
                printf(f"[bold red]✗ Compression Failed: {e}[/bold red]")
                sys.exit(1)

    except KeyboardInterrupt:
        printf("[bold red]PDFwerks was terminated by the user!\n[/bold red]")

    except Exception as e:
        printf(f"[bold red]Unexpected Error: {e}[/bold red]")

    finally:
        printf("[bold #A3BE8C]Goodbye![/bold #A3BE8C]")
