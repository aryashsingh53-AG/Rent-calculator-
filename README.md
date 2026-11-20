# Rent Calculator

Split rent, utilities (electricity, water, internet) and other shared expenses among flatmates, with itemized per-person amounts and CSV/JSON export.

## Features
- Weighted rent split (bigger room = higher weight)
- Per-expense exclusions (e.g. someone who didn't use groceries)
- Cent-accurate rounding: shares always sum to the exact bill
- Exports `summary.csv` and `summary.json`

## Run (Python)
```
python rent_calculator.py              # interactive
python rent_calculator.py example.json # from file
```
No dependencies, Python 3.8+.

## Web version
Open `index.html` in a browser, or host it free with GitHub Pages
(repo Settings → Pages → Deploy from branch → `main` / root).
Live URL: https://aryashsingh53-ag.github.io/Rent-calculator-/
