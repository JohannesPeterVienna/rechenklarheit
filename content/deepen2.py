"""Vertiefung November 2026 für die Rechner mit bisher wenig Erklärtext.
Jeder Abschnitt ergänzt nur, was auf der Seite noch fehlt: Rechenweg, durchgerechnete Beispiele,
Besonderheiten für Österreich und Deutschland mit Quelle, typische Fehler, Grenzen und Häufige Fragen.
Alle Zahlen werden hier in Python berechnet; die wichtigsten prüft test_calc.js zusätzlich mit dem Browser-Code."""
import math
from content.calcs import de, eur
from content.deepen import faq

STAND = "Stand: November 2026"
GII = "https://www.gesetze-im-internet.de"
RIS = '<a href="https://www.ris.bka.gv.at" rel="noopener">Rechtsinformationssystem des Bundes (RIS)</a>'


def gii(path, text):
    return f'<a href="{GII}/{path}" rel="noopener">{text}</a>'


def _annuity(K, p, months):
    i = p / 100 / 12
    return K * i / (1 - (1 + i) ** -months) if i else K / months


def _save(k0, rate, p, months, start=False):
    """Sparplan mit monatlicher Verzinsung; start=True zahlt am Monatsanfang ein."""
    i, k = p / 100 / 12, k0
    for _ in range(months):
        k = (k + rate) * (1 + i) if start else k * (1 + i) + rate
    return k


# ---------- Prozentrechner
_vz_de = 1000 * 0.07 * 30 / 365          # 5 PP über angenommenem Basiszinssatz 2 %
_vz_at = 1000 * 0.04 * 30 / 365          # gesetzliche Zinsen 4 % (§ 1000 ABGB)
_grest, _ggb = 300000 * 0.035, 300000 * 0.011
_grest_de = [(3.5, 300000 * 0.035), (5.0, 300000 * 0.05), (6.5, 300000 * 0.065)]

# ---------- Mehrwertsteuer
_h_de_n = 98 / 1.07 + 15 / 1.19           # Hotelrechnung DE: Übernachtung 7 %, Parkplatz 19 %
_h_de_t = 98 + 15 - _h_de_n
_rt = round(round(49.95 / 1.2, 2) * 1.2, 2)

# ---------- Rabatt
_bike = 1299 * 0.85 * 0.97
_need = 1 - 699 / 899

# ---------- Zinseszins
_i3 = 0.03 / 12
_z_formula = 100 * ((1 + _i3) ** 240 - 1) / _i3
_early = _save(0, 150, 4, 40 * 12)
_late = _save(0, 150, 4, 30 * 12)
_late_eq = 150 * (_early / _late)
_z_end = _save(0, 100, 3, 240)
_z_start = _save(0, 100, 3, 240, start=True)
_ter_a, _ter_b = _save(0, 200, 6, 300), _save(0, 200, 5, 300)

# ---------- Kredit
_K, _p, _m = 20000, 4.5, 60
_ka = _annuity(_K, _p, _m)
_rows = []
_rest = _K
for _k in range(1, 4):
    _z = _rest * _p / 100 / 12; _t = _ka - _z; _rest -= _t
    _rows.append((_k, _z, _t, _rest))
_simple = _K * _p / 100 * 5
_true_int = _ka * _m - _K

# ---------- Dreisatz
_kg_a, _kg_b = 2.79 / 400 * 1000, 6.49
_paint = 2.5 / 10 * 34

# ---------- Strom
_tv_kwh = 100 * 4 / 1000 * 365
_fr_old, _fr_new = 300, 150
_fr_save = (_fr_old - _fr_new) * 0.30
_wm = 55 / 100 * 200
_amp_w = 230 * 8.7

# ---------- Aufschlag
_ek2, _hk, _gz = 80.0, 0.35, 0.12
_sk = _ek2 * (1 + _hk)
_nvk = _sk * (1 + _gz)
_fak = _nvk / _ek2
_disc_m = (90 - 60) / 90 * 100
_be = 3000 / 40

DEEP2 = {}

DEEP2["prozentrechner"] = f"""
<h2>Rechenweg für alle sechs Fragen des Rechners</h2>
<p>Der Rechner kennt sechs Fragestellungen. Hinter allen steckt dieselbe Beziehung W = G × p ÷ 100 – nur die Unbekannte wechselt:</p>
<table class="tbl text"><thead><tr><th>Frage im Rechner</th><th>Formel</th><th>Beispiel</th></tr></thead><tbody>
<tr><td>Wie viel sind x % von …?</td><td>W = G × p ÷ 100</td><td>12 % von 450 = {de(450*0.12)}</td></tr>
<tr><td>Wie viel Prozent sind …?</td><td>p = W ÷ G × 100</td><td>18 von 240 = {de(18/240*100)} %</td></tr>
<tr><td>Von welchem Wert sind es x %?</td><td>G = W ÷ p × 100</td><td>45 € sind 15 % von {eur(45/15*100)}</td></tr>
<tr><td>Veränderung in %</td><td>(neu − alt) ÷ alt × 100</td><td>1.250 → 1.400 = +{de(150/1250*100)} %</td></tr>
<tr><td>Preis nach Rabatt</td><td>G × (1 − p ÷ 100)</td><td>59,90 € − 25 % = {eur(59.90*0.75)}</td></tr>
<tr><td>Preis vor dem Rabatt</td><td>Endpreis ÷ (1 − p ÷ 100)</td><td>{eur(59.90*0.75)} ÷ 0,75 = {eur(59.90)}</td></tr>
</tbody></table>
<p>Ein Prozent ist ein Hundertstel, deshalb lässt sich jeder Prozentsatz auch als Dezimalzahl oder Bruch schreiben: 25 % = 0,25 = 1/4, 12,5 % = 0,125 = 1/8, 2,5 % = 0,025 = 1/40. Wer mit der Dezimalzahl rechnet, spart sich das „÷ 100“: 12 % von 450 sind 450 × 0,12.</p>
<h2>Promille: ein Zehntel Prozent</h2>
<p>Ein Promille (‰) ist ein Tausendstel, also 0,1 %. Promille begegnen dir bei Versicherungsprämien, bei Gebühren und beim Blutalkohol. 2,5 ‰ von 40.000 € sind 40.000 × 2,5 ÷ 1.000 = {eur(40000*2.5/1000)}. Im Prozentrechner gibst du dafür 0,25 % ein.</p>
<h2>Österreich und Deutschland: Prozent beim Wohnungskauf</h2>
<div class="example"><strong>Österreich:</strong> Beim Kauf einer Wohnung um 300.000 € fallen 3,5 % Grunderwerbsteuer an, also {eur(_grest)}, und für die Eintragung ins Grundbuch 1,1 % Eintragungsgebühr, also {eur(_ggb)}. Zusammen sind das {eur(_grest+_ggb)} oder {de((_grest+_ggb)/300000*100,1)} % des Kaufpreises – noch ohne Vertragserrichtung und Maklerprovision. Rechtsgrundlagen: § 7 Grunderwerbsteuergesetz 1987 und Tarifpost 9 Gerichtsgebührengesetz, abrufbar im {RIS} ({STAND}). Es gibt Ausnahmen, etwa einen Stufentarif bei Übertragungen in der Familie und zeitlich befristete Gebührenbefreiungen für Eigenheime – maßgeblich ist die Regel zum Zeitpunkt des Kaufs.</div>
<div class="example"><strong>Deutschland:</strong> Die Grunderwerbsteuer legt jedes Bundesland selbst fest; die Sätze reichen von 3,5 % bis 6,5 %. Bei 300.000 € macht das {" bis ".join(eur(v) for _, v in (_grest_de[0], _grest_de[2]))} aus – ein Unterschied von {eur(_grest_de[2][1]-_grest_de[0][1])} nur durch den Ort. Den aktuellen Satz nennt das Finanzministerium des jeweiligen Landes.</div>
<h2>Zinsen in Prozent und Prozentpunkten: Verzugszinsen</h2>
<p>Gesetzliche Verzugszinsen sind ein gutes Beispiel dafür, warum Prozent und Prozentpunkte auseinandergehalten werden müssen. In Deutschland beträgt der Verzugszins für Verbraucher <strong>5 Prozentpunkte über dem Basiszinssatz</strong> ({gii("bgb/__288.html", "§ 288 BGB")}, {STAND}). Liegt der Basiszinssatz angenommen bei 2 %, sind das 7 % pro Jahr. Für 30 Tage Verzug auf 1.000 € ergibt das 1.000 × 7 % × 30 ÷ 365 = {eur(_vz_de)}. Den jeweils gültigen Basiszinssatz veröffentlicht die Deutsche Bundesbank.</p>
<p>In Österreich betragen die gesetzlichen Zinsen zwischen Privatpersonen 4 % pro Jahr (§ 1000 ABGB, {RIS}). Für dieselben 30 Tage auf 1.000 € sind das {eur(_vz_at)}.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Prozentsätze addieren, deren Grundwerte verschieden sind:</strong> „20 % der Männer und 30 % der Frauen“ ergeben nicht 50 % aller Personen und auch nicht 25 % – das Ergebnis hängt davon ab, wie viele Männer und Frauen es gibt.</div>
<div class="warn"><strong>Komma falsch setzen:</strong> 0,5 % sind 0,005 und nicht 0,05. Bei Gebühren und Zinsen macht dieser Fehler den Betrag zehnmal so groß.</div>
<h2>Grenzen des Rechners</h2>
<p>Der Rechner rechnet mit bis zu vier Nachkommastellen und rundet erst bei der Anzeige. Für Zinsen über mehrere Jahre ist er nicht gedacht, weil sich dort der Grundwert jedes Jahr ändert – dafür gibt es den <a href="/zinseszins-rechner.html">Zinseszins-Rechner</a>. Mehrere Rabatte hintereinander rechnet der <a href="/rabatt-rechner.html">Rabatt-Rechner</a>.</p>
{faq([
("Wie rechne ich einen Prozentsatz ohne Taschenrechner?", "Über 10 % und 1 %: 10 % ist der Betrag mit verschobenem Komma, 1 % ein weiteres Komma. 17 % von 300 sind 30 + 7 × 3 = 51."),
("Was bedeutet „um 200 % gestiegen“?", "Der neue Wert ist dreimal so groß wie der alte: 100 → 300. „Auf 200 %“ heißt dagegen doppelt so groß."),
("Wie viel Prozent sind 3 von 7?", f"3 ÷ 7 × 100 = {de(3/7*100,2)} %. Der Rechner zeigt bis zu vier Nachkommastellen."),
])}
"""

