# DAS732 A1 Plan - LatentX (LAPD Crime Reports 2020–2024)

Plan only. Tableau for every chart. Data is locked: `Crime_Data_from_2020_to_2024.csv` (official LAPD legacy table, 1,004,894 rows, 28 columns, one row = one report).

"Expected" findings below are hypotheses from the verified file facts. Implementers replace them with what Tableau shows. If a chart contradicts the story, write what it shows.

---

## 0. Rules we build to

From the A1 PDF and the professor's follow-up note:

- One starting question. Several charts must build one story. n task sets for n members. No task split across people.
- **Up to 15 figures per person. Fewer is fine.** Graded on how informative each figure is: a chart carrying 3–4 variables beats a 2-variable bar. Variety of methods counts. No padding.
- **Build more, keep fewer.** Each member builds ~14–16 candidate sheets, keeps 8–10 as report figures, lists the rest as "explored, not retained" in one paragraph.
- Every figure: index (Figure N), caption, referenced in the text, interpretation written out. **Subfigures (a)(b)(c) are allowed** — we use them to fold simple views into one richer figure.
- Lay-readable. Video ≤ 5 min: minute 1 preprocess, then each member's story with a few charts. Report: dataset, tasks, chart rationale (marks/channels), captions, inferences, author contributions, AI forms. Images `FigN.png` matching the report; README.
- Guards: reported crime ≠ crime incidence; addresses hundred-block; 2024 is a system-change year (never "crime fell in 2024"); no predictive framing; no descent/race charts; no Weapon / Cross Street / Crm Cd 2–4.

**Variable-density target:** every retained figure encodes ≥ 3 variables (e.g., time × count × category, or place × count × change). Plain 2-variable bars appear only as subfigures inside a richer figure.

---



## 1. Central question

**Between 2020 and 2024, when, where, and what kind of crime did Los Angeles residents report to the LAPD — and which of the changes we see are real patterns rather than artefacts of how the data was recorded?**

Task verbs (Schulz et al. 2013, used lightly): goal exploratory → presentation; means *overview, trend, compare, rank, search, summarize*; targets time (A), space (B), attributes (C).

---



## 2. Story in three acts

**Act 1 — When (Member A).** Reports rose ~200k → ~235k from 2020 to 2022 and held in 2023. 2024 collapses after 7 March because LAPD moved to a new records system. Crime has a daily and weekly rhythm that differs by crime type. Spikes at exactly 12:00 and on the 1st of the month are default entries. Most reports are filed within a day; identity theft is filed weeks later — the first sign that *what* was reported matters.

**Act 2 — Where (Member B).** A few divisions (Central, 77th Street, Pacific, Southwest, Hollywood) and a handful of reporting districts carry the load, and their ranking barely moves year to year. The 2021–22 rise and the 2024 cliff appear in every division at once — the cliff is systemic. Divisions differ in *kind*: Downtown is theft-heavy, South LA has a higher violent share — hand-off to Act 3.

**Act 3 — What and who (Member C).** Vehicle theft, simple assault, identity theft and theft from vehicles are the big four. Identity theft roughly doubled around 2022 and explains much of the rise (and the long delays) A saw. Property crimes mostly have no person victim (age recorded as 0), so victim charts describe the ~70% of reports with a recorded person: assault victims cluster at 25–45; intimate-partner and sex-offence victims are mostly women; most reports remain "Investigation Continued", assaults most often end in arrest.

**Closing sentence:** Reported crime in LA rose through 2022 and levelled in 2023, driven more by theft — especially identity theft — than by violence; it concentrates in Downtown and South LA and in evening hours; the 2024 drop, the noon spike and the 1st-of-month spike are recording artefacts, not crime trends.

---



## 3. Roles and load

Member A is **Lohith P (BT2024248)**, Member B is **Sri Charan (BT2024143)**, and Member C is **R Anish Reddy (BT2024228)**.

