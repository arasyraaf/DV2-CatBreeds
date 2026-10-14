"""Generate specs/05_radar.vg.json (a Vega spec: Vega-Lite has no radar chart).
The breed dropdowns need the list of names, so the spec is written from the data.
Run from the dv2 folder: python scripts/make_radar_spec.py
"""
import csv, json

names = sorted({r["name"] for r in csv.DictReader(open("data/traits_long.csv", encoding="utf-8"))})
INK, MID, CONTEXT, RULE = "#2B2622", "#6B635B", "#BDB6AC", "#E4DED5"

spec = {
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "description": "Radar chart comparing two breeds' trait scores against the average breed",
  "width": 236, "height": 236, "padding": {"top": 40, "bottom": 40, "left": 128, "right": 128},
  "autosize": {"type": "none"},
  "signals": [
    {"name": "radius", "update": "width / 2"},
    {"name": "breedA", "value": "Persian",
     "bind": {"input": "select", "options": names, "name": "Breed (solid) "}},
    {"name": "breedB", "value": "Abyssinian",
     "bind": {"input": "select", "options": names, "name": "Breed (dashed) "}}
  ],
  "data": [
    {"name": "traits", "url": "data/traits_long.csv",
     "format": {"type": "csv", "parse": {"score": "number", "trait_order": "number"}}},
    {"name": "axes", "source": "traits",
     "transform": [{"type": "aggregate", "groupby": ["trait", "trait_order"],
                    "fields": ["score"], "ops": ["mean"], "as": ["avg"]},
                   {"type": "collect", "sort": {"field": "trait_order"}}]},
    {"name": "avg", "source": "axes"},
    {"name": "a", "source": "traits",
     "transform": [{"type": "filter", "expr": "datum.name === breedA"},
                   {"type": "collect", "sort": {"field": "trait_order"}}]},
    {"name": "b", "source": "traits",
     "transform": [{"type": "filter", "expr": "datum.name === breedB"},
                   {"type": "collect", "sort": {"field": "trait_order"}}]},
    {"name": "rings", "values": [1, 2, 3, 4, 5]}
  ],
  "scales": [
    {"name": "angle", "type": "point", "range": {"signal": "[-PI / 2, 3 * PI / 2]"},
     "padding": 0.5, "domain": {"data": "axes", "field": "trait", "sort": {"field": "trait_order", "op": "min"}}},
    {"name": "r", "type": "linear", "range": {"signal": "[0, radius]"}, "zero": True,
     "domain": [0, 5]}
  ]
}

# Build marks explicitly (clearer than facets): rings as polygons through each axis angle.
marks = []
for level in range(1, 6):
    marks.append({
      "type": "line", "from": {"data": "axes"},
      "encode": {"enter": {
        "interpolate": {"value": "linear-closed"},
        "x": {"signal": f"scale('r', {level}) * cos(scale('angle', datum.trait))"},
        "y": {"signal": f"scale('r', {level}) * sin(scale('angle', datum.trait))"},
        "stroke": {"value": RULE}, "strokeWidth": {"value": 1}}}})
# spokes
marks.append({
  "type": "rule", "from": {"data": "axes"},
  "encode": {"enter": {
    "x": {"value": 0}, "y": {"value": 0},
    "x2": {"signal": "radius * cos(scale('angle', datum.trait))"},
    "y2": {"signal": "radius * sin(scale('angle', datum.trait))"},
    "stroke": {"value": RULE}, "strokeWidth": {"value": 1}}}})
# average breed: light filled area
marks.append({
  "type": "line", "from": {"data": "avg"},
  "encode": {"update": {
    "interpolate": {"value": "linear-closed"},
    "x": {"signal": "scale('r', datum.avg) * cos(scale('angle', datum.trait))"},
    "y": {"signal": "scale('r', datum.avg) * sin(scale('angle', datum.trait))"},
    "fill": {"value": CONTEXT}, "fillOpacity": {"value": 0.35},
    "stroke": {"value": CONTEXT}, "strokeWidth": {"value": 1}},
    "hover": {"fillOpacity": {"value": 0.5}}}})
# breed B dashed, breed A solid (line style + label carry identity, not colour)
for src, dash, colour in [("b", [5, 4], MID), ("a", [], INK)]:
    marks.append({
      "type": "line", "from": {"data": src},
      "encode": {"update": {
        "interpolate": {"value": "linear-closed"},
        "x": {"signal": "scale('r', datum.score) * cos(scale('angle', datum.trait))"},
        "y": {"signal": "scale('r', datum.score) * sin(scale('angle', datum.trait))"},
        "stroke": {"value": colour}, "strokeWidth": {"value": 2.5},
        "strokeDash": {"value": dash}}}})
    marks.append({
      "type": "symbol", "from": {"data": src},
      "encode": {"update": {
        "x": {"signal": "scale('r', datum.score) * cos(scale('angle', datum.trait))"},
        "y": {"signal": "scale('r', datum.score) * sin(scale('angle', datum.trait))"},
        "size": {"value": 60}, "fill": {"value": colour if src == "a" else "#FFFFFF"},
        "stroke": {"value": colour}, "strokeWidth": {"value": 2},
        "tooltip": {"signal": "{'Breed': datum.name, 'Trait': datum.trait, 'Score (1 to 5)': datum.score}"}}}})
# axis labels
marks.append({
  "type": "text", "from": {"data": "axes"},
  "encode": {"enter": {
    "x": {"signal": "(radius + 14) * cos(scale('angle', datum.trait))"},
    "y": {"signal": "(radius + 14) * sin(scale('angle', datum.trait))"},
    "text": {"field": "trait"},
    "align": {"signal": "abs(cos(scale('angle', datum.trait))) < 0.1 ? 'center' : cos(scale('angle', datum.trait)) > 0 ? 'left' : 'right'"},
    "baseline": {"signal": "abs(sin(scale('angle', datum.trait))) < 0.1 ? 'middle' : sin(scale('angle', datum.trait)) > 0 ? 'top' : 'bottom'"},
    "fill": {"value": INK}, "fontSize": {"value": 12}, "fontWeight": {"value": 700},
    "font": {"value": "Nunito Sans"}}}})
# ring value labels (1, 3, 5) along the top spoke
marks.append({
  "type": "text", "from": {"data": "rings"},
  "encode": {"enter": {
    "x": {"value": 4}, "y": {"signal": "-scale('r', datum.data)"},
    "text": {"signal": "datum.data % 2 === 1 ? datum.data : ''"},
    "fill": {"value": MID}, "fontSize": {"value": 10}, "baseline": {"value": "middle"},
    "font": {"value": "Nunito Sans"}}}})

# Draw everything inside one group centred on the chart
spec["marks"] = [{"type": "group",
                  "encode": {"enter": {"x": {"signal": "radius"}, "y": {"signal": "radius"}}},
                  "marks": marks}]
json.dump(spec, open("specs/05_radar.vg.json", "w", encoding="utf-8"), indent=2)
print("specs/05_radar.vg.json with", len(names), "breeds in the dropdowns")
