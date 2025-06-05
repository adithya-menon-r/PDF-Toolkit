import fitz
import json
import pytest

from pdfwerks.core.pdf_tools import PDFTools

SAMPLE_TEXTS = [
    ("Testing export, so this is page 1", 30),
    ("PDFwerks is published to PyPI", 20),
    ("The test is being run by pytest", 12)
]


@pytest.fixture
def create_pdf(tmp_path):
    def _make():
        path = tmp_path / "test.pdf"
        pdf = fitz.open()
        for text, size in SAMPLE_TEXTS:
            page = pdf.new_page()
            page.insert_text((72, 72), text, fontsize=size)
        pdf.save(path)
        pdf.close()
        return str(path)
    return _make


@pytest.fixture
def create_empty_pdf(tmp_path):
    def _make():
        path = tmp_path / "empty.pdf"
        pdf = fitz.open()
        pdf.new_page()
        pdf.save(path)
        pdf.close()
        return str(path)
    return _make


def test_extract_to_plain_text(create_pdf):
    pdf_path = create_pdf()
    tool = PDFTools()
    tool.extract_to_plain_text(pdf_path)
    assert tool.generated_file is not None
    extracted = tool.generated_file.getvalue().decode("utf-8")
    for text, _ in SAMPLE_TEXTS:
        assert text in extracted
    assert extracted.count("\n") >= len(SAMPLE_TEXTS)


def test_extract_to_markdown(create_pdf):
    pdf_path = create_pdf()
    tool = PDFTools()
    tool.extract_to_markdown(pdf_path)
    assert tool.generated_file is not None
    extracted = tool.generated_file.getvalue().decode("utf-8")
    assert isinstance(extracted, str)
    assert len(extracted) > 0
    for text, _ in SAMPLE_TEXTS:
        assert text in extracted
    assert any(char in extracted for char in ("#", "*", "-", "`", "\n"))


def test_extract_to_json(create_pdf):
    pdf_path = create_pdf()
    tool = PDFTools()
    tool.extract_to_json(pdf_path)
    assert tool.generated_file is not None
    extracted = tool.generated_file.getvalue().decode("utf-8")
    data = json.loads(extracted)
    assert isinstance(data, list)
    assert len(data) == len(SAMPLE_TEXTS)
    for page in data:
        assert isinstance(page, dict)
        assert "blocks" in page
        assert isinstance(page["blocks"], list)
        for block in page["blocks"]:
            assert isinstance(block, dict)
    for text, _ in SAMPLE_TEXTS:
        assert text in extracted


def test_extract_to_plain_text_empty(create_empty_pdf):
    pdf_path = create_empty_pdf()
    tool = PDFTools()
    tool.extract_to_plain_text(pdf_path)
    assert tool.generated_file is not None
    extracted = tool.generated_file.getvalue().decode("utf-8").strip()
    assert extracted == "" or extracted.isspace()


def test_extract_to_markdown_empty(create_empty_pdf):
    pdf_path = create_empty_pdf()
    tool = PDFTools()
    tool.extract_to_markdown(pdf_path)
    assert tool.generated_file is not None
    extracted = tool.generated_file.getvalue().decode("utf-8").strip()
    assert extracted == "" or extracted.isspace()


def test_extract_to_json_empty(create_empty_pdf):
    pdf_path = create_empty_pdf()
    tool = PDFTools()
    tool.extract_to_json(pdf_path)
    assert tool.generated_file is not None
    extracted = tool.generated_file.getvalue().decode("utf-8").strip()
    data = json.loads(extracted)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0].get("blocks") == []
