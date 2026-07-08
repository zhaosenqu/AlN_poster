"""
ORNL Summer 2026 poster — figure generation from uploaded CSV data.
All numbers derived directly from the uploaded files; figures saved at true
physical size (inches) so fonts land at their literal point size on the
40 x 30 in poster.
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle, FancyBboxPatch
import json, re, os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

U = SCRIPT_DIR
OUT = SCRIPT_DIR / 'figures/'
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- palette
GREEN   = '#007833'   # ORNL green (PMS 356-like)
GREEN_D = '#00542B'
GREEN_L = '#6FB98F'
TEAL    = '#3E8E9E'
AMBER   = '#E8A33D'
RED     = '#B3452C'
INK     = '#1E252B'
MUTED   = '#5B6770'
FAINT   = '#C9D2CC'

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

def save(fig, name):
    fig.savefig(OUT / name, transparent=True, bbox_inches=None)
    plt.close(fig)
    print('saved', name)

# ---------------------------------------------------------------- load data
rc  = pd.read_csv(U / 'rocking_curve_summary.csv')
coh = pd.read_csv(U / 'xrd_coherence_summary.csv')
xrr = pd.read_csv(U / 'XRR_summary.csv')
rms = pd.read_csv(U / 'AFM_RMS_summary.csv')
grn = pd.read_csv(U / 'AFM_grain_summary.csv')

def run_of(s):
    m = re.match(r'^(\d+)_', str(s))
    return int(m.group(1)) if m else None

for df, col in [(rc, 'file'), (coh, 'filename'), (xrr, 'file'), (rms, 'file'), (grn, 'file')]:
    df['run'] = df[col].map(run_of)

# short condition labels (from sputtering logs)
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

# ================================================================ FIG 1
# Concept schematic: amorphous SiO2 problem -> plasma oxynitride template
def hexcol(ax, x, y, w, h, tilt, fc, ec):
    """a tilted 'columnar grain' pictogram"""
    t = np.deg2rad(tilt)
    dx = np.sin(t) * h
    pts = np.array([[x, y], [x + w, y], [x + w + dx, y + h], [x + dx, y + h]])
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=ec, lw=1.6))
    # hexagon cap
    cx, cy = x + w / 2 + dx, y + h
    r = w * 0.58
    ang = np.linspace(0, 2 * np.pi, 7) + np.pi / 6
    ax.add_patch(Polygon(np.c_[cx + r * np.cos(ang), cy + 0.28 * r * np.sin(ang)],
                         closed=True, fc=fc, ec=ec, lw=1.6))

fig, ax = plt.subplots(figsize=(8.4, 5.2))
fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
ax.set_xlim(0, 100); ax.set_ylim(0, 62); ax.axis('off')

for x0, ttl in [(2, 'untreated SiO$_2$'), (56, 'plasma-formed SiO$_x$N$_y$ template')]:
    ax.add_patch(Rectangle((x0, 6), 40, 7, fc='#B9BDC1', ec=INK, lw=1.6))          # Si
    ax.text(x0 + 20, 9.5, 'Si', ha='center', va='center', fontsize=19, color=INK)
    ax.add_patch(Rectangle((x0, 13), 40, 9, fc='#CFE3EE', ec=INK, lw=1.6))         # SiO2
    ax.text(x0 + 20, 17.5, 'SiO$_2$ (amorphous)', ha='center', va='center', fontsize=19, color=INK)
    ax.text(x0 + 20, 58.5, ttl, ha='center', va='center', fontsize=21,
            fontweight='bold', color=INK)

# left: misaligned columns
np.random.seed(3)
for i, xg in enumerate(np.linspace(5, 33, 6)):
    hexcol(ax, xg, 22.4, 4.6, 14 + 4 * np.random.rand(), np.random.uniform(-22, 22),
           '#E5E9E6', MUTED)
ax.text(22, 47.5, 'misoriented / amorphous AlN', ha='center', fontsize=18, color=RED)
ax.text(22, 52.5, '✗ no crystallographic template', ha='center', fontsize=18,
        color=RED, fontweight='bold')

# right: oxynitride layer + aligned columns
ax.add_patch(Rectangle((56, 22), 40, 3.2, fc=GREEN_L, ec=GREEN_D, lw=1.8))
ax.text(76, 23.6, 'SiO$_x$N$_y$  (N$_2$/Ar plasma · 40 W · 600 °C · 10 min)',
        ha='center', va='center', fontsize=15.5, color=GREEN_D, fontweight='bold')
for xg in np.linspace(59, 87, 6):
    hexcol(ax, xg, 25.4, 4.6, 17, 0, '#DCEFE3', GREEN_D)
ax.annotate('', xy=(93.5, 46), xytext=(93.5, 27),
            arrowprops=dict(arrowstyle='-|>', lw=2.6, color=GREEN_D))
ax.text(95.0, 36.5, 'c-axis', rotation=90, va='center', fontsize=17, color=GREEN_D)
ax.text(76, 49.5, '(0002)-textured wurtzite AlN', ha='center', fontsize=18, color=GREEN_D)
ax.text(76, 54.3, '✓ oriented nucleation', ha='center', fontsize=18,
        color=GREEN_D, fontweight='bold')

ax.annotate('', xy=(55, 33), xytext=(44.5, 33),
            arrowprops=dict(arrowstyle='-|>', lw=4, color=AMBER))
ax.text(49.7, 37.2, 'in-situ\nplasma', ha='center', fontsize=16, color='#9C6716',
        fontweight='bold')
save(fig, 'fig1_concept.png')

# ================================================================ FIG 2
# Campaign: outcomes + rocking-curve FWHM vs run, and growth-rate jump
fig, (a1, a2) = plt.subplots(2, 1, figsize=(8.4, 7.0), sharex=True,
                             gridspec_kw=dict(height_ratios=[2.1, 1.0], hspace=0.14))
fig.subplots_adjust(left=0.12, right=0.985, top=0.985, bottom=0.105)

a1.axvspan(0.4, 13.5, color='#F6E3DD', alpha=0.75, lw=0)
a1.axvspan(13.5, 34.6, color='#E2EFE6', alpha=0.75, lw=0)
a2.axvspan(0.4, 13.5, color='#F6E3DD', alpha=0.75, lw=0)
a2.axvspan(13.5, 34.6, color='#E2EFE6', alpha=0.75, lw=0)
for a in (a1, a2):
    a.axvline(13.5, color=INK, ls=(0, (5, 3)), lw=1.8)

amorph = [1, 2, 3, 4, 6, 7]                 # characterized: no AlN signal
swept  = [5, 8, 9, 10, 11, 12, 13]          # grown in leak era (uncharacterized/lost)
scrap  = [16, 18, 19, 20, 21, 23, 31]       # scrapped / faulted runs
a1.scatter(amorph, [2.62] * len(amorph), marker='x', s=150, c=RED, lw=3,
           label='no AlN signal', zorder=5)
a1.scatter(swept, [2.62] * len(swept), marker='x', s=150, c='#D89A8A', lw=3, zorder=4)
a1.scatter(scrap, [2.42] * len(scrap), marker='o', s=95, fc='none', ec=MUTED, lw=2.2,
           label='scrapped run', zorder=4)

rcv = rc[rc.run != 27].copy()
thick = rcv[~rcv.run.isin(THIN)]
thin  = rcv[rcv.run.isin(THIN)]
a1.errorbar(thick.run, thick.fwhm_deg, yerr=thick.fwhm_ci95_deg, fmt='o', ms=13,
            color=GREEN, ecolor=GREEN, capsize=4, lw=2,
            label='~0.5–0.8 µm films', zorder=6)
a1.errorbar(thin.run, thin.fwhm_deg, yerr=thin.fwhm_ci95_deg, fmt='s', ms=12,
            color=TEAL, ecolor=TEAL, capsize=4, lw=2,
            label='~125 nm films', zorder=6)
b = rc[rc.run == BEST]
a1.scatter(b.run, b.fwhm_deg, marker='*', s=650, c=AMBER, ec=INK, lw=1.4, zorder=7)
a1.annotate('best: 1.09°', (BEST, float(b.fwhm_deg.iloc[0])), xytext=(29.3, 0.42),
            fontsize=19, fontweight='bold', color='#9C6716', ha='center')
a1.annotate('run 27 (60-min oxy): 4.7° ↑', (24.6, 2.24), fontsize=15.5, color=MUTED,
            ha='center')
a1.text(7.0, 0.28, 'Ar-line air leak\n(trace O$_2$)', ha='center', fontsize=17,
        color=RED, fontweight='bold')
a1.text(24.0, 0.15, 'leak repaired + oxynitride template', ha='center',
        fontsize=17, color=GREEN_D, fontweight='bold')
a1.set_ylabel('AlN 0002 ω-FWHM (°)')
a1.set_ylim(0, 2.85); a1.set_yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5])
a1.legend(loc='upper left', bbox_to_anchor=(0.012, 0.90), handletextpad=0.25,
          borderaxespad=0, labelspacing=0.3, fontsize=16.5)

# growth-rate panel (Al target at 300 W only)
gr_runs  = [4, 6, 7, 24, 25, 27, 30, 33]
gr_rate  = [90/60, 112/60, 75.6/60, 500/60, 680/60, 800/60, 124.12/10, 125.89/10]
gr_col   = [RED if r < 14 else GREEN for r in gr_runs]
a2.bar(gr_runs, gr_rate, width=0.85, color=gr_col, ec='none')
a2.set_ylabel('growth rate\n(nm min$^{-1}$)', fontsize=20)
a2.set_xlabel('growth run #  (chronological, May 21 → Jul 6)')
a2.set_ylim(0, 14.5); a2.set_yticks([0, 5, 10])
a2.annotate('~6× rate recovery after leak repair\n(O$_2$ target poisoning removed)',
            xy=(1.0, 10.7), fontsize=16.5, color=GREEN_D, ha='left', va='center',
            fontweight='bold')
a2.set_xlim(0.4, 34.6)
a2.set_xticks([1, 5, 10, 14, 20, 25, 30, 34])
save(fig, 'fig2_campaign.png')

# ================================================================ FIG 3
# Rocking-curve FWHM by condition (horizontal bars)
fig, ax = plt.subplots(figsize=(8.4, 6.6))
fig.subplots_adjust(left=0.335, right=0.965, top=0.885, bottom=0.115)
d = rc.copy()
d['thin'] = d.run.isin(THIN)
d = pd.concat([d[~d.thin].sort_values('fwhm_deg', ascending=False),
               d[d.thin].sort_values('fwhm_deg', ascending=False)])
d = d.iloc[::-1].reset_index(drop=True)   # thin group on top
ypos = np.arange(len(d), dtype=float)
ypos[d.thin.values] += 0.65               # visual gap between groups

for i, r in d.iterrows():
    y = ypos[i]
    if r.run == 27:
        ax.barh(y, 2.42, color='#D8DDD9', ec=MUTED, lw=1.2, hatch='//', height=0.72)
        ax.text(2.49, y, '→ 4.7 ± 3.2°\n(poor fit)', va='center',
                fontsize=14.5, color=MUTED)
    else:
        c = TEAL if r.thin else (AMBER if r.run == BEST else GREEN)
        ax.barh(y, r.fwhm_deg, xerr=r.fwhm_ci95_deg, color=c, height=0.72,
                error_kw=dict(ecolor=INK, lw=1.6, capsize=4))
        ax.text(r.fwhm_deg + 0.05, y, f'{r.fwhm_deg:.2f}°',
                va='center', fontsize=17,
                color='#9C6716' if r.run == BEST else INK,
                fontweight='bold' if r.run == BEST else 'normal')

ax.set_yticks(ypos)
ax.set_yticklabels([f'#{r.run}  {LBL[r.run]}' for _, r in d.iterrows()], fontsize=16.5)
ax.set_xlabel('AlN 0002 rocking-curve FWHM (°)   —   lower = sharper texture')
ax.set_xlim(0, 3.42)
ax.axvline(1.0876, color=AMBER, ls=(0, (4, 3)), lw=2)
ax.text(3.30, ypos[d.thin.values].mean(), '10-min growth\n(~125 nm)', ha='right',
        va='center', fontsize=16, color=TEAL, fontweight='bold')
ax.text(3.30, 6.6, '60–74 min growth\n(~0.5–0.8 µm)', ha='right', va='center',
        fontsize=16, color=GREEN_D, fontweight='bold')
ax.set_title('Texture is set by chamber conditioning,\nnot oxynitride bias (all 40 W unless noted)', fontsize=22, pad=10)
save(fig, 'fig3_rocking.png')

# ================================================================ FIG 4
# Coherence length + c lattice parameter
cv = coh[coh.run != 25].copy()            # run 25 fit collapsed (21 µm artifact)
cv = cv.sort_values('run')
fig, (a1, a2) = plt.subplots(2, 1, figsize=(8.4, 5.6), sharex=True,
                             gridspec_kw=dict(height_ratios=[1.25, 1.0], hspace=0.16))
fig.subplots_adjust(left=0.155, right=0.975, top=0.975, bottom=0.135)
x = np.arange(len(cv))
cols = [TEAL if r in THIN else GREEN for r in cv.run]
a1.bar(x, cv.coherence_length_nm, color=cols, width=0.72)
for xi, v in zip(x, cv.coherence_length_nm):
    a1.text(xi, v + 0.7, f'{v:.0f}', ha='center', fontsize=16.5, color=INK)
a1.set_ylabel('coherence length\nL$_{002}$ (nm)', fontsize=21)
a1.set_ylim(0, 36)
a1.text(0.02, 0.94, 'out-of-plane crystallite size  (Scherrer / pseudo-Voigt, 0002)',
        transform=a1.transAxes, fontsize=16.5, color=MUTED, va='top')

c0 = 4.9792
a2.axhspan(c0 * 0.999, c0 * 1.001, color='#E2EFE6', lw=0)
a2.axhline(c0, color=GREEN_D, ls=(0, (4, 3)), lw=2)
a2.scatter(x, cv.c_lattice_ang, s=140, c=cols, ec=INK, lw=1.2, zorder=5)
a2.text(len(cv) - 0.35, c0 - 0.0012, 'relaxed c$_0$ = 4.979 Å', ha='right',
        fontsize=16.5, color=GREEN_D)
a2.set_ylabel('c lattice (Å)', fontsize=21)
a2.set_ylim(4.9755, 4.9865)
a2.set_xticks(x)
a2.set_xticklabels([f'#{r}' for r in cv.run], fontsize=18)
a2.set_xlabel('growth run')
a2.text(0.02, 0.10, 'all films within 0.08 % of relaxed c$_0$  →  nearly strain-free',
        transform=a2.transAxes, fontsize=16.5, color=INK)
save(fig, 'fig4_coherence.png')

# ================================================================ FIG 5
# AFM RMS roughness by sample and scan size
rms['size'] = rms.scan_x_um.astype(float)
rr = rms[~rms.file.str.contains('masked')].copy()
order = [15, 22, 24, 25, 26, 27]
fig, ax = plt.subplots(figsize=(8.4, 5.2))
fig.subplots_adjust(left=0.095, right=0.98, top=0.895, bottom=0.14)
ax.plot([], [], color=INK, lw=3, label='sample mean')
mk = {1.0: ('o', GREEN), 2.0: ('s', TEAL), 5.0: ('D', '#8A6FA8')}
for j, run in enumerate(order):
    sub = rr[rr.run == run]
    m = sub.Sq_RMS_nm.mean()
    ax.hlines(m, j - 0.32, j + 0.32, color=INK, lw=3, zorder=6)
    for s, (marker, c) in mk.items():
        v = sub[sub['size'] == s].Sq_RMS_nm
        ax.scatter(np.full(len(v), j) + (s - 2.6) * 0.055, v, marker=marker, s=110,
                   c=c, ec='white', lw=0.8, zorder=5,
                   label=f'{s:.0f} µm scan' if j == 0 else None)
ax.set_xticks(range(len(order)))
ax.set_xticklabels([f'#{r}' for r in order], fontsize=18)
ax.set_xlabel('growth run')
ax.set_ylabel('RMS roughness S$_q$ (nm)')
ax.set_ylim(0, 3.15)
ax.legend(loc='upper left', ncols=1, handletextpad=0.2)
ax.annotate('60-min oxynitridation\n(lit.-style recipe):\n4–7× rougher', xy=(5, 2.62),
            xytext=(3.1, 2.30), fontsize=16.5, color=RED, fontweight='bold',
            arrowprops=dict(arrowstyle='-|>', color=RED, lw=2))
ax.text(0.02, 0.055,
        'grounded-stage control (#23): S$_q$ ≈ 70 nm — 100× rougher (off scale)',
        transform=ax.transAxes, fontsize=16, color=MUTED, style='italic')
ax.axhline(1.0, color=FAINT, lw=1.4, ls=(0, (3, 3)))
ax.text(len(order) - 0.45, 1.05, 'sub-nm target', ha='right', fontsize=15.5, color=MUTED)
ax.set_title('Sub-nanometer surfaces across the process window', pad=12)
save(fig, 'fig5_afm_rms.png')

# ================================================================ FIG 6
# Surface feature size (1 µm scans) vs XRD coherence length
g1 = grn[(grn.scan_x_um == 1.0) & (~grn.file.str.contains('masked'))].copy()
runs6 = [15, 22, 24, 25, 26, 27]
med = [g1[g1.run == r].median_equiv_diameter_nm.mean() for r in runs6]
sd  = [g1[g1.run == r].median_equiv_diameter_nm.std(ddof=0) if (g1.run == r).sum() > 1
       else g1[g1.run == r].std_equiv_diameter_nm.mean() / np.sqrt(g1[g1.run == r].grain_count.mean())
       for r in runs6]
cohmap = dict(zip(coh.run, coh.coherence_length_nm))
fig, ax = plt.subplots(figsize=(8.4, 4.8))
fig.subplots_adjust(left=0.10, right=0.98, top=0.97, bottom=0.16)
x = np.arange(len(runs6))
ax.bar(x, med, yerr=sd, width=0.62, color=GREEN_L, ec=GREEN_D, lw=1.4,
       error_kw=dict(ecolor=INK, lw=1.6, capsize=4),
       label='AFM surface feature Ø (median, 1 µm scans)')
have = [i for i, r in enumerate(runs6) if r in cohmap and r != 25]
ax.scatter([x[i] for i in have], [cohmap[runs6[i]] for i in have], marker='D', s=170,
           c=AMBER, ec=INK, lw=1.3, zorder=6, label='XRD coherence length L$_{002}$')
ax.set_xticks(x); ax.set_xticklabels([f'#{r}' for r in runs6], fontsize=18)
ax.set_xlabel('growth run')
ax.set_ylabel('length scale (nm)')
ax.set_ylim(0, 50)
ax.legend(loc='upper left', handletextpad=0.35)
ax.annotate('lateral ≈ vertical length scale\n→ columnar grains', xy=(2.0, 33.5),
            fontsize=17.5, color=GREEN_D, fontweight='bold')
save(fig, 'fig6_grains.png')

# ================================================================ FIG 7
# XRR: density (reliable fits) + growth-rate comparison
ok = xrr[xrr.run.isin([26, 30, 32, 33])].sort_values('run')
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 4.0),
                             gridspec_kw=dict(width_ratios=[1.15, 1.0], wspace=0.45))
fig.subplots_adjust(left=0.115, right=0.985, top=0.855, bottom=0.175)
x = np.arange(len(ok))
a1.axhspan(3.255 * 0.95, 3.255, color='#E2EFE6', lw=0)
a1.axhline(3.255, color=GREEN_D, ls=(0, (4, 3)), lw=2)
a1.text(len(ok) - 0.4, 3.268, 'bulk AlN 3.26', ha='right', fontsize=15.5, color=GREEN_D)
a1.errorbar(x, ok.rho_gcm3, yerr=ok.rho_err.astype(float), fmt='o', ms=13, c=GREEN,
            ecolor=INK, capsize=5, lw=2)
a1.set_xticks(x); a1.set_xticklabels([f'#{r}' for r in ok.run], fontsize=17)
a1.set_ylabel('density (g cm$^{-3}$)', fontsize=20)
a1.set_ylim(2.55, 3.62)
a1.set_title('90–102 % bulk density', fontsize=20, pad=8)

t = [('#30', 124.12, 0.06, 123.1), ('#33', 125.89, 0.06, 126.1)]
x2 = np.arange(len(t))
a2.bar(x2, [v[1] for v in t], yerr=[v[2] for v in t], width=0.55, color=TEAL,
       error_kw=dict(ecolor=INK, lw=1.6, capsize=4))
a2.scatter(x2, [v[3] for v in t], marker='_', s=900, c=AMBER, lw=4, zorder=6,
           label='FFT cross-check')
for xi, v in zip(x2, t):
    a2.text(xi, v[1] + 4, f'{v[1]:.0f} nm', ha='center', fontsize=16.5, color=INK)
a2.set_xticks(x2); a2.set_xticklabels([v[0] for v in t], fontsize=17)
a2.set_ylim(0, 150)
a2.set_ylabel('thickness (nm)', fontsize=20)
a2.set_title('10-min films → 12.5 nm min$^{-1}$', fontsize=20, pad=8)
a2.legend(loc='lower center', fontsize=15, handletextpad=0.2)
for a in (a1, a2):
    a.tick_params(labelsize=17)
save(fig, 'fig7_xrr.png')

# ================================================================ derived stats
def jd(x): return float(np.round(x, 4))
stats = {
    'best_rc': jd(rc.loc[rc.run == BEST, 'fwhm_deg'].iloc[0]),
    'first_rc': jd(rc.loc[rc.run == 15, 'fwhm_deg'].iloc[0]),
    'improvement_pct': jd(100 * (1 - rc.loc[rc.run == BEST, 'fwhm_deg'].iloc[0] /
                                 rc.loc[rc.run == 15, 'fwhm_deg'].iloc[0])),
    'coh_range': [jd(coh[coh.run != 25].coherence_length_nm.min()),
                  jd(coh[coh.run != 25].coherence_length_nm.max())],
    'strain_max_pct': jd(coh[coh.run != 25].strain_percent.max()),
    'two_theta_range': [jd(coh[coh.run != 25].center_2theta_deg.min()),
                        jd(coh[coh.run != 25].center_2theta_deg.max())],
    'rms_1um_range_non_mercer': [
        jd(rms[(rms.scan_x_um == 1.0) & (rms.run != 27)].Sq_RMS_nm.min()),
        jd(rms[(rms.scan_x_um == 1.0) & (rms.run != 27)].Sq_RMS_nm.max())],
    'feature_d_1um_range': [jd(min(med[:-1])), jd(max(med[:-1]))],
    'density_range_ok': [jd(ok.rho_gcm3.min()), jd(ok.rho_gcm3.max())],
    'rate_leak_era_300W': [jd(90/60), jd(112/60)],
    'rate_fixed_300W': [jd(500/60), jd(125.89/10)],
}
print(json.dumps(stats, indent=1))
