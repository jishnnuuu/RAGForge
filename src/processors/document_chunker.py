import re
import uuid

from schemas.chunk import Chunk
from schemas.document import Document


class DocumentChunker:

    def _is_numeric(
        self,
        text: str
    ) -> bool:

        text = text.strip()

        return bool(
            re.fullmatch(
                r"[\d.,]+",
                text
            )
        )

    def chunk(
        self,
        document: Document
    ) -> list[Chunk]:

        chunks = []

        blocks = document.blocks

        i = 0

        while i < len(blocks):

            block = blocks[i]

            if not block.content:

                i += 1
                continue

            content = block.content

            chunk_type = block.block_type

            confidence = block.confidence

            # ----------------------------------
            # Merge:
            #
            # 602
            # Total Offers
            #
            # =>
            #
            # Total Offers: 602
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

                    i += 2

                    chunks.append(
                        Chunk(
                            chunk_id=str(
                                uuid.uuid4()
                            ),
                            source=document.source,
                            chunk_type="metric",
                            content=content,
                            confidence=confidence
                        )
                    )

                    continue

            chunks.append(
                Chunk(
                    chunk_id=str(
                        uuid.uuid4()
                    ),
                    source=document.source,
                    chunk_type=chunk_type,
                    content=content,
                    confidence=confidence
                )
            )

            i += 1

        return chunks