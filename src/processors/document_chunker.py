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

    def chunk(
        self,
        document: Document
    ) -> list[Chunk]:

        chunks = []

        current_section = None

        blocks = document.blocks

        i = 0

        while i < len(blocks):

            block = blocks[i]

            if not block.content:

                i += 1
                continue

            # ----------------------------------
            # Section Tracking
            # ----------------------------------

            if block.block_type in [
                "header",
                "section_header"
            ]:

                current_section = (
                    block.content
                )

                i += 1
                continue

            content = block.content

            chunk_type = block.block_type

            confidence = block.confidence

            # ----------------------------------
            # Merge Metrics
            # ----------------------------------

            if (
                chunk_type == "text"
                and self._is_numeric(content)
                and i + 1 < len(blocks)
            ):

                next_block = blocks[i + 1]

                if (
                    next_block.block_type == "text"
                    and not self._is_numeric(
                        next_block.content
                    )
                ):

                    content = (
                        f"{next_block.content}: "
                        f"{content}"
                    )

                    confidence = min(
                        confidence,
                        next_block.confidence
                    )

                    chunk_type = "metric"

                    i += 2

                else:

                    i += 1

            else:

                i += 1

            # ----------------------------------
            # Context Enrichment
            # ----------------------------------

            enriched_content = content

            if current_section:

                enriched_content = (
                    f"{current_section}\n\n"
                    f"{content}"
                )

            chunks.append(
                Chunk(
                    chunk_id=str(
                        uuid.uuid4()
                    ),
                    source=document.source,
                    chunk_type=chunk_type,
                    content=enriched_content,
                    confidence=confidence,
                    parent_section=current_section
                )
            )

        return chunks