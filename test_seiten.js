/* Seiten- und Werkzeugtest im echten Browser (Playwright/Chromium), nach dem Bauen: node test_seiten.js
   1. Alle Seiten der Sitemap bei 390 und 1366 px: keine JS-Fehler, kein seitlicher Überlauf, keine toten internen Links.
   2. Jeder Rechner: alle Beispiele anklicken (Ergebnis statt Fehlermeldung), Unsinn in jedes Feld (kein Absturz, kein eingeschleustes HTML),
      Szenario-Vergleich, geteilter Link samt Vergleich, CSV-Inhalt, „Ergebnis kopieren“.
   3. Referenztabelle: Suche, Filter, CSV. Weiterleitungen der zusammengelegten Ratgeber.
   Fremde Hosts (Google) werden blockiert; der lokale Server läuft nur für die Dauer des Tests. */
"use strict";
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const DOCS = path.join(__dirname, "docs");
const MIME = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".png": "image/png", ".xml": "text/xml", ".txt": "text/plain" };
let fails = 0, checks = 0;
const check = (ok, msg) => { checks++; if (!ok) { fails++; console.log("  FAIL " + msg); } };
const BOESE = ['"><img src=x onerror="window.__xss=1">', "<script>window.__xss=1</script>", "javascript:window.__xss=1", "=1+1", "-5", "1e999", "９９", "'; DROP", "🙂", " "];

