from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:

    def __init__(
        self,
        model_name="BAAI/bge-small-en-v1.5"
    ):

        self.model = SentenceTransformer(
            model_name
        )

    def embed(
        self,
        text: str
    ):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )

generator = EmbeddingGenerator()

embedding = generator.embed(
    "Total Offers: 602"
)

print(
    len(embedding)
)