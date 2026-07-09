"""
Figure 4: Coherence length + c lattice parameter
"""
import numpy as np
import matplotlib.pyplot as plt

from fig_utils import (
    load_all_data, save, THIN,
    GREEN, GREEN_D, TEAL, INK, MUTED
)


def main():
    rc, coh, xrr, rms, grn = load_all_data()
    
    cv = coh[coh.run != 25].copy()            # run 25 fit collapsed (21 µm artifact)
    cv = cv.sort_values('run')
    
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8.4, 5.6), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1.25, 1.0], hspace=0.16))
    fig.subplots_adjust(left=0.155, right=0.975, top=0.975, bottom=0.135)
    
    x = np.arange(len(cv))
    cols = [TEAL if r in THIN else GREEN for r in cv.run]
    
    # --- Error propagation from fit uncertainties ---
    # Scherrer equation: L = K*λ / (β*cos(θ))
    # Relative uncertainty in L comes from uncertainty in FWHM (β)
    # δL/L ≈ δβ/β (dominant term, since λ and K are constants)
    # sigma_uncertainty_deg is the uncertainty in the Gaussian width from the fit
    
    # Propagate FWHM uncertainty to coherence length
    # Using sigma_uncertainty as proxy for FWHM uncertainty
    fwhm_rel_err = cv.sigma_uncertainty_deg / cv.fwhm_gauss_deg
    coherence_err = cv.coherence_length_nm * fwhm_rel_err
    # Cap at reasonable values (some fits may have very small uncertainties)
    coherence_err = coherence_err.clip(lower=0.5, upper=cv.coherence_length_nm * 0.15)
    
    # c-lattice parameter uncertainty from center_2theta uncertainty
    # Bragg's law: c = λ / (2*sin(θ))  for (0002) reflection
    # δc/c = δθ * cot(θ) ≈ center_uncertainty_deg * (π/180) * cot(θ)
    theta_rad = np.deg2rad(cv.center_2theta_deg / 2)  # θ from 2θ
    c_lattice_err = cv.c_lattice_ang * cv.center_uncertainty_deg * (np.pi / 180) / np.tan(theta_rad)
    # Set minimum uncertainty floor (typical XRD precision limit)
    c_lattice_err = c_lattice_err.clip(lower=0.0005)
    
    # Coherence length bar chart with error bars
    bars = a1.bar(x, cv.coherence_length_nm, color=cols, width=0.72)
    a1.errorbar(x, cv.coherence_length_nm, yerr=coherence_err, 
                fmt='none', ecolor=INK, elinewidth=1.5, capsize=4, capthick=1.5, zorder=10)
    
    for xi, v, err in zip(x, cv.coherence_length_nm, coherence_err):
        a1.text(xi, v + err + 1.2, f'{v:.0f}', ha='center', fontsize=16.5, color=INK)
    a1.set_ylabel('coherence length\nL$_{0002}$ (nm)', fontsize=21)
    a1.set_ylim(0, 39)  # Increased to accommodate error bars and labels
    a1.text(0.02, 1.03, 'out-of-plane crystallite size  (Scherrer / pseudo-Voigt, 0002)',
            transform=a1.transAxes, fontsize=16.5, color=MUTED, va='top')
    a1.text(-0.12, 1.02, '(a)', transform=a1.transAxes, fontsize=22, fontweight='bold', va='top')

    # c lattice parameter scatter with error bars
    c0 = 4.980
    a2.axhspan(c0 * 0.999, c0 * 1.001, color='#E2EFE6', lw=0)
    a2.axhline(c0, color=GREEN_D, ls=(0, (4, 3)), lw=2)
    a2.errorbar(x, cv.c_lattice_ang, yerr=c_lattice_err,
                fmt='none', ecolor=INK, elinewidth=1.5, capsize=4, capthick=1.5, zorder=4)
    a2.scatter(x, cv.c_lattice_ang, s=140, c=cols, ec=INK, lw=1.2, zorder=5)
    a2.text(len(cv) - 0.35, c0 - 0.0012, 'relaxed c$_0$ = 4.980 Å', ha='right',
            fontsize=16.5, color=GREEN_D)
    a2.set_ylabel('c-lattice (Å)', fontsize=21)
    a2.set_ylim(4.977, 4.988)  # Slightly expanded to show error bars
    a2.set_xticks(x)
    a2.set_xticklabels([f'#{r}' for r in cv.run], fontsize=18)
    a2.set_xlabel('growth run')
    a2.text(0.02, 0.75, 'all films within 0.08 % of relaxed c$_0$  →  nearly strain-free',
            transform=a2.transAxes, fontsize=16.5, color=INK)
    a2.text(-0.12, 1.12, '(b)', transform=a2.transAxes, fontsize=22, fontweight='bold', va='top')
    
    plt.show()
    save(fig, 'fig4_coherence.png')


if __name__ == '__main__':
    main()