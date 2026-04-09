import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Patch

# colors
C = {
    "disk_inner": "#FCDE5A",
    "disk_mid":   "#EF9F27",
    "disk_outer": "#D85A30",
    "disk_edge":  "#BA7517",
    "trap":       "#CC7A00",
    "smbh_edge":  "#555555",
    "bh_fill":    "#3C3489",
    "bh_edge":    "#6655CC",
    "scatter":    "#333333",
    "new_fill":   "#FAC775",
    "new_edge":   "#BA7517",
    "black":      "#111111",
    "gray":       "#555555",
    "pair":       "#3C3489",
    "new_label":  "#A05C00",
}

def rgb(h):
    return np.array([int(h[i:i+2], 16)/255 for i in (1, 3, 5)])

def blend(c1, c2, t):
    return tuple((1 - t) * rgb(c1) + t * rgb(c2))

def add_circle(ax, xy, r, fc, ec=None, lw=1.0, z=6):
    ax.add_patch(Circle(xy, r, facecolor=fc, edgecolor=ec if ec else fc, linewidth=lw, zorder=z))

def add_label(ax, anchor, y, title, subtitle, title_color, dot_color, x=5.6):
    ax.plot([anchor[0], x - 0.05], [anchor[1], y],
            color="#666666", lw=1.1, linestyle=(0, (5, 2)), zorder=4)
    ax.plot(*anchor, "o", color=dot_color, ms=3.5, zorder=9)
    ax.text(x, y + 0.08, title, color=title_color, fontsize=10,
            fontweight="bold", va="bottom", zorder=10)
    if subtitle:
        ax.text(x, y - 0.28, subtitle, color=C["gray"], fontsize=8.5,
                va="bottom", zorder=10)

fig, ax = plt.subplots(figsize=(13, 7.5))
ax.set(xlim=(-5.5, 11), ylim=(-4.5, 5.5), aspect="equal")
ax.axis("off")
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

disk_rx, disk_ry = 4.6, 1.56
trap_rx, trap_ry = 2.16, 0.70

# disk gradient
for f in np.linspace(1, 1/60, 60):
    if f < 0.25:
        color = (*rgb(C["disk_inner"]), 0.75 * (1 - 0.3 * f / 0.25))
    elif f < 0.55:
        color = (*blend(C["disk_inner"], C["disk_mid"], (f - 0.25) / 0.30), 0.58)
    else:
        t = (f - 0.55) / 0.45
        color = (*blend(C["disk_mid"], C["disk_outer"], t),
                 np.interp(t, [0, 1], [0.50, 0.08]))
    ax.add_patch(Ellipse((0, 0), 2 * disk_rx * f, 2 * disk_ry * f, color=color, zorder=1))

ax.add_patch(Ellipse((0, 0), 2 * disk_rx, 2 * disk_ry,
                     fill=False, edgecolor=C["disk_edge"], linewidth=1.8, zorder=3))

ax.add_patch(Ellipse((0, 0), 2 * trap_rx, 2 * trap_ry,
                     fill=False, edgecolor=C["trap"], linewidth=2.2,
                     linestyle=(0, (6, 2)), zorder=4))
ax.text(-1.4, 0.55, r"$r_\mathrm{disk}$", color=C["trap"],
        fontsize=11, fontweight="bold", zorder=10)

