"""Merge trait scores (old TheCatAPI, via Internet Archive snapshot 1 Apr 2026)
with coat group, lifespan and weight from the current TheCatAPI breed list.
Run from the dv2 folder: python scripts/merge_traits.py  ->  data/breeds_master.csv
"""
import csv, json

TRAITS = ["adaptability", "affection_level", "child_friendly", "dog_friendly",
          "energy_level", "grooming", "health_issues", "intelligence",
          "shedding_level", "social_needs", "stranger_friendly", "vocalisation"]
FLAGS = ["hairless", "rex", "short_legs", "hypoallergenic", "natural", "rare", "lap"]
COAT = {"Short-haired": "Short", "Long-haired": "Long", "Semi-longhair": "Long",
        "Short/Long-hair": "Short or long", "Short/Medium-hair": "Short or long",
        "Rex": "Curly (rex)", "Hairless": "Hairless", "Hybrid": "Hybrid"}
FIX_CC = {"SP": "SG"}

old = json.load(open("data/catapi_breeds_archived_traits.json", encoding="utf-8"))
new = {b["id"]: b for b in json.load(open("data/catapi_breeds.json", encoding="utf-8"))}

def rng(s):
    try:
        lo, hi = [float(x) for x in str(s).replace("–", "-").split("-")]
        return lo, hi
    except Exception:
        return None, None

with open("data/breeds_master.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "name", "origin", "country_code", "coat", "life_min", "life_max",
                "weight_kg_min", "weight_kg_max", "temperament"] + TRAITS + FLAGS)
    for b in old:
        n = new[b["id"]]                     # current record: coat group, lifespan, weight
        lmin, lmax = rng(n.get("life_span"))
        wmin, wmax = rng((n.get("weight") or {}).get("metric"))
        w.writerow([b["id"], b["name"], n.get("origin"),
                    FIX_CC.get(n.get("country_code"), n.get("country_code")),
                    COAT.get(n.get("breed_group"), "Unclassified"),
                    lmin, lmax, wmin, wmax, n.get("temperament")]
                   + [b[t] for t in TRAITS] + [b.get(x) for x in FLAGS])
print(len(old), "breeds -> data/breeds_master.csv")
