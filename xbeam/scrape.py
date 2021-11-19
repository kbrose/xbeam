from datetime import datetime, timedelta
from pathlib import Path
import time
import json

import requests


def getpuz(date: datetime):
    result = requests.get(
        "https://www.xwordinfo.com/JSON/Data.aspx",
        params={
            "date": f"{date.month}/{date.day}/{date.year}",
            "format": "text",
        },
        headers={"Referer": "https://www.xwordinfo.com/JSON/"},
    )
    return result.json()


def scrape(
    earliest: datetime, latest: datetime, folder: Path, overwrite=False
):
    n = (latest - earliest).days
    progbar_size = 60
    print("|" + " " * progbar_size + "|\r", end="")
    for delta in range(n):
        date = latest - timedelta(days=delta)
        dest = folder / (date.isoformat()[:10] + ".json")
        if overwrite or not dest.is_file():
            puz = getpuz(date)
            with open(dest, "w") as f:
                json.dump(puz, f)
            time.sleep(0.5)
        progress = int(progbar_size * delta / n)
        print(
            "\r|"
            + "-" * progress
            + " " * (progbar_size - progress)
            + f"| {delta/n:.2%}",
            end="",
        )
    print()


if __name__ == "__main__":
    dest = Path(__file__).parents[1] / "data"
    dest.mkdir(exist_ok=True)
    scrape(datetime(1979, 1, 1), datetime(2021, 11, 18), dest)
