"""Eigenwert (18.11.2026): Beispiele zum Anklicken, zwei Rechner mit gesetzlichen Sätzen, eigene Grafiken und
„Mit deinen Werten ausprobieren“ für die Ratgeber. Alle Zahlen werden hier berechnet; Sätze kommen aus content/referenz.py."""
import math
from urllib.parse import urlencode
from content.calcs import form, inp, select, de, eur
from content import referenz as R
from content import guides as G

REF = "/saetze-und-grenzwerte.html"


def q(**kw):
    return urlencode(kw)


# ---------- Beispiele zum Anklicken: Rechner-Kennung → [(Beschriftung, Eingaben)]
EX = {
    "percent": [("15 % von 80", dict(mode="anteil", a=80, b=15)), ("12 von 48 in Prozent", dict(mode="satz", a=12, b=48)),
                ("von 80 auf 96", dict(mode="veraenderung", a=80, b=96)), ("59,90 € nach 25 % Rabatt: Preis davor", dict(mode="ursprung", a="59,90", b=25)),
                ("Zins von 2 % auf 3 %", dict(mode="veraenderung", a=2, b=3))],
    "mwst": [("119 € brutto, Deutschland 19 %", dict(dir="b2n", amount=119, rate=19)), ("360 € brutto, Österreich 20 %", dict(dir="b2n", amount=360, rate=20)),
             ("250 € netto plus 20 %", dict(dir="n2b", amount=250, rate=20)), ("Lebensmittel 4,9 %: 10,49 € brutto", dict(dir="b2n", amount="10,49", rate="4.9")),
             ("Hotel Deutschland 7 %: 107 € brutto", dict(dir="b2n", amount=107, rate=7))],
    "rabatt": [("30 % und dann 20 %", dict(price=100, r1=30, r2=20, skonto="")), ("20 % Rabatt plus 3 % Skonto", dict(price=8000, r1=20, r2="", skonto=3)),
               ("nur 2 % Skonto auf 1.500 €", dict(price=1500, r1="", r2="", skonto=2)), ("50 % und 50 %", dict(price=80, r1=50, r2=50, skonto=""))],
    "zins": [("100 € im Monat, 20 Jahre, 3 %", dict(start=0, monthly=100, rate=3, years=20)), ("10.000 € einmalig, 10 Jahre, 2,5 %", dict(start=10000, monthly=0, rate="2,5", years=10)),
             ("5.000 € Start plus 50 € im Monat, 18 Jahre, 4 %", dict(start=5000, monthly=50, rate=4, years=18)), ("Festgeld 18 Monate, 3 %", dict(start=20000, monthly=0, rate=3, years="1,5"))],
    "kredit": [("20.000 €, 5 Jahre, 4,5 %", dict(amount=20000, rate="4,5", years=5)), ("Autokredit 15.000 €, 4 Jahre, 6,9 %", dict(amount=15000, rate="6,9", years=4)),
               ("Wohnkredit 200.000 €, 25 Jahre, 3,5 %", dict(amount=200000, rate="3,5", years=25)), ("0-%-Finanzierung 2.400 €, 2 Jahre", dict(amount=2400, rate=0, years=2))],
    "kreditvergleich": [("niedriger Zins mit Gebühren gegen höheren ohne", dict(amount=20000, years=5, a_rate="4,5", a_fee=0, a_monthly=0, b_rate="3,9", b_fee=400, b_monthly=3)),
                        ("15.000 €: 4,5 % plus 400 € gegen 5,2 %", dict(amount=15000, years=5, a_rate="4,5", a_fee=400, a_monthly=0, b_rate="5,2", b_fee=0, b_monthly=0)),
                        ("nur Kontoführung 5 € im Monat", dict(amount=25000, years=7, a_rate="4,9", a_fee=0, a_monthly=5, b_rate="4,9", b_fee=0, b_monthly=0))],
    "inflation": [("1.000 € in 10 Jahren bei 2 %", dict(amount=1000, rate=2, years=10)), ("Österreich 2025: 3,6 %", dict(amount=10000, rate="3,6", years=10)),
                  ("Deutschland 2025: 2,2 %", dict(amount=10000, rate="2,2", years=10)), ("50.000 € in 25 Jahren bei 2 %", dict(amount=50000, rate=2, years=25))],
    "dreisatz": [("4 Brötchen kosten 3 €, was kosten 10?", dict(kind="pro", a=4, b=3, c=10)), ("3 Maler brauchen 8 Tage, 4 Maler?", dict(kind="anti", a=3, b=8, c=4)),
                 ("250 g kosten 1,99 €, Preis für 1.000 g", dict(kind="pro", a=250, b="1,99", c=1000)), ("bei 100 km/h 3 Stunden, bei 120 km/h?", dict(kind="anti", a=100, b=3, c=120))],
    "bruch": [("3/4 + 5/6", dict(a=3, b=4, op="+", c=5, d=6)), ("2/3 von 3/4", dict(a=2, b=3, op="*", c=3, d=4)), ("7/8 − 1/3", dict(a=7, b=8, op="-", c=1, d=3)),
              ("3/4 geteilt durch 1/8", dict(a=3, b=4, op="/", c=1, d=8)), ("84/126 kürzen", dict(a=84, b=126, op="*", c=1, d=1))],
    "einheit": [("55 Zoll in cm", {"cat": "laenge", "value": 55, "from": "Zoll", "to": "cm"}), ("1 Joch in m²", {"cat": "flaeche", "value": 1, "from": "Joch", "to": "m²"}),
                ("25 dag in g", {"cat": "masse", "value": 25, "from": "dag", "to": "g"}), ("70 mph in km/h", {"cat": "tempo", "value": 70, "from": "mph", "to": "km/h"}),
                ("350 °F in °C", {"cat": "temp", "value": 350, "from": "°F", "to": "°C"}), ("1 Cup (US) in ml", {"cat": "volumen", "value": 1, "from": "Cup (US)", "to": "ml"})],
    "schnitt": [("Schularbeiten 2 1 3 2 4", dict(values="2 1 3 2 4", weights="")), ("Noten mit doppelt zählenden Schularbeiten", dict(values="2 3 1 2 1", weights="2 2 1 1 1")),
                ("Gehälter mit einem Ausreißer", dict(values="2400 2600 2700 2900 9500", weights="")), ("zweimal tanken: 1,60 € und 1,80 €", dict(values="1,60 1,80", weights="40 20"))],
    "lohn": [("3.000 € bei 38,5 Stunden, 14 Gehälter", dict(dir="m2h", amount=3000, hours="38,5", salaries=14)), ("dieselben 3.000 € mit 12 Gehältern", dict(dir="m2h", amount=3000, hours="38,5", salaries=12)),
             ("Mindestlohn Deutschland 13,90 €, 40 Stunden", dict(dir="h2m", amount="13,90", hours=40, salaries=12)), ("Teilzeit 20 Stunden, 1.400 €", dict(dir="m2h", amount=1400, hours=20, salaries=14))],
    "strom": [("Fernseher 100 W, 4 Stunden täglich", dict(mode="watt", watt=100, hours=4, days=365, price=30)), ("Router 10 W, rund um die Uhr", dict(mode="watt", watt=10, hours=24, days=365, price=30)),
              ("Kühlschrank laut Label 150 kWh", dict(mode="label", kwh=150, price=30)), ("Heizlüfter 2.000 W, 3 Stunden an 60 Tagen", dict(mode="watt", watt=2000, hours=3, days=60, price=30))],
    "fahrt": [("Wien–Salzburg und zurück zu dritt", dict(fuel="fuel", km=300, trip=2, cons="6,5", price="1,70", people=3)), ("Pendeln 28 km einfach, allein", dict(fuel="fuel", km=28, trip=2, cons=6, price="1,70", people=1)),
              ("Elektroauto 230 km, zu Hause geladen", dict(fuel="ev", km=230, trip=1, cons=18, price="0,30", people=1)), ("Elektroauto 230 km, Schnelllader 0,65 €", dict(fuel="ev", km=230, trip=1, cons=18, price="0,65", people=1))],
    "tip": [("87,40 € zu viert, 10 %", dict(bill="87,40", pct=10, round=1, people=4)), ("Kaffee 4,20 €, aufrunden", dict(bill="4,20", pct=0, round="0.5", people=1)),
            ("Abendessen 126 € zu zweit, 8 %", dict(bill=126, pct=8, round=5, people=2)), ("Taxi 23,60 €, 5 %", dict(bill="23,60", pct=5, round=1, people=1))],
    "marge": [("Einkauf 60 €, Verkauf 100 €", dict(mode="ekvk", ek=60, b=100, vat=20)), ("Einkauf 60 € plus 50 % Aufschlag", dict(mode="auf", ek=60, b=50, vat=20)),
              ("Einkauf 60 €, Zielmarge 40 %", dict(mode="span", ek=60, b=40, vat=20)), ("Deutschland: Einkauf 12 €, Zielmarge 55 %", dict(mode="span", ek=12, b=55, vat=19))],
    "pendler": [("Österreich: 32 km, Öffis zumutbar", dict(land="at", km=32, art="klein", tage=11, gsat=30)), ("Österreich: 45 km, Öffis unzumutbar", dict(land="at", km=45, art="gross", tage=11, gsat=40)),
                ("Österreich: Teilzeit, 8 Fahrten im Monat", dict(land="at", km=45, art="klein", tage=8, gsat=30)), ("Österreich: 15 km – klein oder groß?", dict(land="at", km=15, art="klein", tage=20, gsat=0)),
                ("Deutschland: 28 km, 220 Tage", dict(land="de", km=28, atage=220, auto=1, andere="", gsde="")), ("Deutschland: 80 km mit der Bahn", dict(land="de", km=80, atage=220, auto=0, andere="", gsde=""))],
    "verzug": [("Deutschland, Privatkunde: 1.200 € seit 1.3.2026", dict(land="de_v", betrag=1200, von="2026-03-01", bis="2026-10-31")),
               ("Deutschland, Firmenkunde: 5.000 €", dict(land="de_u", betrag=5000, von="2026-01-15", bis="2026-10-31")),
               ("Österreich, Unternehmer: 5.000 €", dict(land="at_u", betrag=5000, von="2026-01-15", bis="2026-10-31")),
               ("Österreich, 4 % fest: 1.200 €", dict(land="at_v", betrag=1200, von="2026-03-01", bis="2026-10-31")),
               ("über den Zinssprung 2024/2025", dict(land="de_u", betrag=10000, von="2024-10-01", bis="2025-03-31"))],
}


