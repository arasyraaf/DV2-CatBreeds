"""Chart data for origin map, weight boxplot and Google Trends charts.
Run from the dv2 folder: python scripts/prep_mvp.py
"""
import csv
from collections import Counter, defaultdict

COAT4 = {"Short": "Short", "Hybrid": "Short", "Long": "Long", "Short or long": "Short or long",
         "Curly (rex)": "Rex or hairless", "Hairless": "Rex or hairless"}
breeds = list(csv.DictReader(open("data/breeds_master.csv", encoding="utf-8")))

# Origin symbol map: breeds per country of origin (67 breeds)
ref = {r["country_code"]: r for r in csv.DictReader(open("data/breed_origin_counts.csv", encoding="utf-8"))}
n = Counter(); names = defaultdict(list)
for b in breeds:
    cc = b["country_code"]
    n[cc] += 1; names[cc].append(b["name"])
with open("data/origin_counts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["country_code", "country", "lat", "lon", "n_breeds", "breeds"])
    for cc, k in n.most_common():
        r = ref.get(cc)
        if not r:
            print("MISSING centroid for", cc, names[cc]); continue
        w.writerow([cc, r["country"], r["lat"], r["lon"], k, "; ".join(sorted(names[cc]))])
print("origins:", n.most_common(8))

# Weight by coat group (mid-point of each breed's weight range)
with open("data/weight_by_coat.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["name", "coat", "weight_mid", "weight_min", "weight_max"])
    for b in breeds:
        if b["weight_kg_min"] and b["weight_kg_max"]:
            lo, hi = float(b["weight_kg_min"]), float(b["weight_kg_max"])
            w.writerow([b["name"], COAT4[b["coat"]], round((lo + hi) / 2, 2), lo, hi])

# Google Trends: share of the five breeds, per 12-month window
def load(path):
    rows = list(csv.reader(open(path, encoding="utf-8")))
    head = [h.split(":")[0].replace(" cat", "") for h in rows[2][1:]]
    data = [(r[0], [float(x) for x in r[1:]]) for r in rows[3:] if r and r[0]]
    return head, data

windows = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
slope, bump = [], []
for code, country in (("au", "Australia"), ("my", "Malaysia")):
    head, data = load(f"data/trends_{code}.csv")
    N, W = len(data), 52
    for k, label in enumerate(windows):
        seg = data[N - (5 - k) * W: N - (4 - k) * W] if k < 4 else data[N - W:]
        avg = [sum(x[1][i] for x in seg) / len(seg) for i in range(5)]
        tot = sum(avg)
        order = sorted(range(5), key=lambda i: -avg[i])
        for rank, i in enumerate(order, 1):
            row = {"country": country, "breed": head[i], "window": label,
                   "share": round(100 * avg[i] / tot, 1), "rank": rank}
            bump.append(row)
            if label == windows[-1]:
                slope.append(row)
for name, rows in (("trends_bump.csv", bump), ("trends_slope.csv", slope)):
    with open("data/" + name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("trends rows:", len(bump), len(slope))
