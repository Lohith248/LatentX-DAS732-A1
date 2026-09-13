"""Build lapd_a1_clean.csv from the locked official LAPD file. Does not change the source CSV."""
from __future__ import annotations

import csv
import json
import random
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "Crime_Data_from_2020_to_2024.csv"
OUT = ROOT / "lapd_a1_clean.csv"
STATS = ROOT / "preprocess_stats.json"
MAP = ROOT / "crime_family_map.csv"

DROP = {
    "Mocodes",
    "Weapon Used Cd",
    "Weapon Desc",
    "Cross Street",
    "Crm Cd 1",
    "Crm Cd 2",
    "Crm Cd 3",
    "Crm Cd 4",
    "Vict Descent",
    "LOCATION",
}

BUREAU = {
    "Central": "Central",
    "Rampart": "Central",
    "Hollenbeck": "Central",
    "Northeast": "Central",
    "Newton": "Central",
    "77th Street": "South",
    "Southwest": "South",
    "Harbor": "South",
    "Southeast": "South",
    "Van Nuys": "Valley",
    "West Valley": "Valley",
    "N Hollywood": "Valley",
    "Foothill": "Valley",
    "Devonshire": "Valley",
    "Mission": "Valley",
    "Topanga": "Valley",
    "Hollywood": "West",
    "Wilshire": "West",
    "West LA": "West",
    "Pacific": "West",
    "Olympic": "West",
}

DATE_FMTS = ("%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y", "%Y-%m-%d")


def parse_date(value: str):
    text = (value or "").strip()
    if not text:
        return None
    for fmt in DATE_FMTS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def to_float(value: str) -> float | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def coords_ok(lat: float | None, lon: float | None) -> bool:
    if lat is None or lon is None:
        return False
    if lat == 0 and lon == 0:
        return False
    return 33.70 <= lat <= 34.35 and -118.70 <= lon <= -118.15


def crime_family(desc: str) -> str:
    d = (desc or "").upper()
    if any(
        x in d
        for x in (
            "IDENTITY",
            "BUNCO",
            "CREDIT CARD",
            "FORGERY",
            "EMBEZZLEMENT",
            "COUNTERFEIT",
            "EXTORTION",
            "UNAUTHORIZED COMPUTER",
            "DOCUMENT WORTHLESS",
            "DEFRAUDING INNKEEPER",
            "DISHONEST EMPLOYEE",
            "INSURANCE FRAUD",
            "BRIBERY",
        )
    ):
        return "Identity theft & fraud"
    if "BURGLARY FROM VEHICLE" in d or "THEFT FROM MOTOR VEHICLE" in d:
        return "Theft from vehicle"
    if "BOAT - STOLEN" in d or "DRIVING WITHOUT OWNER CONSENT" in d:
        return "Vehicle theft"
    if "VEHICLE" in d and ("STOLEN" in d or "ATTEMPT STOLEN" in d):
        return "Vehicle theft"
    if "BURGLARY" in d:
        return "Burglary"
    if "LETTERS, LEWD" not in d and any(
        x in d
        for x in (
            "RAPE",
            "SEXUAL",
            "ORAL COPULATION",
            "SODOMY",
            "INDECENT EXPOSURE",
            "PEEPING",
            "PORNOGRAPHY",
            "INCEST",
            "BEASTIALITY",
            "PIMPING",
            "PANDERING",
            "LEWD/LASCIVIOUS",
            "LEWD CONDUCT",
            "BATTERY WITH SEXUAL CONTACT",
            "SEX OFFENDER",
            "HUMAN TRAFFICKING - COMMERCIAL SEX",
            "SEX,UNLAWFUL",
            "CRM AGNST CHLD",
            "CHILD ANNOYING",
        )
    ):
        return "Sex offences"
    if "VANDALISM" in d or d == "ARSON" or "TELEPHONE PROPERTY - DAMAGE" in d:
        return "Vandalism"
    if any(
        x in d
        for x in (
            "BATTERY - SIMPLE",
            "INTIMATE PARTNER - SIMPLE",
            "OTHER ASSAULT",
            "CHILD ABUSE (PHYSICAL) - SIMPLE",
            "BATTERY POLICE (SIMPLE)",
            "BATTERY ON A FIREFIGHTER",
        )
    ):
        return "Simple assault"
    if any(
        x in d
        for x in (
            "ASSAULT WITH DEADLY",
            "INTIMATE PARTNER - AGGRAVATED",
            "ROBBERY",
            "HOMICIDE",
            "MANSLAUGHTER",
            "CHILD ABUSE (PHYSICAL) - AGGRAVATED",
            "DISCHARGE FIREARMS",
            "SHOTS FIRED",
            "KIDNAPPING",
            "BRANDISH",
            "LYNCHING",
        )
    ):
        return "Aggravated assault, robbery & homicide"
    if any(
        x in d
        for x in (
            "THEFT",
            "SHOPLIFTING",
            "PICKPOCKET",
            "PURSE SNATCHING",
            "BIKE -",
            "TILL TAP",
            "PETTY THEFT - AUTO",
            "DRUNK ROLL",
        )
    ):
        return "Other theft"
    return "Other"


