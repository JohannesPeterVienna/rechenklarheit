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
// Unsinnige Eingaben müssen abgelehnt werden (Ergebnis mit error-Flag statt Zahl)
const rejects = [
  ["kredit", { amount: -5, rate: 4.5, years: 5 }],
  ["fahrt", { fuel: "fuel", km: -5, trip: 1, cons: 6.5, price: 1.7, people: 1 }],
  ["zins", { start: -100, monthly: 50, rate: 3, years: 10 }],
  ["inflation", { amount: -1000, rate: 2, years: 10 }],
  ["lohn", { dir: "m2h", amount: -3000, hours: 38.5, salaries: 14 }],
];
for (const [k, v] of rejects) { const r = C[k](form(v)); if (!r || r.result !== null) { console.error("FEHLER: nicht abgelehnt", k, v, r && r.result); bad++; } }
// Gegenbeispiele aus der Gegenprüfung (Nov. 2026): RK01 Laufzeit in Monaten, RK02 Eingaben vollständig prüfen
const check = (name, ok, info) => { if (!ok) { console.error("FEHLER", name, info); bad++; } };
{ // RK01: 1,5 Jahre = 18 Monate nach dem Monatsmodell der Seite: 1000 × 1,01^18
  const r = C.zins(form({ start: 1000, monthly: 0, rate: 12, years: "1,5" }));
  const exp = 1000 * Math.pow(1.01, 18);
  check("RK01 Ergebnis 1,5 Jahre", r.result !== null && Math.abs(num(r.result) - exp) < 0.006, r.result);
  check("RK01 Beschriftung", r.label === "nach 1,5 Jahren (18 Monaten)", r.label);
  check("RK01 Tabelle letzte Zeile 1,5", /<td>1,5<\/td><td>[^<]*<\/td><td>[^<]*<\/td><td>1\.196,15/.test(r.extra || ""), "Tabelle passt nicht");
  const w = C.zins(form({ start: 1000, monthly: 0, rate: 12, years: 2 }));
  check("RK01 ganze Jahre", w.label === "nach 2 Jahren" && Math.abs(num(w.result) - 1000 * Math.pow(1.01, 24)) < 0.006, w.label + " " + w.result);
  const odd = C.zins(form({ start: 1000, monthly: 0, rate: 12, years: "1,3" }));
  check("RK01 keine ganzen Monate abgelehnt", odd.result === null && /ganze Monate/.test(odd.note), odd.result);
}
const rejects2 = [
  ["RK02 Startkapital oops", "zins", { start: "oops", monthly: 50, rate: 3, years: 10 }, /Startkapital/],
  ["RK02 Sparrate oops", "zins", { start: 0, monthly: "x", rate: 3, years: 10 }, /Sparrate/],
  ["RK02 ungültiger Wert", "schnitt", { values: "2 invalid 4", weights: "1 2" }, /Wert Nr\. 2/],
  ["RK02 ungültiges Gewicht", "schnitt", { values: "2 3 4", weights: "1 x 2" }, /Gewicht Nr\. 2/],
  ["RK02 Gewichte 0/0", "schnitt", { values: "2 4", weights: "0 0" }, /Summe der Gewichte/],
  ["RK02 negatives Gewicht", "schnitt", { values: "2 4", weights: "-1 2" }, /Gewicht Nr\. 1 ist negativ/],
  ["RK02 Gewichtsanzahl", "schnitt", { values: "2 3 4", weights: "1 2" }, /gleich viele/],
  ["RK02 Strom negative Stunden", "strom", { mode: "watt", watt: 100, hours: -4, days: 365, price: 30 }, /0–24/],
  ["RK02 Strom negative Tage", "strom", { mode: "watt", watt: 100, hours: 4, days: -1, price: 30 }, /0–366/],
  ["RK02 Strom 367 Tage", "strom", { mode: "watt", watt: 100, hours: 4, days: 367, price: 30 }, /0–366/],
  ["RK02 Strom 25 Stunden", "strom", { mode: "watt", watt: 100, hours: 25, days: 365, price: 30 }, /0–24/],
  ["RK02 Rabatt ungültig", "rabatt", { price: 100, r1: "abc", r2: "", skonto: "" }, /Zahlen/],
];
for (const [name, k, v, re] of rejects2) { const r = C[k](form(v)); check(name, r && r.result === null && re.test(r.note || ""), r && (r.result + " / " + r.note)); }
{ // gültige Fälle bleiben gültig
  const g = C.schnitt(form({ values: "2 4", weights: "1 3" })); check("Gewichteter Schnitt 3,5", num(g.result) === 3.5, g.result);
  const g0 = C.schnitt(form({ values: "2 4", weights: "0 1" })); check("Gewicht 0 erlaubt", num(g0.result) === 4, g0.result);
  const m = C.schnitt(form({ values: "2; 1\n3  2 4", weights: "" })); check("Mittelwert ohne Gewichte", num(m.result) === 2.4, m.result);
  const z = C.zins(form({ start: "", monthly: 100, rate: 3, years: 20 })); check("Startkapital leer = 0", Math.abs(num(z.result) - 32830.20) < 0.02, z.result);
  const rb = C.rabatt(form({ price: 100, r1: 10, r2: "", skonto: "" })); check("Rabatt leer = 0", num(rb.result) === 90, rb.result);
}
// Beispiele aus den Erklärtexten (Nov. 2026): Python-Text und Browser-Rechner müssen dasselbe ergeben
const pages = [
  ["Seite Prozent 18 von 240", "percent", { mode: "satz", a: 18, b: 240 }, 7.5],
  ["Seite Prozent Grundwert 45/15", "percent", { mode: "grund", a: 45, b: 15 }, 300],
  ["Seite Prozent 12 % von 450", "percent", { mode: "anteil", a: 450, b: 12 }, 54],
  ["Seite MwSt 49,95 brutto 20 %", "mwst", { dir: "b2n", amount: "49,95", rate: 20 }, 41.63],
  ["Seite MwSt 113 brutto 19 %", "mwst", { dir: "b2n", amount: 113, rate: 19 }, 94.96],
  ["Seite Rabatt Fahrrad", "rabatt", { price: 1299, r1: 15, r2: "", skonto: 3 }, 1071.03],
  ["Seite Zinseszins Formel", "zins", { start: 0, monthly: 100, rate: 3, years: 20 }, 32830.20],
  ["Seite Zinseszins früh", "zins", { start: 0, monthly: 150, rate: 4, years: 40 }, 177294.20],
  ["Seite Zinseszins spät", "zins", { start: 0, monthly: 150, rate: 4, years: 30 }, 104107.41],
  ["Seite Dreisatz Raten", "dreisatz", { a: 6, b: 250, c: 4, kind: "anti" }, 375],
  ["Seite Dreisatz Kaffee", "dreisatz", { a: 400, b: "2,79", c: 1000, kind: "pro" }, 6.975],
  ["Seite Strom Kühlschrank-Label", "strom", { mode: "label", kwh: 150, price: 30 }, 45],
  ["Seite Marge Kalkulation", "marge", { mode: "ekvk", ek: 80, b: "120,96", vat: 20 }, 33.86],
];
for (const [name, k, v, exp] of pages) { const r = C[k](form(v)); check(name, r && r.result !== null && Math.abs(num(r.result) - exp) < 0.011, r && r.result); }
{ const b = C.bruch(form({ a: 84, b: 126, op: "*", c: 1, d: 1 })); check("Seite Bruch 84/126 = 2/3", b.result === "2/3", b.result);
  const m = C.bruch(form({ a: 11, b: 4, op: "*", c: 4, d: 3 })); check("Seite Bruch 11/4 × 4/3 = 11/3", m.result === "11/3", m.result);
  const k = C.kredit(form({ amount: 20000, rate: 4.5, years: 5 })); check("Seite Kredit Zinsen 1. Jahr", /<td>1<\/td><td>825,35/.test(k.extra || ""), "Tilgungsplan Jahr 1"); }
if (bad) process.exit(1); console.log(`Rechner-Test: ${cases.length} Fälle + ${rejects.length} Ablehnungen + ${rejects2.length + 10} Gegenbeispiele + ${pages.length + 3} Seitenbeispiele OK`);
