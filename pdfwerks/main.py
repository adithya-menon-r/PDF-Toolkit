import sys
import warnings
from rich import print as printf

from .cli_interface import run_cli
from .tui_interface import run_tui

deprecation_msg = (
    "PDFwerks will switch its core dependency from [bold]PyPDF[/bold] to [bold]PyMuPDF[/bold] in version [bold green]1.0.0[/bold green].\n"
    "This version is now considered [bold red]deprecated[/bold red], and its behaviour may differ from future releases.\n"
    "Please test your workflows accordingly and refer to the repo/docs for more info."
)
printf(f"[bold yellow]⚠ Deprecation Notice[/bold yellow]\n[yellow]{deprecation_msg}\n[/yellow]")
warnings.warn(
    "This version of PDFwerks is deprecated due to the upcoming switch in core dependency in version 1.0.0.",
    DeprecationWarning,
    stacklevel=2
)

def main():
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_tui()


if __name__ == "__main__":
    main()
