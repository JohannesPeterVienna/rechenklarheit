// Automatischer Test: Entscheidungslogik von assets/consent.js (Google-CMP vs. eigener Statistik-Zettel).
// Läuft ohne Browser – Fenster, Dokument, Cookies, Speicher und Uhr sind nachgebaut.
const fs = require("fs"), vm = require("vm");
const CODE = fs.readFileSync(__dirname + "/assets/consent.js", "utf8");
const GA = "G-T00HRG2YVF", GTM = "googletagmanager.com", TAG = 864e5;
let bad = 0, n = 0;
const check = (name, ok, info) => { n++; if (!ok) { console.error("FEHLER", name, info === undefined ? "" : info); bad++; } };

function speicher(start = {}) {
  const m = new Map(Object.entries(start));
  return { getItem: k => (m.has(k) ? m.get(k) : null), setItem: (k, v) => m.set(k, String(v)), removeItem: k => m.delete(k), _m: m };
}

/** Baut eine Seite nach und führt consent.js darin aus. */
function seite({ tcf = null, gpc = false, store = speicher(), cookies = {}, ohneWerbung = false, cm = 0, hash = "", jetzt = Date.now() } = {}) {
  let uhr = 0; const timer = [];
  const skripte = [], klicks = [], cookieWrites = [], neben = [];
  const jar = new Map(Object.entries(cookies));
  const el = tag => {
    const e = { tagName: tag.toUpperCase(), children: [], attrs: {}, hidden: false, style: {}, listeners: {}, isConnected: true, offsetHeight: 180, textContent: "",
      classList: { s: new Set(), add(c) { this.s.add(c); }, remove(c) { this.s.delete(c); }, contains(c) { return this.s.has(c); } },
      setAttribute(k, v) { this.attrs[k] = String(v); }, hasAttribute(k) { return k in this.attrs; },
      append(...xs) { this.children.push(...xs); }, prepend(x) { this.children.unshift(x); }, after(x) { neben.push(x); },
      addEventListener(t, f) { (this.listeners[t] = this.listeners[t] || []).push(f); }, focus() { doc.activeElement = this; }, closest() { return null; } };
    return e;
  };
  const skript = el("script"); if (ohneWerbung) skript.setAttribute("data-ohne-werbung", "");
  const doc = {
    currentScript: skript, body: el("body"), head: { appendChild: s => skripte.push(s.src) }, activeElement: null,
    createElement: el, querySelector: sel => (sel === ".skip" ? skip : null), querySelectorAll: () => [],
    addEventListener: (t, f) => { if (t === "click") klicks.push(f); },
    get cookie() { return [...jar].map(([k, v]) => `${k}=${v}`).join("; "); },
    set cookie(s) { cookieWrites.push(s); const [kv] = s.split(";"); const [k, v] = kv.split("="); if (/max-age=0|1970/.test(s)) jar.delete(k.trim()); else jar.set(k.trim(), v); }
  };
  const skip = el("a");
  const loc = { hostname: "www.rechenklarheit.de", pathname: "/", search: "", hash, href: "/" };
  const win = {
    document: doc, navigator: gpc ? { globalPrivacyControl: true } : {}, location: loc, localStorage: store,
    history: { replaceState() { loc.hash = ""; } },
    setTimeout: (f, ms) => timer.push({ at: uhr + (ms || 0), f }), Date: class extends Date { constructor(...a) { a.length ? super(...a) : super(jetzt + uhr); } static now() { return jetzt + uhr; } },
    JSON, Math, Object, String, Number, Boolean, Array, isFinite, console
  };
  win.window = win;
  if (tcf) win.__tcfapi = (cmd, v, cb) => { if (cmd === "addEventListener") { win.__tcfCb = cb; cb(tcf, true); } };
  win.googlefc = { callbackQueue: [], getGoogleConsentModeValues: () => ({ analyticsStoragePurposeConsentStatus: cm }) };
  vm.runInNewContext(CODE, win);
  const tick = ms => { const bis = uhr + ms; for (;;) { timer.sort((a, b) => a.at - b.at); const t = timer[0]; if (!t || t.at > bis) break; timer.shift(); uhr = t.at; t.f(); } uhr = bis; };
  const zettel = () => neben.find(x => x.className === "statzettel");
  const sichtbar = () => Boolean(zettel() && !zettel().hidden);
  const knopf = text => { const z = zettel(); const w = z && z.children.find(c => c.className === "statzettel-wahl"); return w && w.children.find(b => b.textContent === text); };
  const druecke = text => knopf(text).listeners.click.forEach(f => f());
  const einstellungen = () => { const b = el("button"); b.closest = () => b; klicks.forEach(f => f({ target: b, preventDefault() {} })); return b; };
  const gtm = () => skripte.filter(s => s && s.includes(GTM)).length;
  const ads = () => skripte.filter(s => s && s.includes("adsbygoogle")).length;
  const dl = () => win.dataLayer.map(a => Array.from(a));
  const werbungFreigegeben = () => dl().some(a => a[0] === "consent" && a[2] && ["ad_storage", "ad_user_data", "ad_personalization"].some(k => a[2][k] === "granted"));
  return { win, doc, tick, zettel, sichtbar, druecke, einstellungen, gtm, ads, dl, werbungFreigegeben, store, jar, cookieWrites, loc };
}

