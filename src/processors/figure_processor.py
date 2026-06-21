from schemas.document import (
    Document
)


class FigureProcessor:

    def get_figures(
        self,
        document: Document
    ):

        figures = []

        for block in document.blocks:

            if (
                block.block_type
                == "figure"
            ):

                figures.append(
                    {
                        "path": block.figure_path,
                        "bbox": block.bbox,
                        "block_type": block.block_type
                    }
                )

        return figures

    def process(
        self,
        document: Document
    ):
        return self.get_figures(
            document
        )