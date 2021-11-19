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
            if puz.numbers[i, j] > 0:
                ax.text(
                    j + 0.05,
                    rows - i - 0.03,
                    str(puz.numbers[i, j]),
                    fontsize=6,
                    fontweight=500,
                    horizontalalignment="left",
                    verticalalignment="top",
                    rasterized=True,
                )

    return ax
