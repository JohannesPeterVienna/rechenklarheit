/* Anzeigenplätze im ersten Bildschirm (Playwright/Chromium), nach dem Bauen: node test_erster_bildschirm.js
   Läuft über alle Seiten der Sitemap bei 1366×768 und 390×844. Ein Stub ersetzt adsbygoogle.js; die Plätze werden
   gefüllt simuliert (data-ad-status="filled", responsive Blöcke bekommen ihre Zielgröße).
   Prüft: Kopfplatz vollständig im ersten Bildschirm und im erwarteten Format · Half-Page der Lese-Seiten beginnt im ersten
   Bildschirm · jeder Platz ≥ 150 px von jedem Bedienelement (Formularfelder, Knöpfe, Beispiel-Chips, Filter, Verlauf) ·
   Abstand zu Navigations- und Brotkrumen-Links · Überschrift und Beginn von Inhalt bzw. Rechner ohne Scrollen sichtbar ·
   mobil höchstens ein flacher Platz im ersten Bildschirm und Anzeigenanteil < 30 % der Inhaltshöhe (Better Ads Standards) ·
   kein horizontaler Überlauf · keine JS-Fehler · kein Layout-Sprung beim Einfügen und Füllen (CLS) ·
   "unfilled", GPC und blockierter Loader: kein freigehaltener Platz · Seiten ohne Werbung bleiben ohne Platz.
   ($$eval ist die Playwright-Abfrage im Browser der Testseite, kein eval von Fremdtext.) */
"use strict";
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");

const DOCS = path.join(__dirname, "docs");
const MIME = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".png": "image/png", ".xml": "text/xml" };
const STUB = "(window.adsbygoogle = window.adsbygoogle || []).loaded = true;";   // Loader „geladen“, liefert aber nie eine Anzeige
const ABSTAND = 150, LINK_ABSTAND = 40;
let fails = 0, checks = 0;
function check(ok, msg){ checks++; if (!ok) { fails++; console.log("  FAIL " + msg); } }

/* Im Browser: Plätze füllen und vermessen */
function vermessen(){
  document.querySelectorAll(".ad.on ins.adsbygoogle").forEach(i => {
    const b = i.parentElement, k = b.dataset.ad, cw = b.parentElement.getBoundingClientRect().width;
    if (!i.style.height) {      // responsiver Block: Zielgröße wie von Google zu erwarten
      const [w, h] = k === "half" ? [300, 600] : k === "rect" ? (cw >= 336 ? [336, 280] : [300, 250]) : cw >= 728 ? [728, 90] : [Math.min(cw, 336), 280];
      i.style.cssText += `;display:inline-block;width:${w}px;height:${h}px`;
    }
    i.setAttribute("data-ad-status", "filled");
  });
  const R = e => { const b = e.getBoundingClientRect(); return { l: b.left, r: b.right, t: b.top + scrollY, b: b.bottom + scrollY, w: b.width, h: b.height }; };
  const da = e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.height > 0 && getComputedStyle(e).visibility !== "hidden"; };
  const weg = (a, b) => Math.hypot(Math.max(0, a.l - b.r, b.l - a.r), Math.max(0, a.t - b.b, b.t - a.b));
  const name = e => e.tagName.toLowerCase() + (e.name ? `[${e.name}]` : "") + (e.className ? "." + String(e.className).split(" ")[0] : "");
  const bedien = [...document.querySelectorAll("input, select, textarea, button, summary, a.btn-beleg, .chip")].filter(da).map(e => ({ r: R(e), n: name(e) }));
  const links = [...document.querySelectorAll("header a, .crumbs a")].filter(da).map(e => ({ r: R(e), n: name(e) }));
  const naechst = (r, liste) => liste.reduce((m, c) => { const d = weg(r, c.r); return d < m.d ? { d, n: c.n } : m; }, { d: Infinity, n: "–" });
  const ads = [...document.querySelectorAll(".ad.on")].filter(da).map(b => { const r = R(b.querySelector("ins")), m = naechst(r, bedien), l = naechst(r, links);
    return { art: b.dataset.ad, w: Math.round(r.w), h: Math.round(r.h), oben: Math.round(r.t), unten: Math.round(r.b), rechts: r.r, abstand: Math.round(m.d), an: m.n, link: Math.round(l.d),
             label: getComputedStyle(b, "::before").content.includes("Werbung"), imInhalt: !!b.closest("main") && !b.closest("aside") && !b.matches(".ad--superbanner,.ad--mbanner") }; });
  const q = s => document.querySelector(s), top = s => q(s) ? Math.round(R(q(s)).t) : null;
  const inhalt = q("main article, main .layout > div") || q("main");
  return { ads, h1: R(q("h1")), text: top(".lead, main p"), blatt: top(".sheet"), feld: top("form[data-calc] input, form[data-calc] select"),
           inhaltH: R(q("main")).h - (q("aside.side") && getComputedStyle(q(".layout")).gridTemplateColumns.split(" ").length === 1 ? R(q("aside.side")).h : 0),
           ueber: document.documentElement.scrollWidth - document.documentElement.clientWidth, plaetze: document.querySelectorAll(".platz").length };
}

