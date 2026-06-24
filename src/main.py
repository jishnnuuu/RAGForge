import json

from services.surya_service import (
    SuryaService
)

from extractors.image_extractor import (
    ImageExtractor
)

from processors.figure_processor import (
    FigureProcessor
)

from processors.document_chunker import (
    DocumentChunker
)

from embeddings.embedding_generator import (
    EmbeddingGenerator
)

from retrieval.similarity_search import (
    SimilaritySearch
)


IMAGE_PATH = "samples/placement_2024.jpg"

TEST_QUERY = (
    "How many placement offers were made?"
)


def main():

    # ==================================================
    # Load Models
    # ==================================================

    print("\nLoading Surya...")
    print("=" * 80)

    surya_service = SuryaService()

    # ==================================================
    # Extraction
    # ==================================================

    print("\nExtracting document...")
    print("=" * 80)

    extractor = ImageExtractor(
        surya_service
    )

    document = extractor.extract(
        IMAGE_PATH
    )

    print(
        "Document extracted successfully."
    )

    # ==================================================
    # Figures
    # ==================================================

    print("\nProcessing figures...")
    print("=" * 80)

    figure_processor = FigureProcessor()

    figures = figure_processor.process(
        document
    )

    print(
        f"Detected {len(figures)} figure(s)\n"
    )

    for idx, figure in enumerate(
        figures,
        start=1
    ):

        print(
            f"Figure {idx}: "
            f"{figure['path']}"
        )

    # ==================================================
    # Chunking
    # ==================================================

    print("\nGenerating chunks...")
    print("=" * 80)

    chunker = DocumentChunker()

    chunks = chunker.chunk(
        document
    )

    print(
        f"Generated {len(chunks)} chunk(s)"
    )

    print("\nChunk Preview:")
    print("=" * 80)

    for idx, chunk in enumerate(
        chunks,
        start=1
    ):

        print(
            f"\nChunk {idx}"
        )

        print(
            f"Type       : "
            f"{chunk.chunk_type}"
        )

        print(
            f"Confidence : "
            f"{chunk.confidence:.3f}"
        )

        print(
            f"Content    : "
            f"{chunk.content[:200]}"
        )

    # ==================================================
    # Embeddings
    # ==================================================

    print("\nGenerating embeddings...")
    print("=" * 80)

    embedder = (
        EmbeddingGenerator()
    )

    chunk_texts = [
        chunk.content
        for chunk in chunks
    ]

    chunk_embeddings = (
        embedder.embed_batch(
            chunk_texts
        )
    )

    print(
        f"Generated embeddings for "
        f"{len(chunk_embeddings)} chunks"
    )

    # ==================================================
    # Retrieval Test
    # ==================================================

    print("\nRunning retrieval test...")
    print("=" * 80)

    print(
        f"Query: {TEST_QUERY}"
    )

    query_embedding = (
        embedder.embed(
            TEST_QUERY
        )
    )

    searcher = (
        SimilaritySearch()
    )

    results = searcher.search(
        query_embedding,
        chunk_embeddings,
        top_k=5
    )

    print("\nTop Matches:")
    print("=" * 80)

    for idx, score in results:

        print(
            f"\nScore: "
            f"{score:.4f}"
        )

        print(
            f"Chunk Type: "
            f"{chunks[idx].chunk_type}"
        )

        print(
            f"Content: "
            f"{chunks[idx].content}"
        )

    # ==================================================
    # Save Outputs
    # ==================================================

    print("\nSaving outputs...")
    print("=" * 80)

    with open(
        "outputs/result.json",
        "w"
    ) as f:

        f.write(
            document.model_dump_json(
                indent=4
            )
        )

    with open(
        "outputs/chunks.json",
        "w"
    ) as f:

        json.dump(
            [
                chunk.model_dump()
                for chunk in chunks
            ],
            f,  m 
            indent=4
        )

    print(
        "Saved outputs/result.json"
    )

    print(
        "Saved outputs/chunks.json"
    )

    print(
        "\nPipeline completed successfully."
    )


if __name__ == "__main__":
    main()