const hidden = { gdprApplies: true, eventStatus: "tcloaded", tcString: "", displayStatus: "hidden", purpose: { consents: {} }, vendor: { consents: {} } };
const decidedNo = { gdprApplies: true, eventStatus: "useractioncomplete", tcString: "CQxyz", displayStatus: "hidden", purpose: { consents: {} }, vendor: { consents: {} } };
const decidedYes = { gdprApplies: true, eventStatus: "tcloaded", tcString: "CQabc", displayStatus: "hidden", purpose: { consents: { 1: true } }, vendor: { consents: { 755: true } } };
const wahl = (w, alterTage = 1) => speicher({ "rk-statistik-wahl": JSON.stringify({ v: 1, wahl: w, zeit: Date.now() - alterTage * TAG }) });

// 1) Reine Funktionen
{ const R = seite().win.RK_EINWILLIGUNG, jetzt = Date.UTC(2026, 10, 4);
  check("rein: hidden ist keine Entscheidung", !R.googleEntschieden(hidden) && !R.googleZustaendig(hidden));
  check("rein: useractioncomplete entscheidet", R.googleEntschieden(decidedNo));
  check("rein: tcloaded mit tcString entscheidet", R.googleEntschieden(decidedYes));
  check("rein: tcloaded ohne tcString nicht", !R.googleEntschieden({ eventStatus: "tcloaded", tcString: "" }));
  check("rein: gdprApplies false → Google", R.googleZustaendig({ gdprApplies: false, eventStatus: "tcloaded", tcString: "" }));
  check("rein: Dialog sichtbar → Google", R.googleZustaendig({ gdprApplies: true, eventStatus: "cmpuishown", displayStatus: "visible" }));
  check("rein: disabled → Übergang", !R.googleZustaendig({ gdprApplies: true, eventStatus: "tcloaded", tcString: "", displayStatus: "disabled" }));
  check("rein: zustaendig ohne tcfapi wartet", R.zustaendig(null, false, null, false) === "warten");
  check("rein: zustaendig ohne tcfapi fragt", R.zustaendig(null, true, null, false) === "fragen");
  check("rein: CMP schlägt eigene Wahl", R.zustaendig(decidedNo, true, "ja", false) === "google");
  check("rein: GPC", R.zustaendig(hidden, true, "ja", true) === "gpc");
  check("rein: eigene Wahl gilt", R.zustaendig(hidden, true, "nein", false) === "nein");
  const vor = m => { const d = new Date(jetzt); d.setMonth(d.getMonth() - m); return d.getTime(); };
  check("rein: 11 Monate gültig", R.wahlGueltig({ v: 1, wahl: "ja", zeit: vor(11) }, jetzt) === "ja");
  check("rein: 12 Monate abgelaufen", R.wahlGueltig({ v: 1, wahl: "ja", zeit: vor(12) }, jetzt) === null);
  check("rein: falsche Version", R.wahlGueltig({ v: 2, wahl: "ja", zeit: vor(1) }, jetzt) === null);
  check("rein: Unsinn", R.wahlGueltig({ v: 1, wahl: "vielleicht", zeit: vor(1) }, jetzt) === null && R.wahlGueltig(null, jetzt) === null);
  check("rein: Zeit in der Zukunft", R.wahlGueltig({ v: 1, wahl: "ja", zeit: jetzt + 3 * TAG }, jetzt) === null);
}

