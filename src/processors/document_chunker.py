import uuid

from schemas.chunk import Chunk
from schemas.document import Document


class DocumentChunker:

    def chunk(
        self,
        document: Document
    ):

        chunks = []

        for block in document.blocks:

            if not block.content:
                continue

            chunks.append(
                Chunk(
                    chunk_id=str(
                        uuid.uuid4()
                    ),
                    source=document.source,
                    chunk_type=block.block_type,
                    content=block.content
                )
            )

        return chunks