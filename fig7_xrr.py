"""
Figure 7: XRR - density (reliable fits) + growth-rate comparison
"""
import numpy as np
import matplotlib.pyplot as plt

from fig_utils import (
    load_all_data, save,
    GREEN, GREEN_D, TEAL, AMBER, INK
)


def main():
    rc, coh, xrr, rms, grn = load_all_data()
    
    ok = xrr[xrr.run.isin([26, 30, 32, 33])].sort_values('run')
    
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 4.0),
                                 gridspec_kw=dict(width_ratios=[1.15, 1.0], wspace=0.45))
    fig.subplots_adjust(left=0.115, right=0.985, top=0.855, bottom=0.175)
    
    x = np.arange(len(ok))
    
    # Density panel
    a1.axhspan(3.255 * 0.95, 3.255, color='#E2EFE6', lw=0)
    a1.axhline(3.255, color=GREEN_D, ls=(0, (4, 3)), lw=2)
    a1.text(len(ok) - 0.4, 3.268, 'bulk AlN 3.26', ha='right', fontsize=15.5, color=GREEN_D)
    a1.errorbar(x, ok.rho_gcm3, yerr=ok.rho_err.astype(float), fmt='o', ms=13, c=GREEN,
                ecolor=INK, capsize=5, lw=2)
    a1.set_xticks(x)
    a1.set_xticklabels([f'#{r}' for r in ok.run], fontsize=17)
    a1.set_ylabel('density (g cm$^{-3}$)', fontsize=20)
    a1.set_ylim(2.55, 3.62)
    a1.set_xlabel('AlN XRR density', fontsize=20)
    # Thickness panel
    t = [('#30', 124.12, 0.06, 123.1), ('#33', 125.89, 0.06, 126.1)]
    x2 = np.arange(len(t))
    a2.bar(x2, [v[1] for v in t], yerr=[v[2] for v in t], width=0.55, color=TEAL,
           error_kw=dict(ecolor=INK, lw=1.6, capsize=4))
    for xi, v in zip(x2, t):
        a2.text(xi, v[1] + 4, f'{v[1]:.0f} nm', ha='center', fontsize=16.5, color=INK)
    a2.set_xticks(x2)
    a2.set_xticklabels([v[0] for v in t], fontsize=17)
    a2.set_ylim(0, 150)
    a2.set_ylabel('thickness (nm)', fontsize=20)
    a2.set_xlabel('10-min growth', fontsize=20)
    a2.legend(loc='lower center', fontsize=15, handletextpad=0.2)
    
    for a in (a1, a2):
        a.tick_params(labelsize=17)
    
    plt.show()
    save(fig, 'fig7_xrr.png')


if __name__ == '__main__':
    main()