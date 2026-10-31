"""Vertiefung (Oktober 2026): Beispiele AT/DE, typische Fehler, Grenzen und Häufige Fragen.
Wird an Artikel und Rechner angehängt. Alle Beispielwerte werden hier in Python berechnet."""
import math
from content.calcs import de, eur

STAND = "Stand: Oktober 2026"
SRC_KM_AT = f'<a href="https://www.oesterreich.gv.at/themen/steuern_und_finanzen/unterstuetzungen_beihilfen_und_foerderungen/pendlerpauschale_und_kilometergeld/Seite.350300.html" rel="noopener">oesterreich.gv.at – Pendlerpauschale und Kilometergeld</a> ({STAND})'
SRC_9_ESTG = f'<a href="https://www.gesetze-im-internet.de/estg/__9.html" rel="noopener">§ 9 EStG auf gesetze-im-internet.de</a> ({STAND})'
SRC_9A_ESTG = f'<a href="https://www.gesetze-im-internet.de/estg/__9a.html" rel="noopener">§ 9a EStG</a> ({STAND})'
SRC_3_ESTG = f'<a href="https://www.gesetze-im-internet.de/estg/__3.html" rel="noopener">§ 3 Nr. 51 EStG auf gesetze-im-internet.de</a> ({STAND})'
SRC_PANGV16 = f'<a href="https://www.gesetze-im-internet.de/pangv_2022/__16.html" rel="noopener">§ 16 Preisangabenverordnung</a> ({STAND})'
SRC_PANGV11 = f'<a href="https://www.gesetze-im-internet.de/pangv_2022/__11.html" rel="noopener">§ 11 Preisangabenverordnung</a> ({STAND})'
SRC_USTDV33 = f'<a href="https://www.gesetze-im-internet.de/ustdv_1980/__33.html" rel="noopener">§ 33 UStDV</a> ({STAND})'
SRC_MILO = f'<a href="https://www.gesetze-im-internet.de/milov5/__1.html" rel="noopener">§ 1 Fünfte Mindestlohnanpassungsverordnung</a> ({STAND})'
SRC_BURLG = f'<a href="https://www.gesetze-im-internet.de/burlg/__3.html" rel="noopener">§ 3 Bundesurlaubsgesetz</a> ({STAND})'
SRC_STAT_AT = f'<a href="https://www.statistik.at/fileadmin/announcement/2026/01/20260119VPIJahr2025.pdf" rel="noopener">Statistik Austria, VPI Jahresdurchschnitt 2025</a> ({STAND})'
SRC_DESTATIS = f'<a href="https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/01/PD26_019_611.html" rel="noopener">Destatis, Pressemitteilung Nr. 019 vom 16. Januar 2026</a> ({STAND})'

# ---------- amtliche Werte (geprüft in den oben verlinkten Primärquellen)
KM_AT, KM_AT_MIT, KM_AT_MAX = 0.50, 0.15, 30000      # Kilometergeld PKW, Mitfahrer, steuerfreie km/Jahr
EP_DE, EP_DE_MAX, AN_PAUSCH = 0.38, 4500, 1230       # Entfernungspauschale, Höchstbetrag, Arbeitnehmer-Pauschbetrag
MILO_26, MILO_27 = 13.90, 14.60                      # Mindestlohn DE
VPI_DE = {2021: 3.1, 2022: 6.9, 2023: 5.9, 2024: 2.2, 2025: 2.2}
HVPI_DE_25 = 2.3
VPI_AT = {2024: 2.9, 2025: 3.6}
VPI_AT_IDX = {2024: 123.8, 2025: 128.2}             # VPI 2020 = 100, Jahresdurchschnitt


def _pct(x, d=1):
    return f"{de(x, d)} %"


def faq(items):
    return "<h2>Häufige Fragen</h2>\n" + "\n".join(f"<h3>{q}</h3>\n<p>{a}</p>" for q, a in items)


def _apr(net, pay, n, extra_month=0.0):
    """Effektiver Jahreszins nach EU-Methode (jährliche Abzinsung, t in Jahren), per Bisektion."""
    lo, hi = 0.0, 1.0
    for _ in range(200):
        x = (lo + hi) / 2
        pv = sum((pay + extra_month) / (1 + x) ** (k / 12) for k in range(1, n + 1))
        lo, hi = (x, hi) if pv > net else (lo, x)
    return x * 100


def _annuity(K, p, months):
    i = p / 100 / 12
    return K * i / (1 - (1 + i) ** -months)


# ---------- Prozentpunkte
_at_pp = VPI_AT[2025] - VPI_AT[2024]
_at_rel = _at_pp / VPI_AT[2024] * 100
_hz_a, _hz_b = 200000 * 0.03, 200000 * 0.04

# ---------- Grundwert
_g_at, _g_de = 2800, 3200
_g_at_m, _g_de_m = _g_at * 0.03, _g_de * 0.03

# ---------- Rabatte
_r_pick = 3.49 * 0.75
_r_de = 249 * 0.8 - 20
_r_de2 = (249 - 20) * 0.8

# ---------- Mehrwertsteuer
_pos = [1.99, 2.49, 0.89, 3.29, 1.19]
_pos_round = sum(round(b - b / 1.2, 2) for b in _pos)
_pos_sum = sum(_pos) - sum(_pos) / 1.2

# ---------- Kredit
_k1_rate = _annuity(10000, 5, 60)
_k1_eff0 = ((1 + 0.05 / 12) ** 12 - 1) * 100
_k1_eff = _apr(10000 - 300, _k1_rate, 60)
_k2_rate = _annuity(25000, 4.9, 84)
_k2_eff = _apr(25000, _k2_rate, 84, extra_month=5)

# ---------- 72er-Regel
_dbl = lambda p: math.log(2) / math.log(1 + p / 100)
_tri = lambda p: math.log(3) / math.log(1 + p / 100)

# ---------- Durchschnitt
_t1l, _t1p, _t2l, _t2p = 40, 1.55, 20, 1.75
_t_simple = (_t1p + _t2p) / 2
_t_weight = (_t1l * _t1p + _t2l * _t2p) / (_t1l + _t2l)
_kl = [(24, 2.1), (12, 3.0)]
_kl_wrong = (2.1 + 3.0) / 2
_kl_right = sum(n * x for n, x in _kl) / sum(n for n, _ in _kl)
_sample = [2, 2, 3, 1, 2, 5, 2, 4]
_s_sorted = sorted(_sample)
_s_mean = sum(_sample) / len(_sample)
_s_med = (_s_sorted[3] + _s_sorted[4]) / 2

# ---------- Fahrt
_dr_km = 230 * 2
_dr_kmg = _dr_km * KM_AT
_dr_sprit = _dr_km * 6.5 / 100 * 1.70
_ep_km, _ep_days = 23, 220
_ep = _ep_km * _ep_days * EP_DE
_ep_wrong = _ep_km * 2 * _ep_days * EP_DE

# ---------- Inflation
_de_cum = math.prod(1 + v / 100 for v in VPI_DE.values())
_de_sum = sum(VPI_DE.values())
_at_cum = (1 + VPI_AT[2024] / 100) * (1 + VPI_AT[2025] / 100)
_rent = 800 * VPI_AT_IDX[2025] / VPI_AT_IDX[2024]

# ---------- Stundenlohn
_mi_m = MILO_26 * 40 * 52 / 12
_mi_m27 = MILO_27 * 40 * 52 / 12
_ai_h = 3500 * 14 / (38.5 * 52)
_ai_h2 = 3500 * 14 / (43.5 * 52)
_pend_h = 3000 * 14 / ((38.5 + 5) * 52)

# ---------- Trinkgeld
_aufr = (90 - 87.40) / 87.40 * 100
_tg_orig, _tg_paid = 64.00, 64.00 - 15

_brot = 3.00 / 1.10 * 1.049
_kA = _annuity(15000, 4.5, 60); _kB = _annuity(15000, 5.2, 60)
_kA_eff = _apr(15000 - 400, _kA, 60); _kB_eff = _apr(15000, _kB, 60)
_sp = sum(100 * (1 + 0.04 / 12) ** k for k in range(1, 18 * 12 + 1))

DEEP = {}

