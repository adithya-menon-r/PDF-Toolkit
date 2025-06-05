# PDFwerks

**PDFwerks** is a lightweight yet comprehensive tool for working with PDFs directly from your terminal. It provides essential PDF manipulation tools all in one easy to use package

> **Why PDFwerks?**  
> Well, a few months ago, I needed to merge some important stuff like my Aadhaar and other IDs. I used the usual online tools, but it got me thinking, "Who even knows what happens to my files after I upload them?" That’s when I decided to build PDFwerks - a local tool that keeps your documents safe and under your control.
---

[![PyPI version](https://img.shields.io/pypi/v/pdfwerks.svg)](https://pypi.org/project/pdfwerks/)
[![Publish PDFwerks](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/publish.yaml/badge.svg)](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/publish.yaml)
[![Deploy Docs](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/deploy.yaml/badge.svg)](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/deploy.yaml)
[![Run pytest](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/test.yaml/badge.svg)](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/test.yaml)
![License](https://img.shields.io/github/license/adithya-menon-r/PDFwerks)

## Tools Available

- ✅ Merge PDFs, images, and text files into a single PDF  
- ✅ Compress PDFs with three adjustable compression levels  
- ✅ Convert images to a PDF  
- ✅ Extract text from a PDF to plain text, markdown or json 

> _**More tools coming soon!**_

!!! success "No uploads required"
    All operations happen **locally on your machine**, ensuring your sensitive documents stay secure and private. No shady websites. No dumb paid subscriptions.

## Installation

Install via `pip`:

```bash
pip install pdfwerks
```

And that's it, you're good to go! Check out the [Getting Started guide](getting-started.md) to learn how to use PDFwerks.

???+ info "For Devs: Installation & Setup"

    Follow these steps to test, contribute, or customize PDFwerks locally:

    1. **Clone the repository:**

        ```bash
        git clone https://github.com/adithya-menon-r/PDFwerks.git
        cd PDFwerks
        ```

    2. **Create a virtual environment and activate it:**

        ```bash
        python -m venv .venv
        .venv\Scripts\activate    # On Linux/Mac: source .venv/bin/activate
        ```

    3. **Install dependencies and the package in editable mode:**

        ```bash
        pip install -e .
        ```

    Depending on what you are working on, you can install extras as needed:

    - **For tests**

        ```bash
        pip install -e .[test]
        ```

    - **For documentation**

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

PDFwerks is licensed under the [MIT License](https://github.com/adithya-menon-r/PDFwerks/blob/main/LICENSE)
