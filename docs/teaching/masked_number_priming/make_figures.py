"""Figures for the masked number priming walkthrough.

Run from the repository root:  python docs/teaching/masked_number_priming/make_figures.py
Every number in the figures is counted from a block that SweetPea generates.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "skills/sweetpea/examples/masked_number_priming"))
import design  # noqa: E402

SURFACE, INK, MUTED = "#fcfcfb", "#0b0b0b", "#52514e"
BLUE, ORANGE, GRID = "#2a78d6", "#eb6834", "#d9d8d2"
TITLES = {
    "as_published": "As published",
    "drop_identical_double_congruent": "Same-number pairs removed,\nother congruent pairs doubled",
    "proposed": "One congruent and one incongruent\ntarget per prime",
}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "text.color": INK,
                     "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})


def pair_counts(name):
    trials = design.one_block(name)
    return trials.groupby(["prime_number", "target_number"]).size().to_dict(), sorted(trials["target_number"].unique())


def draw_grid(ax, name):
    counts, targets = pair_counts(name)
    for row, prime in enumerate(design.NUMBERS):
        for col, target in enumerate(targets):
            n = counts.get((prime, target), 0)
            x, y = col, len(design.NUMBERS) - 1 - row
            if n == 0:
                ax.add_patch(Rectangle((x + .04, y + .04), .92, .92, facecolor=SURFACE, edgecolor=GRID, linestyle=(0, (3, 3))))
                ax.text(x + .5, y + .5, "not\nshown", ha="center", va="center", color=MUTED, fontsize=9)
                continue
            congruent = design.same_side_of_five(prime, target)
            identical = prime == target
            ax.add_patch(Rectangle((x + .04, y + .04), .92, .92, facecolor=BLUE if congruent else ORANGE,
                                   alpha=.30, edgecolor="none"))
            if identical:
                ax.add_patch(Rectangle((x + .04, y + .04), .92, .92, facecolor="none", edgecolor=BLUE,
                                       hatch="///", linewidth=0))
                ax.add_patch(Rectangle((x + .1, y + .18), .8, .64, facecolor=SURFACE, edgecolor="none"))
            ax.text(x + .5, y + .56, str(n), ha="center", va="center", fontsize=15, fontweight="bold")
            ax.text(x + .5, y + .30, "same number" if identical else ("congruent" if congruent else "incongruent"),
                    ha="center", va="center", fontsize=7.5, color=MUTED)
    ax.set_xlim(0, len(targets)); ax.set_ylim(0, len(design.NUMBERS)); ax.set_aspect("equal")
    ax.set_xticks([i + .5 for i in range(len(targets))], targets)
    ax.set_yticks([i + .5 for i in range(len(design.NUMBERS))], design.NUMBERS[::-1])
    ax.xaxis.tick_top(); ax.xaxis.set_label_position("top")
    ax.set_xlabel("target number"); ax.set_ylabel("prime number")
    ax.tick_params(length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_title(TITLES[name], fontsize=12, fontweight="bold", pad=34, loc="left")


def legend(fig):
    handles = [Patch(facecolor=BLUE, alpha=.30, label="congruent, different numbers"),
               Patch(facecolor=SURFACE, edgecolor=BLUE, hatch="///", label="congruent, same number"),
               Patch(facecolor=ORANGE, alpha=.30, label="incongruent")]
    fig.legend(handles=handles, loc="lower center", ncol=3 if fig.get_figwidth() > 8 else 1, frameon=False, fontsize=10)


def figure(names, filename, width):
    fig, axes = plt.subplots(1, len(names), figsize=(width, 5.4), facecolor=SURFACE)
    for ax, name in zip([axes] if len(names) == 1 else axes, names):
        ax.set_facecolor(SURFACE)
        draw_grid(ax, name)
    fig.suptitle("Trials per block for every prime-target pair", x=.02, ha="left", fontsize=13, color=MUTED)
    legend(fig)
    fig.tight_layout(rect=(0, .07 if fig.get_figwidth() > 8 else .16, 1, .95))
    fig.savefig(HERE / "figures" / filename, dpi=200, facecolor=SURFACE, bbox_inches="tight", pad_inches=.25)
    plt.close(fig)


if __name__ == "__main__":
    figure(["as_published"], "1_as_published.png", 5.6)
    figure(["drop_identical_double_congruent"], "2_doubled.png", 5.6)
    figure(["proposed"], "3_proposed.png", 5.6)
