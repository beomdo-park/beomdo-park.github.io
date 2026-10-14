"""QEC decoder concept figure: (a) syndrome -> (b) Transformer decoder -> (c) correction.

Layout borrowed from a Nano Banana draft (3 panels, round stack, layer stack, bit strips).
Every colored element is computed from qec_concept_data.json:
  syndrome = H @ errors (mod 2),  residual = H @ (errors XOR correction) (mod 2).
Sized at print width (5.5 in, NeurIPS/ICLR single column) so LaTeX includes it 1:1.
Run:  python make_qec_decoder_concept.py   ->  qec_decoder_concept.pdf / .png
"""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, Wedge

HERE = pathlib.Path(__file__).resolve().parent
DATA = json.loads((HERE / "qec_concept_data.json").read_text(encoding="utf-8"))

COL_W = 5.5
PALETTE = {"correction": "#1b9e77", "syndrome": "#d95f02", "error": "#b2182b",
           "ink": "#333333", "gray": "#666666", "qubit": "#e9e9e9", "panel": "#f7f7f7"}
plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans"})

# ---------------------------------------------------------------- data -> bits
N = DATA["n_data"]
STABS = DATA["stabilizers"]
errors = set(DATA["errors"])
correction = set(errors)          # illustrative: a successful decode returns the error pattern


def parity(stab, flips):
    return sum(q in flips for q in stab["support"]) % 2


syndrome = [parity(s, errors) for s in STABS]
residual = [parity(s, errors ^ correction) for s in STABS]
mask = [int(q in correction) for q in range(N)]
assert len(syndrome) == 8 and sum(residual) == 0

# ---------------------------------------------------------------- canvas
X0, X1, Y0, Y1 = -0.1, 30.1, -0.1, 9.7
fig, ax = plt.subplots(figsize=(COL_W, COL_W * (Y1 - Y0) / (X1 - X0)))
ax.set_xlim(X0, X1)
ax.set_ylim(Y0, Y1)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(0, 0, 1, 1)

PANEL_Y0, PANEL_Y1, TITLE_Y = 1.4, 8.4, 8.8
LAT_Y, S = 5.5, 1.45


def frame(x0, y0, x1, y1, fc, ec=PALETTE["ink"], lw=0.9, z=0):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0,
                                boxstyle="round,pad=0,rounding_size=0.4",
                                fc=fc, ec=ec, lw=lw, zorder=z))


def qpos(q, cx, cy):
    r, c = divmod(q, 3)
    return cx + (c - 1) * S, cy - (r - 1) * S


def lattice(cx, cy, lit, err, corr):
    for k in range(3):
        ax.plot([cx - S, cx + S], [cy - (k - 1) * S] * 2, color=PALETTE["gray"], lw=0.7, zorder=1)
        ax.plot([cx + (k - 1) * S] * 2, [cy - S, cy + S], color=PALETTE["gray"], lw=0.7, zorder=1)
    for st, on in zip(STABS, lit):
        fc = PALETTE["syndrome"] if on else "white"
        pts = [qpos(q, cx, cy) for q in st["support"]]
        mx = sum(p[0] for p in pts) / len(pts)
        my = sum(p[1] for p in pts) / len(pts)
        if st["kind"] == "bulk":
            h = 0.27 * S
            ax.add_patch(Rectangle((mx - h, my - h), 2 * h, 2 * h, fc=fc, ec=PALETTE["ink"], lw=0.7, zorder=2))
        else:
            ang = {"top": (0, 180), "bottom": (180, 360), "right": (-90, 90), "left": (90, 270)}[st["side"]]
            ax.add_patch(Wedge((mx, my), 0.36 * S, *ang, fc=fc, ec=PALETTE["ink"], lw=0.7, zorder=2))
    r = 0.25 * S
    for q in range(N):
        x, y = qpos(q, cx, cy)
        if q in err:
            ax.add_patch(Circle((x, y), r, fc=PALETTE["error"], ec=PALETTE["ink"], lw=0.8, zorder=3))
            ax.text(x, y - 0.03, "×", color="white", ha="center", va="center", fontsize=8, zorder=4)
        elif q in corr:
            ax.add_patch(Circle((x, y), r, fc="white", ec=PALETTE["correction"], lw=1.8, zorder=3))
            ax.text(x, y - 0.02, "✓", color=PALETTE["correction"], ha="center", va="center", fontsize=8, zorder=4)
        else:
            ax.add_patch(Circle((x, y), r, fc=PALETTE["qubit"], ec=PALETTE["ink"], lw=0.8, zorder=3))


def bitstrip(cx, y, bits, on_color, label, size=0.3):
    gap = size * 1.12
    x0 = cx - len(bits) * gap / 2
    for i, b in enumerate(bits):
        ax.add_patch(Rectangle((x0 + i * gap, y), size, size, fc=on_color if b else "white",
                               ec=PALETTE["ink"], lw=0.6, zorder=5))
    ax.text(cx, y + size + 0.3, label, ha="center", va="bottom", color=PALETTE["ink"])