DEEP2["mehrwertsteuer-rechner"] = f"""
<h2>Die Formeln für beide Richtungen</h2>
<p>Mit s als Steuersatz in Dezimalschreibweise (20 % = 0,2) gelten vier Beziehungen:</p>
<ul><li><strong>Steuer aus netto:</strong> Steuer = Netto × s</li>
<li><strong>Brutto aus netto:</strong> Brutto = Netto × (1 + s)</li>
<li><strong>Netto aus brutto:</strong> Netto = Brutto ÷ (1 + s)</li>
<li><strong>Steuer aus brutto:</strong> Steuer = Brutto × s ÷ (1 + s)</li></ul>
<p>Die vierte Formel ist praktisch, wenn nur die enthaltene Steuer gesucht ist: 89,90 € brutto mit 20 % enthalten 89,90 × 0,2 ÷ 1,2 = {eur(89.90*0.2/1.2)} Steuer.</p>
<h2>Durchgerechnet: eine Rechnung mit zwei Sätzen</h2>
<div class="example"><strong>Hotel in Deutschland:</strong> Für die Übernachtung gilt der ermäßigte Satz von 7 %; Leistungen, die nicht unmittelbar der Beherbergung dienen – etwa der Hotelparkplatz –, sind davon ausdrücklich ausgenommen ({gii("ustg_1980/__12.html", "§ 12 Abs. 2 Nr. 11 UStG")}, {STAND}) und kosten 19 %. Eine Rechnung über 98,00 € Übernachtung und 15,00 € Parkplatz enthält netto 98 ÷ 1,07 + 15 ÷ 1,19 = {eur(_h_de_n)} und {eur(_h_de_t)} Steuer. Wer die ganze Summe von 113,00 € mit 19 % herausrechnet, kommt auf {eur(113-113/1.19)} Steuer – zu viel, weil der größere Teil nur mit 7 % besteuert ist.</div>
<div class="example"><strong>Österreich:</strong> Auch hier gilt für die Beherbergung der ermäßigte Satz von 10 %, Getränke aus der Minibar werden dagegen meist mit 20 % abgerechnet. Die Rechnung muss die Beträge je Steuersatz getrennt ausweisen; zum Herausrechnen nimmst du jeden Block für sich.</div>
<h2>Kleinunternehmer: Rechnungen ohne Umsatzsteuer</h2>
<p>Kleine Unternehmen sind in beiden Ländern von der Umsatzsteuer befreit, solange ihr Umsatz unter einer Grenze bleibt. In Österreich liegt sie seit 2025 bei 55.000 € Bruttoumsatz im Jahr (§ 6 Abs. 1 Z 27 UStG 1994, {RIS}). In Deutschland darf der Umsatz im Vorjahr 25.000 € nicht überschritten haben und im laufenden Jahr 100.000 € nicht überschreiten ({gii("ustg_1980/__19.html", "§ 19 UStG")}, {STAND}). Auf solchen Rechnungen steht keine Steuer – der Rechnungsbetrag ist dann zugleich netto und brutto, und es gibt nichts herauszurechnen.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Hin- und Herrechnen mit gerundeten Zwischenwerten:</strong> 49,95 € brutto ergeben bei 20 % genau 41,625 € netto, gerundet {eur(round(49.95/1.2,2))}. Wer diesen gerundeten Wert wieder mit 1,2 malnimmt, erhält {eur(_rt)} statt 49,95 €. Der Rechner rechnet ungerundet weiter und rundet erst bei der Anzeige.</div>
<div class="warn"><strong>Netto- und Bruttopreise vergleichen:</strong> Angebote für Unternehmen nennen oft Nettopreise, Angebote für Privatkunden Bruttopreise. Ein „Angebot um 1.000 €“ kann deshalb 1.000 € oder 1.200 € bedeuten. Für Privatpersonen zählt immer der Bruttobetrag, denn sie können die Steuer nicht als Vorsteuer zurückholen.</div>
<h2>Grenzen des Rechners</h2>
<p>Der Rechner wendet einen Satz auf den ganzen Betrag an. Er prüft nicht, welcher Satz für eine Ware oder Leistung gilt, und kennt keine Sonderregeln wie die Umkehr der Steuerschuld bei bestimmten Leistungen zwischen Unternehmen. Für eigene Sätze, etwa aus einem anderen EU-Land, wähle „eigener Satz“.</p>
{faq([
("Ist Mehrwertsteuer dasselbe wie Umsatzsteuer?", "Ja. Im Gesetz heißt sie in beiden Ländern Umsatzsteuer, im Alltag sagt man meist Mehrwertsteuer."),
("Wie viel Steuer steckt in 1.000 € brutto bei 19 %?", f"1.000 × 0,19 ÷ 1,19 = {eur(1000*0.19/1.19)}."),
("Kann ich den Rechner für die Schweiz verwenden?", "Ja, mit „eigener Satz“. Die Schweizer Sätze sind niedriger als in Österreich und Deutschland; den aktuellen Satz nennt die Eidgenössische Steuerverwaltung."),
])}
"""

