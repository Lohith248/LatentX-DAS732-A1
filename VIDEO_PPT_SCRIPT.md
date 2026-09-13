# Team LatentX — Final Five-Minute Video and PPT Script

## Final production decision

Use **8 slides**, **7 full figure images**, and **3 short live Tableau demonstrations**. The report keeps 13 numbered figures drawn from the full 28-export archive; the video explains only the strongest evidence. Figure numbers below follow the workbook/archive numbering used on the charts themselves.

The video must feel like a clear explanation, not a list of charts and not a fictional investigation.

### Team

- **Lohith P (BT2024248)** — preprocessing and Act I: When
- **Sri Charan (BT2024143)** — Act II: Where
- **R Anish Reddy (BT2024228)** — Act III: What and who was recorded

### Selected evidence

| Use | Figures |
|---|---|
| PPT anchor images | Fig. 1, 2, 9, 12, 19, 21, 28 |
| Live Tableau demonstration | Fig. 7, 16, 28 |
| Complete evidential record | Report Figs. 1–13; archive Fig. 1–28 |

This is enough visual variety without shrinking charts until their labels become unreadable.

### Timing

| Time | Speaker | Segment |
|---|---|---|
| 0:00–0:14 | Lohith | Team greeting and title |
| 0:14–0:31 | Lohith | Question and three-act structure |
| 0:31–0:58 | Lohith | Concise preprocessing |
| 0:58–1:54 | Lohith | Act I + Tableau Fig. 7 |
| 1:54–2:58 | Sri Charan | Introduction, Act II + Tableau Fig. 16 |
| 2:58–4:06 | R Anish Reddy | Introduction, Act III + Tableau Fig. 28 |
| 4:06–4:43 | Lohith | Synthesis and limitations |
| 4:43–4:55 | Lohith | Reproducibility and close |

Target: **4:50–4:55**. The remaining seconds are a safety margin.

---

# Slide 1 — Team and project opening

**Time:** 0:00–0:14  
**Speaker:** Lohith  
**Eyebrow:** `TEAM LATENTX PRESENTS`  
**Main heading:** Reading Reported Crime Without Reading Recording Artefacts as Trends  
**Subheading:** LAPD Legacy Reports, 2020–2024

**Names displayed**

`Lohith P (BT2024248)`  
`Sri Charan (BT2024143)`  
`R Anish Reddy (BT2024228)`

**Footer**

`DAS732 Data Visualization · IIIT Bangalore · T1 2026–27`

**Visual direction**

- Use the chosen template with a restrained academic treatment.
- A faint outline of Los Angeles or subtle street-grid texture is acceptable.
- Do not use crime-scene tape, weapons, blood, sirens, detectives, fingerprints, or “case file” language.
- Keep the title and team name dominant. No chart is needed on the opening slide.

**Exact spoken script — 31 words**

> Hi everyone. We are Team LatentX. I’m Lohith P, and with Sri Charan and R Anish Reddy, we explored how to read LAPD crime reports without mistaking recording artefacts for trends.

---

# Slide 2 — Starting question and story structure

**Time:** 0:14–0:31  
**Speaker:** Lohith  
**Heading:** One question guides the entire analysis

**Central question, displayed prominently**

> Between 2020 and 2024, when, where, and what kind of crime was reported to the LAPD—and which visible changes are patterns rather than recording artefacts?

**Three-act diagram**

`WHEN — Lohith` → `WHERE — Sri Charan` → `WHAT / WHO RECORDED — R Anish Reddy`

Under each act:

- **When:** trend, rhythm, delay, coverage
- **Where:** division volume, mix, concentration
- **What/who:** crime type, relative growth, recorded victim fields

Caption under the arrows:

`The arrows show narrative sequence, not causation.`

**Exact spoken script — 38 words**

> We began with one question: when, where, and what kind of crime was reported, and which changes came from recording practice? Our three task sets follow one sequence: when establishes comparability, where locates concentration, and what explains composition.

---

# Slide 3 — Data and preprocessing

**Time:** 0:31–0:58  
**Speaker:** Lohith  
**Heading:** First, make one million reports comparable  
**Subheading:** One row is one reported incident in the frozen LAPD legacy table—not a population rate.

**Horizontal preprocessing diagram**

`Official LAPD freeze` → `Validate 1,004,894 reports` → `Parse dates and delay` → `Flag noon and day-one defaults` → `Clean coordinates and victim fields` → `Derive families` → `Tableau`

Use compact line icons only: database, check, calendar, clock, map pin, category grid, dashboard.

**Four compact fact cards**

| FACT | VALUE |
|---|---|
| Source grain | `DR_NO = one report` |
| Comparable years | `2020–2023` |
| Coordinate sample | `200,000 rows · seed 732` |
| 2024 | `Incomplete legacy coverage after 7 Mar` |

