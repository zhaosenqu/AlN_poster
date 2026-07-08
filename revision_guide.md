# Poster Revision Guide — *Seeding Wurtzite AlN on Amorphous SiO₂*
### For the ORNL RSI poster competition

Every concern from the critical review is addressed below, grouped by the seven
evaluation criteria. Each item is labeled:

- **✅ FIXED** — exact replacement text is given; paste it into PowerPoint.
- **🔧 CODE** — a runnable fix ships in the accompanying scripts (`poster_style.py`,
  `check_colorblind.py`, `fig3_recolored_demo.py`).
- **⚠️ MISSING** — depends on data or a decision only you have. I give the wording
  for each branch and label exactly what to confirm.

---

## 0. Print-blockers — do these first

| # | Item | Status |
|---|------|--------|
| 1 | Acknowledgment still reads `LDRD… .` (unfilled placeholder) | ⚠️ → §7.1 |
| 2 | **Two figures are numbered "Fig 5"** (rocking-curve overlay *and* roughness plot) | ✅ → §3.1 |
| 3 | Two AFM images have no figure number and no caption | ✅ → §3.4 |
| 4 | "BEOL-compatible" conflicts with the 600 °C step | ✅ → §6.1 |
| 5 | 102 % bulk density is unphysical as written | ✅ → §6.3 |
| 6 | `X⁽²⁾` should be `χ⁽²⁾` (two places) | ✅ → §5.3 |
| 7 | No untreated-SiO₂ control ⇒ template effect not isolated from the leak fix | ⚠️ → §1.1 |

---

## 1. Overall theme & cohesion

### 1.1 The template effect is confounded with the chamber repair ⚠️ MISSING (CRITICAL)

The leak repair and the oxynitride template arrived together, so nothing on the
poster separates "we fixed the O₂ leak" from "the template seeds texture." Yet the
title and the **What we showed** box attribute the texture to the template.

**Decide one of two branches:**

- **Branch A — a post-repair run on *untreated* SiO₂ exists.**
  Add it to Fig 3 as a labeled bar (e.g. "#xx no plasma, post-repair"). One bar
  showing broad/absent texture *without* the template, next to the treated bars,
  is the single most persuasive data point you can add. This converts the causal
  claim from "proposed" to "demonstrated."

- **Branch B — no such control exists (likely).** Keep the causal language
  hedged and lean on prior literature that *directly* shows the plasma forms the
  interfacial layer (you have this in your library):
  - Hayden 2023 — XPS depth profiling shows the Ar/N₂ plasma converts native
    oxide to a nitrogen-rich oxynitride SiOₓNᵧ.
  - Mercer 2025 — cross-sectional TEM + EELS resolve an amorphous SiNₓ / Si₃N₄
    interlayer after plasma treatment.

  Then make the untreated-SiO₂ control your headline **future work** line. See
  §6.2 for the exact hedged wording that keeps the story honest and still strong.

### 1.2 Consolidate the two takeaway boxes ✅ FIXED

Right now **What we showed** (bottom-left) and **Why it matters** (bottom-center)
are split across columns. Merge into one closing panel titled
**"6. Conclusions & outlook"** placed at the bottom of column 4 (where a reader's
eye finishes). Suggested content:

> **6. Conclusions & outlook**
> A 10-minute N₂/Ar plasma converts amorphous SiO₂ into an interfacial
> oxynitride that seeds (0002)-textured wurtzite AlN — no epitaxial substrate,
> no seed layer, ≤ 600 °C. Best 600-nm films reach ω-FWHM = 1.09° with
> near-bulk density and sub-nm roughness. Because SiO₂ is the cladding in every
> photonics foundry stack, this is a low-thermal-budget route to χ⁽²⁾ waveguides
> on glass for the ORNL Lab-to-Fab QPIC platform.
> **Next:** (i) untreated-SiO₂ control to isolate the template; (ii) XPS / X-TEM
> to confirm interface chemistry; (iii) lower-temperature oxynitridation for true
> BEOL compatibility.

---

## 2. Layout & fitting

