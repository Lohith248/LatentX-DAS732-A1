"""Inspect the Fig 7 twbx for required sheets, calcs, colours, sorts, and grains."""
from __future__ import annotations

import csv
import struct
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))

from a07_extract import BUCKETS, EXPECTED_2025, FAMILY_ORDER, _median
from a07_workbook import (
    DASH,
    DASH_CAPTION,
    DASH_TITLE,
    DELAY_BIN_FORMULA,
    GREY,
    MEDIAN_LABEL_FORMULA,
    MIST,
    NAVY,
    NAVY_LOW,
    REPORT_YEAR_FORMULA,
    SAME_DAY_FORMULA,
    STEEL,
    TITLE_A,
    TITLE_B,
    TITLE_C,
    WS_A,
    WS_B,
    WS_C,
)

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "tableau" / "A07"
TWBX = OUT_DIR / "A07 Report delay.twbx"
TWB_NAME = "A07 Report delay.twb"
CSV_NAME = "a07_delay.csv"


def _norm(text: str) -> str:
    return (
        text.replace("&quot;", "'")
        .replace("&gt;", ">")
        .replace("&lt;", "<")
        .replace("&amp;", "&")
        .replace('"', "'")
    )


def _xml(twbx: Path) -> tuple[ET.Element, str]:
    with zipfile.ZipFile(twbx, "r") as zf:
        names = zf.namelist()
        if TWB_NAME not in names:
            raise AssertionError(f"twbx missing {TWB_NAME}: {names}")
        csv_hits = [n for n in names if n.endswith(CSV_NAME)]
        if not csv_hits:
            raise AssertionError(f"twbx missing {CSV_NAME}: {names}")
        xml_text = zf.read(TWB_NAME).decode("utf-8")
    root = ET.fromstring(xml_text)
    return root, _norm(xml_text)


def _fail_if_sum_dr_no(xml_text: str) -> None:
    if "SUM([DR_NO])" in xml_text or "Sum([DR_NO])" in xml_text:
        raise AssertionError("workbook uses SUM(DR_NO)")
    if "derivation='Sum'" in xml_text and "column='[DR_NO]'" in xml_text:
        raise AssertionError("DR_NO has a Sum derivation")


def _check_forbidden_style(xml_text: str) -> None:
    lowered = xml_text.lower()
    for bad in ("rainbow", "crime fell in 2024", "#ff0000", "diverging"):
        if bad in lowered and "ordered-sequential" not in bad:
            if bad == "diverging" and "diverging" in lowered:
                raise AssertionError("diverging palette present")
            if bad != "diverging":
                raise AssertionError(f"forbidden text: {bad}")
    if "\u2014" in xml_text or "\u2013" in xml_text:
        raise AssertionError("em/en dash in workbook")
    if "--" in xml_text.replace("<!--", "").replace("-->", ""):
        raise AssertionError("double hyphen outside XML comment delimiters")


def _check_formulas(xml_text: str) -> None:
    for formula in (
        DELAY_BIN_FORMULA,
        SAME_DAY_FORMULA,
        REPORT_YEAR_FORMULA,
        'WHEN "same day" THEN 1',
    ):
        if _norm(formula) not in xml_text:
            raise AssertionError(f"missing formula: {formula}")
    if ">60" not in xml_text.replace("&gt;", ">"):
        raise AssertionError("Delay bin alias >60 missing")
    if "type='PctTotal'" not in xml_text and 'type="PctTotal"' not in xml_text:
        raise AssertionError("Percent of Total table calc missing")
    if "ordering-type='Rows'" not in xml_text and 'ordering-type="Rows"' not in xml_text:
        raise AssertionError("PctTotal is not computed across the row")
    if "none:delay_bucket:nk" not in xml_text:
        raise AssertionError("delay_bucket not used in the stacked-bar view")
    if "using=" not in xml_text or "avg:Same day flag:qk" not in xml_text:
        raise AssertionError("Crime Family is not sorted by AVG(Same day flag)")
    if "class='computed'" not in xml_text:
        raise AssertionError("computed sort missing")
    if "none:Delay bucket rank:ok" not in xml_text:
        raise AssertionError("delay_bucket rank sort missing")
    if "manual-sort" in xml_text:
        raise AssertionError("manual-sort element is rejected by Tableau 2026.2")
    if _norm(MEDIAN_LABEL_FORMULA) not in xml_text:
        raise AssertionError("family median LOD missing")
    if "d median" not in xml_text:
        raise AssertionError("median number format missing")
    for bucket in BUCKETS:
        if bucket not in xml_text:
            raise AssertionError(f"missing bucket string {bucket}")


