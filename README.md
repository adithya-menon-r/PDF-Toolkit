# PDFwerks

PDFwerks is a lightweight yet comprehensive, command-line tool for working with PDFs. It provides essential PDF manipulation tools all in one easy to use package. All operations are performed locally on your machine, ensuring your sensitive documents stay secure and private. With PDFwerks, you can finally say goodbye to uploading your documents to shady websites or paying for basic PDF operations.

[![PyPI version](https://img.shields.io/pypi/v/pdfwerks.svg)](https://pypi.org/project/pdfwerks/)
[![Publish PDFwerks](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/publish.yaml/badge.svg)](https://github.com/adithya-menon-r/PDFwerks/actions/workflows/publish.yaml)
![License](https://img.shields.io/github/license/adithya-menon-r/PDFwerks)

## Installation & Usage
You can install **PDFwerks** using `pip`:
```bash
pip install pdfwerks
```

Once installed, run the tool from your terminal with:
```bash
pdfwerks
```

> Note: This project is still a work in progress. Currently, only the **`Merge PDFs`** tool is available. More tools and features like CLA based usage are in the works. 

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

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Install the package in editable mode:

    ```bash
    pip install -e .
    ```

You can now make changes to the code and test them without reinstalling.

## License
This project is licensed under the [MIT LICENSE](LICENSE)