(async () => {
  const server = http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
    const f = path.join(DOCS, p);
    if (!f.startsWith(DOCS) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404, { "content-type": "text/html" }); return res.end(fs.readFileSync(path.join(DOCS, "404.html"))); }
    res.writeHead(200, { "content-type": MIME[path.extname(f)] || "application/octet-stream" }); res.end(fs.readFileSync(f));
  });
  await new Promise(r => server.listen(0, "127.0.0.1", r));
  const BASE = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  const seiten = [...fs.readFileSync(path.join(DOCS, "sitemap.xml"), "utf8").matchAll(/<loc>https:\/\/rechenklarheit\.de([^<]*)<\/loc>/g)].map(m => m[1]);
  check(seiten.length >= 25, `Sitemap hat ${seiten.length} Seiten`);
  const neu = async (w, h) => {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, acceptDownloads: true, permissions: ["clipboard-read", "clipboard-write"] });
    await ctx.route(u => !u.href.startsWith(BASE), r => r.abort());
    const page = await ctx.newPage(); page._err = [];
    page.on("pageerror", e => page._err.push(e.message));
    page.on("console", m => { if (m.type() === "error" && !/Failed to load resource|ERR_FAILED|ERR_BLOCKED/.test(m.text())) page._err.push(m.text()); });
    return { ctx, page };
  };

  // ---------- 1. Sitemap bei zwei Breiten
  const links = new Set();
  for (const [w, h] of [[390, 844], [1366, 900]]) {
    const { ctx, page } = await neu(w, h);
    for (const s of seiten) {
      page._err.length = 0;
      const r = await page.goto(BASE + s, { waitUntil: "load" });
      check(r.status() === 200, `${w}px ${s}: Status ${r.status()}`);
      await page.waitForTimeout(60);
      const m = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, h1: document.querySelectorAll("h1").length,
        breit: [...document.querySelectorAll("main *")].filter(e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.right > document.documentElement.clientWidth + 1 && !e.closest(".scroll") && !e.closest(".ad"); }).slice(0, 3).map(e => e.tagName + "." + e.className),
        hrefs: [...document.querySelectorAll("a[href]")].map(a => a.getAttribute("href")) }));
      check(m.sw <= m.cw + 1, `${w}px ${s}: seitlicher Überlauf ${m.sw} > ${m.cw} ${m.breit.join(" ")}`);
      check(m.breit.length === 0, `${w}px ${s}: Element ragt über den Rand: ${m.breit.join(" ")}`);
      check(m.h1 === 1, `${w}px ${s}: ${m.h1} h1`);
      check(page._err.length === 0, `${w}px ${s}: JS-Fehler ${page._err.join(" | ")}`);
      m.hrefs.forEach(x => links.add(x));
      if (w === 390) { const selbst = await page.evaluate(() => [...document.querySelectorAll("main .prose a[href], main .cards a[href]")].map(a => a.getAttribute("href")).filter(h => h.split("#")[0].split("?")[0] === location.pathname && !h.includes("#") && !h.includes("?")));
        check(selbst.length === 0, `${s}: Link auf sich selbst im Inhalt: ${selbst.join(" ")}`); }
    }
    await ctx.close();
  }
  for (const l of links) {
    if (!l.startsWith("/")) continue;
    const [p, anker] = l.split("#"); const datei = path.join(DOCS, p.split("?")[0] === "/" ? "index.html" : p.split("?")[0]);
    check(fs.existsSync(datei), `toter Link ${l}`);
    if (fs.existsSync(datei) && anker) check(new RegExp(`id="${anker}"`).test(fs.readFileSync(datei, "utf8")), `Anker fehlt: ${l}`);
    if (fs.existsSync(datei)) check(!/http-equiv="refresh"/.test(fs.readFileSync(datei, "utf8")), `Link zeigt auf eine Weiterleitung: ${l}`);
  }

  // ---------- 2. Rechner durchklicken
  const { ctx, page } = await neu(390, 844);
  const rechner = seiten.filter(s => /<form data-calc=/.test(fs.readFileSync(path.join(DOCS, s === "/" ? "index.html" : s), "utf8")));
  check(rechner.length >= 18, `${rechner.length} Seiten mit Rechner`);
  const ergebnis = () => page.evaluate(() => ({ val: document.querySelector("form[data-calc] .res-val")?.textContent || "", hint: document.querySelector("form[data-calc] .hint")?.textContent || "", steps: document.querySelectorAll("form[data-calc] .way li").length }));
  for (const s of rechner) {
    page._err.length = 0;
    await page.goto(BASE + s, { waitUntil: "load" });
    const start = await ergebnis();
    check(start.val !== "" && start.steps >= 2, `${s}: Startwerte liefern Ergebnis mit Rechenweg`);
    const n = await page.locator("[data-ex]").count();
    check(n >= 3, `${s}: ${n} Beispiele`);
    for (let i = 0; i < n; i++) {
      await page.locator("[data-ex]").nth(i).click();
      const e = await ergebnis();
      check(e.val !== "" && e.steps >= 2 && !/NaN|undefined|Infinity/.test(e.val), `${s}: Beispiel ${i + 1} → „${e.val}“ ${e.hint}`);
      check(await page.locator("[data-ex]").nth(i).getAttribute("aria-pressed") === "true", `${s}: Beispiel ${i + 1} als gewählt markiert`);
    }
    check(new URL(page.url()).search === "", `${s}: Beispiele ändern die Adresse nicht`);
    // Tastatur: erstes Beispiel per Enter
    await page.locator("[data-ex]").first().focus(); await page.keyboard.press("Enter");
    check((await ergebnis()).val !== "", `${s}: Beispiel per Tastatur`);
    // Szenario-Vergleich
    await page.locator("[data-pin]").click();
    check(await page.locator(".cmp table").count() === 1 || await page.locator(".cmp").count() === 1, `${s}: Vergleich erscheint`);
    check(await page.evaluate(() => document.activeElement?.hasAttribute("data-unpin")), `${s}: Fokus bleibt nach „merken“ bei den Aktionen`);
    if (n > 1) { await page.locator("[data-ex]").nth(1).click(); check(await page.locator(".cmp").count() === 1, `${s}: Vergleich bleibt nach Änderung`); }
    // Link mit Vergleich: Adresse enthält vgl=, neu geladen entsteht derselbe Vergleich
    const vorher = await ergebnis();
    await page.locator("[data-share]").click();
    const url = page.url();
    check(/[?&]vgl=/.test(url), `${s}: geteilter Link enthält den Vergleich`);
    check(await page.evaluate(() => navigator.clipboard.readText()) === url, `${s}: Link in der Zwischenablage`);
    await page.goto(url, { waitUntil: "load" });
    const nachher = await ergebnis();
    check(nachher.val === vorher.val, `${s}: geteilter Link stellt das Ergebnis wieder her („${vorher.val}“ / „${nachher.val}“)`);
    check(await page.locator(".cmp").count() === 1, `${s}: geteilter Link stellt den Vergleich wieder her`);
    // Kopieren
    await page.locator("[data-copy]").click();
    const txt = await page.evaluate(() => navigator.clipboard.readText());
    check(txt.includes("Rechenweg:") && txt.includes(nachher.val) && txt.includes("Vergleich mit Szenario A") && !/<[a-z]/i.test(txt), `${s}: kopierter Text vollständig und ohne HTML`);
    await page.locator("[data-unpin]").click();
    check(await page.locator(".cmp").count() === 0, `${s}: Vergleich beendet`);
    // CSV, wo es eine Tabelle gibt
    if (await page.locator("[data-csv]").count()) {
      const [dl] = await Promise.all([page.waitForEvent("download"), page.locator("[data-csv]").click()]);
      const csv = fs.readFileSync(await dl.path(), "utf8");
      check(csv.charCodeAt(0) === 0xFEFF && csv.split("\r\n").length > 2 && csv.split("\r\n").slice(0, -1).every(z => /^("[^"]*"(;|$))+$/.test(z.replace("﻿", ""))), `${s}: CSV wohlgeformt`);
      check(!csv.split("\r\n").some(z => z.replace("﻿", "").split(";").some(c => /^"[=+@\t]/.test(c) || /^"-(?!\d)/.test(c))), `${s}: CSV ohne Formelzellen`);
    }
    // Unsinn in jedes Textfeld, einzeln und überall zugleich
    const felder = await page.evaluate(() => [...document.querySelector("form[data-calc]").elements].filter(e => e.name && !e.closest("[hidden]") && (e.tagName === "TEXTAREA" || (e.tagName === "INPUT" && e.type !== "date"))).map(e => e.name));
    for (const b of BOESE) {
      for (const f of felder) await page.locator(`form[data-calc] [name="${f}"]`).fill(b);
      const e = await page.evaluate(() => ({ out: document.querySelector("form[data-calc] [data-out]").innerHTML, xss: window.__xss, img: document.querySelectorAll("form[data-calc] [data-out] img, form[data-calc] [data-out] script").length }));
      check(!e.xss && e.img === 0, `${s}: eingeschleustes HTML bei ${JSON.stringify(b)}`);
      check(!/NaN|undefined|Infinity|\[object/.test(e.out.replace(/<[^>]+>/g, " ")), `${s}: Unsinn ${JSON.stringify(b)} zeigt ${e.out.replace(/<[^>]+>/g, " ").slice(0, 90)}`);
    }
    // Unsinn über die Adresse (geteilter Link von fremder Hand)
    const q = felder.map(f => `${encodeURIComponent(f)}=${encodeURIComponent(BOESE[0])}`).join("&") + "&mode=" + encodeURIComponent(BOESE[1]) + "&land=" + encodeURIComponent(BOESE[0]) + "&vgl=" + encodeURIComponent("a=" + BOESE[0] + "&km=" + BOESE[1]);
    await page.goto(BASE + s + "?" + q, { waitUntil: "load" });
    const e = await page.evaluate(() => ({ xss: window.__xss, img: document.querySelectorAll("main img, main script").length }));
    check(!e.xss && e.img === 0, `${s}: XSS über Adresse`);
    check(page._err.length === 0, `${s}: JS-Fehler ${page._err.join(" | ")}`);
  }

  // Datumsfelder des Verzugszinsen-Rechners
  await page.goto(BASE + "/verzugszinsen-rechner.html");
  await page.locator('[name="von"]').fill("2026-10-31"); await page.locator('[name="bis"]').fill("2026-03-01");
  check(/vor dem ersten/.test((await ergebnis()).hint), "Verzug: Ende vor Beginn wird erklärt");
  await page.locator('[name="von"]').fill(""); check(/Datum/.test((await ergebnis()).hint), "Verzug: leeres Datum wird erklärt");
  // Pendlerrechner: Länderwechsel blendet die passenden Felder ein
  await page.goto(BASE + "/pendlerrechner.html");
  await page.locator('[name="land"]').selectOption("de");
  check(await page.locator('[name="atage"]').isVisible() && !(await page.locator('[name="tage"]').isVisible()), "Pendler: Felder für Deutschland");
  check(/2\.340,80/.test(await page.evaluate(() => { const f = document.querySelector("form"); f.elements.km.value = "28"; f.dispatchEvent(new Event("input")); return f.querySelector(".res-val").textContent; })), "Pendler: Deutschland 28 km × 220 Tage");

  // ---------- 3. Referenztabelle
  await page.goto(BASE + "/saetze-und-grenzwerte.html");
  const alle = await page.locator("#saetze tbody tr").count();
  check(alle >= 40, `Referenztabelle: ${alle} Zeilen`);
  check(await page.evaluate(() => [...document.querySelectorAll("#saetze tbody tr")].every(tr => tr.querySelector("td:nth-child(4) a[href^='https://']") && /abgerufen am \d/.test(tr.textContent))), "Referenztabelle: jede Zeile mit Quelle und Abrufdatum");
  await page.locator('[name="q"]').fill("pendler");
  const p1 = await page.locator("#saetze tbody tr:visible").count();
  check(p1 >= 3 && p1 < alle, `Suche „pendler“: ${p1} Zeilen`);
  await page.locator('[name="land"]').selectOption("DE");
  check(await page.locator("#saetze tbody tr:visible").count() === 0 && await page.locator("[data-filter-empty]").isVisible(), "Suche ohne Treffer zeigt Hinweis");
  await page.locator("[data-filter-reset]").click();
  check(await page.locator("#saetze tbody tr:visible").count() === alle, "Filter zurückgesetzt");
  await page.locator('[name="thema"]').selectOption("Zinsen und Verzug");
  const [dl] = await Promise.all([page.waitForEvent("download"), page.locator("[data-filter-csv]").click()]);
  const csv = fs.readFileSync(await dl.path(), "utf8");
  check(csv.split("\r\n").length - 2 === await page.locator("#saetze tbody tr:visible").count() && /§ 288 Abs\. 1 BGB/.test(csv), "Referenz-CSV enthält die angezeigten Zeilen");
  await page.goto(BASE + "/saetze-und-grenzwerte.html?q=" + encodeURIComponent('<img src=x onerror="window.__xss=1">'));
  check(!(await page.evaluate(() => window.__xss)) && await page.locator("[data-filter-empty]").isVisible(), "Referenztabelle: Suchwort aus der Adresse ist harmlos");
  // „nachrechnen“ nur bei Links mit Eingaben; jeder Parameter muss ein echtes, sichtbares Feld des Zielrechners sein und ankommen
  const tl = await page.evaluate(() => [...document.querySelectorAll("#saetze td:last-child a")].map(a => [a.getAttribute("href"), a.textContent]));
  check(tl.every(([h, t]) => t === (h.includes("?") ? "nachrechnen" : "zum Thema")), "Referenztabelle: Linktext passt zum Ziel");
  for (const h of [...new Set(tl.map(x => x[0]))].filter(h => h.includes("?"))) {
    await page.goto(BASE + h);
    const fehlt = await page.evaluate(() => { const f = document.querySelector("form[data-calc]"); if (!f) return ["kein Rechner"];
      return [...new URLSearchParams(location.search)].filter(([k, v]) => { const el = f.elements[k]; return !el || el.closest("[hidden]") || (el.value !== v && el.value.replace(",", ".") !== v); }).map(x => x.join("=")); });
    check(fehlt.length === 0, `nachrechnen ${h}: Parameter ohne passendes Feld: ${fehlt.join(", ")}`);
    check(await page.locator("form[data-calc] .res-val").count() === 1, `nachrechnen ${h}: Ergebnis`);
  }
  await page.goto(BASE + "/saetze-und-grenzwerte.html");
  // Anzeigenfläche steht nach dem Inhalt, mindestens 250 px von Filterformular und Tabellenkopf entfernt
  const abst = await page.evaluate(() => { const ad = document.querySelector("article .ad--billboard"), f = document.querySelector(".rf-filter"); const r = e => { const b = e.getBoundingClientRect(); return [b.top + scrollY, b.bottom + scrollY]; };
    return { n: document.querySelectorAll("article .ad--billboard").length, d: r(ad)[0] - r(f)[1], nach: !!(document.querySelector("#saetze").compareDocumentPosition(ad) & 4) }; });
  check(abst.n === 1 && abst.nach && abst.d >= 250, `Sätze-Seite: Anzeige ${Math.round(abst.d)} px unter dem Filter`);
  for (const s of ["/saetze-und-grenzwerte.html", "/pendlerrechner.html", "/verzugszinsen-rechner.html"]) { await page.goto(BASE + s); check(/Werte bis 31\.12\.2026; Aktualisierung Anfang Jänner 2027/.test(await page.locator(".jw").first().innerText()), `${s}: Hinweis zum Jahreswechsel sichtbar`); }
  await page.goto(BASE + "/pendlerrechner.html");
  check(/Kalenderjahr 2026, nicht für 2025/.test(await page.locator("form .jw").innerText()) && /2026/.test(await page.locator(".res-label").innerText()) && /nicht für 2025/.test(await page.locator(".way li").first().innerText()), "Pendler: Jahr 2026 an Formular und Ergebnis");
  await page.goto(BASE + "/saetze-und-grenzwerte.html");
  // „nachrechnen“-Links führen zu einem Ergebnis
  const tools = await page.evaluate(() => [...new Set([...document.querySelectorAll("#saetze td:last-child a")].map(a => a.getAttribute("href")))]);
  for (const t of tools) { await page.goto(BASE + t); const e = await page.evaluate(() => document.querySelector("form[data-calc] .res-val, article h1")?.textContent || ""); check(e !== "", `nachrechnen ${t}`); }

  // Weiterleitungen
  for (const alt of ["rabatte-kombinieren", "mehrwertsteuer-herausrechnen", "zinseszins-und-72er-regel", "sollzins-und-effektivzins"]) {
    const h = fs.readFileSync(path.join(DOCS, alt + ".html"), "utf8");
    check(/noindex/.test(h) && /rel="canonical"/.test(h) && /http-equiv="refresh"/.test(h) && !seiten.includes(`/${alt}.html`), `Weiterleitung ${alt}`);
    await page.goto(BASE + `/${alt}.html`); await page.waitForURL(u => !u.pathname.includes(alt), { timeout: 5000 }).catch(() => {});
    check(!page.url().includes(alt) && await page.locator("form[data-calc]").count() === 1, `Weiterleitung ${alt} landet auf dem Rechner`);
  }
  await ctx.close(); await browser.close(); server.close();
  console.log(fails ? `Seiten-Test: ${fails} von ${checks} Prüfungen fehlgeschlagen` : `Seiten-Test: ${checks} Prüfungen OK`);
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
