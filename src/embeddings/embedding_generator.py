from sentence_transformers import (
    SentenceTransformer
)


class EmbeddingGenerator:

    def __init__(
        self,
        model_name: str = (
            "BAAI/bge-small-en-v1.5"
        )
    ):

        print(
            f"Loading embedding model: "
            f"{model_name}"
        )

        self.model = (
            SentenceTransformer(
                model_name
            )
        )

    def embed(
        self,
        text: str
    ):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )

    def embed_batch(
        self,
        texts: list[str]
    ):

        return self.model.encode(
            texts,
            normalize_embeddings=True
        )