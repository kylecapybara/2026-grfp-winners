from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


DATA_PATH = Path("awards.csv")
FIGURE_DIR = Path("figures")
FIELD = "Engineering - Chemical Engineering"

# Okabe-Ito colorblind-safe palette.
COLORS = {
    "orange": "#E69F00",
    "sky_blue": "#56B4E9",
    "bluish_green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "reddish_purple": "#CC79A7",
    "black": "#000000",
}


def wrap_labels(values, width=34):
    return [textwrap.fill(str(value), width=width) for value in values]


def finish_figure(fig, path):
    fig.savefig(
        path,
        dpi=600,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)


def style_axis(ax, axis="x"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis=axis, color="#D9E2E8", linewidth=0.7, alpha=0.8)
    ax.set_axisbelow(True)


def field_breakdown(df):
    return (
        df.assign(
            same_institution=df["Current Institution"].eq(
                df["Baccalaureate Institution"]
            ),
            different_institution=(
                df["Current Institution"].notna()
                & df["Current Institution"].ne(df["Baccalaureate Institution"])
            ),
        )
        .groupby("Field of Study", dropna=False)
        .agg(
            total_awards=("Name", "size"),
            same_institution=("same_institution", "sum"),
            different_institution=("different_institution", "sum"),
        )
        .reset_index()
        .sort_values(["total_awards", "Field of Study"], ascending=[False, True])
    )


def plot_top_fields(field_counts):
    top = field_counts.head(15).sort_values("total_awards")
    fig, ax = plt.subplots(figsize=(10.5, 8.5), layout="constrained")
    bars = ax.barh(
        wrap_labels(top["Field of Study"]),
        top["total_awards"],
        color=COLORS["vermillion"],
        edgecolor=COLORS["black"],
        linewidth=0.8,
    )
    ax.bar_label(bars, padding=4, fontsize=8.5)
    ax.set_title("Fields receiving the most 2026 NSF GRFP awards", loc="left", weight="bold")
    ax.set_xlabel("Number of awards")
    ax.set_ylabel("")
    ax.set_xlim(0, top["total_awards"].max() * 1.12)
    style_axis(ax)
    finish_figure(fig, FIGURE_DIR / "top-fields-total-awards.png")


def plot_field_pathways(field_counts):
    top = field_counts.head(12).sort_values("total_awards")
    y = np.arange(len(top))
    height = 0.34
    fig, ax = plt.subplots(figsize=(10.5, 8.3), layout="constrained")
    same = ax.barh(
        y - height / 2,
        top["same_institution"],
        height,
        label="Senior Undergraduates",
        color=COLORS["orange"],
        edgecolor=COLORS["black"],
        linewidth=0.8,
    )
    different = ax.barh(
        y + height / 2,
        top["different_institution"],
        height,
        label="1st year PhD students",
        color=COLORS["sky_blue"],
        edgecolor=COLORS["black"],
        linewidth=0.8,
    )
    ax.bar_label(same, padding=3, fontsize=8)
    ax.bar_label(different, padding=3, fontsize=8)
    ax.set_yticks(y, wrap_labels(top["Field of Study"]))
    ax.set_title(
        "The proportion of senior undergraduates is not constant among top-awarded fields",
        loc="left",
        weight="bold",
    )
    ax.set_xlabel("Number of awards")
    ax.set_ylabel("")
    ax.legend(frameon=False, loc="lower right")
    ax.set_xlim(0, max(top["same_institution"].max(), top["different_institution"].max()) * 1.16)
    style_axis(ax)
    finish_figure(fig, FIGURE_DIR / "top-fields-institutional-pathways.png")


def plot_chemical_engineering_phd_institutions(df):
    counts = (
        df.loc[
            (df["Field of Study"] == FIELD)
            & df["Current Institution"].notna()
            & df["Current Institution"].ne(df["Baccalaureate Institution"]),
            "Current Institution",
        ]
        .value_counts()
        .head(15)
        .sort_values()
    )
    fig, ax = plt.subplots(figsize=(10, 7.5), layout="constrained")
    bars = ax.barh(
        wrap_labels(counts.index, width=38),
        counts.values,
        color=COLORS["bluish_green"],
        edgecolor=COLORS["black"],
        linewidth=0.8,
    )
    ax.bar_label(bars, padding=4, fontsize=8.5)
    ax.set_title(
        "Leading institutions for Chemical Engineering first-year PhD winners",
        loc="left",
        weight="bold",
    )
    ax.set_xlabel("Number of winners")
    ax.set_ylabel("")
    ax.set_xlim(0, counts.max() * 1.18)
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    style_axis(ax)
    finish_figure(
        fig,
        FIGURE_DIR / "chemical-engineering-first-year-phd-institutions.png",
    )


def main():
    FIGURE_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(DATA_PATH, encoding="latin1")
    counts = field_breakdown(df)
    plot_top_fields(counts)
    plot_field_pathways(counts)
    plot_chemical_engineering_phd_institutions(df)


if __name__ == "__main__":
    main()