# r_b
ax.annotate("", xy=(disk_rx, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-", color="#333333", lw=1.4, linestyle="dashed"))
ax.plot([disk_rx, disk_rx], [-0.15, 0.15], color="#333333", lw=1.6, zorder=5)
ax.text(disk_rx + 0.12, 0.0, r"$r_b$", color=C["black"],
        fontsize=11, fontweight="bold", va="center", zorder=10)

# SMBH
add_circle(ax, (0, 0), 0.54, "#1a1a18", C["smbh_edge"], 1.4, 6)
ax.text(0,  0.12, r"$M$",  color=C["black"], fontsize=9, fontweight="bold",
        ha="center", va="center", zorder=8)
ax.text(0, -0.15, "SMBH", color="#B4B2A9", fontsize=7,
        ha="center", va="center", zorder=8)

# merging pair
bh1, bh2 = (-1.92, 0.22), (-1.65, -0.18)
for p in (bh1, bh2):
    add_circle(ax, p, 0.16, C["bh_fill"], C["bh_edge"], 1.3, 6)

ax.annotate("", xy=(bh2[0] + 0.05, bh2[1] + 0.05), xytext=(bh1[0] + 0.05, bh1[1] - 0.10),
            arrowprops=dict(arrowstyle="->", color=C["bh_edge"], lw=1.2,
                            connectionstyle="arc3,rad=0.35"),
            zorder=8)

# new objects
cluster = (-3.2, -0.30)
offsets = [(-0.28, 0.22), (0.0, 0.34), (0.28, 0.18),
           (-0.18, -0.22), (0.18, -0.28), (0.38, -0.08), (-0.38, 0.0)]
sizes = [0.10, 0.08, 0.09, 0.07, 0.09, 0.08, 0.07]
for (dx, dy), r in zip(offsets, sizes):
    add_circle(ax, (cluster[0] + dx, cluster[1] + dy), r,
               C["new_fill"], C["new_edge"], 0.9, 6)

# scattered BHs
scattered = [(2.40, 3.80), (-0.60, 4.20), (-3.00, 2.80),
             (-3.40, -2.60), (0.40, -3.90), (3.20, -3.40)]
for p in scattered:
    add_circle(ax, p, 0.13, C["scatter"], C["scatter"], 1.0, 5)

# labels
add_label(ax, (0.38, 0.46), 3.2,
          r"Supermassive BH ($M_\mathrm{SMBH}$)", None,
          C["black"], C["smbh_edge"])

add_label(ax, (2.40, 3.80), 2.2,
          r"$N_\mathrm{sbh,pre}$ -- scattered BHs",
          "Pre-existing population, captured by disk",
          C["scatter"], C["scatter"])

add_label(ax, (-trap_rx + 0.05, 0.0), 1.0,
          r"Migration trap ($r_\mathrm{disk}$)",
          "Torque reversal stalls inward drift",
          C["trap"], C["trap"])

add_label(ax, (bh2[0] + 0.10, bh2[1]), -0.2,
          "Merging BH pair",
          r"Harden via disk torques $\rightarrow$ GW merger",
          C["pair"], C["pair"])

add_label(ax, (cluster[0] + 0.40, cluster[1] - 0.10), -1.4,
          r"$N_\mathrm{sbh,new}$ -- new compact objects",
          "Products of SN explosions + BH mergers",
          C["new_label"], C["new_edge"])

ax.text(0.5, 0.97, "Black Hole Mergers & Supernova Explosions in AGN Disks",
        transform=ax.transAxes, ha="center", va="top",
        color=C["black"], fontsize=13, fontweight="bold")

ax.legend(handles=[
    Patch(facecolor=C["bh_fill"], edgecolor=C["bh_edge"], label="In-disk SBH (merging)"),
    Patch(facecolor=C["scatter"], edgecolor=C["scatter"], label=r"$N_\mathrm{sbh,pre}$ (scattered)"),
    Patch(facecolor=C["new_fill"], edgecolor=C["new_edge"], label=r"$N_\mathrm{sbh,new}$ (SN + merger)")
], loc="lower left", framealpha=0.8, facecolor="white",
   edgecolor="#cccccc", fontsize=9, labelcolor=C["black"])

plt.tight_layout(pad=0.3)
plt.savefig("agn_disk.png", dpi=180, bbox_inches="tight", facecolor="white")
plt.savefig("agn_disk.pdf", bbox_inches="tight", facecolor="white")
print("done -- agn_disk.png and agn_disk.pdf saved.")
