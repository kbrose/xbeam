from datetime import datetime, timedelta
from pathlib import Path
import time
import json

import requests


def getpuz(date: datetime):
    url = "https://www.xwordinfo.com/Crossword?date={month}/{day}/{year}"
    try:
        result = requests.get(
            "https://www.xwordinfo.com/JSON/Data.aspx",
            params={
                "date": f"{date.month}/{date.day}/{date.year}",
                "format": "text",
            },
            headers={"Referer": "https://www.xwordinfo.com/JSON/"},
        )
        return result.json()
    except Exception:
        print()
        raise


def scrape(
    earliest: datetime, latest: datetime, folder: Path, overwrite=False
):
    n = (latest - earliest).days
    print("|" + " " * 50 + "|\r", end="")
    for delta in range(n):
        date = latest - timedelta(days=delta)
        dest = folder / (date.isoformat()[:10] + ".json")
        if overwrite or not dest.is_file():
            puz = getpuz(date)
            with open(dest, "w") as f:
                json.dump(puz, f)
            time.sleep(0.1)
        progress = int(50 * delta / n)
        print(
            "\r|"
            + "-" * progress
            + " " * (50 - progress)
            + f"| {delta/n:.1%}",
            end="",
        )
    print()


if __name__ == "__main__":
    dest = Path(__file__).parents[1] / "data"
    dest.mkdir(exist_ok=True)
    scrape(datetime(2010, 1, 1), datetime(2021, 11, 14), dest)
