import json
from pathlib import Path

from schemas.chunk import Chunk


class CorpusLoader:

    def __init__(self):

        self.base_dir = Path(
            "data/documents"
        )

    def load_chunks(
        self
    ) -> list[Chunk]:

        chunks = []

        for chunk_file in self.base_dir.glob(
            "*/chunks.json"
        ):

            with open(
                chunk_file
            ) as f:

                data = json.load(f)

            chunks.extend(
                [
                    Chunk(**chunk)
                    for chunk in data
                ]
            )

        return chunks