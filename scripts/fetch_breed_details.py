"""Fetch the FULL record for every breed from TheCatAPI (one call per breed),
so we get the 1-5 trait scores that the /v1/breeds list leaves out.

Run from the dv2 folder (Python 3, no extra packages needed):
  Windows PowerShell:  $env:CATAPI_KEY="your_key"; python scripts/fetch_breed_details.py
  macOS/Linux:         CATAPI_KEY=your_key python3 scripts/fetch_breed_details.py

Reads:  data/catapi_breeds.json            (the list you already downloaded)
Writes: data/catapi_breeds_full.json       (raw per-breed records, source of truth)
        data/breeds_traits_full.csv        (one row per breed, traits filled in)
"""
import csv, json, os, sys, time, urllib.request, urllib.error

KEY = os.environ.get("CATAPI_KEY")
if not KEY:
    sys.exit("Set CATAPI_KEY first (see the top of this file).")

TRAITS = ["adaptability", "affection_level", "child_friendly", "dog_friendly",
          "energy_level", "grooming", "health_issues", "intelligence",
          "shedding_level", "social_needs", "stranger_friendly", "vocalisation"]
FLAGS = ["hairless", "natural", "rare", "rex", "suppressed_tail", "short_legs",
         "hypoallergenic", "experimental", "indoor", "lap"]
FIX_CC = {"SP": "SG"}  # TheCatAPI uses SP for Singapore; ISO is SG

def get(breed_id, tries=3):
    req = urllib.request.Request(
        f"https://api.thecatapi.com/v1/breeds/{breed_id}",
        headers={"x-api-key": KEY, "User-Agent": "FIT3179-student-project"})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:            # rate limited: wait and retry
                time.sleep(5 * (attempt + 1))
                continue
            print(f"  {breed_id}: HTTP {e.code}")
            return None
        except Exception as e:
            print(f"  {breed_id}: {e}")
            time.sleep(2)
    return None

def rng(s):
    """'14 - 15' -> (14.0, 15.0); (None, None) if unparseable."""
    try:
        lo, hi = [float(x) for x in str(s).replace("–", "-").split("-")]
        return lo, hi
    except Exception:
        return None, None

ids = [b["id"] for b in json.load(open("data/catapi_breeds.json", encoding="utf-8"))]
print(f"Fetching {len(ids)} breeds...")

full = []
for i, bid in enumerate(ids, 1):
    rec = get(bid)
    if rec:
        full.append(rec)
    if i % 10 == 0:
        print(f"  {i}/{len(ids)}")
    time.sleep(0.3)

json.dump(full, open("data/catapi_breeds_full.json", "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)

cols = (["id", "name", "origin", "country_code", "breed_group", "life_min", "life_max",
         "weight_kg_min", "weight_kg_max", "temperament"] + TRAITS + FLAGS)
with open("data/breeds_traits_full.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(cols)
    for b in full:
        lmin, lmax = rng(b.get("life_span"))
        wmin, wmax = rng((b.get("weight") or {}).get("metric"))
        cc = FIX_CC.get(b.get("country_code"), b.get("country_code"))
        w.writerow([b.get("id"), b.get("name"), b.get("origin"), cc, b.get("breed_group"),
                    lmin, lmax, wmin, wmax, b.get("temperament")]
                   + [b.get(t) for t in TRAITS] + [b.get(x) for x in FLAGS])

# ---- Report: did we actually get trait scores? ----
with_traits = sum(1 for b in full if b.get("energy_level") is not None)
print(f"\nDone: {len(full)}/{len(ids)} breeds fetched; {with_traits} have trait scores.")
if full and with_traits == 0:
    print("No trait scores came back. Keys in a record were:")
    print(sorted(full[0].keys()))
print("Send me data/catapi_breeds_full.json and data/breeds_traits_full.csv")
