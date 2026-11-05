/* Werbeflächen-Test im echten Browser (Playwright/Chromium), nach dem Bauen: node test_werbeflaechen.js
   Ein Stub ersetzt adsbygoogle.js und liefert nie eine Anzeige.
   Prüft: ohne data-ad-status="filled" ist keine Werbefläche zu sehen (keine Höhe, kein Abstand, kein „Werbung“);
          mit data-ad-status="filled" ist sie da – samt 150 px Abstand der Half-Page unter dem Verlauf-Kasten. */
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
    const sichtbar = await flaechen(page);
    check(sichtbar.length === 0, `${breite} px ${pfad}: keine leere Werbefläche sichtbar ${sichtbar.length ? JSON.stringify(sichtbar) : ""}`);
    check(errors.length === 0, `${breite} px ${pfad}: keine JS-Fehler ${errors.join(" | ")}`);
    await ctx.close();
  }

  {
    const { ctx, page } = await oeffnen(1366, "/prozentrechner.html");
    await page.$$eval(".ad.on ins.adsbygoogle", l => l.forEach(i => i.setAttribute("data-ad-status", "filled")));
    const da = Object.fromEntries((await flaechen(page)).map(x => [x.art, x]));
    check(da.superbanner && da.superbanner.h >= 90 && da.superbanner.label, "filled: Superbanner mit „Werbung“ sichtbar");
    check(da.superbanner && da.superbanner.unten === 120, "filled: Superbanner-Abstand zum Fußzeilen-Knopf bleibt");
    check(da.half && da.half.h >= 600 && da.half.oben === 150, "filled: Half-Page mit 150 px Abstand zum Verlauf-Kasten");
    check(await page.$$eval(".ad.on", l => l.every(b => b.classList.contains("ad--voll"))), "filled: Rückfall-Klasse .ad--voll gesetzt");
    await ctx.close();
  }
  {
    const { ctx, page } = await oeffnen(390, "/prozentrechner.html");
    await page.$$eval(".ad.on ins.adsbygoogle", l => l.forEach(i => i.setAttribute("data-ad-status", "unfilled")));
    check((await flaechen(page)).length === 0, "unfilled: alles bleibt zugeklappt");
    await page.$eval('.ad.on[data-ad="rect"] ins.adsbygoogle', i => i.setAttribute("data-ad-status", "filled"));
    const da = await flaechen(page);
    check(da.length === 1 && da[0].art === "rect", "390 px: nur die gefüllte Fläche erscheint");
    await ctx.close();
  }

  await browser.close(); server.close();
  console.log(fails ? `Werbeflächen-Test: ${fails} Fehler` : "Werbeflächen-Test: OK");
  process.exit(fails ? 1 : 0);
})();