|                  | Member A                                                                                     | Member B                                                                                        | Member C                                                                                                                                         |
| ---------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Task set         | **Data + When** (preprocess owner)                                                           | **Where**                                                                                       | **What and who**                                                                                                                                 |
| Columns owned    | `DATE OCC`, `Date Rptd`, `TIME OCC`, derived hour/weekday/month/delay, artefact flags        | `AREA`, `AREA NAME`, `Rpt Dist No`, `LAT/LON`, `bureau`, `has_coords`, `map_sample`             | `Crm Cd Desc`, `crime_family`, `Part 1-2`, `Premis Desc`, `premise_family`, `vict_age_clean`, `vict_sex_clean`, `victim_recorded`, `Status Desc` |
| Report figures   | 8 (Fig 1–8)                                                                                  | 10 (Fig 9–18)                                                                                   | 10 (Fig 19–28)                                                                                                                                   |
| Candidates built | ~13                                                                                          | ~15                                                                                             | ~15                                                                                                                                              |
| Extra duty       | Preprocess script, `lapd_a1_clean.csv`, Tableau extract, README data section, video minute 1 | Report template, figure numbering, `images/` folder, Tableau Story assembly, workbook packaging | Slides, video recording/editing, AI declaration forms collection, final proofread                                                                |
| Video            | 0:00–1:54 and 4:06–4:55                                                                     | 1:54–2:58                                                                                       | 2:58–4:06                                                                                                                                        |


Shared bridge fields: A uses `crime_family` in two figures; B uses `crime_family` and `hour_occ` in three; C uses `hour_occ`/`delay_days` in one. The chart still belongs to the member whose target it serves.

---



## 4. Shared preprocess (Member A)

**Output:** `lapd_a1_clean.csv` (all rows, original columns minus drops, plus new fields). Tableau connects once, builds an extract; packaged workbook `LatentX_A1.twbx` ships with it. One data source, no joins.


| Step              | Rule                                                                                                                                                                                                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Drop              | `Mocodes`, `Weapon Used Cd`, `Weapon Desc`, `Cross Street`, `Crm Cd 1`–`Crm Cd 4` (keep `Crm Cd`), `Vict Descent`, `LOCATION`.                                                                                                                                           |
| Dates             | `DATE OCC`, `Date Rptd` → date only.                                                                                                                                                                                                                                     |
| `hour_occ`        | `TIME OCC // 100`, 0–23.                                                                                                                                                                                                                                                 |
| `is_noon_default` | 1 if `TIME OCC == 1200`. `is_first_of_month`                                                                                                                                                                                                                             |
| `has_coords`      | 1 if LAT/LON not 0,0 and inside lat 33.70–34.35, lon −118.70 to −118.15; else 0 and null the coords (~2,240 rows).                                                                                                                                                       |
| `map_sample`      | 1 for 200,000 random `has_coords=1` rows, seed 732. Point/density/hex maps filter on it; all aggregates use every row.                                                                                                                                                   |
| `bureau`          | 21-row lookup: Central (Central, Rampart, Hollenbeck, Northeast, Newton), South (77th Street, Southwest, Harbor, Southeast), Valley (Van Nuys, West Valley, N Hollywood, Foothill, Devonshire, Mission, Topanga), West (Hollywood, Wilshire, West LA, Pacific, Olympic). |
| `vict_age_clean`  | keep 1–99; ≤ 0 (LAPD placeholder) and > 99 → null. Report counts removed. `age_bin` = 5-year bins.                                                                                                                                                                       |
| `vict_sex_clean`  | `M`, `F`; `X`, `H`, `-`, blank → `Unknown`. `victim_recorded` = age not null and sex in (M, F).                                                                                                                                                                          |
| `crime_family`    | 10 families from `Crm Cd Desc` keywords: Vehicle theft · Theft from vehicle · Burglary · Other theft · Identity theft & fraud · Simple assault · Aggravated assault, robbery & homicide · Vandalism · Sex offences · Other. Full table in README.                        |
| `premise_family`  | 5 from `Premis Desc`: Street/sidewalk/parking · Residence · Vehicle/transit · Business · Other/public. Table in README.                                                                                                                                                  |


**Tableau calculated fields (native):** Year, Month, Weekday, Week-of-year, Day-of-month from `DATE OCC`; `delay_days = DATEDIFF('day',[DATE OCC],[Date Rptd])`; `delay_bucket` (same day / 1–7 / 8–30 / 31+); `is_2024_partial`; `day_night` (06–17 vs 18–05); shared filter set **Full years 2020–2023** used on every comparison; 2024 shown only in time charts, always grey.

**Colour rules:** sequential single-hue for counts; diverging blue–white–red only for % change; one fixed qualitative palette for the 10 families (same hue for a family in every sheet); grey for 2024 and Unknown; never rainbow.

**Filled maps:** implementer downloads the *LAPD Divisions* polygon layer from LA GeoHub and joins on division name. Fallback: symbol map at division centroids.

**Workbook:** sheets `A01_…`, `B01_…`, `C01_…`; one Tableau Story with three story points holding only the video charts.

