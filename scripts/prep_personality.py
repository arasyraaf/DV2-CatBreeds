"""Chart data for the personality section, all from data/breeds_master.csv (67 breeds).
Run from the dv2 folder: python scripts/prep_personality.py
"""
import csv
from collections import Counter, defaultdict

# Coat groups used on the whole page (4 groups -> 4 fixed colours in the design system).
# The 2 hybrids (Bengal, Savannah) both have short coats, so they join "Short".
COAT4 = {"Short": "Short", "Hybrid": "Short", "Long": "Long", "Short or long": "Short or long",
         "Curly (rex)": "Rex or hairless", "Hairless": "Rex or hairless"}
# Traits that actually vary between breeds, in display order, with plain-English labels
TRAITS = [("energy_level", "Energy"), ("social_needs", "Needs company"),
          ("stranger_friendly", "Stranger-friendly"), ("vocalisation", "Talkative"),
          ("intelligence", "Intelligence"), ("grooming", "Grooming needs"),
          ("shedding_level", "Shedding"), ("health_issues", "Health issues")]

rows = list(csv.DictReader(open("data/breeds_master.csv", encoding="utf-8")))
for r in rows:
    r["coat4"] = COAT4[r["coat"]]

# Long format: one row per breed x trait
with open("data/traits_long.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["name", "coat", "origin", "trait", "trait_order", "score"])
    for r in rows:
        for i, (key, label) in enumerate(TRAITS):
            w.writerow([r["name"], r["coat4"], r["origin"], label, i, int(r[key])])

# Temperament
WORDS = ["Affectionate", "Intelligent", "Playful", "Social", "Active", "Gentle",
         "Loyal", "Curious", "Friendly", "Calm", "Independent", "Quiet"]
n = Counter(r["coat4"] for r in rows)
hits = defaultdict(Counter)
for r in rows:
    words = {x.strip().title() for x in r["temperament"].split(",")}
    for word in WORDS:
        hits[r["coat4"]][word] += word in words
with open("data/heatmap_temperament.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["group", "group_label", "n", "word", "count", "pct"])
    for g in ["Short", "Long", "Short or long", "Rex or hairless"]:
        for word in WORDS:
            w.writerow([g, f"{g} ({n[g]})", n[g], word, hits[g][word],
                        round(100 * hits[g][word] / n[g])])
print(dict(n))
for g in ["Short", "Long", "Short or long", "Rex or hairless"]:
    print(f"{g:16}", " ".join(f"{word[:5]}={round(100*hits[g][word]/n[g]):>3}" for word in WORDS))
