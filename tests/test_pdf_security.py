import fitz
import pytest
import pikepdf

from pdfwerks.core.pdf_tools import PDFTools


def create_test_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    pdf = fitz.open()
    page = pdf.new_page()
    page.insert_text((100, 100), "Some content to test PDF Security Operations")
    pdf.save(pdf_path)
    pdf.close()
    return str(pdf_path)


@pytest.fixture
def test_pdf(tmp_path):
    return create_test_pdf(tmp_path)


def test_enable_pdf_encryption(test_pdf):
    tool = PDFTools()
    password = "test"
    tool.enable_pdf_encryption(test_pdf, password)
    assert tool.generated_file is not None

    with pytest.raises(ValueError, match="PDF is already password protected"):
        tool.enable_pdf_encryption(tool.generated_file, password)
    
    with pytest.raises(pikepdf.PasswordError):
        with pikepdf.open(filename_or_stream=tool.generated_file) as pdf:
            pass
    
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as pdf:
        assert pdf.needs_pass
        pdf.authenticate(password)
        assert "Some content to test PDF Security Operations" in pdf[0].get_text()


def test_disable_pdf_encryption(test_pdf):
    tool = PDFTools()
    password = "test"
    tool.enable_pdf_encryption(test_pdf, password)
    encrypted_pdf = tool.generated_file
    
    with pytest.raises(ValueError, match="Incorrect password"):
        tool.disable_pdf_encryption(encrypted_pdf, "randompwd")
    
    tool.disable_pdf_encryption(encrypted_pdf, password)
    assert tool.generated_file is not None
    
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as pdf:
        assert "Some content to test PDF Security Operations" in pdf[0].get_text()


def test_update_pdf_password(test_pdf):
    tool = PDFTools()
    old_pwd = "oldpwd"
    new_pwd = "newpwd"
    tool.enable_pdf_encryption(test_pdf, old_pwd)
    encrypted_pdf = tool.generated_file
    
    with pytest.raises(ValueError, match="Incorrect password"):
        tool.update_pdf_password(encrypted_pdf, "wrongpwd", new_pwd)
    
    tool.update_pdf_password(encrypted_pdf, old_pwd, new_pwd)
    assert tool.generated_file is not None
    
    with pytest.raises(pikepdf.PasswordError):
        with pikepdf.open(filename_or_stream=tool.generated_file) as pdf:
            pass
    
    with pikepdf.open(filename_or_stream=tool.generated_file, password=new_pwd) as pdf:
        assert len(pdf.pages) == 1
        
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as pdf:
        assert pdf.needs_pass
        pdf.authenticate(new_pwd)
        assert "Some content to test PDF Security Operations" in pdf[0].get_text()


def test_enable_encryption_on_encrypted_pdf(test_pdf):
    tool = PDFTools()
    password = "test"
    tool.enable_pdf_encryption(test_pdf, password)
    encrypted_pdf = tool.generated_file

    with pytest.raises(ValueError, match="PDF is already password protected"):
        tool.enable_pdf_encryption(encrypted_pdf, "pwd")


def test_disable_encryption_on_unencrypted_pdf(test_pdf):
    tool = PDFTools()
    with pytest.raises(ValueError, match="PDF is not password protected"):
        tool.disable_pdf_encryption(test_pdf, "pwd")


def test_update_password_on_unencrypted_pdf(test_pdf):
    tool = PDFTools()
    with pytest.raises(ValueError, match="PDF is not password protected"):
        tool.update_pdf_password(test_pdf, "oldpwd", "newpwd")


def test_encryption_with_empty_password(test_pdf):
    tool = PDFTools()
    with pytest.raises(ValueError, match="Password can't be empty"):
        tool.enable_pdf_encryption(test_pdf, "")


def test_disable_encryption_with_empty_password(test_pdf):
    tool = PDFTools()
    password = "test"
    tool.enable_pdf_encryption(test_pdf, password)
    encrypted_pdf = tool.generated_file
    
    with pytest.raises(ValueError, match="Password can't be empty"):
        tool.disable_pdf_encryption(encrypted_pdf, "")


def test_update_password_with_empty_passwords(test_pdf):
    tool = PDFTools()
    password = "test"
    tool.enable_pdf_encryption(test_pdf, password)
    encrypted_pdf = tool.generated_file
    
    with pytest.raises(ValueError, match="Password can't be empty"):
        tool.update_pdf_password(encrypted_pdf, "", "newpwd")
    
    with pytest.raises(ValueError, match="Password can't be empty"):
        tool.update_pdf_password(encrypted_pdf, password, "")
    
    with pytest.raises(ValueError, match="Password can't be empty"):
        tool.update_pdf_password(encrypted_pdf, "", "")


def test_encryption_with_special_chars(test_pdf):
    tool = PDFTools()
    password = "!@#$%^&*()_+"
    tool.enable_pdf_encryption(test_pdf, password)
    encrypted_pdf = tool.generated_file
    
    tool.disable_pdf_encryption(encrypted_pdf, password)
    assert tool.generated_file is not None
    
    with fitz.open(stream=tool.generated_file.getvalue(), filetype="pdf") as pdf:
        assert "Some content to test PDF Security Operations" in pdf[0].get_text()