**Small footer**

`All aggregate views use the full relevant rows. NIBRS was not merged because it has a different offence-level grain.`

**Exact spoken script — 57 words**

> After course-staff approval, we used the official frozen LAPD table: 1,004,894 reports. We parsed dates and delay, flagged noon and day-one defaults, nulled 2,240 invalid coordinates, cleaned victim fields, and derived families. Aggregates use the full relevant rows; coordinate maps use a fixed sample. Because the legacy system changed in March 2024, comparisons use 2020 through 2023.

---

# Slide 4 — Act I: When

**Time:** 0:58–1:42  
**Speaker:** Lohith  
**Heading:** When: a rise, a plateau—and a broken series

**Visual layout**

- Left, dominant: `images/Fig1.png`.
- Right, supporting: `images/Fig2.png`.
- Preserve chart proportions, axes, labels, and legends.
- Crop empty margins only. Never redraw the charts.

**Metric strip**

`199,847 in 2020` → `235,259 in 2022` → `232,345 in 2023`

**Three rubric boxes**

| TASK | VISUALIZATION SOLUTION | INFERENCE |
|---|---|---|
| Overview · trend · compare · summarize | Daily line + 28-day mean; monthly bars against the earlier same-month baseline | Rise through 2022; 2023 plateau; post-March 2024 is coverage loss |

**Callouts**

- On Fig. 1: `7 Mar 2024 — legacy RMS transition`
- On Fig. 2: `April 73% · December 26% of prior same-month mean`
- Caveat: `2024 is context, not a comparable crime year`

**Exact spoken script — 89 words**

> My task was to overview, trend, compare, and summarize when reports entered the record. Figure 1 combines daily reports with a 28-day moving average, preserving daily variation while exposing the trend. Reports rise from 199,847 in 2020 to 235,259 in 2022, then level at 232,345 in 2023. Figure 2 tests the 2024 break against the earlier same-month baseline. January through March remain close, but April falls to 73 percent and December to 26 percent after the system transition. This is loss of legacy-table coverage, not a comparable citywide trend.

## Tableau demonstration — Figure 7

**Time:** 1:42–1:54  
**Spoken reference:** **Figure 7**  
**Workbook:** `tableau/A07/A07 Report delay.twbx`

The current workbook contains the three component sheets of Figure 7 rather than one dashboard object:

- `A07a Delay histogram`
- `A07b Delay by family`
- `A07c Year grid`

**Screen action**

1. Start with the workbook already open; loading must not appear in the video.
2. For two seconds, keep the Tableau authoring interface and the three sheet tabs visible. This proves it is a workbook built in Tableau.
3. Open `A07b Delay by family`.
4. Hover the `Identity theft & fraud` row and point once to its `7 day median` label.
5. Do not open tooltips on several rows or change filters.

**Exact spoken script — 29 words**

> We built Figure 7 from three Tableau sheets. Its normalized family view shows a seven-day median for identity theft against zero days for assault—our bridge from when to what.

---

# Slide 5 — Act II: Where

**Time:** 1:54–2:44  
**Speaker:** Sri Charan  
**Heading:** Where: volume concentrates, but crime mix differs

**Visual layout**

- Left: `images/Fig9.png`, approximately 52% width.
- Right: `images/Fig12.png`, approximately 48% width.
- Keep the map legend and heatmap cells readable.
- Do not rearrange, recolour, or recreate either figure.

**Three rubric boxes**

| TASK | VISUALIZATION SOLUTION | INFERENCE |
|---|---|---|
| Overview · rank · compare · search | Sequential division choropleth + row-normalized family heatmap | Central leads volume; South-bureau divisions have a larger assault-family mix |

**Callout cards**

- `Central · 59,456 reports`
- `77th Street · 40.6% combined assault-family share`
- `Southeast · 39.6% combined assault-family share`

**Caveat**

`These are recorded counts and shares—not population rates or predictions of individual risk.`

**Exact spoken script — 101 words**

> Hello everyone, I’m Sri Charan. My task was to overview, rank, compare, and search across place. Figure 9 uses geographic position and sequential colour to show division workload. Central leads with 59,456 reports, followed by 77th Street and Pacific. But the map cannot show what produces that volume, so Figure 12 normalizes every division row to 100 percent. The combined assault-family share reaches 40.6 percent in 77th Street and 39.6 percent in Southeast, while Central and several West-side divisions are more theft-oriented. The two views therefore separate volume from composition. They describe reported workload, not population-normalized risk or a predictive hotspot.

## Tableau demonstration — Figure 16

**Time:** 2:44–2:58  
**Spoken reference:** Call it **Figure 16**.  
**Workbook:** `tableau/FINAL_SUBMISSION_MEMBER_B/FINAL_SUBMISSION_MEMBER_B/LatentX_B_FINAL.twbx`  
**Dashboard:** `Figure 16`