def beispiele(calc):
    items = EX.get(calc, [])
    if not items:
        return ""
    b = "".join(f'<button type="button" class="chip" data-ex="{urlencode(v)}" aria-pressed="false">{t}</button>' for t, v in items)
    return f'<div class="ex no-print" role="group" aria-label="Beispiele zum Anklicken"><span>Beispiele:</span>{b}</div>'


def mit_beispielen(form_html, calc):
    """Setzt die Beispiel-Knöpfe direkt vor die Ergebnisfläche des Formulars."""
    marker = '<div data-out aria-live="polite"></div>'
    assert marker in form_html, calc
    return form_html.replace(marker, beispiele(calc) + marker)


# ---------- Grafiken (SVG, aus denselben Zahlen wie der Text)
W, H, PL, PB, PT, PR = 480, 250, 66, 40, 16, 12


def _sx(x, x0, x1):
    return PL + (x - x0) / (x1 - x0) * (W - PL - PR)


def _sy(y, y0, y1):
    return H - PB - (y - y0) / (y1 - y0) * (H - PB - PT)


def linien(serien, xt, yt, xlab, titel, cap, yfmt=lambda v: de(v, 0), marke=None):
    """serien: [(Name, [(x, y)…], Stil)], xt/yt: Achsenwerte. Stil 'a' = Füllerblau, 'b' = gestrichelt."""
    x0, x1, y0, y1 = xt[0], xt[-1], yt[0], yt[-1]
    g = "".join(f'<line x1="{PL}" x2="{W - PR}" y1="{_sy(y, y0, y1):.1f}" y2="{_sy(y, y0, y1):.1f}"/><text x="{PL - 6}" y="{_sy(y, y0, y1) + 4:.1f}" text-anchor="end">{yfmt(y)}</text>' for y in yt)
    g += "".join(f'<text x="{_sx(x, x0, x1):.1f}" y="{H - PB + 16}" text-anchor="middle">{de(x, 0)}</text>' for x in xt)
    g += f'<text x="{(PL + W - PR) / 2:.0f}" y="{H - 2}" text-anchor="middle">{xlab}</text>'
    leg = ""
    for name, pts, stil in serien:
        d = " ".join(f'{"M" if i == 0 else "L"}{_sx(x, x0, x1):.1f} {_sy(y, y0, y1):.1f}' for i, (x, y) in enumerate(pts))
        g += f'<path d="{d}" fill="none" class="ln ln-{stil}"/>'
        leg += f'<span><i class="lg-{stil}"></i>{name}</span>'
    if marke:
        mx, my, mt = marke
        g += f'<circle cx="{_sx(mx, x0, x1):.1f}" cy="{_sy(my, y0, y1):.1f}" r="5" class="pt"/><text x="{_sx(mx, x0, x1) + 9:.1f}" y="{_sy(my, y0, y1) + 16:.1f}" class="lbl">{mt}</text>'
    return f'<figure class="chart fig"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{titel}">{g}</svg><figcaption><span class="legend">{leg}</span>{cap}</figcaption></figure>'


