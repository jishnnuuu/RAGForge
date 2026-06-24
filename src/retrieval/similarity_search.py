import numpy as np


class SimilaritySearch:

    def search(
        self,
        query_embedding,
        chunk_embeddings,
        top_k: int = 5
    ):

        similarities = (
            chunk_embeddings
            @ query_embedding
        )

        top_indices = np.argsort(
            similarities
        )[::-1][:top_k]

        results = []

        for idx in top_indices:

            results.append(
                (
                    idx,
                    float(
                        similarities[idx]
                    )
                )
            )

        return results