DEEP["prozent-oder-prozentpunkte"] = f"""
<h2>Beide Rechnungen Schritt für Schritt</h2>
<p>Für jede Veränderung zwischen zwei Prozentzahlen gibt es zwei richtige Antworten – du musst nur sagen, welche du meinst.</p>
<ol><li><strong>Differenz in Prozentpunkten:</strong> neuer Wert minus alter Wert. Das Ergebnis ist eine absolute Größe.</li>
<li><strong>Veränderung in Prozent:</strong> Differenz geteilt durch den alten Wert, mal 100. Das Ergebnis ist eine relative Größe.</li></ol>
<table class="tbl text"><thead><tr><th>von → nach</th><th>Prozentpunkte</th><th>Prozent</th></tr></thead><tbody>
{''.join(f'<tr><td>{de(a,1)} % → {de(b,1)} %</td><td>{"+" if b>a else "−"}{de(abs(b-a),1)}</td><td>{"+" if b>a else "−"}{de(abs(b-a)/a*100,1)} %</td></tr>' for a, b in ((1, 2), (2, 2.5), (4, 3), (10, 12), (20, 15), (40, 41)))}
</tbody></table>
<p>Die letzte Zeile zeigt: Bei hohen Ausgangswerten ist ein Prozentpunkt relativ wenig, bei niedrigen sehr viel.</p>
<h2>Beispiel mit echten Zahlen: Inflation in Österreich</h2>
<div class="example">Laut Statistik Austria lag die Inflationsrate im Jahresdurchschnitt 2024 bei {de(VPI_AT[2024],1)} % und 2025 bei {de(VPI_AT[2025],1)} %. Die Teuerung ist also um <strong>{de(_at_pp,1)} Prozentpunkte</strong> gestiegen – relativ betrachtet um <strong>{_pct(_at_rel)}</strong>. Beide Aussagen stimmen. Quelle: {SRC_STAT_AT}.</div>
<div class="example">In Deutschland lag die Rate laut Destatis 2024 und 2025 jeweils bei {de(VPI_DE[2025],1)} %. Die Veränderung beträgt 0 Prozentpunkte und 0 % – die Preise sind trotzdem weiter gestiegen, nur nicht schneller als im Jahr davor. Quelle: {SRC_DESTATIS}.</div>
<h2>Beispiel Wohnkredit</h2>
<p>Bei 200.000 € Restschuld kosten 3 % Zinsen im ersten Jahr rund {eur(_hz_a)}, 4 % rund {eur(_hz_b)}. Ein Prozentpunkt mehr bedeutet hier {eur(_hz_b-_hz_a)} pro Jahr oder {_pct((_hz_b-_hz_a)/_hz_a*100)} höhere Zinskosten. Die Rechnung vereinfacht, weil die Restschuld im Laufe des Jahres sinkt – an der Größenordnung ändert das wenig.</p>
<h2>Beispiel Steuersatz: 10 % auf 4,9 %</h2>
<p>Seit 1. Juli 2026 gilt in Österreich für ausgewählte Grundnahrungsmittel 4,9 % statt 10 % Umsatzsteuer. Der Satz ist um {de(10-4.9,1)} Prozentpunkte gesunken, die Steuer selbst um {_pct((10-4.9)/10*100,0)}. Für den Preis heißt das weniger: Ein Brot um 3,00 € brutto mit 10 % kostet mit 4,9 % – bei unverändertem Nettopreis – {eur(_brot)}, also {_pct((3-_brot)/3*100)} weniger. Der Grund: Die Steuer ist nur ein kleiner Teil des Bruttopreises.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>„Die Zinsen sinken um 1 %“:</strong> Gemeint sind fast immer Prozentpunkte. Wörtlich genommen würden 4 % um 1 % sinken – auf 3,96 %. Frag im Zweifel nach.</div>
<div class="warn"><strong>Prozentpunkte addieren, Prozente nicht:</strong> Steigt eine Quote zweimal um 2 Prozentpunkte, sind es zusammen 4 Prozentpunkte. Zwei Anstiege um je 10 % ergeben dagegen nicht 20 %, sondern {de((1.1*1.1-1)*100,0)} %.</div>
<h2>Basispunkte</h2>
<p>Im Finanzbereich wird oft in Basispunkten gerechnet: 1 Basispunkt ist ein Hundertstel Prozentpunkt. 25 Basispunkte sind also 0,25 Prozentpunkte – eine übliche Schrittweite bei Leitzinsänderungen.</p>
<h2>Grenzen</h2>
<p>Prozentpunkte vergleichen nur sinnvoll Prozentzahlen mit derselben Bezugsgröße. Eine Arbeitslosenquote nach nationaler Definition lässt sich nicht in Prozentpunkten mit einer nach internationaler Definition vergleichen.</p>
{faq([
("Ist ein Prozentpunkt immer kleiner als ein Prozent?", "Nein. Ob ein Prozentpunkt relativ viel oder wenig ist, hängt vom Ausgangswert ab. Von 1 % auf 2 % ist ein Prozentpunkt, relativ aber eine Verdopplung (+100 %)."),
("Wie schreibe ich Prozentpunkte richtig ab?", "Üblich ist „Prozentpunkte“ ausgeschrieben oder die Abkürzung „PP“ bzw. „Pp.“. Das Zeichen % sollte nur für Prozent stehen."),
("Kann eine Veränderung in Prozent negativ sein, in Prozentpunkten aber positiv?", "Nein. Beide haben immer dasselbe Vorzeichen, weil beide aus derselben Differenz berechnet werden – nur mit anderer Bezugsgröße."),
])}
"""

DEEP["grundwert-richtig-waehlen"] = f"""
<h2>Gehaltserhöhung: Grundwert ist das alte Gehalt</h2>
<div class="example"><strong>Österreich:</strong> Ein Bruttogehalt von {eur(_g_at)} steigt um 3 %. Das sind {eur(_g_at_m)} mehr pro Monat. Weil in Österreich meist 14 Gehälter gezahlt werden, ergibt das {eur(_g_at_m*14)} mehr pro Jahr – nicht {eur(_g_at_m*12)}.</div>
<div class="example"><strong>Deutschland:</strong> {eur(_g_de)} brutto plus 3 % ergeben {eur(_g_de*1.03)} – also {eur(_g_de_m)} mehr pro Monat und bei 12 Gehältern {eur(_g_de_m*12)} pro Jahr.</div>
<p>Der Prozentsatz ist in beiden Ländern gleich, der Betrag nicht: Er hängt vom Grundwert ab, also vom bisherigen Gehalt und davon, wie oft es im Jahr gezahlt wird.</p>
<h2>„Teurer als“ und „billiger als“ sind nicht spiegelbildlich</h2>
<p>Kostet Produkt A 125 € und Produkt B 100 €, ist A um 25 % teurer als B – Grundwert ist B. Umgekehrt ist B aber nur um 20 % billiger als A – Grundwert ist jetzt A. Wer Preise in zwei Geschäften oder Ländern vergleicht, sollte deshalb immer dazusagen, welcher Preis die Basis ist.</p>
<table class="tbl text"><thead><tr><th>A ist teurer als B um …</th><th>B ist billiger als A um …</th></tr></thead><tbody>
{''.join(f'<tr><td>{p} %</td><td>{de(p/(100+p)*100,1)} %</td></tr>' for p in (5, 10, 20, 50, 100))}
</tbody></table>
<h2>Grundwert bei Preisen mit Steuer</h2>
<p>Die Umsatzsteuer wird auf den Nettopreis aufgeschlagen. Der Nettopreis ist also der Grundwert, der Bruttopreis ist Grundwert plus Prozentwert. Wer vom Bruttopreis ausgeht, braucht deshalb einen anderen Rechenweg – das zeigt der Ratgeber <a href="/mehrwertsteuer-herausrechnen.html">Mehrwertsteuer herausrechnen</a>.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Mit dem Endwert rechnen:</strong> „Nach 15 % Preiserhöhung kostet das Abo 23 €. Wie viel war es vorher?“ Falsch: 23 € − 15 % = {eur(23*0.85)}. Richtig: 23 ÷ 1,15 = {eur(23/1.15)}. Der alte Preis ist der Grundwert, nicht der neue.</div>
<div class="warn"><strong>Verschiedene Grundwerte vergleichen:</strong> „Umsatz +10 %, Gewinn +10 %“ heißt nicht, dass beide um denselben Betrag gestiegen sind. 10 % von 1 Million Umsatz sind etwas völlig anderes als 10 % von 50.000 € Gewinn.</div>
<h2>Grenzen</h2>
<p>Prozentangaben ohne genannten Grundwert sind nicht überprüfbar. Steht in einer Werbung „bis zu 40 % günstiger“, fehlt die Angabe, wovon – vom früheren Preis, von der unverbindlichen Preisempfehlung oder vom teuersten Mitbewerber. Erst mit dem Grundwert wird aus der Prozentzahl eine nachrechenbare Aussage.</p>
{faq([
("Was ist der Grundwert beim Rabatt?", "Der ursprüngliche Preis vor dem Rabatt. 20 % Rabatt auf 80 € sind 16 €, der neue Preis ist 64 €. Wer nachträglich den alten Preis sucht, teilt 64 durch 0,8."),
("Woran erkenne ich den Grundwert in einer Textaufgabe?", "Er steht meist nach „von“ oder „als“: „20 % von 250“, „teurer als der Vorjahrespreis“. Bei Veränderungen ist es immer der Wert vor der Veränderung."),
("Kann der Grundwert kleiner sein als der Prozentwert?", "Ja. Dann ist der Prozentsatz größer als 100 %. Ein Preis, der von 40 € auf 100 € steigt, hat sich um 150 % erhöht."),
("Warum gleichen sich +10 % und −10 % nicht aus?", f"Weil sich der Grundwert dazwischen ändert: 100 → 110 → 99. Das Minus bezieht sich auf 110, nicht auf 100. Zurück auf 100 führt erst ein Minus von {de(10/110*100,2)} %."),
])}
"""

