class RAGPipeline:

    def __init__(
        self,
        retriever,
        llm
    ):

        self.retriever = retriever
        self.llm = llm

    def ask(
        self,
        query: str,
        top_k: int = 3
    ):

        results = (
            self.retriever.retrieve(
                query,
                top_k=top_k
            )
        )

        documents = (
            results["documents"][0]
        )

        metadatas = (
            results["metadatas"][0]
        )

        context_parts = []

        for doc, meta in zip(
            documents,
            metadatas
        ):

            context_parts.append(
                f"""
Source:
{meta['source']}

Content:
{doc}
"""
            )

        context = "\n\n".join(
            context_parts
        )

        prompt = f"""
You are a college website assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context,
say:

"I could not find that information."

Context:
{context}

Question:
{query}

Answer:
"""

        answer = self.llm.generate(
            prompt
        )

        return answer