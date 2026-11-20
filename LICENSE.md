# Rent Calculator

Split rent, utilities (electricity, water, internet) and other shared expenses among flatmates, with itemized per-person amounts and CSV/JSON export.

## Features
- Weighted rent split (bigger room = higher weight)
- Per-expense exclusions (e.g. someone who didn't use groceries)
- Cent-accurate rounding using `Decimal`: shares always sum to the exact bill
- Exports `summary.csv` and `summary.json`

## Run
```
python rent_calculator.py              # interactive
python rent_calculator.py example.json # from file
```
No dependencies, Python 3.8+.
