"""Ratgeber November 2026. Alle Beispielzahlen werden hier in Python berechnet.
Annahmen (Preise, Sätze) sind im Text als Annahme gekennzeichnet; amtliche Werte tragen Quelle und Stand."""
import math
from content.calcs import de, eur
from content.deepen import faq, _apr, VPI_AT, VPI_DE, SRC_STAT_AT, SRC_DESTATIS

STAND = "Stand: November 2026"
GII = "https://www.gesetze-im-internet.de"
RIS = '<a href="https://www.ris.bka.gv.at" rel="noopener">RIS</a>'


def gii(path, text):
    return f'<a href="{GII}/{path}" rel="noopener">{text}</a>'


def pct(x, d=1):
    return f"{de(x, d)} %".replace("-", "−")


def annuity(K, p, months):
    i = p / 100 / 12
    return K * i / (1 - (1 + i) ** -months) if i else K / months


def run_loan(K, p, rate, extra=None, max_m=1200):
    """Tilgt mit fester Rate; extra = {Monat: Betrag} Sondertilgung nach der Rate dieses Monats.
    Liefert (Monate, Zinsen gesamt, tatsächlich geleistete Sondertilgungen)."""
    i, b, m, interest, paid_extra = p / 100 / 12, K, 0, 0.0, 0.0
    extra = extra or {}
    while b > 0.005 and m < max_m:
        m += 1
        z = b * i; interest += z
        b -= min(rate, b + z) - z
        if m in extra and b > 0.005:
            x = min(extra[m], b); b -= x; paid_extra += x
    return m, interest, paid_extra


def balance_after(K, p, rate, months):
    i, b = p / 100 / 12, K
    for _ in range(months):
        b -= rate - b * i
    return b


# =====================================================================
# 1  Wärmepumpe
_gas, _eta = 18000, 0.90
_heat = _gas * _eta
_oil_l = 2000
_heat_oil = _oil_l * 10 * 0.85
_jaz = 3.3
_wp_kwh = _heat / _jaz
_p_std, _p_wp = 0.28, 0.22
_gas_price = 0.10
_ww_day = 40 * 4.186 * 35 / 3600          # kWh Wärme pro Person und Tag: 40 l, von 10 auf 45 °C
_ww_year = _ww_day * 365
_hwb_area, _hwb = 140, 60
_nb_heat = _hwb_area * _hwb
_heizstab = 300 * 1.0                      # Annahme: 300 kWh Heizstab bei Frost

WP = {
"slug": "waermepumpe-stromkosten",
"title": "Stromkosten einer Wärmepumpe abschätzen: Rechenweg mit Jahresarbeitszahl",
"teaser": "Wärmebedarf ÷ Jahresarbeitszahl = Stromverbrauch. So rechnest du es für dein Haus durch.",
"description": "Stromverbrauch und Stromkosten einer Wärmepumpe selbst abschätzen: Wärmebedarf aus der alten Gas- oder Ölrechnung, Jahresarbeitszahl, Warmwasser und Tarif – mit Rechenbeispielen für Österreich und Deutschland.",
"related": ["stromtarife-vergleichen", "realzins-sparen-inflation", "kredit-sondertilgung"],
"body": f"""
<p>Wie viel Strom eine Wärmepumpe braucht, lässt sich mit einer einzigen Division abschätzen: <strong>Stromverbrauch = Wärmebedarf ÷ Jahresarbeitszahl</strong>. Die eigentliche Arbeit liegt darin, die beiden Werte realistisch zu bestimmen. Dieser Ratgeber zeigt den Weg Schritt für Schritt – mit den Zahlen aus deiner bisherigen Heizungsrechnung, mit Messwerten aus einem großen Feldtest und mit dem Warmwasser, das oft vergessen wird. Eine Heizlastberechnung durch einen Fachbetrieb ersetzt die Abschätzung nicht; sie hilft aber, Angebote und Werbeversprechen einzuordnen.</p>

<h2>Schritt 1: Den Wärmebedarf aus der alten Rechnung ableiten</h2>
<p>Der beste Ausgangspunkt ist dein tatsächlicher Verbrauch der letzten Jahre. Eine Gas- oder Ölheizung wandelt den Brennstoff nicht vollständig in nutzbare Wärme um; ein Teil geht über Abgas und Kessel verloren. Deshalb wird der Brennstoffverbrauch mit dem <strong>Nutzungsgrad</strong> multipliziert. Für einen gut eingestellten Brennwertkessel ist 0,9 eine vorsichtige Annahme, für ältere Kessel eher 0,8 bis 0,85.</p>
<div class="example"><strong>Gasheizung:</strong> Laut Jahresabrechnung wurden {de(_gas,0)} kWh Gas verbraucht (Gasrechnungen weisen den Verbrauch in Österreich und Deutschland in kWh aus). Nutzwärme: {de(_gas,0)} × {de(_eta,2)} = <strong>{de(_heat,0)} kWh</strong>.</div>
<div class="example"><strong>Ölheizung:</strong> Ein Liter Heizöl enthält rund 10 kWh Energie. {de(_oil_l,0)} Liter im Jahr bei einem Nutzungsgrad von 0,85 ergeben {de(_oil_l,0)} × 10 × 0,85 = <strong>{de(_heat_oil,0)} kWh</strong> Nutzwärme.</div>
<p>Nimm wenn möglich den Durchschnitt aus zwei oder drei Jahren, denn ein milder Winter drückt den Verbrauch. Hat der alte Kessel auch das Warmwasser bereitet, steckt es in dieser Zahl schon drin.</p>
<p><strong>Neubau oder unbekannter Verbrauch:</strong> Dann hilft der Energieausweis. In Österreich nennt er den Heizwärmebedarf (HWB) in kWh pro Quadratmeter und Jahr. Ein Haus mit {_hwb_area} m² und einem HWB von {_hwb} kWh/m² braucht rund {_hwb_area} × {_hwb} = {de(_nb_heat,0)} kWh Heizwärme, zuzüglich Warmwasser. Der deutsche Energieausweis nennt meist den Endenergiebedarf oder -verbrauch; für eine grobe Schätzung lässt er sich ähnlich verwenden. Beide Werte beruhen auf Normbedingungen und können vom echten Verbrauch deutlich abweichen.</p>

<h2>Schritt 2: Die Jahresarbeitszahl realistisch wählen</h2>
<p>Die <strong>Jahresarbeitszahl (JAZ)</strong> sagt, wie viele Kilowattstunden Wärme die Wärmepumpe im Jahresmittel aus einer Kilowattstunde Strom macht. Sie ist nicht dasselbe wie der COP aus dem Datenblatt: Der COP gilt für einen einzelnen Prüfpunkt, etwa 7 °C Außenluft und 35 °C Vorlauf. Die JAZ enthält dagegen kalte Tage, Abtauen, Warmwasser und den Heizstab – sie ist deshalb fast immer niedriger.</p>
<p>Belastbare Werte liefern Feldmessungen. Das Fraunhofer-Institut für Solare Energiesysteme hat Wärmepumpen in bestehenden Wohngebäuden über mehrere Jahre vermessen. In der Zwischenauswertung 2024 erreichten 22 ausgewertete Luft-Wasser-Wärmepumpen eine mittlere JAZ von 3,3, die Spanne reichte von 2,4 bis 4,0. Erdreich-Wärmepumpen schneiden in solchen Messungen besser ab, weil das Erdreich im Winter wärmer ist als die Außenluft. Quelle: <a href="https://www.ise.fraunhofer.de/de/presse-und-medien/news/2024/waermepumpenfeldstest-zwischenergebnisse-bestaetigen-effizienten-betrieb-auch-im-altbau.html" rel="noopener">Fraunhofer ISE, Zwischenergebnisse Wärmepumpen-Feldtest</a> ({STAND}).</p>
<p>Für eine erste Rechnung im Altbau mit Luft-Wasser-Wärmepumpe ist eine JAZ von 3 bis 3,5 eine vernünftige Annahme. Wer niedrige Vorlauftemperaturen erreicht – Fußbodenheizung oder große Heizkörper –, darf mit dem oberen Ende rechnen; bei kleinen Heizkörpern und hohen Vorlauftemperaturen eher mit dem unteren.</p>

<h2>Schritt 3: Strombedarf und Kosten ausrechnen</h2>
<div class="example"><strong>Das Gas-Beispiel weitergerechnet:</strong> {de(_heat,0)} kWh Wärme ÷ JAZ {de(_jaz,1)} = <strong>{de(_wp_kwh,0)} kWh Strom</strong> im Jahr. Bei einem angenommenen Arbeitspreis von {de(_p_std*100,0)} Cent pro kWh kostet das {eur(_wp_kwh*_p_std)}; mit einem angenommenen Wärmepumpentarif von {de(_p_wp*100,0)} Cent sind es {eur(_wp_kwh*_p_wp)}.</div>
<p>Wie empfindlich das Ergebnis auf beide Annahmen reagiert, zeigt die Tabelle für denselben Wärmebedarf von {de(_heat,0)} kWh:</p>
<table class="tbl"><thead><tr><th>JAZ</th><th>Strom (kWh)</th><th>bei 22 ct</th><th>bei 28 ct</th><th>bei 34 ct</th></tr></thead><tbody>
{''.join(f'<tr><td>{de(j,1)}</td><td>{de(_heat/j,0)}</td>' + ''.join(f'<td>{eur(_heat/j*p)}</td>' for p in (0.22, 0.28, 0.34)) + '</tr>' for j in (2.5, 3.0, 3.5, 4.0, 4.5))}
</tbody></table>
<p>Zwischen der ungünstigsten Kombination (JAZ 2,5 bei 34 ct) und der günstigsten (JAZ 4,5 bei 22 ct) liegt fast das Dreifache. Deshalb ist eine einzelne Zahl ohne Annahmen wenig wert – lass dir bei Angeboten zeigen, mit welcher JAZ und welchem Wärmebedarf gerechnet wurde.</p>

<h2>Warmwasser nicht vergessen</h2>
<p>Hat bisher ein Durchlauferhitzer oder Elektroboiler das Warmwasser bereitet, ist es in der Gasrechnung nicht enthalten und kommt dazu. Die Größenordnung lässt sich physikalisch abschätzen: Um 40 Liter Wasser von 10 °C auf 45 °C zu erwärmen, braucht es 40 × 4,186 kJ × 35 ÷ 3.600 = {de(_ww_day,2)} kWh. Pro Person und Jahr sind das rund {de(_ww_year,0)} kWh Nutzwärme, für vier Personen {de(_ww_year*4,0)} kWh – ohne Verluste von Speicher und Leitungen, die in der Praxis spürbar dazukommen. Weil Warmwasser höhere Temperaturen braucht als die Heizung, arbeitet die Wärmepumpe dabei mit einer niedrigeren Arbeitszahl.</p>

<h2>Vergleich mit den bisherigen Heizkosten</h2>
<div class="example">Bei einem angenommenen Gaspreis von {de(_gas_price*100,0)} Cent pro kWh kosteten {de(_gas,0)} kWh Gas {eur(_gas*_gas_price)} im Jahr, ohne Grundgebühr. Die Wärmepumpe läge im Beispiel bei {eur(_wp_kwh*_p_std)} (Haushaltstarif) bzw. {eur(_wp_kwh*_p_wp)} (Wärmepumpentarif). Der Vorteil hängt also stark vom Verhältnis zwischen Strom- und Gaspreis ab: Kostet eine Kilowattstunde Wärme aus der Wärmepumpe (Strompreis ÷ JAZ) mehr als eine aus dem Gaskessel (Gaspreis ÷ Nutzungsgrad), wird die Wärmepumpe im Betrieb teurer.</div>
<p>Die Faustregel daraus: Teile deinen Strompreis durch die erwartete JAZ und vergleiche das Ergebnis mit dem Gaspreis geteilt durch den Nutzungsgrad. 28 ÷ 3,3 = {de(28/3.3,1)} Cent pro kWh Wärme gegen 10 ÷ 0,9 = {de(10/0.9,1)} Cent. Investitionskosten, Förderungen, Wartung und Grundgebühren sind darin nicht enthalten.</p>

<h2>Österreich und Deutschland: Tarife und Information</h2>
<p>In beiden Ländern bieten viele Energieversorger eigene Wärmepumpentarife an, oft mit getrenntem Zähler. In Deutschland können steuerbare Verbrauchseinrichtungen wie Wärmepumpen seit 2024 reduzierte Netzentgelte erhalten, wenn der Netzbetreiber ihre Leistung in Ausnahmefällen begrenzen darf (§ 14a Energiewirtschaftsgesetz); Details erklärt die <a href="https://www.bundesnetzagentur.de" rel="noopener">Bundesnetzagentur</a>. In Österreich vergleicht der amtliche Tarifkalkulator der <a href="https://www.e-control.at" rel="noopener">E-Control</a> Strom- und Gastarife, und die Klimaschutzinitiative <a href="https://www.klimaaktiv.at" rel="noopener">klimaaktiv</a> informiert über Heizungstausch und Wärmepumpen ({STAND}). Förderungen ändern sich häufig; maßgeblich sind die Bedingungen zum Zeitpunkt des Antrags.</p>

<h2>Typische Fehler</h2>
<div class="warn"><strong>Heizlast mit Wärmebedarf verwechseln:</strong> Die Heizlast in Kilowatt (kW) bestimmt, wie groß die Wärmepumpe sein muss. Der Wärmebedarf in Kilowattstunden (kWh) bestimmt die Stromrechnung. Eine 8-kW-Wärmepumpe verbraucht nicht 8 kWh pro Stunde Strom.</div>
<div class="warn"><strong>COP statt JAZ einsetzen:</strong> Mit dem Datenblatt-COP von zum Beispiel 4,5 statt einer realistischen JAZ von 3,3 sinkt der berechnete Strombedarf von {de(_heat/3.3,0)} auf {de(_heat/4.5,0)} kWh – um mehr als ein Viertel zu optimistisch.</div>
<div class="warn"><strong>Heizstab ignorieren:</strong> An sehr kalten Tagen oder bei zu klein ausgelegten Anlagen springt ein elektrischer Heizstab ein. Er macht aus 1 kWh Strom nur 1 kWh Wärme. Schon {de(_heizstab,0)} kWh Heizstab-Strom kosten bei 28 Cent {eur(_heizstab*0.28)} zusätzlich.</div>

<h2>Grenzen dieser Abschätzung</h2>
<p>Die Rechnung liefert eine Größenordnung für das Jahr, keine Garantie. Wetter, Nutzerverhalten, hydraulischer Abgleich, Einstellung der Heizkurve und Warmwasserbedarf verändern das Ergebnis. Für einzelne Geräte mit fester Leistung eignet sich der <a href="/stromkosten-rechner.html">Stromkosten-Rechner</a>; für die Wärmepumpe trägst du dort im Modus „Jahresverbrauch“ das Ergebnis aus Schritt 3 ein und erhältst die Kosten pro Monat und Tag. Welcher Stromtarif bei diesem Verbrauch günstiger ist, zeigt der Ratgeber <a href="/stromtarife-vergleichen.html">Stromtarife vergleichen</a>.</p>
{faq([
("Wie viel Strom braucht eine Wärmepumpe pro Quadratmeter?", "Das hängt fast nur vom Wärmebedarf des Hauses ab. Ein gut gedämmter Neubau braucht pro Quadratmeter einen Bruchteil dessen, was ein unsanierter Altbau braucht – Durchschnittswerte pro m² sind deshalb wenig aussagekräftig."),
("Ist eine JAZ von 3 gut?", "Für eine Luft-Wasser-Wärmepumpe im Altbau ist das ein üblicher Wert. Höhere Werte erreichen vor allem Anlagen mit niedriger Vorlauftemperatur und Erdreich-Wärmepumpen."),
("Lohnt sich ein eigener Wärmepumpentarif?", "Rechne Grundgebühr, Zählerkosten und Arbeitspreis beider Varianten für deinen Verbrauch durch. Ein niedrigerer Arbeitspreis kann durch eine zweite Grundgebühr teilweise aufgezehrt werden."),
("Kann ich mit einer Photovoltaikanlage rechnen?", "Teilweise. Den größten Wärmebedarf gibt es im Winter, wenn die Anlage am wenigsten Strom liefert. Für die Abschätzung ist es vorsichtiger, nur einen kleinen Teil des Wärmepumpenstroms als Eigenverbrauch anzusetzen."),
])}
""",
}