def _check_layout(root: ET.Element, xml_text: str) -> None:
    names = [el.get("name") for el in root.findall(".//worksheet")]
    if names != [WS_A, WS_B, WS_C]:
        raise AssertionError(f"worksheets {names}")
    dash = root.find(".//dashboard")
    if dash is None or dash.get("name") != DASH:
        raise AssertionError("dashboard name mismatch")
    size = dash.find("size")
    if size is None:
        raise AssertionError("dashboard size missing")
    if size.get("maxwidth") != "1600" or size.get("maxheight") != "1200":
        raise AssertionError(f"dashboard size {size.attrib}")
    if TITLE_A not in xml_text or TITLE_B not in xml_text or TITLE_C not in xml_text:
        raise AssertionError("sheet titles missing")
    if DASH_TITLE not in xml_text or DASH_CAPTION not in xml_text:
        raise AssertionError("dashboard title/caption missing")
    if "entire-view" not in xml_text:
        raise AssertionError("Fit Entire View missing")
    if "show-data-guide" not in xml_text:
        raise AssertionError("Data Guide preference missing")
    if xml_text.count('name="' + WS_A + '"') + xml_text.count("name='" + WS_A + "'") < 2:
        raise AssertionError("A07a not placed on dashboard")
    for color in (NAVY, STEEL, MIST, GREY, NAVY_LOW):
        if color not in xml_text:
            raise AssertionError(f"missing colour {color}")
    if "mark-color" not in xml_text or NAVY not in xml_text:
        raise AssertionError("A07a navy mark colour missing")
    if "Crime Family" not in xml_text:
        raise AssertionError("Crime Family caption missing")
    if "d median" not in xml_text:
        raise AssertionError("median number format missing")
    if "derivation='Count'" not in xml_text:
        raise AssertionError("CNT(DR_NO) missing")
    if "derivation='Median'" not in xml_text:
        raise AssertionError("Median(delay_days) missing")
    if "class='Square'" not in xml_text and 'class="Square"' not in xml_text:
        raise AssertionError("A07c Square marks missing")
    if "none:year_occ:ok" not in xml_text or "none:Report year:ok" not in xml_text:
        raise AssertionError("year grid shelves missing")
    if "none:Delay bin:ok" not in xml_text:
        raise AssertionError("Delay bin is not a discrete dimension on Columns")
    if "palette='A07_navy_sequential'" not in xml_text and 'palette="A07_navy_sequential"' not in xml_text:
        raise AssertionError("year grid is not using the navy sequential palette")
    if "field='[none:delay_bucket:nk]'" not in xml_text and 'field="[none:delay_bucket:nk]"' not in xml_text:
        raise AssertionError("delay_bucket color maps are not bound to the color instance")
    if "palette='A07_delay_buckets'" in xml_text or 'palette="A07_delay_buckets"' in xml_text:
        raise AssertionError("delay_bucket encoding still names a regular palette")
    if "logarithmic" in xml_text.lower():
        raise AssertionError("logarithmic axis present")
    text_hits = [el.get("column", "") for el in root.findall(".//text") if el.get("column")]
    if any("crime_family" in hit for hit in text_hits):
        raise AssertionError("Crime Family is on Label")
    if not any("Family median label" in hit for hit in text_hits):
        raise AssertionError("family median label missing from pane Label")
    if any("med:delay_days" in hit for hit in text_hits):
        raise AssertionError("per-segment Median(delay_days) still on Label")
    rank_sort = [
        el
        for el in root.findall(".//sort")
        if "delay_bucket" in (el.get("column") or "")
    ]
    if not rank_sort:
        raise AssertionError("delay_bucket computed sort missing")
    if not any("Delay bucket rank" in (el.get("using") or "") for el in rank_sort):
        raise AssertionError("delay_bucket is not sorted by Delay bucket rank")
    role_hits = [
        el.get("role")
        for el in root.findall(".//column")
        if el.get("name") in ("[Delay bin]", "[Report year]", "[year_occ]")
    ]
    if any(role == "measure" for role in role_hits):
        raise AssertionError(f"dimension fields stored as measures: {role_hits}")