def balken(items, titel, cap, einheit="", ymax=None, noten=()):
    """items: [(Beschriftung, Wert, Stil)], noten: [(Index von, Index bis, Text)] als Klammer über zwei Balken."""
    ymax = ymax or max(v for _, v, _ in items) * 1.25
    n = len(items); bw = (W - PL - PR) / n
    g = f'<line x1="{PL}" x2="{W - PR}" y1="{H - PB}" y2="{H - PB}"/>'
    xs = []
    for i, (lab, v, stil) in enumerate(items):
        x = PL + i * bw + bw * 0.22; w = bw * 0.56; y = _sy(v, 0, ymax)
        xs.append((x + w / 2, y))
        g += f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{H - PB - y:.1f}" class="bar bar-{stil}"/>'
        g += f'<text x="{x + w / 2:.1f}" y="{y - 6:.1f}" text-anchor="middle" class="lbl">{de(v, 2)}{einheit}</text><text x="{x + w / 2:.1f}" y="{H - PB + 16}" text-anchor="middle">{lab}</text>'
    for a, b, t in noten:
        ya = min(xs[a][1], xs[b][1]) - 26
        g += f'<path d="M{xs[a][0]:.1f} {ya + 6:.1f}V{ya:.1f}H{xs[b][0]:.1f}V{ya + 6:.1f}" fill="none" class="ln ln-b"/><text x="{(xs[a][0] + xs[b][0]) / 2:.1f}" y="{ya - 5:.1f}" text-anchor="middle" class="lbl">{t}</text>'
    return f'<figure class="chart fig"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{titel}">{g}</svg><figcaption>{cap}</figcaption></figure>'


def probier(href, text, was):
    return f'<p class="probier no-print"><a class="btn-beleg" href="{href}">{text}</a><span class="small muted">{was}</span></p>'


def _rest(K, p, rate, monate, extra=None):
    pts, b, i = [(0, K)], K, p / 100 / 12
    for m in range(1, monate + 1):
        b = max(0.0, b * (1 + i) - rate - ((extra or {}).get(m, 0)))
        pts.append((m, b))
        if b <= 0:
            break
    return pts


_s_ohne = _rest(G._K, G._p, G._r, 60)
_s_mit = _rest(G._K, G._p, G._r, 60, {12: 2000})
_kk = lambda r, n: 10000 / (1 + r / 100) ** n

