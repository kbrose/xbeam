import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from puzzle import Puzzle


def plot_grid(puz: Puzzle) -> Axes:
    rows, cols = puz.boxes.shape
    ax = plt.subplots(1)[1]
    ax.imshow(
        puz.boxes[::-1, :],
        cmap="gray",
        origin="lower",
        extent=(0, cols, 0, rows),
    )

    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))
    ax.grid(True, which="major", color="black")
    ax.tick_params(
        bottom=False, left=False, labelbottom=False, labelleft=False
    )

    for i in range(rows):
        for j in range(cols):
            if puz.shades is not None and puz.shades[i, j]:
                ax.add_patch(
                    plt.Polygon(
                        [
                            (j, rows - i),
                            (j, rows - i - 1),
                            (j + 1, rows - i - 1),
                            (j + 1, rows - i),
                        ],
                        edgecolor=None,
                        facecolor=(0, 0, 0, 0.3),
                    )
                )
            if puz.circles is not None and puz.circles[i, j]:
                ax.add_patch(
                    plt.Circle(
                        (j + 0.5, rows - i - 0.5),
                        0.49,
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
                    rasterized=True,
                )

    return ax


if __name__ == "__main__":
    from parse_xwordinfo import parse
    import json
    from pathlib import Path

    with open(Path(__file__).parents[1] / "data/2021-09-12.json") as f:
        plot_grid(parse(json.load(f)))

    # with open(Path(__file__).parents[1] / "data/2021-09-14.json") as f:
    #     plot_grid(parse(json.load(f)))

    plt.show()
