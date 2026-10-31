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
   Werte laut developers.google.com/funding-choices/fc-api-docs */
(() => {
  const PUB = "ca-pub-7811071715414905";
  const GA = "G-T00HRG2YVF";
  const GOOGLE_VENDOR = 755;
  const CM_GRANTED = 1, CM_NOT_APPLICABLE = 3;
  const US_OHNE_OPTOUT = [1, 2];   // usstatesoptout: DOES_NOT_APPLY, NOT_OPTED_OUT (3 = OPTED_OUT, 0 = UNKNOWN)

  // Consent-Mode-Grundwerte vor jedem Google-Skript (auch vor adsbygoogle.js)
  const dl = window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function(){ dl.push(arguments); };
  window[`ga-disable-${GA}`] = true;
  window.gtag("consent", "default", {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    analytics_storage: "denied",
    wait_for_update: 500
  });
  const fc = window.googlefc = window.googlefc || {};
  fc.callbackQueue = fc.callbackQueue || [];

  // Anzeigenblöcke: Block-IDs werden nach der AdSense-Freigabe hier eingetragen.
  const SLOTS = { billboard: "", rect: "", half: "", superbanner: "", sky: "" };
  // Feste IAB-Formate: Superbanner 728×90, Wide Skyscraper 160×600. Die übrigen Plätze sind responsiv
  // (Billboard 970×250 / Leaderboard 728×90 / Mobile 320×100, Half Page 300×600, Medium Rectangle 300×250).
  const FIXED = { superbanner: [728, 90], sky: [160, 600] };

  const gpc = navigator.globalPrivacyControl === true;

  function loadAds(){
    if (gpc) return;
    const s = document.createElement("script");
    s.async = true; s.crossOrigin = "anonymous";
    s.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${PUB}`;
    document.head.appendChild(s);
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
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    });
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
    const f = freigabe(tcStand, analyticsStatus, usStatus);
    if (f === true) { if (messung !== "an") messungAn(); }
    else if (f === false) { if (messung !== "aus") messungAus(); }
    else if (messung === "an") messungAus();               // Widerruf: Dialog offen, Einwilligung gelöscht
  }

  function watchConsent(tries = 0){
    if (typeof window.__tcfapi !== "function"){
      if (tries < 40) setTimeout(() => watchConsent(tries + 1), 250);
      return;
    }
    window.__tcfapi("addEventListener", 2, (tc, ok) => {
      if (!ok || !tc) return;
      tcStand = tc;
      abgleich();
      if (tc.eventStatus !== "cmpuishown") setTimeout(abgleich, 300);   // CM-Werte ziehen ggf. nach
    });
  }
  fc.callbackQueue.push({ CONSENT_MODE_DATA_READY: abgleich, INITIAL_US_STATES_OPT_OUT_DATA_READY: abgleich });

  // Link „Datenschutz-Einstellungen" im Seitenfuß öffnet den Google-Dialog erneut
  document.addEventListener("click", e => {
    if (!e.target.closest("[data-privacy-settings]")) return;
    e.preventDefault();
    fc.callbackQueue.push(() => { if (typeof fc.showRevocationMessage === "function") fc.showRevocationMessage(); });
  });

  loadAds();
  watchConsent();
})();
