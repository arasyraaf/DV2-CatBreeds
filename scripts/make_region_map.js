// Cut the Oceania + Southeast Asia countries out of Natural Earth 1:50m (world-atlas)
// and save a small TopoJSON for the page. Run: node make_region_map.js <countries-50m.json> <out.json>
const fs = require("fs");
const { feature } = require("topojson-client");
const { topology } = require("topojson-server");

const IDS = {
  "036": "AUS", "554": "NZL", "360": "IDN", "608": "PHL", "764": "THA", "704": "VNM",
  "458": "MYS", "702": "SGP", "598": "PNG", "626": "TLS", "096": "BRN", "116": "KHM",
  "418": "LAO", "104": "MMR"
};
const world = JSON.parse(fs.readFileSync(process.argv[2]));
const fc = feature(world, world.objects.countries);
fc.features = fc.features
  .filter(f => IDS[f.id])
  .map(f => ({ type: "Feature", id: f.id,
               properties: { name: f.properties.name, iso3: IDS[f.id] },
               geometry: f.geometry }));
const topo = topology({ countries: fc }, 1e5);
fs.writeFileSync(process.argv[3], JSON.stringify(topo));
console.log(fc.features.length, "countries,", (fs.statSync(process.argv[3]).size / 1024).toFixed(0), "KB");
