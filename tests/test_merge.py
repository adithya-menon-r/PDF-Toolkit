import fitz
import pytest
from PIL import Image

from pdfwerks.core.pdf_tools import PDFTools


def create_test_image(path, format=None):
    img = Image.new("RGB", (100, 100), (0, 0, 0))
    img.save(path, format=format)


def create_test_pdf(path, pages=1):
    pdf = fitz.open()
    for _ in range(pages):
        pdf.new_page()
    pdf.save(path)
    pdf.close()


@pytest.fixture
def generate_req_files(tmp_path):
    def _make(file_types):
        paths = []
        for i, file_type in enumerate(file_types, start=1):
            if file_type == "pdf":
                path = tmp_path / f"file{i}.pdf"
                create_test_pdf(path)
            elif file_type == "multipage_pdf":
                path = tmp_path / f"file{i}.pdf"
                create_test_pdf(path, pages=3)
            elif file_type == "png":
                path = tmp_path / f"image{i}.png"
                create_test_image(path)
            elif file_type == "jpg":
                path = tmp_path / f"image{i}.jpg"
                create_test_image(path, format="JPEG")
            elif file_type == "txt":
                path = tmp_path / f"note{i}.txt"
                path.write_text("Testing the Merge PDFs tool in PDFwerks")
            else:
                path = tmp_path / f"file{i}.{file_type}"
                path.write_text(f"This is a test .{file_type} file.")
            paths.append(str(path))
        return paths
    return _make


@pytest.mark.parametrize("file_types, expected_pages", [
    (["pdf", "pdf"], 2),
    (["pdf", "pdf", "pdf"], 3),
    (["multipage_pdf", "pdf"], 4),
    (["multipage_pdf", "multipage_pdf"], 6),
    (["pdf", "png"], 2),
    (["png", "jpg"], 2),
    (["jpg", "png", "jpg"], 3),
    (["pdf", "txt"], 2),
    (["jpg", "txt"], 2),
    (["txt", "txt"], 2),
    (["pdf", "jpg", "pdf", "png", "txt", "pdf"], 6),
])
def test_merge_general(generate_req_files, file_types, expected_pages):
    files = generate_req_files(file_types)
    tool = PDFTools()
    tool.merge(files)
    assert tool.generated_file is not None
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as result:
        assert len(result) == expected_pages


def test_merge_with_unsupported_files(generate_req_files):
    files = generate_req_files(["pdf", "png", "txt", "md", "py", "pdf", "jpg"])
    tool = PDFTools()
    tool.merge(files)
    assert tool.generated_file is not None
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as result:
        assert len(result) == 5


def test_merge_empty():
    tool = PDFTools()
    with pytest.raises(ValueError, match="No files provided for merging"):
        tool.merge([])
