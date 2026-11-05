/* Werbung und Statistik — beides läuft über Googles zertifizierte Einwilligungsverwaltung (TCF 2.2).
   Messregel für Google Analytics:
     · DSGVO gilt (oder unklar): TCF Zweck 1 (Speichern) + Anbieter 755 (Google) zugestimmt UND
       Consent Mode der Google-CMP analyticsStoragePurposeConsentStatus === GRANTED (1).
     · DSGVO gilt laut CMP nicht: Statuswert GRANTED (1) oder NOT_APPLICABLE (3) und die CMP meldet
       ausdrücklich keinen US-Opt-out (googlefc.usstatesoptout: DOES_NOT_APPLY 1 / NOT_OPTED_OUT 2).
   Fehlend, UNKNOWN (0), DENIED (2), NOT_CONFIGURED (4), ein offener Dialog oder eine Ausnahme einer
   CMP-Schnittstelle = keine Messung. Ein klares TCF-Nein sperrt sofort, bevor die Consent-Mode-
   Schnittstelle überhaupt gefragt wird. Ablehnung/Widerruf → consent update "denied", ga-disable,
   keine weiteren Treffer. Signals und Werbepersonalisierung sind deaktiviert.
   Werte laut developers.google.com/funding-choices/fc-api-docs

   Übergangs-Zettel „Statistik“ (seit 4.11.2026): Die Google-CMP lädt, zeigt ihre EU-Mitteilung aber
   nicht an (displayStatus "hidden"). Meldet sie nach 3 s keine echte TCF-Entscheidung
   (useractioncomplete oder tcloaded mit tcString) und gilt nicht ausdrücklich gdprApplies === false,
   fragt ein eigener Zettel nur nach der Reichweitenmessung. Er setzt ausschließlich analytics_storage;
   ad_storage, ad_user_data und ad_personalization fasst er nie an. Sobald die Google-CMP entscheidet
   (oder ihren Dialog zeigt), gilt wieder allein die TCF-Logik oben; eine echte Google-Entscheidung löscht die
   eigene Wahl, ein Google-Nein nach Zettel-Ja zusätzlich die _ga-Cookies.
   GPC: keine Messung, der Zettel wird nicht von selbst gezeigt. Seiten ohne Werbung (Impressum,
   Datenschutz, 404) binden dieses Skript mit data-ohne-werbung ein: kein AdSense, kein Analytics,
   nur „Datenschutz-Einstellungen“. */