def elbow(points):
    xs, ys = zip(*points)
    ax.plot(xs[:-1], ys[:-1], color=PALETTE["ink"], lw=1.2, zorder=1, solid_joinstyle="miter")
    ax.annotate("", xy=points[-1], xytext=points[-2],
                arrowprops=dict(arrowstyle="-|>", color=PALETTE["ink"], lw=1.2, mutation_scale=9,
                                shrinkA=0, shrinkB=0))


def title(x, text):
    ax.text(x, TITLE_Y, text, ha="left", va="bottom", fontsize=8.5, color=PALETTE["ink"])


# ---------------------------------------------------------------- (a) syndrome extraction
AX0, AX1, ACX = 0.4, 6.6, 3.5
for k in (2, 1):                                   # remaining measurement rounds, stacked behind
    frame(AX0 + 0.25 * k, PANEL_Y0 - 0.25 * k, AX1 + 0.25 * k, PANEL_Y1 - 0.25 * k,
          fc="white", ec="#b5b5b5", lw=0.7, z=-3)
frame(AX0, PANEL_Y0, AX1, PANEL_Y1, fc="white", z=-1)
lattice(ACX, LAT_Y, syndrome, errors, set())
bitstrip(ACX, 2.05, syndrome, PALETTE["syndrome"], "8-bit syndrome")
title(AX0, f"(a) Syndrome ({DATA['rounds']} rounds)")

# ---------------------------------------------------------------- (b) Transformer decoder
BX0, BX1 = 11.9, 17.9
frame(BX0, PANEL_Y0, BX1, PANEL_Y1, fc=PALETTE["panel"], z=-1)
LH, LG, LY = 1.35, 0.3, 1.75
layers = ["Embedding", "Attention", "Attention", "Linear head"]
centers = []
for i, name in enumerate(layers):
    y = LY + i * (LH + LG)
    centers.append(y + LH / 2)
    frame(BX0 + 0.35, y, BX1 - 0.35, y + LH, fc="white", lw=0.8)
    if name == "Attention":
        ax.text(BX0 + 0.6, y + LH / 2, name, ha="left", va="center", color=PALETTE["ink"])
        gx = [BX1 - 2.05 + j * 0.42 for j in range(4)]
        for xa in gx:
            for xb in gx:
                ax.plot([xa, xb], [y + LH - 0.32, y + 0.32], color="#9a9a9a", lw=0.35, zorder=3)
        for xa in gx:
            for yy in (y + LH - 0.32, y + 0.32):
                ax.add_patch(Circle((xa, yy), 0.07, fc=PALETTE["ink"], lw=0, zorder=4))
    else:
        ax.text((BX0 + BX1) / 2, y + LH / 2, name, ha="center", va="center", color=PALETTE["ink"])
title(BX0, "(b) Transformer decoder")

# syndrome enters the embedding layer; the mask leaves from the linear head
elbow([(AX1 + 0.7, LAT_Y), (9.6, LAT_Y), (9.6, centers[0]), (BX0 - 0.15, centers[0])])
CX0, CX1, CCX = 23.6, 29.8, 26.7
elbow([(BX1 + 0.15, centers[-1]), (20.4, centers[-1]), (20.4, LAT_Y), (CX0 - 0.1, LAT_Y)])

# ---------------------------------------------------------------- (c) correction applied
frame(CX0, PANEL_Y0, CX1, PANEL_Y1, fc="white", z=-1)
lattice(CCX, LAT_Y, residual, set(), correction)
bitstrip(CCX, 2.05, mask, PALETTE["correction"], "9-bit correction")
title(CX0, "(c) Correction applied")

# ---------------------------------------------------------------- legend (shape + color redundancy)
LEG_Y = 0.45
x = 9.2
for label, shape, color in [("error", "dot", PALETTE["error"]),
                            ("syndrome", "square", PALETTE["syndrome"]),
                            ("correction", "ring", PALETTE["correction"])]:
    if shape == "dot":
        ax.add_patch(Circle((x, LEG_Y), 0.24, fc=color, ec=PALETTE["ink"], lw=0.6))
    elif shape == "square":
        ax.add_patch(Rectangle((x - 0.22, LEG_Y - 0.22), 0.44, 0.44, fc=color, ec=PALETTE["ink"], lw=0.6))
    else:
        ax.add_patch(Circle((x, LEG_Y), 0.24, fc="white", ec=color, lw=1.6))
    ax.text(x + 0.5, LEG_Y, label, va="center", color=PALETTE["ink"])
    x += 0.5 + 0.36 * len(label) + 1.6

fig.savefig(HERE / "qec_decoder_concept.pdf", bbox_inches="tight", pad_inches=0.03)
fig.savefig(HERE / "qec_decoder_concept.png", dpi=300, bbox_inches="tight", pad_inches=0.03)
print("syndrome", syndrome, "| mask", mask, "| residual", residual)
