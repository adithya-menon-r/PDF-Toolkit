import fitz
import pytest
from PIL import Image

from pdfwerks.core.pdf_tools import PDFTools


def create_test_image(tmp_path, format="PNG", size=(800, 600)):
    img_path = tmp_path / f"test.{format.lower()}"
    img = Image.new("RGB", size, (255, 255, 255))
    img.save(img_path, format=format)
    return str(img_path)


@pytest.fixture
def sample_png(tmp_path):
    return create_test_image(tmp_path, "PNG")


@pytest.fixture
def sample_jpg(tmp_path):
    return create_test_image(tmp_path, "JPEG")


def test_convert_png_to_pdf(sample_png):
    tool = PDFTools()
    tool.convert_img_to_pdf(sample_png)
    assert tool.generated_file is not None
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as result:
        assert len(result) == 1
        page = result[0]
        assert page.rect.width > 0
        assert page.rect.height > 0


def test_convert_jpg_to_pdf(sample_jpg):
    tool = PDFTools()
    tool.convert_img_to_pdf(sample_jpg)
    assert tool.generated_file is not None
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as result:
        assert len(result) == 1


def test_convert_small_image(tmp_path):
    img_path = create_test_image(tmp_path, "PNG", size=(100, 100))
    tool = PDFTools()
    tool.convert_img_to_pdf(img_path)
    assert tool.generated_file is not None
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as result:
        assert len(result) == 1
        page = result[0]
        assert page.rect.width >= 100 


def test_convert_large_image(tmp_path):
    img_path = create_test_image(tmp_path, "PNG", size=(2000, 1500))
    tool = PDFTools()
    tool.convert_img_to_pdf(img_path)
    assert tool.generated_file is not None
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as result:
        assert len(result) == 1
        page = result[0]
        assert page.rect.width <= 595


def test_convert_nonexistent_image():
    tool = PDFTools()
    with pytest.raises(Exception):
        tool.convert_img_to_pdf("nonexistent.png")


def test_convert_invalid_image(tmp_path):
    invalid_path = tmp_path / "invalid.png"
    invalid_path.write_text("This is definitely not an image. Believe me.")
    tool = PDFTools()
    with pytest.raises(Exception):
        tool.convert_img_to_pdf(str(invalid_path))