### 2.1 Section 3 bullets duplicate the Fig 2 caption ✅ FIXED

The three bullets restate the caption almost verbatim (1.09°, 6× rate, the leak).
Cut the overlap. Replace the Section-3 bullet block with:

> - **Runs 1–13 were X-ray amorphous** across every temperature (250–500 °C),
>   power (150–350 W), geometry, and gas ratio we tried.
> - **Root cause:** an air leak in the Ar line. Trace O₂ poisoned the Al target
>   (6× slower growth) and suppressed wurtzite nucleation.
> - **After repair + template:** every film shows the AlN E₂(high) Raman mode
>   (657 cm⁻¹) and 0002 texture; ω-FWHM tightened 1.74° → 1.09° (−37 %).

Let the caption carry the numbers; let the bullets carry the *logic*.

### 2.2 Whitespace ✅ FIXED

After you consolidate the takeaway boxes (§1.2) and trim §2.1, column 2 gains
room. Nudge Fig 2 up ~1 cm and give the "Lessons from preliminary results" box a
little more internal padding so it reads as three distinct lessons.

---

## 3. Figures & captions

### 3.1 Duplicate figure number ✅ FIXED

There are two "Fig 5"s. Renumber left-to-right, top-to-bottom across the whole
poster and standardize the label style to **"Fig N."** (period, bold number):

| Panel | Current | New |
|-------|---------|-----|
| Schematic (col 1) | Fig 1 | **Fig 1** |
| FWHM chronology (col 2) | Fig 2 | **Fig 2** |
| Rocking-curve bars (col 3) | Fig 3 | **Fig 3** |
| Coherence + lattice (col 3) | Fig 4 | **Fig 4** |
| RC/2θ overlay (col 3) | Fig 5 | **Fig 5** |
| Roughness vs run (col 4) | **Fig 5 (dup)** | **Fig 6** |
| Feature Ø vs run (col 4) | Fig 6 | **Fig 7** |
| Density + thickness (col 4) | Fig 7 | **Fig 8** |
| AFM topographies (col 4) | *(none)* | **Fig 9(a,b)** |

Then update every in-text/caption reference to match. Also fix the mixed
"Fig 5" vs "Fig. 5" styling — pick **"Fig N."** everywhere.

### 3.2 Caption depth is inconsistent ✅ FIXED

Fig 1 gets four sentences; Fig 7's whole caption is one clause. Bring the terse
column-4 captions up to a uniform "assertion + method + scale" pattern:

