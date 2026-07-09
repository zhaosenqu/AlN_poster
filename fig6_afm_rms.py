"""
Figure 6: AFM RMS roughness by sample (simplified for publication)
Uses error bars (mean ± std) instead of individual data points.
"""
import numpy as np
import matplotlib.pyplot as plt

from fig_utils import (
    load_all_data, save,
    GREEN, TEAL, RED, INK, MUTED, FAINT
)

# Font size constants for consistency
LABEL_SIZE = 11
TICK_SIZE = 10
ANNOT_SIZE = 10


def main():
    rc, coh, xrr, rms, grn = load_all_data()
    
    rms['size'] = rms.scan_x_um.astype(float)
    rr = rms[~rms.file.str.contains('masked')].copy()
    
    # Runs with complete AFM datasets (matches original figure)
    order = [15, 22, 24, 25, 26, 27, 28, 30, 33]
    outlier_idx = order.index(27)
    
    # Compute mean and std for each run
    means = []
    stds = []
    for run in order:
        sub = rr[rr.run == run]
        means.append(sub.Sq_RMS_nm.mean())
        stds.append(sub.Sq_RMS_nm.std())
    
    means = np.array(means)
    stds = np.array(stds)
    x = np.arange(len(order))
    
    # Separate indices for normal vs outlier
    normal_mask = np.ones(len(order), dtype=bool)
    normal_mask[outlier_idx] = False
    
    # Create figure - journal double-column width
    fig, ax = plt.subplots(figsize=(7, 4.5))
    
    # Plot normal points with error bars
    ax.errorbar(
        x[normal_mask], means[normal_mask], yerr=stds[normal_mask],
        fmt='s', markersize=10,
        color=TEAL, ecolor=TEAL, elinewidth=1.5, capsize=8, capthick=1.5,
         markeredgewidth=1, zorder=5,
        label='Mean ± std'
    )
    
    # Plot outlier (run #27) in red
    ax.errorbar(
        x[outlier_idx], means[outlier_idx], yerr=stds[outlier_idx],
        fmt='s', markersize=10,
        color=RED, ecolor=RED, elinewidth=1.5, capsize=8, capthick=1.5, markeredgewidth=1, zorder=6
    )
    
    # Reference line
    ax.axhline(1.0, color=FAINT, lw=1.5, ls='--', zorder=1)
    ax.text(
        len(order) - 0.5, 1.08, 'sub-nm target',
        ha='right', fontsize=ANNOT_SIZE, color=MUTED
    )
    
    # Annotation for outlier
    ax.annotate(
        '60-min oxynitridation\n(Mercer et al.): 4–7× rougher',
        xy=(outlier_idx, means[outlier_idx]),
        xytext=(outlier_idx - 1.5, 1.8),
        fontsize=ANNOT_SIZE, color=RED, fontweight='bold',
        ha='center', va='bottom',
        arrowprops=dict(arrowstyle='->', color=RED, lw=1.5)
    )
    
    # Bottom annotation
    ax.text(
        0.02, 0.03,
        '#23 stage grounded control: $S_q$ ≈ 70 nm (off scale)',
        transform=ax.transAxes, fontsize=ANNOT_SIZE, color=MUTED, style='italic'
    )
    
    # Axis configuration
    ax.set_xticks(x)
    ax.set_xticklabels([f'#{r}' for r in order], fontsize=TICK_SIZE)
    ax.set_xlabel('Growth run', fontsize=LABEL_SIZE)
    ax.set_ylabel('RMS roughness $S_q$ (nm)', fontsize=LABEL_SIZE)
    ax.set_ylim(0, 2.7)
    ax.set_xlim(-0.5, len(order) - 0.5)
    ax.tick_params(axis='y', labelsize=TICK_SIZE)
    
    # Legend
    leg = ax.legend(
        loc='upper left',
        fontsize=ANNOT_SIZE,
        frameon=True,
        framealpha=0.95,
        edgecolor=MUTED,
        fancybox=False
    )
    leg.get_frame().set_linewidth(1.2)
    
    # Clean spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(1.2)
    ax.spines['left'].set_linewidth(1.2)
    
    # Tick styling
    ax.tick_params(which='both', direction='in', top=False, right=False)
    
    fig.tight_layout()
    save(fig, 'fig6_afm_rms')
    plt.close(fig)


if __name__ == '__main__':
    main()