DEEP["rabatte-kombinieren"] = f"""
<h2>Die allgemeine Formel</h2>
<p>Für beliebig viele Rabatte r₁, r₂, r₃ … gilt: Endpreis = Preis × (1 − r₁) × (1 − r₂) × (1 − r₃) … Die Reihenfolge der Prozent-Rabatte spielt dabei keine Rolle, weil sich Faktoren vertauschen lassen.</p>
<div class="example"><strong>Österreich – Rabattpickerl im Supermarkt:</strong> Ein Produkt um 3,49 € mit einem −25-%-Pickerl kostet 3,49 × 0,75 = {eur(_r_pick)}. Gibt es in derselben Woche zusätzlich 10 % auf das ganze Sortiment, sind es {eur(_r_pick*0.9)} – insgesamt eine Ersparnis von {_pct((1-0.75*0.9)*100)}, nicht 35 %.</div>
<div class="example"><strong>Deutschland – Prozent plus Gutschein:</strong> Ein Mantel um 249 € mit 20 % Rabatt und einem 20-€-Gutschein. Wird zuerst der Prozent-Rabatt abgezogen, zahlst du {eur(_r_de)}; wird zuerst der Gutschein abgezogen, {eur(_r_de2)}. Welche Reihenfolge gilt, steht in den Gutscheinbedingungen.</div>
<h2>Aktionen in Prozent umrechnen</h2>
<p>Mengenaktionen sind oft schwerer zu durchschauen als ein Prozent-Rabatt. So viel sparst du pro Stück, wenn du die volle Aktionsmenge kaufst:</p>
<table class="tbl text"><thead><tr><th>Aktion</th><th>Ersparnis pro Stück</th></tr></thead><tbody>
<tr><td>3 zum Preis von 2</td><td>{_pct((1-2/3)*100)}</td></tr>
<tr><td>2. Artikel −50 %</td><td>{_pct((1-1.5/2)*100)}</td></tr>
<tr><td>4 zum Preis von 3</td><td>{_pct((1-3/4)*100)}</td></tr>
<tr><td>3. Artikel gratis bei 3 verschiedenen Preisen</td><td>abhängig vom günstigsten Artikel</td></tr>
</tbody></table>
<p>„2. Artikel −50 %“ klingt nach der Hälfte, entspricht aber nur einem Viertel Ersparnis – und nur, wenn du wirklich zwei Stück brauchst.</p>
<h2>Welcher Rabatt fehlt noch bis zum Wunschpreis?</h2>
<p>Steht ein Artikel bereits mit 20 % Rabatt und du willst insgesamt 40 % sparen, brauchst du noch einen zweiten Rabatt von 1 − 0,6 ÷ 0,8 = {_pct((1-0.6/0.8)*100)} – nicht 20 %.</p>
<h2>Rabatt und Mehrwertsteuer</h2>
<p>Ein Prozent-Rabatt wirkt auf Netto- und Bruttopreis gleich stark. 20 % Rabatt auf 120 € brutto ergeben 96 € brutto; netto sind es in Österreich 100 € → {eur(96/1.2)}, also ebenfalls genau 20 % weniger. Für Unternehmen, die mit Nettopreisen rechnen, und für Privatkundinnen mit Bruttopreisen ist die Ersparnis in Prozent deshalb dieselbe. Anders ist es bei einem festen Euro-Rabatt: 20 € auf 120 € brutto sind {_pct(20/120*100)} Ersparnis, auf 100 € netto gerechnet aber 20 %.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Rabatte addieren:</strong> 50 % + 50 % sind keine 100 %, also kein Gratisartikel, sondern 75 % Ersparnis.</div>
<div class="warn"><strong>Den Streichpreis ungeprüft übernehmen:</strong> Die Ersparnis ist nur so viel wert wie der Ausgangspreis. In Deutschland muss ein Händler bei einer Preisermäßigung für Waren den niedrigsten Gesamtpreis der letzten 30 Tage angeben (mit Ausnahmen, etwa für schnell verderbliche Ware). Quelle: {SRC_PANGV11}.</div>
<h2>Rückwärts: Was kostete der Artikel ursprünglich?</h2>
<p>Zahlst du nach zwei Rabatten von 30 % und 10 % noch 50,40 €, war der Ausgangspreis 50,40 ÷ (0,7 × 0,9) = {eur(50.40/(0.7*0.9))}. Wer stattdessen 40 % auf 50,40 € aufschlägt, kommt auf {eur(50.40*1.4)} und liegt deutlich zu niedrig – derselbe Grundwert-Fehler wie bei einem einzelnen Rabatt.</p>
<h2>Grenzen</h2>
<p>Die Rechnung zeigt den Preis, nicht den Nutzen. Eine Mengenaktion spart nur, wenn du die zusätzliche Menge auch verbrauchst. Versandkosten, Mindestbestellwerte und Rückgabebedingungen ändern die echte Ersparnis zusätzlich.</p>
{faq([
("Wie berechne ich den Rabatt in Prozent aus zwei Preisen?", "(alter Preis − neuer Preis) ÷ alter Preis × 100. Von 79,90 € auf 59,90 € sind das rund 25 %."),
("Ist es egal, welcher Prozent-Rabatt zuerst kommt?", "Ja. Zwei Prozent-Rabatte ergeben in jeder Reihenfolge denselben Endpreis. Nur bei einem festen Euro-Betrag (Gutschein) zählt die Reihenfolge."),
("Wie viel Prozent spare ich bei 30 % + 30 %?", f"Du zahlst 0,7 × 0,7 = 0,49 des Preises und sparst {de((1-0.49)*100,0)} %."),
("Gilt Skonto auch als zusätzlicher Rabatt?", "Rechnerisch ja: Skonto wird vom bereits rabattierten Rechnungsbetrag abgezogen und wirkt wie ein weiterer Faktor in der Formel."),
])}
"""

