# PDFwerks
PDFwerks is a lightweight yet comprehensive, tool for working with PDFs. It provides essential PDF manipulation tools all in one easy to use package. All operations are performed locally on your machine, ensuring your sensitive documents stay secure and private. With PDFwerks, you can finally say goodbye to uploading your documents to shady websites or paying for basic PDF operations.

[![PyPI version](https://img.shields.io/pypi/v/pdfwerks.svg)](https://pypi.org/project/pdfwerks/)
[![Publish PDFwerks](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/publish.yaml/badge.svg)](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/publish.yaml)
[![Deploy Docs](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/deploy.yaml/badge.svg)](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/deploy.yaml)
![License](https://img.shields.io/github/license/adithya-menon-r/PDFwerks)

![PDFwerks TUI](/docs/assets/TUI-Interface.png)

## Installation
You can install **PDFwerks** using `pip`:
```bash
pip install pdfwerks
```

## Usage
Run the tool directly from your terminal with:
```bash
pdfwerks
```

### Command Line Interface (CLI)
You can also use **PDFwerks** through the CLI for quick PDF operations without using the TUI.

#### Merge PDFs
```bash
pdfwerks merge file1.pdf file2.jpg [file3.pdf ...] [-o OUTPUT]
```
- Merge two or more files into one PDF. (Supported File Types: `*.pdf`, `*.jpg`, `*.png`, `*.jpeg`, `*.webp`, `*.svg`, `*.txt`)
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/merged.pdf` if not specified)

#### Compress PDFs
```bash
pdfwerks compress file.pdf [--level LEVEL] [-o OUTPUT]
```
- Compress and reduce the size of a PDF file
- Use `--level` to choose the compression strength - `low`, `medium` (default), or `high`.
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/compressed.pdf` if not specified)

#### Convert Image to PDF
```bash
pdfwerks convert_image file.jpg [-o OUTPUT]
```
- Converts any image to a PDF file (Supported File Types: `*.jpg`, `*.png`, `*.jpeg`, `*.webp`)
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/converted.pdf` if not specified)

#### Help & Version
```bash
pdfwerks --help
pdfwerks --version
```

> Note: More tools and features are in the works. 

## For Developers
If you want to test, contribute or customize the tool locally:

1. Clone the repository:

    ```bash
    git clone https://github.com/adithya-menon-r/PDFwerks.git
    cd PDFwerks
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv .venv
    .venv\Scripts\activate    # On Linux/Mac: source .venv/bin/activate
    ```

3. Install the package in editable mode:

    ```bash
    pip install -e .
    ```

You can now make changes to the code and test them without reinstalling.

## License
PDFwerks is licensed under the [MIT LICENSE](LICENSE)

## Author
PDFwerks is developed and maintained by [Adithya Menon R](https://github.com/adithya-menon-r)