# =====================================================================
# 2  Kredit mit Sondertilgung
_K, _p, _n = 20000, 4.5, 60
_r = annuity(_K, _p, _n)
_base_int = _r * _n - _K
_b12 = balance_after(_K, _p, _r, 12)
_int12 = 12 * _r - (_K - _b12)
_mA, _intA, _ = run_loan(_b12 - 2000, _p, _r)
_m36, _int36, _ = run_loan(_K, _p, _r, extra={36: 2000})
_m1, _int1, _ = run_loan(_K, _p, _r, extra={1: 2000})
_rB = annuity(_b12 - 2000, _p, 48)
_intB = _int12 + _rB * 48 - (_b12 - 2000)
_vfe = 2000 * 0.01
_HK, _hp = 200000, 3.5
_hr = annuity(_HK, _hp, 300)
_h_base = _hr * 300 - _HK
_h_m, _h_int, _h_extra_total = run_loan(_HK, _hp, _hr, extra={12 * k: 5000 for k in range(1, 26)})
_tg_net_at = 2.0 * 0.75

SONDER = {
"slug": "kredit-sondertilgung",
"title": "Kredit mit Sondertilgung: Wie viel Zinsen eine Extrazahlung spart",
"teaser": "Kürzere Laufzeit oder niedrigere Rate? Zwei Wege, durchgerechnet – mit den Regeln in AT und DE.",
"description": "Sondertilgung beim Ratenkredit und Wohnkredit: wie viel Zinsen eine Extrazahlung spart, ob die Rate oder die Laufzeit sinken soll, was eine Vorfälligkeitsentschädigung kostet – mit Rechenbeispielen und den Regeln in Österreich und Deutschland.",
"related": ["sollzins-und-effektivzins", "realzins-sparen-inflation", "skonto-oder-ratenzahlung"],
"body": f"""
<p>Eine Sondertilgung ist eine Zahlung zusätzlich zur vereinbarten Rate, die direkt die Restschuld senkt. Weil Zinsen immer auf die aktuelle Restschuld berechnet werden, spart jeder vorzeitig zurückgezahlte Euro die Zinsen für die gesamte restliche Laufzeit. Wie viel das ausmacht, hängt von drei Dingen ab: dem Zinssatz, dem Zeitpunkt der Extrazahlung und davon, ob danach die Laufzeit oder die Rate sinkt.</p>

<h2>Das Ausgangsbeispiel</h2>
<p>Ein Ratenkredit über {eur(_K)} mit {de(_p,1)} % Sollzins und 5 Jahren Laufzeit hat eine Monatsrate von {eur(_r)}. Ohne Sondertilgung fallen insgesamt {eur(_base_int)} Zinsen an. Nach zwölf Raten beträgt die Restschuld {eur(_b12)}; in diesem ersten Jahr wurden {eur(_int12)} Zinsen gezahlt. Jetzt kommen 2.000 € aus einer Prämie oder dem Urlaubsgeld als Sondertilgung dazu – die Restschuld sinkt auf {eur(_b12-2000)}.</p>

<h2>Weg A: Rate gleich lassen, Laufzeit verkürzen</h2>
<div class="example">Die Rate bleibt bei {eur(_r)}. Die Restschuld von {eur(_b12-2000)} ist dann nach weiteren <strong>{_mA} Monaten</strong> getilgt statt nach 48 – der Kredit läuft insgesamt {12+_mA} statt 60 Monate. Zinsen gesamt: {eur(_int12+_intA)}. Ersparnis gegenüber dem Ausgangskredit: <strong>{eur(_base_int-_int12-_intA)}</strong>.</div>

<h2>Weg B: Laufzeit gleich lassen, Rate senken</h2>
<div class="example">Die restlichen 48 Monate bleiben. Die neue Rate für {eur(_b12-2000)} beträgt {eur(_rB)}, also {eur(_r-_rB)} weniger im Monat. Zinsen gesamt: {eur(_intB)}. Ersparnis: <strong>{eur(_base_int-_intB)}</strong>.</div>
<p>Weg A spart mehr, weil die Restschuld danach schneller sinkt und damit auch in jedem folgenden Monat weniger Zinsen anfallen. Weg B verschafft dafür monatlich mehr Spielraum. Welche Variante gilt, legt der Vertrag oder die Bank fest – frag vor der Zahlung nach, und lass dir den neuen Tilgungsplan schriftlich geben.</p>

<h2>Je früher, desto mehr: der Zeitpunkt</h2>
<p>Dieselben 2.000 € sparen mehr Zinsen, je früher sie fließen, weil sie die Schuld über eine längere Restlaufzeit verkleinern. Bei gleichbleibender Rate (Weg A) ergibt sich:</p>
<table class="tbl"><thead><tr><th>Sondertilgung nach Rate</th><th>Laufzeit</th><th>Zinsersparnis</th></tr></thead><tbody>
<tr><td>1</td><td>{_m1} Monate</td><td>{eur(_base_int-_int1)}</td></tr>
<tr><td>12</td><td>{12+_mA} Monate</td><td>{eur(_base_int-_int12-_intA)}</td></tr>
<tr><td>36</td><td>{_m36} Monate</td><td>{eur(_base_int-_int36)}</td></tr></tbody></table>
<p>Die Ersparnis wächst mit der verbleibenden Laufzeit, ist aber auch nach drei Jahren noch spürbar.</p>

<h2>Wohnkredit: jährliche Sondertilgungen über viele Jahre</h2>
<div class="example">{eur(_HK)} zu {de(_hp,1)} % auf 25 Jahre ergeben eine Rate von {eur(_hr)} und {eur(_h_base)} Zinsen. Zahlt man zusätzlich jedes Jahr nach der zwölften Rate 5.000 € und lässt die Rate gleich, ist der Kredit nach <strong>{_h_m} Monaten</strong> ({de(_h_m/12,1)} Jahren) abbezahlt. Die Zinsen sinken auf {eur(_h_int)} – eine Ersparnis von {eur(_h_base-_h_int)} bei Sondertilgungen von zusammen {eur(_h_extra_total)}.</div>
<p>Bei Wohnkrediten mit fixem Zins ist das Recht auf Sondertilgung oft vertraglich begrenzt, zum Beispiel auf einen bestimmten Prozentsatz der Kreditsumme pro Jahr. Dieses Recht sollte vor Vertragsabschluss verhandelt werden – nachträglich ist es schwer zu bekommen.</p>

<h2>Österreich: vorzeitige Rückzahlung nach dem Verbraucherkreditgesetz</h2>
<p>Bei Verbraucherkrediten darfst du jederzeit ganz oder teilweise vorzeitig zurückzahlen (§ 16 Verbraucherkreditgesetz, {RIS}). Die Bank kann bei fixem Sollzins eine Entschädigung verlangen, die nach dem Gesetz höchstens 1 % des vorzeitig zurückgezahlten Betrags beträgt, bei einer Restlaufzeit von höchstens einem Jahr höchstens 0,5 %. Keine Entschädigung fällt an, wenn innerhalb von zwölf Monaten insgesamt höchstens 10.000 € vorzeitig zurückgezahlt werden. Für Wohnkredite, die durch eine Hypothek besichert sind, gilt das Hypothekar- und Immobilienkreditgesetz (HIKrG) mit eigenen Regeln. Prüfe die genauen Bedingungen in deinem Vertrag; Auskunft geben auch die Arbeiterkammer und der Verein für Konsumenteninformation.</p>

<h2>Deutschland: § 500 und § 502 BGB</h2>
<p>Auch in Deutschland können Verbraucher ein Darlehen jederzeit ganz oder teilweise vorzeitig zurückzahlen ({gii("bgb/__500.html", "§ 500 Abs. 2 BGB")}). Die Vorfälligkeitsentschädigung für Allgemein-Verbraucherdarlehen ist auf 1 % des vorzeitig zurückgezahlten Betrags begrenzt, bei höchstens einem Jahr Restlaufzeit auf 0,5 %, und darf die Sollzinsen für die restliche Laufzeit nicht übersteigen ({gii("bgb/__502.html", "§ 502 BGB")}, {STAND}). Für Immobiliar-Verbraucherdarlehen mit fester Zinsbindung ist eine vorzeitige Rückzahlung nur bei berechtigtem Interesse möglich; dann richtet sich die Entschädigung nach dem tatsächlichen Zinsschaden der Bank und kann deutlich höher sein.</p>
<div class="example"><strong>Lohnt es sich trotz Entschädigung?</strong> Im Ratenkredit-Beispiel kostet in Deutschland eine Entschädigung von höchstens 1 % auf 2.000 € maximal {eur(_vfe)}. In Österreich fällt bei 2.000 € gar keine Entschädigung an. Dem stehen {eur(_base_int-_int12-_intA)} gesparte Zinsen gegenüber – die Sondertilgung lohnt sich klar.</div>
<p class="small muted">Hinweis: Die neue EU-Verbraucherkreditrichtlinie (EU) 2023/2225 ist ab 20. November 2026 anzuwenden. Für Verträge, die danach geschlossen werden, können sich Details ändern. Maßgeblich ist das zum Vertragsabschluss geltende Recht.</p>

<h2>Sondertilgung oder lieber sparen?</h2>
<p>Eine Sondertilgung „verzinst“ sich mit dem Sollzins des Kredits – sicher und ohne Steuer, weil gesparte Zinsen kein Einkommen sind. Ein Tagesgeld mit angenommenen 2 % bringt in Österreich nach 25 % Kapitalertragsteuer nur {pct(_tg_net_at,1)}. Solange der Kreditzins darüber liegt, ist die Sondertilgung rechnerisch die bessere Anlage. Zwei Einschränkungen gelten trotzdem:</p>
<ul><li><strong>Reserve zuerst:</strong> Geld, das in den Kredit fließt, ist weg. Eine Rücklage für Reparaturen oder Jobverlust sollte vorher stehen, sonst droht ein teurer Überziehungsrahmen.</li>
<li><strong>Teuerste Schuld zuerst:</strong> Wer mehrere Kredite hat, tilgt zuerst den mit dem höchsten Zinssatz – meist den Konsum- oder Überziehungskredit, nicht den Wohnkredit.</li></ul>

<h2>Typische Fehler</h2>
<div class="warn"><strong>Ersparnis als Sollzins × Betrag × Gesamtlaufzeit rechnen:</strong> Gespart wird nur für die Restlaufzeit, und auch dort nur, solange die Schuld ohne Sondertilgung noch bestanden hätte.</div>
<div class="warn"><strong>Neue Rate nicht prüfen:</strong> Manche Banken senken nach einer Sondertilgung automatisch die Rate. Wer eigentlich Weg A wollte, verschenkt dann einen Teil der Ersparnis.</div>

<h2>Grenzen der Rechnung</h2>
<p>Die Beispiele rechnen mit festem Sollzins, monatlicher Verrechnung und ohne Gebühren. Bei variablem Zins ändert sich die Ersparnis mit dem Referenzzinssatz. Die Monatsrate und den Tilgungsplan ohne Sondertilgung zeigt der <a href="/kreditrechner.html">Kreditrechner</a>; den Unterschied zwischen Soll- und Effektivzins erklärt der Ratgeber <a href="/sollzins-und-effektivzins.html">Sollzins und Effektivzins</a>.</p>
{faq([
("Wann ist der beste Zeitpunkt für eine Sondertilgung?", "So früh wie möglich, sobald eine ausreichende Rücklage besteht. Jeder Monat früher spart Zinsen."),
("Muss die Bank eine Sondertilgung annehmen?", "Bei Verbraucherkrediten besteht in Österreich und Deutschland ein gesetzliches Recht auf vorzeitige Rückzahlung. Bei Wohnkrediten mit fester Zinsbindung sind die Rechte eingeschränkter; dort zählt der Vertrag."),
("Sinkt durch die Sondertilgung der Effektivzins?", "Nein, der Zinssatz bleibt gleich. Es sinkt die Summe der Zinsen, weil die Schuld kleiner ist oder kürzer läuft."),
])}
""",
}