# Ratgeber-Kennung → (HTML, das direkt nach dem ersten Absatz eingefügt wird)
ARTIKEL_PLUS = {
    "prozent-oder-prozentpunkte": balken([("vorher", 2, "b"), ("nachher", 3, "a")], "Balken: Zinssatz 2 Prozent und 3 Prozent",
        "Dieselbe Veränderung, zwei richtige Angaben: Der Abstand der Balken ist 1 Prozentpunkt, der neue Balken ist um die Hälfte höher als der alte.", " %", 4.2,
        [(0, 1, "+1 Prozentpunkt = +50 %")])
        + probier("/prozentrechner.html?" + q(mode="veraenderung", a=2, b=3), "Mit deinen Zahlen ausprobieren", "Der Prozentrechner zeigt die relative Veränderung; die Prozentpunkte sind die Differenz deiner beiden Eingaben."),
    "grundwert-richtig-waehlen": balken([("Ausgangspreis", 100, "b"), ("nach +25 %", 125, "a"), ("nach −25 %", 93.75, "a")], "Balken: 100 Euro, plus 25 Prozent, dann minus 25 Prozent",
        "Erst +25 %, dann −25 %: Der zweite Prozentsatz bezieht sich auf 125 € und nimmt deshalb 31,25 € weg, nicht 25 €.", " €", 165, [(1, 2, "−25 % von 125 € = −31,25 €")])
        + probier("/prozentrechner.html?" + q(mode="veraenderung", a=125, b=100), "Rückweg nachrechnen: von 125 auf 100", "Im Rechenweg steht, welcher Wert der Grundwert ist."),
    "kredit-sondertilgung": linien([("mit 2.000 € Sondertilgung nach 12 Monaten", _s_mit, "a"), ("ohne Sondertilgung", _s_ohne, "b")], [0, 12, 24, 36, 48, 60], [0, 5000, 10000, 15000, 20000],
        "Monate seit Auszahlung", "Restschuld mit und ohne Sondertilgung",
        f"Restschuld des Beispielkredits ({eur(G._K)}, {de(G._p, 1)} %, Rate {eur(G._r)}). Nach der Sondertilgung läuft die Kurve tiefer und erreicht null nach {12 + G._mA} statt 60 Monaten.", lambda v: de(v, 0) + " €")
        + probier("/kreditrechner.html?" + q(amount=18000, rate="4,5", years=5, vgl=q(amount=20000, rate="4,5", years=5)), "Eigene Kreditsumme im Vergleich rechnen",
                  "Öffnet den Kreditrechner mit zwei Szenarien nebeneinander: 20.000 € und 18.000 € bei gleicher Laufzeit. Den Zeitpunkt einer Sondertilgung bildet der Rechner nicht ab."),
    "stromtarife-vergleichen": linien([("Tarif A: höhere Grundgebühr, niedrigerer Arbeitspreis", [(x, G._gA * 12 + G._aA * x) for x in (0, 5000)], "a"),
                                       ("Tarif B: niedrigere Grundgebühr, höherer Arbeitspreis", [(x, G._gB * 12 + G._aB * x) for x in (0, 5000)], "b")],
        [0, 1000, 2000, 3000, 4000, 5000], [0, 400, 800, 1200, 1600], "Jahresverbrauch in kWh", "Jahreskosten zweier Stromtarife nach Verbrauch",
        f"Die beiden Beispieltarife aus dem Text. Die Linien schneiden sich bei {de(G._be, 0)} kWh: Darunter ist Tarif B günstiger, darüber Tarif A.", lambda v: de(v, 0) + " €",
        (G._be, G._gA * 12 + G._aA * G._be, f"Gewinnschwelle {de(G._be, 0)} kWh"))
        + probier("/stromkosten-rechner.html?" + q(mode="label", kwh=3500, price=28, vgl=q(mode="label", kwh=3500, price=32)), "Zwei Arbeitspreise für deinen Verbrauch vergleichen",
                  "Öffnet den Stromkosten-Rechner mit 28 und 32 Cent nebeneinander. Die Grundgebühr rechnet er nicht mit – sie kommt wie in Formel 1 dazu."),
    "realzins-sparen-inflation": linien([("bei 2,2 % Inflation (Deutschland 2025)", [(n, _kk(2.2, n)) for n in range(0, 21)], "a"), ("bei 3,6 % Inflation (Österreich 2025)", [(n, _kk(3.6, n)) for n in range(0, 21)], "b")],
        [0, 5, 10, 15, 20], [0, 2500, 5000, 7500, 10000], "Jahre", "Kaufkraft von 10.000 Euro bei gleichbleibender Inflation",
        f"Kaufkraft von 10.000 € ohne Verzinsung, wenn die Jahresraten von 2025 unverändert blieben – eine Annahme, keine Prognose. Nach 20 Jahren: {eur(_kk(2.2, 20))} bzw. {eur(_kk(3.6, 20))}.", lambda v: de(v, 0) + " €")
        + probier("/inflationsrechner.html?" + q(amount=10000, rate="3,6", years=10, vgl=q(amount=10000, rate="2,2", years=10)), "Mit deinem Betrag und deiner Rate rechnen", "Öffnet den Inflationsrechner mit beiden Raten als Szenario A und B."),
    "bruttolohn-14-gehaelter": probier("/stundenlohn-rechner.html?" + q(dir="m2h", amount=3000, hours="38,5", salaries=14, vgl=q(dir="m2h", amount=3000, hours="38,5", salaries=12)),
                                       "Stundenlohn mit 14 und mit 12 Gehältern vergleichen", f'Brutto-Vergleich im Stundenlohn-Rechner. Die festen Sätze für Sonderzahlungen stehen mit Fundstelle in der Tabelle <a href="{REF}?q=sonstige+bez%C3%BCge">Sätze und Grenzwerte</a>.'),
    "skonto-oder-ratenzahlung": probier("/rabatt-rechner.html?" + q(price=8000, r1="", r2="", skonto=3), "Skonto für deinen Rechnungsbetrag ausrechnen",
                                        f'Wird nicht rechtzeitig gezahlt, zeigt der <a href="/verzugszinsen-rechner.html">Verzugszinsen-Rechner</a> die gesetzlichen Zinsen taggenau.'),
    "waermepumpe-stromkosten": probier("/stromkosten-rechner.html?" + q(mode="label", kwh=round(G._wp_kwh), price=round(G._p_wp * 100), vgl=q(mode="label", kwh=round(G._wp_kwh), price=round(G._p_std * 100))),
                                       "Strombedarf mit zwei Strompreisen vergleichen", f"Öffnet den Stromkosten-Rechner mit dem Beispiel aus Schritt 3 ({de(G._wp_kwh, 0)} kWh) bei {de(G._p_wp * 100, 0)} und {de(G._p_std * 100, 0)} Cent."),
}


# ---------- Rechner 1: Pendlerrechner
def _pp(art, km, tage):
    base = 0
    for j, (ab, e) in enumerate(R.PENDLER_AT[art]):
        if (km >= ab) if j == 0 else (km > ab):
            base = e
    f = 1 if tage >= 11 else 2 / 3 if tage >= 8 else 1 / 3 if tage >= 4 else 0
    return (base * f, R.PENDLEREURO_AT * km * f) if base else (0, 0)


def _ep(km, tage, auto=True):
    roh = math.floor(km) * tage * R.ENTF_DE
    return roh if auto else min(roh, R.ENTF_DE_MAX)


def _stufen_tab():
    def rows(art):
        t = R.PENDLER_AT[art]
        return "".join(f"<tr><td>{'ab' if j == 0 else 'über'} {ab} km{f' bis {t[j + 1][0]} km' if j + 1 < len(t) else ''}</td><td>{eur(e)}</td><td>{eur(e / 12)}</td></tr>" for j, (ab, e) in enumerate(t))
    return (f'<div class="scroll"><table class="tbl"><thead><tr><th>Einfache Strecke</th><th>pro Jahr</th><th>pro Monat</th></tr></thead><tbody>'
            f'<tr><th colspan="3" scope="rowgroup">Kleines Pendlerpauschale – Massenverkehrsmittel zumutbar (lit. c)</th></tr>{rows("klein")}'
            f'<tr><th colspan="3" scope="rowgroup">Großes Pendlerpauschale – Massenverkehrsmittel mindestens auf halber Strecke unzumutbar (lit. d)</th></tr>{rows("gross")}</tbody></table></div>')


_a1 = _pp("klein", 32, 11); _a2 = _pp("klein", 45, 8); _a3 = _pp("gross", 45, 11)
_d1 = _ep(28, 220); _d2 = _ep(80, 220, False); _d2roh = _ep(80, 220)
_de_gleich = math.ceil(R.AN_PAUSCH_DE / (220 * R.ENTF_DE))

