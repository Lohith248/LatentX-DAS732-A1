# Data

The two large CSVs are not on GitHub (each is over 200 MB). Upload them to the Drive folder named `data`.

| File | What it is |
|---|---|
| Crime_Data_from_2020_to_2024.csv | Official LAPD freeze. Do not edit. |
| lapd_a1_clean.csv | Clean file used in Tableau. |
| crime_family_map.csv | Description-to-family map (also on GitHub). |
| preprocess_stats.json | Counts written by the preprocess script (also on GitHub). |

Rebuild the clean file locally with `python scripts/preprocess_lapd_a1.py`.