# =====================================================================
# 3  14 Gehälter Österreich (vereinfacht)
_mb = 3000
_sz = 2 * _mb
_sechstel = 12 * _mb / 6
_sv_sz = 0.17
_sv_sz_amt = _sz * _sv_sz
_lst_sz = (_sz - _sv_sz_amt - 620) * 0.06
_net_sz = _sz - _sv_sz_amt - _lst_sz
_tp = 1100
_sv_l, _gst = 0.18, 0.30
_net100_l = 100 * (1 - _sv_l) * (1 - _gst)
_net100_s = 100 * (1 - _sv_sz) * (1 - 0.06)
_bonus = 4000

GEHALT = {
"slug": "bruttolohn-14-gehaelter",
"title": "14 Gehälter in Österreich: Was vom Urlaubs- und Weihnachtsgeld bleibt (vereinfacht)",
"teaser": "Warum das 13. und 14. Gehalt netto mehr bringt als ein normales – mit Rechenweg und klaren Grenzen.",
"description": "Urlaubs- und Weihnachtsgeld in Österreich vereinfacht berechnet: Jahressechstel, Freibetrag von 620 €, fester Steuersatz von 6 % und Sozialversicherung – mit Beispielen und Verweis auf den Brutto-Netto-Rechner des Finanzministeriums.",
"related": ["grundwert-richtig-waehlen", "prozent-oder-prozentpunkte", "realzins-sparen-inflation"],
"body": f"""
<p>In Österreich bekommen die meisten Angestellten und Arbeiter 14 Gehälter im Jahr: zwölf Monatsgehälter plus Urlaubs- und Weihnachtsgeld. Diese beiden <strong>Sonderzahlungen</strong> sind nicht im Gesetz vorgeschrieben, sondern in den Kollektivverträgen geregelt, die für fast alle Branchen gelten. Steuerlich werden sie als „sonstige Bezüge“ begünstigt – deshalb bleibt von einem 13. oder 14. Gehalt netto deutlich mehr übrig als von einem normalen Monatsgehalt gleicher Höhe.</p>
<div class="warn"><strong>Vereinfachung:</strong> Die Rechnungen auf dieser Seite zeigen das Prinzip. Sie verwenden runde Annahmen für die Sozialversicherung und lassen Absetzbeträge, Pendlerpauschale, Familienbonus und weitere Sonderfälle weg. Für eine genaue Berechnung nutze den offiziellen <a href="https://www.bmf.gv.at/brutto-netto-rechner" rel="noopener">Brutto-Netto-Rechner des Finanzministeriums</a> oder deine Lohnverrechnung. Allgemeine Informationen bietet <a href="https://www.oesterreich.gv.at" rel="noopener">oesterreich.gv.at</a> ({STAND}).</div>

<h2>Die drei Regeln für Sonderzahlungen</h2>
<ol><li><strong>Jahressechstel:</strong> Begünstigt sind sonstige Bezüge bis zu einem Sechstel der laufenden Bezüge des Jahres. Zwölf Monatsgehälter geteilt durch sechs ergibt genau zwei Monatsgehälter – deshalb passen Urlaubs- und Weihnachtsgeld in Höhe je eines Monatsgehalts normalerweise vollständig hinein.</li>
<li><strong>Freibetrag von 620 €:</strong> Die ersten 620 € innerhalb des Jahressechstels bleiben steuerfrei. Der Freibetrag wird nach Abzug der Sozialversicherung berücksichtigt und steht pro Kalenderjahr nur einmal zu.</li>
<li><strong>Fester Steuersatz von 6 %:</strong> Der Teil über 620 € wird nicht nach dem Tarif, sondern mit festen 6 % versteuert. Für sehr hohe Sonderzahlungen steigen die festen Sätze stufenweise.</li></ol>
<p>Dazu kommt eine <strong>Freigrenze</strong>: Beträgt das Jahressechstel höchstens 2.615 € (2026; 2025: 2.570 €), fällt auf die sonstigen Bezüge innerhalb des Sechstels keine Lohnsteuer an. Den Wert für 2026 nennt die Wirtschaftskammer. Rechtsgrundlage ist § 67 Einkommensteuergesetz 1988 ({RIS}); eine Übersicht bietet die <a href="https://www.wko.at/lohnverrechnung/sonstige-bezuege-lohnsteuerliche-behandlung-faq" rel="noopener">WKO zu sonstigen Bezügen</a> ({STAND}).</p>

<h2>Durchgerechnet: 3.000 € brutto im Monat</h2>
<p>Annahmen: 14 Gehälter zu je {eur(_mb)} brutto, keine weiteren Sonderzahlungen, Sozialversicherung auf Sonderzahlungen rund {de(_sv_sz*100,0)} %.</p>
<table class="tbl text"><tbody>
<tr><td>Laufende Bezüge im Jahr (12 × {eur(_mb)})</td><td>{eur(12*_mb)}</td></tr>
<tr><td>Jahressechstel ({eur(12*_mb)} ÷ 6)</td><td>{eur(_sechstel)}</td></tr>
<tr><td>Urlaubs- und Weihnachtsgeld zusammen</td><td>{eur(_sz)} – passt ins Sechstel</td></tr>
<tr><td>− Sozialversicherung (Annahme {de(_sv_sz*100,0)} %)</td><td>{eur(_sv_sz_amt)}</td></tr>
<tr><td>− Freibetrag</td><td>620,00 €</td></tr>
<tr><td>= mit 6 % zu versteuern</td><td>{eur(_sz-_sv_sz_amt-620)}</td></tr>
<tr><td>Lohnsteuer (6 %)</td><td>{eur(_lst_sz)}</td></tr>
<tr><td><strong>Netto aus beiden Sonderzahlungen</strong></td><td><strong>{eur(_net_sz)}</strong> ({pct(_net_sz/_sz*100)} des Bruttobetrags)</td></tr></tbody></table>
<p>Die Lohnsteuer auf beide Sonderzahlungen beträgt also nur {eur(_lst_sz)} – ein effektiver Steuersatz von {pct(_lst_sz/_sz*100)} auf den Bruttobetrag. Auf das laufende Gehalt fällt bei diesem Einkommen dagegen der normale Tarif an, dessen Grenzsteuersatz in dieser Einkommenshöhe in der Regel 30 % beträgt. Der Tarif kennt Stufen von 0 % bis 55 %.</p>

<h2>Was 100 € mehr brutto netto bedeuten</h2>
<p>Der Unterschied wird am deutlichsten, wenn man 100 € zusätzliches Brutto vergleicht. Mit vereinfachten Annahmen – {de(_sv_l*100,0)} % Sozialversicherung und 30 % Grenzsteuersatz auf laufende Bezüge, {de(_sv_sz*100,0)} % Sozialversicherung und 6 % auf Sonderzahlungen:</p>
<ul><li>100 € im laufenden Gehalt: 100 × (1 − {de(_sv_l,2)}) × (1 − 0,30) = <strong>{eur(_net100_l)}</strong> netto</li>
<li>100 € in einer Sonderzahlung: 100 × (1 − {de(_sv_sz,2)}) × (1 − 0,06) = <strong>{eur(_net100_s)}</strong> netto</li></ul>
<p>Eine Gehaltserhöhung um 100 € im Monat bringt bei 14 Zahlungen also zwölfmal den ersten und zweimal den zweiten Betrag: rund {eur(12*_net100_l+2*_net100_s)} netto im Jahr bei {eur(1400)} brutto. Wie man Gehaltserhöhungen in Prozent richtig vergleicht, zeigt der Ratgeber <a href="/grundwert-richtig-waehlen.html">Den richtigen Grundwert wählen</a>.</p>

<h2>Teilzeit: unter der Freigrenze</h2>
<div class="example">Bei {eur(_tp)} brutto im Monat beträgt das Jahressechstel 12 × {eur(_tp)} ÷ 6 = {eur(12*_tp/6)}. Das liegt unter der Freigrenze von 2.615 € (2026) – auf Urlaubs- und Weihnachtsgeld von zusammen {eur(2*_tp)} fällt dann keine Lohnsteuer an. Sozialversicherung wird trotzdem abgezogen, sofern das Einkommen über der Geringfügigkeitsgrenze liegt.</div>

<h2>Wenn das Jahressechstel überschritten wird</h2>
<p>Erhält jemand mit {eur(_mb)} Monatsgehalt im Dezember zusätzlich eine Prämie von {eur(_bonus)} als Einmalzahlung, liegen die sonstigen Bezüge bei {eur(_sz+_bonus)}. Das Jahressechstel beträgt aber nur {eur(_sechstel)}. Der Überhang von {eur(_sz+_bonus-_sechstel)} wird nicht mit 6 %, sondern wie ein laufender Bezug nach dem Tarif versteuert. Für die Lohnverrechnung gibt es dafür genaue Regeln, etwa wenn das Gehalt im Laufe des Jahres steigt oder Sonderzahlungen unterjährig ausgezahlt werden – das Sechstel wird dann aus den bisherigen laufenden Bezügen hochgerechnet und am Jahresende kontrolliert.</p>

<h2>Österreich und Deutschland im Vergleich</h2>
<p>In Deutschland gibt es keine vergleichbare Begünstigung. Weihnachts- oder Urlaubsgeld wird dort als sonstiger Bezug nach dem normalen Tarif besteuert und ist zudem nicht flächendeckend üblich. Wer Gehaltsangebote aus beiden Ländern vergleicht, sollte deshalb nicht nur 12 mit 14 Gehältern vergleichen, sondern auf das Jahresbrutto und – mit den jeweiligen offiziellen Rechnern – auf das Jahresnetto umrechnen. Den Brutto-Stundenlohn bei 12 oder 14 Gehältern zeigt der <a href="/stundenlohn-rechner.html">Stundenlohn-Rechner</a>.</p>

<h2>Typische Fehler</h2>
<div class="warn"><strong>Jahresgehalt durch 12 teilen:</strong> Ein Angebot über 42.000 € brutto im Jahr bedeutet in Österreich meist 3.000 € pro Monat (14 ×), nicht 3.500 € (12 ×).</div>
<div class="warn"><strong>Den Freibetrag doppelt rechnen:</strong> Die 620 € gelten einmal pro Jahr, nicht je Sonderzahlung – auch nicht bei einem Jobwechsel. Zu viel berücksichtigte Beträge werden in der Arbeitnehmerveranlagung korrigiert.</div>

<h2>Grenzen dieser Darstellung</h2>
<p>Die Sozialversicherungssätze hängen von Beschäftigtengruppe und Einkommenshöhe ab; bei niedrigen Einkommen ist etwa der Beitrag zur Arbeitslosenversicherung reduziert, und für Sonderzahlungen gilt eine eigene Höchstbeitragsgrundlage. Die festen Steuersätze, der Freibetrag und die Freigrenze können sich ändern. Die Zahlen hier sind deshalb Näherungen; verbindlich sind die Lohnabrechnung und der <a href="https://www.bmf.gv.at/brutto-netto-rechner" rel="noopener">BMF-Brutto-Netto-Rechner</a>.</p>
{faq([
("Steht mir Urlaubs- und Weihnachtsgeld gesetzlich zu?", "Nicht aufgrund eines Gesetzes, aber in den meisten Fällen aufgrund des Kollektivvertrags. Was für dich gilt, steht im Kollektivvertrag deiner Branche oder im Arbeitsvertrag."),
("Warum ist mein Weihnachtsgeld netto höher als mein Novembergehalt?", "Weil auf die Sonderzahlung statt des Tarifs nur 6 % Lohnsteuer anfallen und die Sozialversicherung etwas niedriger ist."),
("Bekomme ich die Sonderzahlungen auch anteilig?", "Wer nicht das ganze Jahr beschäftigt ist, erhält sie nach den meisten Kollektivverträgen anteilig. Die Details regelt der jeweilige Kollektivvertrag."),
])}
""",
}

