# LatentX — DAS732 Assignment 1

Official LAPD crime reports, 2020–2024. Team LatentX, IIIT Bangalore, Term 1 2026–27.

**Question.** Between 2020 and 2024, when, where, and what kind of crime did Los Angeles residents report to the LAPD, and which visible changes are recording artefacts rather than patterns?

## Team

| Member | Roll | Task | Figures |
|---|---|---|---|
| Lohith P | BT2024248 | Preprocessing and when | Fig 1–8 |
| Sri Charan | BT2024143 | Where | Fig 9–18 |
| R Anish Reddy | BT2024228 | What and who was recorded | Fig 19–28 |

## What is in this repository

```
figures/                 28 Tableau exports, split by act
workbooks/               four packaged Tableau files
scripts/                 official download check and preprocess
data/README.md           where the two large CSVs live (Drive)
crime_family_map.csv
preprocess_stats.json
```

The IEEE report is not in this push. It is still being edited.

The official freeze and the clean extract are on Google Drive, in the `data` folder. GitHub will not take files over 100 MB.

## Data

Assigned list item: LAPD Crime Data 2020–2024. We use the official City of Los Angeles Open Data table, **Crime Data from 2020 to Present**, dataset `2nrs-mtv8`, CC0.

- Page: https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8
- Local freeze name: `Crime_Data_from_2020_to_2024.csv`
- Grain: one reported incident (`DR_NO`)
- Size of the freeze we used: 1,004,894 rows, 28 columns
- Compare years: 2020–2023
- 2024 is incomplete after LAPD left this legacy system for NIBRS on 7 March 2024

Rebuild the clean file after you download the official CSV:

```
python scripts/download_lapd_official.py --check-only
python scripts/preprocess_lapd_a1.py
```

## How to read the figures

Start with `figures/act1-when/`. Fig 1 and Fig 2 set the comparable window. Noon and first-of-month spikes are defaults. Identity theft has a seven-day median delay.

Then `figures/act2-where/`. Central, 77th Street, and Pacific lead volume. Division mix is not the same as volume. Reporting-district load has a long tail.

Then `figures/act3-what/`. Vehicle stolen is the largest description. Identity theft is the steep riser. Victim fields describe recorded persons, not every affected person.

These are report counts, not crime rates.

The IEEE report uses all 28 exports. Report figure N is `FigN.png`.

## Workbooks

See `workbooks/README.md`. Open the `.twbx` files in Tableau Desktop.

## License

LAPD source data: CC0. This repository’s scripts and figure packaging: team LatentX, for the course submission.
