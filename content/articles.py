"""Ratgeber-Artikel für Rechenklarheit."""
from content.calcs import de, eur

ARTICLES = [
{
"slug": "prozent-oder-prozentpunkte",
"title": "Prozent oder Prozentpunkte? Der Unterschied mit Beispielen",
"teaser": "Von 2 auf 3 % sind ein Prozentpunkt – aber 50 Prozent mehr.",
"description": "Prozent und Prozentpunkte verständlich erklärt: wann man welches Wort verwendet und warum die Verwechslung bei Zinsen und Wahlen so häufig ist.",
"body": f"""
<p>Prozentpunkte beschreiben den Abstand zwischen zwei Prozentzahlen. Prozent beschreiben das Verhältnis. Steigt ein Zinssatz von 2 % auf 3 %, ist er um <strong>einen Prozentpunkt</strong> gestiegen – aber um <strong>50 Prozent</strong>, weil 1 die Hälfte von 2 ist.</p>
<h2>Faustregel</h2>
<ul><li><strong>Prozentpunkte:</strong> Du ziehst zwei Prozentzahlen voneinander ab. 3 % − 2 % = 1 Prozentpunkt.</li>
<li><strong>Prozent:</strong> Du setzt die Veränderung ins Verhältnis zum Ausgangswert. (3 − 2) ÷ 2 × 100 = 50 %.</li></ul>
<h2>Wo die Verwechslung teuer wird</h2>
<div class="example"><strong>Kreditzinsen:</strong> Ein Anstieg von 4 % auf 5 % klingt nach „nur einem Prozent“. Tatsächlich steigen die Zinskosten um ein Viertel, also 25 %.</div>
<div class="example"><strong>Wahlergebnisse:</strong> Legt eine Partei von 10 % auf 12 % zu, gewinnt sie 2 Prozentpunkte – aber 20 % mehr Stimmen als zuvor.</div>
<div class="example"><strong>Arbeitslosenquote:</strong> Sinkt sie von 6 % auf 5 %, ist sie um einen Prozentpunkt gesunken, also um rund {de(1/6*100,1)} %.</div>
<p>Den Unterschied rechnet der <a href="/prozentrechner.html">Prozentrechner</a> im Modus „Veränderung“ für dich aus.</p>
""",
},
{
"slug": "grundwert-richtig-waehlen",
"title": "Den richtigen Grundwert wählen: Warum +25 % und −25 % nicht null ergeben",
"teaser": "Jede Prozentangabe braucht eine Basis. Wer sie verwechselt, rechnet falsch.",
"description": "Warum +25 % und −25 % nicht zum Ausgangswert führen: der Grundwert in der Prozentrechnung, mit Beispielen zu Preisen, Gehältern und Aktien.",
"body": f"""
<p>Ein Prozentsatz ist immer ein Anteil von etwas – vom Grundwert. Ändert sich der Grundwert, bedeutet derselbe Prozentsatz einen anderen Betrag. Darum gleichen sich Zuwachs und Abschlag mit gleichem Prozentsatz nicht aus.</p>
<h2>Das klassische Beispiel</h2>
<div class="example">Ein Preis von 100 € steigt um 25 % auf 125 €. Dann sinkt er um 25 % – aber von 125 €: 125 − 31,25 = <strong>{eur(93.75)}</strong>.</div>
<p>Um von 125 € zurück auf 100 € zu kommen, braucht es ein Minus von 25 ÷ 125 = <strong>20 %</strong>.</p>
<h2>Bei Geldanlagen besonders wichtig</h2>
<p>Verliert eine Aktie 50 %, muss sie danach um 100 % steigen, um wieder beim Ausgangswert zu sein. Nach einem Minus von 20 % braucht es ein Plus von 25 %.</p>
<table class="tbl text"><thead><tr><th>Verlust</th><th>nötiger Gewinn zum Ausgleich</th></tr></thead><tbody>
{''.join(f'<tr><td>−{l} %</td><td>+{de(l/(100-l)*100,1)} %</td></tr>' for l in (10, 20, 25, 33.33, 50, 75))}
</tbody></table>
<h2>So findest du den richtigen Grundwert</h2>
<p>Frag dich: Wovon ist die Rede? Bei „Der Preis ist um 20 % gestiegen“ ist es der alte Preis. Bei „Der Rabatt beträgt 20 %“ ist es der ursprüngliche Preis. Bei „20 % Mehrwertsteuer“ ist es der Nettobetrag.</p>
<p>Der <a href="/prozentrechner.html">Prozentrechner</a> zeigt im Rechenweg immer, welcher Wert als Grundwert dient.</p>
""",
},
{
"slug": "rabatte-kombinieren",
"title": "Rabatte kombinieren: Was 30 % + 20 % wirklich bringen",
"teaser": "Doppelte Rabatte addieren sich nicht. So rechnest du die echte Ersparnis.",
"description": "Mehrere Rabatte richtig berechnen: warum 30 % plus 20 % nur 44 % Ersparnis ergeben und wie man die echte Gesamtersparnis schnell ausrechnet.",
"body": f"""
<p>Bekommst du auf einen reduzierten Preis noch einmal Rabatt, wird der zweite Rabatt vom bereits reduzierten Preis abgezogen. 30 % und danach 20 % ergeben deshalb nicht 50 %, sondern {de((1-0.7*0.8)*100)} %.</p>
<h2>Die schnelle Rechnung</h2>
<p>Multipliziere die Anteile, die du jeweils zahlst: Bei 30 % Rabatt zahlst du 70 %, bei 20 % zahlst du 80 %. 0,7 × 0,8 = 0,56 – du zahlst 56 % und sparst 44 %.</p>
<table class="tbl text"><thead><tr><th>Rabatte</th><th>tatsächliche Ersparnis</th></tr></thead><tbody>
{''.join(f'<tr><td>{a} % + {b} %</td><td>{de((1-(1-a/100)*(1-b/100))*100,1)} %</td></tr>' for a,b in ((10,10),(20,10),(30,20),(50,20),(50,50)))}
</tbody></table>
<h2>Was Händler damit meinen</h2>
<p>„Zusätzlich 20 % auf bereits reduzierte Ware“ ist eine korrekte Formulierung. Irreführend wäre es, die Summe der Rabatte als Gesamtersparnis zu bewerben.</p>
<p>Der <a href="/rabatt-rechner.html">Rabatt-Rechner</a> verrechnet bis zu zwei Rabatte und Skonto und zeigt die echte Ersparnis.</p>
""",
},
{
"slug": "mehrwertsteuer-herausrechnen",
"title": "Mehrwertsteuer herausrechnen: durch 1,2 teilen statt 20 % abziehen",
"teaser": "Der häufigste Fehler bei Rechnungen – und die einfache Lösung.",
"description": "Mehrwertsteuer aus dem Bruttobetrag herausrechnen: warum man durch 1,2 bzw. 1,19 teilt, mit Beispielen für Österreich und Deutschland.",
"body": f"""
<p>Um den Nettobetrag aus einem Bruttobetrag zu erhalten, teilst du durch 1 plus Steuersatz: in Österreich bei 20 % durch 1,2, in Deutschland bei 19 % durch 1,19. 20 % vom Bruttobetrag abzuziehen ist falsch.</p>
<h2>Warum Abziehen nicht funktioniert</h2>
<p>Die Steuer wird auf den Nettobetrag aufgeschlagen. 100 € netto plus 20 % ergeben 120 € brutto. Ziehst du von 120 € wieder 20 % ab, rechnest du 20 % vom größeren Betrag und landest bei 96 € – nicht bei 100 €.</p>
<h2>Die Teiler im Überblick</h2>
<table class="tbl text"><thead><tr><th>Steuersatz</th><th>Netto = Brutto ÷</th><th>Steueranteil im Brutto</th></tr></thead><tbody>
{''.join(f'<tr><td>{de(r,1) if r%1 else r} %</td><td>{de(1+r/100,3 if r%1 else 2)}</td><td>{de(r/(100+r)*100,2)} %</td></tr>' for r in (20,13,10,4.9,19,7))}
</tbody></table>
<div class="example"><strong>Beispiel Österreich:</strong> Eine Rechnung über 360 € brutto mit 20 % enthält 360 ÷ 1,2 = {eur(300)} netto und {eur(60)} Steuer.</div>
<div class="example"><strong>Beispiel Deutschland:</strong> 238 € brutto mit 19 % ergeben 238 ÷ 1,19 = {eur(200)} netto und {eur(38)} Steuer.</div>
<p>Schneller geht es mit dem <a href="/mehrwertsteuer-rechner.html">Mehrwertsteuer-Rechner</a>.</p>
""",
},
{
"slug": "zinseszins-und-72er-regel",
"title": "Zinseszins und 72er-Regel: Wann sich Geld verdoppelt",
"teaser": "Eine Faustformel, die man im Kopf rechnen kann.",
"description": "Die 72er-Regel erklärt: In wie vielen Jahren sich Geld durch Zinseszins verdoppelt, wie genau die Faustformel ist und wie sie bei Inflation hilft.",
"body": f"""
<p>Teile 72 durch den Zinssatz, und du erhältst ungefähr die Zahl der Jahre, nach denen sich ein Betrag durch Zinseszins verdoppelt hat. Bei 4 % sind das 72 ÷ 4 = 18 Jahre.</p>
<h2>Wie genau ist die Regel?</h2>
<table class="tbl text"><thead><tr><th>Zinssatz</th><th>72er-Regel</th><th>exakt</th></tr></thead><tbody>
{''.join(f'<tr><td>{p} %</td><td>{de(72/p,1)} Jahre</td><td>{de(__import__("math").log(2)/__import__("math").log(1+p/100),1)} Jahre</td></tr>' for p in (1,2,3,4,6,8,10))}
</tbody></table>
<p>Zwischen 3 und 10 % liegt die Faustformel höchstens rund ein halbes Jahr daneben. Bei sehr niedrigen Zinssätzen überschätzt sie die Dauer etwas.</p>
<h2>Auch für Inflation</h2>
<p>Die Regel funktioniert auch rückwärts: Bei 3 % Inflation halbiert sich die Kaufkraft von Geld in rund 24 Jahren. Den genauen Wert zeigt der <a href="/inflationsrechner.html">Inflationsrechner</a>.</p>
<h2>Warum gerade 72?</h2>
<p>Exakt wäre die Verdopplungszeit ln(2) ÷ ln(1 + p). Für kleine Zinssätze ist das ungefähr 69,3 ÷ p. Die 72 ist etwas größer, gleicht die Ungenauigkeit bei üblichen Zinssätzen aus und ist durch viele Zahlen teilbar – 2, 3, 4, 6, 8, 9 und 12.</p>
""",
},
{
"slug": "sollzins-und-effektivzins",
"title": "Sollzins und Effektivzins: Welcher Wert zählt beim Kredit?",
"teaser": "Nur der effektive Jahreszins macht Kreditangebote vergleichbar.",
"description": "Sollzins und effektiver Jahreszins beim Kredit: was der Unterschied ist, welche Kosten enthalten sind und wie man Angebote richtig vergleicht.",
"body": """
<p>Der Sollzins ist der reine Preis für das geliehene Geld. Der effektive Jahreszins enthält zusätzlich die Kosten, die du für den Kredit zahlen musst, etwa Bearbeitungsgebühren. Zum Vergleichen von Angeboten ist deshalb der Effektivzins der richtige Wert.</p>
<h2>Was im Effektivzins steckt</h2>
<ul><li>Sollzins</li><li>Bearbeitungs- und Abschlussgebühren</li><li>Kosten, die verpflichtend mit dem Kredit verbunden sind, etwa für eine vorgeschriebene Kontoführung</li></ul>
<p>Freiwillige Zusatzprodukte wie eine Restschuldversicherung sind oft nicht enthalten, verteuern den Kredit aber trotzdem. Prüfe, ob sie wirklich nötig sind.</p>
<h2>Was das Gesetz verlangt</h2>
<p>In Österreich (Verbraucherkreditgesetz) und Deutschland (Preisangabenverordnung) muss bei Verbraucherkrediten der effektive Jahreszins angegeben werden. Die Berechnungsmethode ist EU-weit einheitlich.</p>
<h2>Gebunden oder variabel?</h2>
<p>Ein fixer Sollzins bleibt über die vereinbarte Zeit gleich. Ein variabler Zins ist an einen Referenzzinssatz wie den Euribor gekoppelt und kann steigen oder fallen – die Rate ändert sich dann mit.</p>
<p>Mit dem <a href="/kreditrechner.html">Kreditrechner</a> siehst du, wie sich ein Zinsunterschied auf die Monatsrate und die Gesamtkosten auswirkt.</p>
<p class="small muted">Ohne Gewähr; keine Finanzberatung.</p>
""",
},
]
