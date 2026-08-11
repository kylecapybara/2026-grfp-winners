# 2026 NSF GRFP winners

An exploratory analysis of 2026 NSF Graduate Research Fellowship Program awards, with a focus on fields of study and Chemical Engineering institutional pathways.

The published Quarto report is available at <https://kylecapybara.github.io/2026-grfp-winners/>.

## Reproduce the analysis

The public repository intentionally excludes the person-level `awards.csv` source data and the name-bearing Jupyter notebook. With a local copy of `awards.csv`, install the Python dependencies and regenerate the 600-DPI figures:

```bash
python -m pip install -r requirements.txt
python make_visualizations.py
```

Render the report from the committed aggregate tables and figures:

```bash
quarto render
```

The charts use the colorblind-safe Okabe–Ito palette. Every bar chart is exported at 600 DPI with black bar edges.
