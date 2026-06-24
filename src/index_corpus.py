from storage.corpus_loader import (
    CorpusLoader
)

from embeddings.embedding_generator import (
    EmbeddingGenerator
)

from vectorstores.chroma_store import (
    ChromaStore
)


def main():

    print(
        "\nLoading corpus..."
    )

    loader = CorpusLoader()

    chunks = loader.load_chunks()

    print(
        f"Loaded {len(chunks)} chunks"
    )

    print(
        "\nGenerating embeddings..."
    )

    embedder = (
        EmbeddingGenerator()
    )

    embeddings = (
        embedder.embed_batch(
            [
                chunk.content
                for chunk in chunks
            ]
        )
    )

    print(
        "\nIndexing into Chroma..."
    )

    store = ChromaStore()

    store.reset()

    store.add_chunks(
        chunks,
        embeddings
    )

    print(
        f"Indexed "
        f"{store.count()} chunks"
    )


if __name__ == "__main__":
    main()