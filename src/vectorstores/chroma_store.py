from chromadb import PersistentClient


class ChromaStore:

    def __init__(
        self,
        collection_name: str = "ragforge"
    ):

        self.client = PersistentClient(
            path="data/chroma"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

    def add_chunks(
        self,
        chunks,
        embeddings
    ):

        self.collection.add(
            ids=[
                chunk.chunk_id
                for chunk in chunks
            ],

            documents=[
                chunk.content
                for chunk in chunks
            ],

            metadatas=[
                {
                    "source": chunk.source,
                    "chunk_type": chunk.chunk_type,
                    "title": (
                        chunk.title
                        if chunk.title
                        else ""
                    )
                }
                for chunk in chunks
            ],

            embeddings=embeddings.tolist()
        )

    def search(
        self,
        query_embedding,
        top_k: int = 5
    ):

        return self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k
        )

    def count(self):

        return self.collection.count()

    def reset(self):

        self.client.delete_collection(
            "ragforge"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="ragforge"
            )
        )