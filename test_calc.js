// Automatischer Test: rechnet Beispiele mit den echten Rechner-Funktionen nach.
const fs = require("fs");
global.window = {}; global.location = { search: "" }; global.history = { replaceState() {} };
global.document = { readyState: "complete", querySelector: () => null, querySelectorAll: () => [], addEventListener() {} };
eval(fs.readFileSync(__dirname + "/assets/calc.js", "utf8"));
const C = window.RK_CALC;
const form = (vals) => ({ elements: Object.fromEntries(Object.entries(vals).map(([k, v]) => [k, { value: String(v) }])), dataset: {}, querySelector: () => null, querySelectorAll: () => [] });
const num = s => Number(String(s).replace(/[^\d,-]/g, "").replace(",", "."));
const cases = [
  ["percent", { mode: "anteil", a: 80, b: 15 }, 12],
  ["percent", { mode: "veraenderung", a: 80, b: 96 }, 20],
  ["kredit", { amount: 20000, rate: 4.5, years: 5 }, 372.86],
  ["inflation", { amount: 1000, rate: 2, years: 10 }, 820.35],
  ["strom", { mode: "watt", watt: 100, hours: 4, days: 365, price: 30 }, 43.8],
  ["fahrt", { fuel: "fuel", km: 230, trip: 2, cons: 6.5, price: 1.7, people: 3 }, 16.94],
  ["tip", { bill: 87.4, pct: 10, round: 1, people: 4 }, 24.25],
  ["marge", { mode: "span", ek: 60, b: 40, vat: 20 }, 100],
  ["dreisatz", { a: 4, b: 300, c: 6, kind: "prop" }, 450],
  ["lohn", { dir: "m2h", amount: 3000, hours: 38.5, salaries: 14 }, 20.98],
];
let bad = 0;
for (const [k, v, exp] of cases) {
  const r = C[k](form(v)); const got = num(r.result);
  if (Math.abs(got - exp) > 0.011) { console.error("FEHLER", k, v, "erwartet", exp, "erhalten", r.result); bad++; }
}
if (bad) process.exit(1); console.log(`Rechner-Test: ${cases.length} Fälle OK`);
