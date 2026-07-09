"""
Overlay of AlN 0002 rocking curves for runs 27, 26, and 29.

Place this script in the same directory as fig_utils.py and the three .xy files.
Outputs transparent PNG/PDF/SVG files to ./figures via fig_utils.save().
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from fig_utils import save, GREEN, AMBER, MUTED, INK


CURVES = [
    ("data/rc/27_0629_Mercer_RC.xy", "#27: soak, 60 min oxy", MUTED, "-"),
    ("data/rc/26_0629_mixed_ps_RC.xy", "#26: soak, 10 min oxy", GREEN, "-"),
    ("data/rc/29_0630_no_350_RC.xy", "#29: no soak, 10 min oxy", AMBER, "-"),
]


def load_xy(path: Path) -> tuple[np.ndarray, np.ndarray]:
    data = np.loadtxt(path)
    return data[:, 0], data[:, 1]


def normalize_intensity(y: np.ndarray) -> np.ndarray:
    n_edge = max(3, y.size // 20)
    background = np.median(np.r_[y[:n_edge], y[-n_edge:]])
    y_corr = np.clip(y - background, 0, None)
    return y_corr / y_corr.max()


def main() -> None:
    base = Path(__file__).resolve().parent

    fig, ax = plt.subplots(figsize=(12, 5))
    fig.subplots_adjust(left=0.13, right=0.98, top=0.96, bottom=0.16)

    for filename, label, color, linestyle in CURVES:
        omega, intensity = load_xy(base / filename)
        ax.plot(
            omega,
            normalize_intensity(intensity),
            color=color,
            lw=2.8,
            ls=linestyle,
            solid_capstyle="round",
            label=label,
        )

    ax.set_xlabel(r"Rocking angle, $\omega$ (°)")
    ax.set_ylabel("Normalized intensity (a.u.)")
    ax.set_xlim(15, 20.0)
    ax.set_ylim(-0.03, 1.08)
    ax.set_xticks(np.arange(15, 21, 1))
    ax.set_yticks(np.linspace(0, 1, 6))
    ax.grid(axis="y", color="#D8DED9", lw=0.8, alpha=0.25)

    ax.legend(
        loc="upper left",           # Position: 'upper left', 'lower right', etc.
        frameon=True,                # Show frame around legend
        framealpha=0.95,             # Frame transparency (1 = opaque)
        edgecolor="#CCCCCC",       # Frame border color
        facecolor="white",           # Background color
        borderpad=0.8,               # Padding inside frame
        labelspacing=0.6,            # Vertical space between entries
        handlelength=2.0,            # Length of the line samples
        handleheight=1.0,            # Height of the line samples
        prop={'size': 16}  # Bundles size and bold together safely
    )

    plt.show()
    save(fig, "fig5_rc_overlay")


if __name__ == "__main__":
    main()