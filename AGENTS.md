# DAS732 A1 (LatentX)

Locked source is the official LAPD table, not Kaggle.

## Source change (put this in the report)

- Assigned list item: LAPD Crime Data 2020-2024. Original Excel Kaggle link was `aadigupta1601/lapd-crime-data-2020-2024` (now 403). A later Kaggle mirror is `saurabhbadole/crime-incidents-in-los-angeles-2020-to-present` (snapshot 18 Aug 2024).
- Team asked the course staff whether official LAPD Open Data could be used instead of Kaggle. Staff reply (10 Sep 2026): use whatever is better, mention it in the report.
- We use the official frozen file only for A1, A2, and A3.

Official page: https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8  
CSV download: https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD  
Local file: `Crime_Data_from_2020_to_2024.csv`  
Re-download / check: `python scripts/download_lapd_official.py` or `python scripts/download_lapd_official.py --check-only`

## Verified file facts (checked 10 Sep 2026)

- 1,004,894 rows, 28 columns, 255,460,843 bytes
- Grain: one reported incident (`DR_NO`)
- `DATE OCC`: 1 Jan 2020 to 30 Dec 2024
- `Date Rptd`: 1 Jan 2020 to 28 Mar 2025. Only 94 rows have a 2025 report date. Those are late filings, not a 2025 crime year.
- Occurrence counts: 2020 199847, 2021 209876, 2022 235259, 2023 232345, 2024 127567
- 2024 months exist through December, but counts fall after March 2024 (LAPD left this legacy system for NIBRS). 2024 is not a full comparable year.
- No 2025 or 2026 occurrence series in this file
- 2,240 rows have LAT/LON 0,0
- License: CC0

## A1 rules (PDF `DAS732_T1-26-27_A1 (1).pdf`)

Deadline 13 Sep 2026, 11:59 pm IST. Group of 3. Tableau preferred.

Start from one question. Several plots must build one story. n task sets for n members. Do not split one task across people. Lay-readable plots. 5-minute video. Report with author contributions and per-member AI forms. Image folder `FigN.ext` matching the report.

## Analysis guards

- This is reported crime, not true incidence. Addresses are hundred-block. Do not frame predictive policing. Do not treat victim descent as a cause.
- Compare full years 2020-2023. Label 2024 as a transition / incomplete-coverage year.
- Weapon, Cross Street, Crm Cd 2-4 are mostly empty. Keep them off the core story.
- Tableau point maps: sample 150k-300k. Use full data for area/month aggregates.

## Next chat

Do not change `Crime_Data_from_2020_to_2024.csv`. Story, split, and figure list: `A1_PLAN.md`. Clean file for Tableau: `lapd_a1_clean.csv` (script `scripts/preprocess_lapd_a1.py`). Lohith P (BT2024248) is Member A (When + preprocess), Sri Charan (BT2024143) is Member B (place/maps), and R Anish Reddy (BT2024228) is Member C (type/victims).

Tableau is built **by hand**, not generated TWBX XML. A generated `LatentX_A01.twbx` opened but titles/schema were fragile; keep using `tableau/A01/a01_daily.csv` as the Fig 1 table. One chart at a time: user says Next after exporting `FigN.png`.

NIBRS tables exist (`k7nn-b2ep`) but do **not** complete 2024 and must not be merged into A1.

GeoHub division polygons: browser shapefile export; API dump was truncated. Symbol-map fallback is allowed.