---



## 5. Chart types: what to use and what to avoid in Tableau

**Best for this data (high variable density, still lay-readable):** small-multiple heatmaps (trellis), cycle plot, calendar heatmap, dual-axis map (fill + sized circles), hex-bin map, small-multiple line panels, indexed lines, 100% stacked area, treemap coloured by change, age-pyramid trellis, Pareto (bar + cumulative line), bump chart, scatter with size and colour.

**Good as supporting views or subfigures:** highlight table with numbers, stacked ranked bar, 100% stacked bar sorted by a share, histogram, one box plot.

**Avoid:** stand-alone 2-variable bars, pie/donut, packed bubbles, word cloud, radar, 3D, Sankey and chord (painful in Tableau, not lay-readable), parallel coordinates (not lay-readable), anything needing a scalar or vector field (contours, isosurfaces, quiver).

**Other tools:** Tableau does everything below. If the calendar heatmap or Marimekko proves fiddly, Python (matplotlib) with the same palette is an acceptable fallback for that one figure; say so in the report. Do not mix tools otherwise.

---



## 6. Member figure sets

Line format: **Figure title** · Tableau build · variables encoded · why this idiom · what we expect to learn.

### Member A — Data + When (8 figures, Fig 1–8)

Task words: *overview, trend, compare, summarize.*

1. **Fig 1 — Five years, day by day.** Line: daily count 2020–2024 (thin grey) with 28-day moving average (table calc, bold), reference lines at Mar 2020 lockdown and 7 Mar 2024 system change, 2024 shaded · day, count, smoothed count, event annotations · the moving average shows shape without the weekday noise, and annotations carry the two events a lay viewer needs · spring-2020 dip, climb to 2022, plateau 2023, cliff after March 2024.
2. **Fig 2 — Why 2024 is not a crime drop.** Dual-axis: bars = 2024 monthly count; line = 2020–2023 monthly average; labels = 2024 as % of average · month, count, baseline, coverage % · the plainest side-by-side of a year against its norm · Jan–Mar ≈ 90–100%; Apr 68%; May–Nov 40–45%; Dec 24%. Caption: the legacy system stopped receiving new reports on 7 Mar 2024.
3. **Fig 3 — Seasonality, month by month (cycle plot).** Month on columns; inside each month a mini line of 2020→2023 with a per-month mean reference line; 2024 point in grey · month, year, count, month mean · a cycle plot separates season (across panels) from trend (within panel) in one view · summer months higher, February lowest; within every month the 2020→2022 rise is visible; 2024 sits far below from April.
4. **Fig 4 — The week's rhythm differs by crime (heatmap trellis).** Heatmap hour × weekday, one panel per top-6 `crime_family`, colour = share within family · hour, weekday, family, share · one heatmap shows a rhythm; a trellis shows that the rhythm depends on the crime · simple assault peaks Fri/Sat night; vehicle theft peaks evening every day; burglary daytime weekdays; identity theft has a bright 12:00 column (unknown time defaults to noon).
5. **Fig 5 — The calendar (calendar heatmaps, 2020–2023).** Small multiples, one calendar per year: week-of-year × weekday cells, colour = count · date, weekday, year, count · a calendar is the most familiar grid a lay reader knows · the 1st of each month is dark, 1 Jan darkest; March–April 2020 pale (lockdown); weekends slightly darker.
6. **Fig 6 — Recording artefacts (three subfigures).** (a) bar: count by hour with 12:00 highlighted; (b) bar: count by day-of-month with the 1st highlighted; (c) ranked bar: share of reports stamped exactly 12:00, by `crime_family` · hour/day, count, family, share · the two simple bars only earn their place next to (c), which explains who the artefact belongs to · ~1 in 8 reports carries a default noon time; identity theft and fraud highest (victim does not know when it happened); assaults lowest.
7. **Fig 7 — How long before a crime is reported (three subfigures).** (a) histogram of `delay_days` 0–60 plus ">60"; (b) 100% stacked bar of `delay_bucket` by `crime_family`, sorted by same-day share, median-days label; (c) highlight table occurrence-year × report-year (count) · delay, bucket, family, median; occ year, rptd year · distribution, then who owns the tail, then the honest year-crossing count · most reports same or next day; identity theft median weeks; only 94 reports for 2024 crimes were filed in 2025 — no 2025 crime year exists here.
8. **Fig 8 — Year-over-year change by month (highlight table).** Rows Year 2021–2024, columns Month, cell = % change vs same month previous year, diverging colour, numbers shown · year, month, % change, sign · a diverging table shows direction and size at a glance, and it is the one place a diverging palette is right · 2021 vs 2020 rebound in spring; 2022 up across the board; 2023 flat; 2024 deep red from April.

