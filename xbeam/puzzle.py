from typing import NamedTuple

import numpy as np


class Puzzle(NamedTuple):
    boxes: np.ndarray  # 1 indicates blank space
    numbers: np.ndarray
    circles: np.ndarray | None
    shades: np.ndarray | None
    title: str | None
    across: dict[int, str]
    down: dict[int, str] | None


def validate_grid_numbers(puz: Puzzle):
    # Sometimes the constructors make a real doozy and this "fails".
    # See https://www.xwordinfo.com/Crossword?date=11/29/2018
    # for an example
    numbers = puz.numbers
    boxes = puz.boxes
    assert (np.diff(numbers[numbers > 0]) > 0).all()
    for i in range(boxes.shape[0]):
        for j in range(boxes.shape[1]):
            if boxes[i, j]:
                if i == 0:
                    if (numbers[i : i + 3, j] == 1).all():
                        assert numbers[i, j] > 0
                if j == 0:
                    if (numbers[i, j : j + 3] == 1).all():
                        assert numbers[i, j] > 0
                if i > 0:
                    if boxes[i - 1, j] == 0:
                        if (
                            i + 3 < boxes.shape[0]
                            and (boxes[i : i + 3, j] == 1).all()
                        ):
                            assert numbers[i, j] > 0
                if j > 0:
                    if boxes[i, j - 1] == 0:
                        if (
                            j + 3 < boxes.shape[1]
                            and (boxes[i, j : j + 3] == 1).all()
                        ):
                            assert numbers[i, j] > 0
            elif numbers[i, j] > 0:
                raise AssertionError
