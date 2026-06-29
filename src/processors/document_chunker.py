import re
import uuid

from schemas.chunk import Chunk
from schemas.document import Document

from processors.document_formatter import (
    DocumentFormatter
)


class DocumentChunker:

    def __init__(self):

        self.formatter = DocumentFormatter()

    # =====================================================

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

    # =====================================================

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

        for header in headers:

            upper = header.upper()

            if any(
                keyword in upper
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

        return max(
            headers,
            key=len
        )

    # =====================================================

    def chunk(
        self,
        document: Document
    ) -> list[Chunk]:

        chunks = []

        title = self._extract_title(
            document
        )
        
        current_section = title

        content_parts = []

        table_counter = 1

        blocks = document.blocks

        i = 0

        while i < len(blocks):

            block = blocks[i]

            if not block.content:

                i += 1
                continue

            # -------------------------------------------------
            # Ignore document headers
            # -------------------------------------------------

            if block.block_type == "header":

                i += 1
                continue
                
            # ---------------------------------------
            # Track current section
            # ---------------------------------------

            if block.block_type == "section_header":

                current_section = block.content

                content_parts.append(
                    block.content
                )

                i += 1

                continue

            # -------------------------------------------------
            # Tables
            # -------------------------------------------------

            if block.block_type == "table":

                embedding_text = block.content

                if current_section:

                    embedding_text = (
                        f"{current_section}\n\n"
                        f"{embedding_text}"
                    )

                llm_text = self.formatter.format(
                    block
                )

                if not llm_text:

                    llm_text = embedding_text

                elif current_section:

                    llm_text = (
                        f"{current_section}\n\n"
                        f"{llm_text}"
                    )

                chunks.append(

                    Chunk(

                        chunk_id=str(
                            uuid.uuid4()
                        ),

                        source=document.source,

                        chunk_type="table",

                        title=current_section or f"Table {table_counter}",

                        embedding_text=embedding_text,

                        llm_text=llm_text,

                        metadata={
                            "has_html": bool(
                                block.raw_html
                            )
                        }

                    )

                )

                table_counter += 1

                i += 1

                continue

            # -------------------------------------------------
            # Metric Normalization
            # 602 + Total Offers
            # ->
            # Total Offers: 602
            # -------------------------------------------------

            if (
                block.block_type == "text"
                and self._is_numeric(
                    block.content
                )
                and i + 1 < len(blocks)
            ):

                next_block = blocks[i + 1]

                if (
                    next_block.block_type == "text"
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

            # -------------------------------------------------
            # Main document content
            # -------------------------------------------------

            if block.block_type in [

                "text",

                "metric",

                # "section_header",

                "footer"

            ]:

                if (
                    hasattr(block, "confidence")
                    and block.confidence is not None
                    and block.confidence < 0.75
                ):

                    i += 1
                    continue

                content_parts.append(
                    block.content
                )
            i += 1

        # -------------------------------------------------
        # Main Content Chunk
        # -------------------------------------------------

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

                    embedding_text=main_content,

                    llm_text=main_content,

                    metadata={}

                )

            )

        return chunks