**Candidates built, expected to be cut:** plain year bar; weekday totals bar; weekday × family heatmap; running-total-by-day-of-year race; hour profile weekday vs weekend lines. Kept as sheets in the workbook; one sentence each in the report's "explored, not retained" paragraph.

**Video (A shows 4):** Fig 1, 2, 4, 7(b).

### Member B — Where (10 figures, Fig 9–18)

Task words: *overview, rank, compare, search.*

1. **Fig 9 — Volume and change on one map (dual-axis map).** Filled map of 21 divisions, colour = total 2020–2023 (sequential); overlaid circles at centroids, size = |% change 2020→2023|, colour = sign (diverging) · division, total, change, direction · geography is the natural frame; two layers answer "how much" and "which way" together · Downtown and South LA dark; growth largest where? (confirm).
2. **Fig 10 — Divisions ranked, with what they report.** Stacked horizontal bar: divisions sorted by total 2020–2023, segments = `crime_family`, total label · division, family, count · a ranked bar becomes informative when the bars are decomposed · Central ≈ 2× Foothill; Central's bar is mostly theft; 77th/Southeast bars carry more assault.
3. **Fig 11 — Every division moves together (line trellis).** 21 panels, monthly count 2020–2024, shared y, 2024 grey, coloured by `bureau` · month, count, division, bureau, coverage · 21 lines in one panel would be spaghetti; panels keep each readable · the same rise and the same April-2024 cliff in every panel → systemic.
4. **Fig 12 — What each division reports (heatmap).** Divisions (grouped by bureau) × `crime_family`, colour = row share · division, bureau, family, share · composition matrix · Central/Pacific theft-heavy; 77th/Southeast/Newton assault-heavy; West LA/Wilshire theft-from-vehicle.
5. **Fig 13 — Busiest is not most violent (scatter).** x = total 2020–2023, y = % violent (aggravated + simple assault, robbery, homicide), size = % change 2020→2023, colour = bureau, label = division · four variables · two rankings in one picture · Central high-volume but mid-share; South bureau high-share at moderate volume.
6. **Fig 14 — Where reports sit, day vs night (hex-bin maps).** Two hex-bin maps (HEXBINX/Y on the 200k sample), colour = count, panels `day_night` · location, count, time-of-day · hex bins fix overplotting and respect the hundred-block rounding better than raw points · night tightens onto Downtown, Hollywood, Venice; day spreads along commercial corridors.
7. **Fig 15 — Where each kind of crime sits (density trellis).** Four density maps, one per top-4 `crime_family`, same extent · location, density, family · comparing four small maps beats one map with four colours · vehicle theft everywhere; assault Downtown and South LA; theft from vehicle Westside; identity theft follows residential density.
8. **Fig 16 — A few districts carry the city (Pareto).** Reporting districts sorted by count (bars) with cumulative % line on a second axis; reference line at 80% · district rank, count, cumulative share · the classic "few carry most" chart · roughly the top 20% of districts hold ~50%+ of reports (confirm); the top few are Downtown.
9. **Fig 17 — Ranks barely move (bump chart).** Year 2020–2023 × rank of division, lines coloured by bureau, labels at both ends · year, rank, division, bureau · a bump chart answers "did the order change?" directly · top five stable; movement only in the middle.
10. **Fig 18 — When each division is busy (heatmap).** Division × hour, colour = row share, rows sorted by peak hour · division, hour, share · sorting by peak hour makes the pattern read top-to-bottom · Hollywood and Central late-night peaks; Valley divisions evening peaks.

**Candidates built, expected to be cut:** raw point map coloured by division; histogram of reports per district; division × year highlight table (superseded by Fig 9 + 11); filled map of change alone (folded into Fig 9); dumbbell of volume share vs violent share (superseded by Fig 13).

**Video (B shows 4):** Fig 9, 11, 12, 16.

### Member C — What and who (10 figures, Fig 19–28)

Task words: *overview, rank, compare, summarize.*

