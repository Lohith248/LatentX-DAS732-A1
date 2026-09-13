# Scripts

Only these two files belong here.

`download_lapd_official.py` checks or downloads the official LAPD freeze (`Crime_Data_from_2020_to_2024.csv`).

`preprocess_lapd_a1.py` reads that freeze and writes `lapd_a1_clean.csv` plus `preprocess_stats.json`. It does not change the official file.

```
python scripts/download_lapd_official.py --check-only
python scripts/preprocess_lapd_a1.py
```

The two large CSVs are not on GitHub. They are in the Drive `data` folder.
