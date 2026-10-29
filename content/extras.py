"""Vertiefende Abschnitte für die Rechner – werden an den jeweiligen Erklärtext angehängt. Zahlen in Python berechnet."""
import math
from content.calcs import de, eur


def _rate(K, p, years):
    i, m = p / 100 / 12, years * 12
    return K * i / (1 - (1 + i) ** -m)


_r5, _r7, _r10 = _rate(20000, 4.5, 5), _rate(20000, 4.5, 7), _rate(20000, 4.5, 10)
_skonto = 2 / 98 * 360 / 20 * 100
_eff_m = ((1 + 0.03 / 12) ** 12 - 1) * 100

EXTRAS = {
"prozentrechner": f"""
<h2>Drei Rechentricks für den Alltag</h2>
<ul><li><strong>10 % ist eine Kommastelle:</strong> 10 % von 84 € sind 8,40 €. 5 % sind die Hälfte davon (4,20 €), 15 % die Summe aus beidem (12,60 €).</li>
<li><strong>Umdrehen erlaubt:</strong> 8 % von 50 sind dasselbe wie 50 % von 8 – also 4. Das klappt immer, weil beide Male 8 × 50 ÷ 100 gerechnet wird.</li>
<li><strong>1 % als Baustein:</strong> 1 % von 2.350 € sind 23,50 €. 3 % sind dann 70,50 €, 7 % sind {eur(2350*0.07)}.</li></ul>
<h2>Warum +20 % und dann −20 % nicht null ergibt</h2>
<p>Steigt ein Preis von 100 € um 20 % auf 120 € und fällt danach um 20 %, landet er bei 96 € – denn die 20 % beziehen sich beim zweiten Mal auf die größere Basis von 120 €. Um von 120 € wieder auf 100 € zu kommen, braucht es ein Minus von nur {de(20/120*100)} %. Deshalb ist bei Veränderungen immer wichtig, auf welchen Ausgangswert sich die Prozentzahl bezieht.</p>
<h2>Häufige Fragen</h2>
<p><strong>Was ist der Unterschied zwischen Prozent und Prozentpunkten?</strong> Steigt ein Zinssatz von 2 % auf 3 %, ist er um einen Prozentpunkt gestiegen, aber um 50 Prozent. Mehr dazu im Ratgeber <a href="/prozent-oder-prozentpunkte.html">Prozent oder Prozentpunkte</a>.</p>
<p><strong>Kann ein Anteil mehr als 100 % sein?</strong> Ja, wenn der Prozentwert größer ist als der Grundwert: 150 sind 150 % von 100. Bei Anteilen eines Ganzen (etwa Stimmen einer Wahl) ist bei 100 % Schluss.</p>
""",
"mehrwertsteuer-rechner": f"""
<h2>Der klassische Fehler beim Herausrechnen</h2>
<p>Wer von 119 € einfach 19 % abzieht, bekommt {eur(119*0.81)} – und liegt falsch. Die 19 % wurden auf den Nettopreis aufgeschlagen, nicht auf den Bruttopreis. Richtig ist: 119 € ÷ 1,19 = 100 €. Der Rechner nimmt dir diese Division ab.</p>
<h2>Wie viel Steuer steckt im Bruttopreis?</h2>
<p>Für den schnellen Überblick hilft der Anteil der Steuer am Bruttobetrag:</p>
<ul><li>20 % USt (Österreich): {de(20/120*100)} % des Bruttopreises sind Steuer – also ein Sechstel.</li>
<li>19 % USt (Deutschland): {de(19/119*100)} % des Bruttopreises.</li>
<li>10 % USt: {de(10/110*100)} % · 7 % USt: {de(7/107*100)} % · 13 % USt: {de(13/113*100)} %.</li></ul>
<p>Bei einem Einkauf um 60 € brutto in Österreich sind also 10 € Umsatzsteuer enthalten.</p>
<h2>Umsatzsteuer, Mehrwertsteuer, Vorsteuer</h2>
<p>Umsatzsteuer und Mehrwertsteuer meinen im Alltag dasselbe; im Gesetz heißt sie Umsatzsteuer. Unternehmen schlagen sie auf ihre Preise auf und führen sie ans Finanzamt ab. Die Steuer, die sie selbst beim Einkauf zahlen, holen sie sich als <strong>Vorsteuer</strong> zurück. Wirtschaftlich trägt sie deshalb die Endkundin oder der Endkunde. Kleinunternehmer sind von der Umsatzsteuer befreit und weisen auf ihren Rechnungen keine aus.</p>
<p class="small muted">Welcher Steuersatz für welche Ware oder Leistung gilt, regeln das österreichische und das deutsche Umsatzsteuergesetz. Im Zweifel hilft die Steuerberatung.</p>
""",
"rabatt-rechner": f"""
<h2>Zwei Rabatte sind nicht die Summe</h2>
<p>20 % Rabatt und zusätzlich 10 % sind nicht 30 %, sondern 28 %: Der zweite Rabatt wird vom bereits reduzierten Preis abgezogen. 100 € × 0,8 × 0,9 = 72 €. Die Reihenfolge spielt dabei keine Rolle – 10 % zuerst und dann 20 % ergibt ebenfalls 72 €.</p>
<h2>Euro-Rabatt und Prozent-Rabatt: Hier zählt die Reihenfolge</h2>
<p>Gibt es einen Gutschein über 10 € und zusätzlich 10 % Rabatt, ist die Reihenfolge entscheidend. Bei 100 €: erst 10 € abziehen, dann 10 % ergibt {eur((100-10)*0.9)}. Erst 10 %, dann 10 € ergibt {eur(100*0.9-10)}. Für Kundinnen und Kunden ist es günstiger, wenn der Prozent-Rabatt zuerst angewendet wird.</p>
<h2>Skonto: der unterschätzte Zins</h2>
<p>„2 % Skonto bei Zahlung binnen 10 Tagen, sonst 30 Tage netto“ klingt nach wenig. Wer das Skonto nicht nutzt, bezahlt aber 2 % dafür, das Geld 20 Tage länger zu behalten. Aufs Jahr gerechnet entspricht das einem Zinssatz von rund {de(_skonto,1)} %. Selbst ein Überziehungsrahmen ist meist günstiger – Skonto auszunutzen lohnt sich fast immer.</p>
""",
"zinseszins-rechner": f"""
<h2>Monatliche oder jährliche Verzinsung?</h2>
<p>Banken nennen meist einen Jahreszinssatz. Werden die Zinsen monatlich gutgeschrieben, verzinsen sie sich schon im Laufe des Jahres mit. Aus 3 % pro Jahr werden bei monatlicher Gutschrift effektiv {de(_eff_m,3)} %. Der Unterschied ist klein, summiert sich über Jahrzehnte aber.</p>
<h2>Die 72er-Regel</h2>
<p>Wie lange dauert es, bis sich ein Betrag verdoppelt? Teile 72 durch den Zinssatz: Bei 3 % sind es rund 24 Jahre, bei 6 % rund 12 Jahre. Genau gerechnet sind es bei 3 % {de(math.log(2)/math.log(1.03),1)} Jahre. Mehr dazu im Ratgeber <a href="/zinseszins-und-72er-regel.html">Zinseszins und 72er-Regel</a>.</p>
<h2>Was der Rechner nicht berücksichtigt</h2>
<ul><li><strong>Steuern:</strong> Zinserträge sind steuerpflichtig – in Österreich über die Kapitalertragsteuer, in Deutschland über die Abgeltungsteuer. Der Rechner zeigt Werte vor Steuern.</li>
<li><strong>Inflation:</strong> Das Endkapital ist ein Nominalbetrag. Was es in 20 Jahren wert ist, zeigt der <a href="/inflationsrechner.html">Inflationsrechner</a>.</li>
<li><strong>Schwankungen:</strong> Bei Aktien oder Fonds gibt es keinen festen Zins. Eine angenommene Durchschnittsrendite ist nur ein Szenario, keine Zusage.</li></ul>
""",
"kreditrechner": f"""
<h2>Längere Laufzeit: niedrigere Rate, höhere Kosten</h2>
<p>Bei 20.000 € und 4,5 % Sollzins:</p>
<ul><li>5 Jahre: Rate {eur(_r5)}, Zinskosten {eur(_r5*60-20000)}</li>
<li>7 Jahre: Rate {eur(_r7)}, Zinskosten {eur(_r7*84-20000)}</li>
<li>10 Jahre: Rate {eur(_r10)}, Zinskosten {eur(_r10*120-20000)}</li></ul>
<p>Die doppelte Laufzeit senkt die Rate um rund {de((1-_r10/_r5)*100,0)} %, mehr als verdoppelt aber die Zinskosten. Eine gute Faustregel: so kurz wie möglich, so lang wie nötig – die Rate sollte auch dann noch tragbar sein, wenn unerwartete Ausgaben kommen.</p>
<h2>Warum am Anfang vor allem Zinsen gezahlt werden</h2>
<p>Bei einem Annuitätenkredit bleibt die Rate gleich. Zinsen fallen aber immer auf die aktuelle Restschuld an – und die ist am Anfang am höchsten. Deshalb ist der Zinsanteil zu Beginn groß und schrumpft mit jeder Rate, während der Tilgungsanteil wächst. Das Diagramm über dem Tilgungsplan zeigt genau diese Verschiebung.</p>
<h2>Sollzins, Effektivzins, Sondertilgung</h2>
<p>Der <strong>Sollzins</strong> ist der reine Zins auf die Restschuld. Der <strong>effektive Jahreszins</strong> enthält zusätzlich Kosten wie Bearbeitungsgebühren und ist deshalb die bessere Zahl zum Vergleichen von Angeboten. Erlaubt der Vertrag <strong>Sondertilgungen</strong>, senkt jede Zahlung die Restschuld sofort – und damit alle künftigen Zinsen. Details im Ratgeber <a href="/sollzins-und-effektivzins.html">Sollzins und Effektivzins</a>.</p>
""",
"inflationsrechner": f"""
<h2>Wann sich die Kaufkraft halbiert</h2>
<p>Bei 2 % Inflation pro Jahr ist Geld nach rund {de(math.log(2)/math.log(1.02),0)} Jahren nur noch die Hälfte wert, bei 3 % nach rund {de(math.log(2)/math.log(1.03),0)} Jahren, bei 5 % schon nach rund {de(math.log(2)/math.log(1.05),0)} Jahren. Als Faustregel teilt man 70 durch die Inflationsrate.</p>
<h2>Realzins: was vom Zins übrig bleibt</h2>
<p>Der Realzins zeigt, ob Erspartes tatsächlich mehr wert wird. Näherungsweise ist er der Zins minus die Inflation. Genauer: (1 + Zins) ÷ (1 + Inflation) − 1. Bei 3 % Zinsen und 2 % Inflation bleiben real {de((1.03/1.02-1)*100)} % – nach Steuern entsprechend weniger.</p>
<h2>Persönliche Inflation</h2>
<p>Die offizielle Inflationsrate beruht auf einem durchschnittlichen Warenkorb. Wer überdurchschnittlich viel für Energie, Miete oder Lebensmittel ausgibt, erlebt eine andere, „persönliche“ Teuerung. Für eigene Überlegungen kann es sinnvoll sein, mit einer etwas höheren Rate zu rechnen als dem offiziellen Wert.</p>
""",
"dreisatz-rechner": f"""
<h2>Proportional oder umgekehrt?</h2>
<p>Die entscheidende Frage: Wenn eine Größe steigt, steigt die andere mit (je mehr, desto mehr) – oder sinkt sie (je mehr, desto weniger)?</p>
<ul><li><strong>Proportional:</strong> Ein Rezept für 4 Personen braucht 300 g Mehl. Für 6 Personen: 300 ÷ 4 × 6 = 450 g.</li>
<li><strong>Umgekehrt proportional:</strong> 4 Personen streichen eine Wohnung in 6 Tagen. 3 Personen brauchen dafür 4 × 6 ÷ 3 = 8 Tage.</li></ul>
<h2>Wann der Dreisatz nicht passt</h2>
<p>Der Dreisatz setzt voraus, dass sich die Größen gleichmäßig verhalten. Bei einer Taxifahrt mit Grundgebühr stimmt das nicht: Kostet die erste Strecke von 5 km 15 € inklusive 4 € Grundgebühr, kosten 10 km nicht 30 €, sondern 4 € + 2 × 11 € = 26 €. Auch Mengenrabatte, Staffelpreise oder Steuertarife folgen keinem Dreisatz.</p>
<h2>Doppelter Dreisatz</h2>
<p>Hängt ein Ergebnis von zwei Größen ab, rechnet man zwei Dreisätze hintereinander: 3 Maschinen stellen in 4 Stunden 600 Teile her. Wie viele schaffen 5 Maschinen in 6 Stunden? Erst auf 1 Maschine (200 Teile in 4 Stunden), dann auf 1 Stunde (50 Teile), dann hochrechnen: 50 × 5 × 6 = 1.500 Teile.</p>
""",
"bruchrechner": f"""
<h2>Die vier Regeln auf einen Blick</h2>
<ul><li><strong>Plus und Minus:</strong> Erst auf einen gemeinsamen Nenner bringen, dann die Zähler verrechnen. 1/4 + 1/6 = 3/12 + 2/12 = 5/12.</li>
<li><strong>Mal:</strong> Zähler mal Zähler, Nenner mal Nenner. 2/3 × 3/4 = 6/12 = 1/2.</li>
<li><strong>Geteilt:</strong> Mit dem Kehrwert malnehmen. 2/3 ÷ 4/5 = 2/3 × 5/4 = 10/12 = 5/6.</li>
<li><strong>Kürzen:</strong> Zähler und Nenner durch ihren größten gemeinsamen Teiler teilen.</li></ul>
<h2>Warum Teilen durch einen Bruch Malnehmen mit dem Kehrwert ist</h2>
<p>„Wie oft passt 1/4 in 3?“ – zwölfmal, denn in jedes Ganze passen vier Viertel. 3 ÷ 1/4 = 3 × 4 = 12. Der Kehrwert sagt also, wie viele Teile auf ein Ganzes kommen.</p>
<h2>Brüche und Kommazahlen</h2>
<p>Manche Brüche werden zu endlichen Dezimalzahlen (1/8 = 0,125), andere laufen unendlich weiter (1/3 = 0,333…). Endlich wird ein gekürzter Bruch genau dann, wenn sein Nenner nur die Primfaktoren 2 und 5 enthält. Deshalb rechnet man mit 1/3 oft genauer als mit 0,33.</p>
""",
"einheitenrechner": f"""
<h2>Einheiten, die man in Österreich kennen sollte</h2>
<ul><li><strong>Dekagramm (dag):</strong> 1 dag = 10 g. Beim Fleischhauer bestellt man „20 Deka Extrawurst“ – also 200 g.</li>
<li><strong>Joch:</strong> ein historisches Flächenmaß, das in der Landwirtschaft noch vorkommt. Ein Katastraljoch sind rund 5.755 m², gut ein halber Hektar.</li></ul>
<h2>Größenvergleiche, die helfen</h2>
<ul><li>Ein Hektar sind 10.000 m² – etwa {de(10000/(105*68),1)} Fußballfelder mit 105 × 68 Metern.</li>
<li>Ein 55-Zoll-Fernseher hat eine Bildschirmdiagonale von {de(55*2.54,1)} cm.</li>
<li>100 km/h sind {de(100/3.6,1)} Meter pro Sekunde – bei einer Sekunde Reaktionszeit fährt man also knapp 28 Meter ungebremst weiter.</li></ul>
<h2>Fahrenheit im Kopf umrechnen</h2>
<p>Für eine grobe Schätzung reicht: °C × 2 + 30. 20 °C ergeben so 70 °F (genau: 68 °F). In die andere Richtung: (°F − 30) ÷ 2. Für Rezepte aus den USA ist der genaue Wert wichtiger – 350 °F sind {de((350-32)*5/9,0)} °C.</p>
""",
"durchschnitt-rechner": f"""
<h2>Die Falle mit der Durchschnittsgeschwindigkeit</h2>
<p>Hin fährst du mit 60 km/h, zurück mit 40 km/h. Der Durchschnitt ist nicht 50 km/h, sondern 48 km/h: Für 60 km Strecke brauchst du hin eine Stunde und zurück anderthalb Stunden – 120 km in 2,5 Stunden. Bei Geschwindigkeiten über gleiche Strecken braucht es das <strong>harmonische Mittel</strong>.</p>
<h2>Durchschnittliche Wachstumsrate</h2>
<p>Steigt ein Wert ein Jahr um 10 % und fällt im nächsten um 10 %, ist der Durchschnitt nicht 0 %. Aus 100 werden 110, dann 99. Für Renditen über mehrere Jahre nimmt man deshalb das <strong>geometrische Mittel</strong>: (1,1 × 0,9)<sup>1/2</sup> − 1 = {de(((1.1*0.9)**0.5-1)*100)} % pro Jahr.</p>
<h2>Wann der Median die bessere Wahl ist</h2>
<p>Bei Einkommen, Mieten oder Hauspreisen ziehen wenige sehr hohe Werte den Mittelwert nach oben. Der Median – der Wert in der Mitte – beschreibt dann besser, was „typisch“ ist. Deshalb berichten Statistikämter beim Einkommen meist den Median.</p>
""",
"stundenlohn-rechner": f"""
<h2>Überstunden richtig bewerten</h2>
<p>In Österreich gebührt für Überstunden ein Zuschlag von 50 % (§ 10 Arbeitszeitgesetz), sofern Kollektivvertrag oder Vereinbarung nichts Günstigeres vorsehen. Bei einem Stundenlohn von 20 € ist eine Überstunde also 30 € brutto wert. In Deutschland gibt es keinen gesetzlichen Überstundenzuschlag; er ergibt sich aus Tarif- oder Arbeitsvertrag.</p>
<h2>Teilzeit fair vergleichen</h2>
<p>Wer von 38,5 auf 30 Stunden reduziert, verdient im gleichen Verhältnis weniger: 30 ÷ 38,5 = {de(30/38.5*100,1)} % des bisherigen Gehalts. Der Stundenlohn bleibt gleich. Netto fällt der Unterschied wegen der progressiven Lohnsteuer oft etwas kleiner aus.</p>
<h2>Selbstständig: Stundensatz ist nicht Stundenlohn</h2>
<p>Wer selbstständig arbeitet, muss mit dem Stundensatz auch Urlaub, Krankheit, Sozialversicherung, Ausstattung und Zeiten ohne Aufträge finanzieren. Bei rund 1.000 bis 1.200 tatsächlich verrechenbaren Stunden pro Jahr liegt ein kostendeckender Stundensatz meist beim Doppelten oder mehr des vergleichbaren Angestellten-Stundenlohns.</p>
""",
}
