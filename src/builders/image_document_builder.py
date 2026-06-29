from schemas.document import (
    Document,
    ContentBlock
)


class ImageDocumentBuilder:

    def build(
        self,
        source: str,
        page,
        figure_cropper,
        html_parser,
        normalize_label,
        image
    ) -> Document:

        blocks = []

        figure_counter = 0

        for block in page.blocks:

            block_type = normalize_label(
                block.label
            )

            raw_html = block.html or ""

            content = html_parser.parse(
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

                figure_path = figure_cropper.crop(
                    image=image,
                    bbox=block.bbox,
                    figure_name=f"figure_{figure_counter}"
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
            key=lambda block: block.reading_order
        )

        return Document(
            source=source,
            blocks=blocks
        )