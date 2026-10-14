// World countries (Natural Earth 1:110m via world-atlas) -> data/world_110m.topo.json
const fs = require("fs");
const w = JSON.parse(fs.readFileSync(process.argv[2]));
fs.writeFileSync(process.argv[3], JSON.stringify(w));
console.log((fs.statSync(process.argv[3]).size / 1024).toFixed(0), "KB");
