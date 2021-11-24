import html
import json
import time
from pathlib import Path

import numpy as np

from .puzzle import Puzzle


def parse(data: dict) -> Puzzle:
    num_rows, num_cols = data["size"]["rows"], data["size"]["cols"]

    boxes = np.zeros((num_rows, num_cols), dtype="uint8")
    for i, entry in enumerate(data["grid"]):
        boxes[i // num_cols, i % num_cols] = entry != "."

    numbers = np.zeros((num_rows, num_cols), dtype="uint8")
    for i, entry in enumerate(data["gridnums"]):
        numbers[i // num_cols, i % num_cols] = entry

    circles = None
    if data["circles"]:
        circles = np.zeros((num_rows, num_cols), dtype="uint8")
        for i, entry in enumerate(data["circles"]):
            circles[i // num_cols, i % num_cols] = entry

    shades = None
    if data["shadecircles"] == "true":
        shades = circles
        circles = None

    title = data["title"] if data["hastitle"] else None

    across = {
        int(clue.split(". ")[0]): html.unescape(clue.split(". ", 1)[1])
        for clue in data["clues"]["across"]
    }
    down = None
    if not data["uniclue"]:
        down = {
            int(clue.split(". ")[0]): html.unescape(clue.split(". ", 1)[1])
            for clue in data["clues"]["down"]
        }

    return Puzzle(
        boxes=boxes,
        numbers=numbers,
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
        files = list((Path(__file__).parents[1] / "data").glob("*.json"))
        for f in files:
            total += 1
            if has_succeeded.get(f):
                continue
            try:
                parse(json.loads(f.read_text()))
            except Exception:
                errors += 1
            else:
                has_succeeded[f] = True
        print(f"\rerror rate: {errors / total:.1%} ({errors})", end="")
        time.sleep(0.5)


if __name__ == "__main__":
    monitor_parse_success()