DEEP["mehrwertsteuer-herausrechnen"] = f"""
<h2>Schnelle Tabelle: Wie viel Steuer steckt im Betrag?</h2>
<table class="tbl"><thead><tr><th>Brutto</th><th>Steuer bei 20 %</th><th>Steuer bei 19 %</th><th>Steuer bei 10 %</th><th>Steuer bei 7 %</th></tr></thead><tbody>
{''.join(f'<tr><td>{eur(b)}</td>' + ''.join(f'<td>{eur(b-b/(1+r/100))}</td>' for r in (20, 19, 10, 7)) + '</tr>' for b in (10, 50, 100, 500, 1000))}
</tbody></table>
<h2>Durchgerechnet: Handwerkerrechnung</h2>
<div class="example"><strong>Österreich:</strong> Eine Malerrechnung lautet auf 1.548,00 € brutto mit 20 %. Netto: 1.548 ÷ 1,2 = {eur(1548/1.2)}. Steuer: {eur(1548-1548/1.2)}. Gegenprobe: {eur(1548/1.2)} × 1,2 = {eur(1548)}.</div>
<div class="example"><strong>Deutschland:</strong> Dieselbe Leistung kostet 1.547,00 € brutto mit 19 %. Netto: 1.547 ÷ 1,19 = {eur(1547/1.19)}. Steuer: {eur(1547-1547/1.19)}.</div>
<p>Die Gegenprobe lohnt sich immer: Netto mal Teiler muss wieder den Bruttobetrag ergeben, höchstens mit einem Cent Rundungsdifferenz.</p>
<h2>Rundung: pro Position oder auf die Summe?</h2>
<p>Ein Kassenbon mit fünf Artikeln zu 20 % ({", ".join(eur(p) for p in _pos)}) ergibt eine Bruttosumme von {eur(sum(_pos))}. Rechnest du die Steuer aus der Summe heraus, sind es {eur(_pos_sum)}. Rundest du bei jedem Artikel einzeln auf Cent und addierst, kommst du auf {eur(_pos_round)}. Kleine Abweichungen von ein, zwei Cent sind deshalb normal und kein Rechenfehler – entscheidend ist der Betrag, der auf der Rechnung ausgewiesen ist.</p>
<h2>Kleinbetragsrechnungen in Deutschland</h2>
<p>Bei Rechnungen bis 250 € darf in Deutschland statt Netto und Steuer getrennt auch das Entgelt samt Steuer in einer Summe stehen, zusammen mit dem Steuersatz. Wer die Vorsteuer daraus braucht, muss sie selbst herausrechnen – genau mit dem Teiler aus der Tabelle oben. Quelle: {SRC_USTDV33}.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Mit 0,8 malnehmen:</strong> Brutto × 0,8 ist dasselbe wie 20 % abziehen und deshalb falsch. Richtig ist Brutto × 0,8333… oder eben ÷ 1,2.</div>
<div class="warn"><strong>Den falschen Satz verwenden:</strong> Eine deutsche Rechnung mit 19 % lässt sich nicht mit dem österreichischen Teiler 1,2 zerlegen. Maßgeblich ist immer der Satz, der auf der Rechnung steht.</div>
<h2>Grenzen</h2>
<p>Das Herausrechnen funktioniert nur, wenn ein einziger Steuersatz auf den ganzen Betrag angewendet wurde. Enthält eine Rechnung Positionen mit verschiedenen Sätzen, musst du jede Gruppe getrennt herausrechnen. Bei steuerfreien Leistungen oder Rechnungen von Kleinunternehmern gibt es nichts herauszurechnen.</p>
{faq([
("Was mache ich mit einem Kassenbon mit mehreren Steuersätzen?", "Die Beträge nach Steuersatz gruppieren und jede Gruppe mit ihrem Teiler herausrechnen. Auf österreichischen Kassenbons sind die Sätze meist mit Buchstaben gekennzeichnet und unten zusammengefasst."),
("Warum ist die Steuer bei 20 % ein Sechstel des Bruttobetrags?", "Weil der Bruttobetrag aus sechs Fünfteln des Nettobetrags besteht: 100 % netto plus 20 % Steuer = 120 %. Die Steuer ist 20 von 120, also ein Sechstel."),
("Kann ich die Steuer auch mit einem Prozentsatz vom Bruttobetrag berechnen?", f"Ja: Steuer = Brutto × Satz ÷ (100 + Satz). Bei 19 % sind das {de(19/119*100,2)} % des Bruttobetrags."),
("Wie rechne ich netto in brutto um?", "Netto mal 1 plus Steuersatz: 100 € netto × 1,2 = 120 € brutto in Österreich, × 1,19 = 119 € in Deutschland."),
])}
"""

DEEP["sollzins-und-effektivzins"] = f"""
<h2>Durchgerechnet: Warum der Effektivzins höher ist</h2>
<div class="example"><strong>Deutschland – Ratenkredit mit Bearbeitungsgebühr:</strong> 10.000 €, 5 Jahre, 5 % Sollzins, monatliche Rate {eur(_k1_rate)}. Schon ohne Gebühr liegt der effektive Jahreszins bei {_pct(_k1_eff0,2)}, weil die Zinsen monatlich verrechnet werden. Werden zusätzlich 300 € Bearbeitungsgebühr fällig, steigt er auf rund {_pct(_k1_eff,2)}: Du zahlst dieselben Raten, bekommst aber wirtschaftlich nur 9.700 €.</div>
<div class="example"><strong>Österreich – Kredit mit Pflichtkonto:</strong> 25.000 €, 7 Jahre, 4,9 % Sollzins, Rate {eur(_k2_rate)}. Verlangt die Bank dafür ein Girokonto um 5 € im Monat, das ohne den Kredit nicht nötig wäre, steigt der effektive Jahreszins auf rund {_pct(_k2_eff,2)}. Über die Laufzeit sind das {eur(5*84)} zusätzliche Kosten.</div>
<p>Die Effektivzinsen in diesen Beispielen sind nach der EU-einheitlichen Methode berechnet: Alle Zahlungen werden mit dem gesuchten Zinssatz auf den Auszahlungstag abgezinst, bis sie dem ausgezahlten Betrag entsprechen.</p>
<h2>Was in Deutschland einbezogen wird – und was nicht</h2>
<p>Die Preisangabenverordnung legt fest, dass in den effektiven Jahreszins alle Zinsen und sonstigen Kosten einfließen, die der Verbraucher im Zusammenhang mit dem Kreditvertrag zahlen muss und die der Bank bekannt sind – ausdrücklich auch Vermittlungskosten und Kosten für ein Konto, das Voraussetzung für den Kredit ist. Nicht einbezogen werden unter anderem Notarkosten, Grundbuchgebühren für die Eigentumsübertragung, Kosten bei Zahlungsverzug und freiwillige Versicherungen. In der Werbung muss der effektive Jahreszins mindestens so deutlich hervorgehoben werden wie jeder andere Zinssatz. Quelle: {SRC_PANGV16}.</p>
<table class="tbl text"><thead><tr><th>Kostenart</th><th>im Effektivzins?</th></tr></thead><tbody>
<tr><td>Sollzinsen</td><td>ja</td></tr><tr><td>Bearbeitungs- und Vermittlungsgebühr</td><td>ja</td></tr>
<tr><td>Pflichtkonto für den Kredit</td><td>ja</td></tr><tr><td>freiwillige Restschuldversicherung</td><td>nein</td></tr>
<tr><td>Notar, Grundbucheintrag der Eigentumsübertragung</td><td>nein</td></tr><tr><td>Verzugskosten</td><td>nein</td></tr>
</tbody></table>
<h2>Zwei Angebote vergleichen</h2>
<p>15.000 € über 5 Jahre. <strong>Angebot A:</strong> 4,5 % Sollzins plus 400 € Bearbeitungsgebühr, Rate {eur(_kA)}. <strong>Angebot B:</strong> 5,2 % Sollzins ohne Gebühr, Rate {eur(_kB)}.</p>
<table class="tbl"><thead><tr><th>Angebot</th><th>Effektivzins</th><th>Gesamtkosten</th></tr></thead><tbody>
<tr><td>A</td><td>{_pct(_kA_eff,2)}</td><td>{eur(_kA*60+400-15000)}</td></tr>
<tr><td>B</td><td>{_pct(_kB_eff,2)}</td><td>{eur(_kB*60-15000)}</td></tr></tbody></table>
<p>Der niedrigere Sollzins allein entscheidet nicht – erst Effektivzins und Gesamtkosten zeigen, welches Angebot günstiger ist.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Nur die Rate vergleichen:</strong> Eine niedrigere Rate kommt oft nur von einer längeren Laufzeit. Vergleiche Effektivzins und Gesamtbetrag – beide stehen in den vorvertraglichen Informationen.</div>
<div class="warn"><strong>„Ab“-Zinsen für bare Münze nehmen:</strong> Werbezinsen gelten oft nur bei bester Bonität. Entscheidend ist der Effektivzins im persönlichen Angebot.</div>
<h2>Grenzen des Effektivzinses</h2>
<p>Bei variablem Zins wird angenommen, dass Sollzins und Kosten bis zum Ende der Laufzeit gleich bleiben (§ 16 Abs. 5 PAngV). Steigt der Referenzzins, ist der tatsächliche Zins später höher. Auch Kosten außerhalb der Berechnung, etwa eine freiwillige Versicherung, musst du selbst dazurechnen.</p>
{faq([
("Kann der Effektivzins niedriger sein als der Sollzins?", "Bei üblichen Verträgen nicht. Ohne Gebühren und mit jährlicher Zinsverrechnung sind beide gleich; Gebühren und unterjährige Verrechnung erhöhen den Effektivzins."),
("Warum ist der Effektivzins bei kleinen Krediten oft höher?", "Feste Gebühren fallen bei einem kleinen Betrag stärker ins Gewicht. 300 € Gebühr sind bei 5.000 € relativ doppelt so teuer wie bei 10.000 €."),
("Welche Zahl gehört in den Kreditrechner?", "Der Sollzins, denn mit ihm wird die Rate berechnet. Den Effektivzins brauchst du zum Vergleich der Angebote."),
])}
"""

