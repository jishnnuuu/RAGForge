import fitz

from schemas.document import (
    Document,
    ContentBlock
)


class PDFDocumentBuilder:

    def build(
        self,
        pdf,
        source: str
    ) -> Document:

        blocks = []

        reading_order = 0

        for page in pdf:

            page_dict = page.get_text(
                "dict"
            )

            for block in page_dict.get(
                "blocks",
                []
            ):

                if block.get("type") != 0:
                    continue

                text_parts = []

                for line in block.get(
                    "lines",
                    []
                ):

                    for span in line.get(
                        "spans",
                        []
                    ):

                        text_parts.append(
                            span.get(
                                "text",
                                ""
                            )
                        )

                    text_parts.append(
                        "\n"
                    )

                text = "".join(
                    text_parts
                ).strip()

                if not text:
                    continue

                blocks.append(

                    ContentBlock(

                        block_type="text",

                        content=text,

                        raw_html="",

                        reading_order=reading_order,

                        confidence=1.0,

                        bbox=list(
                            block.get(
                                "bbox",
                                ()
                            )
                        ),

                        figure_path=None

                    )

                )

                reading_order += 1

        return Document(

            source=source,

            blocks=blocks

        )