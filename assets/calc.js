/* Rechenklarheit — alle Rechner laufen im Browser. Jeder Rechner liefert Ergebnis und Rechenweg. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const nf = (x, d = 2) => Number.isFinite(x) ? new Intl.NumberFormat("de-DE", { maximumFractionDigits: d, minimumFractionDigits: 0 }).format(x) : "–";
  const eur = x => Number.isFinite(x) ? new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" }).format(x) : "–";
  const pc = (x, d = 2) => `${nf(x, d)} %`;
  const num = v => { if (v === undefined || v === null) return NaN; const s = String(v).trim().replace(/\s/g, "").replace(/\.(?=\d{3}(\D|$))/g, "").replace(",", "."); return s === "" ? NaN : Number(s); };
  const val = (f, n) => num(f.elements[n]?.value);
  const sel = (f, n) => f.elements[n]?.value;
  const line = (t) => `<li>${t}</li>`;
  const bad = msg => ({ result: null, note: msg });

  const C = {};

  C.percent = f => {
    const mode = sel(f, "mode");
    const a = val(f, "a"), b = val(f, "b");
    $$("[data-mode-label]", f).forEach(el => { el.textContent = el.dataset[mode] || el.textContent; });
    if (!Number.isFinite(a) || !Number.isFinite(b)) return bad("Bitte beide Felder ausfüllen.");
    switch (mode) {
      case "anteil": { const w = a * b / 100; return { result: nf(w, 4), label: `${pc(b)} von ${nf(a, 4)}`, steps: [line(`Prozentwert = Grundwert × Prozentsatz ÷ 100`), line(`= ${nf(a, 4)} × ${nf(b, 4)} ÷ 100`), line(`= <mark>${nf(w, 4)}</mark>`)] }; }
      case "satz": { if (b === 0) return bad("Der Grundwert darf nicht 0 sein."); const p = a / b * 100; return { result: pc(p, 4), label: `${nf(a, 4)} von ${nf(b, 4)}`, steps: [line(`Prozentsatz = Prozentwert ÷ Grundwert × 100`), line(`= ${nf(a, 4)} ÷ ${nf(b, 4)} × 100`), line(`= <mark>${pc(p, 4)}</mark>`)] }; }
      case "grund": { if (b === 0) return bad("Der Prozentsatz darf nicht 0 sein."); const g = a / b * 100; return { result: nf(g, 4), label: `${nf(a, 4)} sind ${pc(b)} von …`, steps: [line(`Grundwert = Prozentwert ÷ Prozentsatz × 100`), line(`= ${nf(a, 4)} ÷ ${nf(b, 4)} × 100`), line(`= <mark>${nf(g, 4)}</mark>`)] }; }
      case "veraenderung": { if (a === 0) return bad("Der alte Wert darf nicht 0 sein – von 0 aus gibt es keine prozentuale Veränderung."); const d = b - a, p = d / a * 100; return { result: (p > 0 ? "+" : "") + pc(p), label: `von ${nf(a, 4)} auf ${nf(b, 4)}`, steps: [line(`Differenz = neu − alt = ${nf(b, 4)} − ${nf(a, 4)} = ${nf(d, 4)}`), line(`Veränderung = Differenz ÷ alter Wert × 100`), line(`= ${nf(d, 4)} ÷ ${nf(a, 4)} × 100 = <mark>${(p > 0 ? "+" : "") + pc(p)}</mark>`), line(`Basis ist immer der <b>alte</b> Wert. Zurück auf ${nf(a, 4)} wären es ${pc(-d / b * 100)}.`)] }; }
      case "rabatt": { const e = a * (1 - b / 100); return { result: eur(e), label: `${eur(a)} minus ${pc(b)}`, steps: [line(`Ersparnis = ${eur(a)} × ${nf(b, 4)} ÷ 100 = ${eur(a - e)}`), line(`Endpreis = ${eur(a)} − ${eur(a - e)} = <mark>${eur(e)}</mark>`), line(`Kurzweg: ${eur(a)} × (1 − ${nf(b / 100, 4)}) = ${eur(e)}`)] }; }
      case "ursprung": { if (b >= 100) return bad("Ein Rabatt von 100 % oder mehr hat keinen Ausgangspreis."); const o = a / (1 - b / 100); return { result: eur(o), label: `${eur(a)} nach ${pc(b)} Rabatt`, steps: [line(`Der Endpreis entspricht ${pc(100 - b)} des Ausgangspreises.`), line(`Ausgangspreis = ${eur(a)} ÷ ${nf(1 - b / 100, 4)}`), line(`= <mark>${eur(o)}</mark>`), line(`Achtung: ${pc(b)} auf den Endpreis aufschlagen ergibt ${eur(a * (1 + b / 100))} – das ist <b>falsch</b>.`)] }; }
    }
  };

  C.mwst = f => {
    const amt = val(f, "amount"); let rate = num(sel(f, "rate"));
    if (sel(f, "rate") === "custom") rate = val(f, "custom");
    const dir = sel(f, "dir");
    if (!Number.isFinite(amt) || !Number.isFinite(rate)) return bad("Betrag und Steuersatz eingeben.");
    const q = 1 + rate / 100;
    if (dir === "n2b") { const t = amt * rate / 100; return { result: eur(amt + t), label: `brutto bei ${pc(rate, 1)}`, steps: [line(`Steuer = ${eur(amt)} × ${nf(rate, 2)} ÷ 100 = ${eur(t)}`), line(`Brutto = ${eur(amt)} + ${eur(t)} = <mark>${eur(amt + t)}</mark>`)] }; }
    const n = amt / q, t = amt - n;
    return { result: eur(n), label: `netto bei ${pc(rate, 1)}`, steps: [line(`Netto = Brutto ÷ ${nf(q, 4)}`), line(`= ${eur(amt)} ÷ ${nf(q, 4)} = <mark>${eur(n)}</mark>`), line(`Enthaltene Steuer = ${eur(amt)} − ${eur(n)} = ${eur(t)}`), line(`Nicht ${pc(rate, 1)} vom Bruttobetrag abziehen – das ergäbe ${eur(amt * (1 - rate / 100))} und wäre zu wenig.`)] };
  };

  C.rabatt = f => {
    const p = val(f, "price"); const r1 = val(f, "r1") || 0, r2 = val(f, "r2") || 0, sk = val(f, "skonto") || 0;
    if (!Number.isFinite(p)) return bad("Bitte den Preis eingeben.");
    let x = p; const st = [line(`Ausgangspreis: ${eur(p)}`)];
    for (const [r, n] of [[r1, "1. Rabatt"], [r2, "2. Rabatt"], [sk, "Skonto"]]) { if (!r) continue; const nx = x * (1 - r / 100); st.push(line(`${n} ${pc(r)}: ${eur(x)} × ${nf(1 - r / 100, 4)} = ${eur(nx)}`)); x = nx; }
    const tot = (1 - x / p) * 100;
    st.push(line(`Endpreis: <mark>${eur(x)}</mark>`));
    st.push(line(`Gesamtersparnis: ${eur(p - x)} = <b>${pc(tot)}</b>${(r1 && r2) ? ` – nicht ${pc(r1 + r2 + sk)}, weil jeder Rabatt auf den schon reduzierten Preis wirkt` : ""}`));
    return { result: eur(x), label: `Ersparnis ${pc(tot)}`, steps: st };
  };

  C.zins = f => {
    const k0 = val(f, "start") || 0, rate = val(f, "monthly") || 0, p = val(f, "rate"), n = val(f, "years");
    if (!Number.isFinite(p) || !Number.isFinite(n) || n <= 0 || n > 80) return bad("Zinssatz und Laufzeit (1–80 Jahre) eingeben.");
    const i = p / 100 / 12; let k = k0, paid = k0; const rows = [];
    for (let y = 1; y <= n; y++) {
      for (let m = 0; m < 12; m++) { k = k * (1 + i) + rate; paid += rate; }
      rows.push([y, paid, k - paid, k]);
    }
    const int = k - paid;
    const table = `<div class="scroll"><table class="tbl small"><thead><tr><th>Jahr</th><th>Eingezahlt</th><th>Zinsen gesamt</th><th>Kapital</th></tr></thead><tbody>${rows.map(r => `<tr><td>${r[0]}</td><td>${eur(r[1])}</td><td>${eur(r[2])}</td><td>${eur(r[3])}</td></tr>`).join("")}</tbody></table></div>`;
    return { result: eur(k), label: `nach ${nf(n, 0)} Jahren`, steps: [line(`Monatszins = ${pc(p)} ÷ 12 = ${pc(p / 12, 4)}`), line(`Jeden Monat: Kapital × ${nf(1 + i, 6)} + ${eur(rate)} Sparrate`), line(`Eingezahlt: ${eur(paid)} · davon Zinsen: <mark>${eur(int)}</mark>`), line(`Zinsen machen ${pc(paid ? int / k * 100 : 0, 1)} des Endkapitals aus.`)], extra: table };
  };

  C.kredit = f => {
    const K = val(f, "amount"), p = val(f, "rate"), n = val(f, "years");
    if (!Number.isFinite(K) || !Number.isFinite(p) || !Number.isFinite(n) || n <= 0 || n > 50) return bad("Betrag, Sollzins und Laufzeit (bis 50 Jahre) eingeben.");
    const m = Math.round(n * 12), i = p / 100 / 12;
    const a = i === 0 ? K / m : K * i / (1 - Math.pow(1 + i, -m));
    const total = a * m, interest = total - K;
    let rest = K; const rows = [];
    for (let y = 1; y <= Math.ceil(m / 12); y++) {
      let zi = 0, ti = 0;
      for (let k = 0; k < 12 && rest > 0.005; k++) { const z = rest * i; const t = Math.min(a - z, rest); zi += z; ti += t; rest -= t; }
      rows.push([y, zi, ti, Math.max(rest, 0)]);
    }
    const table = `<div class="scroll"><table class="tbl small"><thead><tr><th>Jahr</th><th>Zinsen</th><th>Tilgung</th><th>Restschuld</th></tr></thead><tbody>${rows.map(r => `<tr><td>${r[0]}</td><td>${eur(r[1])}</td><td>${eur(r[2])}</td><td>${eur(r[3])}</td></tr>`).join("")}</tbody></table></div>`;
    return { result: eur(a), label: "Monatsrate", steps: [line(`Monatszins i = ${pc(p)} ÷ 12 = ${nf(i * 100, 4)} %`), line(`Rate = Kredit × i ÷ (1 − (1 + i)<sup>−${m}</sup>)`), line(`= <mark>${eur(a)}</mark> pro Monat, ${m} Raten`), line(`Zurückgezahlt gesamt: ${eur(total)} · Zinskosten: <b>${eur(interest)}</b>`), line(`Ohne Gebühren gerechnet. Der Effektivzins im Angebot enthält zusätzlich Kosten wie Bearbeitungsgebühren.`)], extra: table };
  };

  C.inflation = f => {
    const a = val(f, "amount"), r = val(f, "rate"), n = val(f, "years");
    if (!Number.isFinite(a) || !Number.isFinite(r) || !Number.isFinite(n)) return bad("Betrag, Inflationsrate und Jahre eingeben.");
    const q = Math.pow(1 + r / 100, n);
    return { result: eur(a / q), label: `Kaufkraft von ${eur(a)} in ${nf(n, 0)} Jahren`, steps: [line(`Preisfaktor = (1 + ${nf(r / 100, 4)})<sup>${nf(n, 0)}</sup> = ${nf(q, 4)}`), line(`Was heute ${eur(a)} kostet, kostet dann ${eur(a * q)}.`), line(`Kaufkraft = ${eur(a)} ÷ ${nf(q, 4)} = <mark>${eur(a / q)}</mark>`), line(`Verlust an Kaufkraft: ${pc((1 - 1 / q) * 100, 1)}`)] };
  };

  C.dreisatz = f => {
    const a = val(f, "a"), b = val(f, "b"), c = val(f, "c"), anti = sel(f, "kind") === "anti";
    if (![a, b, c].every(Number.isFinite) || a === 0) return bad("Alle drei Werte eingeben, der erste darf nicht 0 sein.");
    if (!anti) { const x = b / a * c; return { result: nf(x, 4), label: "proportional", steps: [line(`${nf(a, 4)} → ${nf(b, 4)}`), line(`1 → ${nf(b, 4)} ÷ ${nf(a, 4)} = ${nf(b / a, 6)}`), line(`${nf(c, 4)} → ${nf(b / a, 6)} × ${nf(c, 4)} = <mark>${nf(x, 4)}</mark>`)] }; }
    if (c === 0) return bad("Beim umgekehrten Dreisatz darf der dritte Wert nicht 0 sein.");
    const x = a * b / c;
    return { result: nf(x, 4), label: "umgekehrt proportional", steps: [line(`${nf(a, 4)} → ${nf(b, 4)}`), line(`1 → ${nf(b, 4)} × ${nf(a, 4)} = ${nf(a * b, 4)}`), line(`${nf(c, 4)} → ${nf(a * b, 4)} ÷ ${nf(c, 4)} = <mark>${nf(x, 4)}</mark>`)] };
  };

  const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
  C.bruch = f => {
    const [a, b, c, d] = ["a", "b", "c", "d"].map(n => val(f, n)); const op = sel(f, "op");
    if (![a, b, c, d].every(x => Number.isInteger(x))) return bad("Bitte ganze Zahlen für Zähler und Nenner eingeben.");
    if (b === 0 || d === 0) return bad("Ein Nenner darf nicht 0 sein.");
    let n, m; const st = [];
    if (op === "+" || op === "-") {
      const l = Math.abs(b * d) / gcd(b, d); const a2 = a * (l / b), c2 = c * (l / d);
      st.push(line(`Gemeinsamer Nenner (kgV von ${b} und ${d}): ${l}`));
      st.push(line(`${a}/${b} = ${a2}/${l} · ${c}/${d} = ${c2}/${l}`));
      n = op === "+" ? a2 + c2 : a2 - c2; m = l;
      st.push(line(`${a2} ${op} ${c2} = ${n} → ${n}/${m}`));
    } else if (op === "*") { n = a * c; m = b * d; st.push(line(`Zähler mal Zähler, Nenner mal Nenner: ${a}·${c} / ${b}·${d} = ${n}/${m}`)); }
    else { if (c === 0) return bad("Durch 0 kann man nicht teilen."); n = a * d; m = b * c; st.push(line(`Mit dem Kehrwert malnehmen: ${a}/${b} × ${d}/${c} = ${n}/${m}`)); }
    if (m < 0) { n = -n; m = -m; }
    const g = gcd(n, m); const rn = n / g, rm = m / g;
    if (g > 1) st.push(line(`Kürzen durch ${g}: ${n}/${m} = ${rn}/${rm}`));
    const whole = Math.trunc(rn / rm), rest = Math.abs(rn % rm);
    const mixed = rm !== 1 && Math.abs(rn) > rm ? ` = ${whole} ${rest}/${rm}` : "";
    st.push(line(`Ergebnis: <mark>${rm === 1 ? rn : `${rn}/${rm}`}</mark>${mixed} ≈ ${nf(rn / rm, 6)}`));
    return { result: rm === 1 ? `${rn}` : `${rn}/${rm}`, label: `≈ ${nf(rn / rm, 6)}`, steps: st };
  };

  const UNITS = {
    laenge: { label: "Länge", base: "m", u: { mm: 0.001, cm: 0.01, m: 1, km: 1000, Zoll: 0.0254, Fuß: 0.3048, Meile: 1609.344, Seemeile: 1852 } },
    flaeche: { label: "Fläche", base: "m²", u: { "cm²": 1e-4, "m²": 1, Ar: 100, Hektar: 1e4, "km²": 1e6, Joch: 5754.642, Acre: 4046.8564224 } },
    volumen: { label: "Volumen", base: "l", u: { ml: 0.001, cl: 0.01, dl: 0.1, l: 1, "m³": 1000, "Gallone (US)": 3.785411784, "Cup (US)": 0.2365882365 } },
    masse: { label: "Gewicht", base: "kg", u: { mg: 1e-6, g: 0.001, dag: 0.01, kg: 1, t: 1000, Pfund: 0.45359237, Unze: 0.028349523125 } },
    tempo: { label: "Geschwindigkeit", base: "m/s", u: { "km/h": 1 / 3.6, "m/s": 1, mph: 0.44704, Knoten: 1852 / 3600 } },
    temp: { label: "Temperatur", base: "°C", u: { "°C": 0, "°F": 0, K: 0 } },
  };
  C.einheit = f => {
    const cat = sel(f, "cat"), v = val(f, "value");
    const fromSel = f.elements.from, toSel = f.elements.to;
    if (fromSel.dataset.cat !== cat) {
      const keys = Object.keys(UNITS[cat].u);
      fromSel.innerHTML = toSel.innerHTML = keys.map(k => `<option>${k}</option>`).join("");
      fromSel.value = keys[cat === "temp" ? 0 : Math.min(2, keys.length - 1)]; toSel.value = keys[cat === "temp" ? 1 : Math.min(3, keys.length - 1)];
      fromSel.dataset.cat = cat;
    }
    if (!Number.isFinite(v)) return bad("Bitte einen Wert eingeben.");
    const a = fromSel.value, b = toSel.value;
    if (cat === "temp") {
      const toC = { "°C": x => x, "°F": x => (x - 32) * 5 / 9, K: x => x - 273.15 }[a](v);
      const r = { "°C": x => x, "°F": x => x * 9 / 5 + 32, K: x => x + 273.15 }[b](toC);
      return { result: `${nf(r, 4)} ${b}`, label: `${nf(v, 4)} ${a}`, steps: [line(`Umweg über Grad Celsius: ${nf(v, 4)} ${a} = ${nf(toC, 4)} °C`), line(`${nf(toC, 4)} °C = <mark>${nf(r, 4)} ${b}</mark>`), line(`Formeln: °F = °C × 9/5 + 32 · K = °C + 273,15`)] };
    }
    const U = UNITS[cat].u, base = v * U[a], r = base / U[b];
    return { result: `${nf(r, 6)} ${b}`, label: `${nf(v, 6)} ${a}`, steps: [line(`1 ${a} = ${nf(U[a], 8)} ${UNITS[cat].base}`), line(`${nf(v, 6)} ${a} = ${nf(base, 8)} ${UNITS[cat].base}`), line(`÷ ${nf(U[b], 8)} (1 ${b} in ${UNITS[cat].base}) = <mark>${nf(r, 6)} ${b}</mark>`)] };
  };

  C.schnitt = f => {
    const vals = String(f.elements.values.value).split(/[;\n\s]+/).map(num).filter(Number.isFinite);
    const ws = String(f.elements.weights?.value || "").split(/[;\n\s]+/).map(num).filter(Number.isFinite);
    if (!vals.length) return bad("Zahlen mit Leerzeichen, Strichpunkt oder Zeilenumbruch trennen.");
    const s = [...vals].sort((x, y) => x - y), n = vals.length, sum = vals.reduce((a, b) => a + b, 0);
    const med = n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2;
    const st = [line(`Summe = ${nf(sum, 4)} · Anzahl = ${n}`), line(`Mittelwert = ${nf(sum, 4)} ÷ ${n} = <mark>${nf(sum / n, 4)}</mark>`), line(`Median (mittlerer Wert der sortierten Liste): ${nf(med, 4)}`), line(`Kleinster Wert ${nf(s[0], 4)} · größter Wert ${nf(s[n - 1], 4)}`)];
    let res = nf(sum / n, 4), label = "Mittelwert";
    if (ws.length === n) {
      const wsum = ws.reduce((a, b) => a + b, 0); const wm = vals.reduce((a, v, k) => a + v * ws[k], 0) / wsum;
      st.unshift(line(`Gewichtet: Σ(Wert × Gewicht) ÷ Σ Gewichte = ${nf(wm * wsum, 4)} ÷ ${nf(wsum, 4)} = <mark>${nf(wm, 4)}</mark>`));
      res = nf(wm, 4); label = "gewichteter Schnitt";
    } else if (ws.length) st.push(line(`Für den gewichteten Schnitt braucht es gleich viele Gewichte wie Werte (${ws.length} statt ${n}).`));
    return { result: res, label, steps: st };
  };

  C.lohn = f => {
    const dir = sel(f, "dir"), hours = val(f, "hours"), amount = val(f, "amount"), salaries = num(sel(f, "salaries"));
    if (![hours, amount, salaries].every(Number.isFinite) || hours <= 0) return bad("Betrag und Wochenstunden eingeben.");
    const hpy = hours * 52, hpm = hpy / 12;
    if (dir === "m2h") {
      const year = amount * salaries, h = year / hpy;
      return { result: eur(h), label: "brutto pro Stunde", steps: [line(`Jahresgehalt = ${eur(amount)} × ${salaries} = ${eur(year)}`), line(`Jahresstunden = ${nf(hours, 2)} × 52 Wochen = ${nf(hpy, 1)}`), line(`Stundenlohn = ${eur(year)} ÷ ${nf(hpy, 1)} = <mark>${eur(h)}</mark>`), salaries === 14 ? line(`Mit 14 Gehältern (Urlaubs- und Weihnachtsgeld) ist der Stundenlohn um ein Sechstel höher als mit 12.`) : line(`Bei 12 Gehältern ohne Sonderzahlungen.`)] };
    }
    const year = amount * hpy, mon = year / salaries;
    return { result: eur(mon), label: `brutto pro Monat (${salaries}×)`, steps: [line(`Jahresstunden = ${nf(hours, 2)} × 52 = ${nf(hpy, 1)} (≈ ${nf(hpm, 1)} pro Monat)`), line(`Jahresbrutto = ${eur(amount)} × ${nf(hpy, 1)} = ${eur(year)}`), line(`Monatsgehalt = ${eur(year)} ÷ ${salaries} = <mark>${eur(mon)}</mark>`)] };
  };

  function run(form) {
    const fn = C[form.dataset.calc]; if (!fn) return;
    let r; try { r = fn(form); } catch (e) { r = bad("Bitte die Eingaben prüfen."); }
    const out = $(`[data-out="${form.id}"]`) || form.querySelector("[data-out]"); if (!out || !r) return;
    if (!r.result) { out.innerHTML = `<p class="hint">${r.note}</p>`; return; }
    out.innerHTML = `<div class="res"><span class="res-label">${r.label || "Ergebnis"}</span><output class="res-val">${r.result}</output></div><h3 class="way-h">Rechenweg</h3><ol class="way">${r.steps.join("")}</ol>${r.extra || ""}`;
  }

  function init() {
    $$("form[data-calc]").forEach(f => {
      f.addEventListener("input", () => run(f));
      f.addEventListener("change", () => run(f));
      f.addEventListener("submit", e => { e.preventDefault(); run(f); });
      $$("[data-show-when]", f).forEach(el => {
        const [name, v] = el.dataset.showWhen.split("=");
        const upd = () => { el.hidden = sel(f, name) !== v; };
        f.addEventListener("change", upd); upd();
      });
      run(f);
    });
    // Modus-Beschriftungen des Prozentrechners
    $$("form[data-calc=percent]").forEach(f => {
      const L = { anteil: ["Grundwert", "Prozentsatz (%)"], satz: ["Prozentwert", "Grundwert"], grund: ["Prozentwert", "Prozentsatz (%)"], veraenderung: ["Alter Wert", "Neuer Wert"], rabatt: ["Preis (€)", "Rabatt (%)"], ursprung: ["Endpreis (€)", "Rabatt (%)"] };
      const upd = () => { const m = sel(f, "mode"); const [x, y] = L[m]; $("[data-l=a]", f).textContent = x; $("[data-l=b]", f).textContent = y; };
      f.elements.mode.addEventListener("change", upd); upd();
    });
  }
  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", init) : init();
})();