def premise_family(desc: str) -> str:
    d = (desc or "").upper()
    if not d:
        return "Other/public"
    if "BUS STOP" in d:
        return "Street/sidewalk/parking"
    if any(
        x in d
        for x in (
            "MTA",
            "TRAIN",
            "TRANSPORTATION",
            "UNION STATION",
            "AIRPORT",
            "VEHICLE, PASSENGER",
            "TAXI",
            "METRO",
            "MTA BUS",
        )
    ):
        return "Vehicle/transit"
    if any(
        x in d
        for x in (
            "STREET",
            "SIDEWALK",
            "PARKING",
            "ALLEY",
            "DRIVEWAY",
            "PARK/PLAYGROUND",
            "BEACH",
            "YARD (",
            "OTHER/OUTSIDE",
            "TRANSIENT ENCAMPMENT",
            "FREEWAY",
        )
    ):
        return "Street/sidewalk/parking"
    if any(
        x in d
        for x in (
            "DWELLING",
            "RESIDENCE",
            "CONDO",
            "APARTMENT",
            "PORCH",
            "GARAGE/CARPORT",
            "HOTEL",
            "MOTEL",
            "GROUP HOME",
            "MOBILE HOME",
            "NURSING",
            "CONVALESCENT",
            "TRANSITIONAL HOUSING",
            "HALFWAY",
            "SINGLE FAMILY",
            "MULTI-UNIT",
        )
    ):
        return "Residence"
    if any(
        x in d
        for x in (
            "STORE",
            "MARKET",
            "MART",
            "RESTAURANT",
            "BANK",
            "OFFICE",
            "GAS STATION",
            "GYM",
            "BAR/",
            "NIGHT CLUB",
            "HOSPITAL",
            "SCHOOL",
            "COLLEGE",
            "CHURCH",
            "WAREHOUSE",
            "CONSTRUCTION",
            "SHOPPING MALL",
            "THE GROVE",
            "LAUNDROMAT",
            "COFFEE",
            "LIBRARY",
            "BEAUTY",
            "SHOP",
            "ATM",
            "OTHER BUSINESS",
            "OTHER STORE",
        )
    ):
        return "Business"
    return "Other/public"


def delay_bucket(days: int | None) -> str:
    if days is None:
        return ""
    if days <= 0:
        return "same day"
    if days <= 7:
        return "1-7 days"
    if days <= 30:
        return "8-30 days"
    return "31+ days"


