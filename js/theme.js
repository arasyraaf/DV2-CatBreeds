const COLOURS = {
  au: "#0072B2",
  my: "#E69F00",
  context: "#BDB6AC",
  coat: { "Short": "#009E73", "Long": "#CC79A7", "Short or long": "#882255", "Rex or hairless": "#7B5EA7" },
  accent: "#D55E00",
  ink: "#2B2622",
  inkSoft: "#6B635B",
  rule: "#E4DED5"
};

// Reusable scale snippets. Use these in specs instead of retyping colours.
// e.g. "color": {"field": "coat", "scale": COAT_SCALE}
const COAT_SCALE = { domain: Object.keys(COLOURS.coat), range: Object.values(COLOURS.coat) };
const COUNTRY_SCALE = { domain: ["Australia", "Malaysia"], range: [COLOURS.au, COLOURS.my] };

const VEGA_CONFIG = {
  background: "#FFFFFF",
  font: "Nunito Sans",
  padding: 8,
  view: { stroke: null },
  title: { font: "Fraunces", fontSize: 16, fontWeight: 600, color: COLOURS.ink, anchor: "start" },
  axis: {
    labelFont: "Nunito Sans", titleFont: "Nunito Sans",
    labelFontSize: 12, titleFontSize: 12, titleFontWeight: 600,
    labelColor: COLOURS.inkSoft, titleColor: COLOURS.inkSoft,
    gridColor: COLOURS.rule, domainColor: COLOURS.rule, tickColor: COLOURS.rule
  },
  legend: {
    labelFont: "Nunito Sans", titleFont: "Nunito Sans",
    labelFontSize: 12, titleFontSize: 12,
    labelLimit: 0,
    orient: "top"
  },
  text: { font: "Nunito Sans", fontSize: 12, color: COLOURS.ink },
  range: {
    // Sequential maps: one warm single-hue ramp for every quantitative choropleth
    ramp: { scheme: "browns" }
  },
  mark: { color: COLOURS.context }
};

function embedChart(selector, specPath) {
  return vegaEmbed(selector, specPath, {
    config: VEGA_CONFIG,
    actions: false,
    renderer: "svg"
  }).catch(err => {
    document.querySelector(selector).textContent = "Chart failed to load: " + specPath;
    console.error(err);
  });
}
