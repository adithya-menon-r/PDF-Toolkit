# PDFwerks
PDFwerks is a lightweight yet comprehensive, tool for working with PDFs. It provides essential PDF manipulation tools all in one easy to use package. All operations are performed locally on your machine, ensuring your sensitive documents stay secure and private. With PDFwerks, you can finally say goodbye to uploading your documents to shady websites or paying for basic PDF operations.

[![PyPI version](https://img.shields.io/pypi/v/pdfwerks.svg)](https://pypi.org/project/pdfwerks/)
[![Publish PDFwerks](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/publish.yaml/badge.svg)](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/publish.yaml)
[![Deploy Docs](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/deploy.yaml/badge.svg)](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/deploy.yaml)
[![Run pytest](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/test.yaml/badge.svg)](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/test.yaml)
![License](https://img.shields.io/github/license/adithya-menon-r/PDFwerks)

![PDFwerks TUI](/docs/assets/TUI-Interface.png)

## Documentation
Check out the `official documentation` here: [PDFwerks Documentation](https://adithya-menon-r.github.io/PDFwerks). It's more detailed and well I put a lot of effort, so go see it :)

## Cross Platform Support
**PDFwerks** is a cross platform PDF toolkit and works across all major operating systems.

It has been **locally tested and verified on both Ubuntu (including WSL2) and Windows**. Additionally, **Continuous Integration (CI) tests are run on Windows, macOS, and Ubuntu**, ensuring core functionality remains stable across environments.

> ⚠️ **Important:** `tkinter` is a required dependency for PDFwerks. For OS specific installation instructions, see the [PDFwerks Documentation](https://adithya-menon-r.github.io/PDFwerks)

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
- Merge two or more files into one PDF. (Supported File Types: `*.pdf`, `*.jpg`, `*.png`, `*.jpeg`, `*.txt`)
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
pdfwerks convert-image file.jpg [-o OUTPUT]
```
- Converts any image to a PDF file (Supported File Types: `*.jpg`, `*.png`, `*.jpeg`)
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/converted.pdf` if not specified)

#### Extract Text
```bash
pdfwerks extract file.pdf --format [text|markdown|json] [-o OUTPUT]
```
- Extract text from a PDF file and export it to the selected formats
- Use `--format` to specify the export format. This is required and must be one of: `text`, `markdown`, or `json`.
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/extracted.[format]` if not specified)

#### PDF Security

##### Enable Password Protection
```bash
pdfwerks enable-pwd file.pdf --pwd PASSWORD [-o OUTPUT]
```
- Enables password protection for a PDF file
- Use `--pwd` to specify the new password for the file. This is required.
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/encrypted.pdf` if not specified)

##### Disable Password Protection
```bash
pdfwerks disable-pwd file.pdf --pwd PASSWORD [-o OUTPUT]
```
- Disables password protection for an encrypted PDF file
- Use `--pwd` to specify the password for the encrypted PDF file. This is required.
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/decrypted.pdf` if not specified)

##### Update PDF Password
```bash
pdfwerks update-pwd file.pdf --old-pwd OLD_PASSWORD --new-pwd NEW_PASSWORD [-o OUTPUT]
```
- Updates the password for a password protected PDF file
- Use `--old-pwd` to specify the old password and `--new-pwd` to specify the new password for the PDF file. These are required.
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/updated_pwd.pdf` if not specified)

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

3. Install dependencies and the package in editable mode:

    ```bash
    pip install -e .
    ```

### Optional Dependencies
Depending on what you are working on, you can install extras as needed:
- For **tests**

    ```bash
    pip install -e .[test]
    ```

- For **documentation**

    ```bash
    pip install -e .[docs]
    ```

You can now make changes to the code, run tests, or build documentation without reinstalling the package.

## Running Tests
Once test dependencies are installed (using `pip install -e .[test]`), you run the full test suite with:

```bash
pytest
```

All test files are located in the `tests/` directory and are automatically discovered by `pytest`.

## License
PDFwerks is licensed under the [MIT LICENSE](LICENSE)

## Author
PDFwerks is developed and maintained by [Adithya Menon R](https://github.com/adithya-menon-r)
