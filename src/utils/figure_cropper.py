from pathlib import Path

from PIL import Image


class FigureCropper:

    def __init__(
        self,
        output_dir: str = "outputs/figures"
    ):

        self.output_dir = Path(
            output_dir
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def crop(
        self,
        image: Image.Image,
        bbox: list[float],
        figure_name: str,
        padding: int = 20
    ) -> str:

        x1, y1, x2, y2 = bbox

        x1 = max(
            0,
            int(x1 - padding)
        )

        y1 = max(
            0,
            int(y1 - padding)
        )

        x2 = min(
            image.width,
            int(x2 + padding)
        )

        y2 = min(
            image.height,
            int(y2 + padding)
        )

        cropped = image.crop(
            (
                x1,
                y1,
                x2,
                y2
            )
        )

        save_path = (
            self.output_dir /
            f"{figure_name}.png"
        )

        cropped.save(
            save_path
        )

        return str(save_path)