DEEP2["rabatt-rechner"] = f"""
<h2>Die Formel für den Gesamtrabatt</h2>
<p>Der Rechner multipliziert die Anteile, die nach jedem Abzug übrig bleiben. Allgemein gilt: <strong>Gesamtrabatt = 1 − (1 − r₁) × (1 − r₂) × (1 − s)</strong>, wobei r₁ und r₂ die Rabatte und s das Skonto als Dezimalzahl sind. Ein Rechenweg mit drei Abzügen:</p>
<div class="example"><strong>Fahrrad um 1.299 €:</strong> 15 % Aktionsrabatt, danach 3 % Skonto bei Barzahlung. 1.299 × 0,85 = {eur(1299*0.85)}; × 0,97 = {eur(_bike)}. Ersparnis: {eur(1299-_bike)} oder {de((1-_bike/1299)*100)} % – nicht 18 %.</div>
<h2>Rückwärts: Welcher Rabatt fehlt bis zum Wunschpreis?</h2>
<p>Ein Fernseher kostet 899 €, du willst höchstens 699 € zahlen. Der nötige Rabatt ist 1 − 699 ÷ 899 = {de(_need*100,1)} %. Bietet der Händler schon 10 %, fehlt noch ein zweiter Rabatt von 1 − 699 ÷ (899 × 0,9) = {de((1-699/(899*0.9))*100,1)} %. Mit diesen Zahlen kannst du gezielt verhandeln, statt pauschal „noch etwas mehr“ zu verlangen.</p>
<h2>Streichpreise in Österreich und Deutschland</h2>
<p>Ein Rabatt ist nur so viel wert wie der Preis, von dem er abgezogen wird. Seit 2022 gilt in beiden Ländern eine EU-Vorgabe (Richtlinie (EU) 2019/2161): Wer eine Preisermäßigung für eine Ware bekanntgibt, muss als Vergleichspreis den niedrigsten Preis der letzten 30 Tage vor der Ermäßigung nennen. In Österreich steht die Regel im Preisauszeichnungsgesetz (§ 9a PrAG, {RIS}), in Deutschland in der Preisangabenverordnung – Details dazu im Ratgeber <a href="/rabatte-kombinieren.html">Rabatte kombinieren</a>. Für den Rechner heißt das: Trag als Preis den Vergleichspreis ein, den der Händler nennt, nicht eine unverbindliche Preisempfehlung.</p>
<h2>Euro-Beträge in Prozent umrechnen</h2>
<p>Der Rechner arbeitet mit Prozent-Rabatten. Einen festen Betrag rechnest du vorher um: 30 € Nachlass auf 240 € sind 30 ÷ 240 × 100 = {de(30/240*100)} %. Achtung: Der Prozentwert gilt nur für diesen einen Preis. Bei einem zweiten Rabatt danach muss der Euro-Betrag an der richtigen Stelle stehen – sonst ändert sich das Ergebnis, wie oben im Abschnitt zu Euro- und Prozent-Rabatt gezeigt.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Skonto vom Listenpreis rechnen:</strong> Skonto bezieht sich auf den Rechnungsbetrag, also auf den Preis nach allen Rabatten. 3 % Skonto auf 1.299 € wären {eur(1299*0.03)}, tatsächlich sind es nur 3 % von {eur(1299*0.85)} = {eur(1299*0.85*0.03)}.</div>
<div class="warn"><strong>Ersparnis mit Ausgabe verwechseln:</strong> „Spare 150 €“ heißt nicht, dass 150 € übrig bleiben, sondern dass du weniger ausgibst als zum Vergleichspreis – sinnvoll nur, wenn du den Artikel ohnehin gekauft hättest.</div>
<h2>Grenzen des Rechners</h2>
<p>Der Rechner kennt zwei Prozent-Rabatte und ein Skonto. Mengenaktionen wie „3 zum Preis von 2“, Gutscheine in Euro und Versandkosten musst du selbst umrechnen. Ob dir Skonto zusteht, steht auf der Rechnung oder in den Zahlungsbedingungen; einen allgemeinen Anspruch darauf gibt es nicht. Ob sich Skonto lohnt, wenn du dafür Geld leihen müsstest, zeigt der Ratgeber <a href="/skonto-oder-ratenzahlung.html">Skonto oder Ratenzahlung</a>.</p>
{faq([
("Wie berechne ich den Rabatt aus altem und neuem Preis?", f"(alt − neu) ÷ alt × 100. Von 129 € auf 99 € sind es {de(30/129*100,1)} %."),
("Darf ich mehrere Rabatte addieren, wenn sie klein sind?", "Als grobe Schätzung ja: 3 % + 2 % ergeben genau 4,94 %, also fast 5 %. Bei großen Rabatten wird der Fehler schnell erheblich."),
("Was ist der Unterschied zwischen Rabatt und Skonto?", "Ein Rabatt ist ein Preisnachlass, zum Beispiel für eine Aktion oder Menge. Skonto ist ein Abzug für schnelles Bezahlen innerhalb einer Frist."),
])}
"""

