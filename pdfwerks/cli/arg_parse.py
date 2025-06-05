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

    # Merge Command ------------------------------------------------------------------
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

    # Compress Command ------------------------------------------------------------------
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

    # Convert Image to PDF Command ------------------------------------------------------------------
    convert_image_parser = subparsers.add_parser(
        "convert-image",
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

    # Text Extraction Command ------------------------------------------------------------------
    extract_parser = subparsers.add_parser(
        "extract",
        help="Extract text from a PDF file and export it to the selected formats"
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

    # PDF Security - Enable Pwd Command ------------------------------------------------------------------
    enable_pwd = subparsers.add_parser(
        "enable-pwd",
        help="Enables password protection for a PDF file"
    )

    enable_pwd.add_argument(
        "file",
        nargs=1,
        help="Path to input PDF file"
    )

    enable_pwd.add_argument(
        "--pwd",
        required=True,
        help="Required new password for the PDF file",
    )

    enable_pwd.add_argument(
        "-o", "--output",
        help="Optional save path. Defaults to ~/Downloads/encrypted.pdf"
    )

    # PDF Security - Disable Pwd Command ------------------------------------------------------------------
    disable_pwd = subparsers.add_parser(
        "disable-pwd",
        help="Disables password protection for an encrypted PDF file"
    )

    disable_pwd.add_argument(
        "file",
        nargs=1,
        help="Path to input encrypted PDF file"
    )

    disable_pwd.add_argument(
        "--pwd",
        required=True,
        help="Required password for the encrypted PDF file",
    )

    disable_pwd.add_argument(
        "-o", "--output",
        help="Optional save path. Defaults to ~/Downloads/decrypted.pdf"
    )

    # PDF Security - Update Pwd Command ------------------------------------------------------------------
    update_pwd = subparsers.add_parser(
        "update-pwd",
        help="Updates the password for a password protected PDF file"
    )

    update_pwd.add_argument(
        "file",
        nargs=1,
        help="Path to input password protected PDF file"
    )

    update_pwd.add_argument(
        "--old-pwd",
        required=True,
        help="Required old password for the PDF file",
    )

    update_pwd.add_argument(
        "--new-pwd",
        required=True,
        help="Required new password for the PDF file",
    )

    update_pwd.add_argument(
        "-o", "--output",
        help="Optional save path. Defaults to ~/Downloads/updated_pwd.pdf"
    )

    return parser.parse_args()
