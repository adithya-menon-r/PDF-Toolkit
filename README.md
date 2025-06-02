# PDF Toolkit

PDF Toolkit is a lightweight yet comprehensive, command-line tool for working with PDFs. It provides essential PDF manipulation tools all in one easy to use package. All operations are performed locally on your machine, ensuring your sensitive documents stay secure and private. With PDF Toolkit, you can finally say goodbye to uploading your documents to shady websites or paying for basic PDF operations.

Finally got it published to **PyPI**! [Check it out on PyPI.](https://pypi.org/project/pdf-toolkit)

## Installation & Usage
You can now install **PDF Toolkit** using `pip`:
```bash
pip install pdf-toolkit
```

Once installed, run the tool from your terminal with:
```bash
pdf-toolkit
```

> Note: This project is still a work in progress. Currently, only the **`Merge PDFs`** tool is available. More tools and features like CLA based usage are in the works. 

## For Developers
If you want to test, contribute or customize the tool locally:

1. Clone the repository:

    ```bash
    git clone https://github.com/adithya-menon-r/PDF-Toolkit.git
    cd PDF-Toolkit
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