PENDLER = {
"slug": "pendlerrechner", "short": "Pendlerrechner", "sym": "⇄",
"teaser": "Pendlerpauschale und Pendlereuro (Österreich), Entfernungspauschale (Deutschland) – mit den Sätzen aus dem Gesetz.",
"title": "Pendlerrechner: Pendlerpauschale und Entfernungspauschale",
"h1": "Pendlerrechner für Österreich und Deutschland",
"lead": "Was steht dir für den Arbeitsweg steuerlich zu? Der Rechner wendet die Stufen und Sätze aus dem Gesetzestext an und zeigt, welche Stufe gilt und warum.",
"description": "Pendlerpauschale und Pendlereuro in Österreich, Entfernungspauschale in Deutschland berechnen – mit Rechenweg, Stufen aus dem Gesetz, Fundstelle und Abrufdatum.",
"formula": "AT: Stufe × Anteil · DE: km × Tage × 0,38 €",
"form": form("pendler",
    select("land", "Land", [("at", "Österreich"), ("de", "Deutschland")], "at")
    + inp("km", "Einfache Strecke Wohnung–Arbeit (km)", "32")
    + '<div data-show-when="land=at" class="fields sub">'
    + select("art", "Massenverkehrsmittel", [("klein", "zumutbar (kleines Pendlerpauschale)"), ("gross", "mindestens auf halber Strecke unzumutbar (großes)")], "klein").replace('class="f"', 'class="f wide"', 1)
    + inp("tage", "Fahrten zur Arbeit pro Kalendermonat", "11", "numeric")
    + select("gsat", "Grenzsteuersatz (optional, für den Überschlag)", [("0", "nicht berechnen"), ("20", "20 %"), ("30", "30 %"), ("40", "40 %"), ("48", "48 %"), ("50", "50 %")], "30")
    + '</div><div data-show-when="land=de" class="fields sub">'
    + inp("atage", "Arbeitstage mit Fahrt pro Jahr", "220", "numeric")
    + select("auto", "Verkehrsmittel", [("1", "eigener oder überlassener Pkw"), ("0", "anderes (Bahn, Bus, Rad, Mitfahrt)")], "1")
    + inp("andere", "Andere Werbungskosten im Jahr (€, optional)", "")
    + inp("gsde", "Grenzsteuersatz (%, optional)", "")
    + "</div>"),
"body": f"""
<h2>Was der Rechner ausgibt</h2>
<p>In beiden Ländern wird der Arbeitsweg über einen Abzug bei der Steuerberechnung berücksichtigt – die Pauschale selbst wird nicht ausgezahlt. Die Regeln sind aber verschieden gebaut:</p>
<div class="scroll"><table class="tbl text"><thead><tr><th></th><th>Österreich</th><th>Deutschland</th></tr></thead><tbody>
<tr><td>Was zählt</td><td>Entfernungsstufe und ob ein Massenverkehrsmittel zumutbar ist</td><td>jeder volle Kilometer der einfachen Entfernung</td></tr>
<tr><td>Rolle der Arbeitstage</td><td>Fahrten pro Kalendermonat: ab 11 voll, 8 bis 10 zwei Drittel, 4 bis 7 ein Drittel</td><td>jeder Arbeitstag mit Fahrt zählt einzeln</td></tr>
<tr><td>Verkehrsmittel</td><td>entscheidet zwischen kleinem und großem Pauschale</td><td>egal – außer beim Höchstbetrag von {eur(R.ENTF_DE_MAX)}</td></tr>
<tr><td>Wirkung</td><td>Pendlerpauschale mindert die Bemessungsgrundlage; der Pendlereuro mindert die Steuer direkt</td><td>Werbungskosten; wirksam, soweit alle Werbungskosten {eur(R.AN_PAUSCH_DE)} übersteigen</td></tr>
<tr><td>Fundstelle</td><td>§ 16 Abs. 1 Z 6 und § 33 Abs. 5 Z 4 EStG 1988</td><td>§ 9 Abs. 1 Satz 3 Nr. 4 und § 9a EStG</td></tr>
</tbody></table></div>
<p>Alle Sätze stehen mit Link zum Gesetzestext, Fassung und Abrufdatum in der Tabelle <a href="{REF}?q=arbeitsweg">Sätze und Grenzwerte</a>. Stand der Werte: {R.ABRUF}.</p>
<h2>Österreich: die Stufen des Pendlerpauschales</h2>
{_stufen_tab()}
<p>Dazu kommt der <strong>Pendlereuro</strong>: {R.PENDLEREURO_AT} € pro Jahr für jeden Kilometer der einfachen Strecke, wenn Anspruch auf ein Pendlerpauschale besteht. Für ihn gilt dieselbe Drittel-Regel. Die hier verwendete Fassung von § 33 Abs. 5 Z 4 gilt laut Rechtsinformationssystem bis 31. Dezember 2026; welche Werte ab 2027 gelten, haben wir nicht geprüft.</p>
<div class="example"><strong>Durchgerechnet (konstruiertes Beispiel):</strong> 32 km, Massenverkehrsmittel zumutbar, 11 oder mehr Fahrten im Monat. Stufe „ab 20 km bis 40 km“: {eur(_a1[0])} Pendlerpauschale im Jahr, dazu 32 × {R.PENDLEREURO_AT} € = {eur(_a1[1])} Pendlereuro. Bei einem Grenzsteuersatz von 30 % senkt das Pauschale die Lohnsteuer um {eur(_a1[0] * 0.3)}, der Pendlereuro um weitere {eur(_a1[1])} – zusammen {eur(_a1[0] * 0.3 + _a1[1])} im Jahr.</div>
<div class="example"><strong>Teilzeit:</strong> 45 km, zumutbar, 8 Fahrten im Monat. Stufe „über 40 km bis 60 km“: {eur(R.PENDLER_AT["klein"][1][1])}, davon zwei Drittel = {eur(_a2[0])}; Pendlereuro 45 × {R.PENDLEREURO_AT} € × 2/3 = {eur(_a2[1])}. Wäre das Massenverkehrsmittel auf mindestens der halben Strecke nicht zumutbar und führe man an 11 Tagen, wären es {eur(_a3[0])}.</div>
<h3>Wann zählt ein Tag?</h3>
<p>Das Gesetz stellt auf Fahrten von der Wohnung zur Arbeitsstätte im Kalendermonat ab. Für Feiertage, Urlaub und Krankenstand ist das Pauschale weiter zu berücksichtigen (lit. h). Wer ein arbeitgebereigenes Kraftfahrzeug für den Arbeitsweg nutzen darf, bekommt kein Pendlerpauschale; für ein arbeitgebereigenes Fahrrad oder Elektrofahrrad gilt das nicht (lit. b).</p>
<h2>Deutschland: die Entfernungspauschale</h2>
<p class="formula">volle Kilometer × Arbeitstage × {de(R.ENTF_DE, 2)} €</p>
<p>Angesetzt wird die einfache Entfernung, nicht Hin- und Rückweg, und nur volle Kilometer. Maßgebend ist die kürzeste Straßenverbindung; eine längere darf angesetzt werden, wenn sie offensichtlich verkehrsgünstiger ist und regelmäßig benutzt wird.</p>
<div class="example"><strong>Durchgerechnet (konstruiertes Beispiel):</strong> 28 km, 220 Arbeitstage: 28 × 220 × {de(R.ENTF_DE, 2)} € = {eur(_d1)}. Ohne weitere Werbungskosten liegen davon {eur(_d1 - R.AN_PAUSCH_DE)} über dem Arbeitnehmer-Pauschbetrag von {eur(R.AN_PAUSCH_DE)} – nur dieser Teil senkt das zu versteuernde Einkommen zusätzlich.</div>
<div class="example"><strong>Höchstbetrag:</strong> 80 km mit der Bahn, 220 Tage: rechnerisch {eur(_d2roh)}, anzusetzen sind höchstens {eur(_d2)}. Mit eigenem oder zur Nutzung überlassenem Kraftwagen gilt die Grenze nicht.</div>
<p>Bei 220 Arbeitstagen und ohne andere Werbungskosten übersteigt die Pauschale den Arbeitnehmer-Pauschbetrag erst ab {_de_gleich} vollen Kilometern ({_de_gleich} × 220 × {de(R.ENTF_DE, 2)} € = {eur(_de_gleich * 220 * R.ENTF_DE)}). Bei kürzeren Wegen bringt sie allein nichts – zusammen mit anderen Werbungskosten aber schon. Dafür gibt es das Feld „Andere Werbungskosten“.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Hin- und Rückweg eintragen:</strong> Beide Länder rechnen mit der einfachen Strecke.</div>
<div class="warn"><strong>Freibetrag mit Auszahlung verwechseln:</strong> {eur(_a1[0])} Pendlerpauschale bedeuten nicht {eur(_a1[0])} mehr Netto, sondern {eur(_a1[0])} weniger Bemessungsgrundlage. Der Pendlereuro dagegen wird in voller Höhe von der Steuer abgezogen.</div>
<div class="warn"><strong>Österreich: großes Pauschale wegen des eigenen Autos annehmen:</strong> Entscheidend ist nicht, womit du fährst, sondern ob ein Massenverkehrsmittel zumutbar wäre.</div>
<h2>Grenzen des Rechners</h2>
<ul><li><strong>Zumutbarkeit und Entfernung in Österreich:</strong> Die Kriterien legt eine Verordnung des Finanzministers fest (§ 16 Abs. 1 Z 6 lit. j). Der Rechner fragt das Ergebnis ab, er ermittelt es nicht. Für die Erklärung gegenüber dem Arbeitgeber ist ein amtliches Formular vorgesehen (lit. g).</li>
<li><strong>Der Überschlag mit dem Grenzsteuersatz</strong> ist eine Näherung: Er unterstellt, dass der ganze Freibetrag in einer Tarifstufe liegt, und berücksichtigt weder Sozialversicherung noch andere Absetzbeträge. In Deutschland bleiben Solidaritätszuschlag und Kirchensteuer außen vor.</li>
<li><strong>Nicht abgebildet:</strong> mehrere Wohnsitze, Werkverkehr, Familienheimfahrten, Jobticket und steuerfreie Arbeitgeberleistungen, die den Abzug mindern, sowie Monate mit wechselnden Verhältnissen.</li>
<li><strong>Keine Steuerberatung.</strong> Verbindlich sind der Gesetzestext und der Bescheid des Finanzamts.</li></ul>
<h2>Häufige Fragen</h2>
<h3>Bekomme ich das Pendlerpauschale auch im Homeoffice-Monat?</h3>
<p>Es kommt auf die Zahl der Fahrten im Kalendermonat an: unter vier Fahrten steht nach lit. e kein Pauschale zu, bei vier bis sieben ein Drittel, bei acht bis zehn zwei Drittel.</p>
<h3>Warum rechnet der Rechner für Österreich nur mit ganzen Kilometern?</h3>
<p>Die Stufen im Gesetz sind in ganzen Kilometern gefasst, und der Pendlereuro wird je Kilometer gewährt. Wie angebrochene Kilometer zu runden sind, regelt die Verordnung; diese Regel haben wir nicht nachgeprüft und bilden sie deshalb nicht nach.</p>
<h3>Zählen in Deutschland auch Tage mit Bahn oder Fahrrad?</h3>
<p>Ja. Die Entfernungspauschale hängt nicht vom Verkehrsmittel ab; ausgenommen sind Flugstrecken und Strecken mit steuerfreier Sammelbeförderung. Ohne eigenen oder überlassenen Kraftwagen gilt aber der Höchstbetrag von {eur(R.ENTF_DE_MAX)} im Jahr.</p>
""",
"related": [],
}


