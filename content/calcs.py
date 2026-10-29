"""Rechner: Formular, Erklärung und durchgerechnete Beispiele (Beispiele werden in Python berechnet)."""
import math


def de(x, d=2):
    s = f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if "," in s:
        s = s.rstrip("0").rstrip(",")
    return s


def eur(x):
    s = f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s} €"


def form(calc, fields, extra=""):
    return f'<form data-calc="{calc}" id="f-{calc}" novalidate><div class="fields">{fields}</div>{extra}<div data-out aria-live="polite"></div></form>'


def inp(name, label, value, mode="decimal", attrs=""):
    return f'<label class="f"><span data-l="{name}">{label}</span><input name="{name}" inputmode="{mode}" value="{value}" autocomplete="off" {attrs}></label>'


def select(name, label, options, value=None):
    o = "".join(f'<option value="{v}"{" selected" if v == value else ""}>{t}</option>' for v, t in options)
    return f'<label class="f">{label}<select name="{name}">{o}</select></label>'


PERCENT_FORM = form("percent",
    select("mode", "Was willst du wissen?", [("anteil", "Wie viel sind x % von …?"), ("satz", "Wie viel Prozent sind …?"),
           ("grund", "Von welchem Wert sind es x %?"), ("veraenderung", "Um wie viel % hat sich … verändert?"),
           ("rabatt", "Preis nach Rabatt"), ("ursprung", "Preis vor dem Rabatt")], "anteil")
    + inp("a", "Grundwert", "80") + inp("b", "Prozentsatz (%)", "15"))

# ---------- Beispielrechnungen
_ch = (96 - 80) / 80 * 100
_mw_n = 119 / 1.19
_r = 200 * 0.8 * 0.9
_k_i = 0.045 / 12
_k_a = 20000 * _k_i / (1 - (1 + _k_i) ** -60)


def _zins(k0, r, p, n):
    i = p / 100 / 12; k = k0
    for _ in range(n * 12):
        k = k * (1 + i) + r
    return k


_z = _zins(0, 100, 3, 20)

