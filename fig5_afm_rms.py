"""
Figure 5: AFM RMS roughness by sample and scan size
"""
import numpy as np
import matplotlib.pyplot as plt

from fig_utils import (
    load_all_data, save,
    GREEN, TEAL, RED, INK, MUTED, FAINT
)


def main():
    rc, coh, xrr, rms, grn = load_all_data()
    
    rms['size'] = rms.scan_x_um.astype(float)
    rr = rms[~rms.file.str.contains('masked')].copy()
    order = [15, 22, 24, 25, 26, 27]
    
    fig, ax = plt.subplots(figsize=(8.4, 5.6))  # slightly taller
    fig.subplots_adjust(left=0.10, right=0.98, top=0.90, bottom=0.13)
    
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
                       label=f'{int(s)} µm scan' if j == 0 else None)
    
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([f'#{r}' for r in order], fontsize=18)
    ax.set_xlabel('growth run')
    ax.set_ylabel('RMS roughness $S_q$ (nm)')  # proper LaTeX formatting
    ax.set_ylim(0, 3.4)  # expanded to fit annotation and data
    
    # Legend in upper left, away from #27 data
    ax.legend(loc='upper left', ncols=1, framealpha=0.95, 
              handletextpad=0.3, fontsize=14)
    
    # Annotation repositioned to avoid overlap with data points
    ax.annotate(
        '60-min oxynitridation\n(recipe from Mercer et al.):\n4-7x rougher',
        xy=(5, 2.75),  # arrow points to approximate data location
        xytext=(4.5, 1.85),  # text moved left
        fontsize=10, color=RED, fontweight = 'bold',
        ha='center', va='bottom',
        arrowprops=dict(arrowstyle='-|>', color=RED, lw=1,
                        connectionstyle='arc3,rad=1')  # curved arrow
    )
    
    # Bottom annotation
    ax.text(0.02, 0.045,
            'grounded-stage control (#23): $S_q$ ≈ 70 nm — 100x rougher (off scale)',
            transform=ax.transAxes, fontsize=14, color=MUTED, style='italic')
    
    # Reference line and label
    ax.axhline(1.0, color=FAINT, lw=1.4, ls=(0, (3, 3)), zorder=1)
    ax.text(4.55, 1.06, 'sub-nm target', ha='right', fontsize=14, color=MUTED)
    
    ax.set_title('Sub-nanometer surfaces across the process window', 
                 fontsize=18, pad=12)
    
    # Minor styling for publication
    ax.tick_params(which='both', direction='in', top=True, right=True)
    plt.show()
    fig.savefig('figures/fig5_afm_rms.png', dpi=300, transparent=True, bbox_inches='tight')


if __name__ == '__main__':
    main()