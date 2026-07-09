#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


HERE = Path(__file__).resolve().parent
MASTER_TABLE = HERE / "data/master_table.csv"

OUT_PNG = HERE / "figures/fig3_rocking.png"
OUT_PDF = HERE / "figures/fig3_rocking.pdf"
OUT_SVG = HERE / "figures/fig3_rocking.svg"  # Add this line
OUT_CAPTION = HERE / "figures/fig3_rocking_caption.md"

RUN_ORDER_60_MIN = [27, 26, 15, 17, 22, 25, 24, 28, 29]
RUN_ORDER_10_MIN = [30, 32, 33]

LABELS = {
    15: "Std. recipe",
    17: "30 W oxynitride",
    22: "N$_2$ cool, 80 min",
    24: "2.5 mTorr pre-sputter",
    25: "Vacuum cool, 3.5 h",
    26: "Mixed pre-sputter",
    27: "60-min oxynitride",
    28: "Mixed pre-sputter, low $P$",
    29: "2.5 mTorr, no soak",
    30: "40 W oxynitride",
    32: "Overnight cool",
    33: "50 W oxynitride",
}

# Values visible in the prior draft but absent from the supplied master table.
# Their error bars are intentionally left blank until the measured fit
# uncertainty is added to master_table.csv.
FALLBACK_VALUES = {
    30: {"rc_fwhm_deg": 2.10, "rc_fwhm_err": np.nan, "rc_valid": True},
    32: {"rc_fwhm_deg": 1.96, "rc_fwhm_err": np.nan, "rc_valid": True},
    33: {"rc_fwhm_deg": 1.93, "rc_fwhm_err": np.nan, "rc_valid": True},
}

INVALID_RUN = 27
INVALID_DISPLAY_VALUE = 2.45
BEST_RUN = 29

from fig_utils import (
    load_all_data, save,
    GREEN, FAINT, MUTED, RED, TEAL, AMBER, INK
)

COLORS = {
    "60min": TEAL,        # CVD-safe blue for 60-min growth
    "10min": GREEN,       # ORNL green for 10-min growth
    "best": AMBER,        # CVD-safe amber for best result
    "invalid": FAINT,     # Light gray for invalid/excluded
    "edge": MUTED,        # Medium gray for edges
    "text": INK,          # Near black for text
    "muted": MUTED,       # Medium gray for annotations
    "grid": FAINT,        # Light gray for gridlines
    "best_text": RED,     # CVD-safe orange for best result text
}



def load_data() -> pd.DataFrame:
    if not MASTER_TABLE.exists():
        raise FileNotFoundError(f"Could not find {MASTER_TABLE}")

    table = pd.read_csv(MASTER_TABLE).copy()
    table["run"] = table["run"].astype(int)

    rows = []
    for run in RUN_ORDER_60_MIN + RUN_ORDER_10_MIN:
        match = table.loc[table["run"] == run].copy()
        if match.empty:
            match = pd.DataFrame({"run": [run]})
        row = match.iloc[0].to_dict()

        if run in FALLBACK_VALUES:
            for key, value in FALLBACK_VALUES[run].items():
                if key not in row or pd.isna(row.get(key)):
                    row[key] = value

        row["condition"] = LABELS.get(run, str(row.get("notes", f"Run {run}")))
        row["growth_group"] = (
            "10 min growth (~125 nm)" if run in RUN_ORDER_10_MIN
            else "60 min growth (~600 nm)"
        )
        rows.append(row)

    return pd.DataFrame(rows)