DEEP["zinseszins-und-72er-regel"] = f"""
<h2>Verwandte Faustregeln</h2>
<ul><li><strong>69er- oder 70er-Regel:</strong> 70 ÷ p ist bei kleinen Sätzen und stetiger Verzinsung genauer. Bei 2 % ergibt sie 35 Jahre, exakt sind es {de(_dbl(2),1)}.</li>
<li><strong>Verdreifachung (114er-Regel):</strong> 114 ÷ p. Bei 6 % ergibt das {de(114/6,1)} Jahre, exakt sind es {de(_tri(6),1)}.</li>
<li><strong>Vervierfachung:</strong> zweimal verdoppeln, also 144 ÷ p.</li></ul>
<h2>Durchgerechnet mit echten Inflationsraten</h2>
<div class="example"><strong>Deutschland:</strong> Destatis meldet für 2025 eine Inflationsrate von {de(VPI_DE[2025],1)} %. Bliebe sie so, hätte sich die Kaufkraft nach 72 ÷ {de(VPI_DE[2025],1)} = {de(72/VPI_DE[2025],1)} Jahren halbiert, exakt nach {de(_dbl(VPI_DE[2025]),1)} Jahren. Quelle: {SRC_DESTATIS}.</div>
<div class="example"><strong>Österreich:</strong> Statistik Austria meldet für 2025 {de(VPI_AT[2025],1)} %. Bei dieser Rate halbiert sich die Kaufkraft nach 72 ÷ {de(VPI_AT[2025],1)} = {de(72/VPI_AT[2025],1)} Jahren, exakt nach {de(_dbl(VPI_AT[2025]),1)} Jahren. Quelle: {SRC_STAT_AT}.</div>
<p>Die Beispiele sind Gedankenspiele: Inflationsraten ändern sich von Jahr zu Jahr. Sie zeigen aber, wie stark ein Unterschied von gut einem Prozentpunkt über Jahrzehnte wirkt.</p>
<h2>Zinseszins in Zahlen</h2>
<table class="tbl"><thead><tr><th>Startbetrag 10.000 €</th><th>nach 10 Jahren</th><th>nach 20 Jahren</th><th>nach 30 Jahren</th></tr></thead><tbody>
{''.join(f'<tr><td>{p} % p. a.</td>' + ''.join(f'<td>{eur(10000*(1+p/100)**n)}</td>' for n in (10, 20, 30)) + '</tr>' for p in (1, 3, 5))}
</tbody></table>
<p>Bei 5 % ist der Betrag nach 30 Jahren mehr als vervierfacht – genau so, wie die Regel mit 72 ÷ 5 ≈ 14,4 Jahren pro Verdopplung erwarten lässt.</p>
<h2>Sparplan statt Einmalbetrag</h2>
<p>Für regelmäßige Einzahlungen gilt die 72er-Regel nicht direkt, weil jede Rate unterschiedlich lange verzinst wird. Ein Beispiel: 100 € im Monat, 18 Jahre, 4 % mit monatlicher Gutschrift. Eingezahlt sind {eur(100*12*18)}, am Ende stehen {eur(_sp)} auf dem Konto. Nur die allerersten Raten haben sich verdoppelt; die späten Raten hatten kaum Zeit zu wachsen. Durchschnittlich ist das Geld also deutlich kürzer angelegt als 18 Jahre. Den genauen Verlauf zeigt der <a href="/zinseszins-rechner.html">Zinseszins-Rechner</a>.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Regel ohne Zinseszins anwenden:</strong> Werden Zinsen jedes Jahr ausgezahlt statt angelegt, gibt es keinen Zinseszins. Dann verdoppelt sich das Kapital bei 4 % erst nach 100 ÷ 4 = 25 Jahren.</div>
<div class="warn"><strong>Steuern und Kosten vergessen:</strong> Die Regel braucht den Zinssatz nach Abzug von Kosten und Steuern. Bleiben von 4 % nach Abzügen nur 3 %, dauert die Verdopplung rund 24 statt 18 Jahre.</div>
<h2>Grenzen</h2>
<p>Die Regel setzt einen gleichbleibenden Zinssatz voraus. Bei Aktien oder Fonds schwankt die Rendite; eine Durchschnittsrendite ergibt nur ein Szenario. Bei sehr hohen Sätzen über 20 % wird die Faustformel spürbar ungenau.</p>
{faq([
("Gilt die 72er-Regel auch für monatliche Verzinsung?", "Ja, wenn du den effektiven Jahreszins einsetzt. Mit dem nominalen Satz unterschätzt sie das Wachstum bei monatlicher Gutschrift leicht."),
("Funktioniert die Regel mit negativen Zinsen?", "Mit einem negativen Satz gibt sie näherungsweise an, wann sich ein Betrag halbiert – genau so wie bei der Inflation."),
("Wie rechne ich die Verdopplungszeit exakt?", "Mit dem Logarithmus: Jahre = ln(2) ÷ ln(1 + p ÷ 100). Der Zinseszins-Rechner zeigt das Ergebnis auch ohne Formel."),
])}
"""