// 2) Kein __tcfapi: Zettel nach 3 s, vorher kein Analytics; Zustimmen lädt gtag.js genau einmal
{ const p = seite();
  check("ohne tcfapi: fehlender AdSense-Loader wird genau einmal ergänzt", p.ads() === 1, p.ads());
  p.tick(2900); check("ohne tcfapi: vor 3 s kein Zettel", !p.sichtbar());
  p.tick(200); check("ohne tcfapi: Zettel nach 3 s", p.sichtbar());
  check("ohne tcfapi: kein Fokusraub beim Aufruf", p.doc.activeElement === null);
  check("ohne tcfapi: vor Zustimmung kein googletagmanager", p.gtm() === 0, p.gtm());
  p.druecke("Zustimmen"); p.tick(5000);
  check("ohne tcfapi: nach Zustimmung genau ein gtag.js", p.gtm() === 1, p.gtm());
  check("ohne tcfapi: Zettel geschlossen", !p.sichtbar());
  check("ohne tcfapi: analytics_storage granted", p.dl().some(a => a[0] === "consent" && a[1] === "update" && a[2].analytics_storage === "granted"));
  check("ohne tcfapi: config ohne Signals/Personalisierung", p.dl().some(a => a[0] === "config" && a[2].allow_google_signals === false && a[2].allow_ad_personalization_signals === false));
  check("ohne tcfapi: Werbung nie freigegeben", !p.werbungFreigegeben());
  check("ohne tcfapi: ga-disable aus", p.win[`ga-disable-${GA}`] === false);
  const e = JSON.parse(p.store.getItem("rk-statistik-wahl"));
  check("ohne tcfapi: gespeichert mit Version und Zeit", e.v === 1 && e.wahl === "ja" && typeof e.zeit === "number", e);
  // Neu laden respektiert die Wahl
  const q = seite({ store: p.store }); q.tick(3100);
  check("neu laden: kein Zettel", !q.sichtbar()); check("neu laden: gtag.js einmal", q.gtm() === 1, q.gtm());
}

// 3) Ablehnen → kein Analytics, auch nach Neuladen
{ const p = seite(); p.tick(3100); p.druecke("Ablehnen"); p.tick(5000);
  check("ablehnen: kein gtag.js", p.gtm() === 0); check("ablehnen: ga-disable an", p.win[`ga-disable-${GA}`] === true);
  const q = seite({ store: p.store }); q.tick(5000); check("ablehnen neu laden: kein Zettel, kein gtag.js", !q.sichtbar() && q.gtm() === 0);
}

// 4) CMP lädt, meldet aber "hidden" → Zettel
{ const p = seite({ tcf: hidden }); p.tick(1000); check("hidden: noch kein Zettel", !p.sichtbar());
  p.tick(2500); check("hidden: Zettel nach 3 s", p.sichtbar()); check("hidden: kein gtag.js", p.gtm() === 0);
  p.druecke("Zustimmen"); p.tick(1000); check("hidden: Zustimmen lädt gtag.js", p.gtm() === 1);
  p.win.__tcfCb(hidden, true); p.tick(1000); check("hidden: weiteres hidden-Ereignis hält Messung", p.win[`ga-disable-${GA}`] === false);
}