1. **Fig 19 — The whole picture (treemap).** Nested `Part 1-2` → `crime_family` → `Crm Cd Desc`, size = count 2020–2023, colour = % change 2020→2023 (diverging) · seriousness, family, description, volume, change · one part-to-whole view that also says what grew · property ≈ 60%, violent ≈ 25%; identity theft the reddest large block.
2. **Fig 20 — Top 15 descriptions, and how they changed.** Bar-in-bar / two measures: sorted bar = count, thin bar or dot = % change 2020→2023, colour = family · description, family, count, change · the standard top-N bar upgraded with change · vehicle stolen first; identity theft third but the fastest riser.
3. **Fig 21 — Which kinds grew (indexed lines).** Year 2020–2023 × (count / 2020 count × 100), one line per family, end labels with 2023 volume · year, family, index, volume · indexing puts a 20k family and a 100k family on one scale · identity theft & fraud ~200 by 2022; vehicle theft ~120; assault ~100–105.
4. **Fig 22 — The mix over time (100% stacked area).** Monthly share by family 2020–2024, 2024 grey-hatched · month, family, share, coverage · shares stay readable even where volume collapses · identity theft band swells in 2022; other bands steady; 2024 mix shifts because the system did.
5. **Fig 23 — Where each kind happens (heatmap or Marimekko).** `crime_family` × `premise_family`, colour = row share. Stretch: Marimekko with column width = family volume · family, premise, share (+ volume) · composition matrix · vehicle theft on street/parking; identity theft at the victim's residence; assaults split residence/street.
6. **Fig 24 — Who is a recorded victim (highlight table).** `crime_family` × Year, cell = % with `victim_recorded`, numbers shown · family, year, share · states the cleaning honestly and shows it is stable · property crimes 10–40%; assault and sex offences > 95%; stable across years.
7. **Fig 25 — Victim age and sex, by crime (pyramid trellis).** Six population pyramids (top-6 families with recorded victims): `age_bin` × count, F left / M right · age, sex, family, count · a pyramid is a familiar shape; six of them show how it changes by crime · intimate-partner assault: women 20–40; robbery/ADW: men 20–40; identity theft: both, 30–60.
8. **Fig 26 — Victim sex by crime (100% stacked bar).** Families sorted by female share, segments F/M/Unknown (grey), count label · family, sex, share, volume · composition sorted by the interesting share · sex offences and intimate-partner mostly female victims; robbery male; theft families mostly Unknown (no person victim).
9. **Fig 27 — What happens to a report (two subfigures).** (a) 100% stacked bar: `Status Desc` share by family, sorted by arrest share; (b) small line: arrest share by year, 2020–2023 · family, status, share, year · outcome composition, then its stability · most reports "Investigation Continued"; assault families highest arrest share; theft lowest; stable over years. Caption: status at data snapshot, not final outcome.
10. **Fig 28 — Identity theft close-up (four subfigures).** (a) monthly count 2020–2024; (b) victim age histogram vs all recorded victims (overlaid, normalised); (c) premise share; (d) `delay_bucket` share vs all crime · month, count, age, premise, delay · the one family that changed most gets one explanatory panel that ties Acts 1 and 3 together · sudden step in 2022; older victims than average; reported at home; reported weeks late. Caption: we do not know the cause from this data.

**Candidates built, expected to be cut:** box plot of age by family (superseded by Fig 25 unless it adds); premise × hour heatmap; Part 1 vs 2 by year stacked bar (folded into Fig 19 colour/nesting); plain top-15 bar (superseded by Fig 20); victim age histogram alone (folded into Fig 28b).

**Video (C shows 4):** Fig 19, 21, 25, 28.

---



## 7. Video spine (4:55; detailed script in `VIDEO_PPT_SCRIPT.md`)


| Time      | Who | Figure           | Point                                                                |
| --------- | --- | ---------------- | -------------------------------------------------------------------- |
| 0:00–0:14 | A   | Slide 1          | Team greeting, names, and project title.                              |
| 0:14–0:31 | A   | Slide 2          | Central question and three-act sequence.                              |
| 0:31–0:58 | A   | Slide 3          | Source, grain, concise preprocessing, comparison window.              |
| 0:58–1:42 | A   | Fig 1, Fig 2     | Rise, 2023 plateau, and 2024 legacy-coverage break.                   |
| 1:42–1:54 | A   | Tableau Fig 7    | Three-sheet workbook; identity-theft reporting delay.                 |
| 1:54–2:44 | B   | Fig 9, Fig 12    | Division volume versus row-normalized crime-family mix.               |
| 2:44–2:58 | B   | Tableau Fig 16   | Pareto interaction; 80% at reporting-district rank 623.               |
| 2:58–3:50 | C   | Fig 19, 21, 28   | Absolute volume, indexed growth, and identity-theft close-up.         |
| 3:50–4:06 | C   | Tableau Fig 28   | Monthly peak and long-delay comparison.                               |
| 4:06–4:43 | A   | Slide 7          | Patterns versus artefacts; exact closing sentence and limits.         |
| 4:43–4:55 | A   | Slide 8          | Completeness, GitHub link, and close.                                  |


