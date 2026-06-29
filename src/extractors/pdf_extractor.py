import fitz

from builders.pdf_document_builder import (
    PDFDocumentBuilder
)


class PDFExtractor:

    def __init__(self):

        self.builder = PDFDocumentBuilder()

    def extract(
        self,
        pdf_path: str
    ):

        pdf = fitz.open(pdf_path)

        return self.builder.build(
            pdf=pdf,
            source=pdf_path
        )