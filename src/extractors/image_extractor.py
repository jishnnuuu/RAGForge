from PIL import Image
from bs4 import BeautifulSoup

from services.surya_service import (
    SuryaService
)

from utils.figure_cropper import (
    FigureCropper
)

from schemas.document import (
    Document,
    ContentBlock
)

from utils.html_parser import (
    HTMLParser
)

from builders.image_document_builder import (
    ImageDocumentBuilder
)

LABEL_MAP = {
    "PageHeader": "header",
    "SectionHeader": "section_header",
    "PageFooter": "footer",
    "Text": "text",
    "Table": "table",
    "Figure": "figure",
    "Picture": "picture"
}


class ImageExtractor:

    def __init__(
        self,
        surya_service: SuryaService
    ):

        self.surya = surya_service

        self.layout_predictor = (
            self.surya.layout_predictor
        )

        self.ocr_predictor = (
            self.surya.ocr_predictor
        )

        self.figure_cropper = FigureCropper()
        
        self.html_parser = HTMLParser()
        
        self.builder = ImageDocumentBuilder()

    

    def normalize_label(
        self,
        label: str
    ) -> str:

        return LABEL_MAP.get(
            label,
            label.lower()
        )

    def extract(
        self,
        image_path: str
    ) -> Document:

        image = Image.open(
            image_path
        )

        layouts = self.layout_predictor(
            [image]
        )

        pages = self.ocr_predictor(
            [image],
            layouts
        )

        return self.builder.build(

            source=image_path,

            page=pages[0],

            figure_cropper=self.figure_cropper,

            html_parser=self.html_parser,

            normalize_label=self.normalize_label,

            image=image

        )