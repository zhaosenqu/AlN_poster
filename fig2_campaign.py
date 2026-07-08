"""
Figure 2: Campaign outcomes - rocking-curve FWHM vs run, and growth-rate jump
"""
import numpy as np
import matplotlib.pyplot as plt

from fig_utils import (
    load_all_data, save, THIN, BEST,
    GREEN, GREEN_D, TEAL, AMBER, RED, INK, MUTED
)


def main():
    rc, coh, xrr, rms, grn = load_all_data()
    
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8.4, 7.2), sharex=True,
                                 gridspec_kw=dict(height_ratios=[2.1, 1.0], hspace=0.12))
    fig.subplots_adjust(left=0.14, right=0.97, top=0.98, bottom=0.105)

    # Background shading
    a1.axvspan(0.4, 13.5, color='#F6E3DD', alpha=0.75, lw=0)
    a1.axvspan(13.5, 34.6, color='#E2EFE6', alpha=0.75, lw=0)
    a2.axvspan(0.4, 13.5, color='#F6E3DD', alpha=0.75, lw=0)
    a2.axvspan(13.5, 34.6, color='#E2EFE6', alpha=0.75, lw=0)
    for a in (a1, a2):
        a.axvline(13.5, color=INK, ls=(0, (5, 3)), lw=1.8)
    
    # Panel labels - (a) moved higher
    a1.text(0.02, 0.99, '(a)', transform=a1.transAxes, fontsize=22, 
            fontweight='bold', va='top')
    a2.text(0.02, 0.92, '(b)', transform=a2.transAxes, fontsize=22, 
            fontweight='bold', va='top')

    # Marker categories - X markers lowered to 2.5°
    amorph = [1, 2, 3, 4, 6, 7]
    swept  = [5, 8, 9, 10, 11, 12, 13]
    scrap  = [16, 18, 19, 20, 21, 23, 31]
    
    a1.scatter(amorph, [2.5] * len(amorph), marker='x', s=150, c=RED, lw=3,
               label='no AlN signal', zorder=5)
    a1.scatter(swept, [2.5] * len(swept), marker='x', s=150, c='#D89A8A', lw=3, 
               zorder=4, label='uncharacterized')
    a1.scatter(scrap, [2.5] * len(scrap), marker='o', s=95, fc='none', ec=MUTED, lw=2.2,
               label='scrapped run', zorder=4)  # lowered to 2.30 to avoid overlap

    # Rocking curve data
    rcv = rc[rc.run != 27].copy()
    thick = rcv[~rcv.run.isin(THIN)]
    thin  = rcv[rcv.run.isin(THIN)]
    
    a1.errorbar(thick.run, thick.fwhm_deg, yerr=thick.fwhm_ci95_deg, fmt='o', ms=13,
                color=GREEN, ecolor=GREEN, capsize=4, lw=2,
                label='~600 µm films', zorder=6)
    a1.errorbar(thin.run, thin.fwhm_deg, yerr=thin.fwhm_ci95_deg, fmt='s', ms=12,
                color=TEAL, ecolor=TEAL, capsize=4, lw=2,
                label='~125 nm films', zorder=6)
    
    # Best result highlight with arrow
    b = rc[rc.run == BEST]
    a1.scatter(b.run, b.fwhm_deg, marker='*', s=650, c=AMBER, ec=INK, lw=1.4, zorder=7)
    a1.annotate('best:\n1.09°', xy=(BEST, float(b.fwhm_deg.iloc[0])), 
                xytext=(32.5, 0.55),
                fontsize=18, fontweight='bold', color='#9C6716', ha='center',
                arrowprops=dict(arrowstyle='->', color='#9C6716', lw=1.5))
    
    # Region annotations - positioned in clear space
    a1.text(7.0, 0.20, 'Ar-line air leak\n(trace O$_2$)', ha='center', fontsize=16,
            color=RED, fontweight='bold')
    a1.text(24.0, 0.20, 'leak repaired +\noxynitride template', ha='center',
            fontsize=15, color=GREEN_D, fontweight='bold')
    
    a1.set_ylabel('AlN 0002 ω-FWHM (°)')
    a1.set_ylim(0, 2.85)
    a1.set_yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5])
    
    # Legend positioned
    a1.legend(loc='upper left', bbox_to_anchor=(0.02, 0.7), handletextpad=0.25,
          borderaxespad=0, labelspacing=0.25, fontsize=13, ncol=1)

    # Growth-rate panel
    gr_runs  = [4, 6, 7, 24, 25, 27, 30, 33]
    gr_rate  = [90/60, 112/60, 75.6/60, 500/60, 680/60, 800/60, 124.12/10, 125.89/10]
    gr_col   = [RED if r < 14 else GREEN for r in gr_runs]
    
    a2.bar(gr_runs, gr_rate, width=0.85, color=gr_col, ec='none')
    a2.set_ylabel('growth rate\n(nm min$^{-1}$)', fontsize=14)
    a2.set_xlabel('growth run #  (chronological, May 21 → Jul 6)')
    a2.set_ylim(0, 15)
    a2.set_yticks([0, 5, 10, 15])
    a2.annotate('~6x growth rate',
                xy=(24, 6), xytext=(14, 14),
                fontsize=14, color=GREEN_D, ha='left', va='center')
    
    a2.set_xlim(0.4, 34.6)
    a2.set_xticks([1, 5, 10, 14, 20, 25, 30, 34])
    
    plt.show()
    save(fig, 'fig2_campaign.png')

if __name__ == '__main__':
    main()