"""Download and check the official LAPD 2020-2024 crime CSV."""
from __future__ import annotations

import csv
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Crime_Data_from_2020_to_2024.csv"
REQUIRED = {
    "DR_NO",
    "Date Rptd",
    "DATE OCC",
    "TIME OCC",
    "AREA",
    "AREA NAME",
    "Crm Cd Desc",
    "LAT",
    "LON",
}


def download() -> None:
    req = Request(URL, headers={"User-Agent": "DAS732-LatentX/1.0"})
    with urlopen(req, timeout=600) as resp, OUT.open("wb") as fh:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            fh.write(chunk)


def parse_dt(value: str):
    text = (value or "").strip()
    for fmt in ("%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def check() -> dict:
    if not OUT.exists() or OUT.stat().st_size < 50_000_000:
        raise SystemExit(f"download too small or missing: {OUT} size={OUT.stat().st_size if OUT.exists() else 0}")
    with OUT.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = reader.fieldnames or []
        missing = REQUIRED - set(fields)
        if missing:
            raise SystemExit(f"missing columns: {sorted(missing)}")
        n = 0
        occ_min = occ_max = rptd_max = None
        zero_geo = 0
        year_counts: dict[int, int] = {}
        for row in reader:
            n += 1
            occ = parse_dt(row.get("DATE OCC") or "")
            rptd = parse_dt(row.get("Date Rptd") or "")
            if occ:
                occ_min = occ if occ_min is None or occ < occ_min else occ_min
                occ_max = occ if occ_max is None or occ > occ_max else occ_max
                year_counts[occ.year] = year_counts.get(occ.year, 0) + 1
            if rptd:
                rptd_max = rptd if rptd_max is None or rptd > rptd_max else rptd
            try:
                lat = float(row.get("LAT") or 0)
                lon = float(row.get("LON") or 0)
            except ValueError:
                lat = lon = 0
            if lat == 0 and lon == 0:
                zero_geo += 1
    return {
        "path": str(OUT),
        "bytes": OUT.stat().st_size,
        "rows": n,
        "columns": len(fields),
        "date_occ_min": occ_min.isoformat() if occ_min else None,
        "date_occ_max": occ_max.isoformat() if occ_max else None,
        "date_rptd_max": rptd_max.isoformat() if rptd_max else None,
        "occ_year_counts": dict(sorted(year_counts.items())),
        "zero_latlon_rows": zero_geo,
        "checked_at": datetime.now().isoformat(timespec="seconds"),
    }


def main() -> None:
    if "--check-only" not in sys.argv:
        print(f"downloading {URL}")
        download()
    info = check()
    print(info)


if __name__ == "__main__":
    main()