(async () => {
  const server = http.createServer((req, res) => {
    const f = path.join(DOCS, decodeURIComponent(req.url.split("?")[0]).replace(/\/$/, "/index.html"));
    if (!f.startsWith(DOCS) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "content-type": MIME[path.extname(f)] || "application/octet-stream" }); res.end(fs.readFileSync(f));
  });
  await new Promise(r => server.listen(0, "127.0.0.1", r));
  const BASE = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  const seiten = [...fs.readFileSync(path.join(DOCS, "sitemap.xml"), "utf8").matchAll(/<loc>https:\/\/rechenklarheit\.de([^<]*)<\/loc>/g)].map(m => m[1]);
  const quelle = s => fs.readFileSync(path.join(DOCS, s === "/" ? "index.html" : s.slice(1)), "utf8");
  const art = s => /<form data-calc=/.test(quelle(s)) ? "rechner" : /class="rf-filter/.test(quelle(s)) ? "tabelle" : "lesen";

  async function oeffnen(vw, vh, pfad, opt = {}){
    const ctx = await browser.newContext({ viewport: { width: vw, height: vh } });
    await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => opt.blockiert ? r.abort() : r.fulfill({ status: 200, contentType: "text/javascript", body: STUB }));
    await ctx.addInitScript(gpc => {
      if (gpc) Object.defineProperty(Navigator.prototype, "globalPrivacyControl", { get: () => true });
      window.__cls = 0; window.__kopfSprung = 0;      // __kopfSprung: Verschiebungen, die Kopfbereich, Überschrift oder einen freigehaltenen Platz treffen
      try { new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) { window.__cls += e.value;
        const h1 = document.querySelector("h1");
        if (e.sources.some(s => s.node && s.node.nodeType === 1 && (s.node.contains(h1) || s.node.closest(".platz, header") || s.node.querySelector(".platz")))) window.__kopfSprung += e.value; } }).observe({ type: "layout-shift", buffered: true }); } catch (_) {}
    }, Boolean(opt.gpc));
    const page = await ctx.newPage(); const fehler = [];
    page.on("pageerror", e => fehler.push(e.message));
    page.on("console", m => { if (m.type() === "error" && !/Failed to load resource|ERR_FAILED|ERR_BLOCKED/.test(m.text())) fehler.push(m.text()); });
    await page.goto(BASE + pfad, { waitUntil: "load" });
    await page.waitForTimeout(250);
    return { ctx, page, fehler };
  }
  const cls = page => page.evaluate(() => new Promise(r => requestAnimationFrame(() => setTimeout(() => r(window.__cls), 120))));

  // ---------- 1. Alle Seiten der Sitemap, gefüllt
  const zeilen = [];
  for (const [vw, vh] of [[1366, 768], [390, 844]]) for (const s of seiten) {
    const typ = art(s), mobil = vw < 768, wo = `${vw} px ${s}`;
    const { ctx, page, fehler } = await oeffnen(vw, vh, s);
    const vorher = await cls(page), kopfSprung = await page.evaluate(() => window.__kopfSprung);
    check(kopfSprung === 0, `${wo}: Einfügen der Plätze verschiebt Überschrift und Kopfbereich nicht (${kopfSprung.toFixed(3)})`);
    const m = await page.evaluate(vermessen);
    const beimFuellen = await cls(page) - vorher;
    check(beimFuellen < 0.01, `${wo}: Füllen verschiebt nichts im Bildschirm (CLS ${beimFuellen.toFixed(3)})`);
    const kopf = m.ads.find(a => a.art === "kopf" || a.art === "kopfflach");
    const soll = mobil ? [320, 100] : typ === "rechner" ? [970, 90] : [970, 250];
    check(kopf && m.ads.indexOf(kopf) === 0, `${wo}: Kopfplatz vorhanden und oberster Platz`);
    if (kopf) {
      check(kopf.w === soll[0] && kopf.h === soll[1], `${wo}: Kopfplatz ${kopf.w}×${kopf.h}, erwartet ${soll.join("×")}`);
      check(kopf.oben >= 0 && kopf.unten <= vh, `${wo}: Kopfplatz vollständig im ersten Bildschirm (${kopf.oben}–${kopf.unten})`);
      check(kopf.unten < m.h1.t, `${wo}: Kopfplatz steht über der Überschrift`);
      check(kopf.link >= LINK_ABSTAND, `${wo}: Kopfplatz ${kopf.link} px von Navigations-/Brotkrumen-Links`);
      check(kopf.label, `${wo}: Kopfplatz mit „Werbung“ beschriftet`);
    }
    for (const a of m.ads) check(a.abstand >= ABSTAND, `${wo}: ${a.art} nur ${a.abstand} px von ${a.an}`);
    check(m.ads.every(a => a.rechts <= vw + 0.5) && m.ueber <= 0, `${wo}: kein horizontaler Überlauf (${m.ueber})`);
    check(m.h1.t >= 0 && m.h1.b <= vh, `${wo}: Überschrift ohne Scrollen sichtbar (${Math.round(m.h1.t)}–${Math.round(m.h1.b)})`);
    check(m.text !== null && m.text < vh - 24, `${wo}: Beginn des Inhalts ohne Scrollen sichtbar (${m.text})`);
    if (typ === "rechner") {
      check(m.feld !== null && m.feld + 44 <= vh, `${wo}: erstes Eingabefeld ohne Scrollen sichtbar (${m.feld})`);
      if (!mobil) check(m.blatt <= vh - 240, `${wo}: Rechner beginnt im ersten Bildschirm mit mindestens 240 px (${m.blatt})`);
    }
    const half = m.ads.find(a => a.art === "half");
    if (!mobil && typ === "lesen") check(half && half.oben < vh && half.w === 300 && half.h === 600, `${wo}: Half-Page 300×600 beginnt im ersten Bildschirm (${half && half.oben})`);
    if (!mobil && typ !== "lesen") check(half && half.oben > vh, `${wo}: Half-Page bleibt unter Rechner bzw. Filter`);
    const erster = m.ads.filter(a => a.oben < vh);
    if (mobil) {
      check(erster.length === 1 && erster[0].h <= 100, `${wo}: im ersten Bildschirm nur ein flacher Platz (${erster.map(a => a.art + " " + a.h).join(", ")})`);
      const anteil = m.ads.filter(a => a.imInhalt).reduce((x, a) => x + a.h, 0) / m.inhaltH;
      check(anteil < 0.3, `${wo}: Anzeigenanteil ${(anteil * 100).toFixed(1)} % der Inhaltshöhe`);
    } else {
      const flaeche = erster.reduce((x, a) => x + a.w * (Math.min(a.unten, vh) - a.oben), 0) / (vw * vh);
      check(flaeche < 0.4, `${wo}: Anzeigenfläche im ersten Bildschirm ${(flaeche * 100).toFixed(0)} %`);
    }
    check(fehler.length === 0, `${wo}: keine JS-Fehler ${fehler.join(" | ")}`);
    if (["/", "/prozentrechner.html", "/prozent-oder-prozentpunkte.html", "/saetze-und-grenzwerte.html"].includes(s))
      for (const a of erster) zeilen.push(`  ${String(vw).padEnd(5)}${s.padEnd(34)}${a.art.padEnd(10)}${(a.w + "×" + a.h).padEnd(9)} oben ${String(a.oben).padStart(4)}  Abstand ${a.abstand}`);
    await ctx.close();
  }
  console.log("Plätze im ersten Bildschirm (gefüllt simuliert):\n" + zeilen.join("\n"));

  // ---------- 2. Zustände der freigehaltenen Plätze
  const hoehen = page => page.$$eval(".platz", l => l.map(p => getComputedStyle(p).display === "none" ? 0 : Math.round(p.getBoundingClientRect().height + parseFloat(getComputedStyle(p).marginTop) + parseFloat(getComputedStyle(p).marginBottom))));
  for (const [vw, vh, pfad, soll] of [[1366, 768, "/prozent-oder-prozentpunkte.html", [290, 650]], [1366, 768, "/prozentrechner.html", [130]], [900, 768, "/prozentrechner.html", [130]], [390, 844, "/prozentrechner.html", [140]]]) {
    const { ctx, page } = await oeffnen(vw, vh, pfad);
    const h = (await hoehen(page)).filter(x => x > 0);
    check(JSON.stringify(h) === JSON.stringify(soll), `${vw} px ${pfad}: freigehaltene Höhe ${h} (erwartet ${soll})`);
    const ins = await page.$$eval(".platz ins.adsbygoogle", l => l.map(i => { const c = getComputedStyle(i), b = i.getBoundingClientRect(); return c.display !== "none" && c.visibility === "visible" && b.width > 0 && b.height > 0 && !getComputedStyle(i.parentElement, "::before").content.includes("Werbung"); }));
    check(ins.length === soll.length && ins.every(Boolean), `${vw} px ${pfad}: ohne Antwort ist das <ins> sichtbar, „Werbung“ steht noch nicht da`);
    const vorher = await cls(page);
    await page.$$eval(".platz ins.adsbygoogle", l => l.forEach(i => i.setAttribute("data-ad-status", "unfilled")));
    await page.waitForTimeout(100);
    check((await hoehen(page)).every(x => x <= 0), `${vw} px ${pfad}: "unfilled" → Platz fällt zusammen`);
    check(await page.$$eval(".platz ins.adsbygoogle", l => l.every(i => getComputedStyle(i).display === "none")), `${vw} px ${pfad}: "unfilled" → ins display:none`);
    console.log(`  Hinweis ${vw} px ${pfad}: Zusammenfallen bei "unfilled" rückt den Inhalt nach oben, CLS ${(await cls(page) - vorher).toFixed(3)} (keine Anzeige im Spiel)`);
    await ctx.close();
  }
  {
    const { ctx, page } = await oeffnen(340, 700, "/prozentrechner.html");
    check((await hoehen(page)).every(x => x <= 0) && await page.$$eval(".platz ins", l => l.length === 0), "340 px: kein Kopfplatz, keine Anfrage");
    check(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth), "340 px: kein horizontaler Überlauf");
    await ctx.close();
  }
  for (const [name, opt] of [["GPC", { gpc: true }], ["Loader blockiert", { blockiert: true }]]) {
    const { ctx, page, fehler } = await oeffnen(1366, 768, "/prozent-oder-prozentpunkte.html", opt);
    check((await hoehen(page)).every(x => x <= 0), `${name}: kein freigehaltener Platz`);
    check(await page.evaluate(() => !document.documentElement.classList.contains("mit-anzeigen")), `${name}: Klasse .mit-anzeigen fehlt`);
    check(fehler.length === 0, `${name}: keine JS-Fehler ${fehler.join(" | ")}`);
    await ctx.close();
  }

  // ---------- 3. Seiten ohne Werbung
  for (const s of ["/imprint.html", "/privacy.html", "/404.html"]) {
    const h = quelle(s);
    check(!/class="[^"]*\b(platz|ad)\b/.test(h) && !/adsbygoogle|mit-anzeigen/.test(h), `${s}: ohne Anzeigenplatz und ohne Loader`);
  }
  check(!fs.existsSync(path.join(DOCS, "shop.html")), "Shop bleibt aus");

  await browser.close(); server.close();
  console.log(fails ? `Erster-Bildschirm-Test: ${fails} von ${checks} Prüfungen fehlgeschlagen` : `Erster-Bildschirm-Test: ${checks} Prüfungen OK`);
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