// 5) Echte CMP-Entscheidung schlägt eigene Wahl
{ const p = seite({ tcf: decidedNo, store: wahl("ja") }); p.tick(5000);
  check("CMP nein vs. eigenes ja: kein Zettel", !p.sichtbar()); check("CMP nein vs. eigenes ja: kein gtag.js", p.gtm() === 0, p.gtm());
  check("CMP nein: Vermerk Google", p.store.getItem("rk-statistik-google") === "1");
  check("CMP nein: eigene Wahl gelöscht", p.store.getItem("rk-statistik-wahl") === null);
  const q = seite({ tcf: decidedYes, cm: 1, store: wahl("nein") }); q.tick(5000);
  check("CMP ja vs. eigenes nein: gtag.js geladen", q.gtm() === 1, q.gtm()); check("CMP ja: kein Zettel", !q.sichtbar());
  // CMP entscheidet erst nach dem Zettel → Zettel zu, TCF-Logik gilt
  const r = seite({ tcf: hidden }); r.tick(3100); check("späte CMP: Zettel offen", r.sichtbar());
  r.win.__tcfCb(decidedNo, true); r.tick(500); check("späte CMP: Zettel geschlossen", !r.sichtbar());
  // eigene Zustimmung aktiv, dann CMP-Nein → Messung aus
  const s = seite({ tcf: hidden, store: wahl("ja") }); s.tick(3100); check("eigenes ja aktiv", s.win[`ga-disable-${GA}`] === false);
  s.win.__tcfCb(decidedNo, true); s.tick(500); check("CMP-Nein beendet eigene Messung", s.win[`ga-disable-${GA}`] === true);
  check("CMP-Nein löscht eigene Wahl", s.store.getItem("rk-statistik-wahl") === null);
  // V1: eigenes Ja → Google-Nein → Neuladen, CMP meldet wieder nur tcloaded ohne tcString ⇒ keine Messung, Zettel fragt neu
  const s2 = seite({ tcf: hidden, store: s.store }); s2.tick(3100);
  check("V1: nach Google-Nein und Neuladen ohne tcString keine Messung", s2.gtm() === 0 && s2.win[`ga-disable-${GA}`] === true, s2.gtm());
  check("V1: Zettel fragt neu", s2.sichtbar());
  // V2: Google-Nein nach eigenem Ja löscht _ga/_ga_*
  const v2 = seite({ tcf: hidden, store: wahl("ja"), cookies: { _ga: "GA1.1.9", _ga_T00HRG2YVF: "GS1", rk: "x" } }); v2.tick(3100);
  v2.win.__tcfCb(decidedNo, true); v2.tick(500);
  check("V2: Google-Nein löscht _ga-Cookies", !v2.jar.has("_ga") && !v2.jar.has("_ga_T00HRG2YVF") && v2.jar.get("rk") === "x", [...v2.jar.keys()]);
  // V2 beim nächsten Aufruf: Zettel-Ja von früher, _ga liegen noch, Google sagt gleich beim Laden Nein
  const v4 = seite({ tcf: decidedNo, store: wahl("ja"), cookies: { _ga: "GA1.1.9", _ga_T00HRG2YVF: "GS1" } }); v4.tick(5000);
  check("V2: Google-Nein beim Laden löscht _ga aus früherem Zettel-Ja", !v4.jar.has("_ga") && !v4.jar.has("_ga_T00HRG2YVF") && v4.gtm() === 0, [...v4.jar.keys()]);
  // Google-Ja nach eigenem Ja: Messung bleibt, Cookies bleiben, eigene Wahl trotzdem gelöscht
  const v3 = seite({ tcf: hidden, cm: 1, store: wahl("ja"), cookies: { _ga: "GA1.1.9" } }); v3.tick(3100);
  v3.win.__tcfCb(decidedYes, true); v3.tick(500);
  check("Google-Ja: Messung bleibt, Cookies bleiben, eigene Wahl gelöscht", v3.win[`ga-disable-${GA}`] === false && v3.jar.has("_ga") && v3.store.getItem("rk-statistik-wahl") === null);
  // gdprApplies false → kein Zettel
  const t = seite({ tcf: { gdprApplies: false, eventStatus: "tcloaded", tcString: "" } }); t.tick(5000);
  check("gdprApplies false: kein Zettel", !t.sichtbar());
  // Einstellungen im Google-Modus → Google-Widerrufsmeldung
  let gezeigt = 0; p.win.googlefc.showRevocationMessage = () => gezeigt++; p.einstellungen();
  p.win.googlefc.callbackQueue.filter(f => typeof f === "function").forEach(f => f());
  check("Google-Modus: Einstellungen → Google-Widerruf", gezeigt === 1 && !p.sichtbar(), gezeigt);
}

// 6) GPC: Statistik aus, Zettel nicht aufdrängen
{ const p = seite({ gpc: true, store: wahl("ja") }); p.tick(5000);
  check("GPC: kein Zettel", !p.sichtbar()); check("GPC: kein gtag.js trotz gespeichertem ja", p.gtm() === 0);
  p.einstellungen(); check("GPC: Einstellungen zeigt Zettel", p.sichtbar());
  const stand = p.zettel().children.find(c => c.className === "statzettel-stand");
  check("GPC: Hinweis statt Knöpfe", /Global Privacy Control/.test(stand.textContent) && p.zettel().children.find(c => c.className === "statzettel-wahl").hidden);
}

// 7) Ablauf nach 12 Monaten
{ const p = seite({ store: wahl("ja", 370) }); p.tick(3100); check("Ablauf: nach 370 Tagen wieder gefragt", p.sichtbar() && p.gtm() === 0);
  const q = seite({ store: wahl("ja", 330) }); q.tick(3100); check("Ablauf: nach 330 Tagen noch gültig", !q.sichtbar() && q.gtm() === 1);
}

