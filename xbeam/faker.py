from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.axes import Axes
from PIL import Image, ImageFilter

from .puzzle import Puzzle


def _draw_square(ax: Axes, i: int, j: int, color=tuple):
    ax.add_patch(
        plt.Polygon(
            [(j, i), (j, i - 1), (j + 1, i - 1), (j + 1, i)],
            edgecolor=None,
            facecolor=color,
        )
    )


def plot_grid(puz: Puzzle, ax: Axes = None) -> Axes:
    rows, cols = puz.boxes.shape
    if ax is None:
        ax = plt.subplots(1)[1]
    ax.set_xlim([0, cols])
    ax.set_ylim([0, rows])
    ax.set_aspect(1)

    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))
    ax.grid(True, which="major", color="black")
    ax.tick_params(
        bottom=False, left=False, labelbottom=False, labelleft=False
    )

    for i in range(rows):
        for j in range(cols):
            if puz.boxes[i, j] == 0:
                _draw_square(ax, rows - i, j, (0, 0, 0))
            if puz.shades is not None and puz.shades[i, j]:
                _draw_square(ax, rows - i, j, (0, 0, 0, 0.3))
            if puz.circles is not None and puz.circles[i, j]:
                ax.add_patch(
                    patches.Arc(
                        (j + 0.5, rows - i - 0.5),
                        0.95,
                        0.95,
                        angle=160,
                        theta1=0,
                        theta2=300 if puz.numbers[i, j] > 0 else 360,
                        edgecolor=(0, 0, 0),
                        facecolor="none",
                        linewidth=0.75,
                    )
                )
            if puz.numbers[i, j] > 0:
                ax.text(
                    j + 0.05,
                    rows - i - 0.05,
                    str(puz.numbers[i, j]),
                    fontsize=5,  # 4 - 6
                    fontweight=500,
                    horizontalalignment="left",
                    verticalalignment="top",
                )

    return ax


def puz2img(puz: Puzzle) -> Image:
    f, ax = plt.subplots(1)
    f.set_size_inches(8.5, 11)
    plot_grid(puz, ax)
    b = BytesIO()
    plt.savefig(
        b,
        format="png",
        transparent=True,
        dpi=300,
        # bbox_inches="tight",
        # pad_inches=2,
    )
    plt.close(f)
    b.seek(0)
    img = Image.open(b)
    img.thumbnail((1500, 1500))
    return img


def paperize(img: Image) -> Image:
    paper = np.clip(np.random.normal(0.9, 0.05, img.size[::-1]), 0, 1)
    base = (
        Image.fromarray((paper * 255).astype("uint8"))
        .filter(ImageFilter.GaussianBlur(radius=1))
        .convert("RGBA")
    )
    return Image.alpha_composite(base, img)


if __name__ == "__main__":
    import json
    from pathlib import Path

    from .parse_xwordinfo import parse

    with open(Path(__file__).parents[1] / "data/2021-09-12.json") as f:
        paperize(puz2img(parse(json.load(f)))).save(
            "/Users/kevin/Desktop/fig1.png"
        )

    with open(Path(__file__).parents[1] / "data/2021-09-14.json") as f:
        paperize(puz2img(parse(json.load(f)))).save(
            "/Users/kevin/Desktop/fig2.png"
        )
