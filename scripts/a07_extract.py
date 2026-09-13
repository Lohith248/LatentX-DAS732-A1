"""Slim Fig 7 extract from lapd_a1_clean.csv. Does not change the locked source."""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "lapd_a1_clean.csv"
OUT_DIR = ROOT / "tableau" / "A07"
CSV_NAME = "a07_delay.csv"

KEEP = (
    "DR_NO",
    "Date Rptd",
    "delay_days",
    "delay_bucket",
    "crime_family",
    "year_occ",
)

BUCKETS = ("same day", "1-7 days", "8-30 days", "31+ days")
FAMILY_ORDER = (
    "Aggravated assault, robbery & homicide",
    "Simple assault",
    "Other",
    "Vandalism",
    "Burglary",
    "Other theft",
    "Sex offences",
    "Vehicle theft",
    "Theft from vehicle",
    "Identity theft & fraud",
)
EXPECTED_2025 = {
    2020: 2,
    2021: 5,
    2022: 4,
    2023: 11,
    2024: 72,
}


def _median(values: list[int]) -> float:
    ordered = sorted(values)
    n = len(ordered)
    if n == 0:
        raise ValueError("empty median")
    mid = n // 2
    if n % 2:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def build_extract() -> Path:
    if not SRC.exists():
        raise FileNotFoundError(f"missing locked clean file: {SRC}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / CSV_NAME

    n = 0
    delay0 = 0
    delay1 = 0
    over60 = 0
    none_delay = 0
    occ_years: Counter[int] = Counter()
    rptd_years: Counter[int] = Counter()
    xy: Counter[tuple[int, int]] = Counter()
    fam_days: dict[str, list[int]] = defaultdict(list)
    fam_same: Counter[str] = Counter()
    buckets: Counter[str] = Counter()

    with SRC.open("r", encoding="utf-8-sig", newline="") as src_fh:
        reader = csv.DictReader(src_fh)
        missing = [c for c in KEEP if c not in (reader.fieldnames or [])]
        if missing:
            raise KeyError(f"clean file missing columns: {missing}")
        with out_path.open("w", encoding="utf-8-sig", newline="") as out_fh:
            writer = csv.DictWriter(out_fh, fieldnames=list(KEEP), lineterminator="\n")
            writer.writeheader()
            for row in reader:
                n += 1
                delay_text = (row.get("delay_days") or "").strip()
                if delay_text == "":
                    none_delay += 1
                    continue
                delay = int(delay_text)
                if delay == 0:
                    delay0 += 1
                elif delay == 1:
                    delay1 += 1
                if delay > 60:
                    over60 += 1
                family = row["crime_family"]
                bucket = row["delay_bucket"]
                occ = int(row["year_occ"])
                rptd = int((row.get("Date Rptd") or "0000")[:4])
                occ_years[occ] += 1
                rptd_years[rptd] += 1
                xy[occ, rptd] += 1
                fam_days[family].append(delay)
                buckets[bucket] += 1
                if bucket == "same day":
                    fam_same[family] += 1
                writer.writerow({key: row[key] for key in KEEP})

    if n != 1_004_894:
        raise AssertionError(f"unexpected clean row count {n}")
    if none_delay != 0:
        raise AssertionError(f"blank delay_days rows: {none_delay}")
    if delay0 != 482_015:
        raise AssertionError(f"delay 0 count {delay0}")
    if delay1 != 222_376:
        raise AssertionError(f"delay 1 count {delay1}")
    if over60 != 37_026:
        raise AssertionError(f">60 count {over60}")
    if occ_years[2025] != 0:
        raise AssertionError("2025 occurrence year present")
    if set(occ_years) != {2020, 2021, 2022, 2023, 2024}:
        raise AssertionError(f"occ years {sorted(occ_years)}")
    if 2025 not in rptd_years:
        raise AssertionError("missing 2025 report year")
    if rptd_years[2025] != 94:
        raise AssertionError(f"2025 filings {rptd_years[2025]}")
    for occ, expected in EXPECTED_2025.items():
        got = xy[occ, 2025]
        if got != expected:
            raise AssertionError(f"{occ} x 2025 = {got}, expected {expected}")
    for bucket in BUCKETS:
        if buckets[bucket] <= 0:
            raise AssertionError(f"empty bucket {bucket}")
    ranked = sorted(
        fam_days,
        key=lambda fam: fam_same[fam] / len(fam_days[fam]),
        reverse=True,
    )
    if tuple(ranked) != FAMILY_ORDER:
        raise AssertionError(f"family same-day order {ranked}")
    if _median(fam_days["Identity theft & fraud"]) != 7:
        raise AssertionError("identity theft median is not 7")
    if _median(fam_days["Simple assault"]) != 0:
        raise AssertionError("simple assault median is not 0")
    if _median(fam_days["Aggravated assault, robbery & homicide"]) != 0:
        raise AssertionError("aggravated family median is not 0")
    if delay0 <= delay1:
        raise AssertionError("0-day bar does not dominate")
    if delay1 <= over60:
        raise AssertionError("1-day bar is not substantial vs >60")

    stats_path = OUT_DIR / "a07_extract_stats.txt"
    lines = [
        f"rows {n}",
        f"delay0 {delay0}",
        f"delay1 {delay1}",
        f"over60 {over60}",
        f"filings_2025 {rptd_years[2025]}",
        f"csv {out_path} bytes {out_path.stat().st_size}",
    ]
    stats_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path
