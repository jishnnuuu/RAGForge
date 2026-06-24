from chromadb import PersistentClient


class ChromaStore:

    def __init__(self):

        self.client = PersistentClient(
            path="data/chroma"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="ragforge"
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
                    "type": chunk.chunk_type,
                    "title": chunk.title
                }
                for chunk in chunks
            ],
            embeddings=embeddings.tolist()
        )

    def search(
        self,
        query_embedding,
        top_k=5
    ):

        return self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k
        )