DEEP2["zinseszins-rechner"] = f"""
<h2>Die Formel hinter dem Sparplan</h2>
<p>Für eine monatliche Sparrate R, den Monatszins i (Jahreszins ÷ 12) und n Monate gilt bei Einzahlung am Monatsende:</p>
<p class="formula">Endwert = K₀ × (1 + i)ⁿ + R × ((1 + i)ⁿ − 1) ÷ i</p>
<div class="example"><strong>Nachgerechnet:</strong> 100 € im Monat, 3 % p. a., 20 Jahre. i = 0,03 ÷ 12 = 0,0025, n = 240. (1,0025)²⁴⁰ = {de((1+_i3)**240,4)}. Endwert = 100 × ({de((1+_i3)**240,4)} − 1) ÷ 0,0025 = {eur(_z_formula)} – genau der Betrag, den der Rechner Monat für Monat ermittelt.</div>
<h2>Früh anfangen oder mehr sparen?</h2>
<div class="example">Zwei Personen sparen bis 65 jeweils 150 € im Monat bei angenommenen 4 % p. a. Wer mit 25 beginnt (40 Jahre), hat am Ende {eur(_early)}, eingezahlt sind {eur(150*480)}. Wer mit 35 beginnt (30 Jahre), hat {eur(_late)} bei {eur(150*360)} Einzahlung. Um mit 35 noch auf dasselbe Endkapital zu kommen, wären rund {eur(_late_eq)} im Monat nötig.</div>
<p>Die zehn zusätzlichen Jahre bringen mehr als die zusätzlichen Einzahlungen, weil die frühen Raten am längsten verzinst werden. Bei schwankenden Anlagen wie Aktienfonds ist das ein Szenario, keine Zusage.</p>
<h2>Kosten wirken ebenfalls mit Zinseszins</h2>
<p>Laufende Kosten werden jedes Jahr vom Vermögen abgezogen und schmälern damit auch künftige Erträge. 200 € im Monat über 25 Jahre ergeben bei 6 % {eur(_ter_a)}, bei 5 % – also nach einem Prozentpunkt Kosten – {eur(_ter_b)}. Der Unterschied von {eur(_ter_a-_ter_b)} ist größer als ein Viertel der gesamten Einzahlungen von {eur(200*300)}. Trag deshalb für Fonds die erwartete Rendite <em>nach</em> Kosten ein.</p>
<h2>Österreich und Deutschland: Einlagensicherung</h2>
<p>Guthaben auf Sparbuch, Tages- und Festgeld sind in beiden Ländern durch die gesetzliche Einlagensicherung bis 100.000 € pro Person und Bank geschützt. Grundlage ist eine EU-Richtlinie, umgesetzt in Österreich im Einlagensicherungs- und Anlegerentschädigungsgesetz (ESAEG, {RIS}) und in Deutschland im {gii("einsig/__8.html", "Einlagensicherungsgesetz, § 8")} ({STAND}). Für Fonds und Aktien gilt diese Sicherung nicht; sie sind als Sondervermögen bzw. im Depot getrennt vom Vermögen der Bank verwahrt, können aber an Wert verlieren.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Einzahlungszeitpunkt übersehen:</strong> Der Rechner bucht die Rate am Monatsende. Wird am Monatsanfang eingezahlt, verzinst sich jede Rate einen Monat länger: Aus {eur(_z_end)} werden {eur(_z_start)}. Vergleiche Angebote deshalb immer mit derselben Annahme.</div>
<div class="warn"><strong>Endkapital mit Kaufkraft verwechseln:</strong> {eur(_z_end)} in 20 Jahren sind nominal gerechnet. Was davon real bleibt, zeigt der Ratgeber <a href="/realzins-sparen-inflation.html">Inflation und Kaufkraft</a>.</div>
<h2>Grenzen des Rechners</h2>
<p>Der Rechner nimmt einen festen Zinssatz über die ganze Laufzeit an und rechnet ohne Steuern und Kosten. Die Laufzeit muss ganze Monate ergeben (bis 80 Jahre). Für Entnahmepläne, steigende Sparraten oder Zinsänderungen ist er nicht ausgelegt.</p>
{faq([
("Was ist der Unterschied zwischen Zins und Zinseszins?", "Zins wird nur auf das eingezahlte Kapital gezahlt. Beim Zinseszins bleiben die Zinsen angelegt und werden in den Folgeperioden mitverzinst."),
("Kann ich auch eine Einmalanlage ohne Sparrate rechnen?", "Ja: Startkapital eintragen und die Sparrate auf 0 setzen. Dann gilt die einfache Formel K₀ × (1 + i)ⁿ."),
("Welcher Zinssatz ist realistisch?", "Für Spareinlagen den Zins, den deine Bank aktuell bietet. Für Fonds gibt es keinen festen Satz – rechne mehrere Szenarien, etwa vorsichtig und optimistisch."),
])}
"""

DEEP2["kreditrechner"] = f"""
<h2>Rechenweg der ersten Raten</h2>
<p>Für 20.000 € zu 4,5 % auf 5 Jahre ist der Monatszins 4,5 % ÷ 12 = 0,375 %. Die Rate von {eur(_ka)} teilt sich jeden Monat in Zinsen auf die Restschuld und Tilgung:</p>
<table class="tbl"><thead><tr><th>Monat</th><th>Zinsen</th><th>Tilgung</th><th>Restschuld</th></tr></thead><tbody>
{''.join(f'<tr><td>{k}</td><td>{eur(z)}</td><td>{eur(t)}</td><td>{eur(r)}</td></tr>' for k, z, t, r in _rows)}
</tbody></table>
<p>Im ersten Monat sind es 20.000 × 0,375 % = {eur(_rows[0][1])} Zinsen, der Rest von {eur(_rows[0][2])} tilgt. Weil die Restschuld sinkt, wird der Zinsanteil jeden Monat ein wenig kleiner und die Tilgung entsprechend größer.</p>
<h2>Österreich und Deutschland: Rechte bei Verbraucherkrediten</h2>
<ul><li><strong>Vorvertragliche Information:</strong> Vor Vertragsabschluss erhältst du in beiden Ländern ein standardisiertes Formular („Europäische Standardinformationen für Verbraucherkredite“) mit Sollzins, effektivem Jahreszins, Gesamtbetrag und Laufzeit. Damit lassen sich die Werte aus diesem Rechner direkt vergleichen.</li>
<li><strong>Rücktritt:</strong> Vom abgeschlossenen Kreditvertrag kannst du innerhalb von 14 Tagen ohne Angabe von Gründen zurücktreten bzw. ihn widerrufen – in Österreich nach § 12 Verbraucherkreditgesetz ({RIS}), in Deutschland nach {gii("bgb/__495.html", "§ 495 BGB")} ({STAND}).</li>
<li><strong>Vorzeitige Rückzahlung:</strong> Ein Verbraucherkredit darf jederzeit ganz oder teilweise vorzeitig zurückgezahlt werden; bei fixem Zinssatz kann die Bank eine begrenzte Entschädigung verlangen. Wie viel Zinsen eine Extrazahlung spart, rechnet der Ratgeber <a href="/kredit-sondertilgung.html">Kredit mit Sondertilgung</a> durch.</li></ul>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Zinsen wie beim Sparbuch rechnen:</strong> 20.000 € × 4,5 % × 5 Jahre = {eur(_simple)} – so viel Zinsen fallen nicht an. Weil du laufend tilgst, sind es tatsächlich nur {eur(_true_int)}. Die einfache Rechnung unterstellt, dass die volle Summe fünf Jahre lang geschuldet wird.</div>
<div class="warn"><strong>Effektivzins in den Rechner eintragen:</strong> Mit dem Effektivzins wird die Rate zu hoch, weil Gebühren dann doppelt zählen würden – einmal im Zins und einmal im Kreditbetrag. Trag den Sollzins ein und vergleiche Angebote über den Effektivzins.</div>
<h2>Grenzen des Rechners</h2>
<p>Der Rechner geht von gleichen Monatsraten, einem festen Sollzins und monatlicher Zinsverrechnung aus. Bearbeitungsgebühren, Kontoführung, Restschuldversicherung, Zinsänderungen bei variablen Krediten und tilgungsfreie Anlaufmonate sind nicht enthalten. In echten Tilgungsplänen ist die letzte Rate wegen Rundung oft ein paar Cent anders.</p>
{faq([
("Wie viel Kredit kann ich mir leisten?", "Rechne die Rate aus und prüfe sie gegen dein Haushaltsbudget nach allen Fixkosten. Plane einen Puffer für unerwartete Ausgaben ein – die Bank prüft deine Kreditwürdigkeit ohnehin, aber ihre Prüfung ersetzt nicht deine eigene."),
("Warum ist die Rate bei 0 % Zins nicht null?", f"Weil du den Kredit trotzdem tilgen musst: 20.000 € auf 60 Monate sind {eur(20000/60)} im Monat."),
("Kann ich auch eine Laufzeit in halben Jahren eingeben?", "Ja. Der Rechner rechnet die Jahre in Monate um, 2,5 Jahre ergeben 30 Raten."),
("Was tun, wenn eine Rate nicht bezahlt werden kann?", "Möglichst früh mit der Bank sprechen. Häufig lassen sich Stundungen oder eine Verlängerung der Laufzeit vereinbaren – das kostet zusätzliche Zinsen, ist aber meist günstiger als Verzugszinsen und Mahngebühren."),
("Gilt der Rechner auch für Wohnkredite?", "Für die Rate ja, wenn Zinssatz und Laufzeit bekannt sind. Bei Wohnkrediten kommen aber oft Gebühren, Zinsbindungsfristen und Sondertilgungsrechte dazu, die der Rechner nicht abbildet."),
])}
"""

