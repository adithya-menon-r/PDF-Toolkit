import os
import fitz
import pytest
from PIL import Image
from io import BytesIO

from pdfwerks.core.pdf_tools import PDFTools


def create_test_pdf(tmp_path, num_pages=1):
    pdf_path = tmp_path / "test.pdf"
    pdf = fitz.open()

    for _ in range(num_pages):
        page = pdf.new_page()
        img = Image.new("RGB", (800, 600), (0, 0, 0))
        img_buffer = BytesIO()
        img.save(img_buffer, format="JPEG", quality=95)
        img_buffer.seek(0)
        rect = fitz.Rect(0, 0, page.rect.width, page.rect.height)
        page.insert_image(rect, stream=img_buffer.getvalue())
    
    pdf.save(pdf_path)
    pdf.close()
    return str(pdf_path)


@pytest.fixture
def test_pdf(tmp_path):
    return create_test_pdf(tmp_path)


@pytest.fixture
def test_multipage_pdf(tmp_path):
    return create_test_pdf(tmp_path, num_pages=3)


@pytest.mark.parametrize("level", [
    ("low"),
    ("medium"),
    ("high"),
])
def test_compress_general(test_pdf, level):
    tool = PDFTools()
    tool.compress(test_pdf, level)
    assert tool.generated_file is not None
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as result:
        assert len(result) == 1
        original_size = os.path.getsize(test_pdf)
        compressed_size = len(tool.generated_file.getvalue())
        assert compressed_size < original_size


def test_compress_multipage(test_multipage_pdf):
    tool = PDFTools()
    tool.compress(test_multipage_pdf, "medium")
    assert tool.generated_file is not None
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as result:
        assert len(result) == 3
        original_size = os.path.getsize(test_multipage_pdf)
        compressed_size = len(tool.generated_file.getvalue())
        assert compressed_size < original_size


def test_compress_empty_pdf(tmp_path):
    pdf_path = tmp_path / "empty.pdf"
    pdf = fitz.open()
    pdf.new_page()
    pdf.save(pdf_path)
    pdf.close()
    
    tool = PDFTools()
    tool.compress(str(pdf_path), "medium")
    assert tool.generated_file is not None
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as result:
        assert len(result) == 1
