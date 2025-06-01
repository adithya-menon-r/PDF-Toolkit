from io import BytesIO
from pathlib import Path
from pypdf import PdfWriter
from termcolor import colored

class PDFMerger:
    def __init__(self):
        self.generated_file = None

    def merge(self, files):
        writer = PdfWriter()
        print("\nWorking on it...")
        for i, pdf in enumerate(files):
            writer.append(pdf)
            print(colored(f"{i+1} Done!", "blue", attrs=["bold"]))
        self.generated_file = BytesIO()
        writer.write(self.generated_file)
        self.generated_file.seek(0)

    def export(self, export_path):
        if self.generated_file is None:
            raise ValueError("No file to export.")

        export_path = Path(export_path)
        print()
        with open(export_path, "wb") as f:
            f.write(self.generated_file.read())
        return export_path
