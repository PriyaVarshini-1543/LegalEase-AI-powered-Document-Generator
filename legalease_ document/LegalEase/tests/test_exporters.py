from exporters.docx_exporter import export_docx
from exporters.pdf_exporter import export_pdf
from exporters.txt_exporter import export_txt


def test_txt_exporter():
    data = export_txt("Test", "Hello")
    assert data.getvalue().startswith(b"Test")


def test_docx_exporter():
    data = export_docx("Test", "Hello world")
    assert data.getvalue().startswith(b"PK")


def test_pdf_exporter():
    data = export_pdf("Test", "Hello world")
    assert data.getvalue().startswith(b"%PDF")
