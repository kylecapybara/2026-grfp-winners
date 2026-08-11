# 2026 NSF GRFP winners

An exploratory analysis of 2026 NSF Graduate Research Fellowship Program awards, with a focus on fields of study and Chemical Engineering institutional pathways.

The published Quarto report is available at <https://kylecapybara.github.io/2026-grfp-winners/>.

## Reproduce the analysis

The public repository intentionally excludes the person-level `awards.csv` source data. The cleared-output Jupyter notebook contains the full analysis and visualization workflow. With a local copy of `awards.csv`, install the Python dependencies and execute the notebook to regenerate the aggregate tables and 600-DPI figures:

```bash
python -m pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace grfp.ipynb
```

Render the report from the committed aggregate tables and figures:

```bash
quarto render
```

