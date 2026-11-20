"""Rent Calculator: split rent, utilities and shared expenses among flatmates.

Usage:
    python rent_calculator.py            # interactive
    python rent_calculator.py data.json  # from a JSON file (see example.json)
Exports summary.csv and summary.json after each run.
"""
import csv
import json
import sys
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def money(x):
    return Decimal(str(x)).quantize(CENT, rounding=ROUND_HALF_UP)


def split(total, weights):
    """Split total by weights, to the cent, so shares always add up exactly."""
    total = money(total)
    wsum = sum(weights.values())
    shares = {n: money(total * w / wsum) for n, w in weights.items()}
    diff = total - sum(shares.values())
    for name in list(shares)[: int(abs(diff / CENT))]:
        shares[name] += CENT if diff > 0 else -CENT
    return shares


def calculate(members, rent, expenses):
    """members: {name: rent_weight}; expenses: [{name, amount, exclude: [names]}]."""
    rows = {n: {"Rent": Decimal(0)} for n in members}
    for n, v in split(rent, members).items():
        rows[n]["Rent"] = v
    for e in expenses:
        included = {n: 1 for n in members if n not in e.get("exclude", [])}
        for n, v in split(e["amount"], included).items():
            rows[n][e["name"]] = v
    for r in rows.values():
        r["Total"] = sum(r.values())
    return rows


def show(rows):
    cols = list(next(iter(rows.values())).keys())
    print(f"\n{'Name':<12}" + "".join(f"{c:>12}" for c in cols))
    print("-" * (12 + 12 * len(cols)))
    for n, r in rows.items():
        print(f"{n:<12}" + "".join(f"{r.get(c, Decimal(0)):>12.2f}" for c in cols))
    grand = sum(r["Total"] for r in rows.values())
    print(f"\nGrand total: {grand:.2f}")


def export(rows):
    cols = sorted({c for r in rows.values() for c in r}, key=lambda c: (c == "Total", c != "Rent", c))
    with open("summary.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Name"] + cols)
        for n, r in rows.items():
            w.writerow([n] + [f"{r.get(c, 0):.2f}" for c in cols])
    with open("summary.json", "w") as f:
        json.dump({n: {c: float(v) for c, v in r.items()} for n, r in rows.items()}, f, indent=2)
    print("Exported summary.csv and summary.json")


def ask_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Enter a number.")


def interactive():
    members = {}
    print("Enter flatmates (blank name to finish).")
    while True:
        name = input("Name: ").strip()
        if not name:
            if members:
                break
            continue
        members[name] = Decimal(str(ask_float(f"  Rent weight for {name} (1 = equal share, e.g. 1.2 = bigger room): ")))
    rent = ask_float("Monthly rent: ")
    expenses = []
    for item in ("Electricity", "Water", "Internet"):
        expenses.append({"name": item, "amount": ask_float(f"{item} bill: ")})
    print("Other shared expenses (blank name to finish).")
    while True:
        name = input("Expense: ").strip()
        if not name:
            break
        exp = {"name": name, "amount": ask_float("  Amount: ")}
        ex = input("  Exclude who? (comma-separated, or blank): ").strip()
        exp["exclude"] = [x.strip() for x in ex.split(",") if x.strip()]
        expenses.append(exp)
    return members, rent, expenses


def from_file(path):
    with open(path) as f:
        d = json.load(f)
    members = {n: Decimal(str(w)) for n, w in d["members"].items()}
    return members, d["rent"], d.get("expenses", [])


if __name__ == "__main__":
    members, rent, expenses = from_file(sys.argv[1]) if len(sys.argv) > 1 else interactive()
    rows = calculate(members, rent, expenses)
    show(rows)
    export(rows)
