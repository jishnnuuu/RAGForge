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

        blocks = []

        figure_counter = 0

        for page in pages:

            for block in page.blocks:

                block_type = self.normalize_label(
                    block.label
                )

                raw_html = block.html or ""

                content = self.html_parser.parse(
                    raw_html
                )

                if (
                    not content
                    and block_type != "figure"
                ):
                    continue

                figure_path = None

                if block_type == "figure":

                    figure_counter += 1

                    figure_path = (
                        self.figure_cropper.crop(
                            image=image,
                            bbox=block.bbox,
                            figure_name=(
                                f"figure_{figure_counter}"
                            )
                        )
                    )

                blocks.append(
                    ContentBlock(
                        block_type=block_type,
                        content=content,
                        raw_html=raw_html,
                        reading_order=block.reading_order,
                        confidence=(
                            block.confidence
                            if block.confidence
                            else 0.0
                        ),
                        bbox=(
                            block.bbox
                            if block.bbox
                            else []
                        ),
                        figure_path=figure_path
                    )
                )

        blocks.sort(
            key=lambda x: x.reading_order
        )

        return Document(
            source=image_path,
            blocks=blocks
        )