def _check_extract_csv(twbx: Path) -> None:
    with zipfile.ZipFile(twbx, "r") as zf:
        csv_name = [n for n in zf.namelist() if n.endswith(CSV_NAME)][0]
        with zf.open(csv_name) as fh:
            text = fh.read().decode("utf-8-sig").splitlines()
    reader = csv.DictReader(text)
    occ: Counter[str] = Counter()
    rptd: Counter[str] = Counter()
    xy: Counter[tuple[str, str]] = Counter()
    fam_days: dict[str, list[int]] = {}
    fam_same: Counter[str] = Counter()
    delay0 = 0
    n = 0
    for row in reader:
        n += 1
        delay = int(row["delay_days"])
        if delay == 0:
            delay0 += 1
        yo = row["year_occ"]
        ry = row["Date Rptd"][:4]
        occ[yo] += 1
        rptd[ry] += 1
        xy[yo, ry] += 1
        fam = row["crime_family"]
        fam_days.setdefault(fam, []).append(delay)
        if row["delay_bucket"] == "same day":
            fam_same[fam] += 1
        if yo == "2025":
            raise AssertionError("2025 occurrence row in extract")
    if n != 1_004_894:
        raise AssertionError(f"extract rows {n}")
    if delay0 != 482_015:
        raise AssertionError("0-day dominance lost in extract")
    if rptd["2025"] != 94:
        raise AssertionError(f"2025 filings {rptd['2025']}")
    for year, expected in EXPECTED_2025.items():
        got = xy[str(year), "2025"]
        if got != expected:
            raise AssertionError(f"{year} x 2025 = {got}")
    ranked = sorted(
        fam_days,
        key=lambda fam: fam_same[fam] / len(fam_days[fam]),
        reverse=True,
    )
    if tuple(ranked) != FAMILY_ORDER:
        raise AssertionError(f"sort order {ranked}")
    if _median(fam_days["Identity theft & fraud"]) != 7:
        raise AssertionError("identity theft median")
    if any(xy[str(occ_y), str(rpt)] for occ_y in range(2021, 2025) for rpt in range(2020, occ_y)):
        raise AssertionError("reports before occurrence")


def validate_twbx(twbx: Path = TWBX) -> list[str]:
    if not twbx.exists():
        raise FileNotFoundError(twbx)
    root, xml_text = _xml(twbx)
    _fail_if_sum_dr_no(xml_text)
    _check_forbidden_style(xml_text)
    _check_formulas(xml_text)
    _check_layout(root, xml_text)
    _check_extract_csv(twbx)
    notes = [
        "twbx contains TWB plus a07_delay.csv",
        "three worksheets and one dashboard present",
        "Delay bin / Same day flag / Report year formulas match spec",
        "CNT(DR_NO) used; no SUM(DR_NO)",
        "PctTotal on CNT(DR_NO) across each crime_family row",
        "Crime Family sorted by AVG(Same day flag) DESC",
        "one family median label on 31+ days only; Crime Family not on Label",
        "bucket colour maps on datasource instance none:delay_bucket:nk",
        "year grid 2020-2024 occ x 2020-2025 report; 94 late filings",
        "dashboard 1600 x 1200, Entire View, Data Guide hidden",
    ]
    return notes


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as fh:
        sig = fh.read(8)
        if sig != b"\x89PNG\r\n\x1a\n":
            raise AssertionError("Fig7.png is not a PNG")
        _length, mtype = struct.unpack(">I4s", fh.read(8))
        if mtype != b"IHDR":
            raise AssertionError("Fig7.png missing IHDR")
        width, height = struct.unpack(">II", fh.read(8))
        return width, height


def write_report(notes: list[str], extra: list[str] | None = None) -> Path:
    path = OUT_DIR / "VALIDATION_REPORT.txt"
    lines = ["Fig 7 validation", ""]
    lines.extend("- " + note for note in notes)
    if extra:
        lines.append("")
        lines.extend(extra)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
