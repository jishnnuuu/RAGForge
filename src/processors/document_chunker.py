import uuid

from schemas.chunk import Chunk
from schemas.document import Document


class DocumentChunker:

    def chunk(
        self,
        document: Document
    ) -> list[Chunk]:

        chunks = []

        title = None

        content_parts = []

        table_counter = 1

        for block in document.blocks:

            if not block.content:
                continue

            # --------------------------
            # Document Title
            # --------------------------

            if (
                block.block_type == "header"
                and title is None
            ):

                title = block.content

                continue

            # --------------------------
            # Tables
            # --------------------------

            if block.block_type == "table":

                chunks.append(
                    Chunk(
                        chunk_id=str(
                            uuid.uuid4()
                        ),
                        source=document.source,
                        chunk_type="table",
                        title=(
                            f"Table {table_counter}"
                        ),
                        content=block.content,
                        metadata={}
                    )
                )

                table_counter += 1

                continue

            # --------------------------
            # Main Content
            # --------------------------

            if block.block_type in [
                "text",
                "metric",
                "section_header",
                "footer"
            ]:

                content_parts.append(
                    block.content
                )

        # --------------------------
        # Main Content Chunk
        # --------------------------

        if content_parts:

            chunks.insert(
                0,
                Chunk(
                    chunk_id=str(
                        uuid.uuid4()
                    ),
                    source=document.source,
                    chunk_type="main_content",
                    title=title,
                    content="\n\n".join(
                        content_parts
                    ),
                    metadata={}
                )
            )

        return chunks