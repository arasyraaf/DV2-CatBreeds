"""Build chart-ready CSVs from the raw data pack.
Run from the dv2 folder:  python scripts/prep_data.py
"""
import csv, json
from collections import Counter, defaultdict

# ---------- Waffle: 100 squares per country ----------
ORDER = ["Found as a stray", "Shelter or rescue", "Friends or family", "Bought", "Other or not stated"]
rows = list(csv.DictReader(open("data/cat_acquisition.csv", encoding="utf-8")))
pct = defaultdict(dict)
for r in rows:
    pct[r["country"]][r["category"]] = int(r["pct"])
for country, d in pct.items():          # AU sums to 93: the rest is vet/other (README to-do)
    rest = 100 - sum(d.values())
    if rest:
        d["Other or not stated"] = rest
with open("data/waffle_acquisition.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["country", "idx", "col", "row", "category", "pct"])
    for country in ["Australia", "New Zealand", "Malaysia"]:
        i = 0
        for cat in ORDER:
            for _ in range(pct[country].get(cat, 0)):
                # fill column by column so each category reads as a solid block
                w.writerow([country, i, i // 10, i % 10, cat, pct[country][cat]])
                i += 1
        assert i == 100, (country, i)

# (Heatmap and trait data are built by scripts/prep_personality.py from the 67-breed table.)