DEEP2["dreisatz-rechner"] = f"""
<h2>Der Dreisatz als Verhältnisgleichung</h2>
<p>Die drei Sätze lassen sich zu einer einzigen Gleichung zusammenfassen. Proportional gilt b ÷ a = x ÷ c, also <strong>x = b × c ÷ a</strong>. Umgekehrt proportional bleibt das Produkt gleich: a × b = c × x, also <strong>x = a × b ÷ c</strong>. Der Rechner zeigt trotzdem den Weg über die Einheit („auf eins“), weil er sich leichter kontrollieren lässt.</p>
<h2>Durchgerechnete Beispiele aus dem Alltag</h2>
<div class="example"><strong>Wandfarbe:</strong> 10 Liter reichen laut Eimer für 34 m², du hast 2,5 Liter. 34 ÷ 10 = 3,4 m² pro Liter; × 2,5 = {de(_paint)} m².</div>
<div class="example"><strong>Akku:</strong> Ein Akku-Rasenmäher schafft mit einer Ladung 400 m² in 50 Minuten. Für 650 m² braucht er 50 ÷ 400 × 650 = {de(50/400*650,2)} Minuten – wenn der Rasen gleich dicht ist.</div>
<div class="example"><strong>Umgekehrt proportional:</strong> Mit 6 Raten zu 250 € ist ein Betrag in einem halben Jahr bezahlt. Mit 4 Raten muss jede Rate 6 × 250 ÷ 4 = {eur(6*250/4)} betragen.</div>
<h2>Österreich und Deutschland: Grundpreise vergleichen</h2>
<p>Im Supermarkt ist der Dreisatz schon erledigt: Händler müssen neben dem Verkaufspreis den <strong>Grundpreis</strong> angeben, also den Preis je Kilogramm oder Liter. Die Pflicht stammt aus der EU-Preisangabenrichtlinie 98/6/EG und gilt deshalb in beiden Ländern – in Deutschland geregelt in {gii("pangv_2022/__4.html", "§ 4 Preisangabenverordnung")} ({STAND}), in Österreich im Preisauszeichnungsgesetz ({RIS}).</p>
<div class="example">Kaffee A: 400 g um 2,79 €. Kaffee B: 1 kg um 6,49 €. Dreisatz für A: 2,79 ÷ 400 × 1.000 = {eur(_kg_a)} pro kg. B ist also um {eur(_kg_a-_kg_b)} pro Kilogramm günstiger – obwohl die Packung mehr als doppelt so viel kostet.</div>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Richtung verwechseln:</strong> Mehr Arbeiter, weniger Zeit – das ist umgekehrt proportional. Wer hier proportional rechnet, bekommt für 8 statt 4 Maler 12 statt 3 Tage heraus. Prüfe das Ergebnis immer mit dem gesunden Menschenverstand: Muss es größer oder kleiner werden?</div>
<div class="warn"><strong>Früh runden:</strong> 7 Stück kosten 10 €. Wer den Stückpreis auf 1,43 € rundet, erhält für 50 Stück 71,50 € statt {eur(10/7*50)}. Der Rechner rechnet mit sechs Nachkommastellen weiter.</div>
<h2>Grenzen des Rechners</h2>
<p>Der Rechner löst einfache Dreisätze mit genau drei bekannten Werten. Für den doppelten Dreisatz rechnest du zweimal hintereinander. Zusammenhänge mit Grundgebühr, Staffelpreisen oder Mengenrabatt sind nicht proportional – dafür ist eine eigene Rechnung nötig.</p>
{faq([
("Woran erkenne ich, ob ich proportional oder umgekehrt rechnen muss?", "Frag dich, was passiert, wenn sich die erste Größe verdoppelt. Verdoppelt sich die zweite mit, ist es proportional. Halbiert sie sich, ist es umgekehrt proportional."),
("Kann ein Wert im Dreisatz 0 sein?", "Der erste Wert nicht, weil durch ihn geteilt wird. Beim umgekehrten Dreisatz darf auch der dritte Wert nicht 0 sein."),
("Ist Prozentrechnung auch ein Dreisatz?", "Ja. 100 % entsprechen dem Grundwert, daraus rechnest du auf 1 % und dann auf den gesuchten Prozentsatz."),
("Kann ich mit dem Dreisatz einen Preis vor einer Erhöhung berechnen?", f"Ja. Kostet etwas nach 8 % Erhöhung 54 €, entsprechen 108 % 54 €. Auf 1 %: 54 ÷ 108 = 0,5 €; auf 100 %: 50 €. Im Rechner: 108 → 54, gesucht 100."),
])}
"""