**Screen action**

1. Start with the workbook already open.
2. Let the workbook/dashboard tabs remain visible for two seconds; do not scroll through every sheet.
3. Open dashboard `Figure 16`.
4. Point to the first bar, RD 0162 (`4,672` reports).
5. Move directly to the labelled `80% at rank 623` reference.

**Exact spoken script — 31 words**

> We created ten place views in Tableau. Figure 16 ranks 1,207 reporting districts; its cumulative curve reaches 80 percent at rank 623. Concentration is substantial, but it remains a long tail.

---

# Slide 6 — Act III: What and who was recorded

**Time:** 2:58–3:50  
**Speaker:** R Anish Reddy  
**Heading:** What changed: theft—especially identity theft

**Visual layout**

- Dominant centre/left: `images/Fig21.png` (indexed family growth).
- Small top-right evidence card: `images/Fig19.png` (treemap).
- Small bottom-right evidence card: `images/Fig28.png` (identity-theft close-up).
- These are three distinct roles: **relative change**, **absolute volume**, and **focused explanation**.
- Keep Fig. 21 fully readable. Fig. 19 and Fig. 28 are supporting previews; do not shrink Fig. 21 to make all three equal.

**Three rubric boxes**

| TASK | VISUALIZATION SOLUTION | INFERENCE |
|---|---|---|
| Overview · rank · compare · summarize | Indexed lines for relative growth; treemap for volume; coordinated close-up for one family | Theft explains more of the rise than violence; identity theft grows and is reported later |

**Metric cards**

- `Identity theft index · 200.9 in 2022`
- `Other theft index · 151.2 in 2023`
- `VEHICLE – STOLEN · 93,674 reports`

**Caveat**

`Victim views describe recorded fields, not every affected person. The data does not identify causes.`

**Exact spoken script — 105 words**

> Hi everyone, I’m R Anish Reddy. My task was to overview, rank, compare, and summarize what was reported and which victim fields were usable. Figure 21 sets every family to 100 in 2020, allowing relative growth from unequal baselines. Identity theft reaches 200.9 in 2022 and remains at 139.2 in 2023; other theft ends at 151.2, while the assault families stay near 108. Figure 19 restores absolute scale: vehicle stolen is the largest description with 93,674 reports. Figure 28 then examines the identity-theft pattern through month, recorded age, premise, and delay. Together, these views make the rise more a theft-composition story than a violence story.

## Tableau demonstration — Figure 28

**Time:** 3:50–4:06  
**Spoken reference:** **Figure 28**  
**Workbook:** `tableau/Final_submission_C/qwerty.twbx`

The current workbook contains Figure 28 as four component worksheets, not a single dashboard object:

- `C28a_Identity_Monthly`
- `C28b_Identity_Age`
- `C28c_Identity_Premise`
- `C28d_Identity_Delay`

**Screen action**

1. Start with the workbook already open and let the C28 sheet tabs remain visible for two seconds.
2. Open `C28a_Identity_Monthly` and hover December 2022 (`2,737`).
3. Click directly to `C28d_Identity_Delay`.
4. Hover the identity-theft mark for `31+ days`.
5. Do not tour all four sheets. The final Fig. 28 preview on the slide already shows the coordinated whole.

**Exact spoken script — 36 words**

> We built Figure 28 from four coordinated Tableau sheets. Monthly identity-theft reports peak at 2,737 in December 2022. The delay view shows about 28 percent at 31-plus days, versus 5.9 percent citywide, without claiming a cause.

---

# Slide 7 — Synthesis

**Time:** 4:06–4:43  
**Speaker:** Lohith  
**Heading:** One question, three task sets, one answer

**Top diagram**

`WHEN: rise → plateau` → `WHERE: concentrated volume + different mix` → `WHAT: theft growth + longer identity-theft delay`

Caption:

`Narrative sequence—not a causal model.`

**Two-column summary table**

| PATTERNS SUPPORTED | RECORDING ARTEFACTS |
|---|---|
| Rise through 2022; 2023 plateau | Post-March 2024 legacy-system cliff |
| Central, 77th Street, Pacific lead volume | Exact-noon spike: 35,198 records |
| Division crime-family mixes differ | First-of-month spike: 46,546 records |
| Theft, especially identity theft, drives relative growth | Late-2024 type mix is not comparable |
| Evening band remains after noon is set aside | Hour 12 must not be called a rush hour |

**Closing sentence displayed verbatim**

> Reported crime in LA rose through 2022 and levelled in 2023, driven more by theft—especially identity theft—than by violence; it concentrates in Downtown and South LA and in evening hours; the 2024 drop, the noon spike and the 1st-of-month spike are recording artefacts, not crime trends.

**Exact spoken script — 64 words**

