import fitz
import logging
from io import BytesIO
from pathlib import Path
from .tui import ProgressBar

logging.getLogger("fitz").setLevel(logging.ERROR)


class PDFTools:
    def __init__(self):
        self.generated_file = None

    def merge(self, files):
        merged_pdf = fitz.open()

        def process_merge(pdf_path):
            pdf = fitz.open(pdf_path)
            merged_pdf.insert_pdf(pdf)
            pdf.close()

        progress = ProgressBar("Merging PDFs", files)
        progress.run(process_merge)

        self.generated_file = BytesIO()
        merged_pdf.save(self.generated_file)
        merged_pdf.close()
        self.generated_file.seek(0)

    def export(self, export_path):
        if self.generated_file is None:
            raise ValueError("No file to export.")

        export_path = Path(export_path)
        with open(export_path, "wb") as f:
            f.write(self.generated_file.read())
        return export_path
