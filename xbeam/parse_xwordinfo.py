from pathlib import Path
from typing import NamedTuple
import time

import bs4
import numpy as np


class Puzzle(NamedTuple):
    boxes: np.ndarray
    # numbers: np.ndarray
    circles: np.ndarray | None
    shades: np.ndarray | None
    title: str | None
    across: dict[int, tuple[str, str]]  # num -> (clue, answer)
    down: dict[int, tuple[str, str]]  # num -> (clue, answer)


def extract_grid_info(table: bs4.element.Tag):
    num_rows = len(table.find_all("tr"))
    num_cols = len(table.find_all("tr")[0].find_all("td"))

    boxes = np.zeros((num_rows, num_cols), dtype="uint8")
    circles = np.zeros((num_rows, num_cols), dtype="uint8")
    shades = np.zeros((num_rows, num_cols), dtype="uint8")

    for i, tr in enumerate(table.find_all("tr")):
        for j, td in enumerate(tr.find_all("td")):
            td_class = td.get("class")

            if td_class == ["black"]:
                boxes[i, j] = 1
            elif td_class == ["bigcircle"]:
                circles[i, j] = 1
            elif td_class == ["shade"]:
                shades[i, j] = 1

    return boxes, circles, shades


def extract_clues_and_answers(
    numclue: bs4.element.Tag,
) -> dict[int, tuple[str, str]]:
    children = numclue.contents
    clues = {}
    for i in range(0, len(children), 2):
        number = int(children[i].string)
        clue = str(children[i + 1].contents[0].string.removesuffix(" : "))
        answer = str(children[i + 1].contents[1].string)
        clues[number] = (clue, answer)
    return clues


def parse(html: str):
    parsed = bs4.BeautifulSoup(html, "html.parser")
    table = parsed.find(id="PuzTable")

    boxes, circles, shades = extract_grid_info(table)

    title = parsed.find(id="PuzTitle").string

    across = extract_clues_and_answers(
        parsed.find(id="ACluesPan").find(
            lambda tag: tag.get("class") == ["numclue"]
        )
    )
    down = extract_clues_and_answers(
        parsed.find(id="DCluesPan").find(
            lambda tag: tag.get("class") == ["numclue"]
        )
    )

    return Puzzle(
        boxes=boxes,
        circles=circles,
        shades=shades,
        title=title,
        across=across,
        down=down,
    )


def monitor_parse_success():
    """
    Used to validate scraper is working correctly.
    """
    has_succeeded = {}
    while True:
        total = 0
        errors = 0
        for f in (Path(__file__).parents[1] / "data").glob("*.html"):
            total += 1
            if has_succeeded.get(f):
                continue
            try:
                parse(f.read_text())
            except Exception:
                errors += 1
            else:
                has_succeeded[f] = True
        print(f"\rerror rate: {errors / total:.1%} ({errors})", end="")
        time.sleep(0.5)


if __name__ == "__main__":
    monitor_parse_success()