# =====================================================================
# 4  Skonto oder Ratenzahlung
_price = 8000
_sk = 0.03
_cash = _price * (1 - _sk)
_nr = 10
_rate0 = _price / _nr
_apr0 = _apr(_cash, _rate0, _nr)
_simple_sk = _sk / (1 - _sk) * 360 / 20 * 100
_exact_sk = ((1 / (1 - 0.02)) ** (365 / 20) - 1) * 100
_r12 = annuity(_price, 5.9, 12)
_int12f = _r12 * 12 - _price
_apr12 = _apr(_cash, _r12, 12)
_dispo = _cash * 0.12 * 1.5 / 12
_tg = _cash * 0.02 * 0.75 * 10 / 12

SKONTO = {
"slug": "skonto-oder-ratenzahlung",
"title": "Skonto oder Ratenzahlung: Was ist günstiger?",
"teaser": "Eine 0-%-Finanzierung kann teurer sein als gedacht – wenn man dafür auf Skonto verzichtet.",
"description": "Skonto nutzen oder in Raten zahlen? Wie man den Zinssatz eines nicht genutzten Skontos ausrechnet, warum 0-%-Finanzierungen versteckte Kosten haben können und was Umsatzsteuer und Verbraucherrecht in Österreich und Deutschland dazu sagen.",
"related": ["rabatte-kombinieren", "sollzins-und-effektivzins", "kredit-sondertilgung"],
"body": f"""
<p>Wer eine größere Anschaffung macht – eine Küche, ein Fahrrad, eine Handwerkerleistung –, hat oft die Wahl: sofort zahlen und dafür Skonto abziehen oder bequem in Raten zahlen, manchmal sogar „zu 0 %“. Beide Angebote lassen sich mit einem einzigen Maßstab vergleichen: dem <strong>effektiven Jahreszins</strong>, den du zahlst, wenn du auf das Skonto verzichtest. Dieser Ratgeber zeigt, wie man ihn ausrechnet, und wann welche Variante günstiger ist.</p>

<h2>Skonto als Zinssatz</h2>
<p>Skonto ist ein Abzug für schnelles Bezahlen. „2 % Skonto innerhalb von 10 Tagen, 30 Tage netto“ heißt: Wer am 10. Tag zahlt, zahlt 98 %; wer bis zum 30. Tag wartet, zahlt 100 %. Wer wartet, „leiht“ sich also 98 % des Betrags für 20 Tage und zahlt dafür 2 % des Betrags – bezogen auf das geliehene Geld 2 ÷ 98 = {pct(2/98*100,2)}.</p>
<p>Aufs Jahr umgerechnet gibt es zwei übliche Rechenwege:</p>
<ul><li><strong>Kaufmännische Näherung:</strong> 2 ÷ 98 × 360 ÷ 20 = {pct(2/98*360/20*100)}. So steht es in vielen Lehrbüchern.</li>
<li><strong>Mit Zinseszins:</strong> (1 + 2/98)<sup>365/20</sup> − 1 = {pct(_exact_sk)}. Das entspricht der Logik des effektiven Jahreszinses, bei dem sich kurze Perioden über das Jahr aufschaukeln.</li></ul>
<p>Beide Zahlen sagen dasselbe: Ein nicht genutztes Skonto ist einer der teuersten Kredite überhaupt. Wer das Geld hat, sollte Skonto praktisch immer nutzen.</p>

<h2>Durchgerechnet: Küche um 8.000 €</h2>
<p>Ein Küchenstudio bietet drei Varianten an:</p>
<ol><li><strong>Sofortzahlung:</strong> {de(_sk*100,0)} % Skonto, also {eur(_cash)}.</li>
<li><strong>0-%-Finanzierung:</strong> {_nr} Monatsraten zu {eur(_rate0)}, zusammen {eur(_price)}, kein Skonto.</li>
<li><strong>Ratenkredit:</strong> 12 Monatsraten mit 5,9 % Sollzins auf {eur(_price)}: Rate {eur(_r12)}, Zinsen {eur(_int12f)}.</li></ol>
<div class="example"><strong>Was die 0-%-Finanzierung wirklich kostet:</strong> Wer sie wählt, verzichtet auf {eur(_price-_cash)} Skonto. Wirtschaftlich bekommt er also {eur(_cash)} und zahlt dafür {_nr} × {eur(_rate0)} zurück. Nach der EU-Methode für den effektiven Jahreszins entspricht das <strong>{pct(_apr0,2)}</strong> – obwohl „0 %“ draufsteht.</div>
<div class="example"><strong>Der Ratenkredit im selben Licht:</strong> Gemessen am Skontopreis von {eur(_cash)} zahlt man 12 × {eur(_r12)} zurück – ein effektiver Jahreszins von {pct(_apr12,2)}. Der Ratenkredit ist hier also nicht nur wegen seiner Zinsen teurer als die Sofortzahlung, sondern auch, weil das Skonto verloren geht.</div>
<p>Die Rechnung zeigt: Eine Finanzierung ist nur dann wirklich zinsfrei, wenn es bei Sofortzahlung keinen Preisvorteil gibt. Frag deshalb immer nach dem Barpreis, bevor du eine Finanzierung annimmst.</p>

<h2>Wenn das Geld knapp ist</h2>
<p>Hast du die {eur(_cash)} auf dem Sparkonto, ist der Vergleich einfach: Bei angenommenen 2 % Tageszins bringen sie in Österreich nach 25 % Kapitalertragsteuer in zehn Monaten nur rund {eur(_tg)} – das Skonto spart {eur(_price-_cash)}. Musst du für die Sofortzahlung dagegen den Überziehungsrahmen nutzen, lohnt sich ein Blick auf dessen Zins: Bei angenommenen 12 % pro Jahr kostet eine Überziehung von {eur(_cash)} über durchschnittlich 1,5 Monate rund {eur(_dispo)} – auch dann ist Skonto noch günstiger, sofern der Rahmen schnell wieder ausgeglichen ist.</p>
<p>Entscheidend ist also nicht, ob „0 %“ draufsteht, sondern was das teuerste Geld ist, das du sonst einsetzen müsstest.</p>

<h2>Österreich und Deutschland: Skonto und Umsatzsteuer</h2>
<p>Skonto mindert nachträglich das Entgelt und damit auch die Bemessungsgrundlage der Umsatzsteuer – in Deutschland nach {gii("ustg_1980/__17.html", "§ 17 UStG")}, in Österreich nach § 16 UStG 1994 ({RIS}). Für Privatkunden spielt das keine Rolle, weil sie den Bruttobetrag zahlen. Unternehmen müssen dagegen die Vorsteuer entsprechend berichtigen. In Deutschland muss eine Rechnung eine im Voraus vereinbarte Minderung des Entgelts wie Skonto angeben ({gii("ustg_1980/__14.html", "§ 14 Abs. 4 UStG")}, {STAND}).</p>
<p>Einen allgemeinen Anspruch auf Skonto gibt es in keinem der beiden Länder. Es gilt nur, wenn es vereinbart ist oder auf der Rechnung steht – samt Frist. Wer zu spät zahlt und trotzdem abzieht, schuldet den Rest.</p>

<h2>Österreich und Deutschland: Ratenkauf ist ein Kredit</h2>
<p>Eine Ratenzahlung beim Händler ist rechtlich in der Regel ein Verbraucherkredit, oft vermittelt über eine Bank. Für entgeltliche Teilzahlungsgeschäfte gelten in Deutschland die Regeln der {gii("bgb/__506.html", "§§ 506 ff. BGB")} mit Widerrufsrecht und Angabe des effektiven Jahreszinses; in Österreich gilt das Verbraucherkreditgesetz ({RIS}). Ob und welche Informationspflichten bei einer echten 0-%-Finanzierung ohne Gebühren greifen, hängt vom Einzelfall ab – lies die vorvertraglichen Informationen und achte auf Bearbeitungsgebühren, Kontoführung oder eine Restschuldversicherung, die die Finanzierung verteuern.</p>

<h2>Checkliste vor der Entscheidung</h2>
<ol><li>Barpreis mit Skonto erfragen – und schriftlich bestätigen lassen.</li><li>Effektiven Jahreszins der Finanzierung gegenüber dem Barpreis ausrechnen, nicht gegenüber dem Listenpreis.</li><li>Prüfen, welches eigene Geld sonst eingesetzt würde: Erspartes, Überziehungsrahmen oder ein anderer Kredit.</li><li>Nebenkosten der Finanzierung lesen: Bearbeitungsgebühr, Kontoführung, Versicherung.</li><li>Erst dann entscheiden – die bequemere Variante ist selten die günstigere.</li></ol>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Nur die Rate betrachten:</strong> {_nr} × {eur(_rate0)} klingen harmlos. Verglichen wird aber mit dem niedrigsten Preis, den du bekommen könntest – nicht mit dem Listenpreis.</div>
<div class="warn"><strong>Skonto-Frist verpassen:</strong> Die Frist beginnt meist mit dem Rechnungsdatum, nicht mit dem Eingang der Rechnung. Wer am letzten Tag überweist, sollte die Buchungsdauer bedenken.</div>
<div class="warn"><strong>Skonto vom falschen Betrag:</strong> Skonto wird vom Rechnungsbetrag nach allen Rabatten abgezogen. Mehrere Abzüge rechnet der <a href="/rabatt-rechner.html">Rabatt-Rechner</a> richtig hintereinander.</div>

<h2>Grenzen der Rechnung</h2>
<p>Die Effektivzinsen in diesem Ratgeber sind nach der EU-Methode mit jährlicher Abzinsung berechnet und gelten für die angegebenen Annahmen. Gebühren, Versicherungen und Lieferverzögerungen ändern das Ergebnis. Wie sich Rate und Zinskosten eines Kredits entwickeln, zeigt der <a href="/kreditrechner.html">Kreditrechner</a>.</p>
{faq([
("Ist 0-%-Finanzierung immer schlecht?", "Nein. Gibt es bei Sofortzahlung keinen Rabatt oder kein Skonto, kostet sie tatsächlich nichts – solange keine Gebühren oder Zusatzprodukte dazukommen."),
("Wie rechne ich Skonto schnell im Kopf in einen Jahreszins um?", "Skontosatz × 360 ÷ (Zahlungsziel − Skontofrist). 3 % bei 10 und 30 Tagen: 3 × 360 ÷ 20 = 54 %. Das ist eine leichte Unterschätzung, reicht aber für die Entscheidung."),
("Darf ich Skonto auch bei Teilzahlungen abziehen?", "Nur wenn das vereinbart ist. Üblich ist Skonto für die vollständige Zahlung innerhalb der Frist."),
("Kann ich als Privatkunde Skonto verlangen?", "Einen Anspruch gibt es nicht, aber fragen kostet nichts. Gerade bei Handwerkerrechnungen und größeren Anschaffungen ist ein Nachlass für sofortige Zahlung oft verhandelbar."),
("Gilt das Rücktrittsrecht auch für den Ratenkauf?", "Wenn die Ratenzahlung ein Kreditvertrag ist, gelten die Rücktritts- bzw. Widerrufsrechte für Verbraucherkredite. Die Frist und die Folgen für den Kaufvertrag stehen in den Vertragsunterlagen."),
])}
""",
}

