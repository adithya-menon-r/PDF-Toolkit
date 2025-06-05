# Getting Started

Haven't installed **PDFwerks**? Check the [Installation instructions](index.md#installation) to install.

## Usage via TUI
You can launch PDFwerks with a simple command:
```bash
pdfwerks
```

This opens the interactive TUI (Text User Interface), allowing you to visually select and execute operations.

<div align="center">
    <img src="https://raw.githubusercontent.com/adithya-menon-r/PDFwerks/refs/heads/main/docs/assets/TUI-Interface.png">
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
        You can input a mix of files - including `*.pdf`, `*.jpg`, `*.png`, `*.jpeg` and `*.txt`. All non-PDF files will be automatically converted to PDF before merging, so everything works seamlessly.

    
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
pdfwerks convert-image file.jpg [-o OUTPUT]
```

- Converts any image to a PDF file

    !!! success "Supported File Types"
        Image files of the folowing types `*.jpg`, `*.png` and `*.jpeg` are supported for conversion.

- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/converted.pdf` if not specified)

### Extract Text
```bash
pdfwerks extract file.pdf --format [text|markdown|json] [-o OUTPUT]
```

- Extract text from a PDF file and export it to the selected formats
- Use `--format` to specify the export format. This is required and must be one of: `text`, `markdown`, or `json`.

    ??? info "Curious about the `json` format?"
        The exported `json` stores not only the extracted text but their positional metadata too. This is especially useful for devs working on `OCR` or `Document processing`.

        **The general output format looks like:**
        ```json
        [
            {
                "width": 612.0, // Width of Page
                "height": 792.0, // Height of Page

                // Blocks are sections of text in a page like paragraphs, sections, etc.
                "blocks": [
                    {
                        "number": 0, // block number of the page
                        "type": 0,

                        // Bounding Box Values
                        "bbox": [
                            169.18162536621094,
                            36.8505859375,
                            456.63177490234375,
                            65.8974609375
                        ],

                        // A block can be divided into lines
                        "lines": [
                            {   
                                // A span is a continuous seq of chars that shares the same visual properties
                                "spans": [
                                    {
                                        "size": 26.0,
                                        "flags": 16,
                                        "bidi": 0,
                                        "char_flags": 24,
                                        "font": "Arial-BoldMT",
                                        "color": 0,
                                        "alpha": 255,
                                        "ascender": 0.800000011920929,
                                        "descender": -0.20000000298023224,
                                        "text": "HEADING TEXT", // Extracted text
                                        "origin": [
                                            169.18162536621094,
                                            60.3876953125
                                        ],
                                        "bbox": [
                                            169.18162536621094,
                                            36.8505859375,
                                            456.63177490234375,
                                            65.8974609375
                                        ]
                                    }
                                ],
                                "wmode": 0,
                                "dir": [
                                    1.0,
                                    0.0
                                ],
                                "bbox": [
                                    169.18162536621094,
                                    36.8505859375,
                                    456.63177490234375,
                                    65.8974609375
                                ]
                            }
                        ]
                    },
                // ... more blocks
                ]
            },
            // ... more pages
        ]
        ```

- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/extracted.[format]` if not specified)

### PDF Security

#### Enable Password Protection

```bash
pdfwerks enable-pwd file.pdf --pwd PASSWORD [-o OUTPUT]
```

- Enables password protection for a PDF file
- Use `--pwd` to specify the new password for the file. This is required.
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/encrypted.pdf` if not specified)

#### Disable Password Protection

```bash
pdfwerks disable-pwd file.pdf --pwd PASSWORD [-o OUTPUT]
```

- Disables password protection for an encrypted PDF file
- Use `--pwd` to specify the password for the encrypted PDF file. This is required.
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/decrypted.pdf` if not specified)

#### Update PDF Password

```bash
pdfwerks update-pwd file.pdf --old-pwd OLD_PASSWORD --new-pwd NEW_PASSWORD [-o OUTPUT]
```

- Updates the password for a password protected PDF file
- Use `--old-pwd` to specify the old password and `--new-pwd` to specify the new password for the PDF file. These are required.
- Use `-o` or `--output` to specify the output file path. (Defaults to `~Downloads/updated_pwd.pdf` if not specified)

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
