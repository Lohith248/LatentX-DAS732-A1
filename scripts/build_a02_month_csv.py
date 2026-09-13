"""Build tableau/A01/a02_month_2024_vs_avg.csv for Fig 2. Does not change the locked source."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "lapd_a1_clean.csv"
OUT = ROOT / "tableau" / "A01" / "a02_month_2024_vs_avg.csv"

MONTHS = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


def main() -> None:
    counts: dict[tuple[int, int], int] = defaultdict(int)
    with SRC.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            year = int(row["year_occ"])
            month = int(row["month_occ"])
            counts[year, month] += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    total_2024 = 0
    with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(
            [
                "Month num",
                "Month",
                "2024 reports",
                "Avg 2020-2023",
                "Pct of average",
                "Coverage",
            ]
        )
        for month in range(1, 13):
            y2024 = counts[2024, month]
            avg = round(
                sum(counts[year, month] for year in (2020, 2021, 2022, 2023)) / 4
            )
            pct = round(100 * y2024 / avg) if avg else 0
            coverage = (
                "Jan-Mar (still on this system)"
                if month <= 3
                else "Apr-Dec (after LAPD left)"
            )
            w.writerow([month, MONTHS[month - 1], y2024, avg, pct, coverage])
            rows.append((month, y2024, avg, pct, coverage))
            total_2024 += y2024

    assert len(rows) == 12
    assert total_2024 == 127_567
    assert 90 <= rows[0][3] <= 110, rows[0]
    assert 85 <= rows[1][3] <= 105, rows[1]
    assert 80 <= rows[2][3] <= 100, rows[2]
    assert 55 <= rows[3][3] <= 75, rows[3]
    assert rows[11][3] < 40, rows[11]
    print(f"wrote {OUT}  2024 total={total_2024}")
    for month, y2024, avg, pct, coverage in rows:
        print(f"  {MONTHS[month - 1]:>3}  2024={y2024:5d}  avg={avg:5d}  {pct:3d}%  {coverage}")


if __name__ == "__main__":
    main()
