/* Werbeflächen-Test im echten Browser (Playwright/Chromium), nach dem Bauen: node test_werbeflaechen.js
   Ein Stub ersetzt adsbygoogle.js und liefert nie eine Anzeige.
   Prüft (AdSense-Hilfe 10762946): ohne data-ad-status bleibt das <ins> sichtbar und ungeschnitten (Breite > 0,
          kein overflow:hidden), nur „Werbung“, Mindesthöhe und Abstände fehlen; "unfilled" → ins display:none;
          "filled"/"unfill-optimized" → Platz mit „Werbung“ – samt 150 px Abstand der Half-Page unter dem Verlauf-Kasten. */
"use strict";
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");

const DOCS = path.join(__dirname, "docs");
const MIME = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".png": "image/png" };
let fails = 0;
function check(ok, msg){ console.log((ok ? "  ok   " : "  FAIL ") + msg); if (!ok) fails++; }

function flaechen(page){
  return page.$$eval(".ad", list => list.map(b => {
    const cs = getComputedStyle(b);
    if (cs.display === "none") return null;
    const h = b.getBoundingClientRect().height;
    return { art: b.dataset.ad, h, oben: parseFloat(cs.marginTop), unten: parseFloat(cs.marginBottom),
             label: getComputedStyle(b, "::before").content.includes("Werbung") && h > 0 };
  }).filter(x => x && (x.h > 0 || x.oben > 0 || x.unten > 0 || x.label)));
}

function inse(page){
  return page.$$eval(".ad.on ins.adsbygoogle", l => l.map(i => {
    const b = i.parentElement, ci = getComputedStyle(i), cb = getComputedStyle(b);
    return { art: b.dataset.ad, display: ci.display, vis: ci.visibility, w: i.getBoundingClientRect().width, insH: i.getBoundingClientRect().height,
             boxH: b.getBoundingClientRect().height, overflow: cb.overflowX + "/" + cb.overflowY, boxVis: cb.visibility,
             label: getComputedStyle(b, "::before").content.includes("Werbung"), abstand: parseFloat(cb.marginTop) + parseFloat(cb.marginBottom), minH: cb.minHeight };
  }));
}
function insOk(l){
  return l.length > 0 && l.every(x => x.display !== "none" && x.vis === "visible" && x.boxVis === "visible" && x.w > 0 && x.overflow === "visible/visible" && x.boxH >= x.insH);
}

(async () => {
  const server = http.createServer((req, res) => {
    const f = path.join(DOCS, decodeURIComponent(req.url.split("?")[0]).replace(/\/$/, "/index.html"));
    if (!f.startsWith(DOCS) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "content-type": MIME[path.extname(f)] || "application/octet-stream" }); res.end(fs.readFileSync(f));
  });
  await new Promise(r => server.listen(0, "127.0.0.1", r));
  const base = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();

  async function oeffnen(breite, pfad){
    const ctx = await browser.newContext({ viewport: { width: breite, height: 900 } });
    await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.fulfill({ status: 200, contentType: "text/javascript", body: "/* Stub ohne Anzeige */" }));
    const page = await ctx.newPage();
    const errors = [];
    page.on("pageerror", e => errors.push(e.message));
    await page.goto(base + pfad);
    await page.waitForFunction(() => document.querySelector(".ad.on ins.adsbygoogle"));
    return { ctx, page, errors };
  }

  for (const breite of [390, 1366]) for (const pfad of ["/", "/prozentrechner.html"]) {
    const { ctx, page, errors } = await oeffnen(breite, pfad);
    const l = await inse(page);
    check(insOk(l), `${breite} px ${pfad}: ohne Status bleibt ins.adsbygoogle sichtbar und ungeschnitten ${insOk(l) ? "" : JSON.stringify(l)}`);
    check(l.every(x => !x.label && x.abstand === 0 && x.minH === "0px"), `${breite} px ${pfad}: ohne Status kein „Werbung“, kein Abstand, keine Mindesthöhe`);
    const sichtbar = await flaechen(page);
    check(sichtbar.every(x => !x.label && x.oben === 0 && x.unten === 0), `${breite} px ${pfad}: kein Beiwerk sichtbar ${JSON.stringify(sichtbar.filter(x => x.label || x.oben || x.unten))}`);
    check(errors.length === 0, `${breite} px ${pfad}: keine JS-Fehler ${errors.join(" | ")}`);
    await ctx.close();
  }

  for (const status of ["filled", "unfill-optimized"]) {
    const { ctx, page } = await oeffnen(1366, "/prozentrechner.html");
    await page.$$eval(".ad.on ins.adsbygoogle", (l, st) => l.forEach(i => i.setAttribute("data-ad-status", st)), status);
    const da = Object.fromEntries((await flaechen(page)).map(x => [x.art, x]));
    check(da.superbanner && da.superbanner.h >= 90 && da.superbanner.label, `${status}: Superbanner mit „Werbung“ sichtbar`);
    check(da.superbanner && da.superbanner.unten === 120, `${status}: Superbanner-Abstand zum Fußzeilen-Knopf bleibt`);
    check(da.half && da.half.h >= 600 && da.half.oben === 150 && da.half.label, `${status}: Half-Page mit „Werbung“ und 150 px Abstand zum Verlauf-Kasten`);
    check(await page.$$eval(".ad.on", l => l.every(b => b.classList.contains("ad--voll"))), `${status}: Rückfall-Klasse .ad--voll gesetzt`);
    await ctx.close();
  }
  {
    const { ctx, page } = await oeffnen(390, "/prozentrechner.html");
    await page.$$eval(".ad.on ins.adsbygoogle", l => l.forEach(i => i.setAttribute("data-ad-status", "unfilled")));
    const l = await inse(page);
    check(l.every(x => x.display === "none" && !x.label && x.boxH === 0), "unfilled: ins display:none, Platz ohne Höhe und „Werbung“");
    check((await flaechen(page)).length === 0, "unfilled: nichts sichtbar");
    await page.$eval('.ad.on[data-ad="rect"] ins.adsbygoogle', i => i.setAttribute("data-ad-status", "filled"));
    const da = await flaechen(page);
    check(da.length === 1 && da[0].art === "rect" && da[0].label, "390 px: nur die gefüllte Fläche erscheint, mit „Werbung“");
    await ctx.close();
  }
  {
    // Browser ohne :has(): :has()-Regeln entfernen, Rückfall-Klasse erzwingen
    const { ctx, page } = await oeffnen(1366, "/prozentrechner.html");
    await page.evaluate(() => {
      for (const sh of document.styleSheets) { try { for (let k = sh.cssRules.length - 1; k >= 0; k--) if (sh.cssRules[k].cssText.includes(":has(")) sh.deleteRule(k); } catch (e) {} }
      document.documentElement.classList.add("ohne-has");
    });
    let l = await inse(page);
    check(insOk(l) && l.every(x => !x.label && x.abstand === 0), "ohne :has(): leer → ins sichtbar, kein Beiwerk");
    await page.$$eval(".ad.on ins.adsbygoogle", l => l.forEach(i => i.setAttribute("data-ad-status", "unfill-optimized")));
    l = await inse(page);
    check(l.every(x => x.label), "ohne :has(): unfill-optimized → „Werbung“ sichtbar");
    await ctx.close();
  }

  await browser.close(); server.close();
  console.log(fails ? `Werbeflächen-Test: ${fails} Fehler` : "Werbeflächen-Test: OK");
  process.exit(fails ? 1 : 0);
})();
