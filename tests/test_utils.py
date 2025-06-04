from pathlib import Path

from pdfwerks.core.utils import get_default_save_path, validate_files, get_unique_save_path


def test_get_default_save_path():
    path = get_default_save_path("test.pdf")
    assert isinstance(path, str)
    assert path.endswith("test.pdf")
    assert Path(path).parent == Path.home() / "Downloads"


def test_validate_files(tmp_path):
    pdf_file = tmp_path / "test.pdf"
    jpg_file = tmp_path / "test.jpg"
    txt_file = tmp_path / "test.txt"
    invalid_file = tmp_path / "test.invalid"
    
    pdf_file.write_text("Testing with some PDF content")
    jpg_file.write_text("Testing with some JPG content")
    txt_file.write_text("Testing with some TXT content")
    invalid_file.write_text("Testing with some Invalid content")
    
    files = [str(pdf_file), str(jpg_file), str(txt_file), str(invalid_file), "non-existent.pdf"]
    allowed_extensions = [".pdf", ".jpg", ".txt"]
    
    valid_files = validate_files(files, allowed_extensions)
    
    assert len(valid_files) == 3
    assert str(pdf_file) in valid_files
    assert str(jpg_file) in valid_files
    assert str(txt_file) in valid_files
    assert str(invalid_file) not in valid_files
    assert "non-existent.pdf" not in valid_files


def test_validate_files_empty():
    assert validate_files([], [".pdf"]) == []
    assert validate_files(["test.pdf"], []) == []


def test_get_unique_save_path(tmp_path):
    base_path = tmp_path / "test.pdf"
    base_path.write_text("Some content already exists")
    unique_path = get_unique_save_path(base_path)
    assert unique_path == tmp_path / "test_1.pdf"
    assert not unique_path.exists()
    unique_path.write_text("Adding some content to the new unique file")
    new_unique_path = get_unique_save_path(base_path)
    assert new_unique_path == tmp_path / "test_2.pdf"


def test_get_unique_save_path_nonexistent(tmp_path):
    base_path = tmp_path / "non-existent.pdf"
    unique_path = get_unique_save_path(base_path)
    assert unique_path == base_path