Slides: team/title, question, preprocess, one evidence slide per act, synthesis, and completeness. Each Tableau clip briefly shows the workbook interface, then one numbered figure and one inference.

---



## 8. Report outline

1. Title, team, date.
2. **Dataset.** Source paragraph (required): *The assigned list item was "LAPD Crime Data 2020–2024" via a Kaggle upload (*`aadigupta1601/lapd-crime-data-2020-2024`*, now 403); a later Kaggle mirror (*`saurabhbadole/crime-incidents-in-los-angeles-2020-to-present`*) is a snapshot of 18 Aug 2024. We asked the course staff whether the official LAPD Open Data table could be used instead; the reply (10 Sep 2026) was to use whichever is better and note it in the report. We use the official "Crime Data from 2020 to Present" table (data.lacity.org, 2nrs-mtv8, CC0), frozen as* `Crime_Data_from_2020_to_2024.csv`*: 1,004,894 rows, 28 columns, one row per report, occurrence dates 1 Jan 2020 – 30 Dec 2024. LAPD moved to a NIBRS system on 7 Mar 2024, so 2024 in this table is incomplete (127,567 rows; monthly counts fall from ~19k to 5–8k after March). The separate NIBRS tables use a different grain (one row per offence) and only reach normal volume in 2025, so they are not merged here. The same frozen file will be used for A2 and A3.* Then a facts table and column groups used/dropped.
3. **Question and tasks.** The question; three task sets with verbs; one paragraph on Schulz et al.
4. **Preprocessing.** §4 table, counts removed per step, family mapping summary, sample method, extract.
5. **Act 1 — When (A).** Fig 1–8.
6. **Act 2 — Where (B).** Fig 9–18.
7. **Act 3 — What and who (C).** Fig 19–28.
8. **Explored, not retained.** One paragraph per member naming the cut candidates and why (this shows we generated more than we kept).
9. **What the story says.** Closing paragraph; how the acts connect.
10. **Limits and what we do not claim.** §9 below.
11. **Author contributions.** Per member: task set, figures built, extra duty, sections written, video segment.
12. **AI declaration forms.** One per member.
13. **Appendix.** Family and premise mapping tables; README of images.

**Caption pattern:** *What is drawn* (marks, axes, colour, filters, years; subfigure letters) → *why this idiom* (one clause on channel or task) → *what we conclude* (one plain sentence, caveat if any). Every figure is cited in the body text before it appears ("Figure 4 shows …").

**Images:** `images/Fig1.png … Fig28.png`, ≥ 1600 px wide; subfigures exported as one composed image per figure. Extra sheets go to `images/extra/` and are listed in the README.

**Marks/channels rationale (reused):** bars = length on a common baseline; lines = position + connection for ordered time; heatmaps/calendars = colour luminance for pattern, highlight tables add numbers where exact values matter; maps = geographic position with sequential fill, circles add a second quantity by size; hex bins = area-aggregated position; treemap = area (weakest) so it carries labels and a colour for change; scatter = two positions plus size and hue; family hues fixed across all sheets; diverging colour only where zero means "no change"; grey = partial or unknown.

---



## 9. What we will not chart and will not claim

**Will not chart:** Weapon, Cross Street, Crm Cd 2–4, Mocodes (mostly empty or coded); victim descent (dropped; invites race-as-cause); 2024 in any year-to-year comparison (time charts only, grey, labelled); raw victim age before cleaning; anything per-capita (no population by division); pie/donut, packed bubbles, word clouds, radar, 3D; parallel coordinates and node-link (no fit for a flat event table); contours, isosurfaces, volume rendering, quiver (no field data); more than one box plot; any figure whose only job is to reach a count.

**Will not claim:** "crime fell in 2024"; that report counts equal crime incidence; exact locations or exact times where the data is rounded or defaulted; any cause for the identity-theft rise, divisional differences or victim demographics; forecasts, hotspot policing or risk scores; rankings of unequal-size divisions as if they were rates.