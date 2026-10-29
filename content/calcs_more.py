"""Weitere Rechner: Stromkosten, Fahrtkosten, Trinkgeld, Aufschlag & Marge. Beispiele in Python berechnet."""
from content.calcs import form, inp, select, de, eur

# ---------- Beispielwerte
_kettle_kwh = 2000 * (10 / 60) / 1000 * 365
_stby_kwh = 10 * 24 * 365 / 1000
_l = 230 * 6.5 / 100
_trip = _l * 1.70
_ev_kwh = 230 * 18 / 100
_bill, _tip = 87.40, 0.10
_ek, _vk = 60, 100

PRESETS = [("", "eigene Werte"), ("10|24", "WLAN-Router (10 W, 24 h)"), ("100|4", "Fernseher (100 W, 4 h)"),
           ("2000|0.17", "Wasserkocher (2.000 W, 10 min)"), ("50|6", "Laptop (50 W, 6 h)"), ("200|4", "Gaming-PC (200 W, 4 h)"),
           ("150|2", "Spielkonsole (150 W, 2 h)"), ("2000|1", "Heizlüfter (2.000 W, 1 h)"), ("5|24", "Gerät im Standby (5 W, 24 h)")]

MORE = [
{
"slug": "stromkosten-rechner", "short": "Stromkosten-Rechner", "sym": "kWh",
"teaser": "Was ein Gerät pro Jahr an Strom kostet – auch im Standby.",
"title": "Stromkosten-Rechner: Verbrauch & Kosten pro Gerät berechnen",
"h1": "Stromkosten-Rechner",
"lead": "Wie viel kostet der Fernseher, der Router oder der Heizlüfter im Jahr? Leistung in Watt, Nutzungsdauer und Strompreis eingeben – oder den Jahresverbrauch vom Energielabel.",
"description": "Stromkosten berechnen: Verbrauch in kWh und Kosten pro Tag, Monat und Jahr für jedes Gerät – mit Standby-Kosten, Energielabel-Modus und Rechenweg.",
"formula": "kWh = Watt × Stunden ÷ 1.000 · Kosten = kWh × Preis",
"form": form("strom", select("mode", "Ich kenne …", [("watt", "die Leistung in Watt"), ("label", "den Jahresverbrauch (Energielabel)")], "watt")
    + f'<div data-show-when="mode=watt" class="fields sub">{select("preset", "Beispielgerät", PRESETS, "100|4")}{inp("watt", "Leistung (Watt)", "100")}{inp("hours", "Stunden pro Tag", "4")}{inp("days", "Tage pro Jahr", "365", "numeric")}</div>'
    + f'<div data-show-when="mode=label" class="fields sub">{inp("kwh", "Verbrauch laut Label (kWh/Jahr)", "150")}</div>'
    + inp("price", "Strompreis (Cent pro kWh)", "30")),
"body": f"""
<h2>So rechnest du Stromkosten aus</h2>
<p>Strom wird in Kilowattstunden (kWh) abgerechnet. Eine Kilowattstunde ist das, was ein Gerät mit 1.000 Watt in einer Stunde verbraucht. Die Rechnung hat deshalb immer drei Schritte:</p>
<ol><li><strong>Leistung × Zeit:</strong> Watt mal Stunden ergibt Wattstunden.</li><li><strong>Durch 1.000:</strong> aus Wattstunden werden Kilowattstunden.</li><li><strong>Mal Strompreis:</strong> Kilowattstunden mal Preis pro kWh ergibt die Kosten.</li></ol>
<div class="example"><strong>Beispiel Wasserkocher:</strong> 2.000 W, jeden Tag 10 Minuten. Pro Tag: 2.000 × 1/6 h ÷ 1.000 = {de(2000/6/1000,3)} kWh. Pro Jahr: {de(_kettle_kwh,1)} kWh. Bei 30 Cent pro kWh kostet das {eur(_kettle_kwh*0.30)} im Jahr.</div>
<h2>Standby: kleine Leistung, lange Laufzeit</h2>
<p>Geräte, die rund um die Uhr laufen, fallen stärker ins Gewicht, als ihre Wattzahl vermuten lässt. Schon 10 Watt Dauerbetrieb ergeben {de(_stby_kwh,1)} kWh im Jahr, bei 30 Cent also {eur(_stby_kwh*0.30)}. Ein Wasserkocher mit der 200-fachen Leistung kostet im Jahr ähnlich viel – weil er nur wenige Minuten am Tag läuft.</p>
<p>Ob ein Gerät im Standby Strom zieht, zeigt ein Strommessgerät aus dem Baumarkt am zuverlässigsten. Steckerleisten mit Schalter trennen mehrere Geräte auf einmal vom Netz.</p>
<h2>Kühlschrank, Waschmaschine & Co.: das Energielabel nutzen</h2>
<p>Bei Geräten, die nicht durchgehend mit voller Leistung laufen, hilft die Wattzahl wenig: Ein Kühlschrank-Kompressor schaltet sich ständig ein und aus. Hier ist der Jahresverbrauch vom EU-Energielabel die bessere Grundlage. Wähle oben „den Jahresverbrauch (Energielabel)“ und trage die kWh-Angabe ein. Bei Waschmaschinen und Geschirrspülern bezieht sich das Label auf 100 Programmdurchläufe – dann den Wert entsprechend umrechnen.</p>
<h2>Welchen Strompreis eingeben?</h2>
<p>Am genauesten ist der <strong>Arbeitspreis</strong> aus deiner Stromrechnung, in Cent pro kWh brutto. Die Grundgebühr gehört nicht dazu: Sie fällt unabhängig davon an, wie viel du verbrauchst, und ändert sich durch ein einzelnes Gerät nicht. Die 30 Cent im Rechner sind nur ein Startwert.</p>
<div class="warn"><strong>Richtwerte:</strong> Die Beispielgeräte nutzen typische Größenordnungen. Die tatsächliche Leistung steht auf dem Typenschild oder im Datenblatt deines Geräts.</div>
""",
"related": [],
},
{
"slug": "fahrtkosten-rechner", "short": "Fahrtkosten-Rechner", "sym": "km",
"teaser": "Sprit- oder Ladekosten einer Fahrt, fair aufgeteilt.",
"title": "Fahrtkosten-Rechner: Spritkosten & Ladekosten pro Fahrt und Person",
"h1": "Fahrtkosten-Rechner",
"lead": "Was kostet die Fahrt in den Urlaub, und wie viel zahlt jeder Mitfahrer? Für Benzin, Diesel und Elektroauto – mit Hin- und Rückfahrt.",
"description": "Spritkosten berechnen: Kosten einer Autofahrt aus Strecke, Verbrauch und Preis, aufgeteilt auf Mitfahrer – auch für Elektroautos.",
"formula": "Kosten = km × Verbrauch ÷ 100 × Preis",
"form": form("fahrt", select("fuel", "Antrieb", [("fuel", "Benzin / Diesel"), ("ev", "Elektro")], "fuel")
    + inp("km", "Strecke einfach (km)", "230") + select("trip", "Fahrt", [("1", "nur hin"), ("2", "hin und zurück")], "2")
    + inp("cons", "Verbrauch (l/100 km)", "6.5") + inp("price", "Preis (€/l)", "1.70") + inp("people", "Personen im Auto", "3", "numeric")),
"body": f"""
<h2>Spritkosten in drei Schritten</h2>
<ol><li><strong>Verbrauch der Strecke:</strong> Kilometer × Verbrauch pro 100 km ÷ 100.</li><li><strong>Kosten:</strong> Liter × Preis pro Liter.</li><li><strong>Aufteilen:</strong> Kosten ÷ Anzahl der Personen.</li></ol>
<div class="example"><strong>Beispiel:</strong> 230 km bei 6,5 l/100 km brauchen {de(_l)} Liter. Bei 1,70 € pro Liter kostet die einfache Fahrt {eur(_trip)}, hin und zurück {eur(_trip*2)}. Zu dritt zahlt jede Person {eur(_trip*2/3)}.</div>
<h2>Elektroauto: Ladekosten statt Spritkosten</h2>
<p>Beim E-Auto steht der Verbrauch in kWh pro 100 km. 230 km mit 18 kWh/100 km brauchen {de(_ev_kwh,1)} kWh. Zuhause geladen zu 30 Cent sind das {eur(_ev_kwh*0.30)}. An öffentlichen Schnellladern ist die Kilowattstunde oft deutlich teurer – trag deshalb den Preis ein, den du tatsächlich zahlst. Ladeverluste von einigen Prozent kommen in der Praxis dazu.</p>
<h2>Welcher Verbrauch ist realistisch?</h2>
<p>Die Herstellerangabe nach WLTP liegt meist unter dem Alltagsverbrauch. Besser ist dein eigener Wert: Tank volltanken, Kilometerstand notieren, beim nächsten Volltanken die getankten Liter durch die gefahrenen Kilometer teilen und mal 100 nehmen. Autobahn mit hohem Tempo, Dachbox und Kälte erhöhen den Verbrauch spürbar.</p>
<h2>Fair teilen bei Fahrgemeinschaften</h2>
<p>Der Rechner teilt die reinen Energiekosten gleichmäßig auf alle Personen im Auto auf – also auch auf die Fahrerin oder den Fahrer. Wer zusätzlich Verschleiß, Versicherung und Wertverlust einrechnen will, landet schnell beim Doppelten. Ein gängiger Kompromiss bei Mitfahrgelegenheiten: Spritkosten teilen, Maut und Parken extra.</p>
""",
"related": [],
},
{
"slug": "trinkgeld-rechner", "short": "Trinkgeld-Rechner", "sym": "♨",
"teaser": "Trinkgeld ausrechnen und die Rechnung gerecht teilen.",
"title": "Trinkgeld-Rechner: Trinkgeld berechnen & Rechnung teilen",
"h1": "Trinkgeld-Rechner",
"lead": "Wie viel Trinkgeld sind 10 Prozent, und was zahlt jeder, wenn ihr die Rechnung teilt? Mit Aufrunden auf einen glatten Betrag.",
"description": "Trinkgeld berechnen und Rechnung teilen: Prozentsatz wählen, auf glatte Beträge aufrunden und den Anteil pro Person sehen – mit Tipps zu Trinkgeld in Österreich und Deutschland.",
"formula": "Gesamt = Rechnung × (1 + Trinkgeld %) · pro Person = Gesamt ÷ Personen",
"form": form("tip", inp("bill", "Rechnungsbetrag (€)", "87.40") + select("pct", "Trinkgeld", [("0", "kein Trinkgeld"), ("5", "5 %"), ("8", "8 %"), ("10", "10 %"), ("12", "12 %"), ("15", "15 %")], "10")
    + select("round", "Aufrunden auf", [("0", "nicht runden"), ("0.5", "50 Cent"), ("1", "1 €"), ("5", "5 €")], "1") + inp("people", "Personen", "4", "numeric")),
"body": f"""
<h2>Trinkgeld ausrechnen</h2>
<p>Trinkgeld wird auf den Rechnungsbetrag aufgeschlagen: Rechnung × Prozentsatz ÷ 100. Viele runden das Ergebnis danach auf einen glatten Betrag auf – das geht beim Bezahlen schneller und fühlt sich großzügiger an.</p>
<div class="example"><strong>Beispiel:</strong> Rechnung {eur(_bill)}, 10 % Trinkgeld = {eur(_bill*_tip)}. Zusammen {eur(_bill*(1+_tip))}, aufgerundet auf den nächsten Euro 97,00 €. Zu viert zahlt jede Person 24,25 €.</div>
<h2>Wie viel Trinkgeld ist üblich?</h2>
<p>In Österreich und Deutschland ist Trinkgeld freiwillig. Die Bedienung ist in den Preisen auf der Karte bereits enthalten. Üblich ist trotzdem, bei gutem Service etwa 5 bis 10 Prozent zu geben oder den Betrag aufzurunden. Im Café reicht oft das Aufrunden, im Restaurant mit Tischservice sind 10 Prozent eine gängige Größe.</p>
<p>Trinkgeld sagt man in der Regel beim Bezahlen an: Statt „Stimmt so“ beim Bargeld nennst du bei der Kartenzahlung den Gesamtbetrag, zum Beispiel „Machen Sie 97“.</p>
<h2>Rechnung gerecht teilen</h2>
<p>Gleich teilen ist am einfachsten, aber nicht immer fair: Wer nur einen Salat hatte, zahlt dann für das Steak der anderen mit. Eine faire Alternative: Jede Person zahlt ihre eigenen Posten plus den gleichen Trinkgeld-Prozentsatz darauf. Dafür einfach die eigene Summe oben als Rechnungsbetrag eintragen und „1 Person“ wählen.</p>
<h2>Trinkgeld im Ausland</h2>
<p>In den USA gehören 15 bis 20 Prozent zum Standard, weil das Personal stark davon lebt. In Japan dagegen ist Trinkgeld unüblich und kann sogar irritieren. Wer reist, informiert sich am besten vorab über die Gepflogenheiten im Zielland.</p>
""",
"related": [],
},
{
"slug": "aufschlag-marge-rechner", "short": "Aufschlag & Marge", "sym": "±",
"teaser": "Kalkulationsaufschlag und Handelsspanne – und warum sie nicht dasselbe sind.",
"title": "Aufschlag- & Margenrechner: Handelsspanne, Kalkulationsaufschlag, Verkaufspreis",
"h1": "Aufschlag & Marge berechnen",
"lead": "Aus Einkaufs- und Verkaufspreis Aufschlag und Handelsspanne berechnen – oder den Verkaufspreis für einen gewünschten Aufschlag oder eine Zielmarge.",
"description": "Handelsspanne und Kalkulationsaufschlag berechnen, Verkaufspreis kalkulieren und Marge in Aufschlag umrechnen – mit Rechenweg und Umsatzsteuer.",
"formula": "Aufschlag = Gewinn ÷ Einkauf · Spanne = Gewinn ÷ Verkauf",
"form": form("marge", select("mode", "Was ist bekannt?", [("ekvk", "Einkaufs- und Verkaufspreis"), ("auf", "Einkaufspreis und Aufschlag"), ("span", "Einkaufspreis und Zielmarge")], "ekvk")
    + inp("ek", "Einkaufspreis netto (€)", "60") + inp("b", "Verkaufspreis netto (€)", "100")
    + select("vat", "Umsatzsteuer für den Bruttopreis", [("20", "20 % (Österreich)"), ("10", "10 % (Österreich, ermäßigt)"), ("19", "19 % (Deutschland)"), ("7", "7 % (Deutschland, ermäßigt)"), ("0", "ohne")], "20")),
"body": f"""
<h2>Aufschlag und Spanne: gleicher Gewinn, andere Basis</h2>
<p>Kaufst du um {eur(_ek)} ein und verkaufst um {eur(_vk)} (beides netto), bleiben {eur(_vk-_ek)} Rohgewinn. Wie viel Prozent das sind, hängt davon ab, worauf du dich beziehst:</p>
<ul><li><strong>Kalkulationsaufschlag</strong> – bezogen auf den Einkaufspreis: {eur(_vk-_ek)} ÷ {eur(_ek)} = {de((_vk-_ek)/_ek*100)} %.</li>
<li><strong>Handelsspanne (Marge)</strong> – bezogen auf den Verkaufspreis: {eur(_vk-_ek)} ÷ {eur(_vk)} = {de((_vk-_ek)/_vk*100)} %.</li></ul>
<p>Beide Werte beschreiben denselben Gewinn. Der Aufschlag ist immer die größere Zahl.</p>
<h2>Der häufigste Kalkulationsfehler</h2>
<p>Wer 40 % Marge erzielen will und deshalb 40 % auf den Einkaufspreis aufschlägt, landet zu niedrig: 60 € + 40 % = 84 €. Die Spanne beträgt dann nur {de(24/84*100)} %. Für echte 40 % Marge muss der Verkaufspreis 60 € ÷ (1 − 0,40) = {eur(60/0.6)} betragen.</p>
<div class="example"><strong>Umrechnen:</strong> Spanne = Aufschlag ÷ (1 + Aufschlag) · Aufschlag = Spanne ÷ (1 − Spanne). Ein Aufschlag von 100 % entspricht einer Spanne von 50 %; eine Spanne von 25 % entspricht einem Aufschlag von {de(0.25/0.75*100)} %.</div>
<h2>Netto rechnen, brutto verkaufen</h2>
<p>Aufschlag und Spanne werden mit Nettopreisen gerechnet, denn die Umsatzsteuer gehört nicht dir, sondern wird ans Finanzamt abgeführt. Der Rechner zeigt zusätzlich den Bruttopreis für Endkunden. Ein Preis von 100 € netto ist in Österreich mit 20 % USt {eur(120)} brutto, in Deutschland mit 19 % {eur(119)}.</p>
<h2>Rohgewinn ist nicht Reingewinn</h2>
<p>Die Spanne deckt erst einmal Miete, Personal, Versand, Zahlungsgebühren und Retouren. Was danach übrig bleibt, ist der eigentliche Gewinn. Gerade im Onlinehandel sind Gebühren von Marktplätzen und Zahlungsanbietern schnell 10 bis 15 Prozent des Verkaufspreises – sie lassen sich als Teil des Einkaufspreises mitrechnen, um eine realistische Marge zu sehen.</p>
""",
"related": ["mehrwertsteuer-herausrechnen", "rabatte-kombinieren"],
},
]
