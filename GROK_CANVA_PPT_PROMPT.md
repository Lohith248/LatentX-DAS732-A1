# Grok / Canva Prompt — Team LatentX A1 Video Deck

## What to attach (only these)

Do **not** drop the whole project folder, all 28 figures, CSVs, or Tableau workbooks into Canva/Grok. Those extra files are for the video demo and the report, not the PPT.

Attach **exactly 8 items** plus the crime template:

### 1. Script (required)

`C:\Users\jagat\Desktop\Sem 5\DV\VIDEO_PPT_SCRIPT.md`

### 2. Crime PPT template (required)

Attach the Canva/crime template you already selected, or paste its Canva link.

### 3. Slide images (required — these 7 only)

Use the copies in `images\`. Do not also attach `report\overleaf_images\` (same files).

| Slide | Role on slide | Full path |
|---|---|---|
| 4 left, dominant | Daily trend | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig1.png` |
| 4 right, supporting | 2024 coverage | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig2.png` |
| 5 left | Division map | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig9.png` |
| 5 right | Division mix heatmap | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig12.png` |
| 6 small card | Crime-type treemap | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig19.png` |
| 6 dominant | Indexed family growth | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig21.png` |
| 6 small card | Identity-theft close-up | `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig28.png` |

### Do not attach to the PPT bot

These stay on disk for the **live Tableau recording**, not Canva:

| Demo | Open this file | Then open this view |
|---|---|---|
| Figure 7 | `C:\Users\jagat\Desktop\Sem 5\DV\tableau\A07\A07 Report delay.twbx` | sheet `A07b Delay by family` |
| Figure 16 | `C:\Users\jagat\Desktop\Sem 5\DV\tableau\FINAL_SUBMISSION_MEMBER_B\FINAL_SUBMISSION_MEMBER_B\LatentX_B_FINAL.twbx` | dashboard `Figure 16` |
| Figure 28 | `C:\Users\jagat\Desktop\Sem 5\DV\tableau\Final_submission_C\qwerty.twbx` | sheets `C28a_Identity_Monthly` then `C28d_Identity_Delay` |

Also do **not** attach:

- `Crime_Data_from_2020_to_2024.csv`
- `lapd_a1_clean.csv`
- `images\Fig3.png` through `Fig8.png`, `Fig10.png`, `Fig11.png`, `Fig13.png`–`Fig18.png`, `Fig20.png`, `Fig22.png`–`Fig27.png`
- the report PDF/TeX

---

## Copy-paste prompt

Paste everything below this line into Grok after attaching the 8 files listed above.

---

Create an editable **eight-slide, 16:9 academic Canva presentation** for a five-minute DAS732 Data Visualization video.

Use the attached crime template as the design system. Use the attached file `VIDEO_PPT_SCRIPT.md` as the exact content specification and single source of truth.

I have attached **only** the files needed for the deck. Use each attached PNG on the slide named below. Do not ask for more images. Do not invent replacements. Do not use any other figure from the project.

### Attached files and where to place them

| Attached file | Put it here |
|---|---|
| `VIDEO_PPT_SCRIPT.md` | Content source for headings, tables, metric cards, caveats, and all presenter notes |
| Crime template / template link | Visual system for all 8 slides |
| `Fig1.png` | Slide 4, left, dominant |
| `Fig2.png` | Slide 4, right, supporting |
| `Fig9.png` | Slide 5, left |
| `Fig12.png` | Slide 5, right |
| `Fig19.png` | Slide 6, small evidence card (absolute volume) |
| `Fig21.png` | Slide 6, dominant chart (relative growth) |
| `Fig28.png` | Slide 6, small evidence card (identity-theft close-up) |

Full disk paths of those images, if you need them for labels:

- `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig1.png`
- `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig2.png`
- `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig9.png`
- `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig12.png`
- `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig19.png`
- `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig21.png`
- `C:\Users\jagat\Desktop\Sem 5\DV\images\Fig28.png`

Slides 1, 2, 3, 7, and 8 have **no chart PNG**. Build those from the script text, tables, and diagrams only.

### Project identity

**Team:** Team LatentX  
**Project title:** Reading Reported Crime Without Reading Recording Artefacts as Trends  
**Subtitle:** LAPD Legacy Reports, 2020–2024  
**Course:** DAS732 Data Visualization · IIIT Bangalore · T1 2026–27

**Authors**

- Lohith P (BT2024248)
- Sri Charan (BT2024143)
- R Anish Reddy (BT2024228)

The deck explains a real data-analysis workflow. It is not a crime drama, detective narrative, fictional case, or sensational news package.

### Mandatory output rules

1. Create exactly **eight slides** in the order specified in `VIDEO_PPT_SCRIPT.md`.
2. Use the exact headings, concise on-slide wording, values, tables, speaker ownership, and timings in that file.
3. Put every block labelled **Exact spoken script** into that slide’s presenter notes. Do not paraphrase it.
4. Keep the separate Tableau demo directions in presenter notes immediately after Slides 4, 5, and 6. Those demos are live recordings, not extra slide images.
5. Use all seven attached figure images on their assigned slides.
6. Use the PNGs as real images. Never redraw, recreate, trace, recolour, retype, stylize, or replace any chart.
7. Preserve chart axes, legends, labels, proportions, and data. Crop only blank outer margins.
8. Do not invent values, additional analysis, maps, charts, sources, or conclusions.
9. Keep all body text readable in a 1920×1080 screen recording.
10. Return an editable Canva presentation and an export-ready PPTX.

### Data-integrity rules

- Say “reports” or “reported records”; do not present counts as population-normalized incidence or risk.
- Treat 2020–2023 as the comparable full-year window.
- Treat 2024 only as incomplete legacy-system coverage after the 7 March 2024 transition.
- Never imply a real citywide crime decline in 2024.
- Do not infer causes for identity-theft growth or divisional differences.
- Do not use victim descent/race.
- Do not imply exact addresses; locations are hundred-blocks.
- Do not turn division counts into “danger” or predictive hotspots.
- Exact-noon stamps are about 3.5% of the complete freeze, not “one in eight.”

### Visual direction

- Preserve the selected template’s typography, grid, and recurring motifs.
- Adapt sensational “crime” elements into a restrained academic treatment.
- Use dark navy/charcoal for structure, white or warm off-white for readability, and muted red only for recording artefacts or supported emphasis.
- Use generous margins and a consistent top title band.
- Keep figure screenshots visually dominant.
- Use concise labels, metric cards, and takeaways instead of paragraphs.
- Use the same `TASK · VISUALIZATION SOLUTION · INFERENCE` strip on Slides 4–6.
- Use flat line icons only on the preprocessing slide.
- Do not use blood, weapons, police tape, handcuffs, sirens, badges, mugshots, evidence boards, fingerprints, newspaper clippings, “case file” wording, red-string diagrams, or generated crime-scene imagery.
- Do not generate fake LAPD or IIIT Bangalore logos.
- Avoid 3-D effects, bevels, neon, glitch transitions, heavy shadows, and decorative clutter.
- Use only subtle fades or simple appear animations; every slide must work with animation disabled.

### Slide-by-slide build

#### Slide 1 — Team and project opening

- Eyebrow: `TEAM LATENTX PRESENTS`.
- Display the exact project title, subtitle, course line, all three names, and roll numbers.
- Make Team LatentX and the project title the visual focus.
- A faint LA outline or subtle street-grid texture may be used decoratively.
- Do not place a data chart here. No PNG.

#### Slide 2 — Question and story structure

- Heading: `One question guides the entire analysis`.
- Display the exact central question from the script.
- Build the exact three-act flow:
  `WHEN — Lohith` → `WHERE — Sri Charan` → `WHAT / WHO RECORDED — R Anish Reddy`.
- Include the short task targets beneath each act.
- Label the arrows as narrative sequence, not causation.
- No PNG.

#### Slide 3 — Data and preprocessing

- Heading: `First, make one million reports comparable`.
- Build the exact seven-step horizontal preprocessing pipeline.
- Add the four fact cards as a compact table or aligned card grid.
- Ensure these are immediately visible:
  `1,004,894 reports`, `DR_NO = one report`, `2020–2023`, `200,000-row sample`, `7 Mar 2024`.
- Include the NIBRS/grain footer.
- Keep the slide clean enough to narrate in 27 seconds.
- No PNG.

#### Slide 4 — Act I: When

- Heading: `When: a rise, a plateau—and a broken series`.
- Insert attached `Fig1.png` as the dominant left visual.
- Insert attached `Fig2.png` as the supporting right visual.
- Add the metric strip, three rubric boxes, callouts, and caveat exactly as specified.
- Do not add another chart.
- Put the Figure 7 Tableau instructions and exact demo narration into presenter notes after the slide narration.

#### Slide 5 — Act II: Where

- Heading: `Where: volume concentrates, but crime mix differs`.
- Insert attached `Fig9.png` left.
- Insert attached `Fig12.png` right.
- Keep the map legend and heatmap labels readable.
- Add the rubric strip, three metric cards, and not-a-rate caveat exactly as specified.
- Put the Figure 16 Tableau instructions and demo narration into presenter notes.

#### Slide 6 — Act III: What and who

- Heading: `What changed: theft—especially identity theft`.
- Insert attached `Fig21.png` as the dominant chart.
- Insert attached `Fig19.png` as the smaller absolute-volume evidence card.
- Insert attached `Fig28.png` as the smaller identity-theft close-up card.
- Maintain a clear hierarchy: relative change first, absolute volume second, close-up third.
- Add the rubric strip, three metric cards, and recorded-victim limitation.
- Put the Figure 28 Tableau instructions and demo narration into presenter notes.

#### Slide 7 — Synthesis

- Heading: `One question, three task sets, one answer`.
- Build the exact WHEN → WHERE → WHAT synthesis diagram.
- Build the exact two-column table:
  `PATTERNS SUPPORTED` versus `RECORDING ARTEFACTS`.
- Do not add a chart. No PNG.
- Display the exact closing sentence verbatim. It must be readable, not tiny footer text.
- Arrows must communicate narrative sequence only.

#### Slide 8 — Reproducibility and close

- Eyebrow: `COMPLETE SUBMISSION`.
- Heading: `Reproducible and reviewable`.
- Use the four deliverable cards, official source line, team footer, and GitHub URL from the script.
- Optional: add a QR code for the exact GitHub URL, but retain the typed URL.
- Keep this as a clean end frame.
- No PNG.

### Presenter notes and handoffs

Use these speakers exactly:

- Slides 1–4: Lohith P
- Slide 5: Sri Charan
- Slide 6: R Anish Reddy
- Slides 7–8: Lohith P

After Slide 4 notes, add:

`CUT TO LIVE TABLEAU — FIGURE 7 — 12 SECONDS`

Workbook (do not import into Canva): `C:\Users\jagat\Desktop\Sem 5\DV\tableau\A07\A07 Report delay.twbx`

After Slide 5 notes, add:

`CUT TO LIVE TABLEAU — FIGURE 16 — 14 SECONDS`

Workbook (do not import into Canva): `C:\Users\jagat\Desktop\Sem 5\DV\tableau\FINAL_SUBMISSION_MEMBER_B\FINAL_SUBMISSION_MEMBER_B\LatentX_B_FINAL.twbx`

After Slide 6 notes, add:

`CUT TO LIVE TABLEAU — FIGURE 28 — 16 SECONDS`

Workbook (do not import into Canva): `C:\Users\jagat\Desktop\Sem 5\DV\tableau\Final_submission_C\qwerty.twbx`

The spoken presentation must refer to them as Figure 7, Figure 16, and Figure 28. Internal worksheet names such as A07b or C28d belong only in presenter notes and must not appear as the public title of the demo.

### Final quality audit

Before returning the deck, verify:

- Exactly eight slides.
- Exactly the seven supplied PNGs are used where specified.
- No extra project image was requested or invented.
- No chart or value was altered.
- All names and roll numbers are correct.
- Every slide contains its exact narration in presenter notes.
- Each member introduces themselves before explaining their task.
- Each member explains a task, visualization solution, and inference.
- Slides 4–6 include the consistent rubric strip.
- The full script plus Tableau clips targets 4:50–4:55.
- The deck is lay-readable at 1080p.
- 2024 is always framed as incomplete legacy coverage.
- The design is academic and polished, not sensational or theatrical.