def make_figure(data: pd.DataFrame) -> plt.Figure:
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 18,
        "axes.labelsize": 12.0,
        "xtick.labelsize": 12.0,
        "ytick.labelsize": 12.0,
        "legend.fontsize": 12,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.linewidth": 0.9,
    })

    y = np.arange(len(data), dtype=float)
    is_thin = data["growth_group"].str.startswith("10 min").to_numpy()
    y[is_thin] += 0.62

    fig, ax = plt.subplots(figsize=(7.1, 5.15), constrained_layout=False)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    fig.subplots_adjust(left=0.335, right=0.985, bottom=0.13, top=0.91)

    for idx, row in data.iterrows():
        run = int(row["run"])
        yi = y[idx]
        fwhm = float(row["rc_fwhm_deg"]) if pd.notna(row.get("rc_fwhm_deg")) else np.nan
        err = float(row["rc_fwhm_err"]) if pd.notna(row.get("rc_fwhm_err")) else np.nan

        if run == INVALID_RUN:
            ax.barh(
                yi, INVALID_DISPLAY_VALUE,
                height=0.62,
                color=COLORS["invalid"],
                edgecolor=COLORS["edge"],
                linewidth=0.9,
                hatch="///",
                zorder=2,
            )
            label = f"poor fit: {fwhm:.1f} ± {err:.1f}°" if np.isfinite(fwhm) and np.isfinite(err) else "poor fit"
            ax.annotate(
                label,
                xy=(INVALID_DISPLAY_VALUE, yi),
                xytext=(2.70, yi),
                va="center",
                ha="left",
                fontsize=8.4,
                color=COLORS["muted"],
                arrowprops=dict(arrowstyle="->", lw=0.9, color=COLORS["muted"], shrinkA=0, shrinkB=4),
            )
            continue

        color = COLORS["10min"] if row["growth_group"].startswith("10 min") else COLORS["60min"]
        if run == BEST_RUN:
            color = COLORS["best"]

        xerr = None if not np.isfinite(err) else [[err], [err]]
        ax.barh(
            yi, fwhm,
            xerr=xerr,
            height=0.62,
            color=color,
            edgecolor="none",
            error_kw=dict(ecolor=COLORS["text"], elinewidth=0.95, capsize=2.4, capthick=0.95),
            zorder=3,
        )

        label_color = "#8A5A00" if run == BEST_RUN else COLORS["text"]
        ax.text(
            fwhm + (err if np.isfinite(err) else 0) + 0.07,
            yi,
            f"{fwhm:.2f}°",
            va="center",
            ha="left",
            fontsize=12.0,
            fontweight="bold" if run == BEST_RUN else "normal",
            color=label_color,
        )

    ax.set_yticks(y)
    ax.set_yticklabels([f"#{int(r.run)}  {r.condition}" for _, r in data.iterrows()])
    ax.invert_yaxis()

    ax.set_xlim(0, 3.35)
    ax.set_xlabel("AlN(0002) rocking-curve FWHM, $\\Delta\\omega$ (°)")

    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(0.5))
    ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(0.25))
    ax.grid(axis="x", which="major", color=COLORS["grid"], lw=0.75, alpha=0.9, zorder=0)
    ax.grid(axis="x", which="minor", color=COLORS["grid"], lw=0.35, alpha=0.55, zorder=0)

    # Best condition reference line; the highlighted bar and legend carry the label.
    best_value = float(data.loc[data["run"] == BEST_RUN, "rc_fwhm_deg"].iloc[0])
    ax.axvline(best_value, color=COLORS["best"], lw=1.05, ls=(0, (4, 3)), zorder=1)

    # Separate growth-duration groups without putting text on top of the labels.
    sep = (y[~is_thin].max() + y[is_thin].min()) / 2
    ax.axhline(sep, color=COLORS["grid"], lw=0.9, zorder=1)

    # A compact color key replaces the overlapping group text from the draft.
    handles = [
        Patch(facecolor=COLORS["60min"], label="60 min growth (~600 nm)"),
        Patch(facecolor=COLORS["10min"], label="10 min growth (~125 nm)"),
        Patch(facecolor=COLORS["best"], label="best measured"),
        Patch(facecolor=COLORS["invalid"], edgecolor=COLORS["edge"], hatch="///", label="poor fit / excluded"),
    ]
    ax.legend(
        handles=handles,
        loc="lower left",
        bbox_to_anchor=(0.0, 1.008),
        ncol=2,
        frameon=False,
        handlelength=1.2,
        columnspacing=1.25,
        borderaxespad=0,
    )

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(COLORS["edge"])
    ax.spines["bottom"].set_color(COLORS["edge"])
    ax.tick_params(axis="both", colors=COLORS["text"], length=3.5)
    ax.tick_params(axis="x", which="minor", length=2.1)

    return fig


def write_caption(data: pd.DataFrame) -> None:
    best = data.loc[data["run"] == BEST_RUN].iloc[0]
    caption = (
        f"**Figure 3. Rocking-curve width identifies process windows that sharpen AlN c-axis texture.** "
        f"AlN(0002) rocking-curve full width at half maximum (FWHM, Δω) for wurtzite AlN films "
        f"grown on oxynitride-treated SiO₂ under the indicated chamber-conditioning and plasma recipes. "
        f"Bars report fitted FWHM values; horizontal error bars denote fit uncertainty where available. "
        f"Lower FWHM corresponds to sharper out-of-plane c-axis texture. In the 60-min growth series, "
        f"lower-pressure pre-sputtering without a 350 °C soak gave the narrowest measured rocking curve "
        f"(run #{BEST_RUN}, Δω = {float(best['rc_fwhm_deg']):.2f}°). The hatched run #{INVALID_RUN} entry "
        f"is retained for transparency but excluded from trend interpretation because the rocking-curve fit "
        f"was unreliable."
    )
    OUT_CAPTION.write_text(caption + "\n", encoding="utf-8")


def main() -> None:
    data = load_data()
    fig = make_figure(data)
    fig.savefig(OUT_PNG, dpi=600, bbox_inches="tight", transparent=True)
    fig.savefig(OUT_PDF, bbox_inches="tight", transparent=True)
    fig.savefig(OUT_SVG, bbox_inches="tight", transparent=True)  # Add this line
    write_caption(data)
    plt.show()
    plt.close(fig)
    print(f"Wrote: {OUT_PNG}")
    print(f"Wrote: {OUT_PDF}")
    print(f"Wrote: {OUT_SVG}")  # Add this line
    print(f"Wrote: {OUT_CAPTION}")


if __name__ == "__main__":
    main()