# =====================================================================
# 5  Inflation und Kaufkraft: Realzins
_bal = 10000
_iz = 2.5
_at_net = _iz * 0.75
_at_real = ((1 + _at_net / 100) / (1 + VPI_AT[2025] / 100) - 1) * 100
_de_net = _iz
_de_real = ((1 + _de_net / 100) / (1 + VPI_DE[2025] / 100) - 1) * 100
_big = 50000
_big_z = _big * _iz / 100
_big_tax = (_big_z - 1000) * 0.26375
_big_net = (_big_z - _big_tax) / _big * 100
_kk = lambda r, n: 1 / (1 + r / 100) ** n
_10y_real = ((1 + _at_net / 100) / 1.02) ** 10

REALZINS = {
"slug": "realzins-sparen-inflation",
"title": "Inflation und Kaufkraft: Was Sparzinsen nach Steuer wirklich bringen",
"teaser": "Nominalzins, Steuer, Inflation – erst alle drei zusammen zeigen, ob Erspartes mehr wert wird.",
"description": "Realzins berechnen: wie Kapitalertragsteuer in Österreich, Abgeltungsteuer in Deutschland und Inflation den Sparzins schmälern – mit der genauen Formel, Rechenbeispielen und den Inflationsraten von Statistik Austria und Destatis.",
"related": ["zinseszins-und-72er-regel", "prozent-oder-prozentpunkte", "kredit-sondertilgung"],
"body": f"""
<p>Ein Sparkonto mit 2,5 % Zinsen klingt nach Gewinn. Ob das Geld tatsächlich mehr wert wird, entscheiden aber zwei Abzüge, die auf dem Kontoauszug nicht stehen: die Steuer auf die Zinsen und die Inflation, die die Kaufkraft jedes Euros verringert. Erst der <strong>Realzins nach Steuern</strong> zeigt, wie viel mehr du dir mit deinem Ersparten in einem Jahr leisten kannst. Dieser Ratgeber zeigt die Rechnung in drei Schritten, jeweils für Österreich und Deutschland.</p>

<h2>Schritt 1: vom Nominalzins zum Zins nach Steuer</h2>
<p><strong>Österreich:</strong> Zinsen aus Geldeinlagen bei Banken unterliegen der Kapitalertragsteuer von 25 % (§ 27a Einkommensteuergesetz 1988, {RIS}). Die Bank zieht sie automatisch ab; einen Freibetrag gibt es dafür nicht. Aus 2,5 % werden 2,5 × 0,75 = <strong>{pct(_at_net,3)}</strong>.</p>
<p><strong>Deutschland:</strong> Kapitalerträge unterliegen der Abgeltungsteuer von 25 % zuzüglich 5,5 % Solidaritätszuschlag darauf, zusammen 26,375 %, gegebenenfalls zuzüglich Kirchensteuer ({gii("estg/__32d.html", "§ 32d EStG")}). Bis zum Sparer-Pauschbetrag von 1.000 € pro Person und Jahr (2.000 € bei Zusammenveranlagung) bleiben Kapitalerträge steuerfrei, wenn der Bank ein Freistellungsauftrag vorliegt oder die Erträge in der Steuererklärung angegeben werden ({gii("estg/__20.html", "§ 20 Abs. 9 EStG")}, {STAND}). Für die meisten Sparerinnen und Sparer mit kleineren Beträgen bleibt der Zins deshalb unversteuert: 2,5 % bleiben 2,5 %.</p>
<div class="example"><strong>Deutschland mit größerem Guthaben:</strong> {eur(_big)} zu {de(_iz,1)} % bringen {eur(_big_z)} Zinsen. {eur(_big_z-1000)} davon liegen über dem Pauschbetrag; die Steuer beträgt {eur(_big_z-1000)} × 26,375 % = {eur(_big_tax)}. Nach Steuer bleiben {pct(_big_net,2)}.</div>

<h2>Schritt 2: die Inflation abziehen – aber richtig</h2>
<p>Die Näherung „Zins minus Inflation“ ist für kleine Werte brauchbar. Genau rechnet man mit der <strong>Fisher-Gleichung</strong>:</p>
<p class="formula">Realzins = (1 + Zins nach Steuer) ÷ (1 + Inflationsrate) − 1</p>
<p>Der Grund: Nach einem Jahr hast du (1 + Zins) Euro, aber jeder Euro kauft nur noch 1 ÷ (1 + Inflation) dessen, was er vorher kaufte.</p>

<h2>Schritt 3: durchgerechnet mit den Inflationsraten 2025</h2>
<div class="example"><strong>Österreich:</strong> Statistik Austria meldet für 2025 eine Inflationsrate von {de(VPI_AT[2025],1)} %. Realzins: 1,01875 ÷ {de(1+VPI_AT[2025]/100,3)} − 1 = <strong>{pct(_at_real,2)}</strong>. Von {eur(_bal)} bleiben real nach einem Jahr {eur(_bal*(1+_at_real/100))} – das Guthaben ist nominal gewachsen, die Kaufkraft gesunken. Quelle: {SRC_STAT_AT}.</div>
<div class="example"><strong>Deutschland:</strong> Destatis meldet für 2025 eine Inflationsrate von {de(VPI_DE[2025],1)} %. Realzins unter dem Pauschbetrag: 1,025 ÷ {de(1+VPI_DE[2025]/100,3)} − 1 = <strong>{pct(_de_real,2)}</strong>. Hier bleibt ein kleiner realer Zuwachs. Quelle: {SRC_DESTATIS}.</div>
<p>Der Unterschied liegt hier vor allem an der höheren österreichischen Inflationsrate 2025 und am fehlenden Freibetrag. Beides kann sich in anderen Jahren anders darstellen.</p>

<h2>Kaufkraft über mehrere Jahre</h2>
<p>Wie stark Inflation über die Zeit wirkt, zeigt der Kaufkraftfaktor 1 ÷ (1 + Inflation)ⁿ. So viel kaufen 1.000 € nach n Jahren noch, gemessen an heutigen Preisen:</p>
<table class="tbl"><thead><tr><th>Inflation p. a.</th><th>nach 5 Jahren</th><th>nach 10 Jahren</th><th>nach 20 Jahren</th></tr></thead><tbody>
{''.join(f'<tr><td>{de(r,1)} %</td>' + ''.join(f'<td>{eur(1000*_kk(r,n))}</td>' for n in (5, 10, 20)) + '</tr>' for r in (2.0, 3.0, 3.6))}
</tbody></table>
<div class="example"><strong>Zehn Jahre Sparbuch in Österreich:</strong> Angenommen, der Zins bleibt bei {de(_iz,1)} % ({pct(_at_net,3)} nach Kapitalertragsteuer) und die Inflation pendelt sich beim EZB-Ziel von 2 % ein. Dann entspricht die Kaufkraft von {eur(_bal)} nach zehn Jahren {eur(_bal*_10y_real)} in heutigen Preisen – eine Veränderung von {pct((_10y_real-1)*100,1)}. Selbst beim Inflationsziel reicht der Zins nach Steuer in diesem Beispiel also nicht ganz für einen realen Zuwachs; bei 3 % Inflation wäre der Verlust deutlich größer.</div>
<p>Die Europäische Zentralbank strebt mittelfristig eine Inflationsrate von 2 % an. Ob sie erreicht wird, ist nicht sicher – für langfristige Überlegungen ist es sinnvoll, mehrere Raten durchzurechnen. Das geht mit dem <a href="/inflationsrechner.html">Inflationsrechner</a>.</p>

<h2>Was das für Entscheidungen bedeutet</h2>
<ul><li><strong>Notgroschen:</strong> Für Geld, das jederzeit verfügbar sein muss, ist ein leicht negativer Realzins oft der Preis der Sicherheit. Entscheidend ist hier die Verfügbarkeit, nicht die Rendite.</li>
<li><strong>Schulden:</strong> Inflation wirkt auch auf Kredite: Ein fester Kreditzins von 4 % bei 3 % Inflation entspricht real nur rund 1 %. Trotzdem ist ein Kredit in der Regel teurer als jeder sichere Sparzins nach Steuer – deshalb rechnet sich eine <a href="/kredit-sondertilgung.html">Sondertilgung</a> oft mehr als Sparen.</li>
<li><strong>Langfristige Anlage:</strong> Wer real wachsen will, muss meist Schwankungen in Kauf nehmen. Ob und wie, ist eine persönliche Entscheidung; dieser Ratgeber ersetzt keine Anlageberatung.</li></ul>

<h2>Typische Fehler</h2>
<div class="warn"><strong>Steuer vergessen:</strong> Wer in Österreich 2,5 % Zins mit 2 % Inflation vergleicht, sieht 0,5 % realen Zuwachs. Nach Kapitalertragsteuer bleiben aber nur {pct(_at_net,3)} – real ein leichtes Minus.</div>
<div class="warn"><strong>Zins und Inflation verschiedener Zeiträume mischen:</strong> Ein Aktionszins für drei Monate ist kein Jahreszins. Vergleiche immer Jahreswerte – und die Inflation des Jahres, in dem du das Geld angelegt hast.</div>
<div class="warn"><strong>Prozente und Prozentpunkte verwechseln:</strong> Steigt der Zins von 2 % auf 2,5 %, ist das ein Plus von 0,5 Prozentpunkten, aber von 25 %. Mehr dazu im Ratgeber <a href="/prozent-oder-prozentpunkte.html">Prozent oder Prozentpunkte</a>.</div>

<h2>Grenzen</h2>
<p>Die offizielle Inflationsrate beruht auf einem durchschnittlichen Warenkorb; deine persönliche Teuerung kann höher oder niedriger sein. Steuerregeln können sich ändern, und Sonderfälle wie Kirchensteuer, Günstigerprüfung oder ausländische Konten sind hier nicht berücksichtigt. Im Zweifel helfen Finanzamt oder Steuerberatung.</p>
{faq([
("Was ist der Unterschied zwischen Nominalzins und Realzins?", "Der Nominalzins ist der Zins in Euro. Der Realzins berücksichtigt zusätzlich, wie sich die Preise verändert haben, und zeigt den Zuwachs an Kaufkraft."),
("Kann der Realzins negativ sein, obwohl ich Zinsen bekomme?", "Ja, immer dann, wenn die Inflation höher ist als der Zins nach Steuer. Das Guthaben wächst dann nominal, kauft aber weniger."),
("Gilt das auch für Festgeld und Sparbuch?", "Ja. In Österreich unterliegen Zinsen aus allen Geldeinlagen bei Banken der Kapitalertragsteuer von 25 %, in Deutschland gilt für alle Zinsen die Abgeltungsteuer. Beim Festgeld kommt hinzu, dass der Zins für die Laufzeit fix ist, die Inflation aber nicht."),
("Muss ich in Österreich die Kapitalertragsteuer selbst abführen?", "Bei Zinsen auf Konten österreichischer Banken nicht – die Bank zieht sie ab, damit ist die Steuer in der Regel abgegolten. Bei Konten im Ausland gelten andere Regeln."),
])}
""",
}