DEEP2["bruchrechner"] = f"""
<h2>Kürzen mit dem größten gemeinsamen Teiler</h2>
<p>Der Rechner kürzt jedes Ergebnis vollständig. Dafür sucht er den größten gemeinsamen Teiler (ggT) mit dem euklidischen Verfahren: Man teilt die größere Zahl durch die kleinere und rechnet mit dem Rest weiter, bis kein Rest mehr bleibt.</p>
<div class="example"><strong>84/126 kürzen:</strong> 126 ÷ 84 = 1 Rest 42. 84 ÷ 42 = 2 Rest 0. Der ggT ist 42, also 84/126 = 2/3.</div>
<p>Das kleinste gemeinsame Vielfache, das der Rechner beim Addieren als Nenner verwendet, folgt daraus: kgV(a, b) = a × b ÷ ggT(a, b). Für 4 und 6 ist das 24 ÷ 2 = 12.</p>
<h2>Gemischte Zahlen</h2>
<p>Eine gemischte Zahl wie 2 ¾ trägst du als unechten Bruch ein: Ganze mal Nenner plus Zähler, also 2 × 4 + 3 = 11, ergibt 11/4. Das Ergebnis zeigt der Rechner wieder als gemischte Zahl, wenn es größer als 1 ist.</p>
<div class="example"><strong>2 ¾ × 1 ⅓:</strong> 11/4 × 4/3 = 44/12 = 11/3 = 3 ⅔. Falsch wäre es, Ganze und Brüche getrennt zu multiplizieren: 2 × 1 und ¾ × ⅓ ergäbe 2 ¼.</div>
<h2>Brüche vergleichen</h2>
<p>Welcher Bruch ist größer, 5/8 oder 3/5? Über Kreuz multiplizieren: 5 × 5 = 25 und 3 × 8 = 24. Weil 25 größer ist, ist 5/8 größer. Kontrolle als Dezimalzahl: 5/8 = 0,625, 3/5 = 0,6.</p>
<h2>Österreich und Deutschland: Brüche im Erbrecht</h2>
<p>Das gesetzliche Erbrecht verteilt Anteile als Brüche – ein Bereich, in dem Bruchrechnen ganz praktisch wird. Die folgenden Beispiele zeigen nur den einfachsten Fall ohne Testament.</p>
<div class="example"><strong>Österreich:</strong> Neben Kindern erbt der Ehegatte 1/3 (§ 744 ABGB, {RIS}). Hinterlässt jemand Ehegatten und zwei Kinder, teilen sich die Kinder die übrigen 2/3: 2/3 ÷ 2 = 1/3 für jedes Kind.</div>
<div class="example"><strong>Deutschland:</strong> Der Ehegatte erbt neben Kindern 1/4 ({gii("bgb/__1931.html", "§ 1931 BGB")}). Lebten die Eheleute im gesetzlichen Güterstand, erhöht sich der Anteil um ein weiteres Viertel ({gii("bgb/__1371.html", "§ 1371 BGB")}, {STAND}): 1/4 + 1/4 = 1/2. Bei zwei Kindern erhält jedes (1 − 1/2) ÷ 2 = 1/4.</div>
<p class="small muted">Vereinfachte Rechenbeispiele, keine Rechtsauskunft. Testamente, Pflichtteile und weitere Angehörige ändern die Anteile; im Einzelfall helfen Notariat oder Rechtsanwalt.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Zähler und Nenner getrennt addieren:</strong> 1/2 + 1/3 ist nicht 2/5. Richtig: 3/6 + 2/6 = 5/6. Schon die Größe verrät den Fehler: 2/5 ist kleiner als 1/2, obwohl etwas dazukommt.</div>
<div class="warn"><strong>Aus Summen kürzen:</strong> In (3 + 6)/6 darf man nicht die 6 wegstreichen. Erst zusammenrechnen: 9/6 = 3/2. Kürzen ist nur bei Faktoren erlaubt, nicht bei Summanden.</div>
<h2>Grenzen des Rechners</h2>
<p>Der Rechner verarbeitet ganze Zahlen in Zähler und Nenner, auch negative. Gemischte Zahlen und Dezimalbrüche musst du vorher umwandeln (0,25 = 1/4). Er rechnet immer zwei Brüche mit einer Rechenart; längere Ausdrücke löst du Schritt für Schritt.</p>
{faq([
("Wie wandle ich eine Dezimalzahl in einen Bruch um?", "Über die Stellen: 0,35 sind 35 Hundertstel, also 35/100, gekürzt 7/20."),
("Was ist ein Kehrwert?", "Der Bruch mit vertauschtem Zähler und Nenner. Der Kehrwert von 3/7 ist 7/3, der von 5 ist 1/5."),
("Warum zeigt der Rechner manchmal eine ganze Zahl?", "Wenn sich der Nenner auf 1 kürzen lässt: 6/3 = 2/1 = 2."),
("Wie rechne ich einen Bruch in Prozent um?", "Zähler durch Nenner teilen und mal 100 nehmen: 3/8 = 0,375 = 37,5 %. Umgekehrt ist 40 % = 40/100 = 2/5."),
("Was ist ein Doppelbruch?", "Ein Bruch, dessen Zähler oder Nenner selbst ein Bruch ist, etwa (3/4) ÷ (5/6). Er wird wie eine Division gerechnet: 3/4 × 6/5 = 18/20 = 9/10."),
])}
"""

DEEP2["stromkosten-rechner"] = f"""
<h2>Rechenweg mit den Startwerten</h2>
<div class="example"><strong>Fernseher, 100 W, 4 Stunden täglich:</strong> 100 × 4 ÷ 1.000 = 0,4 kWh pro Tag. × 365 = {de(_tv_kwh,1)} kWh im Jahr. × 0,30 € = {eur(_tv_kwh*0.30)} im Jahr oder {eur(_tv_kwh*0.30/12)} im Monat. Eine Betriebsstunde kostet 0,1 kWh × 0,30 € = 3 Cent.</div>
<h2>Leistung oder Energie? Watt und Kilowattstunde</h2>
<p>Watt (W) und Kilowatt (kW) geben die <strong>Leistung</strong> an – wie viel ein Gerät in diesem Moment zieht. Kilowattstunden (kWh) sind die <strong>Energie</strong> – Leistung mal Zeit. Ein Heizlüfter mit 2 kW verbraucht in einer Stunde 2 kWh, in einer halben Stunde 1 kWh. Steht auf dem Typenschild nur die Stromstärke in Ampere, hilft die Formel Leistung = Spannung × Strom: Bei 230 V Netzspannung und 8,7 A sind das {de(_amp_w,0)} W. Für Geräte mit Motor oder Netzteil ist das nur eine Obergrenze.</p>
<h2>Altes Gerät tauschen: lohnt sich das?</h2>
<div class="example"><strong>Kühlschrank:</strong> Das alte Gerät verbraucht laut Messgerät 300 kWh im Jahr, ein neues laut Energielabel 150 kWh. Ersparnis bei 30 Cent: (300 − 150) × 0,30 = {eur(_fr_save)} im Jahr. Kostet das neue Gerät 600 €, hat es sich nach rund {de(600/_fr_save,1)} Jahren über den Strom bezahlt gemacht – vorausgesetzt, der Strompreis bleibt gleich.</div>
<div class="example"><strong>Waschmaschine:</strong> Das Label nennt den Verbrauch für 100 Waschgänge im Eco-Programm, zum Beispiel 55 kWh. Bei 200 Waschgängen im Jahr sind das {de(_wm,0)} kWh oder {eur(_wm*0.30)}. Heiße Programme brauchen deutlich mehr, weil der größte Teil der Energie in das Aufheizen des Wassers geht.</div>
<h2>Österreich und Deutschland: Energielabel und Strompreis</h2>
<p>Seit März 2021 gilt für Kühlgeräte, Waschmaschinen, Geschirrspüler und Bildschirme in der ganzen EU eine neue Skala von A bis G ohne „A+++“ (Verordnung (EU) 2017/1369). Ein Gerät mit „A+++“ von früher entspricht deshalb nicht automatisch einem heutigen „A“ – vergleiche den kWh-Wert, nicht die Klasse. Den Arbeitspreis deines Vertrags findest du auf der Stromrechnung. Zum Vergleich von Tarifen bietet in Österreich die Regulierungsbehörde <a href="https://www.e-control.at" rel="noopener">E-Control</a> einen amtlichen Tarifkalkulator; in Deutschland informiert die <a href="https://www.bundesnetzagentur.de" rel="noopener">Bundesnetzagentur</a> über Strompreise und Anbieterwechsel ({STAND}). Wie Grundgebühr und Arbeitspreis zusammenspielen, zeigt der Ratgeber <a href="/stromtarife-vergleichen.html">Stromtarife vergleichen</a>.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Höchstleistung für den Dauerbetrieb ansetzen:</strong> Ein Gaming-PC mit 750-W-Netzteil zieht beim Surfen oft nur einen Bruchteil davon. Wer mit 750 W rechnet, überschätzt die Kosten stark. Ein Messgerät an der Steckdose zeigt den echten Verbrauch.</div>
<div class="warn"><strong>Cent und Euro verwechseln:</strong> Der Rechner erwartet den Preis in Cent pro kWh. Wer 0,30 statt 30 einträgt, bekommt ein hundertmal zu kleines Ergebnis.</div>
<h2>Grenzen des Rechners</h2>
<p>Der Rechner nimmt eine gleichbleibende Leistung an. Geräte mit wechselnder Last – Kühlschrank, Wärmepumpe, Klimagerät – bildet er nur über den Jahresverbrauch ab. Für eine Wärmepumpe brauchst du statt der Wattzahl den Wärmebedarf und die Jahresarbeitszahl; das erklärt der Ratgeber <a href="/waermepumpe-stromkosten.html">Stromkosten einer Wärmepumpe abschätzen</a>.</p>
{faq([
("Wie viel kostet eine Kilowattstunde?", "Das hängt vom Vertrag ab. Maßgeblich ist der Arbeitspreis brutto auf deiner Rechnung; die Grundgebühr zählt für ein einzelnes Gerät nicht."),
("Wie viel Strom braucht ein Haushalt im Jahr?", "Das schwankt stark mit Personenzahl, Warmwasserbereitung und Geräten. Deinen eigenen Wert findest du auf der Jahresabrechnung – er ist für Vergleiche aussagekräftiger als jeder Durchschnitt."),
("Wie rechne ich die Kosten pro Waschgang oder Spülgang aus?", f"Verbrauch laut Label für 100 Durchläufe durch 100 teilen und mit dem Preis malnehmen: 55 kWh ÷ 100 = 0,55 kWh, bei 30 Cent also {de(0.55*30,1)} Cent pro Waschgang."),
])}
"""

