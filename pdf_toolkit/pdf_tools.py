import logging
from io import BytesIO
from pathlib import Path
from pypdf import PdfWriter
from .tui import ProgressBar

logging.getLogger("pypdf").setLevel(logging.ERROR)

class PDFTools:
    def __init__(self):
        self.generated_file = None

    def merge(self, files):
        writer = PdfWriter()

        def process_merge(pdf):
            writer.append(pdf)

        progress = ProgressBar("Merging PDFs", files)
        progress.run(process_merge)

        self.generated_file = BytesIO()
        writer.write(self.generated_file)
        self.generated_file.seek(0)

    def export(self, export_path):
        if self.generated_file is None:
            raise ValueError("No file to export.")

        export_path = Path(export_path)
        with open(export_path, "wb") as f:
            f.write(self.generated_file.read())
        return export_path
