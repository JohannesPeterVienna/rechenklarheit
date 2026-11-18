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
  /* Optionales Feld: leer = 0, sonst muss es eine gültige Zahl sein (sonst NaN → Fehlermeldung) */
  const opt = (f, n) => { const raw = f.elements[n]?.value; return (raw === undefined || raw === null || String(raw).trim() === "") ? 0 : num(raw); };
  /* Liste position-treu einlesen: jeder Eintrag muss eine Zahl sein, sonst Fehler mit Position */
  const parseList = (txt, what) => {
    const toks = String(txt || "").split(/[;\n\s]+/).filter(t => t !== "");
    const out = [];
    for (let k = 0; k < toks.length; k++) { const x = num(toks[k]); if (!Number.isFinite(x)) return { error: `${what} Nr. ${k + 1} („${toks[k].replace(/[<>&"]/g, "")}“) ist keine gültige Zahl.` }; out.push(x); }
    return { list: out };
  };

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
    if (dir === "n2b") { const t = amt * rate / 100; return { result: eur(amt + t), label: `brutto bei ${pc(rate, 1)}`, k: [["Netto", amt, "eur"], ["Steuer", t, "eur"], ["Brutto", amt + t, "eur"]], steps: [line(`Steuer = ${eur(amt)} × ${nf(rate, 2)} ÷ 100 = ${eur(t)}`), line(`Brutto = ${eur(amt)} + ${eur(t)} = <mark>${eur(amt + t)}</mark>`)] }; }
    const n = amt / q, t = amt - n;
    return { result: eur(n), label: `netto bei ${pc(rate, 1)}`, k: [["Netto", n, "eur"], ["Steuer", t, "eur"], ["Brutto", amt, "eur"]], steps: [line(`Netto = Brutto ÷ ${nf(q, 4)}`), line(`= ${eur(amt)} ÷ ${nf(q, 4)} = <mark>${eur(n)}</mark>`), line(`Enthaltene Steuer = ${eur(amt)} − ${eur(n)} = ${eur(t)}`), line(`Nicht ${pc(rate, 1)} vom Bruttobetrag abziehen – das ergäbe ${eur(amt * (1 - rate / 100))} und wäre zu wenig.`)] };
  };

  C.rabatt = f => {
    const p = val(f, "price"); const r1 = opt(f, "r1"), r2 = opt(f, "r2"), sk = opt(f, "skonto");
    if (!Number.isFinite(p)) return bad("Bitte den Preis eingeben.");
    if (![r1, r2, sk].every(Number.isFinite)) return bad("Rabatte und Skonto müssen Zahlen sein (leer = kein Rabatt).");
    let x = p; const st = [line(`Ausgangspreis: ${eur(p)}`)];
    for (const [r, n] of [[r1, "1. Rabatt"], [r2, "2. Rabatt"], [sk, "Skonto"]]) { if (!r) continue; const nx = x * (1 - r / 100); st.push(line(`${n} ${pc(r)}: ${eur(x)} × ${nf(1 - r / 100, 4)} = ${eur(nx)}`)); x = nx; }
    const tot = (1 - x / p) * 100;
    st.push(line(`Endpreis: <mark>${eur(x)}</mark>`));
    st.push(line(`Gesamtersparnis: ${eur(p - x)} = <b>${pc(tot)}</b>${(r1 && r2) ? ` – nicht ${pc(r1 + r2 + sk)}, weil jeder Rabatt auf den schon reduzierten Preis wirkt` : ""}`));
    return { result: eur(x), label: `Ersparnis ${pc(tot)}`, steps: st, k: [["Endpreis", x, "eur"], ["Ersparnis", p - x, "eur"], ["Gesamtrabatt", tot, "pct"]] };
  };

  C.zins = f => {
    const k0 = opt(f, "start"), rate = opt(f, "monthly"), p = val(f, "rate"), n = val(f, "years");
    if (!Number.isFinite(k0)) return bad("Das Startkapital ist keine gültige Zahl (leer lassen für 0 €).");
    if (!Number.isFinite(rate)) return bad("Die Sparrate ist keine gültige Zahl (leer lassen für 0 €).");
    if (!Number.isFinite(p) || !Number.isFinite(n) || n <= 0 || n > 80) return bad("Zinssatz und Laufzeit (1 Monat bis 80 Jahre) eingeben.");
    if (k0 < 0 || rate < 0) return bad("Startkapital und Sparrate dürfen nicht negativ sein.");
    const months = Math.round(n * 12);
    if (months < 1 || Math.abs(n * 12 - months) > 1e-6) return bad("Die Laufzeit muss ganze Monate ergeben – z. B. 1,5 Jahre (18 Monate) oder 0,25 Jahre (3 Monate).");
    const i = p / 100 / 12; let k = k0, paid = k0; const rows = [];
    for (let m = 1; m <= months; m++) {
      k = k * (1 + i) + rate; paid += rate;
      if (m % 12 === 0 || m === months) rows.push([m % 12 === 0 ? String(m / 12) : nf(m / 12, 2), paid, k - paid, k]);
    }
    const int = k - paid;
    const whole = months % 12 === 0;
    const span = whole ? `${nf(months / 12, 0)} ${months === 12 ? "Jahr" : "Jahren"}` : `${nf(months / 12, 2)} Jahren (${months} ${months === 1 ? "Monat" : "Monaten"})`;
    const table = `<div class="scroll"><table class="tbl small"><thead><tr><th>Jahr</th><th>Eingezahlt</th><th>Zinsen gesamt</th><th>Kapital</th></tr></thead><tbody>${rows.map(r => `<tr><td>${r[0]}</td><td>${eur(r[1])}</td><td>${eur(r[2])}</td><td>${eur(r[3])}</td></tr>`).join("")}</tbody></table></div>`;
    const ch = chart(rows.map(r => ({ label: r[0], a: r[1], b: Math.max(r[2], 0) })), ["a", "b"], ["var(--pen)", "var(--marker-strong)"], ["Eingezahlt", "Zinsen"]);
    return { result: eur(k), label: `nach ${span}`, pre: ch, k: [["Endkapital", k, "eur"], ["Eingezahlt", paid, "eur"], ["Zinsen", int, "eur"]], csv: { name: "sparplan", head: ["Jahr", "Eingezahlt", "Zinsen gesamt", "Kapital"], rows: rows.map(r => [r[0], nf(r[1]), nf(r[2]), nf(r[3])]) }, steps: [line(`Monatszins = ${pc(p)} ÷ 12 = ${pc(p / 12, 4)}`), line(`Jeden Monat (${months} Monate): Kapital × ${nf(1 + i, 6)} + ${eur(rate)} Sparrate`), line(`Eingezahlt: ${eur(paid)} · davon Zinsen: <mark>${eur(int)}</mark>`), line(`Zinsen machen ${pc(k ? int / k * 100 : 0, 1)} des Endkapitals aus.`)], extra: table };
  };

  C.kredit = f => {
    const K = val(f, "amount"), p = val(f, "rate"), n = val(f, "years");
    if (!Number.isFinite(K) || !Number.isFinite(p) || !Number.isFinite(n) || n <= 0 || n > 50) return bad("Betrag, Sollzins und Laufzeit (bis 50 Jahre) eingeben.");
    if (K <= 0 || p < 0) return bad("Der Kreditbetrag muss größer als 0 sein, der Sollzins darf nicht negativ sein.");
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
    const ch = chart(rows.map(r => ({ label: r[0], a: r[2], b: r[1] })), ["a", "b"], ["var(--pen)", "var(--red)"], ["Tilgung", "Zinsen"]);
    return { result: eur(a), label: "Monatsrate", pre: ch, k: [["Monatsrate", a, "eur"], ["Zinskosten", interest, "eur"], ["Zurückgezahlt gesamt", total, "eur"]], csv: { name: "tilgungsplan", head: ["Jahr", "Zinsen", "Tilgung", "Restschuld"], rows: rows.map(r => [String(r[0]), nf(r[1]), nf(r[2]), nf(r[3])]) }, steps: [line(`Monatszins i = ${pc(p)} ÷ 12 = ${nf(i * 100, 4)} %`), line(`Rate = Kredit × i ÷ (1 − (1 + i)<sup>−${m}</sup>)`), line(`= <mark>${eur(a)}</mark> pro Monat, ${m} Raten`), line(`Zurückgezahlt gesamt: ${eur(total)} · Zinskosten: <b>${eur(interest)}</b>`), line(`Ohne Gebühren gerechnet. Der Effektivzins im Angebot enthält zusätzlich Kosten wie Bearbeitungsgebühren.`)], extra: table };
  };

  /* Kreditvergleich: zwei Annuitätenkredite mit Gebühren; Effektivzins per Bisektion (Monatszins → (1+r)^12 − 1) */
  const angebot = (K, m, p, fee, mon) => {
    const i = p / 100 / 12, a = i === 0 ? K / m : K * i / (1 - Math.pow(1 + i, -m));
    const total = a * m + fee + mon * m;
    let lo = 0, hi = 0.1, r = 0;
    for (let k = 0; k < 200; k++) {
      r = (lo + hi) / 2; let pv = 0;
      for (let t = 1; t <= m; t++) pv += (a + mon) / Math.pow(1 + r, t);
      if (pv > K - fee) lo = r; else hi = r;
    }
    return { a, total, eff: (Math.pow(1 + r, 12) - 1) * 100 };
  };
  C.kreditvergleich = f => {
    const K = val(f, "amount"), n = val(f, "years");
    const A = ["a_rate", "a_fee", "a_monthly"].map(k => k === "a_rate" ? val(f, k) : opt(f, k));
    const B = ["b_rate", "b_fee", "b_monthly"].map(k => k === "b_rate" ? val(f, k) : opt(f, k));
    if (!Number.isFinite(K) || !Number.isFinite(n) || K <= 0 || n <= 0 || n > 30) return bad("Kreditbetrag und Laufzeit (bis 30 Jahre) eingeben.");
    if (![...A, ...B].every(Number.isFinite)) return bad("Sollzins beider Angebote eingeben; Gebühren leer lassen = 0 €.");
    if ([...A, ...B].some(x => x < 0) || A[0] > 30 || B[0] > 30) return bad("Zinsen und Gebühren dürfen nicht negativ sein, der Sollzins höchstens 30 %.");
    if (A[1] >= K || B[1] >= K) return bad("Die Bearbeitungsgebühr muss kleiner als der Kreditbetrag sein.");
    const m = Math.round(n * 12);
    const a = angebot(K, m, A[0], A[1], A[2]), b = angebot(K, m, B[0], B[1], B[2]);
    const d = Math.abs(a.total - b.total), win = a.total <= b.total ? "A" : "B";
    const row = (t, x, y) => `<tr><td>${t}</td><td>${x}</td><td>${y}</td></tr>`;
    const table = `<div class="scroll"><table class="tbl small"><thead><tr><th></th><th>Angebot A</th><th>Angebot B</th></tr></thead><tbody>${row("Monatsrate", eur(a.a), eur(b.a))}${row("Gebühren gesamt", eur(A[1] + A[2] * m), eur(B[1] + B[2] * m))}${row("Gesamtkosten", eur(a.total), eur(b.total))}${row("Effektivzins (Näherung)", pc(a.eff), pc(b.eff))}</tbody></table></div>`;
    return { result: d < 0.005 ? "gleich teuer" : `Angebot ${win}`, label: d < 0.005 ? "Beide Angebote kosten gleich viel" : `günstiger um ${eur(d)}`, extra: table, k: [["Gesamtkosten A", a.total, "eur"], ["Gesamtkosten B", b.total, "eur"], ["Effektivzins A", a.eff, "pct"], ["Effektivzins B", b.eff, "pct"]],
      steps: [line(`Laufzeit: ${m} Monate, Kredit ${eur(K)}`),
        line(`A: Rate ${eur(a.a)} × ${m} + ${eur(A[1])} + ${eur(A[2])} × ${m} = ${eur(a.total)}`),
        line(`B: Rate ${eur(b.a)} × ${m} + ${eur(B[1])} + ${eur(B[2])} × ${m} = ${eur(b.total)}`),
        d < 0.005 ? line(`Beide Angebote kosten insgesamt <mark>${eur(a.total)}</mark>.`) : line(`Differenz: <mark>${eur(d)}</mark> zugunsten von Angebot ${win}`),
        line(`Effektivzins: A ${pc(a.eff)}, B ${pc(b.eff)} – Näherung für gleichbleibende Raten, ohne Restschuldversicherung`)] };
  };

  C.inflation = f => {
    const a = val(f, "amount"), r = val(f, "rate"), n = val(f, "years");
    if (!Number.isFinite(a) || !Number.isFinite(r) || !Number.isFinite(n)) return bad("Betrag, Inflationsrate und Jahre eingeben.");
    if (a < 0 || n < 0 || r <= -100) return bad("Betrag und Jahre dürfen nicht negativ sein.");
    const q = Math.pow(1 + r / 100, n);
    return { result: eur(a / q), label: `Kaufkraft von ${eur(a)} in ${nf(n, 0)} Jahren`, k: [["Kaufkraft", a / q, "eur"], ["Preis dann", a * q, "eur"], ["Kaufkraftverlust", (1 - 1 / q) * 100, "pct"]], steps: [line(`Preisfaktor = (1 + ${nf(r / 100, 4)})<sup>${nf(n, 0)}</sup> = ${nf(q, 4)}`), line(`Was heute ${eur(a)} kostet, kostet dann ${eur(a * q)}.`), line(`Kaufkraft = ${eur(a)} ÷ ${nf(q, 4)} = <mark>${eur(a / q)}</mark>`), line(`Verlust an Kaufkraft: ${pc((1 - 1 / q) * 100, 1)}`)] };
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
    return { result: rm === 1 ? `${rn}` : `${rn}/${rm}`, label: `≈ ${nf(rn / rm, 6)}`, steps: st, k: [["Dezimalwert", rn / rm, "num"]] };
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
    const pv = parseList(f.elements.values?.value, "Wert");
    if (pv.error) return bad(pv.error);
    const vals = pv.list;
    const pw = parseList(f.elements.weights?.value, "Gewicht");
    if (pw.error) return bad(pw.error);
    const ws = pw.list;
    if (!vals.length) return bad("Zahlen mit Leerzeichen, Strichpunkt oder Zeilenumbruch trennen.");
    if (ws.length && ws.length !== vals.length) return bad(`Für den gewichteten Schnitt braucht es gleich viele Gewichte wie Werte (${ws.length} Gewichte für ${vals.length} Werte).`);
    if (ws.length) {
      const neg = ws.findIndex(w => w < 0);
      if (neg >= 0) return bad(`Gewicht Nr. ${neg + 1} ist negativ – Gewichte müssen 0 oder größer sein.`);
      if (!(ws.reduce((a, b) => a + b, 0) > 0)) return bad("Die Summe der Gewichte muss größer als 0 sein.");
    }
    const s = [...vals].sort((x, y) => x - y), n = vals.length, sum = vals.reduce((a, b) => a + b, 0);
    const med = n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2;
    const st = [line(`Summe = ${nf(sum, 4)} · Anzahl = ${n}`), line(`Mittelwert = ${nf(sum, 4)} ÷ ${n} = <mark>${nf(sum / n, 4)}</mark>`), line(`Median (mittlerer Wert der sortierten Liste): ${nf(med, 4)}`), line(`Kleinster Wert ${nf(s[0], 4)} · größter Wert ${nf(s[n - 1], 4)}`)];
    let res = nf(sum / n, 4), label = "Mittelwert";
    if (ws.length === n) {
      const wsum = ws.reduce((a, b) => a + b, 0); const wm = vals.reduce((a, v, k) => a + v * ws[k], 0) / wsum;
      st.unshift(line(`Gewichtet: Σ(Wert × Gewicht) ÷ Σ Gewichte = ${nf(wm * wsum, 4)} ÷ ${nf(wsum, 4)} = <mark>${nf(wm, 4)}</mark>`));
      res = nf(wm, 4); label = "gewichteter Schnitt";
    }
    return { result: res, label, steps: st };
  };

  C.lohn = f => {
    const dir = sel(f, "dir"), hours = val(f, "hours"), amount = val(f, "amount"), salaries = num(sel(f, "salaries"));
    if (![hours, amount, salaries].every(Number.isFinite) || hours <= 0) return bad("Betrag und Wochenstunden eingeben.");
    if (amount < 0 || hours > 80) return bad("Der Betrag darf nicht negativ sein, die Wochenstunden höchstens 80.");
    const hpy = hours * 52, hpm = hpy / 12;
    if (dir === "m2h") {
      const year = amount * salaries, h = year / hpy;
      return { result: eur(h), label: "brutto pro Stunde", k: [["Stundenlohn", h, "eur"], ["Jahresbrutto", year, "eur"]], steps: [line(`Jahresgehalt = ${eur(amount)} × ${salaries} = ${eur(year)}`), line(`Jahresstunden = ${nf(hours, 2)} × 52 Wochen = ${nf(hpy, 1)}`), line(`Stundenlohn = ${eur(year)} ÷ ${nf(hpy, 1)} = <mark>${eur(h)}</mark>`), salaries === 14 ? line(`Mit 14 Gehältern (Urlaubs- und Weihnachtsgeld) ist der Stundenlohn um ein Sechstel höher als mit 12.`) : line(`Bei 12 Gehältern ohne Sonderzahlungen.`)] };
    }
    const year = amount * hpy, mon = year / salaries;
    return { result: eur(mon), label: `brutto pro Monat (${salaries}×)`, k: [["Monatsgehalt", mon, "eur"], ["Jahresbrutto", year, "eur"]], steps: [line(`Jahresstunden = ${nf(hours, 2)} × 52 = ${nf(hpy, 1)} (≈ ${nf(hpm, 1)} pro Monat)`), line(`Jahresbrutto = ${eur(amount)} × ${nf(hpy, 1)} = ${eur(year)}`), line(`Monatsgehalt = ${eur(year)} ÷ ${salaries} = <mark>${eur(mon)}</mark>`)] };
  };

  /* Achsenwerte: ganze Zahlen mit Tausenderpunkt wie in den Tabellen (z. B. 4.524), ab einer Million kompakt (1,2 Mio.) */
  const axisNum = x => x >= 1e6
    ? new Intl.NumberFormat("de-DE", { notation: "compact", maximumFractionDigits: 1 }).format(x)
    : new Intl.NumberFormat("de-DE", { maximumFractionDigits: 0, useGrouping: true }).format(Math.round(x));
  /* ---------- Balkendiagramm (gestapelt), barrierearm mit Tabelle darunter */
  const chart = (rows, keys, colors, names, fmt = eur) => {
    if (!rows.length) return "";
    const W = 640, H = 220, P = 52, n = rows.length, bw = (W - P - 8) / n;
    const max = Math.max(...rows.map(r => keys.reduce((a, k) => a + r[k], 0))) || 1;
    const step = Math.ceil(n / 10);
    let g = "";
    rows.forEach((r, i) => { let y = H - 22; keys.forEach((k, j) => { const h = r[k] / max * (H - 40); y -= h; g += `<rect x="${(P + i * bw + bw * .12).toFixed(1)}" y="${y.toFixed(1)}" width="${(bw * .76).toFixed(1)}" height="${Math.max(h, 0).toFixed(1)}" fill="${colors[j]}"><title>${r.label}: ${names[j]} ${fmt(r[k])}</title></rect>`; });
      if (i % step === 0 || i === n - 1) g += `<text x="${(P + i * bw + bw / 2).toFixed(1)}" y="${H - 6}" text-anchor="middle">${r.label}</text>`; });
    const ax = [0, .5, 1].map(f => `<text x="${P - 4}" y="${(H - 22 - f * (H - 40) + 4).toFixed(1)}" text-anchor="end">${axisNum(max * f)}</text><line x1="${P}" x2="${W}" y1="${(H - 22 - f * (H - 40)).toFixed(1)}" y2="${(H - 22 - f * (H - 40)).toFixed(1)}" />`).join("");
    const leg = names.map((nm, j) => `<span><i style="background:${colors[j]}"></i>${nm}</span>`).join("");
    return `<figure class="chart"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Diagramm: ${names.join(" und ")} pro Jahr">${ax}${g}</svg><figcaption class="legend">${leg}</figcaption></figure>`;
  };

  C.strom = f => {
    const mode = sel(f, "mode"), price = val(f, "price");
    const pre = f.elements.preset;
    if (pre && pre.value && pre.dataset.applied !== pre.value) { const [w, h] = pre.value.split("|"); f.elements.watt.value = w.replace(".", ","); f.elements.hours.value = h.replace(".", ","); pre.dataset.applied = pre.value; }
    if (!Number.isFinite(price) || price < 0) return bad("Bitte den Strompreis in Cent pro kWh eingeben.");
    const ct = price / 100;
    if (mode === "label") {
      const kwh = val(f, "kwh"); if (!Number.isFinite(kwh) || kwh < 0) return bad("Bitte den Jahresverbrauch in kWh eingeben.");
      return { result: eur(kwh * ct), label: "Stromkosten pro Jahr", k: [["Kosten pro Jahr", kwh * ct, "eur"], ["Verbrauch pro Jahr", kwh, "kWh"]], steps: [line(`${nf(kwh, 1)} kWh × ${nf(price, 2)} Cent = <mark>${eur(kwh * ct)}</mark> pro Jahr`), line(`Pro Monat: ${eur(kwh * ct / 12)} · pro Tag: ${eur(kwh * ct / 365)}`), line(`Spart ein neues Gerät 30 % ein, sind das ${eur(kwh * ct * .3)} im Jahr.`)] };
    }
    const w = val(f, "watt"), h = val(f, "hours"), d = val(f, "days");
    if (![w, h, d].every(Number.isFinite)) return bad("Leistung, Stunden pro Tag (bis 24) und Tage pro Jahr eingeben.");
    if (w < 0 || h < 0 || h > 24 || d < 0 || d > 366) return bad("Leistung darf nicht negativ sein; Stunden pro Tag 0–24, Tage pro Jahr 0–366.");
    const day = w * h / 1000, year = day * d;
    return { result: eur(year * ct), label: "Stromkosten pro Jahr", k: [["Kosten pro Jahr", year * ct, "eur"], ["Verbrauch pro Jahr", year, "kWh"]], steps: [line(`Pro Tag: ${nf(w, 1)} W × ${nf(h, 2)} h ÷ 1.000 = ${nf(day, 3)} kWh`), line(`Pro Jahr: ${nf(day, 3)} kWh × ${nf(d, 0)} Tage = ${nf(year, 1)} kWh`), line(`${nf(year, 1)} kWh × ${nf(price, 2)} Cent = <mark>${eur(year * ct)}</mark>`), line(`Pro Monat ${eur(year * ct / 12)} · pro Betriebsstunde ${eur(w / 1000 * ct)}`)] };
  };

  C.fahrt = f => {
    const ev = sel(f, "fuel") === "ev";
    const lc = $("[data-l=cons]", f), lp = $("[data-l=price]", f);
    if (lc) lc.textContent = ev ? "Verbrauch (kWh/100 km)" : "Verbrauch (l/100 km)";
    if (lp) lp.textContent = ev ? "Strompreis (€/kWh)" : "Preis (€/l)";
    if (f.dataset.fuel !== sel(f, "fuel")) { if (f.dataset.fuel) { f.elements.cons.value = ev ? "18" : "6,5"; f.elements.price.value = ev ? "0,30" : "1,70"; } f.dataset.fuel = sel(f, "fuel"); }
    const km = val(f, "km"), t = num(sel(f, "trip")), c = val(f, "cons"), p = val(f, "price"), n = Math.max(1, Math.round(val(f, "people") || 1));
    if (![km, c, p].every(Number.isFinite)) return bad("Strecke, Verbrauch und Preis eingeben.");
    if (km <= 0 || c < 0 || p < 0) return bad("Strecke muss größer als 0 sein, Verbrauch und Preis dürfen nicht negativ sein.");
    const dist = km * t, q = dist * c / 100, cost = q * p, u = ev ? "kWh" : "l";
    return { result: eur(cost / n), label: n > 1 ? `pro Person (${n} Personen)` : "Kosten der Fahrt", k: [["Kosten der Fahrt", cost, "eur"], ["pro Person", cost / n, "eur"], ["pro 100 km", cost / dist * 100, "eur"]], steps: [line(`Strecke: ${nf(km, 1)} km${t === 2 ? " × 2 (hin und zurück)" : ""} = ${nf(dist, 1)} km`), line(`Verbrauch: ${nf(dist, 1)} km × ${nf(c, 2)} ${u} ÷ 100 = ${nf(q, 2)} ${u}`), line(`Kosten: ${nf(q, 2)} ${u} × ${eur(p)} = ${n > 1 ? eur(cost) : `<mark>${eur(cost)}</mark>`}`), ...(n > 1 ? [line(`Pro Person: ${eur(cost)} ÷ ${n} = <mark>${eur(cost / n)}</mark>`)] : []), line(`Das sind ${nf(cost / dist * 100, 2)} € pro 100 km.`)] };
  };

  C.tip = f => {
    const b = val(f, "bill"), p = num(sel(f, "pct")), r = num(sel(f, "round")), n = Math.max(1, Math.round(val(f, "people") || 1));
    if (!Number.isFinite(b) || b <= 0) return bad("Bitte den Rechnungsbetrag eingeben.");
    const tip = b * p / 100, raw = b + tip, tot = r > 0 ? Math.ceil(raw / r - 1e-9) * r : raw, eff = (tot - b) / b * 100;
    const st = [line(`Trinkgeld: ${eur(b)} × ${nf(p, 0)} % = ${eur(tip)}`), line(`Zusammen: ${eur(raw)}${r > 0 ? ` → aufgerundet auf ${eur(tot)}` : ""}`)];
    if (r > 0) st.push(line(`Tatsächliches Trinkgeld: ${eur(tot - b)} (${pc(eff, 1)})`));
    st.push(n > 1 ? line(`Pro Person: ${eur(tot)} ÷ ${n} = <mark>${eur(tot / n)}</mark>`) : line(`Zu zahlen: <mark>${eur(tot)}</mark>`));
    return { result: eur(n > 1 ? tot / n : tot), label: n > 1 ? `pro Person (gesamt ${eur(tot)})` : "Gesamtbetrag", steps: st, k: [["Gesamtbetrag", tot, "eur"], ["Trinkgeld", tot - b, "eur"], ["pro Person", tot / n, "eur"]] };
  };

  C.marge = f => {
    const mode = sel(f, "mode"), ek = val(f, "ek"), b = val(f, "b"), vat = num(sel(f, "vat"));
    const lb = $("[data-l=b]", f); if (lb) lb.textContent = { ekvk: "Verkaufspreis netto (€)", auf: "Aufschlag (%)", span: "Zielmarge (%)" }[mode];
    if (f.dataset.mode !== mode) { if (f.dataset.mode) f.elements.b.value = { ekvk: "100", auf: "50", span: "40" }[mode]; f.dataset.mode = mode; }
    if (!Number.isFinite(ek) || !Number.isFinite(b) || ek <= 0) return bad("Einkaufspreis und zweiten Wert eingeben.");
    let vk; const st = [];
    if (mode === "ekvk") vk = b;
    else if (mode === "auf") { vk = ek * (1 + b / 100); st.push(line(`Verkaufspreis = ${eur(ek)} × (1 + ${nf(b, 2)} %) = ${eur(vk)}`)); }
    else { if (b >= 100) return bad("Eine Marge von 100 % oder mehr ist nicht möglich."); vk = ek / (1 - b / 100); st.push(line(`Verkaufspreis = ${eur(ek)} ÷ (1 − ${nf(b, 2)} %) = ${eur(vk)}`)); }
    if (vk <= 0) return bad("Der Verkaufspreis muss größer als 0 sein.");
    const g = vk - ek, auf = g / ek * 100, sp = g / vk * 100;
    st.push(line(`Rohgewinn: ${eur(vk)} − ${eur(ek)} = ${eur(g)}`), line(`Aufschlag (auf den Einkauf): ${eur(g)} ÷ ${eur(ek)} = <mark>${pc(auf)}</mark>`), line(`Handelsspanne (vom Verkauf): ${eur(g)} ÷ ${eur(vk)} = <mark>${pc(sp)}</mark>`));
    if (vat > 0) st.push(line(`Bruttopreis mit ${nf(vat, 0)} % USt: ${eur(vk * (1 + vat / 100))}`));
    if (g < 0) st.push(line(`<b>Achtung:</b> Der Verkaufspreis liegt unter dem Einkaufspreis.`));
    return { result: mode === "ekvk" ? pc(sp) : eur(vk), label: mode === "ekvk" ? "Handelsspanne (Marge)" : "Verkaufspreis netto", steps: st, k: [["Verkaufspreis netto", vk, "eur"], ["Rohgewinn", g, "eur"], ["Aufschlag", auf, "pct"], ["Handelsspanne", sp, "pct"]] };
  };


  /* ---------- Sätze aus Gesetz und amtlichen Tabellen. Einzige Quelle ist content/referenz.py; build.py bricht ab, wenn diese Zeile abweicht. */
  /*SAETZE*/const S = {"pendler":{"klein":[[20,696],[40,1356],[60,2016]],"gross":[[2,372],[20,1476],[40,2568],[60,3672]]},"pendlereuro":6,"entf":0.38,"entfMax":4500,"anp":1230,"verzug":{"de_v":5,"de_u":9,"at_u":9.2,"at_a":9.2,"at_v":4},"verzugAb":"2020-01-01","verzugBis":"2026-12-31","basis":{"de":[["2020-01-01",-0.88],["2020-07-01",-0.88],["2021-01-01",-0.88],["2021-07-01",-0.88],["2022-01-01",-0.88],["2022-07-01",-0.88],["2023-01-01",1.62],["2023-07-01",3.12],["2024-01-01",3.62],["2024-07-01",3.37],["2025-01-01",2.27],["2025-07-01",1.27],["2026-01-01",1.27],["2026-07-01",1.52]],"at":[["2020-01-01",-0.62],["2020-07-01",-0.62],["2021-01-01",-0.62],["2021-07-01",-0.62],["2022-01-01",-0.62],["2022-07-01",-0.62],["2023-01-01",1.88],["2023-07-01",3.38],["2024-01-01",3.88],["2024-07-01",3.88],["2025-01-01",2.53],["2025-07-01",1.53],["2026-01-01",1.53],["2026-07-01",1.53]],"atTag":[["2020-01-01",-0.62],["2022-07-27",-0.12],["2022-09-14",0.63],["2022-11-02",1.38],["2022-12-21",1.88],["2023-02-08",2.38],["2023-03-22",2.88],["2023-06-21",3.38],["2023-09-20",3.88],["2024-09-18",3.03],["2024-12-18",2.53],["2025-03-12",2.03],["2025-06-11",1.53],["2026-09-16",2.03]]}};/*/SAETZE*/

  const ganz = x => Number.isFinite(x) && Math.floor(x) === x;
  C.pendler = f => {
    const land = sel(f, "land"), km = val(f, "km");
    if (!Number.isFinite(km) || km < 0 || km > 1000) return bad("Bitte die einfache Entfernung in Kilometern eingeben (0 bis 1.000).");
    if (land === "de") {
      const tage = val(f, "atage"), auto = sel(f, "auto") === "1", andere = opt(f, "andere"), gs = opt(f, "gsde");
      if (!ganz(tage) || tage < 1 || tage > 366) return bad("Arbeitstage pro Jahr als ganze Zahl von 1 bis 366 eingeben.");
      if (!Number.isFinite(andere) || andere < 0) return bad("Andere Werbungskosten müssen eine Zahl ab 0 sein (leer = 0 €).");
      if (!Number.isFinite(gs) || gs < 0 || gs > 45) return bad("Grenzsteuersatz zwischen 0 und 45 % eingeben oder leer lassen.");
      const voll = Math.floor(km), roh = voll * tage * S.entf, ep = auto ? roh : Math.min(roh, S.entfMax);
      const wirksam = Math.max(0, ep + andere - S.anp) - Math.max(0, andere - S.anp);
      const st = [line(`Sätze für das Kalenderjahr 2026 – nicht für die Steuererklärung 2025.`), line(`Volle Kilometer der einfachen Entfernung: ${nf(voll, 0)}${voll !== km ? ` (aus ${nf(km, 2)} km – angebrochene Kilometer zählen nicht)` : ""}`),
        line(`Entfernungspauschale = ${nf(voll, 0)} km × ${nf(tage, 0)} Arbeitstage × ${eur(S.entf)} = ${eur(roh)} (§ 9 Abs. 1 Satz 3 Nr. 4 EStG)`)];
      if (!auto && roh > S.entfMax) st.push(line(`Ohne eigenen oder überlassenen Kraftwagen gilt der Höchstbetrag: <mark>${eur(S.entfMax)}</mark> im Kalenderjahr`));
      else st.push(line(`Anzusetzen: <mark>${eur(ep)}</mark> im Kalenderjahr${auto && roh > S.entfMax ? ` – mit eigenem oder überlassenem Kraftwagen gilt der Höchstbetrag von ${eur(S.entfMax)} nicht` : ""}`));
      st.push(line(`Arbeitnehmer-Pauschbetrag: ${eur(S.anp)} werden ohne Nachweis abgezogen (§ 9a EStG). Mit ${eur(andere)} anderen Werbungskosten wirken von der Pauschale zusätzlich <b>${eur(wirksam)}</b>.`));
      const k = [["Entfernungspauschale pro Jahr", ep, "eur"], ["Zusätzlich wirksam über dem Pauschbetrag", wirksam, "eur"]];
      if (gs > 0) { st.push(line(`Überschlag mit ${pc(gs)} Grenzsteuersatz: ${eur(wirksam)} × ${nf(gs / 100, 4)} = ${eur(wirksam * gs / 100)} weniger Einkommensteuer (ohne Solidaritätszuschlag und Kirchensteuer)`)); k.push(["Steuerersparnis (Überschlag)", wirksam * gs / 100, "eur"]); }
      st.push(line(`Die Pauschale ist ein Abzug vom Einkommen, kein Auszahlungsbetrag.`));
      return { result: eur(ep), label: "Entfernungspauschale 2026 pro Jahr (Werbungskosten)", steps: st, k };
    }
    const art = sel(f, "art") === "gross" ? "gross" : "klein", tage = val(f, "tage"), gs = num(sel(f, "gsat") || "0");
    if (!ganz(km)) return bad("Für Österreich bitte die Entfernung in ganzen Kilometern eingeben, wie sie der Pendlerrechner des Finanzministeriums ausweist.");
    if (!ganz(tage) || tage < 0 || tage > 31) return bad("Fahrten pro Kalendermonat als ganze Zahl von 0 bis 31 eingeben.");
    if (!Number.isFinite(gs)) return bad("Bitte einen Grenzsteuersatz auswählen.");
    const T = S.pendler[art], lit = art === "gross" ? "d" : "c";
    let base = 0, stufe = "";
    T.forEach(([ab, e], j) => { const drin = j === 0 ? km >= ab : km > ab; if (drin) { base = e; stufe = `${j === 0 ? "ab" : "über"} ${ab} km${T[j + 1] ? ` bis ${T[j + 1][0]} km` : ""}`; } });
    if (!base) return { result: eur(0), label: "kein Pendlerpauschale (Regeln 2026)", k: [["Pendlerpauschale pro Jahr", 0, "eur"], ["Pendlereuro pro Jahr", 0, "eur"]],
      steps: [line(art === "gross" ? `Das große Pendlerpauschale beginnt bei mindestens ${T[0][0]} km einfacher Strecke (§ 16 Abs. 1 Z 6 lit. d EStG 1988).` : `Das kleine Pendlerpauschale beginnt bei mindestens ${T[0][0]} km einfacher Strecke (§ 16 Abs. 1 Z 6 lit. c EStG 1988).`),
        line(`Bei ${nf(km, 0)} km steht deshalb weder ein Pendlerpauschale noch ein Pendlereuro zu. Die Fahrtkosten sind mit dem Verkehrsabsetzbetrag abgegolten (lit. a).`),
        ...(art === "klein" && km >= S.pendler.gross[0][0] ? [line(`Ist ein Massenverkehrsmittel mindestens auf der halben Strecke nicht zumutbar, kommt ab ${S.pendler.gross[0][0]} km das große Pendlerpauschale in Frage.`)] : [])] };
    const [z, n, wort] = tage >= 11 ? [1, 1, "voll"] : tage >= 8 ? [2, 3, "zu zwei Dritteln"] : tage >= 4 ? [1, 3, "zu einem Drittel"] : [0, 1, "nicht"];
    const pp = base * z / n, pe = S.pendlereuro * km * z / n;
    const st = [line(`Sätze für das Kalenderjahr 2026 – nicht für 2025; die verwendeten Fassungen gelten bis 31.12.2026.`), line(`${art === "gross" ? "Großes" : "Kleines"} Pendlerpauschale, Stufe „${stufe}“: ${eur(base)} jährlich (§ 16 Abs. 1 Z 6 lit. ${lit} EStG 1988)`),
      line(`${nf(tage, 0)} Fahrten im Kalendermonat: Das Pauschale steht ${wort} zu (lit. e: ab 11 Tagen voll, 8 bis 10 Tage zwei Drittel, 4 bis 7 Tage ein Drittel).`),
      line(`Pendlerpauschale${n > 1 ? ` = ${eur(base)} × ${z}/${n} =` : z ? ":" : ` = ${eur(base)} × 0 =`} <mark>${eur(pp)}</mark> pro Jahr, das sind ${eur(pp / 12)} pro Monat (Freibetrag)`),
      line(`Pendlereuro = ${nf(km, 0)} km × ${eur(S.pendlereuro)}${n > 1 ? ` × ${z}/${n}` : z ? "" : " × 0"} = <b>${eur(pe)}</b> pro Jahr (Absetzbetrag, § 33 Abs. 5 Z 4 EStG 1988)`)];
    const k = [["Pendlerpauschale pro Jahr", pp, "eur"], ["Pendlereuro pro Jahr", pe, "eur"]];
    if (gs > 0) { const ent = pp * gs / 100 + pe; st.push(line(`Überschlag mit ${pc(gs, 0)} Grenzsteuersatz: ${eur(pp)} × ${nf(gs / 100, 2)} + ${eur(pe)} = ${eur(ent)} weniger Lohnsteuer im Jahr`)); k.push(["Steuerentlastung (Überschlag)", ent, "eur"]); }
    else st.push(line(`Der Freibetrag senkt die Steuer um deinen Grenzsteuersatz, der Pendlereuro in voller Höhe. Wähle oben einen Grenzsteuersatz für den Überschlag.`));
    return { result: eur(pp), label: "Pendlerpauschale 2026 pro Jahr (Freibetrag)", steps: st, k };
  };

  /* Verzugszinsen: taggenau, je Halbjahr mit dem dann geltenden Basiszinssatz; Zinstage ÷ Tage des Kalenderjahres; keine Zinseszinsen */
  const tag = s => { const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s || "").trim()); if (!m) return NaN; const t = Date.UTC(+m[1], +m[2] - 1, +m[3]); const d = new Date(t); return d.getUTCFullYear() === +m[1] && d.getUTCMonth() === +m[2] - 1 && d.getUTCDate() === +m[3] ? t : NaN; };
  const TAG = 864e5, dat = t => { const d = new Date(t); return `${d.getUTCDate()}.${d.getUTCMonth() + 1}.${d.getUTCFullYear()}`; };
  C.verzug = f => {
    const land = sel(f, "land"), B = val(f, "betrag"), von = tag(sel(f, "von")), bis = tag(sel(f, "bis"));
    const W = { de_v: ["de", S.verzug.de_v, "§ 288 Abs. 1 BGB"], de_u: ["de", S.verzug.de_u, "§ 288 Abs. 2 BGB"], at_u: ["at", S.verzug.at_u, "§ 456 UGB"], at_a: ["atTag", S.verzug.at_a, "§ 49a ASGG"], at_v: ["", S.verzug.at_v, "§ 1000 Abs. 1, § 1333 Abs. 1 ABGB"] }[land];
    if (!W) return bad("Bitte eine Rechtsgrundlage auswählen.");
    if (!Number.isFinite(B) || B <= 0 || B > 1e9) return bad("Bitte den offenen Betrag eingeben (größer als 0).");
    if (!Number.isFinite(von) || !Number.isFinite(bis)) return bad("Bitte ersten und letzten Zinstag als Datum eingeben.");
    const min = tag(S.verzugAb), max = tag(S.verzugBis);
    if (von < min) return bad(`Der Rechner kennt die Basiszinssätze ab ${dat(min)}. Bitte einen späteren ersten Zinstag wählen.`);
    if (bis > max) return bad(`Der Basiszinssatz steht nur bis ${dat(max)} fest. Bitte einen früheren letzten Zinstag wählen.`);
    if (bis < von) return bad("Der letzte Zinstag liegt vor dem ersten.");
    const fest = land === "at_a";   // § 49a ASGG: Basiszinssatz vom Tag nach der Fälligkeit (= erster Zinstag), für den ganzen Zeitraum
    const basis = t => { if (!W[0]) return 0; const iso = new Date(fest ? von : t).toISOString().slice(0, 10); let v = NaN; for (const [ab, w] of S.basis[W[0]]) if (ab <= iso) v = w; return v; };
    const rows = []; let sum = 0, tage = 0, a = von;
    while (a <= bis) {
      const d = new Date(a), y = d.getUTCFullYear(), h2 = d.getUTCMonth() >= 6;
      const ende = Math.min(bis, h2 ? Date.UTC(y, 11, 31) : Date.UTC(y, 5, 30));
      const n = Math.round((ende - a) / TAG) + 1, jahr = (Date.UTC(y + 1, 0, 1) - Date.UTC(y, 0, 1)) / TAG;
      const b = basis(a), satz = W[0] ? b + W[1] : W[1], z = Math.round(B * satz / 100 * n / jahr * 100 + 1e-7) / 100;   // je Teilzeitraum auf Cent gerundet, damit Zeilen und Summe zusammenpassen
      if (!Number.isFinite(satz)) return bad("Für diesen Zeitraum liegt kein Basiszinssatz vor.");
      rows.push({ a, ende, n, jahr, b, satz, z }); sum += z; tage += n; a = ende + TAG;
    }
    const st = [line(fest ? `Zinssatz = Basiszinssatz am ${dat(von)} (${nf(basis(von), 2)} %) + ${nf(W[1], 1)} Prozentpunkte (${W[2]}: maßgeblich ist der Tag nach dem Eintritt der Fälligkeit – hier der erste Zinstag).` : W[0] ? `Zinssatz = Basiszinssatz + ${nf(W[1], 1)} Prozentpunkte (${W[2]}); der Basiszinssatz wird je Halbjahr angesetzt.` : `Zinssatz = ${nf(W[1], 0)} % pro Jahr, fest (${W[2]}).`)];
    rows.forEach(r => st.push(line(`${dat(r.a)} bis ${dat(r.ende)}: ${eur(B)} × ${pc(r.satz)}${W[0] ? ` (${nf(r.b, 2)} + ${nf(W[1], 1)})` : ""} × ${r.n} ÷ ${r.jahr} Tage = ${eur(r.z)}`)));
    st.push(line(`Summe${rows.length > 1 ? " der gerundeten Teilbeträge" : ""}: <mark>${eur(sum)}</mark> für ${nf(tage, 0)} Zinstage · Forderung samt Zinsen: ${eur(B + sum)}`));
    if (land === "de_u" || land === "at_u") st.push(line(`Zusätzlich kann der Gläubiger eine Pauschale von 40 € verlangen (${land === "de_u" ? "§ 288 Abs. 5 BGB" : "§ 458 UGB"}); sie ist hier nicht eingerechnet.`));
    if (land === "at_v") st.push(line(`Die 4 % gelten nur, soweit keine Sonderregel greift: zwischen Unternehmern § 456 UGB, bei Forderungen aus einem Arbeitsverhältnis § 49a ASGG.`));
    if (fest) st.push(line(`Beruht die Verzögerung auf einer vertretbaren Rechtsansicht des Schuldners, gelten nach § 49a ASGG nur die sonstigen gesetzlichen Zinsen.`));
    st.push(line(`Einfache Zinsen ohne Zinseszins; erster und letzter Zinstag zählen mit. Basiszinssätze bis ${dat(max)}.`));
    const table = `<div class="scroll"><table class="tbl small"><thead><tr><th>Zeitraum</th><th>Tage</th><th>Zinssatz</th><th>Zinsen</th></tr></thead><tbody>${rows.map(r => `<tr><td>${dat(r.a)}–${dat(r.ende)}</td><td>${r.n}</td><td>${pc(r.satz)}</td><td>${eur(r.z)}</td></tr>`).join("")}</tbody></table></div>`;
    return { result: eur(sum), label: `Verzugszinsen für ${nf(tage, 0)} Tage`, steps: st, extra: table, k: [["Verzugszinsen", sum, "eur"], ["Forderung samt Zinsen", B + sum, "eur"], ["Zinstage", tage, "Tage"]],
      csv: { name: "verzugszinsen", head: ["Von", "Bis", "Tage", "Zinssatz in %", "Zinsen in Euro"], rows: rows.map(r => [dat(r.a), dat(r.ende), String(r.n), nf(r.satz), nf(r.z)]) } };
  };

  function run(form) {
    const fn = C[form.dataset.calc]; if (!fn) return;
    let r; try { r = fn(form); } catch (e) { r = bad("Bitte die Eingaben prüfen."); }
    const out = $(`[data-out="${form.id}"]`) || form.querySelector("[data-out]"); if (!out || !r) return;
    if (!r.result) { form._rk = null; out.innerHTML = `<p class="hint">${r.note}</p>`; return; }
    form._rk = r; form._cmp = vergleich(form, r);
    const acts = `<div class="acts no-print"><button type="button" class="btn-beleg" data-pin>${form._A ? "Szenario A neu setzen" : "Als Szenario A merken"}</button>${form._A ? `<button type="button" class="btn-beleg" data-unpin>Vergleich beenden</button>` : ""}<button type="button" class="btn-beleg" data-copy>Ergebnis kopieren</button><button type="button" class="btn-beleg" data-share>Link kopieren</button><button type="button" class="btn-beleg" data-beleg>Als Beleg drucken oder PDF</button>${r.csv ? `<button type="button" class="btn-beleg" data-csv>Tabelle als CSV</button>` : ""}</div>`;
    out.innerHTML = `<div class="res"><span class="res-label">${r.label || "Ergebnis"}</span><output class="res-val">${r.result}</output></div><h3 class="way-h">Rechenweg</h3><ol class="way">${r.steps.join("")}</ol>${form._cmp}${r.pre || ""}${r.extra || ""}${acts}${form._A ? "" : `<p class="small muted no-print">Szenario merken, dann Werte ändern: Der Rechner zeigt beide Ergebnisse nebeneinander.</p>`}`;
    clearTimeout(form._rkT); form._rkT = setTimeout(() => remember(form, r), 1500);
  }

  /* ---------- Ereignisse für Google Analytics (wirken nur nach Einwilligung, siehe consent.js) */
  const track = (name, p = {}) => { try { if (typeof window.gtag === "function" && window["ga-disable-G-T00HRG2YVF"] === false) window.gtag("event", name, p); } catch (e) {} };
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const plain = s => String(s).replace(/<[^>]*>/g, "").replace(/&nbsp;/g, " ");
  const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }, del(k) { try { localStorage.removeItem(k); } catch (e) {} } };

  /* ---------- Vergleich zweier Szenarien: A wird gemerkt, die aktuelle Eingabe ist B. Nichts davon wird gespeichert. */
  const kennzahlen = r => { if (r.k) return r.k; const x = num(plain(r.result).replace(/[^\d,.\-]/g, "")); return Number.isFinite(x) ? [[plain(r.label || "Ergebnis"), x, /%/.test(r.result) ? "pct" : /€/.test(r.result) ? "eur" : "num"]] : []; };
  const zeig = (v, u) => u === "eur" ? eur(v) : u === "pct" ? pc(v) : u === "num" ? nf(v, 4) : `${nf(v, 2)} ${u}`;
  const diff = (a, b, u) => { const d = b - a; if (Math.abs(d) < 5e-7) return "gleich"; const vz = d > 0 ? "+" : "−", ab = Math.abs(d);
    if (u === "pct") return `${vz}${nf(ab, 2)} Prozentpunkte`;
    return `${vz}${zeig(ab, u)}${a !== 0 ? ` (${vz}${pc(ab / Math.abs(a) * 100, 1)})` : ""}`; };
  function vergleich(f, r) {
    const A = f._A; if (!A) return "";
    const ka = kennzahlen(A.r), kb = kennzahlen(r), rows = [];
    kb.forEach(([n, v, u]) => { const x = ka.find(y => y[0] === n && y[2] === u); if (x) rows.push(`<tr><td>${esc(n)}</td><td>${zeig(x[1], u)}</td><td>${zeig(v, u)}</td><td>${diff(x[1], v, u)}</td></tr>`); });
    const jetzt = inputsOf(f), anders = [];
    jetzt.forEach(([n, v]) => { const x = A.inputs.find(y => y[0] === n); if (x && x[1] !== v) anders.push(`${esc(n)}: ${esc(x[1])} → ${esc(v)}`); });
    const kopf = `<h3 class="way-h">Vergleich: Szenario A und B</h3>`;
    if (!rows.length) return `<div class="cmp">${kopf}<p class="small">A: ${esc(plain(A.r.label || ""))} ${esc(plain(A.r.result))} · B: ${esc(plain(r.label || ""))} ${esc(plain(r.result))}. Die beiden Rechnungen haben keine gemeinsame Kennzahl – für eine Gegenüberstellung dieselbe Rechenart wählen.</p></div>`;
    return `<div class="cmp">${kopf}<div class="scroll"><table class="tbl small"><thead><tr><th></th><th>A (gemerkt)</th><th>B (jetzt)</th><th>B gegenüber A</th></tr></thead><tbody>${rows.join("")}</tbody></table></div><p class="small muted">${anders.length ? `Geändert: ${anders.join(" · ")}` : "Noch nichts geändert – ändere oben einen Wert, um Szenario B zu rechnen."}</p></div>`;
  }
  function merke(f) { const r = f._rk; if (!r || !r.result) return; f._A = { r, inputs: inputsOf(f), q: params(f).toString() }; }

  /* ---------- CSV: Strichpunkt-getrennt mit BOM für Tabellenprogramme. Zellen, die als Formel gelesen würden (= + - @ Tab), bekommen ein Hochkomma. */
  const zelle = v => { let s = String(v == null ? "" : v).replace(/\r?\n/g, " "); if (/^[=+\-@\t\r]/.test(s) && !/^-?\d+([.,]\d+)*$/.test(s)) s = "'" + s; return `"${s.replace(/"/g, '""')}"`; };
  const csvText = (head, rows) => "\ufeff" + [head, ...rows].map(z => z.map(zelle).join(";")).join("\r\n") + "\r\n";
  function laden(name, text) {
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([text], { type: "text/csv;charset=utf-8" })); a.download = `rechenklarheit-${name}.csv`;
    document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }
  async function kopiere(text, b, ok) {
    try { await navigator.clipboard.writeText(text); b.textContent = ok; }
    catch (e) { const t = document.createElement("textarea"); t.className = "sharelink"; t.readOnly = true; t.value = text; t.setAttribute("aria-label", "Zum Kopieren markiert"); b.replaceWith(t); t.focus(); t.select(); }
  }
  function alsText(f) {
    const r = f._rk, h1 = document.querySelector("h1")?.textContent.trim() || "Rechnung";
    const z = [`${h1} – Rechenklarheit`, `${plain(r.label || "Ergebnis")}: ${plain(r.result)}`, "", "Eingaben:", ...inputsOf(f).map(([k, v]) => `  ${k}: ${v}`), "", "Rechenweg:", ...r.steps.map((s, i) => `  ${i + 1}. ${plain(s)}`)];
    if (f._A) { const ka = kennzahlen(f._A.r); z.push("", "Vergleich mit Szenario A:"); kennzahlen(r).forEach(([n, v, u]) => { const x = ka.find(y => y[0] === n && y[2] === u); if (x) z.push(`  ${n}: A ${zeig(x[1], u)} · B ${zeig(v, u)} · ${diff(x[1], v, u)}`); }); }
    z.push("", `Nachrechnen: ${link(f)}`, "Ohne Gewähr. Keine Steuer-, Rechts- oder Finanzberatung.");
    return z.join("\n");
  }
  const link = f => { const q = params(f); if (f._A) q.set("vgl", f._A.q); return `${location.origin}${location.pathname}?${q}`; };

  /* ---------- Beleg: Ergebnis mit Eingaben und Rechenweg als druckbares Blatt (Drucken oder „Als PDF sichern“) */
  function inputsOf(f) {
    const rows = [];
    [...f.elements].forEach(el => {
      if (!el.name || el.closest("[hidden]") || el.name === "preset" || el.type === "button") return;
      const lab = el.closest("label"); let t = lab ? (lab.querySelector("[data-l]")?.textContent || lab.firstChild?.textContent || el.name) : el.name;
      const leg = el.closest("fieldset")?.querySelector("legend")?.textContent;
      if (leg) t = `${leg}: ${t}`;
      const v = el.tagName === "SELECT" ? el.options[el.selectedIndex]?.text : el.value;
      if (String(v).trim() !== "") rows.push([t.trim(), v]);
    });
    return rows;
  }
  function beleg(f) {
    const r = f._rk; if (!r || !r.result) return;
    const now = new Date(), url = link(f);
    const h1 = document.querySelector("h1")?.textContent || "Rechnung";
    let el = document.getElementById("beleg");
    if (!el) { el = document.createElement("div"); el.id = "beleg"; document.body.appendChild(el); }
    el.innerHTML = `<div class="b-head">RECHENKLARHEIT · BELEG</div><h2>${esc(h1)}</h2>
<p class="b-meta">${now.toLocaleDateString("de-AT")} · ${now.toLocaleTimeString("de-AT", { hour: "2-digit", minute: "2-digit" })}</p>
<table>${inputsOf(f).map(([k, v]) => `<tr><td>${esc(k)}</td><td>${esc(v)}</td></tr>`).join("")}</table>
<div class="b-sum"><span>${esc(plain(r.label || "Ergebnis"))}</span><strong>${esc(plain(r.result))}</strong></div>
<h3>Rechenweg</h3><ol>${r.steps.join("")}</ol>${f._cmp || ""}${r.extra || ""}
<p class="b-foot">Ohne Gewähr. Ersetzt keine Steuer-, Rechts- oder Finanzberatung.<br>Rechnung nachvollziehen: ${esc(url)}</p>`;
    document.body.classList.add("beleg-druck");
    const done = () => { document.body.classList.remove("beleg-druck"); window.removeEventListener("afterprint", done); };
    window.addEventListener("afterprint", done);
    track("beleg_drucken", { rechner: f.dataset.calc });
    window.print();
  }

  /* ---------- Verlauf „Meine letzten Rechnungen“: nur im Browser (localStorage „rk-verlauf“), max. 12 Einträge */
  const VKEY = "rk-verlauf";
  const loadV = () => { try { const v = JSON.parse(store.get(VKEY) || "[]"); return Array.isArray(v) ? v.filter(x => x && typeof x.url === "string" && x.url.startsWith("/") && !x.url.startsWith("//")) : []; } catch (e) { return []; } };
  const VAN = "rk-verlauf-an";
  const verlaufAn = () => store.get(VAN) === "1";
  function remember(f, r) {
    if (!r || !r.result || !verlaufAn()) return;
    const url = `${location.pathname}?${params(f)}`;
    const h1 = (document.querySelector("h1")?.textContent || "").slice(0, 60);
    const list = loadV().filter(x => x.url !== url);
    list.unshift({ t: h1, l: plain(r.label || "").slice(0, 60), r: plain(r.result).slice(0, 30), url, ts: Date.now() });
    store.set(VKEY, JSON.stringify(list.slice(0, 12)));
    showV();
  }
  function showV() {
    const list = loadV();
    $$("[data-verlauf]").forEach(box => {
      box.hidden = false;
      const an = verlaufAn(), cb = $("[data-verlauf-an]", box);
      if (cb) cb.checked = an;
      $$("[data-verlauf-teil]", box).forEach(e => { e.hidden = !an || !list.length; });
      const ol = $("ol", box); if (!ol) return;
      ol.innerHTML = list.map(x => `<li><a href="${esc(x.url)}"><span>${esc(x.t)}</span><b>${esc(x.r)}</b></a><small>${esc(x.l)}</small></li>`).join("");
    });
  }
  document.addEventListener("change", e => {
    const cb = e.target.closest("[data-verlauf-an]"); if (!cb) return;
    if (cb.checked) { store.set(VAN, "1"); $$("form[data-calc]").forEach(f => f._rk && remember(f, f._rk)); track("verlauf_an"); }
    else { store.del(VAN); store.del(VKEY); }
    showV();
  });
  document.addEventListener("click", e => {
    if (e.target.closest("[data-beleg]")) beleg(e.target.closest("form"));
    const pin = e.target.closest("[data-pin],[data-unpin]");
    if (pin) { const f = pin.closest("form"); if (pin.hasAttribute("data-pin")) { merke(f); track("szenario_merken", { rechner: f.dataset.calc }); } else f._A = null; run(f); (f.querySelector(f._A ? "[data-unpin]" : "[data-pin]") || f).focus(); }
    const cp = e.target.closest("[data-copy]"); if (cp) { const f = cp.closest("form"); if (f._rk) kopiere(alsText(f), cp, "Kopiert ✓"); track("ergebnis_kopieren", { rechner: f.dataset.calc }); }
    const cs = e.target.closest("[data-csv]"); if (cs) { const f = cs.closest("form"), c = f._rk && f._rk.csv; if (c) laden(c.name, csvText(c.head, c.rows)); }
    const ex = e.target.closest("[data-ex]"); if (ex) { const f = document.getElementById(ex.dataset.for) || ex.closest("form"); if (f) { setze(f, new URLSearchParams(ex.dataset.ex)); sync(f); run(f); $$("[data-ex]", ex.parentNode).forEach(b => b.setAttribute("aria-pressed", b === ex ? "true" : "false")); track("beispiel", { rechner: f.dataset.calc }); } }
    if (e.target.closest("[data-verlauf-clear]")) { store.del(VKEY); showV(); track("verlauf_loeschen"); }
    if (e.target.closest("[data-verlauf] a")) track("verlauf_oeffnen");
    if (e.target.closest("[data-share]")) track("link_teilen", { rechner: e.target.closest("form")?.dataset.calc });
    const buy = e.target.closest("[data-shop-buy]"); if (buy) track("shop_kaufen_klick", { produkt: buy.dataset.shopBuy });
  });

  function params(f) {
    const q = new URLSearchParams();
    [...f.elements].forEach(el => { if (el.name && !el.closest("[hidden]") && el.name !== "preset") q.set(el.name, el.value); });
    return q;
  }
  function setze(f, q) {
    ["mode", "fuel", "cat", "dir", "land"].forEach(k => { if (q.has(k) && f.elements[k]) f.elements[k].value = q.get(k); });
    if (f.elements.cat) run(f); // Einheiten-Optionen aufbauen
    if (f.dataset.calc === "fahrt") f.dataset.fuel = sel(f, "fuel");
    if (f.dataset.calc === "marge") f.dataset.mode = sel(f, "mode");
    if (f.elements.preset) { f.elements.preset.value = ""; }
    q.forEach((v, k) => { const el = f.elements[k]; if (el && !(el instanceof RadioNodeList)) el.value = v; });
  }
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-share]"); if (!b) return;
    const f = b.closest("form"), url = link(f);
    kopiere(url, b, "Link kopiert ✓");
    history.replaceState(null, "", url);
  });
  /* Abhängige Anzeige nach programmatischem Setzen: ein-/ausgeblendete Felder und Beschriftungen */
  function sync(f) {
    $$("[data-show-when]", f).forEach(el => { const [name, v] = el.dataset.showWhen.split("="); el.hidden = sel(f, name) !== v; });
    if (f._sync) f._sync();
  }

  /* ---------- Filter für Referenztabellen: Suche über alle Spalten, Land und Thema; angezeigte Zeilen als CSV */
  function filter(form) {
    const tb = document.getElementById(form.dataset.filter); if (!tb) return;
    const zeilen = $$("tbody tr", tb), norm = s => String(s).toLowerCase().replace(/\s+/g, " ");
    const upd = () => {
      const q = norm(form.elements.q.value).split(" ").filter(Boolean), land = form.elements.land.value, th = form.elements.thema.value; let n = 0;
      zeilen.forEach(tr => { const t = norm(tr.textContent); const ok = (!land || tr.dataset.land === land) && (!th || tr.dataset.thema === th) && q.every(w => t.includes(w)); tr.hidden = !ok; if (ok) n++; });
      const c = $(`[data-filter-count="${form.dataset.filter}"]`), leer = $(`[data-filter-empty="${form.dataset.filter}"]`);
      if (c) c.textContent = n === zeilen.length ? `${n} Einträge` : `${n} von ${zeilen.length} Einträgen`;
      if (leer) leer.hidden = n > 0;
    };
    form.addEventListener("input", upd); form.addEventListener("change", upd);
    $("[data-filter-reset]", form)?.addEventListener("click", () => { form.reset(); upd(); form.elements.q.focus(); });
    $("[data-filter-csv]", form)?.addEventListener("click", () => {
      const head = ["Land", "Thema", "Was", "Hinweis", "Wert", "Fundstelle", "Link", "Fassung und Abruf"];
      const t = (el, s) => (s ? el.querySelector(s) : el)?.textContent.trim() || "";
      const rows = zeilen.filter(tr => !tr.hidden).map(tr => { const c = tr.cells; return [c[0].firstChild.textContent.trim(), tr.dataset.thema, t(c[1], "b"), t(c[1], ".rf-h"), t(c[2]), t(c[3], "a"), c[3].querySelector("a")?.href || "", t(c[3], ".rf-h")]; });
      laden("saetze-und-grenzwerte", csvText(head, rows));
    });
    const q0 = new URLSearchParams(location.search).get("q"); if (q0) form.elements.q.value = q0.slice(0, 80);
    upd();
  }

  function init() {
    showV();
    $$("form[data-filter]").forEach(filter);
    $$("form[data-calc]").forEach(f => {
      if (f.dataset.calc === "percent") { // Modus-Beschriftungen des Prozentrechners
        const L = { anteil: ["Grundwert", "Prozentsatz (%)"], satz: ["Prozentwert", "Grundwert"], grund: ["Prozentwert", "Prozentsatz (%)"], veraenderung: ["Alter Wert", "Neuer Wert"], rabatt: ["Preis (€)", "Rabatt (%)"], ursprung: ["Endpreis (€)", "Rabatt (%)"] };
        f._sync = () => { const p = L[sel(f, "mode")]; if (p) { $("[data-l=a]", f).textContent = p[0]; $("[data-l=b]", f).textContent = p[1]; } };
      }
      const q = new URLSearchParams(location.search), vgl = q.get("vgl"); q.delete("vgl"); q.delete("q");
      if (vgl) { setze(f, new URLSearchParams(vgl)); sync(f); run(f); merke(f); }   // geteilter Link mit Vergleich: zuerst Szenario A
      if ([...q.keys()].length) setze(f, q);
      f.addEventListener("input", () => run(f));
      f.addEventListener("change", () => { sync(f); run(f); });
      f.addEventListener("submit", e => { e.preventDefault(); run(f); });
      sync(f); run(f);
    });
  }
  window.RK_CALC = C; window.RK_CSV = { zelle, csvText }; // für automatische Tests
  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", init) : init();
})();