DEEP2["aufschlag-marge-rechner"] = f"""
<h2>Vom Einkaufspreis zum Verkaufspreis: das Kalkulationsschema</h2>
<p>Im Handel wird der Verkaufspreis meist in festen Schritten kalkuliert. Ein Beispiel mit einem Einkaufspreis von {eur(_ek2)} netto, 35 % Handlungskosten (Miete, Personal, Verwaltung) und 12 % Gewinnzuschlag:</p>
<table class="tbl text"><tbody>
<tr><td>Einkaufspreis netto</td><td>{eur(_ek2)}</td></tr>
<tr><td>+ 35 % Handlungskosten</td><td>{eur(_ek2*_hk)}</td></tr>
<tr><td>= Selbstkosten</td><td>{eur(_sk)}</td></tr>
<tr><td>+ 12 % Gewinn auf die Selbstkosten</td><td>{eur(_sk*_gz)}</td></tr>
<tr><td>= Verkaufspreis netto</td><td>{eur(_nvk)}</td></tr>
<tr><td>+ 20 % USt (Österreich)</td><td>{eur(_nvk*1.2)} brutto</td></tr>
<tr><td>+ 19 % USt (Deutschland)</td><td>{eur(_nvk*1.19)} brutto</td></tr></tbody></table>
<p>Der gesamte Kalkulationsaufschlag beträgt ({eur(_nvk)} − {eur(_ek2)}) ÷ {eur(_ek2)} = {de((_fak-1)*100,1)} %, der <strong>Kalkulationsfaktor</strong> {de(_fak,3)}: Einkaufspreis mal Faktor ergibt den Nettoverkaufspreis. Die Handelsspanne liegt bei {de((_nvk-_ek2)/_nvk*100,1)} %. Diese Werte zeigt der Rechner, wenn du {eur(_ek2)} und {eur(_nvk)} einträgst.</p>
<h2>Was ein Rabatt mit der Marge macht</h2>
<div class="example">Ein Artikel kostet im Einkauf 60 € und im Verkauf 100 € netto – 40 % Marge. Gibst du 10 % Rabatt, sinkt der Preis auf 90 €, der Rohgewinn aber von 40 € auf 30 €. Die Marge fällt auf {de(_disc_m,1)} %, der Rohgewinn um ein Viertel. Um denselben Rohgewinn wie vorher zu erzielen, müsstest du {de(40/30,2)}-mal so viel verkaufen, also ein Drittel mehr Stück.</div>
<p>Je kleiner die Marge, desto stärker wirkt jeder Rabatt. Bei 20 % Marge frisst ein Rabatt von 10 % die Hälfte des Rohgewinns.</p>
<h2>Deckungsbeitrag und Gewinnschwelle</h2>
<p>Der Rohgewinn pro Stück heißt in der Kostenrechnung <strong>Deckungsbeitrag</strong>: Er deckt zuerst die Fixkosten. Liegen die Fixkosten bei 3.000 € im Monat und bringt jedes Stück 40 € Deckungsbeitrag, ist die Gewinnschwelle bei 3.000 ÷ 40 = {de(_be,0)} Stück erreicht. Erst ab dem {de(_be+1,0)}. Stück entsteht Gewinn.</p>
<h2>Österreich und Deutschland: Kleinunternehmer kalkulieren anders</h2>
<p>Wer als Kleinunternehmer keine Umsatzsteuer verrechnet, kann sich die Vorsteuer aus dem Einkauf auch nicht zurückholen. Für die Kalkulation ist der Einkaufspreis dann der <em>Bruttopreis</em>, und der Verkaufspreis ist zugleich der Endpreis. Ab welchem Umsatz die Befreiung endet, steht beim <a href="/mehrwertsteuer-rechner.html">Mehrwertsteuer-Rechner</a>. Im Rechner wählst du dafür „ohne“ Umsatzsteuer.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Mit Bruttopreisen kalkulieren:</strong> Wer als umsatzsteuerpflichtiges Unternehmen den Bruttoverkaufspreis mit dem Nettoeinkauf vergleicht, rechnet sich die Marge schön: Die Umsatzsteuer gehört dem Finanzamt.</div>
<div class="warn"><strong>Gewinnzuschlag auf den Einkaufspreis statt auf die Selbstkosten:</strong> 12 % auf {eur(_ek2)} sind {eur(_ek2*0.12)}, 12 % auf {eur(_sk)} aber {eur(_sk*_gz)}. Welche Basis gilt, muss in der eigenen Kalkulation einheitlich festgelegt sein.</div>
<h2>Grenzen des Rechners</h2>
<p>Der Rechner rechnet mit einem Einkaufs- und einem Verkaufspreis. Handlungskosten, Mengenrabatte im Einkauf, Retourenquoten und Zahlungsgebühren musst du selbst einrechnen – am einfachsten, indem du sie zum Einkaufspreis addierst. Eine Kostenrechnung für den ganzen Betrieb ersetzt er nicht.</p>
{faq([
("Was ist eine gute Handelsspanne?", "Das hängt stark von der Branche ab. Entscheidend ist, ob nach Abzug aller Kosten ein Gewinn bleibt – rechne die Gewinnschwelle wie oben aus."),
("Wie rechne ich Marge in Aufschlag um?", f"Aufschlag = Marge ÷ (1 − Marge). 30 % Marge entsprechen {de(0.3/0.7*100,1)} % Aufschlag."),
("Kann die Marge über 100 % liegen?", "Nein. Die Marge bezieht sich auf den Verkaufspreis, und der Gewinn kann nicht größer sein als der Preis. Der Aufschlag dagegen kann beliebig groß werden."),
])}
"""


# ---------- Ergänzungen (eingefügt vor „Typische Fehler“ der jeweiligen Seite)
_shop_b = 49.90
_shop_n = _shop_b / 1.2
_shop_fee = _shop_b * 0.015 + 0.25
_shop_ship = 4.90 / 1.2
_shop_ek = 22.00
_shop_g = _shop_n - _shop_ek - _shop_fee - _shop_ship
_rate_tbl = [(p, _annuity(20000, p, 60)) for p in (3.0, 4.5, 6.0, 8.0)]
_goal = [(p, 10000 * (p / 1200) / ((1 + p / 1200) ** 60 - 1) if p else 10000 / 60) for p in (0, 2, 4)]
_abo = 14.99
_abo_save = 3 * _abo * 0.5
_fx = 0.85

