import sys
from rich import print as printf

from .arg_parse import get_parsed_args
from ..core.pdf_tools import PDFTools
from ..core.utils import validate_files, get_default_save_path, get_unique_save_path


def run_cli():
    try:
        args = get_parsed_args()

        if args.command == "merge":
            files = validate_files(args.files, allowed_extensions=[".pdf", ".jpg", ".png", ".jpeg", ".txt"])

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
            files = validate_files(args.file, allowed_extensions=[".pdf"])

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

        elif args.command == "convert_image":
            files = validate_files(args.file, allowed_extensions=[".jpg", ".png", ".jpeg"])

            if len(files) < 1:
                printf("[bold red]✗ Conversion Failed: 1 input file is required to convert.[/bold red]")
                sys.exit(1)

            save_path = get_unique_save_path(args.output or get_default_save_path("converted.pdf"))

            try:
                tool = PDFTools()
                tool.convert_img_to_pdf(files[0])
                tool.export(save_path)
                printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Conversion done! PDF saved to:[/bold #FFD580] [bold]{save_path}[/bold]\n")
            except Exception as e:
                printf(f"[bold red]✗ Conversion Failed: {e}[/bold red]")
                sys.exit(1)

    except KeyboardInterrupt:
        printf("[bold red]PDFwerks was terminated by the user!\n[/bold red]")

    except Exception as e:
        printf(f"[bold red]Unexpected Error: {e}[/bold red]")

    finally:
        printf("[bold #A3BE8C]Goodbye![/bold #A3BE8C]")