def age_bin(age: int | None) -> str:
    if age is None:
        return ""
    lo = (age // 5) * 5
    return f"{lo}-{lo + 4}"


def parse_time(value: str) -> int | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        n = int(float(text))
    except ValueError:
        return None
    hour = n // 100
    if 0 <= hour <= 23:
        return hour
    return None


def pass_sample_indices() -> set[int]:
    ok: list[int] = []
    with SRC.open("r", encoding="utf-8-sig", newline="") as fh:
        for i, row in enumerate(csv.DictReader(fh)):
            lat = to_float(row.get("LAT") or "")
            lon = to_float(row.get("LON") or "")
            if coords_ok(lat, lon):
                ok.append(i)
    rng = random.Random(732)
    n = min(200_000, len(ok))
    return set(rng.sample(ok, n)), len(ok)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing source: {SRC}")

    sample, n_ok_coords = pass_sample_indices()
    keep_fields: list[str] | None = None
    extra = [
        "year_occ",
        "month_occ",
        "hour_occ",
        "is_noon_default",
        "is_first_of_month",
        "delay_days",
        "delay_bucket",
        "has_coords",
        "map_sample",
        "bureau",
        "vict_age_clean",
        "age_bin",
        "vict_sex_clean",
        "victim_recorded",
        "crime_family",
        "premise_family",
    ]
    stats = {
        "rows": 0,
        "year_occ": Counter(),
        "month_2024": Counter(),
        "crime_family": Counter(),
        "premise_family": Counter(),
        "bureau": Counter(),
        "vict_sex_clean": Counter(),
        "delay_bucket": Counter(),
        "age_le0": 0,
        "age_gt99": 0,
        "age_kept": 0,
        "coords_ok": 0,
        "coords_nulled": 0,
        "map_sample": 0,
        "noon_default": 0,
        "first_of_month": 0,
        "other_crimes": Counter(),
        "desc_to_family": {},
    }

    with SRC.open("r", encoding="utf-8-sig", newline="") as fh, OUT.open(
        "w", encoding="utf-8", newline=""
    ) as out:
        reader = csv.DictReader(fh)
        fields = reader.fieldnames or []
        keep_fields = [c for c in fields if c not in DROP] + extra
        writer = csv.DictWriter(out, fieldnames=keep_fields, extrasaction="ignore")
        writer.writeheader()
        for i, row in enumerate(reader):
            occ = parse_date(row.get("DATE OCC") or "")
            rptd = parse_date(row.get("Date Rptd") or "")
            row["DATE OCC"] = occ.isoformat() if occ else ""
            row["Date Rptd"] = rptd.isoformat() if rptd else ""
            row["year_occ"] = occ.year if occ else ""
            row["month_occ"] = occ.month if occ else ""

            t = (row.get("TIME OCC") or "").strip()
            try:
                t_int = int(float(t)) if t else None
            except ValueError:
                t_int = None
            hour = parse_time(t)
            row["hour_occ"] = hour if hour is not None else ""
            row["is_noon_default"] = 1 if t_int == 1200 else 0
            row["is_first_of_month"] = 1 if occ and occ.day == 1 else 0
            if row["is_noon_default"]:
                stats["noon_default"] += 1
            if row["is_first_of_month"]:
                stats["first_of_month"] += 1

            if occ and rptd:
                days = (rptd - occ).days
                row["delay_days"] = days
                row["delay_bucket"] = delay_bucket(days)
            else:
                row["delay_days"] = ""
                row["delay_bucket"] = ""

            lat = to_float(row.get("LAT") or "")
            lon = to_float(row.get("LON") or "")
            ok = coords_ok(lat, lon)
            row["has_coords"] = 1 if ok else 0
            if ok:
                row["LAT"] = f"{lat:.4f}"
                row["LON"] = f"{lon:.4f}"
                stats["coords_ok"] += 1
            else:
                row["LAT"] = ""
                row["LON"] = ""
                stats["coords_nulled"] += 1
            row["map_sample"] = 1 if i in sample else 0
            if row["map_sample"]:
                stats["map_sample"] += 1

            area = (row.get("AREA NAME") or "").strip()
            row["AREA NAME"] = area
            row["bureau"] = BUREAU.get(area, "Unknown")

            try:
                age_raw = int(float((row.get("Vict Age") or "").strip() or "nan"))
            except ValueError:
                age_raw = None
            if age_raw is None:
                row["vict_age_clean"] = ""
                row["age_bin"] = ""
            elif age_raw <= 0:
                row["vict_age_clean"] = ""
                row["age_bin"] = ""
                stats["age_le0"] += 1
            elif age_raw > 99:
                row["vict_age_clean"] = ""
                row["age_bin"] = ""
                stats["age_gt99"] += 1
            else:
                row["vict_age_clean"] = age_raw
                row["age_bin"] = age_bin(age_raw)
                stats["age_kept"] += 1

            sex = (row.get("Vict Sex") or "").strip()
            row["vict_sex_clean"] = sex if sex in {"M", "F"} else "Unknown"
            row["victim_recorded"] = (
                1 if row["vict_age_clean"] != "" and row["vict_sex_clean"] in {"M", "F"} else 0
            )

            desc = (row.get("Crm Cd Desc") or "").strip()
            fam = crime_family(desc)
            row["crime_family"] = fam
            row["premise_family"] = premise_family(row.get("Premis Desc") or "")
            stats["desc_to_family"].setdefault(desc, fam)

            writer.writerow(row)
            stats["rows"] += 1
            if occ:
                stats["year_occ"][occ.year] += 1
                if occ.year == 2024:
                    stats["month_2024"][occ.month] += 1
            stats["crime_family"][fam] += 1
            stats["premise_family"][row["premise_family"]] += 1
            stats["bureau"][row["bureau"]] += 1
            stats["vict_sex_clean"][row["vict_sex_clean"]] += 1
            if row["delay_bucket"]:
                stats["delay_bucket"][row["delay_bucket"]] += 1
            if fam == "Other" and desc:
                stats["other_crimes"][desc] += 1

    with MAP.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Crm Cd Desc", "crime_family"])
        for desc, fam in sorted(stats["desc_to_family"].items()):
            w.writerow([desc, fam])

    dump = {
        "source": str(SRC.name),
        "output": str(OUT.name),
        "rows": stats["rows"],
        "bytes": OUT.stat().st_size,
        "year_occ": dict(sorted(stats["year_occ"].items())),
        "month_2024": dict(sorted(stats["month_2024"].items())),
        "crime_family": dict(stats["crime_family"].most_common()),
        "premise_family": dict(stats["premise_family"].most_common()),
        "bureau": dict(stats["bureau"].most_common()),
        "vict_sex_clean": dict(stats["vict_sex_clean"].most_common()),
        "delay_bucket": dict(stats["delay_bucket"].most_common()),
        "age_le0": stats["age_le0"],
        "age_gt99": stats["age_gt99"],
        "age_kept": stats["age_kept"],
        "coords_ok": stats["coords_ok"],
        "coords_nulled": stats["coords_nulled"],
        "coord_ok_pass1": n_ok_coords,
        "map_sample": stats["map_sample"],
        "noon_default": stats["noon_default"],
        "first_of_month": stats["first_of_month"],
        "other_crimes_top15": stats["other_crimes"].most_common(15),
        "n_crime_descriptions": len(stats["desc_to_family"]),
    }
    STATS.write_text(json.dumps(dump, indent=2), encoding="utf-8")
    print(json.dumps(dump, indent=2))

    assert dump["rows"] == 1_004_894, dump["rows"]
    assert dump["map_sample"] == 200_000, dump["map_sample"]
    assert dump["coords_nulled"] >= 2_000
    assert dump["year_occ"].get(2024) == 127_567
    assert dump["bureau"].get("Unknown", 0) == 0
    print("ok")


if __name__ == "__main__":
    main()
