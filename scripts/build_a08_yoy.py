"""Build tableau/A08/a08_yoy_month.csv for Fig 8. Does not change the locked source."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "lapd_a1_clean.csv"
OUT_DIR = ROOT / "tableau" / "A08"
OUT = OUT_DIR / "a08_yoy_month.csv"

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
YEAR_TOTALS = {
    2020: 199_847,
    2021: 209_876,
    2022: 235_259,
    2023: 232_345,
    2024: 127_567,
}


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(f"missing clean file: {SRC}")

    counts: dict[tuple[int, int], int] = defaultdict(int)
    with SRC.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            counts[int(row["year_occ"]), int(row["month_occ"])] += 1

    for year, expected in YEAR_TOTALS.items():
        got = sum(counts[year, month] for month in range(1, 13))
        if got != expected:
            raise AssertionError(f"{year} total {got}, expected {expected}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[tuple[int, int, str, int, int, float, str]] = []
    with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(
            [
                "Year",
                "Month num",
                "Month",
                "Reports",
                "Prior year reports",
                "YoY change",
                "Coverage",
            ]
        )
        for year in (2021, 2022, 2023, 2024):
            coverage = "2024 transition" if year == 2024 else "Full year"
            for month in range(1, 13):
                cur = counts[year, month]
                prior = counts[year - 1, month]
                if prior <= 0:
                    raise AssertionError(f"no prior for {year}-{month}")
                yoy = (cur - prior) / prior
                w.writerow(
                    [
                        year,
                        month,
                        MONTHS[month - 1],
                        cur,
                        prior,
                        f"{yoy:.6f}",
                        coverage,
                    ]
                )
                rows.append((year, month, MONTHS[month - 1], cur, prior, yoy, coverage))

    if len(rows) != 48:
        raise AssertionError(f"row count {len(rows)}")
    if any(year == 2020 for year, *_ in rows):
        raise AssertionError("2020 must not be a change row")
    if any(yoy <= 0 for year, month, _n, _c, _p, yoy, _cov in rows if year == 2022):
        raise AssertionError("2022 should be up in every month")
    apr_2024 = next(r[5] for r in rows if r[0] == 2024 and r[1] == 4)
    dec_2024 = next(r[5] for r in rows if r[0] == 2024 and r[1] == 12)
    if apr_2024 > -0.30:
        raise AssertionError(f"2024 Apr YoY {apr_2024}")
    if dec_2024 > -0.70:
        raise AssertionError(f"2024 Dec YoY {dec_2024}")
    spring_2021 = [r[5] for r in rows if r[0] == 2021 and r[1] in (3, 4)]
    if any(val <= 0 for val in spring_2021):
        raise AssertionError("2021 Mar-Apr should rebound above the prior year")

    print(f"wrote {OUT}  rows={len(rows)}")
    print("Year  " + "  ".join(f"{name:>6}" for name in MONTHS))
    for year in (2021, 2022, 2023, 2024):
        cells = [f"{r[5]:+6.1%}" for r in rows if r[0] == year]
        print(f"{year}  " + "  ".join(cells))


if __name__ == "__main__":
    main()