# ---------- Rechner 2: Verzugszinsen
def _basis(tab, iso):
    return [v for d, v in tab if d <= iso][-1]


def _vz(land, B, von, bis):
    """Gleiche Rechnung wie C.verzug in calc.js (taggenau je Halbjahr, Tage ÷ Tage des Kalenderjahres)."""
    from datetime import date, timedelta
    a, e, s = date.fromisoformat(von), date.fromisoformat(bis), 0.0
    while a <= e:
        ende = min(e, date(a.year, 12, 31) if a.month >= 7 else date(a.year, 6, 30))
        n = (ende - a).days + 1
        jahr = 366 if (a.year % 4 == 0 and (a.year % 100 != 0 or a.year % 400 == 0)) else 365
        tab = {"de_v": R.BASIS_DE, "de_u": R.BASIS_DE, "at_u": R.BASIS_AT}.get(land)
        satz = R.VERZUG[land] + (_basis(tab, a.isoformat()) if tab else 0)
        s += B * satz / 100 * n / jahr
        a = ende + timedelta(days=1)
    return s


_bd, _ba = R.BASIS_DE[-1][1], R.BASIS_AT[-1][1]
_v1 = _vz("de_v", 1200, "2026-03-01", "2026-10-31")
_v2 = _vz("at_u", 5000, "2026-01-15", "2026-10-31")
_v3 = _vz("at_v", 5000, "2026-01-15", "2026-10-31")


