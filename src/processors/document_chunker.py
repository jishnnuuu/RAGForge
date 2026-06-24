import re
import uuid

from schemas.chunk import Chunk
from schemas.document import Document


class DocumentChunker:

    def _is_numeric(
        self,
        text: str
    ) -> bool:

        return bool(
            re.fullmatch(
                r"[\d.,]+",
                text.strip()
            )
        )

    def _extract_title(
        self,
        document: Document
    ) -> str | None:

        headers = [
            block.content
            for block in document.blocks
            if (
                block.block_type == "header"
                and block.content
            )
        ]

        if not headers:
            return None

        # Prefer placement/statistics/report style headers
        for header in headers:

            upper_header = header.upper()

            if any(
                keyword in upper_header
                for keyword in [
                    "PLACEMENT",
                    "STATISTICS",
                    "REPORT",
                    "BROCHURE",
                    "ADMISSION",
                    "ACADEMIC"
                ]
            ):
                return header

        # fallback: longest header
        return max(
            headers,
            key=len
        )

    def chunk(
        self,
        document: Document
    ) -> list[Chunk]:

        chunks = []

        title = self._extract_title(
            document
        )

        content_parts = []

        table_counter = 1

        blocks = document.blocks

        i = 0

        while i < len(blocks):

            block = blocks[i]

            if not block.content:

                i += 1
                continue

            # ----------------------------------
            # Skip headers entirely
            # They are metadata now
            # ----------------------------------

            if block.block_type == "header":

                i += 1
                continue

            # ----------------------------------
            # Tables become separate chunks
            # ----------------------------------

            if block.block_type == "table":

                table_content = block.content

                if title:

                    table_content = (
                        f"{title}\n\n"
                        f"{table_content}"
                    )

                chunks.append(
                    Chunk(
                        chunk_id=str(
                            uuid.uuid4()
                        ),
                        source=document.source,
                        chunk_type="table",
                        title=f"Table {table_counter}",
                        content=table_content,
                        metadata={}
                    )
                )

                table_counter += 1

                i += 1
                continue

            # ----------------------------------
            # Metric normalization
            # 602 + Total Offers
            # ->
            # Total Offers: 602
            # ----------------------------------

            if (
                block.block_type == "text"
                and self._is_numeric(
                    block.content
                )
                and i + 1 < len(blocks)
            ):

                next_block = blocks[i + 1]

                if (
                    next_block.block_type
                    == "text"
                    and not self._is_numeric(
                        next_block.content
                    )
                ):

                    content_parts.append(
                        f"{next_block.content}: "
                        f"{block.content}"
                    )

                    i += 2
                    continue

            # ----------------------------------
            # Normal content
            # ----------------------------------

            if block.block_type in [
                "text",
                "metric",
                "section_header",
                "footer"
            ]:

                content_parts.append(
                    block.content
                )

            i += 1

        # ----------------------------------
        # Main Content Chunk
        # ----------------------------------

        if content_parts:

            main_content = "\n\n".join(
                content_parts
            )

            if title:

                main_content = (
                    f"{title}\n\n"
                    f"{main_content}"
                )

            chunks.insert(
                0,
                Chunk(
                    chunk_id=str(
                        uuid.uuid4()
                    ),
                    source=document.source,
                    chunk_type="main_content",
                    title=title,
                    content=main_content,
                    metadata={}
                )
            )

        return chunks