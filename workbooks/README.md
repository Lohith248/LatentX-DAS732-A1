# Tableau workbooks

Open these in Tableau Desktop. Each file is a packaged workbook (`.twbx`).

| File | Member | What it holds |
|---|---|---|
| `lohith-when/LatentX_A01.twbx` | Lohith P | Act I time sheets |
| `lohith-when/A07_report_delay.twbx` | Lohith P | Figure 7 delay sheets |
| `sri-charan-where/LatentX_B_FINAL.twbx` | Sri Charan | Act II place sheets, including Figure 16 |
| `anish-what/LatentX_C_FINAL.twbx` | R Anish Reddy | Act III type and victim sheets, including Figure 28 |

Connect the extract to `lapd_a1_clean.csv` if Tableau asks for the local file. That CSV is not in this repository (it is larger than GitHub’s file limit). Rebuild it with:

```
python scripts/preprocess_lapd_a1.py
```