def _basis_tab():
    rows = "".join(f"<tr><td>{d[8:10].lstrip('0')}.{d[5:7].lstrip('0')}.{d[:4]}</td><td>{de(v, 2)} %</td><td>{de(v + 5, 2)} %</td><td>{de(v + 9, 2)} %</td><td>{de(a, 2)} %</td><td>{de(a + 9.2, 2)} %</td></tr>"
                   for (d, v), (_, a) in zip(reversed(R.BASIS_DE), reversed(R.BASIS_AT)))
    return (f'<div class="scroll"><table class="tbl small"><thead><tr><th>Halbjahr ab</th><th>Basiszins DE</th><th>DE Verbraucher</th><th>DE Unternehmer</th><th>Basiszins AT</th><th>AT Unternehmer</th></tr></thead><tbody>{rows}</tbody></table></div>')


VERZUG = {
"slug": "verzugszinsen-rechner", "short": "Verzugszinsen", "sym": "§",
"teaser": "Gesetzliche Verzugszinsen taggenau – mit den Basiszinssätzen von Bundesbank und OeNB je Halbjahr.",
"title": "Verzugszinsen-Rechner für Deutschland und Österreich",
"h1": "Verzugszinsen-Rechner",
"lead": "Wie viel Zinsen fallen auf eine überfällige Rechnung an? Der Rechner setzt für jedes Halbjahr den Basiszinssatz ein, der dann galt, und zeigt jede Teilrechnung.",
"description": "Gesetzliche Verzugszinsen berechnen: § 288 BGB, § 456 UGB und § 1000 ABGB, taggenau mit den Basiszinssätzen seit 2020 – Rechenweg, Tabelle je Halbjahr, Quellen mit Abrufdatum.",
"formula": "Zinsen = Betrag × Zinssatz × Tage ÷ Tage im Jahr",
"form": form("verzug",
    select("land", "Rechtsgrundlage", [("de_v", "Deutschland – Verbraucher beteiligt (Basiszins + 5)"), ("de_u", "Deutschland – nur Unternehmer, Entgeltforderung (Basiszins + 9)"),
                                        ("at_u", "Österreich – zwischen Unternehmern (Basiszins + 9,2)"), ("at_v", "Österreich – sonst (4 % fest)")], "de_v").replace('class="f"', 'class="f wide"', 1)
    + inp("betrag", "Offener Betrag (€)", "1200")
    + '<label class="f"><span data-l="von">Erster Zinstag</span><input type="date" name="von" value="2026-03-01" min="2020-01-01" max="2026-12-31"></label>'
    + '<label class="f"><span data-l="bis">Letzter Zinstag</span><input type="date" name="bis" value="2026-10-31" min="2020-01-01" max="2026-12-31"></label>'),
"body": f"""
<h2>Welcher Zinssatz gilt für wen?</h2>
<div class="scroll"><table class="tbl text"><thead><tr><th>Fall</th><th>Gesetzlicher Zinssatz</th><th>Im 2. Halbjahr 2026</th><th>Fundstelle</th></tr></thead><tbody>
<tr><td>Deutschland, ein Verbraucher ist beteiligt</td><td>Basiszinssatz + 5 Prozentpunkte</td><td>{de(_bd + 5, 2)} %</td><td>§ 288 Abs. 1 BGB</td></tr>
<tr><td>Deutschland, kein Verbraucher beteiligt, Entgeltforderung</td><td>Basiszinssatz + 9 Prozentpunkte</td><td>{de(_bd + 9, 2)} %</td><td>§ 288 Abs. 2 BGB</td></tr>
<tr><td>Österreich, Geldforderungen zwischen Unternehmern</td><td>Basiszinssatz + 9,2 Prozentpunkte</td><td>{de(_ba + 9.2, 2)} %</td><td>§ 456 UGB</td></tr>
<tr><td>Österreich, sonst</td><td>4 % pro Jahr</td><td>4,00 %</td><td>§ 1333 Abs. 1 in Verbindung mit § 1000 Abs. 1 ABGB</td></tr>
</tbody></table></div>
<p>Die Zuordnung in der Tabelle folgt dem Wortlaut der Vorschriften; ob dein Fall darunter fällt und ab welchem Tag Verzug besteht, beantwortet der Rechner nicht. Aus einem anderen Rechtsgrund – etwa einer vertraglichen Vereinbarung – kann der Gläubiger höhere Zinsen verlangen (§ 288 Abs. 3 BGB). Alle Fundstellen mit Link und Abrufdatum: <a href="{REF}?q=verzug">Sätze und Grenzwerte</a>.</p>
<h2>Die Basiszinssätze je Halbjahr</h2>
<p>Der deutsche Basiszinssatz ändert sich zum 1. Jänner und 1. Juli (§ 247 BGB); die Deutsche Bundesbank gibt ihn bekannt. In Österreich veröffentlicht die Oesterreichische Nationalbank den Basiszinssatz; er ändert sich mit den Zinsbeschlüssen, für § 456 UGB zählt aber der Wert am ersten Kalendertag des Halbjahres. Die Spalte „Basiszins AT“ zeigt deshalb diesen Stichtagswert.</p>
{_basis_tab()}
<p class="small muted">Quellen: Deutsche Bundesbank, „Basiszinssatz nach § 247 BGB“; Oesterreichische Nationalbank, „Basis- und Referenzzinssätze“ (Tabelle zuletzt geändert am 5.10.2026). Beide abgerufen am {R.ABRUF}. Der österreichische Basiszinssatz steht seit 16.9.2026 bei {de(R.BASIS_AT_AENDERUNGEN[-1][1], 2)} %; für das laufende Halbjahr bleibt nach § 456 UGB der Wert vom 1.7.2026 maßgeblich.</p>
<h2>So rechnet der Rechner</h2>
<ol><li>Der Zeitraum wird an jedem 1. Jänner und 1. Juli geteilt.</li>
<li>Für jedes Teilstück gilt der Basiszinssatz des Halbjahres plus Aufschlag – oder in Österreich außerhalb von Unternehmergeschäften fest 4 %.</li>
<li>Zinsen des Teilstücks = Betrag × Zinssatz × Zinstage ÷ Tage des Kalenderjahres (365, im Schaltjahr 366). Erster und letzter Zinstag zählen mit.</li>
<li>Die Teilbeträge werden ungerundet addiert; gerundet wird die Summe.</li></ol>
<div class="example"><strong>Durchgerechnet (konstruiertes Beispiel):</strong> 1.200 € sind in Deutschland gegenüber einem Verbraucher vom 1. März bis 31. Oktober 2026 offen. Bis 30. Juni gilt {de(R.BASIS_DE[-2][1] + 5, 2)} % (122 Tage), ab 1. Juli {de(_bd + 5, 2)} % (123 Tage). Zusammen ergibt das {eur(_v1)}.</div>
<div class="example"><strong>Österreich, 5.000 € vom 15. Jänner bis 31. Oktober 2026:</strong> zwischen Unternehmern {eur(_v2)}, mit den gesetzlichen 4 % dagegen {eur(_v3)}. Der Unterschied kommt allein aus dem Zinssatz – {de(_ba + 9.2, 2)} % gegenüber 4 %.</div>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Mit einem einzigen Zinssatz über mehrere Halbjahre rechnen:</strong> Ändert sich der Basiszinssatz, ändert sich der Verzugszins mit. Von Anfang 2024 bis Mitte 2025 ist der deutsche Basiszinssatz von {de(dict(R.BASIS_DE)["2024-01-01"], 2)} % auf {de(dict(R.BASIS_DE)["2025-07-01"], 2)} % gefallen.</div>
<div class="warn"><strong>„9 Prozent“ statt „9 Prozentpunkte über dem Basiszinssatz“:</strong> Der Aufschlag kommt zum Basiszinssatz dazu. Bei negativem Basiszinssatz lag der Verzugszins unter dem Aufschlag – 2020 bis Mitte 2022 in Deutschland bei {de(dict(R.BASIS_DE)["2020-01-01"] + 9, 2)} % statt 9 %. <a href="/prozent-oder-prozentpunkte.html">Prozent oder Prozentpunkte?</a></div>
<div class="warn"><strong>Zinsen auf Zinsen rechnen:</strong> Der Rechner rechnet einfache Zinsen auf den offenen Betrag.</div>
<h2>Grenzen des Rechners</h2>
<ul><li><strong>Zeitraum:</strong> 1. Jänner 2020 bis 31. Dezember 2026. Der Basiszinssatz für 2027 steht noch nicht fest; ältere Halbjahre haben wir nicht aufgenommen.</li>
<li><strong>Zählweise:</strong> Das Gesetz nennt einen Jahreszinssatz, aber keine Formel für Teilzeiträume. Der Rechner zählt Kalendertage und teilt durch die Tage des jeweiligen Kalenderjahres. Andere Rechner, die immer durch 365 oder mit 30-Tage-Monaten rechnen, kommen auf leicht andere Beträge.</li>
<li><strong>Nicht enthalten:</strong> die Pauschale von 40 € bei Unternehmergeschäften (§ 288 Abs. 5 BGB, § 458 UGB), Mahn- und Inkassokosten, Teilzahlungen während des Verzugs, vertragliche Zinssätze und Zinseszinsen.</li>
<li><strong>Keine Rechtsberatung.</strong> Wann Verzug eintritt und ob ein Verbraucher- oder Unternehmergeschäft vorliegt, ist eine Rechtsfrage.</li></ul>
<h2>Häufige Fragen</h2>
<h3>Warum zeigt der Rechner für Österreich einen anderen Basiszinssatz als die OeNB heute?</h3>
<p>Weil § 456 UGB auf den ersten Kalendertag des Halbjahres abstellt. Eine Änderung mitten im Halbjahr – wie am 16. September 2026 – wirkt für Verzugszinsen erst ab dem nächsten 1. Jänner oder 1. Juli.</p>
<h3>Kann ich Teilzahlungen berücksichtigen?</h3>
<p>Nicht in einer Rechnung. Rechne jeden Abschnitt mit dem jeweils offenen Betrag getrennt und addiere die Ergebnisse; „Als Szenario A merken“ hält den ersten Abschnitt zum Vergleich fest.</p>
""",
"related": ["skonto-oder-ratenzahlung"],
}

