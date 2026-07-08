"""
Compute and print derived statistics from all data.
"""
import json
import numpy as np

from fig_utils import load_all_data, THIN, BEST


def jd(x):
    return float(np.round(x, 4))


def main():
    rc, coh, xrr, rms, grn = load_all_data()
    
    # Grain data for feature sizes
    g1 = grn[(grn.scan_x_um == 1.0) & (~grn.file.str.contains('masked'))].copy()
    runs6 = [15, 22, 24, 25, 26, 27]
    med = [g1[g1.run == r].median_equiv_diameter_nm.mean() for r in runs6]
    
    # XRR reliable fits
    ok = xrr[xrr.run.isin([26, 30, 32, 33])].sort_values('run')
    
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
    
    print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    main()