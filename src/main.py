from extractors.image_extractor import (
    ImageExtractor
)

from processors.figure_processor import (
    FigureProcessor
)

from processors.figure_filter import (
    FigureFilter
)

from services.surya_service import (
    SuryaService
)


IMAGE_PATH = (
    "samples/placement_2024.jpg"
)


def main():

    print(
        "\nLoading Surya..."
    )

    surya_service = (
        SuryaService()
    )

    print(
        "\nExtracting document..."
    )

    extractor = ImageExtractor(
        surya_service
    )

    document = extractor.extract(
        IMAGE_PATH
    )

    print(
        "\nProcessing figures..."
    )

    figure_processor = (
        FigureProcessor()
    )

    figure_results = (
        figure_processor.process(
            document
        )
    )

    print(
        "\nDetected Figures:"
    )
    print("=" * 80)

    for figure in figure_results:

        print(
            figure["path"]
        )

    print(
        "\nFiltering figures..."
    )
    print("=" * 80)

    filterer = FigureFilter(
        surya_service
    )

    useful_figures = []

    for figure in figure_results:

        informative = (
            filterer.is_informative(
                figure["path"]
            )
        )

        print(
            f"{figure['path']} -> "
            f"{informative}"
        )

        if informative:

            useful_figures.append(
                figure
            )

    print(
        "\nUseful Figures:"
    )
    print("=" * 80)

    for figure in useful_figures:

        print(
            figure["path"]
        )

    with open(
        "outputs/result.json",
        "w"
    ) as f:

        f.write(
            document.model_dump_json(
                indent=4
            )
        )


if __name__ == "__main__":
    main()