# Getting Started

Haven't installed **PDFwerks**? Check the [Installation instructions](index.md#installation) to install.

## Usage via TUI
You can launch PDFwerks with a simple command:
```bash
pdfwerks
```

This opens the interactive TUI (Text User Interface), allowing you to visually select and execute operations.

<div align="center">
    <img src="https://github.com/adithya-menon-r/PDFwerks/blob/main/docs/assets/TUI-Interface.png?raw=true">
</div>

---

## Usage via CLI
You can also use PDFwerks through the Command Line Interface (CLI) for quick PDF operations.

### Merge PDFs
```bash
pdfwerks merge file1.pdf file2.jpg [file3.pdf ...] [-o OUTPUT]
```

- Merge two or more files into one PDF.

    !!! success "Supported File Types"
        You can input a mix of files - including `*.pdf`, `*.jpg`, `*.png`, `*.jpeg`, `*.webp`, `*.svg`, and `*.txt`. All non-PDF files will be automatically converted to PDF before merging, so everything works seamlessly.

    
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/merged.pdf` if not specified)

### Compress PDFs
```bash
pdfwerks compress file.pdf [--level LEVEL] [-o OUTPUT]
```

- Compress and reduce the size of a PDF file
- Use `--level` to choose the compression strength - `low`, `medium` (default), or `high`.
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/compressed.pdf` if not specified)

### Convert Image to PDF
```bash
pdfwerks convert_image file.jpg [-o OUTPUT]
```

- Converts any image to a PDF file

    !!! success "Supported File Types"
        Image files of the folowing types `*.jpg`, `*.png`, `*.jpeg` and `*.webp` are supported for conversion.

- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/converted.pdf` if not specified)

### Help
```bash
pdfwerks -h
pdfwerks --help
```

### Version
```bash
pdfwerks -v
pdfwerks --verison
```