_ADD = {
"aufschlag-marge-rechner": f"""
<h2>Durchgerechnet: Was im Onlineshop von 49,90 € bleibt</h2>
<div class="example">Ein Artikel kostet im Shop {eur(_shop_b)} brutto (Österreich, 20 % USt), der Einkauf {eur(_shop_ek)} netto. Netto bleiben {eur(_shop_b)} ÷ 1,2 = {eur(_shop_n)}. Der Zahlungsanbieter verlangt angenommen 1,5 % vom Bruttobetrag plus 0,25 €, also {eur(_shop_fee)}; den Versand von 4,90 € brutto trägt der Shop selbst ({eur(_shop_ship)} netto). Rohgewinn: {eur(_shop_n)} − {eur(_shop_ek)} − {eur(_shop_fee)} − {eur(_shop_ship)} = <strong>{eur(_shop_g)}</strong>. Die Marge sinkt damit von {de((_shop_n-_shop_ek)/_shop_n*100,1)} % (nur Einkauf) auf {de(_shop_g/_shop_n*100,1)} %.</div>
<p>Trag solche Kosten pro Stück in den Rechner ein, indem du sie zum Einkaufspreis addierst: Einkauf {eur(_shop_ek+_shop_fee+_shop_ship)}, Verkauf {eur(_shop_n)}. Dann zeigt er die Marge, die tatsächlich zur Deckung von Miete, Werbung und Arbeitszeit bleibt.</p>
""",
"bruchrechner": f"""
<h2>Brüche im Alltag: Rezepte und Maße</h2>
<div class="example"><strong>Rezept umrechnen:</strong> Ein Rezept für 4 Personen verlangt ¾ Becher Sahne, gekocht wird für 6 Personen. Faktor 6/4 = 3/2. ¾ × 3/2 = 9/8 = 1 ⅛ Becher. Für 2 Personen wäre es ¾ × 1/2 = 3/8 Becher.</div>
<div class="example"><strong>Drei Brüche addieren:</strong> ½ + ⅓ + ¼. Der kleinste gemeinsame Nenner von 2, 3 und 4 ist 12: 6/12 + 4/12 + 3/12 = 13/12 = 1 1/12. Im Rechner gehst du in zwei Schritten vor: erst ½ + ⅓ = 5/6, dann 5/6 + ¼.</div>
<div class="example"><strong>Zoll-Maße:</strong> Werkzeuge und Schrauben aus den USA tragen Bruchmaße. Ein Schlüssel mit 3/8 Zoll misst 3 ÷ 8 × 25,4 = {de(3/8*25.4,3)} mm, einer mit 9/16 Zoll {de(9/16*25.4,3)} mm. Zum Umrechnen hilft der <a href="/einheitenrechner.html">Einheitenrechner</a>.</div>
""",
"dreisatz-rechner": f"""
<h2>Dreisatz mit Zeit und Währung</h2>
<div class="example"><strong>Fahrzeit:</strong> 180 km dauern bei gleichem Tempo 2 Stunden. 300 km dauern 2 ÷ 180 × 300 = {de(2/180*300,4)} Stunden. Das sind <strong>3 Stunden 20 Minuten</strong>, nicht 3 Stunden 33 Minuten: Der Nachkommateil {de(2/180*300-3,4)} Stunden muss mit 60 malgenommen werden ({de((2/180*300-3)*60,0)} Minuten).</div>
<div class="example"><strong>Wechselkurs:</strong> Angenommen, 1 € entspricht {de(_fx,2)} britischen Pfund. Eine Rechnung über 120 £ kostet dann 1 ÷ {de(_fx,2)} × 120 = {eur(120/_fx)}. Den tatsächlichen Kurs und die Gebühren deiner Bank oder Karte findest du in deren Konditionen; Referenzkurse veröffentlicht die Europäische Zentralbank.</div>
""",
"kreditrechner": f"""
<h2>Wie stark der Zinssatz die Rate verändert</h2>
<p>20.000 € auf 5 Jahre bei verschiedenen Sollzinsen:</p>
<table class="tbl"><thead><tr><th>Sollzins</th><th>Monatsrate</th><th>Zinskosten gesamt</th></tr></thead><tbody>
{''.join(f'<tr><td>{de(p,1)} %</td><td>{eur(r)}</td><td>{eur(r*60-20000)}</td></tr>' for p, r in _rate_tbl)}
</tbody></table>
<p>Jeder Prozentpunkt mehr kostet bei diesem Betrag und dieser Laufzeit grob 9 bis 10 € Rate im Monat und mehr als 500 € Zinsen über die Laufzeit. Schon ein halber Prozentpunkt Unterschied zwischen zwei Angeboten lohnt deshalb einen genauen Vergleich.</p>
""",
"rabatt-rechner": f"""
<h2>Rabatte, die nur eine Zeit lang gelten</h2>
<div class="example"><strong>Abo mit Einstiegsrabatt:</strong> Ein Streaming-Abo kostet {eur(_abo)} im Monat, die ersten 3 Monate gibt es 50 % Rabatt. Ersparnis: 3 × {eur(_abo)} × 0,5 = {eur(_abo_save)}. Bezogen auf das erste Jahr mit {eur(12*_abo)} sind das nur {de(_abo_save/(12*_abo)*100,1)} % – und ab dem zweiten Jahr nichts mehr. Wer den Rechner verwendet, trägt deshalb besser den Jahrespreis als Preis und den umgerechneten Prozentsatz als Rabatt ein.</div>
<p>Dasselbe gilt für Einführungsrabatte bei Strom, Mobilfunk oder Versicherungen: Ein großer Prozentsatz auf einen kurzen Zeitraum ist über die Vertragslaufzeit gerechnet oft ein kleiner.</p>
""",
"zinseszins-rechner": f"""
<h2>Rückwärts gerechnet: Wie viel muss ich sparen?</h2>
<p>Wer ein Sparziel hat, löst die Formel nach der Rate auf: <strong>R = Ziel × i ÷ ((1 + i)ⁿ − 1)</strong>. Für 10.000 € in 5 Jahren (60 Monate) ergibt das:</p>
<table class="tbl"><thead><tr><th>Zinssatz p. a.</th><th>nötige Sparrate pro Monat</th><th>davon Zinsen am Ende</th></tr></thead><tbody>
{''.join(f'<tr><td>{de(p,0)} %</td><td>{eur(r)}</td><td>{eur(10000-r*60)}</td></tr>' for p, r in _goal)}
</tbody></table>
<p>Über fünf Jahre machen die Zinsen nur einen kleinen Teil aus; den Großteil leisten die Einzahlungen. Erst über Jahrzehnte überholt der Zinseszins die eigene Sparleistung. Die Rate aus der Tabelle kannst du oben eintragen und das Ergebnis prüfen.</p>
""",
}
for _k, _v in _ADD.items():
    _i = DEEP2[_k].index("<h2>Typische Fehler</h2>")
    DEEP2[_k] = DEEP2[_k][:_i] + _v.strip() + "\n" + DEEP2[_k][_i:]