DEEP["durchschnitt-rechner"] = f"""
<h2>Gewichteter Durchschnitt im Alltag: der Tankpreis</h2>
<div class="example">Du tankst einmal {_t1l} Liter zu {eur(_t1p)} und einmal {_t2l} Liter zu {eur(_t2p)}. Der einfache Mittelwert der Preise ist {eur(_t_simple)}. Bezahlt hast du aber im Schnitt {eur(_t_weight)} pro Liter, weil die größere Menge billiger war. Gewicht ist hier die Literzahl. Trag dafür die Preise als Werte und die Liter als Gewichte ein.</div>
<h2>Notenschnitt in Österreich und Deutschland</h2>
<div class="example"><strong>Österreich (Skala 1 bis 5):</strong> Ein Zeugnis mit den Noten 1, 2, 2, 3, 1, 2 hat einen Schnitt von {de(sum((1,2,2,3,1,2))/6,2)}.</div>
<div class="example"><strong>Deutschland (Skala 1 bis 6):</strong> Die Noten 2, 3, 2, 4, 1, 3 ergeben {de(sum((2,3,2,4,1,3))/6,2)}. Zählen die ersten zwei Fächer doppelt, wird daraus (2×2 + 3×2 + 2 + 4 + 1 + 3) ÷ 8 = {de((4+6+2+4+1+3)/8,2)}.</div>
<p>Wie Schulen, Hochschulen oder Behörden einen Schnitt tatsächlich berechnen und runden, steht in der jeweiligen Prüfungsordnung. Der Rechner zeigt den rechnerischen Wert ungerundet.</p>
<h2>Mittelwert, Median und Modus an einem Beispiel</h2>
<p>Acht Bewertungen eines Produkts: {", ".join(str(x) for x in _sample)}.</p>
<table class="tbl text"><thead><tr><th>Kennzahl</th><th>Ergebnis</th><th>Bedeutung</th></tr></thead><tbody>
<tr><td>Mittelwert</td><td>{de(_s_mean,3)}</td><td>Summe ÷ Anzahl</td></tr>
<tr><td>Median</td><td>{de(_s_med,1)}</td><td>Mitte der sortierten Liste ({" ".join(str(x) for x in _s_sorted)})</td></tr>
<tr><td>Modus</td><td>2</td><td>der häufigste Wert</td></tr></tbody></table>
<p>Bei einer geraden Anzahl gibt es keinen einzelnen mittleren Wert. Der Median ist dann der Mittelwert der beiden mittleren Zahlen.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Durchschnitt von Durchschnitten:</strong> Eine Klasse mit {_kl[0][0]} Kindern hat einen Schnitt von {de(_kl[0][1],1)}, eine mit {_kl[1][0]} Kindern {de(_kl[1][1],1)}. Der Gesamtschnitt ist nicht {de(_kl_wrong,2)}, sondern ({_kl[0][0]} × {de(_kl[0][1],1)} + {_kl[1][0]} × {de(_kl[1][1],1)}) ÷ {_kl[0][0]+_kl[1][0]} = {de(_kl_right,2)}. Die größere Gruppe zählt mehr.</div>
<div class="warn"><strong>Leere Werte als Null zählen:</strong> Fehlt eine Note, gehört sie nicht als 0 in die Liste – das würde den Schnitt verfälschen.</div>
<h2>Grenzen</h2>
<p>Schulnoten sind eine Rangfolge, keine Messgröße: Der Abstand zwischen 1 und 2 ist nicht unbedingt gleich groß wie zwischen 4 und 5. Ein Notenschnitt ist deshalb eine praktische Vereinbarung, kein exaktes Maß. Bei sehr wenigen Werten sagt jeder Durchschnitt wenig aus.</p>
{faq([
("Wann nehme ich den Median statt des Mittelwerts?", "Wenn einzelne Ausreißer das Bild verzerren würden – etwa bei Einkommen, Mieten oder Lieferzeiten."),
("Wie viele Werte kann ich eingeben?", "Beliebig viele, getrennt mit Leerzeichen oder Strichpunkt. Kommazahlen schreibst du mit Komma oder Punkt."),
("Müssen sich die Gewichte auf 100 summieren?", "Nein. Der Rechner teilt durch die Summe der Gewichte. 2-2-1 und 40-40-20 ergeben denselben Schnitt."),
])}
"""

DEEP["einheitenrechner"] = f"""
<h2>Der häufigste Fehler: Flächen und Volumen</h2>
<p>Bei Längen ist der Faktor zwischen Meter und Zentimeter 100. Bei Flächen wird er quadriert, bei Volumen hoch drei genommen:</p>
<table class="tbl text"><thead><tr><th>Größe</th><th>Umrechnung</th><th>Faktor</th></tr></thead><tbody>
<tr><td>Länge</td><td>1 m = 100 cm</td><td>100</td></tr><tr><td>Fläche</td><td>1 m² = 10.000 cm²</td><td>100²</td></tr>
<tr><td>Volumen</td><td>1 m³ = 1.000.000 cm³ = 1.000 l</td><td>100³</td></tr><tr><td>Volumen</td><td>1 l = 1 dm³ = 1.000 cm³</td><td>10³</td></tr></tbody></table>
<div class="example"><strong>Beispiel Estrich:</strong> Ein Raum mit 4,2 × 3,5 m hat {de(4.2*3.5,1)} m². Eine 5 cm dicke Schicht sind {de(4.2*3.5,1)} × 0,05 = {de(4.2*3.5*0.05,3)} m³, also {de(4.2*3.5*0.05*1000,0)} Liter. Wer stattdessen 5 cm mit 100 statt mit 0,05 verrechnet, liegt um ein Vielfaches daneben.</div>
<h2>Mengen beim Wirt und in der Küche</h2>
<p>In Österreich bestellt man Wein oft als <strong>Achterl</strong> (⅛ Liter = 125 ml) oder <strong>Vierterl</strong> (250 ml), Bier als <strong>Seidl</strong> (meist 0,3 l) oder <strong>Krügerl</strong> (meist 0,5 l). In Deutschland ist für Wein der <strong>Schoppen</strong> geläufig, dessen Menge regional schwankt. Maßgeblich ist immer die Angabe auf der Karte oder der Eichstrich am Glas.</p>
<p>Löffelangaben in Rezepten sind Richtwerte: Ein Esslöffel fasst rund 15 ml, ein Teelöffel rund 5 ml. Bei Mehl oder Zucker entspricht ein Volumen nicht einem festen Gewicht – 250 ml Mehl wiegen deutlich weniger als 250 ml Zucker.</p>
<h2>Geschwindigkeiten im Ausland</h2>
<p>130 km/h entsprechen {de(130/1.609344,1)} Meilen pro Stunde (mph). Umgekehrt sind 70 mph {de(70*1.609344,1)} km/h. Wer im Ausland ein Mietauto fährt, sollte wissen, in welcher Einheit Tacho und Schilder anzeigen.</p>
<h2>Vorsätze für große und kleine Zahlen</h2>
<table class="tbl text"><thead><tr><th>Vorsatz</th><th>Zeichen</th><th>Faktor</th></tr></thead><tbody>
<tr><td>Giga</td><td>G</td><td>1.000.000.000</td></tr><tr><td>Mega</td><td>M</td><td>1.000.000</td></tr><tr><td>Kilo</td><td>k</td><td>1.000</td></tr>
<tr><td>Milli</td><td>m</td><td>0,001</td></tr><tr><td>Mikro</td><td>µ</td><td>0,000001</td></tr></tbody></table>
<div class="warn"><strong>Sprachfalle Billion:</strong> Das englische „billion“ ist eine deutsche Milliarde (10⁹). Eine deutsche Billion sind 10¹², auf Englisch „trillion“. Bei übersetzten Zahlen also genau hinsehen.</div>
<h2>Grenzen</h2>
<p>Manche Angaben sind Nennmaße und keine exakten Längen: Ein „28-Zoll“-Fahrradreifen ist nicht genau 71,1 cm groß, und Bildschirmdiagonalen werden gerundet angegeben. Historische Einheiten wie das Joch oder der Schoppen hatten je nach Region und Zeit unterschiedliche Werte. Der Rechner verwendet die heute gebräuchliche Definition.</p>
{faq([
("Wie rechne ich Quadratmeter in Quadratfuß um?", f"1 m² sind rund {de(1/0.3048**2,2)} Quadratfuß, weil 1 Fuß 0,3048 m lang ist und der Faktor quadriert wird."),
("Wie viel ist ein Deka?", "Ein Dekagramm sind 10 Gramm. 25 dag Butter sind 250 g."),
("Warum gibt es bei Gallonen zwei Werte?", f"Die US-Gallone hat {de(3.785411784,2)} Liter, die britische (imperiale) {de(4.54609,2)} Liter. Achte darauf, aus welchem Land die Angabe stammt."),
])}
"""

