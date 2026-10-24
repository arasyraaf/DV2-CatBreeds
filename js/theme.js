const COLOURS = {
  au: "#0072B2",
  my: "#E69F00",
  context: "#BDB6AC",
  coat: { "Short": "#1B7A3E", "Long": "#5C2A4A", "Short or long": "#7A7A1F", "Rex or hairless": "#C2507A" },
  ink: "#2B2622",
  inkSoft: "#6B635B",
  rule: "#E4DED5"
};

const VEGA_CONFIG = {
  background: "#FFFFFF",
  font: "Nunito Sans",
  padding: 8,
  view: { stroke: null },
  title: { font: "Nunito Sans", fontSize: 16, fontWeight: 800, color: COLOURS.ink, anchor: "start" },
  axis: {
    labelFont: "Nunito Sans", titleFont: "Nunito Sans",
    labelFontSize: 12, titleFontSize: 12, titleFontWeight: 600,
    labelLimit: 0, titleLimit: 0,
    labelColor: COLOURS.inkSoft, titleColor: COLOURS.inkSoft,
    gridColor: COLOURS.rule, domainColor: COLOURS.rule, tickColor: COLOURS.rule
  },
  legend: {
    labelFont: "Nunito Sans", titleFont: "Nunito Sans",
    labelFontSize: 12, titleFontSize: 12,
    labelLimit: 0, titleLimit: 0,
    orient: "top"
  },
  text: { font: "Nunito Sans", fontSize: 12, color: COLOURS.ink },
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
