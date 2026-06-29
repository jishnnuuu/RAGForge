from embeddings.embedding_generator import (
    EmbeddingGenerator
)

from vectorstores.chroma_store import (
    ChromaStore
)

from llm.groq_client import (
    GroqClient
)


SYSTEM_PROMPT = """
You are an AI assistant for a college website.

Answer ONLY using the retrieved context.

Rules:

1. Do NOT make up facts.
2. If the answer is not present, reply:
   "I could not find that information in the available documents."
3. Keep answers concise.
4. Mention the source document(s) at the end.
"""


def build_context(results):

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = []

    sources = set()

    for document, metadata in zip(
        documents,
        metadatas
    ):

        sources.add(
            metadata["source"]
        )

        context.append(
            f"""
Source:
{metadata['source']}

Title:
{metadata.get("title","")}

Content:
{document}
"""
        )

    return (
        "\n\n".join(context),
        sources
    )


def main():

    embedder = EmbeddingGenerator()

    store = ChromaStore()

    llm = GroqClient()

    print("=" * 80)
    print("RAGForge Chat")
    print("=" * 80)

    while True:

        query = input(
            "\nAsk (or 'exit'): "
        )

        if query.lower() == "exit":
            break

        query_embedding = embedder.embed(
            query
        )

        results = store.search(
            query_embedding,
            top_k=3
        )

        context, sources = build_context(
            results
        )

        prompt = f"""
Context:

{context}

Question:

{query}

Answer:
"""

        answer = llm.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT
        )

        print("\nAnswer")
        print("-" * 80)

        print(answer)

        print("\nSources")

        for source in sources:

            print(f"- {source}")


if __name__ == "__main__":
    main()