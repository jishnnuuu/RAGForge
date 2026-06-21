from pydantic import BaseModel
from typing import List


class ContentBlock(BaseModel):
    block_type: str
    content: str
    raw_html: str | None = None
    reading_order: int
    confidence: float
    bbox: list[float]
    page_number: int = 1
    figure_path: str | None = None


class Document(BaseModel):
    source: str
    blocks: List[ContentBlock]