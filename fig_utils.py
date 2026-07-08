"""
Shared utilities for ORNL Summer 2026 poster figure generation.
Common imports, color palette, matplotlib settings, and data loading.
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle, FancyBboxPatch
import json
import re
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

U = SCRIPT_DIR / 'data'
OUT = SCRIPT_DIR / 'figures/'
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- palette (CVD-safe)
GREEN   = '#007833'   # ORNL green (PMS 356-like) - keep for branding
GREEN_D = '#00542B'   # dark green - use sparingly
GREEN_L = '#6FB98F'   # light green - use sparingly
TEAL    = '#0072B2'   # CVD-safe blue (was #3E8E9E)
AMBER   = '#E69F00'   # CVD-safe yellow-amber (was #E8A33D)
RED     = '#D55E00'   # CVD-safe orange (was #B3452C)
INK     = '#1E252B'
MUTED   = '#5B6770'
FAINT   = '#C9D2CC'

# ---------------------------------------------------------------- matplotlib settings
def setup_mpl():
    mpl.rcParams.update({
        'font.family': 'DejaVu Sans',
        'font.size': 20,
        'axes.labelsize': 23, 'axes.titlesize': 25, 'axes.titleweight': 'bold',
        'axes.edgecolor': MUTED, 'axes.labelcolor': INK, 'axes.linewidth': 1.6,
        'xtick.labelsize': 19, 'ytick.labelsize': 19,
        'xtick.color': INK, 'ytick.color': INK,
        'legend.fontsize': 18, 'legend.frameon': False,
        'axes.spines.top': False, 'axes.spines.right': False,
        'savefig.dpi': 300, 'figure.dpi': 110,
    })

setup_mpl()

# ---------------------------------------------------------------- helper functions
def save(fig, name):
    stem = Path(name).stem
    for ext in ['png', 'pdf', 'svg']:
        fig.savefig(OUT / f'{stem}.{ext}', 
                    transparent=True, 
                    bbox_inches='tight',
                    dpi=300 if ext == 'png' else None)
    plt.close(fig)
    print(f'saved {stem}.{{png,pdf,svg}}')

def run_of(s):
    m = re.match(r'^(\d+)_', str(s))
    return int(m.group(1)) if m else None

# ---------------------------------------------------------------- load data
def load_all_data():
    rc  = pd.read_csv(U / 'rocking_curve_summary.csv')
    coh = pd.read_csv(U / 'xrd_coherence_summary.csv')
    xrr = pd.read_csv(U / 'XRR_summary.csv')
    rms = pd.read_csv(U / 'AFM_RMS_summary.csv')
    grn = pd.read_csv(U / 'AFM_grain_summary.csv')

    for df, col in [(rc, 'file'), (coh, 'filename'), (xrr, 'file'), (rms, 'file'), (grn, 'file')]:
        df['run'] = df[col].map(run_of)
    
    return rc, coh, xrr, rms, grn

# ---------------------------------------------------------------- condition labels
LBL = {
    15: 'std recipe',
    17: '30 W oxynitride',
    22: 'N$_2$ cool 80 min',
    24: '2.5 mTorr pre-sp.',
    25: 'vac cool 3.5 h',
    26: 'mixed pre-sp.',
    27: '60-min oxy (lit.)',
    28: 'mixed pre-sp. · low P',
    29: '2.5 mTorr · no soak',
    30: '40 W oxynitride',
    32: 'overnight cool',
    33: '50 W oxynitride',
}

THIN = {30, 32, 33}          # 10-min growths, ~125 nm
BEST = 29