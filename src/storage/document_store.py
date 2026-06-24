from pathlib import Path
import json


class DocumentStore:

    def __init__(self):

        self.base_dir = Path(
            "data/documents"
        )

        self.base_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(
        self,
        document,
        chunks
    ):

        document_name = (
            Path(document.source).stem
        )

        document_dir = (
            self.base_dir
            / document_name
        )

        document_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        document_path = (
            document_dir
            / "document.json"
        )

        chunks_path = (
            document_dir
            / "chunks.json"
        )

        with open(
            document_path,
            "w"
        ) as f:

            f.write(
                document.model_dump_json(
                    indent=4
                )
            )

        with open(
            chunks_path,
            "w"
        ) as f:

            json.dump(
                [
                    chunk.model_dump()
                    for chunk in chunks
                ],
                f,
                indent=4
            )

        return document_dir