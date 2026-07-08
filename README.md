# ORNL RSI Summer 2026 Poster Figures

**Analysis and visualization code for (0002)-textured wurtzite AlN thin film growth on plasma-modified SiO₂ substrates.**

[![Author](https://img.shields.io/badge/Author-Zhaosen%20Qu-blue)](mailto:zqu7@jh.edu)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--0894--4343-green)](https://orcid.org/0009-0001-0894-4343)
[![Website Badge](https://img.shields.io/badge/Website-zhaosenqu.github.io-blue?style=flat-square&logo=google-chrome)](https://zhaosenqu.github.io/)

---

## Project Overview

This repository contains Python scripts used to generate publication-quality figures for the Oak Ridge National Laboratory (ORNL) Research Science Internship (RSI) Summer 2026 poster presentation.

The research investigates the growth of highly c-axis oriented aluminum nitride (AlN) thin films using reactive magnetron sputtering on silicon dioxide substrates. The key innovation is the use of nitrogen plasma treatment to create an oxynitride (SiOₓNᵧ) templating layer that promotes preferential (0002) texture in the deposited AlN films.

### Key Findings

- **Best result:** Run #29 achieved a rocking curve FWHM of 1.09° (lowest measured)
- **Process improvement:** ~6× increase in growth rate after system optimization
- **Surface quality:** Sub-nanometer RMS roughness (Sᵩ < 1 nm) achieved across process window
- **Film properties:** Nearly strain-free films within 0.08% of relaxed c-lattice parameter (c₀ = 4.980 Å)

---

## Repository Structure

```
.
├── fig_utils.py          # Shared utilities, color palette, data loading
├── fig1_concept.py       # Conceptual schematic of templating mechanism
├── fig2_campaign.py      # Campaign outcomes: FWHM vs run, growth rate
├── fig3_rocking.py       # Rocking curve FWHM bar chart by condition
├── fig4_coherence.py     # XRD coherence length & c-lattice parameter
├── fig5_afm_rms.py       # AFM RMS surface roughness analysis
├── fig6_grains.py        # Surface feature size vs XRD coherence length
├── fig7_xrr.py           # X-ray reflectivity: density & thickness
├── data/                 # Input CSV data files
│   ├── rocking_curve_summary.csv
│   ├── xrd_coherence_summary.csv
│   ├── XRR_summary.csv
│   ├── AFM_RMS_summary.csv
│   ├── AFM_grain_summary.csv
│   └── master_table.csv
└── figures/              # Output directory (auto-created)
```

---

## Figure Descriptions

| Figure | Script | Description |
|--------|--------|-------------|
| **Fig. 1** | `fig1_concept.py` | Schematic comparing untreated SiO₂ (mixed texture) vs. plasma-modified SiOₓNᵧ ((0002)-textured AlN) |
| **Fig. 2** | `fig2_campaign.py` | Campaign timeline showing rocking curve FWHM evolution and growth rate improvements |
| **Fig. 3** | `fig3_rocking.py` | Horizontal bar chart of rocking curve FWHM by growth condition (60-min and 10-min series) |
| **Fig. 4** | `fig4_coherence.py` | (a) Out-of-plane coherence length via Scherrer analysis, (b) c-lattice parameter comparison |
| **Fig. 5** | `fig5_afm_rms.py` | AFM RMS roughness (Sᵩ) across multiple scan sizes (1, 2, 5 µm) |
| **Fig. 6** | `fig6_grains.py` | AFM surface feature diameter vs. XRD coherence length correlation |
| **Fig. 7** | `fig7_xrr.py` | XRR-derived film density and thickness for 10-min growth series |

---

## Installation

### Requirements

- Python 3.8+
- NumPy
- Pandas
- Matplotlib

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd ornl-rsi-poster-2026

# Install dependencies
pip install numpy pandas matplotlib

# (Optional) For interactive plotting backends
pip install PyQt5  # or use TkAgg
```

---

## Usage

### Generate All Figures

```bash
# Run each figure script individually
python fig1_concept.py
python fig2_campaign.py
python fig3_rocking.py
python fig4_coherence.py
python fig5_afm_rms.py
python fig6_grains.py
python fig7_xrr.py
```

### Output Formats

Figures are automatically saved to the `figures/` directory in multiple formats:

- **PNG** (300–600 DPI, transparent background)
- **PDF** (vector, publication-ready)
- **SVG** (vector, editable)

---

## Data Files

| File | Contents |
|------|----------|
| `rocking_curve_summary.csv` | AlN (0002) ω-scan FWHM values and uncertainties |
| `xrd_coherence_summary.csv` | Scherrer coherence length and c-lattice parameters |
| `XRR_summary.csv` | X-ray reflectivity derived density and thickness |
| `AFM_RMS_summary.csv` | Surface roughness (Sᵩ) from AFM scans |
| `AFM_grain_summary.csv` | Grain/feature size statistics from AFM |
| `master_table.csv` | Combined process parameters and results |

---

## Color Palette

The figures use a **CVD-safe (colorblind-friendly)** palette based on ORNL branding:

| Color | Hex | Usage |
|-------|-----|-------|
| Green | `#007833` | Primary data, ORNL branding |
| Dark Green | `#00542B` | Reference lines, emphasis |
| Teal | `#0072B2` | Secondary data (thin films) |
| Amber | `#E69F00` | Highlights, best results |
| Red | `#D55E00` | Problem indicators, early runs |
| Ink | `#1E252B` | Text, axes |
| Muted | `#5B6770` | Secondary text, annotations |
| Faint | `#C9D2CC` | Reference lines, backgrounds |

---

## Growth Conditions Reference

| Run | Condition | Notes |
|-----|-----------|-------|
| 15 | Standard recipe | Baseline |
| 17 | 30 W oxynitride | — |
| 22 | N₂ cool, 80 min | — |
| 24 | 2.5 mTorr pre-sputter | — |
| 25 | Vacuum cool, 3.5 h | — |
| 26 | Mixed pre-sputter | — |
| 27 | 60-min oxynitride (lit.) | Per Mercer et al. |
| 28 | Mixed pre-sputter, low P | — |
| **29** | **2.5 mTorr, no soak** | **Best result (FWHM = 1.09°)** |
| 30 | 40 W oxynitride | 10-min growth (~125 nm) |
| 32 | Overnight cool | 10-min growth (~125 nm) |
| 33 | 50 W oxynitride | 10-min growth (~125 nm) |

---

## Author

**Zhaosen Qu**  
[zqu7@jh.edu](mailto:zqu7@jh.edu)  
ORCID: [0009-0001-0894-4343](https://orcid.org/0009-0001-0894-4343)

---

## Acknowledgments

This project was developed as part of the Oak Ridge National Laboratory Research Science Internship (RSI) program, Summer 2026.
