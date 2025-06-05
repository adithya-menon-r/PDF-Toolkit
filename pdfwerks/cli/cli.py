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

        elif args.command == "convert-image":
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
        
        elif args.command == "extract":
            files = validate_files(args.file, allowed_extensions=[".pdf"])

            if len(files) < 1:
                printf("[bold red]✗ Extraction Failed: 1 input file is required to extract.[/bold red]")
                sys.exit(1)

            format = args.format
            extensions = {
                "text": "txt",
                "markdown": "md",
                "json": "json"
            }
            save_path = get_unique_save_path(args.output or get_default_save_path(f"extracted.{extensions[format]}"))

            try:
                tool = PDFTools()
                if format == "text":
                    tool.extract_to_text(files[0])
                elif format == "markdown":
                    tool.extract_to_markdown(files[0])
                elif format == "json":
                    tool.extract_to_json(files[0])
                else:
                    printf(f"[bold red]✗ Unknown format: {format}[/bold red]")
                    sys.exit(1)

                tool.export(save_path)
                printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Extracted file saved to:[/bold #FFD580] [bold]{save_path}[/bold]\n")
            except Exception as e:
                printf(f"[bold red]✗ Extraction Failed: {e}[/bold red]")
                sys.exit(1)
                
        elif args.command == "disable-pwd":
            files = validate_files(args.file, allowed_extensions=[".pdf"])

            if len(files) < 1:
                printf("[bold red]✗ Disabling Password Protection Failed: 1 input file is required.[/bold red]")
                sys.exit(1)

            save_path = get_unique_save_path(args.output or get_default_save_path("decrypted.pdf"))

            try:
                tool = PDFTools()
                tool.disable_pdf_encryption(files[0], args.pwd)
                tool.export(save_path)
                printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Decrypted PDF saved to:[/bold #FFD580] [bold]{save_path}[/bold]\n")
            except Exception as e:
                printf(f"[bold red]✗ Decryption Failed: {e}[/bold red]")
                sys.exit(1)

        elif args.command == "enable-pwd":
            files = validate_files(args.file, allowed_extensions=[".pdf"])

            if len(files) < 1:
                printf("[bold red]✗ Enabling Password Protection Failed: 1 input file is required.[/bold red]")
                sys.exit(1)

            save_path = get_unique_save_path(args.output or get_default_save_path("encrypted.pdf"))

            try:
                tool = PDFTools()
                tool.enable_pdf_encryption(files[0], args.pwd)
                tool.export(save_path)
                printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Encrypted PDF saved to:[/bold #FFD580] [bold]{save_path}[/bold]\n")
            except Exception as e:
                printf(f"[bold red]✗ Encryption Failed: {e}[/bold red]")
                sys.exit(1)

        elif args.command == "update-pwd":
            files = validate_files(args.file, allowed_extensions=[".pdf"])

            if len(files) < 1:
                printf("[bold red]✗ Updating PDF Password Failed: 1 input file is required.[/bold red]")
                sys.exit(1)

            save_path = get_unique_save_path(args.output or get_default_save_path("updated_pwd.pdf"))

            try:
                tool = PDFTools()
                tool.update_pdf_password(files[0], args.old_pwd, args.new_pwd)
                tool.export(save_path)
                printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] Password updated PDF saved to:[/bold #FFD580] [bold]{save_path}[/bold]\n")
            except Exception as e:
                printf(f"[bold red]✗ PDF Password Updation Failed: {e}[/bold red]")
                sys.exit(1)
        
    except KeyboardInterrupt:
        printf("[bold red]PDFwerks was terminated by the user!\n[/bold red]")

    except Exception as e:
        printf(f"[bold red]Unexpected Error: {e}[/bold red]")

    finally:
        printf("[bold #A3BE8C]Goodbye![/bold #A3BE8C]")