- **Fig 6 (roughness):** "AFM RMS roughness Sq stays sub-nanometer (0.36–0.70 nm,
  1 µm contact-mode scans) across the entire process window. The 60-min
  literature-style oxynitridation (run #27, Mercer-style recipe) is the lone
  outlier at 4–7× rougher; the grounded-stage control (#23, off-scale) is 100×
  rougher."
- **Fig 7 (feature size):** "Median AFM in-plane feature diameter (17–26 nm)
  tracks the XRD out-of-plane coherence length (25–30 nm). Because both are far
  smaller than the 600-nm film thickness, each grain is a tall, narrow column —
  i.e. the film is columnar." *(see §3.3 for the logic fix)*
- **Fig 8 (density/thickness):** "XRR-derived mass density is 90–102 % of bulk
  AlN (3.26 g cm⁻³) within fit uncertainty; 10-min films are 124–126 nm,
  i.e. a steady 12.5 nm min⁻¹ after the O₂ repair." *(see §6.3)*

### 3.3 Fig 7 (was Fig 6) logic reads backwards ✅ FIXED

"lateral ≈ vertical length scale → columnar grains" is self-contradictory as
written: equal lateral and vertical sizes describe *equiaxed*, not columnar,
grains. The real argument is that the coherently diffracting length (≈ lateral
grain width, ~20–30 nm) is **much smaller than the 600-nm thickness**, so grains
span the thickness as thin columns. Fix the on-figure headline to:

> **grain width ≈ XRD coherence ≪ film thickness → columnar grains**

and the caption as in §3.2. The "vertical length scale" you plotted is the
coherence length, *not* the thickness — say so explicitly.

### 3.4 AFM images are orphaned ✅ FIXED (labels) / ⚠️ MISSING (which is which)

Two topography maps sit at bottom-right with **raw pipeline filenames** as titles
(`22_0624_1um_1.0_00002`, `27_0629_Mercer_1um_1.0_00000`) and no caption.

- Replace the on-image titles with human-readable labels. In your AFM plotting
  script, change `ax.set_title(fname)` to a label map (drop-in in §8.3).
- Add a shared caption. Confirm what the two panels contrast (⚠️): the filenames
  imply **(a)** run #22, your 10-min-style process vs **(b)** run #27, the 60-min
  Mercer-style recipe. If so:

> **Fig 9.** Representative 1 µm AFM topographies. **(a)** Run #22, short
> oxynitridation: fine, uniform sub-nm texture (Sq ≈ 0.5 nm). **(b)** Run #27,
> 60-min Mercer-style oxynitridation: coarser mounds, 4–7× rougher. Color bars in
> nm; note the different z-scales.

**Confirm before printing:** which run each panel actually shows, and that the two
color-bar z-scales are called out (they differ: ±0.8 nm vs ±7 nm — a reader will
misread relative roughness otherwise).

### 3.5 Fig 5 overlay shares one axis for two different scans ✅ FIXED

The overlay plots the rocking curve (Δω) and the 2θ scan (Δ2θ) on a single
"angular offset" axis without noting they are different scan axes. Add one clause
to the caption:

> **Fig 5.** Overlay of the 0002 rocking curve (Δω, mosaic tilt) and the
> symmetric 2θ–ω scan (Δ2θ, d-spacing spread) for run #28, each centered and
> normalized. The ~4× wider rocking curve (FWHM 1.10° vs 0.28°) shows mosaic
> tilt, not lattice-spacing variation, dominates the 0002 breadth.

### 3.6 Fig 4(a) shows values but no error bars ✅ CODE

The coherence-length bars print "29, 29, …" with no uncertainty, which sits
awkwardly next to "every number carries an error bar." Add Scherrer-propagated
error bars. Pattern in §8.2; the same `ax.errorbar(...)` call is already wired
into `fig3_recolored_demo.py`.

---

## 4. Color scheme 🔧 CODE

### 4.1 The problem, confirmed

I simulated your figures under the three common color-vision deficiencies. In
**Fig 2** the red ✗ (failure) and green ● (good) collapse toward the same muddy
hue under deuteranopia/protanopia; only the differing marker *shapes* rescue them.
In **Fig 3** the green and teal bars are close in both hue and luminance.

### 4.2 The fix — ships as code

`poster_style.py` defines a colorblind-safe **Okabe–Ito** palette mapped to your
existing semantics (green = thick/good, a distinct blue = thin, orange = best,
vermillion = failure, gray+hatch = excluded). It also bumps every figure's font
sizes for poster distance.

```python
from poster_style import POSTER_COLORS as C, HATCH, apply_poster_style
apply_poster_style(fig_width_in=7.5)      # width the figure occupies on the poster
ax.bar(x, y, color=C["thick"])            # #009E73  bluish green
ax.bar(x, y, color=C["thin"])             # #0072B2  blue  (was teal)
ax.bar(x, y, color=C["best"])             # #E69F00  orange
```

Redundant encoding is built in: the AFM scan-size series also differ by marker
shape (`o / s / D`), and "excluded" carries a hatch — so the figures survive even
in grayscale.

**Verify before printing:** export each figure to PNG and run

```bash
python check_colorblind.py fig3.png fig6.png fig7.png
```

It writes `*_cvd.png` with Original | Deuteranopia | Protanopia | Tritanopia side
by side. I ran it on the recolored Fig 3 (`fig3_recolored.png`) and all series
stay distinct in every panel — use that as the target.

---

## 5. Typography

### 5.1 Body text passes, figure internals don't ✅ CODE

Measured body sizes are fine for a 40-in poster (72 pt title / 37 pt headers /
24 pt body). The weak point is **inside** the matplotlib figures: tick labels,
the Fig 3 run-condition labels, and the overlay annotations render at ~12–15 pt
equivalent — fine print at conversation distance, and the Fig 3 condition labels
*are* the experiment. `apply_poster_style()` fixes this.

> **Point-size math (important):** matplotlib text is vector text, so it scales
> with the figure when you resize it in PowerPoint. To land ≥ 18 pt on the
> printed poster, generate each figure at the **physical width it will occupy**
> (measure it, in inches) and pass that as `fig_width_in`. If you shrink a figure
> by a factor *k* after export, multiply all point sizes by 1/*k*. The helper
> already scales everything from a single `fig_width_in` knob.

### 5.2 Mechanical inconsistencies ✅ FIXED

Standardize globally:

- **Space before units:** `600nm` → `600 nm`. (You already write `125 nm`.)
- **En dash for ranges, spaced hyphen never:** `10 - 50 W` → `10–50 W`;
  `0.36-0.70 nm` → `0.36–0.70 nm`; keep `2.0–3.1 mTorr`.
- **Percent spacing — pick one:** either `90–102 %` and `<0.08 %` (spaced), or
  `90–102%` and `<0.08%` (unspaced). Don't mix. (SI style is spaced; many
  journals use unspaced. Choose one and apply everywhere.)
- **Degrees:** consistent `°C` and `1.09°` (no space before ° for angles;
  no space in `°C`).

### 5.3 `X⁽²⁾` → `χ⁽²⁾` ✅ FIXED

The second-order nonlinear susceptibility is a Greek chi. It appears as a Latin
"X" in **Section 1** ("strong X⁽²⁾ nonlinearity") and in **Why it matters**
("unlocks X⁽²⁾ waveguides"). Replace both with **χ⁽²⁾**. (In PowerPoint: Insert →
Symbol → Greek small letter chi, or paste χ.)

### 5.4 Font harmony (optional polish) ✅ CODE

Body text is Aptos; figures are Arial. Not wrong, but harmonizing looks
deliberate. `apply_poster_style()` sets the figure font to Arial/Helvetica, which
reads as a near-match to Aptos. (Or switch the whole poster to Arial for a single
family.)

---

## 6. Scientific content

### 6.1 "BEOL-compatible" vs the 600 °C step ✅ FIXED

Back-end-of-line thermal budgets are conventionally ≤ 400–450 °C, but your
oxynitridation is 600 °C (the AlN growth itself is only 350 °C). A photonics
reviewer will flag this. Two honest options:

- **Preferred wording** (keeps the strong claim, drops the overreach):
  > "A **low-thermal-budget** route to textured AlN on glass — 350 °C growth,
  > ≤ 600 °C total, far below the >1000 °C of epitaxial AlN — compatible with
  > CMOS back-end integration once the oxynitridation temperature is reduced."
- Or state the target explicitly and move BEOL to outlook: note that Mercer 2025
  reports AlN-family growth "< 400 °C … compatible with back-end processing," so
  lowering your 600 °C plasma step is a concrete, literature-grounded next step.

Do **not** leave the bare claim "BEOL-compatible" next to a 600 °C process.

### 6.2 No direct evidence the oxynitride layer exists ⚠️ MISSING → hedge + cite

You did not measure the interface in *this* work (no XPS/ellipsometry/FTIR/TEM),
yet **What we showed** states the plasma "converts amorphous SiO₂ into an
oxynitride template." Fix by (a) keeping "proposed/consistent-with" language and
(b) citing the prior *direct* evidence you already have:

> "Consistent with prior XPS (Hayden 2023) and cross-sectional TEM/EELS
> (Mercer 2025) showing that an Ar/N₂ plasma nitridizes the SiO₂ surface into a
> N-rich SiOₓNᵧ / SiNₓ interlayer, we propose this plasma-formed oxynitride seeds
> (0002) texture. Direct interface characterization (XPS, X-TEM) is the immediate
> next step."

Fig 1's caption already says "**proposed** to promote"; make the conclusion box
match that hedge (it currently drops it).

### 6.3 102 % bulk density is unphysical ✅ FIXED / ⚠️ (exact ± is yours)

Density can't exceed the bulk value; 102 % is XRR fit scatter. Report it as
fully-dense-within-uncertainty rather than a range that crosses 100 %:

> "XRR mass density is **97 ± X %** of bulk AlN (3.26 g cm⁻³) — i.e. fully dense
> within fit uncertainty (per-run range 90–102 %)."

Fill in the mean and ± from your Parratt-fit error bars (⚠️ the plot already
shows error bars; read off the mean and typical uncertainty). Keep the "90–102 %"
only as a parenthetical range, not the headline.

### 6.4 "no soak" is undefined ✅ FIXED / ⚠️ confirm meaning

Run #29's label "2.5 mTorr, no soak" and the Fig 3 caption ("without 350 °C
soaking") use an undefined term. Add a one-line footnote under Fig 3:

> "*no soak* = growth initiated without the 350 °C pre-growth substrate hold."

⚠️ Confirm that's the intended meaning (vs. no pre-sputter soak of the target).

### 6.5 74-min growth appears in no figure ⚠️ MISSING (minor)

Methods list "10–74 min," but no shown run is obviously 74 min. Likely just the
span of conditions — confirm the figure runs fall inside the stated range, or
trim the range to what you actually plot. Low priority.

### 6.6 Lattice constants need a citation ✅ FIXED / ⚠️ pick one

Fig 4 uses a = b = 3.110 Å, c₀ = 4.980 Å, space group P6₃mc. Add a citation for
the reference wurtzite-AlN cell (any standard AlN structure ref in your library
works — e.g. Yu 2021 AlN-crystals review, or the Iqbal 2018 sputtering review).
Add "(ref. [x])" after the values in the Fig 4 caption.

---

## 7. Additional — grammar, citations, acknowledgments

### 7.1 Acknowledgment placeholder ⚠️ MISSING → template provided

`LDRD… .` must be completed. Below is competition-ready text built from the
official CNMS / LDRD / UT-Battelle language. **Confirm the bracketed items with
Dr. Kelley** (the project title and any award number — from the funding proposal
the working title is *"Nonlinear Quantum Materials from Lab-to-Fab for Monolithic
Integrated Quantum Photonics,"* LOIS ID 12023):

> **Acknowledgments.** This research was supported by the Laboratory Directed
> Research and Development Program of Oak Ridge National Laboratory (project
> *"[Nonlinear Quantum Materials from Lab-to-Fab for Monolithic Integrated
> Quantum Photonics]"*), managed by UT-Battelle, LLC, for the U.S. Department of
> Energy. This work was performed in part at the Center for Nanophase Materials
> Sciences (CNMS), a U.S. DOE Office of Science User Facility. Z.Q. gratefully
> acknowledges the ORISE Research Science Internship (RSI) program. This
> manuscript has been authored by UT-Battelle, LLC under Contract No.
> DE-AC05-00OR22725 with the U.S. Department of Energy.

(The final contract-number sentence is standard for ORNL-authored work; keep or
drop depending on space — the LDRD and CNMS sentences are the essential two.)

### 7.2 "et. al." → "et al." ✅ FIXED

"et al." is an abbreviation of *et alii*; "et" is a whole word and takes **no
period**. Fix in the **Key references** line ("Xu et. al.") and in the **Fig 6
annotation** ("recipe from Mercer et. al."). → "Xu et al.", "Mercer et al."

### 7.3 References lack titles / DOIs ✅ FIXED

Replace the compressed reference line with full, verified entries (pulled from
your library and confirmed):

> 1. J. Hayden, J. Shepard, and J.-P. Maria, "Ferroelectric Al₁₋ₓBₓN thin films
>    integrated on Si," *Appl. Phys. Lett.* **123**, 072901 (2023).
>    doi:10.1063/5.0156606
> 2. I. Mercer, C. Skidmore, S. Calderon, E. Dickey, and J.-P. Maria,
>    "Ferroelectric Al₁₋ₓBₓN sputtered thin films on n-type Si bottom electrodes,"
>    *J. Mater. Sci.* **60**, 19781–19787 (2025). doi:10.1007/s10853-025-11499-w
> 3. G. F. Harrington and J. Santiso, "Back-to-Basics tutorial: X-ray diffraction
>    of thin films," *J. Electroceram.* **47**, 141–163 (2021).
>    doi:10.1007/s10832-021-00263-6
> 4. X.-H. Xu, H.-S. Wu, C.-J. Zhang, and Z.-H. Jin, "Morphological properties of
>    AlN piezoelectric thin films deposited by DC reactive magnetron sputtering,"
>    *Thin Solid Films* **388**, 62–67 (2001). *(add DOI — verify on publisher
>    site)*

On a poster you can drop article titles to save space, but **keep author,
journal, volume, page, year**. If space is tight, a small QR code to a reference
list is cleaner than a cramped block.

### 7.4 No contact info / QR code ✅ FIXED (add)

Add, near the title block or footer: your email, and a QR code. The best QR
target given your "every number carries an error bar" rigor claim is the **public
repo of your Python batch-fit pipelines** (pseudo-Voigt, Parratt XRR, watershed
AFM). ⚠️ Supply the URL. This is a strong differentiator at a competition — it
lets judges verify the analysis.

### 7.5 Title article (optional) ✅ FIXED

Grammatically the title wants an article: *"…with **a** Plasma-Formed Oxynitride
Template."* Minor; include if it doesn't disturb the layout.

---

## 8. Code drop-ins (details)

The three scripts (`poster_style.py`, `check_colorblind.py`, `fig3_recolored_demo.py`)
are ready to run. Key snippets:

### 8.1 Apply the palette + poster type to any figure

```python
from poster_style import POSTER_COLORS as C, apply_poster_style
apply_poster_style(fig_width_in=7.5)   # = width this figure occupies on the poster
```

### 8.2 Add Scherrer error bars to the coherence bars (Fig 4a)

```python
# vals, errs = your fitted L0002 and its propagated uncertainty per run
ax.bar(runs, vals, color=[C["thick"] if t=="60min" else C["thin"] for t in kind],
       edgecolor="black")
ax.errorbar(runs, vals, yerr=errs, fmt="none", ecolor="black",
            elinewidth=1.4, capsize=4)
```

### 8.3 Replace raw filenames on the AFM images (Fig 9)

```python
LABELS = {                       # filename stem -> human label  (⚠️ confirm mapping)
    "22_0624_1um_1.0_00002":        "(a) Run #22 — short oxynitridation",
    "27_0629_Mercer_1um_1.0_00000": "(b) Run #27 — 60-min Mercer recipe",
}
ax.set_title(LABELS.get(stem, stem))
# and label the color bar so the differing z-scales are explicit:
cbar.set_label("height (nm)")
```

### 8.4 Verify colorblind-safety of every final figure

```bash
python check_colorblind.py fig2.png fig3.png fig6.png fig7.png
# inspect each *_cvd.png ; if two series merge, add a marker shape or hatch
```

---

## Quick status tally

| Criterion | ✅ ready to paste | 🔧 code provided | ⚠️ needs your input |
|-----------|:---:|:---:|:---:|
| 1 Theme & cohesion | 1.2 | — | 1.1 (control) |
| 2 Layout | 2.1, 2.2 | — | — |
| 3 Figures & captions | 3.1–3.3, 3.5 | 3.6 | 3.4 (which AFM run) |
| 4 Color | — | 4.2 | — |
| 5 Typography | 5.2, 5.3 | 5.1, 5.4 | — |
| 6 Science | 6.1, 6.3, 6.4 | — | 6.2, 6.5, 6.6 |
| 7 Additional | 7.2, 7.3, 7.5 | — | 7.1 (LDRD), 7.4 (QR) |

The only items that truly *require you* are: (1.1) the untreated-SiO₂ control,
(6.2) interface evidence, (7.1) the LDRD project name/number, (3.4) the AFM run
mapping, and (7.4) the repo URL. Everything else is written or coded above.