DEEP["fahrtkosten-rechner"] = f"""
<h2>Kilometergeld in Österreich</h2>
<p>Für Dienstreisen mit dem eigenen Pkw beträgt das amtliche Kilometergeld seit 1. Jänner 2025 <strong>{eur(KM_AT)} pro Kilometer</strong>. Es kann für höchstens {de(KM_AT_MAX,0)} Kilometer pro Kalenderjahr steuerfrei ausgezahlt werden. Für Mitfahrerinnen und Mitfahrer sind {eur(KM_AT_MIT)} pro Kilometer vorgesehen. Quelle: {SRC_KM_AT}.</p>
<div class="example"><strong>Beispiel Dienstreise:</strong> Wien – Linz und zurück, 2 × 230 km = {_dr_km} km. Kilometergeld: {_dr_km} × {eur(KM_AT)} = {eur(_dr_kmg)}. Die reinen Spritkosten aus dem Beispiel oben betragen {eur(_dr_sprit)}. Die Differenz von {eur(_dr_kmg-_dr_sprit)} soll Verschleiß, Versicherung, Wertverlust und Service abdecken.</div>
<h2>Entfernungspauschale in Deutschland</h2>
<p>Für den Weg zur ersten Tätigkeitsstätte können Arbeitnehmerinnen und Arbeitnehmer in Deutschland <strong>{eur(EP_DE)} für jeden vollen Kilometer der Entfernung</strong> und jeden Arbeitstag als Werbungskosten ansetzen – höchstens {eur(EP_DE_MAX)} im Jahr; mehr ist möglich, wenn ein eigener oder überlassener Pkw genutzt wird. Gezählt wird die einfache Entfernung, nicht Hin- und Rückweg. Quelle: {SRC_9_ESTG}.</p>
<div class="example"><strong>Beispiel Pendeln:</strong> {_ep_km} km Entfernung, {_ep_days} Arbeitstage: {_ep_km} × {_ep_days} × {eur(EP_DE)} = {eur(_ep)}. Weil ohnehin ein Arbeitnehmer-Pauschbetrag von {eur(AN_PAUSCH)} berücksichtigt wird, wirken sich ohne weitere Werbungskosten nur die {eur(_ep-AN_PAUSCH)} darüber hinaus steuerlich aus. Quelle zum Pauschbetrag: {SRC_9A_ESTG}.</div>
<h2>Spritkosten, Kilometergeld, Vollkosten</h2>
<table class="tbl text"><thead><tr><th>Ansatz</th><th>pro km (Beispiel)</th><th>enthält</th></tr></thead><tbody>
<tr><td>Spritkosten (6,5 l zu 1,70 €)</td><td>{eur(6.5/100*1.70)}</td><td>nur Treibstoff</td></tr>
<tr><td>Kilometergeld Österreich</td><td>{eur(KM_AT)}</td><td>pauschal alle Fahrzeugkosten</td></tr></tbody></table>
<p>Welche Zahl die richtige ist, hängt von der Frage ab: Für das Aufteilen einer Urlaubsfahrt reichen meist die Spritkosten. Für die Frage, was ein eigenes Auto wirklich kostet, sind Vollkosten mit Versicherung, Steuer, Service und Wertverlust ehrlicher.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Entfernung doppelt zählen:</strong> Bei der deutschen Entfernungspauschale zählt nur die einfache Strecke. Wer Hin- und Rückweg ansetzt, kommt im Beispiel auf {eur(_ep_wrong)} statt {eur(_ep)}.</div>
<div class="warn"><strong>Kilometergeld und Pendlerpauschale verwechseln:</strong> Das österreichische Kilometergeld gilt für Dienstreisen, nicht für den täglichen Weg zur Arbeit. Dafür gibt es eigene Regeln.</div>
<h2>Grenzen</h2>
<p>Der Rechner kennt keine Maut, Vignette, Parkgebühren oder Fähren – diese Kosten kommen bei vielen Reisen noch dazu. Steuerliche Fragen im Einzelfall klärst du mit dem Finanzamt oder einer Steuerberatung.</p>
{faq([
("Wie rechne ich den Verbrauch meines Autos selbst aus?", "Getankte Liter ÷ gefahrene Kilometer × 100. Am genauesten wird es, wenn du zweimal vollständig volltankst und dazwischen normal fährst."),
("Zählt die Fahrerin beim Aufteilen mit?", "Im Rechner ja: Die Kosten werden durch alle Personen im Auto geteilt. Soll die Fahrerin nichts zahlen, gib eine Person weniger ein."),
("Lohnt sich Kilometergeld gegenüber den Spritkosten?", f"Im Beispiel deckt das Kilometergeld rund das {de(_dr_kmg/_dr_sprit,1)}-Fache der Spritkosten, weil es alle Fahrzeugkosten abgelten soll."),
])}
"""

DEEP["inflationsrechner"] = f"""
<h2>Die Inflationsraten der letzten Jahre</h2>
<table class="tbl"><thead><tr><th>Jahr</th><th>Deutschland (VPI)</th><th>Österreich (VPI)</th></tr></thead><tbody>
{''.join(f'<tr><td>{y}</td><td>{de(VPI_DE[y],1)} %</td><td>{(de(VPI_AT[y],1) + " %") if y in VPI_AT else "–"}</td></tr>' for y in sorted(VPI_DE))}
</tbody></table>
<p class="small muted">Jahresdurchschnitte. Quellen: {SRC_DESTATIS}; {SRC_STAT_AT}. Für die österreichischen Jahre vor 2024 sind hier nur Werte angegeben, die wir in der verlinkten Quelle geprüft haben.</p>
<h2>Durchgerechnet: Was sind 1.000 € von 2020 heute wert?</h2>
<div class="example"><strong>Deutschland:</strong> Die Preise sind von 2021 bis 2025 insgesamt um ({" × ".join(de(1+v/100,3) for v in VPI_DE.values())} − 1) = {_pct((_de_cum-1)*100)} gestiegen. Was 2020 1.000 € kostete, kostet 2025 im Schnitt {eur(1000*_de_cum)}. Umgekehrt haben 1.000 € nur noch die Kaufkraft von {eur(1000/_de_cum)}.</div>
<div class="example"><strong>Österreich:</strong> Über 2024 und 2025 zusammen ergibt sich 1,029 × 1,036 − 1 = {_pct((_at_cum-1)*100,2)} Teuerung, nicht 2,9 + 3,6 = 6,5 %.</div>
<h2>Wertsicherung mit dem Index berechnen</h2>
<p>Mieten, Unterhaltszahlungen oder Verträge sind oft an den Verbraucherpreisindex gebunden. Gerechnet wird dann nicht mit Raten, sondern mit Indexständen: neuer Betrag = alter Betrag × Index neu ÷ Index alt.</p>
<div class="example">Der österreichische VPI (Basis 2020 = 100) lag im Jahresdurchschnitt 2024 bei {de(VPI_AT_IDX[2024],1)} und 2025 bei {de(VPI_AT_IDX[2025],1)}. Eine Miete von 800 € auf Basis 2024 wäre angepasst {eur(_rent)}. Welcher Monat, welche Indexbasis und welche Schwelle gelten, steht im Vertrag.</div>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Raten addieren:</strong> In Deutschland ergibt die Summe der Raten 2021 bis 2025 {de(_de_sum,1)} %, die tatsächliche Teuerung aber {_pct((_de_cum-1)*100)}. Raten werden multipliziert, weil jedes Jahr auf das höhere Preisniveau aufbaut.</div>
<div class="warn"><strong>Indizes verwechseln:</strong> Neben dem nationalen VPI gibt es den harmonisierten HVPI für EU-Vergleiche. In Deutschland lag er 2025 bei {de(HVPI_DE_25,1)} %, der VPI bei {de(VPI_DE[2025],1)} %. Für Verträge zählt der Index, der im Vertrag steht.</div>
<h2>Grenzen</h2>
<p>Vergangene Raten sagen nichts Sicheres über die Zukunft. Für Planungen über viele Jahre ist eine Spanne – etwa 2 % und 3 % – aussagekräftiger als ein einzelner Wert. Der Rechner nimmt eine gleichbleibende Rate an.</p>
{faq([
("Welche Rate soll ich für die nächsten zehn Jahre eingeben?", "Es gibt keine sichere Zahl. Das Inflationsziel der EZB von 2 % ist ein üblicher Ausgangswert; rechne zusätzlich mit einer höheren Rate, um ein vorsichtiges Szenario zu sehen."),
("Was ist der Unterschied zwischen Inflationsrate und Index?", "Die Rate ist die prozentuale Veränderung zum Vorjahr. Der Index zeigt das Preisniveau im Vergleich zu einem Basisjahr, das auf 100 gesetzt ist."),
("Kann ich auch eine Deflation berechnen?", "Rechnerisch ja: Sinkende Preise erhöhen die Kaufkraft. Der Rechner ist auf positive Raten ausgelegt, weil Deflation in Österreich und Deutschland selten ist."),
])}
"""

