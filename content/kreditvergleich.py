"""Kreditvergleich: zwei Angebote nebeneinander – Rate, Gesamtkosten, Effektivzins (näherungsweise). Beispiele in Python berechnet."""
from content.calcs import form, inp, de, eur


def angebot(K, years, p, fee, monthly):
    """Annuitätenkredit: Rate, Gesamtkosten, effektiver Jahreszins (Monatszins per Bisektion, (1+r)^12 − 1)."""
    m = round(years * 12); i = p / 100 / 12
    a = K / m if i == 0 else K * i / (1 - (1 + i) ** -m)
    total = a * m + fee + monthly * m
    lo, hi = 0.0, 0.1
    for _ in range(200):
        r = (lo + hi) / 2
        pv = sum((a + monthly) / (1 + r) ** k for k in range(1, m + 1))
        if pv > K - fee: lo = r
        else: hi = r
    return a, total, ((1 + r) ** 12 - 1) * 100


_K, _Y = 20000, 5
_A = angebot(_K, _Y, 4.5, 0, 0)
_B = angebot(_K, _Y, 3.9, 400, 3)

KREDITVERGLEICH = {
"slug": "kreditvergleich", "short": "Kreditvergleich", "sym": "A|B",
"teaser": "Zwei Kreditangebote nebeneinander: Rate, Gesamtkosten und Effektivzins.",
"title": "Kreditvergleich: zwei Angebote mit Gebühren vergleichen",
"h1": "Kreditvergleich",
"lead": "Der niedrigere Sollzins ist nicht automatisch das bessere Angebot. Trag zwei Angebote mit Bearbeitungsgebühr und Kontoführung ein – der Rechner zeigt Rate, Gesamtkosten und Effektivzins nebeneinander.",
"description": "Kredite vergleichen: zwei Angebote mit Sollzins, Bearbeitungsgebühr und Kontoführung – Monatsrate, Gesamtkosten und effektiver Jahreszins mit Rechenweg.",
"formula": "Gesamtkosten = Rate × Monate + Gebühren",
"form": form("kreditvergleich",
    inp("amount", "Kreditbetrag (€)", "20000") + inp("years", "Laufzeit (Jahre)", "5")
    + '<fieldset class="offer"><legend>Angebot A</legend>' + inp("a_rate", "Sollzins p. a. (%)", "4.5") + inp("a_fee", "Bearbeitungsgebühr (€)", "0") + inp("a_monthly", "Kontoführung (€ pro Monat)", "0") + "</fieldset>"
    + '<fieldset class="offer"><legend>Angebot B</legend>' + inp("b_rate", "Sollzins p. a. (%)", "3.9") + inp("b_fee", "Bearbeitungsgebühr (€)", "400") + inp("b_monthly", "Kontoführung (€ pro Monat)", "3") + "</fieldset>"),
"body": f"""
<h2>Warum der Sollzins allein täuscht</h2>
<p>Der Sollzins bestimmt nur, wie viel Zinsen auf die Restschuld anfallen. Bearbeitungsgebühren, Kontoführungsentgelte oder Pflicht-Pakete kommen obendrauf. Ein Angebot mit niedrigerem Sollzins kann deshalb unterm Strich teurer sein – genau das zeigt der Vergleich.</p>
<div class="example"><strong>Beispiel:</strong> {eur(_K)} auf {_Y} Jahre. Angebot A: 4,5 % Sollzins, keine Gebühren – Rate {eur(_A[0])}, Gesamtkosten {eur(_A[1])}, Effektivzins rund {de(_A[2], 2)} %. Angebot B: 3,9 % Sollzins, aber 400 € Bearbeitungsgebühr und 3 € Kontoführung im Monat – Rate {eur(_B[0])}, Gesamtkosten {eur(_B[1])}, Effektivzins rund {de(_B[2], 2)} %. Trotz niedrigerem Sollzins ist B um {eur(_B[1] - _A[1])} teurer.</div>
<h2>So rechnet der Vergleich</h2>
<ol>
<li><strong>Rate:</strong> wie im <a href="/kreditrechner.html">Kreditrechner</a> nach der Annuitätenformel Rate = K × i ÷ (1 − (1 + i)<sup>−n</sup>) mit dem Monatszins i = Sollzins ÷ 12.</li>
<li><strong>Gesamtkosten:</strong> alle Raten plus Bearbeitungsgebühr plus Kontoführung über die ganze Laufzeit.</li>
<li><strong>Effektivzins:</strong> Der Rechner sucht den Monatszins, bei dem alle Zahlungen (Rate und Kontoführung) abgezinst genau dem Betrag entsprechen, der dir nach Abzug der Bearbeitungsgebühr tatsächlich bleibt. Daraus wird der Jahreswert (1 + Monatszins)<sup>12</sup> − 1.</li>
</ol>
<h2>Grenzen des Vergleichs</h2>
<p>Der hier berechnete Effektivzins ist eine Näherung für einfache Ratenkredite mit gleichbleibender Rate. Der Wert im Angebot der Bank folgt den gesetzlichen Vorgaben (in Österreich Verbraucherkreditgesetz, in Deutschland Preisangabenverordnung) und kann wegen Auszahlungs- und Ratenterminen leicht abweichen. Kosten einer Restschuldversicherung, Sondertilgungen oder variable Zinsen berücksichtigt der Rechner nicht. Für die Entscheidung zählt das verbindliche Angebot mit dem effektiven Jahreszins aus dem Europäischen Standardinformationsblatt (ESIS bzw. SECCI).</p>
<div class="warn"><strong>Typischer Fehler:</strong> nur die Monatsrate vergleichen. Eine längere Laufzeit senkt die Rate, macht den Kredit aber fast immer teurer. Vergleiche deshalb bei gleicher Laufzeit – und schau auf die Gesamtkosten.</div>
""",
"related": ["sollzins-und-effektivzins", "kredit-sondertilgung"],
}
