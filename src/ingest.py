import argparse

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

from storage.document_store import (
    DocumentStore
)

from vectorstores.chroma_store import (
    ChromaStore
)


def ingest(
    image_path: str
):

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
        image_path
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
        f"Detected {len(figures)} figure(s)"
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

    # ==================================================
    # Embeddings
    # ==================================================

    print("\nGenerating embeddings...")
    print("=" * 80)

    embedder = EmbeddingGenerator()

    embeddings = embedder.embed_batch(
        [
            chunk.embedding_text
            for chunk in chunks
        ]
    )

    print(
        f"Generated embeddings for {len(chunks)} chunks"
    )

    # ==================================================
    # Save Document
    # ==================================================

    print("\nSaving document...")
    print("=" * 80)

    document_store = DocumentStore()

    document_dir = document_store.save(
        document,
        chunks
    )

    print(
        f"Saved document to: {document_dir}"
    )

    # ==================================================
    # Index into Chroma
    # ==================================================

    print("\nIndexing into Chroma...")
    print("=" * 80)

    vector_store = ChromaStore()

    vector_store.add_chunks(
        chunks,
        embeddings
    )

    print(
        f"Indexed {len(chunks)} chunk(s)"
    )

    print(
        "\nIngestion completed successfully."
    )


def main():

    parser = argparse.ArgumentParser(
        description="Ingest an image into RAGForge."
    )

    parser.add_argument(
        "input",
        help="Path to the image"
    )

    args = parser.parse_args()

    ingest(
        args.input
    )


if __name__ == "__main__":
    main()