# =====================================================================
# 6  Stromtarife vergleichen
_gA, _aA = 12.0, 0.28
_gB, _aB = 6.0, 0.32
_be = (_gA - _gB) * 12 / (_aB - _aA)
_use = [1500, 2500, 3500, 5000]
_bonus = 100
_avg = lambda g, a, kwh: (g * 12 + a * kwh) / kwh

TARIF = {
"slug": "stromtarife-vergleichen",
"title": "Stromtarife vergleichen: Grundgebühr, Arbeitspreis und der echte Preis pro kWh",
"teaser": "Ab welchem Verbrauch lohnt sich eine höhere Grundgebühr? Die Gewinnschwelle zweier Tarife ausrechnen.",
"description": "Stromtarife richtig vergleichen: Jahreskosten aus Grundgebühr und Arbeitspreis, Durchschnittspreis pro kWh, Gewinnschwelle zwischen zwei Tarifen und Neukundenbonus – mit Rechenbeispielen und Hinweisen zu E-Control und Bundesnetzagentur.",
"related": ["waermepumpe-stromkosten", "prozent-oder-prozentpunkte", "realzins-sparen-inflation"],
"body": f"""
<p>Ein Stromtarif besteht fast immer aus zwei Teilen: einem festen Betrag pro Monat oder Jahr – Grundgebühr oder Grundpreis – und einem Preis für jede verbrauchte Kilowattstunde, dem <strong>Arbeitspreis</strong>. Welcher Tarif günstiger ist, hängt deshalb vom eigenen Verbrauch ab. Ein niedriger Arbeitspreis nützt wenig, wenn die Grundgebühr ihn bei kleinem Verbrauch auffrisst; eine niedrige Grundgebühr wird bei hohem Verbrauch teuer. Mit drei einfachen Formeln lässt sich das für jeden Haushalt nachrechnen.</p>

<h2>Formel 1: Jahreskosten</h2>
<p class="formula">Jahreskosten = Grundgebühr pro Monat × 12 + Arbeitspreis × Jahresverbrauch</p>
<p>Zwei Beispieltarife mit angenommenen Bruttopreisen:</p>
<ul><li><strong>Tarif A:</strong> {eur(_gA)} Grundgebühr im Monat, {de(_aA*100,0)} Cent pro kWh</li>
<li><strong>Tarif B:</strong> {eur(_gB)} Grundgebühr im Monat, {de(_aB*100,0)} Cent pro kWh</li></ul>
<table class="tbl"><thead><tr><th>Verbrauch</th><th>Tarif A</th><th>Tarif B</th><th>günstiger</th></tr></thead><tbody>
{''.join(f'<tr><td>{de(k,0)} kWh</td><td>{eur(_gA*12+_aA*k)}</td><td>{eur(_gB*12+_aB*k)}</td><td>{"A" if _gA*12+_aA*k < _gB*12+_aB*k else "B"}</td></tr>' for k in _use)}
</tbody></table>

<h2>Formel 2: die Gewinnschwelle zwischen zwei Tarifen</h2>
<p>Ab welchem Verbrauch der Tarif mit der höheren Grundgebühr günstiger wird, ergibt sich, wenn man beide Jahreskosten gleichsetzt:</p>
<p class="formula">Verbrauch = Unterschied der Grundgebühren pro Jahr ÷ Unterschied der Arbeitspreise</p>
<div class="example">Tarif A kostet im Jahr ({eur(_gA)} − {eur(_gB)}) × 12 = {eur((_gA-_gB)*12)} mehr Grundgebühr, spart aber {de((_aB-_aA)*100,0)} Cent pro kWh. Gewinnschwelle: {de((_gA-_gB)*12,0)} ÷ {de(_aB-_aA,2)} = <strong>{de(_be,0)} kWh</strong>. Wer mehr verbraucht, fährt mit Tarif A besser, wer weniger verbraucht, mit Tarif B.</div>
<p>Diese Rechnung funktioniert wie ein <a href="/dreisatz-rechner.html">Dreisatz</a>: Die feste Mehrbelastung wird durch die Ersparnis pro Einheit geteilt. Sie gilt für jede Kombination aus Grund- und Mengenpreis – auch bei Mobilfunk, Bahnkarten oder Mitgliedsbeiträgen.</p>

<h2>Formel 3: der echte Durchschnittspreis pro kWh</h2>
<p class="formula">Durchschnittspreis = Jahreskosten ÷ Jahresverbrauch</p>
<p>Er zeigt, was eine Kilowattstunde einschließlich Grundgebühr im Mittel kostet. Für Tarif A:</p>
<table class="tbl"><thead><tr><th>Verbrauch</th><th>Durchschnittspreis Tarif A</th></tr></thead><tbody>
{''.join(f'<tr><td>{de(k,0)} kWh</td><td>{de(_avg(_gA,_aA,k)*100,1)} Cent</td></tr>' for k in _use)}
</tbody></table>
<p>Der Durchschnittspreis sinkt mit dem Verbrauch, weil sich die Grundgebühr auf mehr Kilowattstunden verteilt. <strong>Für die Frage, was ein einzelnes zusätzliches Gerät kostet, zählt aber nur der Arbeitspreis</strong> – die Grundgebühr fällt ohnehin an. Deshalb verwendet der <a href="/stromkosten-rechner.html">Stromkosten-Rechner</a> den Arbeitspreis.</p>

<h2>Neukundenbonus richtig einrechnen</h2>
<div class="example">Ein Anbieter gewährt {eur(_bonus)} Bonus im ersten Jahr. Bei 2.500 kWh senkt das die Jahreskosten von Tarif B im ersten Jahr von {eur(_gB*12+_aB*2500)} auf {eur(_gB*12+_aB*2500-_bonus)} – billiger als Tarif A mit {eur(_gA*12+_aA*2500)}. Ab dem zweiten Jahr entfällt der Bonus, dann ist B wieder um {eur(_gB*12+_aB*2500-_gA*12-_aA*2500)} teurer. Über zwei Jahre gerechnet ist B insgesamt um {eur(abs(2*(_gB*12+_aB*2500)-_bonus-2*(_gA*12+_aA*2500)))} {"teurer" if 2*(_gB*12+_aB*2500)-_bonus > 2*(_gA*12+_aA*2500) else "günstiger"}, über drei Jahre um {eur(abs(3*(_gB*12+_aB*2500)-_bonus-3*(_gA*12+_aA*2500)))} {"teurer" if 3*(_gB*12+_aB*2500)-_bonus > 3*(_gA*12+_aA*2500) else "günstiger"}.</div>
<p>Vergleiche Tarife mit Bonus deshalb über die Zeit, die du tatsächlich beim Anbieter bleiben willst, und prüfe, ob der Bonus an Bedingungen wie eine Mindestlaufzeit geknüpft ist.</p>

<h2>Verbrauch richtig bestimmen</h2>
<p>Die wichtigste Eingabe ist dein eigener Jahresverbrauch. Er steht auf der letzten Jahresabrechnung. Kommt ein großer Verbraucher dazu – ein Elektroauto, ein Durchlauferhitzer oder eine Wärmepumpe –, verändert sich die Rechnung deutlich: Mit zusätzlich rund {de(round(_wp_kwh,-2),0)} kWh für eine Wärmepumpe (wie im Ratgeber <a href="/waermepumpe-stromkosten.html">Stromkosten einer Wärmepumpe</a> abgeschätzt) liegt fast jeder Haushalt weit über der Gewinnschwelle, und der niedrigere Arbeitspreis wird wichtiger als die Grundgebühr.</p>

<h2>Österreich und Deutschland: wo man Tarife amtlich vergleicht</h2>
<p>Die Stromrechnung enthält in beiden Ländern neben dem Energiepreis des Lieferanten auch Netzkosten, Steuern und Abgaben. Für den Anbietervergleich zählen die Gesamtkosten brutto. In Österreich bietet die Regulierungsbehörde <a href="https://www.e-control.at" rel="noopener">E-Control</a> einen amtlichen Tarifkalkulator, der nach Postleitzahl und Verbrauch die Jahreskosten aller Anbieter berechnet. In Deutschland regelt {gii("enwg_2005/__40.html", "§ 40 Energiewirtschaftsgesetz")}, welche Angaben auf Stromrechnungen stehen müssen; die <a href="https://www.bundesnetzagentur.de" rel="noopener">Bundesnetzagentur</a> informiert über Anbieterwechsel und Verbraucherrechte ({STAND}).</p>

<h2>Typische Fehler</h2>
<div class="warn"><strong>Nur den Arbeitspreis vergleichen:</strong> Bei 1.500 kWh ist Tarif B trotz {de((_aB-_aA)*100,0)} Cent höherem Arbeitspreis um {eur(_gA*12+_aA*1500-_gB*12-_aB*1500)} günstiger.</div>
<div class="warn"><strong>Netto- und Bruttopreise mischen:</strong> Manche Angebote nennen Preise ohne Umsatzsteuer. Vergleiche immer Bruttowerte – das sind die Beträge, die ein Haushalt tatsächlich zahlt.</div>
<div class="warn"><strong>Preisänderungen ignorieren:</strong> Ein Fixpreis gilt nur für die vereinbarte Dauer. Danach kann sich der Arbeitspreis ändern; der Vergleich muss dann neu gerechnet werden.</div>

<h2>Grenzen</h2>
<p>Die Beispieltarife sind erfunden, um die Rechnung zu zeigen; echte Preise unterscheiden sich nach Region, Netzgebiet und Zeitpunkt. Dynamische Tarife mit stündlich wechselnden Preisen lassen sich mit diesen Formeln nur näherungsweise abbilden, weil es dort auf den Zeitpunkt des Verbrauchs ankommt.</p>
{faq([
("Was ist günstiger: hohe oder niedrige Grundgebühr?", "Bei geringem Verbrauch meist die niedrige Grundgebühr, bei hohem Verbrauch der niedrigere Arbeitspreis. Wo die Grenze liegt, zeigt die Gewinnschwelle."),
("Gehört die Grundgebühr in den Stromkosten-Rechner?", "Nein. Für ein einzelnes Gerät zählt nur der Arbeitspreis, weil die Grundgebühr unabhängig davon anfällt."),
("Was ist ein Durchschnittspreis von 33 Cent wert, wenn der Arbeitspreis 28 Cent beträgt?", "Die Differenz ist die auf jede Kilowattstunde verteilte Grundgebühr. Für Vergleiche zwischen Tarifen ist der Durchschnittspreis bei deinem Verbrauch der richtige Wert, für ein einzelnes Gerät der Arbeitspreis."),
("Zählt die Netzgebühr zum Arbeitspreis?", "Das hängt von der Darstellung ab. Manche Angebote nennen nur den Energiepreis des Lieferanten, andere den Gesamtpreis mit Netz, Steuern und Abgaben. Vergleiche immer die Gesamtkosten brutto, wie sie amtliche Tarifrechner ausweisen."),
("Wie oft sollte ich Tarife vergleichen?", "Spätestens, wenn ein Fixpreis ausläuft, der Anbieter die Preise ändert oder sich dein Verbrauch deutlich verändert, etwa durch ein Elektroauto oder eine Wärmepumpe."),
])}
""",
}

