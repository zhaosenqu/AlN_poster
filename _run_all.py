"""
Master script to generate all figures for ORNL Summer 2026 poster.
"""
import fig1_concept
import fig2_campaign
import fig3_rocking
import fig4_coherence
import fig5_afm_rms
import fig6_grains
import fig7_xrr
import compute_stats


def main():
    print("Generating Figure 1: Concept schematic...")
    fig1_concept.main()
    
    print("Generating Figure 2: Campaign overview...")
    fig2_campaign.main()
    
    print("Generating Figure 3: Rocking-curve FWHM by condition...")
    fig3_rocking.main()
    
    print("Generating Figure 4: Coherence length & c lattice...")
    fig4_coherence.main()
    
    print("Generating Figure 5: AFM RMS roughness...")
    fig5_afm_rms.main()
    
    print("Generating Figure 6: Surface feature size vs coherence...")
    fig6_grains.main()
    
    print("Generating Figure 7: XRR density & thickness...")
    fig7_xrr.main()
    
    print("\nComputing derived statistics...")
    compute_stats.main()
    
    print("\nAll figures generated successfully!")


if __name__ == '__main__':
    main()