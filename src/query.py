from embeddings.embedding_generator import (
    EmbeddingGenerator
)

from retrieval.chroma_retriever import (
    ChromaRetriever
)

from vectorstores.chroma_store import (
    ChromaStore
)

from llm.groq_client import (
    GroqClient
)

from rag.rag_pipeline import (
    RAGPipeline
)

def main():

    embedder = (
        EmbeddingGenerator()
    )

    store = ChromaStore()

    retriever = (
        ChromaRetriever(
            store,
            embedder
        )
    )

    while True:

        query = input(
            "\nAsk a question "
            "(exit to quit): "
        )

        if query.lower() == "exit":
            break

        results = (
            retriever.retrieve(
                query,
                top_k=5
            )
        )

        documents = (
            results["documents"][0]
        )

        metadatas = (
            results["metadatas"][0]
        )

        distances = (
            results["distances"][0]
        )

        print(
            "\nResults"
        )

        print("=" * 80)

        for doc, meta, score in zip(
            documents,
            metadatas,
            distances
        ):

            print(
                f"\nSource: "
                f"{meta['source']}"
            )

            print(
                f"Type: "
                f"{meta['chunk_type']}"
            )

            print(
                f"Score: "
                f"{score:.4f}"
            )

            print(
                f"\n{doc[:500]}"
            )

            print(
                "-" * 80
            )


if __name__ == "__main__":
    main()