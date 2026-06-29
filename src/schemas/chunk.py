from pydantic import BaseModel
from typing import Any


class Chunk(BaseModel):

    chunk_id: str

    source: str

    chunk_type: str

    title: str

    # Used for embedding generation
    embedding_text: str

    # Used as context for the LLM
    llm_text: str

    metadata: dict[str, Any] = {}