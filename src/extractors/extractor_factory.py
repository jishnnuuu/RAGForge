from pathlib import Path

from services.surya_service import (
    SuryaService
)

from extractors.image_extractor import (
    ImageExtractor
)

from extractors.pdf_extractor import (
    PDFExtractor
)


class ExtractorFactory:

    def __init__(self):

        self.surya = None

    def create(
        self,
        file_path: str
    ):

        suffix = Path(file_path).suffix.lower()

        if suffix == ".pdf":

            return PDFExtractor()

        if suffix in [
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".tiff",
            ".webp"
        ]:

            if self.surya is None:

                print("\nLoading Surya...")
                print("=" * 80)

                self.surya = SuryaService()

            return ImageExtractor(
                self.surya
            )

        raise ValueError(
            f"Unsupported file type: {suffix}"
        )