CALCS = [
{
"slug": "prozentrechner", "short": "Prozentrechner", "sym": "%",
"teaser": "Anteil, Prozentsatz, Grundwert, Veränderung und Rabatt.",
"title": "Prozentrechner mit Rechenweg: Prozent, Grundwert, Veränderung",
"h1": "Prozentrechner",
"lead": "Sechs Fragen, ein Rechner: Prozentwert, Prozentsatz, Grundwert, prozentuale Veränderung und Rabatte – jeweils mit vollständigem Rechenweg.",
"description": "Prozentrechner mit Rechenweg: Prozentwert, Prozentsatz und Grundwert berechnen, prozentuale Veränderung und Rabatte – kostenlos und verständlich erklärt.",
"formula": "Prozentwert = Grundwert × Prozentsatz ÷ 100",
"form": PERCENT_FORM,
"body": f"""
<h2>Die drei Größen der Prozentrechnung</h2>
<p>Jede Prozentaufgabe besteht aus drei Größen. Zwei davon kennst du, die dritte rechnest du aus.</p>
<ul><li><strong>Grundwert (G):</strong> das Ganze, also 100 %. Zum Beispiel der Preis vor dem Rabatt.</li>
<li><strong>Prozentsatz (p):</strong> der Anteil in Prozent, zum Beispiel 15 %.</li>
<li><strong>Prozentwert (W):</strong> der Anteil als Zahl, zum Beispiel 12 Euro.</li></ul>
<p>Daraus folgen drei Formeln: W = G × p ÷ 100, p = W ÷ G × 100 und G = W ÷ p × 100.</p>
<h2>Beispiele</h2>
<div class="example"><strong>15 % von 80:</strong> 80 × 15 ÷ 100 = {de(80*15/100)}.</div>
<div class="example"><strong>Veränderung von 80 auf 96:</strong> (96 − 80) ÷ 80 × 100 = {de(_ch)} %. Der Wert ist um {de(_ch)} % gestiegen.</div>
<div class="example"><strong>Preis vor dem Rabatt:</strong> Ein Mantel kostet nach 30 % Rabatt 140 €. Ursprünglich kostete er 140 ÷ 0,7 = {eur(140/0.7)} – nicht 140 € + 30 % = {eur(140*1.3)}.</div>
<h2>Die häufigsten Fehler</h2>
<div class="warn"><strong>Falscher Grundwert:</strong> Steigt ein Preis um 25 % und fällt danach um 25 %, ist er nicht wieder beim Ausgangswert. 100 € werden zu 125 € und dann zu {eur(125*0.75)}. Der zweite Prozentsatz bezieht sich auf den neuen, höheren Wert. Mehr dazu im Beitrag <a href="/grundwert-richtig-waehlen.html">Den richtigen Grundwert wählen</a>.</div>
<div class="warn"><strong>Prozent und Prozentpunkte verwechseln:</strong> Steigt ein Zinssatz von 2 % auf 3 %, ist das ein Plus von einem Prozentpunkt, aber von 50 Prozent. <a href="/prozent-oder-prozentpunkte.html">Prozent oder Prozentpunkte?</a></div>
""",
"related": ["prozent-oder-prozentpunkte", "grundwert-richtig-waehlen"],
},
{
"slug": "mehrwertsteuer-rechner", "short": "Mehrwertsteuer-Rechner", "sym": "USt",
"teaser": "Netto und brutto für Österreich (20/13/10 %) und Deutschland (19/7 %).",
"title": "Mehrwertsteuer-Rechner Österreich & Deutschland: netto ↔ brutto",
"h1": "Mehrwertsteuer-Rechner",
"lead": "Brutto aus netto oder netto aus brutto – mit den Steuersätzen für Österreich und Deutschland und dem richtigen Rechenweg zum Herausrechnen.",
"description": "Mehrwertsteuer berechnen: netto in brutto und brutto in netto umrechnen, mit 20, 13 und 10 % für Österreich sowie 19 und 7 % für Deutschland.",
"formula": "Netto = Brutto ÷ (1 + Steuersatz)",
"form": form("mwst",
    select("dir", "Richtung", [("b2n", "Brutto → netto (Steuer herausrechnen)"), ("n2b", "Netto → brutto (Steuer aufschlagen)")], "b2n")
    + inp("amount", "Betrag (€)", "120")
    + select("rate", "Steuersatz", [("20", "Österreich 20 % (Normalsatz)"), ("13", "Österreich 13 %"), ("10", "Österreich 10 %"),
             ("19", "Deutschland 19 % (Regelsatz)"), ("7", "Deutschland 7 %"), ("custom", "eigener Satz")], "20")
    + '<label class="f" data-show-when="rate=custom">Eigener Satz (%)<input name="custom" inputmode="decimal" value="8.1"></label>'),
"body": f"""
<h2>Steuersätze in Österreich und Deutschland</h2>
<table class="tbl text"><thead><tr><th>Land</th><th>Normalsatz</th><th>Ermäßigt</th></tr></thead><tbody>
<tr><td>Österreich</td><td>20 %</td><td>10 % (z. B. viele Lebensmittel) und 13 %</td></tr>
<tr><td>Deutschland</td><td>19 %</td><td>7 % (z. B. viele Lebensmittel)</td></tr></tbody></table>
<p class="small muted">Welcher Satz für eine bestimmte Ware oder Leistung gilt, regeln das österreichische Umsatzsteuergesetz und das deutsche Umsatzsteuergesetz. Im Zweifel gilt die Rechnung oder die Auskunft des Finanzamts.</p>
<h2>Mehrwertsteuer herausrechnen – so geht es richtig</h2>
<p>Der Bruttobetrag ist 100 % plus Steuer, also bei 20 % genau 120 % des Nettobetrags. Deshalb teilst du durch 1,2 – und ziehst nicht einfach 20 % ab.</p>
<div class="example"><strong>Österreich:</strong> 120 € brutto ÷ 1,2 = {eur(100)} netto. Enthaltene Steuer: {eur(20)}.</div>
<div class="example"><strong>Deutschland:</strong> 119 € brutto ÷ 1,19 = {eur(_mw_n)} netto. Enthaltene Steuer: {eur(119-_mw_n)}.</div>
<div class="warn"><strong>Typischer Fehler:</strong> 120 € minus 20 % ergibt {eur(96)} – das ist um {eur(4)} zu wenig, weil die 20 % auf den Nettobetrag gerechnet werden, nicht auf den Bruttobetrag.</div>
<h2>Faustregel für den Steueranteil</h2>
<p>Bei 20 % steckt im Bruttobetrag immer genau ein Sechstel Steuer, bei 19 % sind es 19/119, also rund 15,97 %, bei 10 % ein Elftel und bei 7 % 7/107, rund 6,54 %.</p>
""",
"related": ["mehrwertsteuer-herausrechnen"],
},
{
"slug": "rabatt-rechner", "short": "Rabatt-Rechner", "sym": "−%",
"teaser": "Mehrere Rabatte und Skonto hintereinander richtig verrechnen.",
"title": "Rabatt-Rechner: mehrere Rabatte und Skonto richtig rechnen",
"h1": "Rabatt-Rechner",
"lead": "Was kostet es wirklich nach Aktionsrabatt, Zusatzrabatt und Skonto? Der Rechner zeigt Endpreis, Ersparnis und den tatsächlichen Gesamtrabatt.",
"description": "Rabatt berechnen: Endpreis und echte Gesamtersparnis bei mehreren Rabatten hintereinander und Skonto – mit Rechenweg.",
"formula": "Endpreis = Preis × (1 − r₁) × (1 − r₂)",
"form": form("rabatt", inp("price", "Preis (€)", "200") + inp("r1", "1. Rabatt (%)", "20") + inp("r2", "2. Rabatt (%)", "10") + inp("skonto", "Skonto (%)", "")),
"body": f"""
<h2>Warum 20 % + 10 % nicht 30 % sind</h2>
<p>Jeder weitere Rabatt wird vom bereits reduzierten Preis abgezogen. Bei 200 € mit 20 % und danach 10 % zahlst du 200 × 0,8 × 0,9 = {eur(_r)}. Das sind {de((1-_r/200)*100)} % Ersparnis, nicht 30 %.</p>
<div class="example"><strong>Die Reihenfolge ist egal:</strong> 200 × 0,9 × 0,8 ergibt ebenfalls {eur(_r)}. Multiplikation ist vertauschbar.</div>
<h2>Skonto</h2>
<p>Skonto ist ein Abzug für schnelle Zahlung, meist 2 bis 3 % innerhalb von 10 bis 14 Tagen. Es wirkt wie ein weiterer Rabatt auf den bereits rabattierten Betrag. Für Unternehmen lohnt sich Skonto fast immer: 2 % für 20 Tage früheres Zahlen entsprechen auf ein Jahr gerechnet einem Zinssatz von rund 37 %.</p>
""",
"related": ["rabatte-kombinieren", "grundwert-richtig-waehlen"],
},
{
"slug": "zinseszins-rechner", "short": "Zinseszins- & Sparrechner", "sym": "∑",
"teaser": "Wie aus einer monatlichen Sparrate über die Jahre Kapital wird.",
"title": "Zinseszinsrechner & Sparplan-Rechner mit Jahrestabelle",
"h1": "Zinseszins- und Sparrechner",
"lead": "Startkapital, monatliche Sparrate, Zinssatz und Laufzeit eingeben – der Rechner zeigt das Endkapital und Jahr für Jahr, wie viel davon Zinsen sind.",
"description": "Zinseszins berechnen: Sparplan mit Startkapital und monatlicher Rate, Endkapital und Zinsanteil Jahr für Jahr – mit Rechenweg.",
"formula": "Kₙ = K₀ × (1 + p)ⁿ",
"form": form("zins", inp("start", "Startkapital (€)", "0") + inp("monthly", "Sparrate pro Monat (€)", "100") + inp("rate", "Zinssatz p. a. (%)", "3") + inp("years", "Laufzeit (Jahre)", "20", "numeric")),
"body": f"""
<h2>Was der Zinseszins bewirkt</h2>
<p>Zinsen, die auf dem Konto bleiben, bringen im nächsten Jahr selbst Zinsen. Dadurch wächst das Kapital nicht gleichmäßig, sondern immer schneller.</p>
<div class="example"><strong>100 € im Monat, 3 % Zinsen, 20 Jahre:</strong> Eingezahlt sind {eur(24000)}, am Ende stehen {eur(_z)} auf dem Konto. Rund {eur(_z-24000)} davon sind Zinsen.</div>
<h2>Die 72er-Regel</h2>
<p>Teilst du 72 durch den Zinssatz, erhältst du ungefähr die Jahre, in denen sich ein Betrag verdoppelt. Bei 3 % sind das rund 24 Jahre, bei 6 % rund 12 Jahre. <a href="/zinseszins-und-72er-regel.html">Mehr zur 72er-Regel</a></p>
<h2>Was der Rechner nicht berücksichtigt</h2>
<ul><li><strong>Steuern:</strong> In Österreich fallen auf Zinsen aus Bankguthaben 25 % Kapitalertragsteuer an, auf andere Kapitalerträge meist 27,5 %. In Deutschland gilt die Abgeltungsteuer von 25 % plus Solidaritätszuschlag, mit einem Sparerpauschbetrag von 1.000 € pro Person und Jahr.</li>
<li><strong>Inflation:</strong> Was die Summe in 20 Jahren wert ist, zeigt der <a href="/inflationsrechner.html">Inflationsrechner</a>.</li>
<li><strong>Schwankende Erträge:</strong> Bei Aktien oder Fonds gibt es keinen festen Zinssatz. Der Rechner zeigt dann nur ein Szenario.</li></ul>
<p class="small muted">Gerechnet wird mit monatlicher Verzinsung (Jahreszinssatz ÷ 12) und Einzahlung am Monatsende.</p>
""",
"related": ["zinseszins-und-72er-regel"],
},
{
"slug": "kreditrechner", "short": "Kreditrechner", "sym": "€",
"teaser": "Monatsrate, Zinskosten und Tilgungsplan für einen Ratenkredit.",
"title": "Kreditrechner: Monatsrate, Zinskosten & Tilgungsplan",
"h1": "Kreditrechner",
"lead": "Wie hoch ist die Monatsrate, und was kostet der Kredit insgesamt? Mit Tilgungsplan Jahr für Jahr.",
"description": "Kredit berechnen: Monatsrate, Gesamtkosten und Tilgungsplan für Ratenkredite und Annuitätendarlehen – mit Rechenweg.",
"formula": "Rate = K × i ÷ (1 − (1 + i)⁻ⁿ)",
"form": form("kredit", inp("amount", "Kreditbetrag (€)", "20000") + inp("rate", "Sollzins p. a. (%)", "4.5") + inp("years", "Laufzeit (Jahre)", "5")),
"body": f"""
<h2>So wird die Rate berechnet</h2>
<p>Bei einem Ratenkredit (Annuitätenkredit) zahlst du jeden Monat denselben Betrag. Am Anfang besteht die Rate vor allem aus Zinsen, gegen Ende fast nur aus Tilgung, weil die Restschuld immer kleiner wird.</p>
<div class="example"><strong>20.000 € zu 4,5 % auf 5 Jahre:</strong> Die Monatsrate beträgt {eur(_k_a)}. Insgesamt zahlst du {eur(_k_a*60)} zurück, die Zinskosten liegen also bei {eur(_k_a*60-20000)}.</div>
<h2>Sollzins oder Effektivzins?</h2>
<p>Der Sollzins ist der reine Zinssatz. Der effektive Jahreszins enthält zusätzlich Kosten wie Bearbeitungsgebühren und ist deshalb der richtige Wert, um Angebote zu vergleichen. Kreditgeber müssen ihn in Österreich und Deutschland angeben. <a href="/sollzins-und-effektivzins.html">Der Unterschied im Detail</a></p>
<div class="warn"><strong>Vorsicht bei langen Laufzeiten:</strong> Eine niedrigere Rate durch längere Laufzeit bedeutet fast immer deutlich höhere Gesamtkosten.</div>
<p class="small muted">Der Rechner ersetzt kein Kreditangebot und keine Beratung. Gebühren, Versicherungen und Zinsänderungen sind nicht enthalten.</p>
""",
"related": ["sollzins-und-effektivzins"],
},
{
"slug": "inflationsrechner", "short": "Inflationsrechner", "sym": "↘",
"teaser": "Was Geld in einigen Jahren noch wert ist.",
"title": "Inflationsrechner: Kaufkraft und künftige Preise berechnen",
"h1": "Inflationsrechner",
"lead": "Wie viel ist ein Betrag in zehn Jahren noch wert, wenn die Preise jedes Jahr steigen? Und was kostet heute 100 € Gekauftes dann?",
"description": "Inflation berechnen: Kaufkraftverlust und künftige Preise bei einer angenommenen Inflationsrate – mit Rechenweg.",
"formula": "Kaufkraft = Betrag ÷ (1 + i)ⁿ",
"form": form("inflation", inp("amount", "Betrag heute (€)", "1000") + inp("rate", "Inflationsrate p. a. (%)", "2") + inp("years", "Jahre", "10", "numeric")),
"body": f"""
<h2>Inflation wirkt wie ein Zinseszins rückwärts</h2>
<p>Steigen die Preise jedes Jahr um 2 %, kostet ein Warenkorb, der heute 1.000 € kostet, in zehn Jahren {eur(1000*1.02**10)}. Umgekehrt kaufst du mit 1.000 € dann nur noch so viel wie heute mit {eur(1000/1.02**10)}.</p>
<h2>Welche Inflationsrate eingeben?</h2>
<p>Die offiziellen Werte veröffentlichen <a href="https://www.statistik.at" rel="noopener">Statistik Austria</a> (Verbraucherpreisindex) und das <a href="https://www.destatis.de" rel="noopener">Statistische Bundesamt</a> in Deutschland. Die Europäische Zentralbank strebt mittelfristig eine Inflationsrate von 2 % an – ein guter Ausgangswert für langfristige Überlegungen.</p>
<div class="warn"><strong>Zinsen und Inflation:</strong> Bringt ein Sparbuch 1 % Zinsen bei 2 % Inflation, verliert das Geld real an Wert, obwohl der Kontostand steigt.</div>
""",
"related": ["zinseszins-und-72er-regel"],
},
{
"slug": "dreisatz-rechner", "short": "Dreisatz-Rechner", "sym": "⅓",
"teaser": "Proportional und umgekehrt proportional – mit allen drei Sätzen.",
"title": "Dreisatz-Rechner: proportional und umgekehrt mit Rechenweg",
"h1": "Dreisatz-Rechner",
"lead": "Drei Werte bekannt, einer gesucht: Der Rechner löst proportionale und umgekehrt proportionale Dreisätze und schreibt alle drei Sätze mit.",
"description": "Dreisatz online berechnen: proportionaler und umgekehrter (antiproportionaler) Dreisatz mit vollständigem Rechenweg und Beispielen.",
"formula": "a → b, also c → b ÷ a × c",
"form": form("dreisatz", select("kind", "Art", [("pro", "proportional (je mehr, desto mehr)"), ("anti", "umgekehrt (je mehr, desto weniger)")], "pro")
    + inp("a", "Wenn …", "4") + inp("b", "… dann …", "6") + inp("c", "Wie viel bei …?", "10")),
"body": f"""
<h2>Die drei Sätze</h2>
<ol><li>Aussage: 4 Brötchen kosten 6 €.</li><li>Auf eins zurückrechnen: 1 Brötchen kostet 6 ÷ 4 = 1,50 €.</li><li>Auf das Gesuchte hochrechnen: 10 Brötchen kosten 1,50 × 10 = 15 €.</li></ol>
<h2>Proportional oder umgekehrt?</h2>
<p><strong>Proportional</strong> heißt: Verdoppelt sich die eine Größe, verdoppelt sich auch die andere – mehr Brötchen, höherer Preis.</p>
<p><strong>Umgekehrt proportional</strong> heißt: Verdoppelt sich die eine Größe, halbiert sich die andere. Beispiel: 4 Personen streichen eine Wohnung in 6 Stunden. 8 Personen brauchen 4 × 6 ÷ 8 = 3 Stunden.</p>
<div class="warn"><strong>Nicht alles ist proportional:</strong> Ein Kuchen backt nicht schneller, wenn man zwei in den Ofen schiebt. Prüfe immer, ob der Zusammenhang wirklich gleichmäßig ist.</div>
""",
"related": ["prozent-oder-prozentpunkte"],
},
{
"slug": "bruchrechner", "short": "Bruchrechner", "sym": "½",
"teaser": "Brüche addieren, subtrahieren, multiplizieren, dividieren und kürzen.",
"title": "Bruchrechner mit Rechenweg: plus, minus, mal, geteilt & kürzen",
"h1": "Bruchrechner",
"lead": "Zwei Brüche eingeben, Rechenart wählen – der Rechner findet den gemeinsamen Nenner, kürzt und zeigt jeden Schritt.",
"description": "Brüche online berechnen: addieren, subtrahieren, multiplizieren und dividieren mit gekürztem Ergebnis, gemischter Zahl und Rechenweg.",
"formula": "a/b + c/d = (a·d + c·b) / (b·d)",
"form": form("bruch", inp("a", "Zähler 1", "3", "numeric") + inp("b", "Nenner 1", "4", "numeric")
    + select("op", "Rechenart", [("+", "+ plus"), ("-", "− minus"), ("*", "× mal"), ("/", "÷ geteilt")], "+")
    + inp("c", "Zähler 2", "5", "numeric") + inp("d", "Nenner 2", "6", "numeric")),
"body": """
<h2>Die vier Grundregeln</h2>
<ul><li><strong>Addieren und Subtrahieren:</strong> Erst auf einen gemeinsamen Nenner bringen, dann die Zähler verrechnen. 3/4 + 5/6 = 9/12 + 10/12 = 19/12 = 1 7/12.</li>
<li><strong>Multiplizieren:</strong> Zähler mal Zähler, Nenner mal Nenner. 2/3 × 3/4 = 6/12 = 1/2.</li>
<li><strong>Dividieren:</strong> Mit dem Kehrwert des zweiten Bruchs malnehmen. 2/3 ÷ 4/5 = 2/3 × 5/4 = 10/12 = 5/6.</li>
<li><strong>Kürzen:</strong> Zähler und Nenner durch ihren größten gemeinsamen Teiler teilen.</li></ul>
<h2>Der kleinste gemeinsame Nenner</h2>
<p>Man kann immer die beiden Nenner multiplizieren. Kleinere Zahlen erhältst du mit dem kleinsten gemeinsamen Vielfachen: Für 4 und 6 ist das 12 statt 24. Der Rechner verwendet automatisch das kleinste gemeinsame Vielfache.</p>
""",
"related": [],
},
{
"slug": "einheitenrechner", "short": "Einheitenrechner", "sym": "⇄",
"teaser": "Länge, Fläche, Volumen, Gewicht, Tempo und Temperatur.",
"title": "Einheitenrechner: Länge, Fläche, Volumen, Gewicht & Temperatur",
"h1": "Einheitenrechner",
"lead": "Von Zoll in Zentimeter, von Joch in Hektar, von Fahrenheit in Celsius – mit dem Umrechnungsfaktor und dem Rechenweg.",
"description": "Einheiten umrechnen: Länge, Fläche, Volumen, Gewicht, Geschwindigkeit und Temperatur – mit Faktor und Rechenweg, inklusive Dekagramm und Joch.",
"formula": "Wert × Faktor (von) ÷ Faktor (nach)",
"form": form("einheit", select("cat", "Größe", [("laenge", "Länge"), ("flaeche", "Fläche"), ("volumen", "Volumen"), ("masse", "Gewicht"), ("tempo", "Geschwindigkeit"), ("temp", "Temperatur")], "laenge")
    + inp("value", "Wert", "12") + '<label class="f">von<select name="from"></select></label><label class="f">nach<select name="to"></select></label>'),
"body": """
<h2>Österreichische Einheiten</h2>
<ul><li><strong>Dekagramm (dag):</strong> 1 dag = 10 g. „10 Deka Wurst“ sind also 100 g.</li>
<li><strong>Joch:</strong> alte Flächeneinheit, in Österreich vor allem in der Landwirtschaft noch geläufig. 1 Joch = 5.754,642 m², rund 0,58 Hektar.</li></ul>
<h2>Wichtige Umrechnungen</h2>
<table class="tbl text"><tbody>
<tr><td>1 Zoll</td><td>2,54 cm</td></tr><tr><td>1 Meile</td><td>1,609 km</td></tr>
<tr><td>1 Hektar</td><td>10.000 m² = 100 Ar</td></tr><tr><td>1 Pfund (international)</td><td>453,59 g</td></tr>
<tr><td>1 Cup (US)</td><td>236,6 ml</td></tr><tr><td>100 km/h</td><td>27,78 m/s</td></tr>
<tr><td>0 °C</td><td>32 °F = 273,15 K</td></tr></tbody></table>
<p>Temperaturen lassen sich nicht mit einem einfachen Faktor umrechnen, weil die Skalen unterschiedliche Nullpunkte haben. Der Rechner rechnet deshalb über Grad Celsius.</p>
""",
"related": [],
},
{
"slug": "durchschnitt-rechner", "short": "Durchschnitt & Notenschnitt", "sym": "x̄",
"teaser": "Mittelwert, Median und gewichteter Notenschnitt.",
"title": "Durchschnitt berechnen: Mittelwert, Median & gewichteter Notenschnitt",
"h1": "Durchschnitt und Notenschnitt",
"lead": "Zahlen einfügen und Mittelwert, Median, Minimum und Maximum erhalten. Mit Gewichten wird daraus ein gewichteter Notenschnitt.",
"description": "Durchschnitt berechnen: arithmetisches Mittel, Median und gewichteter Durchschnitt, zum Beispiel für den Notenschnitt – mit Rechenweg.",
"formula": "x̄ = Summe ÷ Anzahl",
"form": form("schnitt", '<label class="f" style="grid-column:1/-1">Werte (mit Leerzeichen oder Strichpunkt getrennt)<textarea name="values">2 1 3 2 4</textarea></label>'
    + '<label class="f" style="grid-column:1/-1">Gewichte (optional, gleiche Anzahl)<input name="weights" value="" placeholder="z. B. 2 2 1 1 1"></label>'),
"body": f"""
<h2>Mittelwert oder Median?</h2>
<p>Der <strong>Mittelwert</strong> ist die Summe geteilt durch die Anzahl. Der <strong>Median</strong> ist der Wert in der Mitte der sortierten Liste. Ausreißer verzerren den Mittelwert, den Median kaum: Bei den Gehältern 2.000, 2.200, 2.400 und 20.000 € liegt der Mittelwert bei {eur((2000+2200+2400+20000)/4)}, der Median bei {eur(2300)}.</p>
<h2>Gewichteter Notenschnitt</h2>
<p>Zählen Schularbeiten doppelt, gibst du ihnen das Gewicht 2. Noten 2 und 3 mit Gewicht 2, Note 1 mit Gewicht 1: (2×2 + 3×2 + 1×1) ÷ (2 + 2 + 1) = {de((4+6+1)/5)}.</p>
<p class="small muted">In Österreich reicht die Notenskala von 1 bis 5, in Deutschland von 1 bis 6.</p>
""",
"related": [],
},
{
"slug": "stundenlohn-rechner", "short": "Stundenlohn-Rechner", "sym": "h",
"teaser": "Monatsgehalt in Stundenlohn – mit 14 Gehältern für Österreich.",
"title": "Stundenlohn-Rechner: Monatsgehalt ↔ Stundenlohn (12 oder 14 Gehälter)",
"h1": "Stundenlohn-Rechner",
"lead": "Was verdiene ich pro Stunde? Der Rechner berücksichtigt die Wochenstunden und ob du 12 oder 14 Gehälter im Jahr bekommst.",
"description": "Stundenlohn berechnen aus dem Monatsgehalt und umgekehrt – mit 14 Gehältern für Österreich oder 12 für Deutschland, brutto.",
"formula": "Stundenlohn = Monatsgehalt × Gehälter ÷ (Wochenstunden × 52)",
"form": form("lohn", select("dir", "Richtung", [("m2h", "Monatsgehalt → Stundenlohn"), ("h2m", "Stundenlohn → Monatsgehalt")], "m2h")
    + inp("amount", "Betrag brutto (€)", "3000") + inp("hours", "Wochenstunden", "38.5")
    + select("salaries", "Gehälter pro Jahr", [("14", "14 (Österreich, mit Urlaubs- und Weihnachtsgeld)"), ("12", "12")], "14")),
"body": f"""
<h2>Warum 14 Gehälter den Stundenlohn erhöhen</h2>
<p>In Österreich sehen die meisten Kollektivverträge zusätzlich zu zwölf Monatsgehältern Urlaubs- und Weihnachtsgeld vor, also 14 Zahlungen. Bei 3.000 € brutto und 38,5 Wochenstunden ergibt das {eur(3000*14/(38.5*52))} pro Stunde. Mit 12 Gehältern wären es {eur(3000*12/(38.5*52))}.</p>
<h2>Wie viele Stunden hat ein Monat?</h2>
<p>Ein Jahr hat 52 Wochen, ein Monat im Schnitt also 52 ÷ 12 ≈ 4,33 Wochen. Bei 40 Wochenstunden sind das rund {de(40*52/12,1)} Stunden pro Monat, bei 38,5 Stunden rund {de(38.5*52/12,1)}.</p>
<p class="small muted">Alle Werte brutto. Urlaub und Feiertage sind bezahlt und deshalb nicht abgezogen. Für das Nettogehalt sind Sozialversicherung und Lohnsteuer zu berücksichtigen.</p>
""",
"related": [],
},
]

from content.calcs_more import MORE as _MORE  # noqa: E402
CALCS += _MORE
