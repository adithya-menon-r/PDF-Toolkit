import fitz
import json
import logging
import pikepdf
import pymupdf4llm
from PIL import Image
from io import BytesIO
from pathlib import Path
from rich import print as printf

from ..tui.components import ProgressBar

logging.getLogger("fitz").setLevel(logging.ERROR)


class PDFTools:
    def __init__(self):
        self.generated_file = None
    
    def _is_pdf_encrypted(self, file):
        try:
            with pikepdf.open(file):
                return False
        except pikepdf.PasswordError:
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to open PDF: {e}")
    
    def _image_to_pdf_stream(self, img_path):
        BORDER = 5
        A4_WIDTH = 595

        max_width = A4_WIDTH - 2 * BORDER

        pdf = fitz.open()
        img = Image.open(img_path)
        width_px, height_px = img.size

        dpi = img.info.get("dpi", (72, 72))
        width_pt = width_px * 72 / dpi[0]
        height_pt = height_px * 72 / dpi[1]

        if width_pt > max_width:
            scale = max_width / width_pt
            page_width = float(A4_WIDTH)
        else:
            scale = 1.0
            page_width = float(width_pt + 2 * BORDER)

        scaled_width = float(width_pt * scale)
        scaled_height = float(height_pt * scale)
        page_height = float(scaled_height + 2 * BORDER)

        page = pdf.new_page(-1, page_width, page_height)
        rect = fitz.Rect(BORDER, BORDER, BORDER + scaled_width, BORDER + scaled_height)
        page.insert_image(rect, filename=img_path)

        pdf_buffer = BytesIO()
        pdf.save(pdf_buffer)
        pdf.close()
        pdf_buffer.seek(0)
        return pdf_buffer

    def merge(self, files):
        if not files:
            raise ValueError("No files provided for merging")
        
        merged_pdf = fitz.open()

        def process_file(file_path):
            extension = Path(file_path).suffix.lower()
            try:
                if extension == ".pdf":
                    with fitz.open(file_path) as pdf:
                        merged_pdf.insert_pdf(pdf)
                elif extension in [".png", ".jpg", ".jpeg"]:
                    img_stream = self._image_to_pdf_stream(file_path)
                    with fitz.open(stream=img_stream, filetype="pdf") as img_doc:
                        merged_pdf.insert_pdf(img_doc)
                else:
                    merged_pdf.insert_file(file_path)
            except Exception as e:
                printf(f"[bold yellow]  - Skipping {file_path}: {e!r}[/bold yellow]")

        progress = ProgressBar("Merging PDFs", files)
        progress.run(process_file)
        self.generated_file = BytesIO()
        merged_pdf.save(self.generated_file)
        merged_pdf.close()
        self.generated_file.seek(0)

    def compress(self, file, level):
        level = level.lower()
        if level == "high":
            image_quality = 40
            image_resize_factor = 0.3
        elif level == "medium":
            image_quality = 60
            image_resize_factor = 0.5
        elif level == "low":
            image_quality = 80
            image_resize_factor = 0.8

        pdf = fitz.open(file)

        def process_page(page):
            for img in page.get_images(full=True):
                xref = img[0]
                extracted = pdf.extract_image(xref)
                raw = extracted["image"]

                try:
                    pil_img = Image.open(BytesIO(raw)).convert("RGB")
                except Exception:
                    continue

                new_w = max(1, int(pil_img.width * image_resize_factor))
                new_h = max(1, int(pil_img.height * image_resize_factor))
                pil_img = pil_img.resize((new_w, new_h), Image.LANCZOS)

                buffer = BytesIO()
                pil_img.save(buffer, format="JPEG", quality=image_quality)
                new_stream = buffer.getvalue()

                page.replace_image(xref, stream=new_stream)

        progress = ProgressBar("Compressing PDF", pdf)
        progress.run(process_page)
        self.generated_file = BytesIO()
        pdf.save(self.generated_file, garbage=4, deflate=True, clean=True)
        pdf.close()
        self.generated_file.seek(0)

    def convert_img_to_pdf(self, img_path):
        self.generated_file = self._image_to_pdf_stream(img_path)
    
    def extract_to_plain_text(self, file):
        pdf = fitz.open(file)
        extracted_text = ""

        def process_page(page):
            nonlocal extracted_text
            extracted_text += page.get_text() + "\n"

        progress = ProgressBar("Extracting Text", pdf)
        progress.run(process_page)

        pdf.close()
        self.generated_file = BytesIO()
        self.generated_file.write(extracted_text.encode("utf-8"))
        self.generated_file.seek(0)

    def extract_to_markdown(self, file):
        def process_file():
            md_text = pymupdf4llm.to_markdown(file)
            self.generated_file = BytesIO()
            self.generated_file.write(md_text.encode("utf-8"))
            self.generated_file.seek(0)
        
        progress = ProgressBar("Extracting Text", mode="simple")
        progress.run(process_file)
    
    def extract_to_json(self, file):
        pdf = fitz.open(file)
        all_pages_json = []

        def process_page(page):
            page_json = page.get_text("json")
            all_pages_json.append(json.loads(page_json))

        progress = ProgressBar("Extracting Text", pdf)
        progress.run(process_page)

        pdf.close()
        self.generated_file = BytesIO()
        json_text = json.dumps(all_pages_json, indent=2)
        self.generated_file.write(json_text.encode("utf-8"))
        self.generated_file.seek(0)
    
    def enable_pdf_encryption(self, file, pwd):
        if not pwd:
            raise ValueError("Password can't be empty")
        if self._is_pdf_encrypted(file):
            raise ValueError("PDF is already password protected")

        def process_file():
            try:
                with pikepdf.open(file) as pdf:
                    self.generated_file = BytesIO()
                    pdf.save(
                        self.generated_file,
                        encryption=pikepdf.Encryption(user=pwd, owner=pwd, R=4)
                    )
                    self.generated_file.seek(0)
            except pikepdf.PasswordError:
                raise ValueError("Failed to open PDF - requires password or is encrypted.")
        
        progress = ProgressBar("Enabling Password Protection", mode="simple")
        progress.run(process_file)
    
    def disable_pdf_encryption(self, file, pwd):
        if not pwd:
            raise ValueError("Password can't be empty")
        if not self._is_pdf_encrypted(file):
            raise ValueError("PDF is not password protected")

        def process_file():
            try:
                with pikepdf.open(file, password=pwd) as pdf:
                    self.generated_file = BytesIO()
                    pdf.save(self.generated_file)
                    self.generated_file.seek(0)
            except pikepdf.PasswordError:
                raise ValueError("Incorrect password or cannot decrypt PDF")

        progress = ProgressBar("Disabling Password Protection", mode="simple")
        progress.run(process_file)

    def update_pdf_password(self, file, old_pwd, new_pwd):
        if not old_pwd or not new_pwd:
            raise ValueError("Password can't be empty")
        self.disable_pdf_encryption(file, old_pwd)
        self.generated_file.seek(0)
        self.enable_pdf_encryption(self.generated_file, new_pwd)
    
    def delete_pages(self, file, pages):
        if not pages:
            raise ValueError("No pages specified for deletion")
        
        pdf = fitz.open(file)
        pages = sorted(pages, reverse=True)
        if len(pages) == len(pdf):
            raise ValueError("Cannot delete all pages")
        for page in pages:
            if page < 0 or page >= len(pdf):
                raise ValueError("Page index out of range")
            
        def process_file(index):
            pdf.delete_page(index)
        
        progress = ProgressBar("Deleting Pages", pages)
        progress.run(process_file)
        self.generated_file = BytesIO()
        pdf.save(self.generated_file)
        pdf.close()
        self.generated_file.seek(0)
        
    def export(self, export_path):
        if self.generated_file is None:
            raise ValueError("No file to export.")
        export_path = Path(export_path)
        self.generated_file.seek(0)
        with open(export_path, "wb") as f:
            f.write(self.generated_file.read())
        return export_path
