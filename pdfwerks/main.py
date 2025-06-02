import sys
from .cli_interface import run_cli
from .tui_interface import run_tui


def main():
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_tui()


if __name__ == "__main__":
    main()
