from pydantic import BaseModel


class Chunk(BaseModel):

    chunk_id: str

    source: str

    chunk_type: str

    content: str

    confidence: float

    parent_section: str | None = None