GUIDES = [WP, SONDER, GEHALT, SKONTO, REALZINS, TARIF]
for _g in GUIDES:
    _g["published"] = "2026-11-04"


# ---------- Ergänzungen (eingefügt vor „Typische Fehler“)
def _sz_net(mb, sv=0.17):
    sz = 2 * mb; s = sz * sv; t = max(sz - s - 620, 0) * 0.06
    return sz, s, t, sz - s - t


_rate_plus = _r + 50
_m_plus, _int_plus, _ = run_loan(_K, _p, _rate_plus)
_m_once, _int_once, _ = run_loan(_K, _p, _r, extra={12: 600, 24: 600, 36: 600, 48: 600})
_be_at = lambda pi: pi / 0.75
_be_de = lambda pi: pi / (1 - 0.26375)
_buy_m = 20000
_sk_year = _buy_m * 12 * 0.02
_kk_cost = _buy_m * 0.98 * 0.09 * 20 / 360 * 12
_pA_old, _pA_new = 0.28, 0.31
_k_old, _k_new = _gA * 12 + _pA_old * 2500, _gA * 12 + _pA_new * 2500
_abschlag = _k_old / 12
_nach = _gA * 12 + _pA_old * 2750 - _abschlag * 12

_GADD = {
"bruttolohn-14-gehaelter": f"""
<h2>Sonderzahlungen bei verschiedenen Gehältern</h2>
<p>Mit denselben vereinfachten Annahmen (Sonderzahlungen je ein Monatsgehalt, rund 17 % Sozialversicherung, Freibetrag 620 €, 6 % Steuer, keine weiteren sonstigen Bezüge im Jahr):</p>
<div class="scroll"><table class="tbl"><thead><tr><th>Monatsbrutto</th><th>Sonderzahlungen brutto</th><th>Lohnsteuer darauf</th><th>netto (ca.)</th></tr></thead><tbody>
{''.join(f'<tr><td>{eur(m)}</td><td>{eur(_sz_net(m)[0])}</td><td>{eur(_sz_net(m)[2])}</td><td>{eur(_sz_net(m)[3])}</td></tr>' for m in (2000, 2500, 3000, 4000, 5000))}
</tbody></table></div>
<p>Die Lohnsteuer bleibt in allen Zeilen bei rund 5 % des Bruttobetrags oder darunter. Den größeren Abzug macht die Sozialversicherung aus. Für Sonderzahlungen gilt eine eigene jährliche Höchstbeitragsgrundlage; darüber fallen keine weiteren Beiträge an – bei den Gehältern in der Tabelle wird sie nicht erreicht.</p>
<h2>Wann wird ausgezahlt?</h2>
<p>Den Zeitpunkt legt der Kollektivvertrag fest. Häufig wird das Urlaubsgeld mit dem Gehalt für Mai oder Juni und das Weihnachtsgeld mit dem Novembergehalt ausgezahlt; manche Verträge sehen andere Termine oder eine Aufteilung vor. Wer im Laufe des Jahres ein- oder austritt, erhält in vielen Kollektivverträgen einen anteiligen Betrag. Das Jahressechstel wird in der Lohnverrechnung schon unterjährig aus den bisher bezahlten laufenden Bezügen hochgerechnet – deshalb kann sich die Steuer auf das Weihnachtsgeld ändern, wenn das Gehalt zwischen Juni und November gestiegen ist.</p>
""",
"kredit-sondertilgung": f"""
<h2>Einmal im Jahr oder jeden Monat ein bisschen mehr?</h2>
<p>Wer keinen größeren Betrag auf einmal hat, kann auch die Rate erhöhen, sofern der Vertrag das erlaubt. Zwei Varianten für den Ausgangskredit über {eur(_K)}, beide mit 600 € zusätzlicher Tilgung pro Jahr:</p>
<ul><li><strong>Rate um 50 € erhöhen:</strong> {eur(_rate_plus)} statt {eur(_r)}. Der Kredit ist nach {_m_plus} Monaten getilgt, die Zinsen betragen {eur(_int_plus)} – eine Ersparnis von {eur(_base_int-_int_plus)}.</li>
<li><strong>Jährlich 600 € Sondertilgung</strong> nach der 12., 24., 36. und 48. Rate: Laufzeit {_m_once} Monate, Zinsen {eur(_int_once)}, Ersparnis {eur(_base_int-_int_once)}.</li></ul>
<p>Die monatliche Variante spart etwas mehr, weil jeder zusätzliche Euro früher wirkt. Der Unterschied ist aber klein; entscheidend ist, dass überhaupt zusätzlich getilgt wird – und dass die Bank die Zahlung wirklich als Tilgung verbucht.</p>
""",
"realzins-sparen-inflation": f"""
<h2>Welcher Zins erhält die Kaufkraft?</h2>
<p>Damit Erspartes real nicht an Wert verliert, muss der Zins nach Steuer mindestens so hoch sein wie die Inflation. Umgekehrt gerechnet heißt das: <strong>nötiger Nominalzins = Inflationsrate ÷ (1 − Steuersatz)</strong>. Exakt gilt diese Rechnung für den Realzins von null, weil dann Fisher-Gleichung und Näherung übereinstimmen.</p>
<div class="scroll"><table class="tbl"><thead><tr><th>Inflation</th><th>Österreich (25 % KESt)</th><th>DE über Pauschbetrag (26,375 %)</th><th>DE unter Pauschbetrag</th></tr></thead><tbody>
{''.join(f'<tr><td>{de(pi,1)} %</td><td>{pct(_be_at(pi),2)}</td><td>{pct(_be_de(pi),2)}</td><td>{pct(pi,2)}</td></tr>' for pi in (2.0, 2.2, 3.0, 3.6))}
</tbody></table></div>
<p>Bei 2 % Inflation braucht es in Österreich also rund 2,67 % Zins, damit nach Kapitalertragsteuer kein Kaufkraftverlust entsteht. Die Steuer wirkt dabei wie ein Aufschlag auf die Inflation: Sie wird auf den ganzen Zins erhoben, auch auf den Teil, der nur die Teuerung ausgleicht.</p>
""",
"skonto-oder-ratenzahlung": f"""
<h2>Skonto im Unternehmen: ein Jahr durchgerechnet</h2>
<div class="example">Ein Betrieb kauft jeden Monat Waren um {eur(_buy_m)} bei einem Lieferanten mit „2 % Skonto binnen 10 Tagen, 30 Tage netto“. Nutzt er das Skonto immer, spart er im Jahr 2 % von {eur(_buy_m*12)} = <strong>{eur(_sk_year)}</strong>. Fehlt das Geld am 10. Tag und muss er dafür das Kontokorrent mit angenommenen 9 % Zinsen für jeweils 20 Tage nutzen, kostet das pro Monat {eur(_buy_m*0.98)} × 9 % × 20 ÷ 360 = {eur(_buy_m*0.98*0.09*20/360)}, im Jahr {eur(_kk_cost)}. Es bleibt ein Vorteil von {eur(_sk_year-_kk_cost)}.</div>
<p>Für die Liquiditätsplanung heißt das: Skontofristen gehören in den Zahlungsplan wie Fixkosten. Wer sie regelmäßig verpasst, zahlt rechnerisch einen Zins, den kaum ein Kredit erreicht.</p>
""",
"stromtarife-vergleichen": f"""
<h2>Preiserhöhung: Prozent beim Arbeitspreis ist nicht Prozent bei den Kosten</h2>
<div class="example">Der Arbeitspreis von Tarif A steigt von {de(_pA_old*100,0)} auf {de(_pA_new*100,0)} Cent – ein Plus von {de((_pA_new-_pA_old)/_pA_old*100,1)} %. Bei 2.500 kWh steigen die Jahreskosten aber von {eur(_k_old)} auf {eur(_k_new)}, also nur um {de((_k_new-_k_old)/_k_old*100,1)} %, weil die Grundgebühr gleich bleibt. Umgekehrt wirkt eine Erhöhung der Grundgebühr bei kleinem Verbrauch prozentual stärker als bei großem.</div>
<p>Der Unterschied zwischen dem Anstieg eines Preisbestandteils und dem Anstieg der Gesamtkosten ist ein typischer Grundwert-Fehler. Mehr dazu im Ratgeber <a href="/grundwert-richtig-waehlen.html">Den richtigen Grundwert wählen</a>.</p>
<h2>Monatliche Teilbeträge richtig festlegen</h2>
<p>Die meisten Haushalte zahlen monatliche Teilbeträge (in Deutschland meist „Abschlag“ genannt), die am Ende des Abrechnungsjahres mit dem tatsächlichen Verbrauch verrechnet werden. Der passende Teilbetrag ist einfach: Jahreskosten ÷ 12.</p>
<div class="example">Tarif A bei 2.500 kWh: {eur(_k_old)} ÷ 12 = {eur(_abschlag)} pro Monat. Steigt der Verbrauch im Jahr um 10 % auf 2.750 kWh, kostet das Jahr {eur(_gA*12+_pA_old*2750)}. Mit dem alten Teilbetrag entsteht eine Nachzahlung von {eur(_nach)} – genau die zusätzlichen 250 kWh mal Arbeitspreis.</div>
<p>Wer weiß, dass ein neuer Großverbraucher dazukommt, passt den Teilbetrag besser gleich an, statt am Jahresende eine hohe Nachzahlung zu erhalten.</p>
""",
}
for _g in GUIDES:
    if _g["slug"] in _GADD:
        _i = _g["body"].index("<h2>Typische Fehler</h2>")
        _g["body"] = _g["body"][:_i] + _GADD[_g["slug"]].strip() + "\n" + _g["body"][_i:]