DEEP["stundenlohn-rechner"] = f"""
<h2>Mindestlohn in Deutschland umgerechnet</h2>
<p>Der gesetzliche Mindestlohn beträgt seit 1. Jänner 2026 {eur(MILO_26)} brutto je Zeitstunde und ab 1. Jänner 2027 {eur(MILO_27)}. Quelle: {SRC_MILO}.</p>
<div class="example">Bei 40 Wochenstunden ergibt das {eur(MILO_26)} × 40 × 52 ÷ 12 = {eur(_mi_m)} brutto im Monat (12 Gehälter). Ab 2027 sind es {eur(_mi_m27)}. Bei Teilzeit mit 20 Stunden halbiert sich der Betrag entsprechend.</div>
<p>Österreich kennt keinen gesetzlichen Mindestlohn. Die Untergrenzen ergeben sich aus den Kollektivverträgen der jeweiligen Branche.</p>
<h2>Gehälter im Vergleich</h2>
<table class="tbl"><thead><tr><th>Monatsbrutto</th><th>38,5 h, 14 Gehälter</th><th>40 h, 12 Gehälter</th></tr></thead><tbody>
{''.join(f'<tr><td>{eur(m)}</td><td>{eur(m*14/(38.5*52))}</td><td>{eur(m*12/(40*52))}</td></tr>' for m in (2000, 2500, 3000, 3500, 4000))}
</tbody></table>
<p>Die Tabelle zeigt, warum Monatsgehälter aus Österreich und Deutschland nicht direkt vergleichbar sind: Dasselbe Monatsbrutto ergibt bei 14 Gehältern und kürzerer Wochenarbeitszeit einen deutlich höheren Stundenlohn. Für einen fairen Vergleich zwischen den Ländern rechne beide Angebote aufs Jahresbrutto oder auf die Stunde um.</p>
<h2>Der echte Stundenlohn: All-in und Pendelzeit</h2>
<div class="example"><strong>All-in-Vertrag:</strong> 3.500 € brutto, 14 Gehälter, offiziell 38,5 Stunden. Stundenlohn: {eur(_ai_h)}. Werden regelmäßig 5 Stunden pro Woche mehr gearbeitet, die mit dem All-in-Gehalt abgegolten sind, sinkt er auf {eur(_ai_h2)}.</div>
<div class="example"><strong>Pendelzeit mitrechnen:</strong> Wer 3.000 € bei 38,5 Stunden verdient und wöchentlich 5 Stunden pendelt, kommt auf {eur(3000*14/(38.5*52))} pro Arbeitsstunde, aber nur auf {eur(_pend_h)} pro Stunde, die für den Job aufgewendet wird. Das hilft beim Vergleich eines näheren Jobs mit etwas weniger Gehalt.</div>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Mit 4 Wochen pro Monat rechnen:</strong> Ein Monat hat im Schnitt 4,33 Wochen. Wer mit 4 rechnet, setzt bei 40 Wochenstunden 160 statt {de(40*52/12,1)} Stunden an und überschätzt den Stundenlohn um gut 8 %.</div>
<div class="warn"><strong>Urlaub abziehen:</strong> Bezahlter Urlaub ist Teil des Gehalts. In Deutschland stehen mindestens 24 Werktage Urlaub im Jahr zu (bezogen auf eine Sechs-Tage-Woche); dafür wird nicht weniger gezahlt. Quelle: {SRC_BURLG}.</div>
<h2>Grenzen</h2>
<p>Der Rechner arbeitet mit Bruttowerten. Netto hängen Stundenlohn und Monatsgehalt von Lohnsteuer, Sozialversicherung und persönlichen Umständen ab. Zuschläge, Prämien und Sachbezüge sind nicht enthalten.</p>
{faq([
("Wie viele Arbeitsstunden hat ein Jahr?", f"Bei 40 Wochenstunden sind es 40 × 52 = {de(40*52,0)} bezahlte Stunden, bei 38,5 Stunden {de(38.5*52,0)}. Urlaub und Feiertage sind darin enthalten, weil sie bezahlt werden."),
("Wie rechne ich einen Stundenlohn in ein Jahresgehalt um?", "Stundenlohn × Wochenstunden × 52. Für das Monatsgehalt teilst du anschließend durch die Zahl der Gehälter."),
("Ist der Stundenlohn bei Teilzeit niedriger?", "Nein, bei gleichem Vertrag bleibt der Stundenlohn gleich; nur die Zahl der bezahlten Stunden sinkt."),
])}
"""

DEEP["trinkgeld-rechner"] = f"""
<h2>Schnelltabelle: Trinkgeld nach Rechnungsbetrag</h2>
<table class="tbl"><thead><tr><th>Rechnung</th><th>5 %</th><th>10 %</th><th>15 %</th></tr></thead><tbody>
{''.join(f'<tr><td>{eur(b)}</td>' + ''.join(f'<td>{eur(b*p/100)}</td>' for p in (5, 10, 15)) + '</tr>' for b in (12, 25, 48, 80, 150))}
</tbody></table>
<h2>Durchgerechnet in Wien und Berlin</h2>
<div class="example"><strong>Kaffeehaus in Wien:</strong> Zwei Melange und ein Strudel kosten zusammen 15,60 €. Wer auf 17 € aufrundet, gibt {eur(17-15.60)} Trinkgeld, das sind {_pct((17-15.60)/15.60*100)}.</div>
<div class="example"><strong>Restaurant in Berlin:</strong> Eine Rechnung über 63,80 € mit 10 % Trinkgeld ergibt {eur(63.80*1.1)}. Gesagt wird dann meist ein glatter Betrag, etwa „70, bitte“ – das sind {_pct((70-63.80)/63.80*100)} Trinkgeld.</div>
<h2>Was Aufrunden in Prozent bedeutet</h2>
<p>Aufrunden fühlt sich nach wenig an, kann aber je nach Betrag sehr unterschiedlich ausfallen. Die {eur(87.40)} aus dem Beispiel oben auf 90 € aufgerundet sind {_pct(_aufr)}. Bei kleinen Beträgen ist der Prozentsatz schnell hoch: 3,20 € auf 4 € aufgerundet sind schon {_pct(0.8/3.2*100,0)}.</p>
<h2>Trinkgeld und Steuer</h2>
<p>In Deutschland sind Trinkgelder für Angestellte steuerfrei, wenn sie von Gästen freiwillig und ohne Rechtsanspruch zusätzlich zum Rechnungsbetrag gegeben werden. Quelle: {SRC_3_ESTG}. Für dich als Gast ändert das nichts an der Rechnung. Es bedeutet aber, dass ein auf der Karte verpflichtend aufgeschlagenes „Service-Entgelt“ etwas anderes ist als freiwilliges Trinkgeld.</p>
<h2>Typische Fehler</h2>
<div class="warn"><strong>Trinkgeld auf den reduzierten Betrag:</strong> Bei einem Gutschein über 15 € auf eine Rechnung von {eur(_tg_orig)} bezahlst du nur {eur(_tg_paid)}. Das Service hat aber die volle Rechnung betreut. 10 % vom vollen Betrag sind {eur(_tg_orig*0.1)}, vom reduzierten nur {eur(_tg_paid*0.1)}.</div>
<div class="warn"><strong>Doppelt teilen:</strong> Wird erst die Rechnung geteilt und jede Person rundet ihren Anteil auf, kann das Trinkgeld höher oder niedriger ausfallen als gedacht. Einfacher: Gesamtbetrag samt Trinkgeld festlegen und dann teilen.</div>
<h2>Grenzen</h2>
<p>Für die Höhe von Trinkgeld gibt es keine verbindliche Regel. Die Prozentwerte im Rechner sind übliche Größenordnungen, keine Vorgabe. Wie viel du gibst, hängt vom Service, vom Lokal und von deinem Budget ab.</p>
{faq([
("Gebe ich Trinkgeld vom Brutto- oder Nettobetrag?", "Vom Betrag auf der Rechnung, also brutto. Die Umsatzsteuer herauszurechnen ist beim Trinkgeld nicht üblich."),
("Kann ich Trinkgeld mit Karte geben?", "Ja. Nenne beim Bezahlen den Gesamtbetrag inklusive Trinkgeld oder wähle ihn am Kartenterminal, wenn das angeboten wird."),
("Wie viel Trinkgeld beim Lieferdienst?", "Auch hier ist Trinkgeld freiwillig. Viele runden auf oder geben einen festen Betrag von ein, zwei Euro pro Lieferung, unabhängig vom Bestellwert."),
])}
"""