> Reported crime in LA rose through 2022 and levelled in 2023, driven more by theft—especially identity theft—than by violence; it concentrates in Downtown and South LA and in evening hours; the 2024 drop, the noon spike and the first-of-month spike are recording artefacts, not crime trends. Counts are reports, not incidence rates; locations are hundred-blocks, times can be approximate, and status is a snapshot.

---

# Slide 8 — Reproducibility and end frame

**Time:** 4:43–4:55  
**Speaker:** Lohith  
**Eyebrow:** `COMPLETE SUBMISSION`  
**Heading:** Reproducible and reviewable

**Four deliverable cards**

1. `IEEE report · 13 numbered figures + 28-image archive`
2. `Python preprocessing + README`
3. `Tableau workbooks for all three members`
4. `Official LAPD source · 2nrs-mtv8 · CC0`

**GitHub link**

`github.com/Lohith248/LatentX-DAS732-A1`

An optional QR code may point to the same link, but the typed URL must remain visible.

**Team footer**

`Lohith P · Sri Charan · R Anish Reddy`

**Exact spoken script — 22 words**

> Our report keeps 13 numbered figures from a 28-image archive; preprocessing code, README, and all three Tableau workbooks are packaged for review. We are Team LatentX. Thank you.

Hold the final frame until 5:00 if needed.

---

# Recording directions

## Tableau strategy

The strongest demonstration is **not** to browse every worksheet. For each member:

1. Pre-open the workbook before the recording.
2. Show the authoring interface or workbook tabs for only two to three seconds so the assessor sees that it is a real Tableau workbook.
3. Open one numbered figure.
4. Make one controlled interaction: one hover or one direct sheet switch.
5. Explain one inference.
6. Cut back to the PPT.

This is clearer than spending the video on loading, scrolling, or proving every field.

## Video assembly

- Record at 1920×1080 or higher, 16:9.
- Record the PPT narration and three Tableau clips separately, then join them with clean cuts.
- Do not show workbook loading or file browsing.
- Keep Tableau’s Rows/Columns shelves or tabs visible briefly, but maximize the chart before reading values.
- Keep the cursor still except for the scripted action.
- Use a restrained fade or hard cut; avoid dramatic transitions.
- Do not add background music unless it is extremely soft and does not reduce speech clarity.
- Speak naturally at approximately 125–135 words per minute.
- Every member must state their name, task, visualization solution, and inference.

## Final claim guardrails

- Use “reports,” “reported records,” and “legacy-table coverage,” not true crime incidence.
- Never describe 2024 as a decline in citywide crime.
- Exact noon is 35,198 reports, about 3.5%; never say “one in eight.”
- 2024 is incomplete after the 7 Mar 2024 records-system transition.
- Maps show counts or shares, not population rates or predictive hotspots.
- Addresses represent hundred-blocks.
- Unknown recorded sex is missingness.
- `Status Desc` is a snapshot, not a final outcome.
- Do not claim causes for identity-theft growth or divisional differences.

# PPT asset manifest

Grok/Canva needs **only** the crime template, this script, and the seven PNGs below. Full paths:

| Attach to Grok/Canva? | File |
|---|---|
| Yes — script | `C:\Users\jagat\Desktop\Sem 5\DV\VIDEO_PPT_SCRIPT.md` |
| Yes — prompt | `C:\Users\jagat\Desktop\Sem 5\DV\GROK_CANVA_PPT_PROMPT.md` (or paste its copy-paste block) |
| Yes — Slide 4 left | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig1.png` |
| Yes — Slide 4 right | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig2.png` |
| Yes — Slide 5 left | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig9.png` |
| Yes — Slide 5 right | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig12.png` |
| Yes — Slide 6 small card | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig19.png` |
| Yes — Slide 6 dominant | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig21.png` |
| Yes — Slide 6 small card | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig28.png` |
| No — live Tableau Fig. 7 | `C:\Users\jagat\Desktop\Sem 5\DV\tableau\A07\A07 Report delay.twbx` |
| No — live Tableau Fig. 16 | `C:\Users\jagat\Desktop\Sem 5\DV\tableau\FINAL_SUBMISSION_MEMBER_B\FINAL_SUBMISSION_MEMBER_B\LatentX_B_FINAL.twbx` |
| No — live Tableau Fig. 28 | `C:\Users\jagat\Desktop\Sem 5\DV\tableau\Final_submission_C\qwerty.twbx` |

Do not attach the remaining `Fig3`–`Fig8`, `Fig10`–`Fig11`, `Fig13`–`Fig18`, `Fig20`, `Fig22`–`Fig27` images, or the CSV extracts. The identical PNGs also exist in `C:\Users\jagat\Desktop\Sem 5\DV\report\overleaf_images\`; use the `images\` copies for the PPT bot.

