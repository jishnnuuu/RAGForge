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


IMAGE_PATH = "samples/placement_2024.jpg"


def main():

    print("\nLoading Surya...")
    print("=" * 80)

    surya_service = SuryaService()

    print("\nExtracting document...")
    print("=" * 80)

    extractor = ImageExtractor(
        surya_service
    )

    document = extractor.extract(
        IMAGE_PATH
    )

    print("Document extracted successfully.")

    print("\nProcessing figures...")
    print("=" * 80)

    figure_processor = FigureProcessor()

    figures = figure_processor.process(
        document
    )

    print(f"Detected {len(figures)} figure(s)\n")

    for idx, figure in enumerate(
        figures,
        start=1
    ):

        print(
            f"Figure {idx}: "
            f"{figure['path']}"
        )

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
            f"Type       : {chunk.chunk_type}"
        )

        print(
            f"Confidence : "
            f"{chunk.confidence:.3f}"
        )

        print(
            f"Content    : "
            f"{chunk.content[:200]}"
        )

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
            f,
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