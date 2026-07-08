"""
Figure 1: Plasma-modified SiOxNy templating for (0002)-textured wurtzite AlN.

Panel (a): Untreated SiO2 → mixed/polycrystalline AlN with random c-axis orientations.
Panel (b): Nitrogen-plasma-modified SiOxNy → preferential (0002) texture with c-axis ⊥ substrate.
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection

# -----------------------------------------------------------------------------
# Shared palette (CVD-safe)
# -----------------------------------------------------------------------------
try:
    from fig_utils import GREEN, GREEN_D, GREEN_L, TEAL, AMBER, RED, INK, MUTED, FAINT, OUT
except Exception:
    GREEN = "#007833"
    GREEN_D = "#00542B"
    GREEN_L = "#6FB98F"
    TEAL = "#0072B2"
    AMBER = "#E69F00"
    RED = "#D55E00"
    INK = "#1E252B"
    MUTED = "#5B6770"
    FAINT = "#C9D2CC"
    OUT = Path(__file__).resolve().parent / "figures"

SCRIPT_DIR = Path(__file__).resolve().parent
OUT = Path(OUT)
OUT.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Publication-safe matplotlib settings
# -----------------------------------------------------------------------------
mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.linewidth": 1.0,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "savefig.dpi": 600,
    "figure.dpi": 180,
})

# -----------------------------------------------------------------------------
# Colors and font sizes
# -----------------------------------------------------------------------------
PANEL_EDGE = "#D6DDD8"
SI_FILL = "#B8BDC2"
SIO2_FILL = "#CFE3EE"
SION_FILL = "#CDEDD9"
ALN_MIX_FILL = "#E9ECEA"
ALN_TEXT_FILL = "#DCEFE3"
PLANE_GREY = "#6D767D"
BOND_COLOR = "#4A5568"  # Bond line color

FS_PANEL = 12
FS_TITLE = 11
FS_SUBTITLE = 9
FS_LABEL = 8.5
FS_SMALL = 7


# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def rotate_xy(points: np.ndarray, angle_deg: float, center: tuple[float, float]) -> np.ndarray:
    """Rotate Nx2 points about center by angle_deg."""
    theta = np.deg2rad(angle_deg)
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    c = np.asarray(center)
    return (points - c) @ rot.T + c


def add_panel_box(ax, x: float, y: float, w: float, h: float) -> None:
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.03,rounding_size=0.08",
        fc="white", ec=PANEL_EDGE, lw=0.9, zorder=0,
    )
    ax.add_patch(box)


def substrate_stack(ax, x0: float, y0: float, width: float, *, oxynitride: bool = False) -> float:
    """Draw Si / SiO2 stack; return top y-coordinate for AlN growth."""
    si_h = 0.38
    sio2_h = 0.48
    sion_h = 0.22 if oxynitride else 0.0

    ax.add_patch(Rectangle((x0, y0), width, si_h, fc=SI_FILL, ec=INK, lw=0.8, zorder=2))
    ax.text(x0 + width / 2, y0 + si_h / 2, "Si", ha="center", va="center", fontsize=FS_LABEL, color=INK)

    ax.add_patch(Rectangle((x0, y0 + si_h), width, sio2_h, fc=SIO2_FILL, ec=INK, lw=0.8, zorder=2))
    ax.text(x0 + width / 2, y0 + si_h + sio2_h / 2, r"SiO$_2$", ha="center", va="center", fontsize=FS_LABEL, color=INK)

    if oxynitride:
        ax.add_patch(Rectangle((x0, y0 + si_h + sio2_h), width, sion_h, fc=SION_FILL, ec=GREEN_D, lw=0.85, zorder=3))
        ax.text(x0 + width / 2, y0 + si_h + sio2_h + sion_h / 2, r"SiO$_x$N$_y$", ha="center", va="center", 
                fontsize=FS_SMALL, color=GREEN_D, fontweight="bold")

    return y0 + si_h + sio2_h + sion_h


def irregular_surface(x0: float, width: float, y: float, amp: float, n: int = 80) -> tuple[np.ndarray, np.ndarray]:
    xs = np.linspace(x0, x0 + width, n)
    ys = y + amp * (0.55 * np.sin(np.linspace(0, 3.5 * np.pi, n)) + 0.25 * np.sin(np.linspace(0, 9 * np.pi, n) + 0.7))
    return xs, ys


def film_background(ax, x0: float, y0: float, width: float, height: float, fill: str, edge: str, *, rough: bool = False) -> None:
    if rough:
        xs, ys = irregular_surface(x0, width, y0 + height, 0.045)
        pts = np.vstack([[x0, y0], [x0 + width, y0], np.c_[xs[::-1], ys[::-1]], [x0, y0]])
        ax.add_patch(Polygon(pts, closed=True, fc=fill, ec=edge, lw=0.9, zorder=2))
    else:
        ax.add_patch(Rectangle((x0, y0), width, height, fc=fill, ec=edge, lw=0.9, zorder=2))


def draw_bond(ax, p1: np.ndarray, p2: np.ndarray, color: str = BOND_COLOR, 
              lw: float = 0.8, alpha: float = 0.7, zorder: int = 5, clip_patch=None) -> Line2D:
    """Draw a bond line between two points."""
    line = Line2D([p1[0], p2[0]], [p1[1], p2[1]], 
                  lw=lw, color=color, alpha=alpha, zorder=zorder, solid_capstyle='round')
    if clip_patch is not None:
        line.set_clip_path(clip_patch)
    ax.add_line(line)
    return line


# -----------------------------------------------------------------------------
# Wurtzite crystallite drawing (crystallographically accurate with bonds)
# -----------------------------------------------------------------------------
def draw_wurtzite_crystallite(
    ax,
    cx: float,
    cy: float,
    w: float,
    h: float,
    angle: float,
    *,
    face: str,
    edge: str,
    plane_color: str,
    arrow_color: str,
    alpha: float = 1.0,
    show_bonds: bool = True,
) -> None:
    """
    Draw a wurtzite crystallite with proper (0002) basal planes, Al-N bilayer structure, and bonds.
    
    The crystallite is shown in cross-section (viewed along [11-20]), displaying:
    - Hexagonal prism morphology (elongated along c-axis, c/a ≈ 1.6)
    - (0002) basal planes as horizontal lines perpendicular to c-axis
    - Al-N bilayers with correct wurtzite stacking (u ≈ 0.382)
    - Tetrahedral Al-N bonds
    - c-axis arrow indicating crystallographic orientation
    """
    # Hexagonal prism cross-section vertices
    hw, hh = w * 0.5, h * 0.5
    taper = 0.15 * w
    
    local = np.array([
        [cx - hw, cy - hh + taper],
        [cx - hw, cy + hh - taper],
        [cx - hw + taper, cy + hh],
        [cx + hw - taper, cy + hh],
        [cx + hw, cy + hh - taper],
        [cx + hw, cy - hh + taper],
        [cx + hw - taper, cy - hh],
        [cx - hw + taper, cy - hh],
    ])
    
    pts = rotate_xy(local, angle, (cx, cy))
    patch = Polygon(pts, closed=True, fc=face, ec=edge, lw=0.9, alpha=alpha, zorder=4)
    ax.add_patch(patch)
    
    # Wurtzite bilayer structure parameters
    n_bilayers = 4
    u_param = 0.382
    bilayer_spacing = h * 0.8 / (n_bilayers + 0.5)
    
    # Store atom positions for bond drawing
    al_positions = []
    n_positions = []
    
    for i in range(n_bilayers):
        y_base = cy - h * 0.35 + i * bilayer_spacing
        y_al = y_base + bilayer_spacing * 0.15
        y_n = y_al + u_param * bilayer_spacing
        
        # (0002) basal plane line
        plane_pts = np.array([[cx - w * 0.38, y_base], [cx + w * 0.38, y_base]])
        plane_pts = rotate_xy(plane_pts, angle, (cx, cy))
        line = Line2D(plane_pts[:, 0], plane_pts[:, 1], lw=0.6, color=plane_color, 
                      alpha=0.5, zorder=5, linestyle='--')
        line.set_clip_path(patch)
        ax.add_line(line)
        
        # Al atoms positions
        n_al = 3
        layer_al = []
        for j in range(n_al):
            x_al = cx - w * 0.25 + j * (w * 0.5 / max(1, n_al - 1))
            pt = rotate_xy(np.array([[x_al, y_al]]), angle, (cx, cy))[0]
            layer_al.append(pt)
        al_positions.append(layer_al)
        
        # N atoms positions
        n_n = 2
        layer_n = []
        for j in range(n_n):
            x_n = cx - w * 0.12 + j * (w * 0.24 / max(1, n_n - 1))
            pt = rotate_xy(np.array([[x_n, y_n]]), angle, (cx, cy))[0]
            layer_n.append(pt)
        n_positions.append(layer_n)
    
    # Draw bonds (Al-N tetrahedral coordination)
    if show_bonds:
        for i, (al_layer, n_layer) in enumerate(zip(al_positions, n_positions)):
            # Bonds from Al to N in same bilayer (upward bonds)
            for al_pos in al_layer:
                for n_pos in n_layer:
                    dist = np.sqrt((al_pos[0] - n_pos[0])**2 + (al_pos[1] - n_pos[1])**2)
                    if dist < w * 0.25:  # Only connect nearby atoms
                        draw_bond(ax, al_pos, n_pos, color=BOND_COLOR, lw=0.7, 
                                  alpha=0.6, zorder=5, clip_patch=patch)
            
            # Bonds from N to Al in next bilayer (downward bonds to complete tetrahedra)
            if i < len(al_positions) - 1:
                next_al_layer = al_positions[i + 1]
                for n_pos in n_layer:
                    for al_pos in next_al_layer:
                        dist = np.sqrt((al_pos[0] - n_pos[0])**2 + (al_pos[1] - n_pos[1])**2)
                        if dist < w * 0.3:
                            draw_bond(ax, n_pos, al_pos, color=BOND_COLOR, lw=0.7,
                                      alpha=0.6, zorder=5, clip_patch=patch)
    
    # Draw atoms (on top of bonds)
    for al_layer in al_positions:
        for pt in al_layer:
            sc = ax.scatter(pt[0], pt[1], s=14, c=TEAL, edgecolors='white', 
                           linewidths=0.3, zorder=7, alpha=0.95)
            sc.set_clip_path(patch)
    
    for n_layer in n_positions:
        for pt in n_layer:
            sc = ax.scatter(pt[0], pt[1], s=9, c=AMBER, edgecolors='white',
                           linewidths=0.2, zorder=7, alpha=0.95)
            sc.set_clip_path(patch)
    
    # c-axis arrow
    arrow_start = np.array([[cx, cy - h * 0.15]])
    arrow_end = np.array([[cx, cy + h * 0.42]])
    arrow_start = rotate_xy(arrow_start, angle, (cx, cy))
    arrow_end = rotate_xy(arrow_end, angle, (cx, cy))
    ax.add_patch(FancyArrowPatch(
        arrow_start[0], arrow_end[0],
        arrowstyle="-|>", mutation_scale=6, lw=1.0, color=arrow_color, zorder=8
    ))


def draw_mixed_aln(ax, x0: float, y0: float, width: float, height: float) -> None:
    """
    Untreated case: mixed/randomly oriented wurtzite nanocrystallites.
    Shows polycrystalline AlN with random c-axis orientations on amorphous SiO2.
    """
    film_background(ax, x0, y0, width, height, ALN_MIX_FILL, MUTED, rough=True)

    rng = np.random.default_rng(42)
    
    # Two rows of crystallites with random orientations
    centers = [
        (x0 + 0.50, y0 + 0.35), (x0 + 1.15, y0 + 0.38), (x0 + 1.85, y0 + 0.36),
        (x0 + 2.55, y0 + 0.37), (x0 + 3.25, y0 + 0.35),
        (x0 + 0.80, y0 + 0.90), (x0 + 1.50, y0 + 0.92), (x0 + 2.20, y0 + 0.88),
        (x0 + 2.95, y0 + 0.91),
    ]
    
    angles = [-52, 18, 78, -28, 42, 58, -68, 8, -15]
    
    for (cx, cy), ang in zip(centers, angles):
        draw_wurtzite_crystallite(
            ax, cx, cy,
            w=0.48 + 0.08 * rng.random(),
            h=0.50 + 0.10 * rng.random(),
            angle=ang,
            face="#F7F8F7",
            edge=MUTED,
            plane_color=PLANE_GREY,
            arrow_color=RED,
            alpha=0.95,
            show_bonds=True,
        )

    ax.text(x0 + width / 2, y0 + height + 0.12, "random c-axis",
            ha="center", va="bottom", fontsize=FS_SMALL, color=RED, fontweight="bold")


def draw_textured_aln(ax, x0: float, y0: float, width: float, height: float) -> None:
    """
    Treated case: (0002)-textured AlN with c-axis perpendicular to substrate.
    Shows columnar grains with aligned wurtzite bilayer structure and bonds.
    """
    film_background(ax, x0, y0, width, height, ALN_TEXT_FILL, GREEN_D, rough=False)
    
    # Wurtzite bilayer parameters
    n_bilayers = 7
    u_param = 0.382
    bilayer_h = (height - 0.15) / n_bilayers
    
    # Grain boundaries
    grain_boundaries = [x0 + 1.28, x0 + 2.45]
    
    # Store all atom positions for bond drawing
    all_al_positions = []
    all_n_positions = []
    
    # Draw continuous (0002) planes across columnar grains
    for i in range(n_bilayers):
        y_base = y0 + 0.08 + i * bilayer_h
        y_al = y_base + bilayer_h * 0.25
        y_n = y_al + u_param * bilayer_h * 0.7
        
        # (0002) basal plane lines (broken at grain boundaries)
        segments = [
            (x0 + 0.12, grain_boundaries[0] - 0.06),
            (grain_boundaries[0] + 0.06, grain_boundaries[1] - 0.06),
            (grain_boundaries[1] + 0.06, x0 + width - 0.12),
        ]
        
        for x_start, x_end in segments:
            ax.plot([x_start, x_end], [y_base, y_base],
                    color=GREEN_D, lw=0.8, solid_capstyle="round", zorder=5, 
                    alpha=0.6, linestyle='--')
        
        # Al atoms positions
        n_al = 11
        x_al_positions = np.linspace(x0 + 0.25, x0 + width - 0.25, n_al)
        layer_al = [(x, y_al) for x in x_al_positions]
        all_al_positions.append(layer_al)
        
        # N atoms positions (offset horizontally for wurtzite stacking)
        n_n = 10
        x_n_positions = np.linspace(x0 + 0.32, x0 + width - 0.32, n_n)
        layer_n = [(x, y_n) for x in x_n_positions]
        all_n_positions.append(layer_n)
    
    # Draw bonds between Al and N atoms
    for i, (al_layer, n_layer) in enumerate(zip(all_al_positions, all_n_positions)):
        # Bonds from Al to N in same bilayer
        for al_pos in al_layer:
            for n_pos in n_layer:
                dx = abs(al_pos[0] - n_pos[0])
                # Connect to nearest N atoms (tetrahedral geometry)
                if dx < (width / n_al) * 1.2:
                    # Skip bonds across grain boundaries
                    crosses_boundary = any(
                        min(al_pos[0], n_pos[0]) < gb < max(al_pos[0], n_pos[0])
                        for gb in grain_boundaries
                    )
                    if not crosses_boundary:
                        draw_bond(ax, np.array(al_pos), np.array(n_pos), 
                                  color=BOND_COLOR, lw=0.6, alpha=0.5, zorder=5)
        
        # Bonds from N to Al in next bilayer
        if i < len(all_al_positions) - 1:
            next_al_layer = all_al_positions[i + 1]
            for n_pos in n_layer:
                for al_pos in next_al_layer:
                    dx = abs(al_pos[0] - n_pos[0])
                    if dx < (width / n_al) * 1.2:
                        crosses_boundary = any(
                            min(al_pos[0], n_pos[0]) < gb < max(al_pos[0], n_pos[0])
                            for gb in grain_boundaries
                        )
                        if not crosses_boundary:
                            draw_bond(ax, np.array(n_pos), np.array(al_pos),
                                      color=BOND_COLOR, lw=0.6, alpha=0.5, zorder=5)
    
    # Draw atoms on top of bonds
    for al_layer in all_al_positions:
        for x, y in al_layer:
            ax.scatter(x, y, s=12, c=TEAL, edgecolors='white', 
                      linewidths=0.25, zorder=6, alpha=0.9)
    
    for n_layer in all_n_positions:
        for x, y in n_layer:
            ax.scatter(x, y, s=8, c=AMBER, edgecolors='white',
                      linewidths=0.2, zorder=6, alpha=0.9)
    
    # Columnar grain boundaries
    for xb in grain_boundaries:
        yy = np.linspace(y0 + 0.05, y0 + height - 0.05, 20)
        xx = xb + 0.015 * np.sin(np.linspace(0, 2.5 * np.pi, 20))
        ax.plot(xx, yy, color=GREEN_D, lw=0.8, alpha=0.5, zorder=4)
    
    # c-axis arrow
    ax.add_patch(FancyArrowPatch(
        (x0 + width + 0.08, y0 + 0.20),
        (x0 + width + 0.08, y0 + height - 0.10),
        arrowstyle="-|>", mutation_scale=10, lw=1.4, color=GREEN_D, zorder=7
    ))
    ax.text(x0 + width + 0.22, y0 + height / 2, r"$\mathbf{c}$",
            ha="left", va="center", fontsize=FS_LABEL, color=GREEN_D, fontweight="bold")
    
    ax.text(x0 + width / 2, y0 + height + 0.12, r"(0002) $\parallel$ substrate",
            ha="center", va="bottom", fontsize=FS_SMALL, color=GREEN_D, fontweight="bold")


def draw_process_arrow(ax) -> None:
    """Draw arrow indicating plasma treatment process."""
    ax.add_patch(FancyArrowPatch(
        (5.20, 2.05), (6.10, 2.05),
        arrowstyle="simple",
        mutation_scale=14,
        fc=AMBER, ec=AMBER, lw=0, zorder=5
    ))
    ax.text(5.65, 2.48, r"N$_2$ plasma",
            ha="center", va="center", fontsize=FS_LABEL, color="#8A5A00", fontweight="bold")


def save_publication(fig, stem: str = "fig1_concept") -> None:
    """Save publication-quality outputs (both opaque and transparent backgrounds)."""
    for transparent, suffix in [(False, ""), (True, "_transparent")]:
        facecolor = "none" if transparent else "white"
        for ext in ("pdf", "svg", "png"):
            fig.savefig(
                OUT / f"{stem}{suffix}.{ext}",
                bbox_inches="tight",
                pad_inches=0.02,
                transparent=transparent,
                facecolor=facecolor,
                dpi=600 if ext == "png" else None,
            )
    print(f"Saved {stem} (opaque + transparent) as PDF, SVG, PNG in {OUT}")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> None:
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 4.6)
    ax.set_aspect("equal")
    ax.axis("off")

    # Panel containers
    add_panel_box(ax, 0.20, 0.20, 4.70, 4.20)
    add_panel_box(ax, 6.30, 0.20, 4.80, 4.20)

    # Panel (a): Untreated SiO2
    ax.text(0.38, 4.18, "(a)", fontsize=FS_PANEL, fontweight="bold", color=INK, ha="left", va="center")
    ax.text(2.55, 4.18, r"Untreated SiO$_2$", fontsize=FS_TITLE, fontweight="bold", color=INK, ha="center", va="center")
    ax.text(2.55, 3.90, "mixed texture", fontsize=FS_SUBTITLE, color=RED, fontweight="bold", ha="center", va="center")

    # Panel (b): Plasma-modified
    ax.text(6.48, 4.18, "(b)", fontsize=FS_PANEL, fontweight="bold", color=INK, ha="left", va="center")
    ax.text(8.70, 4.18, r"Plasma-modified SiO$_x$N$_y$", fontsize=FS_TITLE, fontweight="bold", color=INK, ha="center", va="center")
    ax.text(8.70, 3.90, "(0002)-textured AlN", fontsize=FS_SUBTITLE, color=GREEN_D, fontweight="bold", ha="center", va="center")

    # Cross-section stacks
    left_x, right_x = 0.70, 6.80
    stack_w = 3.75
    y_base = 0.55
    left_top = substrate_stack(ax, left_x, y_base, stack_w, oxynitride=False)
    right_top = substrate_stack(ax, right_x, y_base, stack_w, oxynitride=True)

    # AlN films
    film_h = 1.30
    draw_mixed_aln(ax, left_x, left_top, stack_w, film_h)
    draw_textured_aln(ax, right_x, right_top, stack_w, film_h)

    # AlN labels
    ax.text(left_x - 0.10, left_top + film_h / 2, "AlN", ha="right", va="center",
            fontsize=FS_LABEL, color=MUTED, rotation=90)
    ax.text(right_x - 0.10, right_top + film_h / 2, "AlN", ha="right", va="center",
            fontsize=FS_LABEL, color=GREEN_D, rotation=90)

    # Process arrow
    draw_process_arrow(ax)

    # Legend for Al/N atoms and bonds
    legend_x, legend_y = 0.40, 0.32
    # Bond line in legend
    ax.plot([legend_x - 0.08, legend_x + 0.08], [legend_y, legend_y], 
            color=BOND_COLOR, lw=1.0, alpha=0.7, zorder=20)
    ax.scatter([legend_x - 0.08], [legend_y], s=14, c=TEAL, edgecolors='white',
               linewidths=0.3, zorder=21)
    ax.scatter([legend_x + 0.08], [legend_y], s=10, c=AMBER, edgecolors='white',
               linewidths=0.2, zorder=21)
    ax.text(legend_x + 0.22, legend_y, "Al–N", ha="left", va="center", 
            fontsize=FS_SMALL, color=MUTED)

    plt.show()
    save_publication(fig)
    plt.close(fig)


if __name__ == "__main__":
    main()