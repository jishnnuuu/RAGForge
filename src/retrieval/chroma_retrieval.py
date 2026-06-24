class ChromaRetriever:

    def __init__(
        self,
        store,
        embedder
    ):

        self.store = store
        self.embedder = embedder

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        query_embedding = (
            self.embedder.embed(
                query
            )
        )

        return self.store.search(
            query_embedding,
            top_k
        )