import fitz
import pytest

from pdfwerks.core.pdf_tools import PDFTools
from pdfwerks.core.utils import parse_page_ranges

def create_test_pdf(tmp_path, num_pages):
    pdf_path = tmp_path / "test.pdf"
    pdf = fitz.open()
    for i in range(num_pages):
        page = pdf.new_page()
        page.insert_text((50, 50), f"Page {i+1}")
    pdf.save(str(pdf_path))
    pdf.close()
    return pdf_path

def test_delete_single_page(tmp_path):
    pdf_path = create_test_pdf(tmp_path, 5)
    tools = PDFTools()
    tools.delete_pages(str(pdf_path), [2])
    output_path = tmp_path / "output.pdf"
    tools.export(str(output_path))

    with fitz.open(str(output_path)) as pdf:
        assert len(pdf) == 4
        assert pdf[0].get_text().strip() == "Page 1"
        assert pdf[1].get_text().strip() == "Page 2"
        assert pdf[2].get_text().strip() == "Page 4"
        assert pdf[3].get_text().strip() == "Page 5"

def test_delete_multiple_pages(tmp_path):
    pdf_path = create_test_pdf(tmp_path, 10)
    tools = PDFTools()
    tools.delete_pages(str(pdf_path), [1, 4, 7])
    output_path = tmp_path / "output.pdf"
    tools.export(str(output_path))
    
    with fitz.open(str(output_path)) as pdf:
        assert len(pdf) == 7
        expected_pages = ["Page 1", "Page 3", "Page 4", "Page 6", "Page 7", "Page 9", "Page 10"]
        for i, expected in enumerate(expected_pages):
            assert pdf[i].get_text().strip() == expected

def test_delete_consecutive_pages(tmp_path):
    pdf_path = create_test_pdf(tmp_path, 8)
    tools = PDFTools()
    tools.delete_pages(str(pdf_path), [2, 3, 4])
    output_path = tmp_path / "output.pdf"
    tools.export(str(output_path))
    
    with fitz.open(str(output_path)) as pdf:
        assert len(pdf) == 5
        expected_pages = ["Page 1", "Page 2", "Page 6", "Page 7", "Page 8"]
        for i, expected in enumerate(expected_pages):
            assert pdf[i].get_text().strip() == expected

def test_delete_all_pages(tmp_path):
    pdf_path = create_test_pdf(tmp_path, 3)
    tools = PDFTools()
    with pytest.raises(ValueError, match="Cannot delete all pages"):
        tools.delete_pages(str(pdf_path), [0, 1, 2])

def test_delete_pages_invalid_indices(tmp_path):
    pdf_path = create_test_pdf(tmp_path, 5)
    tools = PDFTools()
    with pytest.raises(ValueError, match="Page index out of range"):
        tools.delete_pages(str(pdf_path), [-1])
    
    with pytest.raises(ValueError, match="Page index out of range"):
        tools.delete_pages(str(pdf_path), [5])

def test_delete_pages_with_ranges(tmp_path):
    pdf_path = create_test_pdf(tmp_path, 10)
    tools = PDFTools()
    pages = parse_page_ranges("2-4,7,9-10", str(pdf_path))
    tools.delete_pages(str(pdf_path), pages)
    output_path = tmp_path / "output.pdf"
    tools.export(str(output_path))
    
    with fitz.open(str(output_path)) as pdf:
        assert len(pdf) == 4
        expected_pages = ["Page 1", "Page 5", "Page 6", "Page 8"]
        for i, expected in enumerate(expected_pages):
            assert pdf[i].get_text().strip() == expected

def test_delete_pages_empty(tmp_path):
    pdf_path = create_test_pdf(tmp_path, 5)
    tools = PDFTools()
    with pytest.raises(ValueError, match="No pages specified for deletion"):
        tools.delete_pages(str(pdf_path), [])