(() => {
  const skript = document.currentScript;                       // nur beim ersten, synchronen Durchlauf gesetzt
  const ohneWerbung = Boolean(skript && skript.hasAttribute("data-ohne-werbung"));
  const PUB = "ca-pub-7811071715414905";
  const GA = "G-T00HRG2YVF";
  const GOOGLE_VENDOR = 755;
  const CM_GRANTED = 1, CM_NOT_APPLICABLE = 3;
  const US_OHNE_OPTOUT = [1, 2];   // usstatesoptout: DOES_NOT_APPLY, NOT_OPTED_OUT (3 = OPTED_OUT, 0 = UNKNOWN)

  // Consent-Mode-Grundwerte vor jedem Google-Skript (auch vor adsbygoogle.js)
  const dl = window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function(){ dl.push(arguments); };
  window[`ga-disable-${GA}`] = true;
  // Die Grundwerte setzt bereits das Inline-Skript im <head> vor dem statischen AdSense-Loader.
  // Fehlt es (z. B. ältere Zwischenspeicher-Fassung einer Seite), werden sie hier gesetzt.
  if (!window.__rkConsentDefault) {
    window.gtag("consent", "default", {
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      analytics_storage: "denied",
      wait_for_update: 500
    });
    window.__rkConsentDefault = true;
  }
  const fc = window.googlefc = window.googlefc || {};
  fc.callbackQueue = fc.callbackQueue || [];

  // Anzeigenblöcke: Block-IDs werden nach der AdSense-Freigabe hier eingetragen.
  // AdSense-Anzeigenblöcke (Konto pub-7811071715414905, gemeinsame Blöcke „Themen-Websites – …“, angelegt 17.10. und 5.11.2026)
  const SLOTS = { billboard: "7497607759", rect: "1292301217", half: "1292301217", superbanner: "5774811012", sky: "5064364572", mbanner: "5396758258" };
  // Feste IAB-Formate: Superbanner 728×90, Wide Skyscraper 160×600. Die übrigen Plätze sind responsiv
  // (Billboard 970×250 / Leaderboard 728×90 / Mobile 320×100, Half Page 300×600, Medium Rectangle 300×250).
  const FIXED = { superbanner: [728, 90], sky: [160, 600], mbanner: [320, 100] };

  const gpc = navigator.globalPrivacyControl === true;

  function loadAds(){
    if (gpc) return;
    // Der Loader steht statisch im <head>. Nur falls er fehlt, wird er hier ergänzt – nie ein zweites Mal.
    if (!document.querySelector('script[src*="pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"]')) {
      const s = document.createElement("script");
      s.async = true; s.crossOrigin = "anonymous";
      s.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${PUB}`;
      document.head.appendChild(s);
    }
    document.querySelectorAll(".ad[data-ad]").forEach(box => {
      const id = SLOTS[box.dataset.ad];
      if (!id) return;
      box.classList.add("on");
      if (box.offsetParent === null) { box.classList.remove("on"); return; }   // auf diesem Bildschirm ausgeblendet
      const ins = document.createElement("ins");
      ins.className = "adsbygoogle"; ins.dataset.adClient = PUB; ins.dataset.adSlot = id;
      const fixed = FIXED[box.dataset.ad];
      if (fixed) { ins.style.cssText = `display:inline-block;width:${fixed[0]}px;height:${fixed[1]}px`; }
      else {
        ins.style.display = "block";
        ins.dataset.adFormat = box.dataset.ad === "half" ? "vertical" : "auto";
        ins.dataset.fullWidthResponsive = "true";
      }
      box.appendChild(ins);
      beobachteStatus(box, ins);
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    });
  }

  /* Rückfallebene für Browser ohne :has(): Erst wenn Google antwortet (data-ad-status="filled" oder
     "unfill-optimized"), bekommt der Platz .ad--voll und zeigt in style.css Beschriftung und Abstände.
     Das <ins> selbst bleibt immer sichtbar. */
  function beobachteStatus(box, ins){
    const hatHas = !!(window.CSS && CSS.supports && CSS.supports("selector(:has(a))"));
    if (!hatHas) document.documentElement.classList.add("ohne-has");
    const setzen = () => { if (["filled", "unfill-optimized"].includes(ins.getAttribute("data-ad-status"))) box.classList.add("ad--voll"); else box.classList.remove("ad--voll"); };
    setzen();
    if (window.MutationObserver) new MutationObserver(setzen).observe(ins, { attributes: true, attributeFilter: ["data-ad-status"] });
  }

  /** Reine Entscheidung: true = messen, false = nicht messen, null = noch offen.
      cmStatus/usStatus sind Funktionen – sie werden erst gefragt, wenn das TCF-Signal kein Nein ist. */
  function freigabe(tc, cmStatus, usStatus){
    if (gpc) return false;
    if (!tc) return null;
    if (tc.gdprApplies === false){                     // außerhalb von EWR/UK/CH
      const cm = cmStatus();
      return (cm === CM_GRANTED || cm === CM_NOT_APPLICABLE) && US_OHNE_OPTOUT.includes(usStatus());
    }
    const fertig = tc.eventStatus === "tcloaded" || tc.eventStatus === "useractioncomplete";
    if (!fertig) return null;
    const zweck1 = Boolean(tc.purpose?.consents?.[1]);
    const google = Boolean(tc.vendor?.consents?.[GOOGLE_VENDOR]);
    if (!zweck1 || !google) return false;
    return cmStatus() === CM_GRANTED;
  }

  function analyticsStatus(){
    try {
      const v = typeof fc.getGoogleConsentModeValues === "function" ? fc.getGoogleConsentModeValues() : null;
      return v && typeof v.analyticsStoragePurposeConsentStatus === "number" ? v.analyticsStoragePurposeConsentStatus : 0;
    } catch (_) { return 0; }
  }

  function usStatus(){
    try {
      const u = fc.usstatesoptout;
      return u && typeof u.getInitialUsStatesOptOutStatus === "function" ? u.getInitialUsStatesOptOutStatus() : 0;
    } catch (_) { return -1; }                         // Fehler → wie Opt-out behandeln
  }

  let tcStand = null;
  let messung = "aus-default";   // "an" | "aus" | "aus-default"
  let gaGeladen = false;

  function messungAn(){
    window[`ga-disable-${GA}`] = false;
    gtag("consent", "update", { analytics_storage: "granted" });
    if (!gaGeladen){
      gaGeladen = true;
      gtag("js", new Date());
      const s = document.createElement("script"); s.async = true;
      s.src = `https://www.googletagmanager.com/gtag/js?id=${GA}`;
      document.head.appendChild(s);
    }
    gtag("config", GA, { allow_google_signals: false, allow_ad_personalization_signals: false });
    messung = "an";
  }

  function messungAus(){
    window[`ga-disable-${GA}`] = true;
    const update = { analytics_storage: "denied" };
    if (!tcStand?.purpose?.consents?.[1]) Object.assign(update, { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied" });
    gtag("consent", "update", update);
    messung = "aus";
  }

  function abgleich(){
    if (uebergang && !googleZustaendig(tcStand)) { eigeneWahlAnwenden(); return; }
    const f = freigabe(tcStand, analyticsStatus, usStatus);
    if (f === true) { if (messung !== "an") messungAn(); }
    else if (f === false) { if (messung !== "aus") messungAus(); }
    else if (messung === "an") messungAus();               // Widerruf: Dialog offen, Einwilligung gelöscht
    // Hat zuvor der Zettel die Messung erlaubt und sagt Google jetzt Nein, verschwinden auch die _ga-Cookies.
    if (zettelHatGemessen && f !== null) { zettelHatGemessen = false; if (f === false) gaRadieren(document, location.hostname); }
  }

  function watchConsent(tries = 0){
    if (typeof window.__tcfapi !== "function"){
      if (tries < 40) setTimeout(() => watchConsent(tries + 1), 250);
      return;
    }
    window.__tcfapi("addEventListener", 2, (tc, ok) => {
      if (!ok || !tc) return;
      tcStand = tc;
      if (googleZustaendig(tc)) googleUebernimmt();
      abgleich();
      if (tc.eventStatus !== "cmpuishown") setTimeout(abgleich, 300);   // CM-Werte ziehen ggf. nach
    });
  }

  /* ── Übergangs-Zettel „Statistik“ ───────────────────────────────────────────────────────────── */
  const WAHL_KEY = "rk-statistik-wahl";        // {"v":1,"wahl":"ja"|"nein","zeit":<ms seit 1970>}
  const GOOGLE_KEY = "rk-statistik-google";    // "1" = Google-CMP hat zuletzt selbst entschieden
  const WAHL_V = 1, WAHL_MONATE = 12, WARTEN_MS = 3000;

  /** Echte TCF-Entscheidung der Google-CMP: Nutzer hat gewählt, oder eine gespeicherte Wahl wurde geladen. */
  function googleEntschieden(tc){
    return Boolean(tc) && (tc.eventStatus === "useractioncomplete" ||
      (tc.eventStatus === "tcloaded" && typeof tc.tcString === "string" && tc.tcString !== ""));
  }
  /** Google ist zuständig: echte Entscheidung, Dialog gerade sichtbar oder DSGVO laut CMP ausdrücklich nicht anwendbar. */
  function googleZustaendig(tc){
    return Boolean(tc) && (tc.gdprApplies === false || googleEntschieden(tc) ||
      (tc.eventStatus === "cmpuishown" && tc.displayStatus !== "hidden" && tc.displayStatus !== "disabled") ||
      tc.displayStatus === "visible");             // „cmpuishown“ mit hidden/disabled ist genau der Fehlerfall: Google zeigt nichts
  }
  /** Gespeicherte eigene Wahl prüfen: "ja" | "nein" | null (fehlt, fremde Version, kaputt oder älter als 12 Monate). */
  function wahlGueltig(eintrag, jetzt){
    if (!eintrag || eintrag.v !== WAHL_V || (eintrag.wahl !== "ja" && eintrag.wahl !== "nein")) return null;
    if (typeof eintrag.zeit !== "number" || !isFinite(eintrag.zeit) || eintrag.zeit > jetzt + 864e5) return null;
    const ablauf = new Date(eintrag.zeit); ablauf.setMonth(ablauf.getMonth() + WAHL_MONATE);
    return jetzt < ablauf.getTime() ? eintrag.wahl : null;
  }
  /** Wer bestimmt jetzt über die Statistik? "google" | "warten" | "gpc" | "ja" | "nein" | "fragen" */
  function zustaendig(tc, reif, wahl, gpcAn){
    if (googleZustaendig(tc)) return "google";
    if (!reif) return "warten";
    if (gpcAn) return "gpc";
    return wahl || "fragen";
  }
  /** Radiert die Analytics-Cookies (_ga, _ga_…) aus: auf dem Host und jeder Elterndomain, jeweils mit und ohne führenden Punkt. */
  function gaRadieren(doc, host){
    const namen = String(doc.cookie || "").split(";").map(k => k.split("=")[0].trim())
      .filter(n => n === "_ga" || n.startsWith("_ga_"));
    const teile = String(host || "").split("."), domains = [""];
    if (!/^[\d.]+$/.test(host || "")) for (let i = 0; i < teile.length - 1; i++) { const d = teile.slice(i).join("."); domains.push(`;domain=${d}`, `;domain=.${d}`); }
    for (const n of namen) for (const d of domains) doc.cookie = `${n}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;max-age=0;path=/${d}`;
    return namen;
  }

  function ablage(key, wert){                  // lesen (ein Argument) bzw. schreiben/löschen (null)
    try {
      if (arguments.length === 1) return window.localStorage.getItem(key);
      if (wert === null) window.localStorage.removeItem(key); else window.localStorage.setItem(key, wert);
    } catch (_) { /* Speicher gesperrt: dann wird eben beim nächsten Besuch erneut gefragt */ }
    return null;
  }
  let wahlDieseSitzung = null;     // falls der Speicher gesperrt ist, gilt die Wahl wenigstens bis zum Neuladen
  function eigenerEintrag(){
    let e = null;
    try { e = JSON.parse(ablage(WAHL_KEY) || "null"); } catch (_) { e = null; }
    if (!wahlGueltig(e, Date.now())) e = wahlDieseSitzung;
    return wahlGueltig(e, Date.now()) ? e : null;
  }
  const eigeneWahl = () => { const e = eigenerEintrag(); return e ? e.wahl : null; };

  let reif = false;            // Wartezeit für die Google-CMP vorbei
  let zettelHatGemessen = false;   // Messung läuft aufgrund der Zettel-Wahl
  let uebergang = false;       // eigener Zettel ist zuständig
  let einstellungenOffen = null;   // Einstellungen angefordert, bevor klar war, wer zuständig ist (Auslöser-Element)

  function statistikAusEigen(){
    window[`ga-disable-${GA}`] = true;
    if (messung !== "aus") gtag("consent", "update", { analytics_storage: "denied" });   // nur Statistik – Werbung bleibt unberührt "denied"
    messung = "aus";
    gaRadieren(document, location.hostname);
  }
  function eigeneWahlAnwenden(){
    if (ohneWerbung) return;                   // ohne Werbung auch kein Analytics
    if (!gpc && eigeneWahl() === "ja") { if (messung !== "an") messungAn(); zettelHatGemessen = true; }
    else if (messung === "an" || eigeneWahl() === "nein") statistikAusEigen();
  }
  function googleUebernimmt(){
    uebergang = false;
    zettelZu(false);
    if (googleEntschieden(tcStand)) {             // echte Google-Entscheidung ersetzt die Zettel-Wahl endgültig
      if (eigeneWahl() === "ja") zettelHatGemessen = true;   // _ga stammen evtl. aus einem früheren Besuch – bei Google-Nein ausradieren
      ablage(WAHL_KEY, null); wahlDieseSitzung = null;
    }
    if (googleEntschieden(tcStand) || tcStand?.gdprApplies === false) ablage(GOOGLE_KEY, "1");
  }
  function wartezeitVorbei(){
    reif = true;
    const wer = zustaendig(tcStand, true, eigeneWahl(), gpc);
    if (wer === "google") googleUebernimmt();
    else {
      uebergang = true;
      ablage(GOOGLE_KEY, null);
      abgleich();
      if (wer === "fragen" && !einstellungenOffen) zettelAuf(null);
    }
    if (einstellungenOffen) { const a = einstellungenOffen; einstellungenOffen = null; einstellungen(a === true ? null : a); }
  }

  /* Der Zettel: ein Blatt Karopapier unten am Rand, blockiert nichts. */
  let zettel = null, zettelStand = null, zettelText = null, zettelWahl = null, zettelOk = null, zettelTitel = null, ausloeser = null;
  const el = (tag, klasse, text) => { const e = document.createElement(tag); if (klasse) e.className = klasse; if (text) e.textContent = text; return e; };

  function zettelBauen(){
    zettel = el("section", "statzettel");
    zettel.id = "statzettel";
    zettel.setAttribute("role", "region");
    zettel.setAttribute("aria-labelledby", "statzettel-titel");
    zettel.setAttribute("aria-describedby", "statzettel-text");
    zettel.hidden = true;
    const marke = el("p", "statzettel-marke", "Statistik · nur Reichweite");
    zettelTitel = el("h2", "statzettel-titel", "Dürfen wir mitzählen?");
    zettelTitel.id = "statzettel-titel"; zettelTitel.tabIndex = -1;
    zettelText = el("p", "statzettel-text");
    zettelText.id = "statzettel-text";
    zettelText.append("Nur mit deinem Ja zählen wir mit Google Analytics (Google Ireland Ltd.), welche Rechner und Ratgeber " +
      "genutzt werden – reine Reichweitenmessung. Google setzt dafür Cookies; Daten können in die USA gelangen. " +
      "Keine Werbung, keine Werbe-Einwilligung. Widerruf jederzeit über „Datenschutz-Einstellungen“ im Seitenfuß. ");
    const mehr = el("a", "", "Datenschutzerklärung"); mehr.href = "/privacy.html#statistik-zettel";
    zettelText.append(mehr, ".");
    zettelStand = el("p", "statzettel-stand"); zettelStand.hidden = true;
    zettelWahl = el("div", "statzettel-wahl");
    const nein = el("button", "stift", "Ablehnen"), ja = el("button", "stift", "Zustimmen");
    nein.type = ja.type = "button";
    nein.addEventListener("click", () => zettelEntscheidung("nein"));
    ja.addEventListener("click", () => zettelEntscheidung("ja"));
    zettelWahl.append(nein, ja);
    zettelOk = el("button", "stift", "Verstanden"); zettelOk.type = "button"; zettelOk.hidden = true;
    zettelOk.addEventListener("click", () => zettelZu(true));
    const zu = el("button", "statzettel-zu", "×"); zu.type = "button";
    zu.setAttribute("aria-label", "Schließen, ohne zu entscheiden");
    zu.addEventListener("click", () => zettelZu(true));        // nur weglegen – es wird nichts gespeichert und nichts gemessen
    zettel.append(marke, zettelTitel, zettelText, zettelStand, zettelWahl, zettelOk, zu);   // Schließen zuletzt in der Tab-Reihenfolge
    zettel.addEventListener("keydown", e => { if (e.key === "Escape") { e.preventDefault(); zettelZu(true); } });   // schließt nur, entscheidet nichts
    const skip = document.querySelector(".skip");          // gleich nach „Zum Inhalt“ im Quelltext, sichtbar aber am unteren Rand
    if (skip && skip.after) skip.after(zettel); else document.body.prepend(zettel);
  }

  function datum(ms){ try { return new Date(ms).toLocaleDateString("de-AT", { day: "numeric", month: "long", year: "numeric" }); } catch (_) { return ""; } }

  function zettelAuf(von){
    if (!zettel) zettelBauen();
    const e = eigenerEintrag();
    if (gpc) {
      zettelStand.textContent = "Dein Browser sendet „Global Privacy Control“. Deshalb bleibt die Statistik aus – du musst nichts tun.";
      zettelStand.hidden = false; zettelWahl.hidden = true; zettelOk.hidden = false;
    } else {
      zettelStand.textContent = e ? `Deine Wahl: ${e.wahl === "ja" ? "zugestimmt" : "abgelehnt"} am ${datum(e.zeit)}.` : "";
      zettelStand.hidden = !e; zettelWahl.hidden = false; zettelOk.hidden = true;
    }
    if (ohneWerbung && !gpc) {
      zettelStand.textContent = (zettelStand.textContent ? zettelStand.textContent + " " : "") + "Auf dieser Seite wird ohnehin nichts gemessen; deine Wahl gilt für die übrigen Seiten.";
      zettelStand.hidden = false;
    }
    zettel.hidden = false;
    document.body.classList.add("mit-statzettel");
    document.body.style.paddingBottom = `${(zettel.offsetHeight || 0) + 24}px`;
    ausloeser = von;
    if (von) zettelTitel.focus();            // nur bei bewusstem Öffnen – beim Seitenaufruf wird kein Fokus gestohlen
  }

  function zettelZu(fokusZurueck){
    if (!zettel || zettel.hidden) return;
    zettel.hidden = true;
    document.body.classList.remove("mit-statzettel");
    document.body.style.paddingBottom = "";
    if (fokusZurueck && ausloeser && ausloeser.isConnected) ausloeser.focus();
    ausloeser = null;
  }

  function zettelEntscheidung(wahl){
    wahlDieseSitzung = { v: WAHL_V, wahl, zeit: Date.now() };
    ablage(WAHL_KEY, JSON.stringify(wahlDieseSitzung));
    zettelZu(true);
    if (wahl === "nein" || ohneWerbung) { if (wahl === "nein") statistikAusEigen(); return; }
    if (uebergang && !googleZustaendig(tcStand)) eigeneWahlAnwenden();
  }

  /** „Datenschutz-Einstellungen“: im Übergang der eigene Zettel, sonst wie bisher die Google-Widerrufsmeldung. */
  function einstellungen(von){
    if (ohneWerbung) {
      // Ohne Werbung ist die Google-CMP hier nicht geladen. Hat sie zuletzt selbst entschieden, öffnet die Startseite ihren Dialog.
      if (ablage(GOOGLE_KEY) === "1") { location.href = "/#datenschutz-einstellungen"; return; }
      zettelAuf(von);
      return;
    }
    if (googleZustaendig(tcStand) || (reif && !uebergang)) {
      fc.callbackQueue.push(() => { if (typeof fc.showRevocationMessage === "function") fc.showRevocationMessage(); });
      return;
    }
    if (!reif) { einstellungenOffen = von || true; return; }   // gleich nach der Wartezeit
    zettelAuf(von);
  }

  document.addEventListener("click", e => {
    const knopf = e.target.closest && e.target.closest("[data-privacy-settings]");
    if (!knopf) return;
    e.preventDefault();
    einstellungen(knopf);
  });

  window.RK_EINWILLIGUNG = { googleEntschieden, googleZustaendig, wahlGueltig, zustaendig, gaRadieren, WAHL_KEY, GOOGLE_KEY };

  if (!ohneWerbung) {
    fc.callbackQueue.push({ CONSENT_MODE_DATA_READY: abgleich, INITIAL_US_STATES_OPT_OUT_DATA_READY: abgleich });
    loadAds();
    watchConsent();
    setTimeout(wartezeitVorbei, WARTEN_MS);
  }
  if (location.hash === "#datenschutz-einstellungen") {
    try { history.replaceState(null, "", location.pathname + location.search); } catch (_) {}
    einstellungen(null);
  }
})();
