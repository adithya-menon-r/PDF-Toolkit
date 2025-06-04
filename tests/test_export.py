import fitz
import pytest
from pathlib import Path
from io import BytesIO
import os
from PIL import Image

from pdfwerks.core.pdf_tools import PDFTools


def create_test_pdf():
    pdf = fitz.open()
    page = pdf.new_page()
    page.insert_text((100, 100), "Just adding some content in Test PDF")
    buffer = BytesIO()
    pdf.save(buffer)
    pdf.close()
    buffer.seek(0)
    return buffer


@pytest.fixture
def tool_with_pdf():
    tool = PDFTools()
    tool.generated_file = create_test_pdf()
    return tool


def test_export_general(tool_with_pdf, tmp_path):
    export_path = tmp_path / "exported.pdf"
    result_path = tool_with_pdf.export(str(export_path))
    assert result_path == export_path
    assert export_path.exists()
    assert export_path.stat().st_size > 0
    with fitz.open(export_path) as pdf:
        assert len(pdf) == 1
        assert "Just adding some content in Test PDF" in pdf[0].get_text()


def test_export_no_content():
    tool = PDFTools()
    with pytest.raises(ValueError, match="No file to export"):
        tool.export("test.pdf")


def test_export_large_file(tool_with_pdf, tmp_path):
    pdf = fitz.open()
    for _ in range(50):
        page = pdf.new_page()
        page.insert_text((100, 100), "Adding some test PDF content" * 1000)
        img = Image.new("RGB", (800, 600), (255, 255, 255))
        img_buffer = BytesIO()
        img.save(img_buffer, format="JPEG", quality=95)
        img_buffer.seek(0)
        page.insert_image(fitz.Rect(0, 0, page.rect.width, page.rect.height), stream=img_buffer.getvalue())
    
    buffer = BytesIO()
    pdf.save(buffer)
    pdf.close()
    buffer.seek(0)
    tool_with_pdf.generated_file = buffer
    export_path = tmp_path / "large.pdf"
    result_path = tool_with_pdf.export(str(export_path))
    
    assert result_path == export_path
    assert export_path.exists()
