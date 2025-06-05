import argparse
from importlib.metadata import version as get_version

try:
    __version__ = get_version("pdfwerks")
except Exception:
    __version__ = "unknown"


def get_parsed_args():
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
        help="Merge multiple files into one PDF (Supported: *.pdf, *.jpg, *.png, *.jpeg, *.txt)",
    )

    merge_parser.add_argument(
        "files",
        nargs="+",
        help="Paths to input files (at least 2 required)"
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
        help="Optional level of compression. Defaults to medium level",
    )

    compress_parser.add_argument(
        "-o", "--output",
        help="Optional save path. Defaults to ~/Downloads/compressed.pdf"
    )

    convert_image_parser = subparsers.add_parser(
        "convert_image",
        help="Converts any image to a PDF file (Supported: *.jpg, *.png, *.jpeg)",
    )

    convert_image_parser.add_argument(
        "file",
        nargs=1,
        help="Path to input image file"
    )

    convert_image_parser.add_argument(
        "-o", "--output",
        help="Optional save path. Defaults to ~/Downloads/converted.pdf"
    )

    extract_parser = subparsers.add_parser(
        "extract",
        help="Extract text from a PDF file and export it to one of the supported formats"
    )

    extract_parser.add_argument(
        "file",
        nargs=1,
        help="Path to input PDF file"
    )

    extract_parser.add_argument(
        "--format",
        choices=["text", "markdown", "json"],
        required=True,
        help="Required export format for extracted text. Supported: text, markdown, or json.",
    )

    extract_parser.add_argument(
        "-o", "--output",
        help="Optional save path. Defaults to ~/Downloads/extracted.[format]"
    )

    return parser.parse_args()