NEU = [PENDLER, VERZUG]

# ---------- Zusammengelegte Seiten: alte Adresse → (neue Adresse, Titel der Zielseite, übernommene Abschnitte)
MERGE = {
    "rabatte-kombinieren": ("rabatt-rechner", ["Die schnelle Rechnung", "Aktionen in Prozent umrechnen", "Rabatt und Mehrwertsteuer", "Rückwärts: Was kostete der Artikel ursprünglich?"]),
    "mehrwertsteuer-herausrechnen": ("mehrwertsteuer-rechner", ["Die Teiler im Überblick", "Schnelle Tabelle: Wie viel Steuer steckt im Betrag?", "Rundung: pro Position oder auf die Summe?", "Kleinbetragsrechnungen in Deutschland"]),
    "zinseszins-und-72er-regel": ("zinseszins-rechner", ["Wie genau ist die Regel?", "Warum gerade 72?", "Verwandte Faustregeln", "Zinseszins in Zahlen"]),
    "sollzins-und-effektivzins": ("kreditvergleich", ["Was im Effektivzins steckt", "Gebunden oder variabel?", "Durchgerechnet: Warum der Effektivzins höher ist", "Was in Deutschland einbezogen wird – und was nicht", "Typische Fehler", "Grenzen des Effektivzinses"]),
}


def abschnitte(body, titel):
    """Schneidet die genannten <h2>-Abschnitte aus einem Ratgebertext, in der dort stehenden Reihenfolge."""
    import re
    teile = re.split(r"(?=<h2[ >])", body)
    out, gefunden = [], set()
    for t in teile:
        m = re.match(r"<h2[^>]*>(.*?)</h2>", t, re.S)
        if m and m.group(1).strip() in titel:
            out.append(t.strip()); gefunden.add(m.group(1).strip())
    fehlt = set(titel) - gefunden
    assert not fehlt, f"Abschnitt nicht gefunden: {fehlt}"
    return "\n".join(out)
