"""
Figure 6: Surface feature size (1 µm scans) vs XRD coherence length
"""
import matplotlib
matplotlib.use('TkAgg')  # or 'QtAgg' if you have PyQt installed
import numpy as np
import matplotlib.pyplot as plt

from fig_utils import (
    load_all_data, save,
    GREEN, TEAL, AMBER, INK
)


def main():
    rc, coh, xrr, rms, grn = load_all_data()
    
    g1 = grn[(grn.scan_x_um == 1.0) & (~grn.file.str.contains('masked'))].copy()
    runs6 = [15, 22, 24, 25, 26, 27]
    
    med = [g1[g1.run == r].median_equiv_diameter_nm.mean() for r in runs6]
    sd = []
    for r in runs6:
        subset = g1[g1.run == r]
        if len(subset) > 1:
            sd.append(subset.median_equiv_diameter_nm.std(ddof=0))
        else:
            grain_count = subset.grain_count.mean()
            if grain_count > 0:
                sd.append(subset.std_equiv_diameter_nm.mean() / np.sqrt(grain_count))
            else:
                sd.append(0)
    
    cohmap = dict(zip(coh.run, coh.coherence_length_nm))
    
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    fig.subplots_adjust(left=0.10, right=0.98, top=0.97, bottom=0.16)
    
    x = np.arange(len(runs6))
    ax.bar(x, med, yerr=sd, width=0.62, color=GREEN, lw=1.4,
           error_kw=dict(ecolor=INK, lw=1.6, capsize=4),
           label='AFM surface feature Ø (median, 1 µm scans)')
    
    have = [i for i, r in enumerate(runs6) if r in cohmap and r != 25]
    ax.scatter([x[i] for i in have], [cohmap[runs6[i]] for i in have], marker='D', s=170,
               c=AMBER, ec=INK, lw=1.3, zorder=6, label='XRD coherence length L$_{002}$')
    
    ax.set_xticks(x)
    ax.set_xticklabels([f'#{r}' for r in runs6], fontsize=18)
    ax.set_xlabel('growth run', fontsize=18)
    ax.set_ylabel('length scale (nm)', fontsize=18)
    ax.set_ylim(0, 55)
    ax.legend(loc='upper left', handletextpad=0.35, fontsize=12)
    
    plt.show()

    save(fig, 'fig6_feature_vs_coherence')
    plt.close(fig)


if __name__ == '__main__':
    main()