// 8) Widerruf über „Datenschutz-Einstellungen“ löscht _ga-Cookies
{ const p = seite({ store: wahl("ja"), cookies: { _ga: "GA1.1.1", _ga_T00HRG2YVF: "GS1", rk: "x" } }); p.tick(3100);
  check("Widerruf: Messung an", p.win[`ga-disable-${GA}`] === false);
  const b = p.einstellungen(); check("Widerruf: Zettel offen", p.sichtbar());
  check("Widerruf: Fokus im Zettel", p.doc.activeElement && p.doc.activeElement.id === "statzettel-titel");
  check("Widerruf: Stand angezeigt", /zugestimmt am/.test(p.zettel().children.find(c => c.className === "statzettel-stand").textContent));
  p.druecke("Ablehnen");
  check("Widerruf: _ga gelöscht", !p.jar.has("_ga") && !p.jar.has("_ga_T00HRG2YVF"), [...p.jar.keys()]);
  check("Widerruf: fremdes Cookie bleibt", p.jar.get("rk") === "x");
  check("Widerruf: auch mit Domain .rechenklarheit.de", p.cookieWrites.some(w => w.startsWith("_ga=") && w.includes("domain=.rechenklarheit.de")));
  check("Widerruf: ga-disable an", p.win[`ga-disable-${GA}`] === true);
  check("Widerruf: analytics_storage denied", p.dl().filter(a => a[0] === "consent" && a[1] === "update").pop()[2].analytics_storage === "denied");
  check("Widerruf: Fokus zurück zum Knopf", p.doc.activeElement === b);
  check("Widerruf: Werbung nie freigegeben", !p.werbungFreigegeben());
  check("Widerruf: Wahl nein gespeichert", JSON.parse(p.store.getItem("rk-statistik-wahl")).wahl === "nein");
}

// 9) Escape schließt nur
{ const p = seite(); p.tick(3100);
  p.zettel().listeners.keydown.forEach(f => f({ key: "Escape", preventDefault() {} }));
  check("Escape: Zettel zu", !p.sichtbar()); check("Escape: nichts gespeichert, kein gtag.js", p.store.getItem("rk-statistik-wahl") === null && p.gtm() === 0);
}
{ const p = seite(); p.tick(3100);
  const zu = p.zettel().children.find(c => c.className === "statzettel-zu");
  check("Schließen-Knopf beschriftet", zu && /ohne zu entscheiden/.test(zu.attrs["aria-label"]));
  zu.listeners.click.forEach(f => f());
  check("Schließen: Zettel zu, nichts gespeichert, kein gtag.js", !p.sichtbar() && p.store.getItem("rk-statistik-wahl") === null && p.gtm() === 0);
  const q = seite({ store: p.store }); q.tick(3100); check("Schließen: beim nächsten Aufruf wieder gefragt", q.sichtbar());
}

// 10) Einstellungen vor Ablauf der Wartezeit → Zettel kommt nach 3 s
{ const p = seite(); p.tick(500); p.einstellungen(); check("früher Klick: noch nicht offen", !p.sichtbar());
  p.tick(2600); check("früher Klick: nach Wartezeit offen", p.sichtbar()); }

// 11) Seiten ohne Werbung (Impressum, Datenschutz)
{ const p = seite({ ohneWerbung: true, store: wahl("ja") }); p.tick(5000);
  check("ohne Werbung: kein AdSense", p.ads() === 0); check("ohne Werbung: kein gtag.js", p.gtm() === 0); check("ohne Werbung: kein Zettel von selbst", !p.sichtbar());
  p.einstellungen(); check("ohne Werbung: Einstellungen öffnen Zettel", p.sichtbar());
  p.druecke("Zustimmen"); p.tick(1000); check("ohne Werbung: Zustimmen lädt trotzdem nichts", p.gtm() === 0);
  const q = seite({ ohneWerbung: true, store: speicher({ "rk-statistik-google": "1" }) }); q.einstellungen();
  check("ohne Werbung + Google zuständig: zur Startseite", q.loc.href === "/#datenschutz-einstellungen" && !q.sichtbar(), q.loc.href);
  const r = seite({ hash: "#datenschutz-einstellungen" }); r.tick(3100); check("Startseite mit #datenschutz-einstellungen öffnet Einstellungen", r.sichtbar());
}

// 12) Gesperrter Speicher: kein Absturz, Zettel erscheint jedes Mal
{ const kaputt = { getItem() { throw new Error("SecurityError"); }, setItem() { throw new Error("SecurityError"); }, removeItem() { throw new Error("x"); } };
  let ok = true; try { const p = seite({ store: kaputt }); p.tick(3100); ok = p.sichtbar(); p.druecke("Zustimmen"); p.tick(100); ok = ok && p.gtm() === 1; } catch (e) { ok = false; }
  check("Speicher gesperrt: läuft weiter", ok);
}

if (bad) process.exit(1);
console.log(`Einwilligungs-Test: ${n} Prüfungen OK`);
