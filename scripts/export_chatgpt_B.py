"""Small Person-B extracts for ChatGPT. Not a row-split of the crime file."""
from __future__ import annotations

import csv
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "lapd_a1_clean.csv"
OUT = ROOT / "chatgpt_B"
OUT.mkdir(exist_ok=True)

VIOLENT = {
    "Aggravated assault, robbery & homicide",
    "Simple assault",
}


def write_counts(path: Path, header: list[str], counter: Counter) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for key, n in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])):
            if isinstance(key, tuple):
                w.writerow([*key, n])
            else:
                w.writerow([key, n])


def main() -> None:
    area_year: Counter = Counter()
    area_month: Counter = Counter()
    area_family: Counter = Counter()
    area_hour: Counter = Counter()
    district: Counter = Counter()
    bureau_of: dict[str, str] = {}
    map_pool: list[list[str]] = []
    rng = random.Random(732)
    n_map = 0

    with SRC.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            area = row["AREA NAME"]
            bureau = row["bureau"]
            bureau_of[area] = bureau
            year = int(row["year_occ"] or 0)
            month = int(row["month_occ"] or 0)
            hour = row["hour_occ"]
            fam = row["crime_family"]
            area_year[(area, bureau, year)] += 1
            area_month[(area, bureau, year, month)] += 1
            area_hour[(area, bureau, hour)] += 1
            if 2020 <= year <= 2023:
                area_family[(area, bureau, fam)] += 1
                district[(row["Rpt Dist No"], area, bureau)] += 1
            if row.get("map_sample") == "1" and row.get("LAT") and row.get("LON"):
                n_map += 1
                h = int(hour) if hour != "" else -1
                rec = [
                    row["LAT"],
                    row["LON"],
                    area,
                    bureau,
                    row["hour_occ"],
                    fam,
                    row["year_occ"],
                    "night" if h >= 18 or 0 <= h <= 5 else "day",
                ]
                if len(map_pool) < 40_000:
                    map_pool.append(rec)
                else:
                    j = rng.randrange(n_map)
                    if j < 40_000:
                        map_pool[j] = rec

    write_counts(
        OUT / "B_area_year.csv",
        ["AREA NAME", "bureau", "year_occ", "n"],
        area_year,
    )
    write_counts(
        OUT / "B_area_month.csv",
        ["AREA NAME", "bureau", "year_occ", "month_occ", "n"],
        area_month,
    )
    write_counts(
        OUT / "B_area_family_2020_2023.csv",
        ["AREA NAME", "bureau", "crime_family", "n"],
        area_family,
    )
    write_counts(
        OUT / "B_area_hour.csv",
        ["AREA NAME", "bureau", "hour_occ", "n"],
        area_hour,
    )
    write_counts(
        OUT / "B_district_2020_2023.csv",
        ["Rpt Dist No", "AREA NAME", "bureau", "n"],
        district,
    )

    scatter_path = OUT / "B_division_scatter_2020_2023.csv"
    tot: Counter = Counter()
    viol: Counter = Counter()
    y2020: Counter = Counter()
    y2023: Counter = Counter()
    for (area, bureau, year), n in area_year.items():
        if 2020 <= year <= 2023:
            tot[area] += n
        if year == 2020:
            y2020[area] = n
        if year == 2023:
            y2023[area] = n
    for (area, bureau, fam), n in area_family.items():
        if fam in VIOLENT:
            viol[area] += n
    with scatter_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(
            ["AREA NAME", "bureau", "n_2020_2023", "pct_violent", "pct_change_2020_2023"]
        )
        for area, n in tot.most_common():
            pct_v = round(100 * viol[area] / n, 2) if n else 0
            ch = round(100 * (y2023[area] - y2020[area]) / y2020[area], 2) if y2020[area] else ""
            w.writerow([area, bureau_of[area], n, pct_v, ch])

    pts = OUT / "B_map_points_40k.csv"
    with pts.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(
            ["LAT", "LON", "AREA NAME", "bureau", "hour_occ", "crime_family", "year_occ", "day_night"]
        )
        w.writerows(map_pool)

    print("wrote", OUT)
    for p in sorted(OUT.glob("*.csv")):
        print(p.name, p.stat().st_size)


if __name__ == "__main__":
    main()
