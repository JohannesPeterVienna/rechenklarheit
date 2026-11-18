"""Sätze und Grenzwerte aus Gesetz und amtlichen Quellen – eine Zeile je Wert, mit Fundstelle, Fassung und Abrufdatum.

Jeder Wert wurde am Abrufdatum im Wortlaut der verlinkten Quelle nachgelesen (Österreich: konsolidierte Fassung im
Rechtsinformationssystem des Bundes; Deutschland: gesetze-im-internet.de; Basiszinssätze: OeNB und Deutsche Bundesbank).
Die Rechner „Pendlerrechner“ und „Verzugszinsen“ verwenden dieselben Zahlen; build.py prüft, dass calc.js nicht abweicht.
"""
import html

ABRUF = "18.11.2026"
RIS = "https://ris.bka.gv.at/eli/"
GII = "https://www.gesetze-im-internet.de/"
OENB = "https://www.oenb.at/isaweb/report.do?report=2.1"
BBK = "https://www.bundesbank.de/de/bundesbank/organisation/agb-und-regelungen/basiszinssatz-607820"

# ---------- Werte, die auch die Rechner verwenden (einzige Stelle, an der sie stehen)
PENDLER_AT = {  # § 16 Abs. 1 Z 6 lit. c und d EStG 1988, Euro jährlich; Schlüssel = „mehr als … km“ (klein: ab 20 km, groß: ab 2 km)
    "klein": [(20, 696), (40, 1356), (60, 2016)],
    "gross": [(2, 372), (20, 1476), (40, 2568), (60, 3672)],
}
PENDLEREURO_AT = 6          # § 33 Abs. 5 Z 4 EStG 1988: Euro jährlich je km einfacher Strecke (Fassung bis 31.12.2026)
ENTF_DE = 0.38              # § 9 Abs. 1 Satz 3 Nr. 4 EStG: Euro je vollem Entfernungskilometer und Arbeitstag
ENTF_DE_MAX = 4500          # Höchstbetrag ohne eigenen oder überlassenen Kraftwagen
AN_PAUSCH_DE = 1230         # § 9a Satz 1 Nr. 1 Buchst. a EStG
# Basiszinssatz Deutschland (§ 247 BGB), jeweils ab 1.1. und 1.7. – Tabelle der Deutschen Bundesbank
BASIS_DE = [("2020-01-01", -0.88), ("2020-07-01", -0.88), ("2021-01-01", -0.88), ("2021-07-01", -0.88), ("2022-01-01", -0.88),
            ("2022-07-01", -0.88), ("2023-01-01", 1.62), ("2023-07-01", 3.12), ("2024-01-01", 3.62), ("2024-07-01", 3.37),
            ("2025-01-01", 2.27), ("2025-07-01", 1.27), ("2026-01-01", 1.27), ("2026-07-01", 1.52)]
# Basiszinssatz Österreich: Änderungstage laut OeNB. Für § 456 UGB zählt der Wert am ersten Kalendertag des Halbjahres.
BASIS_AT_AENDERUNGEN = [("2016-03-16", -0.62), ("2022-07-27", -0.12), ("2022-09-14", 0.63), ("2022-11-02", 1.38), ("2022-12-21", 1.88),
                        ("2023-02-08", 2.38), ("2023-03-22", 2.88), ("2023-06-21", 3.38), ("2023-09-20", 3.88), ("2024-09-18", 3.03),
                        ("2024-12-18", 2.53), ("2025-03-12", 2.03), ("2025-06-11", 1.53), ("2026-09-16", 2.03)]


def _at_halbjahre():
    out = []
    for y in range(2020, 2027):
        for md in ("01-01", "07-01"):
            d = f"{y}-{md}"
            out.append((d, [v for s, v in BASIS_AT_AENDERUNGEN if s <= d][-1]))
    return out


BASIS_AT = _at_halbjahre()
VERZUG = {"de_v": 5, "de_u": 9, "at_u": 9.2, "at_a": 9.2, "at_v": 4}     # Prozentpunkte über Basiszinssatz bzw. fester Satz (at_v)
BASIS_AT_AB2020 = [x for x in BASIS_AT_AENDERUNGEN if x[0] >= "2020-01-01"]
BASIS_AT_TAG = [("2020-01-01", [v for d, v in BASIS_AT_AENDERUNGEN if d <= "2020-01-01"][-1])] + BASIS_AT_AB2020   # Tageswerte für § 49a ASGG
VERZUG_BIS = "2026-12-31"                                    # letzter Tag, für den der Basiszinssatz feststeht


def _de(x, d=2):
    s = f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


def _stufen(rows, erste):
    out = []
    for i, (ab, eur) in enumerate(rows):
        bis = rows[i + 1][0] if i + 1 < len(rows) else None
        von = f"ab {ab} km" if i == 0 and erste else f"über {ab} km"
        out.append(f"{von}{f' bis {bis} km' if bis else ''}: {_de(eur, 0)} €")
    return " · ".join(out)


# ---------- Tabelle: (Land, Thema, Bezeichnung, Wert, Fundstelle, Link, Fassung/Stand, Hinweis, Rechner-Link)
R = []


def row(land, thema, name, wert, fund, url, stand, hinweis="", tool=""):
    R.append(dict(land=land, thema=thema, name=name, wert=wert, fund=fund, url=url, stand=stand, hinweis=hinweis, tool=tool))


U10 = RIS + "bgbl/1994/663/P10/NOR40278068"
row("AT", "Umsatzsteuer", "Normalsteuersatz", "20 %", "§ 10 Abs. 1 UStG 1994", U10, "Fassung in Kraft seit 1.7.2026", "", "/mehrwertsteuer-rechner.html?dir=b2n&amount=120&rate=20")
row("AT", "Umsatzsteuer", "Ermäßigter Satz (Anlage 1, u. a. Wohnungsmiete, Beherbergung)", "10 %", "§ 10 Abs. 2 UStG 1994", U10, "Fassung in Kraft seit 1.7.2026", "Gilt nur, soweit nicht der Satz von 4,9 % anzuwenden ist.", "/mehrwertsteuer-rechner.html?dir=b2n&amount=110&rate=10")
row("AT", "Umsatzsteuer", "Ermäßigter Satz (Anlage 2 und weitere Umsätze)", "13 %", "§ 10 Abs. 3 UStG 1994", U10, "Fassung in Kraft seit 1.7.2026", "", "/mehrwertsteuer-rechner.html?dir=b2n&amount=113&rate=13")
row("AT", "Umsatzsteuer", "Ermäßigter Satz für die in Anlage 3 aufgezählten Gegenstände", "4,9 %", "§ 10 Abs. 1a UStG 1994", U10, "in Kraft seit 1.7.2026 (BGBl. I Nr. 37/2026)", "Nur wenn die Lieferung ausschließlich Gegenstände der Anlage 3 betrifft.", "/mehrwertsteuer-rechner.html?dir=b2n&amount=104.90&rate=4.9")
row("AT", "Umsatzsteuer", "Kleinunternehmergrenze (Umsatz im Vorjahr und im laufenden Jahr)", "55.000 €", "§ 6 Abs. 1 Z 27 UStG 1994", RIS + "bgbl/1994/663/P6/NOR40273856", "Fassung in Kraft seit 1.1.2026")
row("DE", "Umsatzsteuer", "Regelsteuersatz", "19 %", "§ 12 Abs. 1 UStG", GII + "ustg_1980/__12.html", "abgerufene Fassung", "", "/mehrwertsteuer-rechner.html?dir=b2n&amount=119&rate=19")
row("DE", "Umsatzsteuer", "Ermäßigter Satz", "7 %", "§ 12 Abs. 2 UStG", GII + "ustg_1980/__12.html", "abgerufene Fassung", "", "/mehrwertsteuer-rechner.html?dir=b2n&amount=107&rate=7")
row("DE", "Umsatzsteuer", "Kleinunternehmer: Gesamtumsatz im Vorjahr / im laufenden Jahr", "25.000 € / 100.000 €", "§ 19 Abs. 1 UStG", GII + "ustg_1980/__19.html", "abgerufene Fassung")
row("DE", "Umsatzsteuer", "Kleinbetragsrechnung bis zu einem Gesamtbetrag von", "250 €", "§ 33 UStDV", GII + "ustdv_1980/__33.html", "abgerufene Fassung")

P16 = RIS + "bgbl/1988/400/P16/NOR40274823"
row("AT", "Arbeitsweg", "Kleines Pendlerpauschale (Massenverkehrsmittel zumutbar), jährlich", _stufen(PENDLER_AT["klein"], True), "§ 16 Abs. 1 Z 6 lit. c EStG 1988", P16, "Fassung 24.12.2025 bis 31.12.2026", "Freibetrag: mindert die Bemessungsgrundlage, nicht die Steuer selbst.", "/pendlerrechner.html?land=at&km=32&art=klein&tage=11")
row("AT", "Arbeitsweg", "Großes Pendlerpauschale (Massenverkehrsmittel mindestens auf halber Strecke unzumutbar), jährlich", _stufen(PENDLER_AT["gross"], True), "§ 16 Abs. 1 Z 6 lit. d EStG 1988", P16, "Fassung 24.12.2025 bis 31.12.2026", "", "/pendlerrechner.html?land=at&km=32&art=gross&tage=11")
row("AT", "Arbeitsweg", "Pendlerpauschale bei weniger Fahrten im Kalendermonat", "ab 11 Tagen voll · 8 bis 10 Tage zwei Drittel · 4 bis 7 Tage ein Drittel", "§ 16 Abs. 1 Z 6 lit. e EStG 1988", P16, "Fassung 24.12.2025 bis 31.12.2026", "", "/pendlerrechner.html?land=at&km=45&art=klein&tage=8")
row("AT", "Arbeitsweg", "Pendlereuro je Kilometer der einfachen Fahrtstrecke, jährlich", f"{PENDLEREURO_AT} €", "§ 33 Abs. 5 Z 4 EStG 1988", RIS + "bgbl/1988/400/P33/NOR40279893", "Fassung 30.7.2026 bis 31.12.2026", "Absetzbetrag: mindert die Steuer direkt. Setzt Anspruch auf ein Pendlerpauschale voraus.", "/pendlerrechner.html?land=at&km=32&art=klein&tage=11")
row("AT", "Arbeitsweg", "Kilometergeld: Pkw / Motorrad / Zuschlag je mitbeförderter Person / Fahrrad", "0,50 € / 0,25 € / 0,15 € / 0,25 € je km", "§ 10 Abs. 3 bis 5 Reisegebührenvorschrift 1955", RIS + "bgbl/1955/133/P10/NOR40269627", "Fassung in Kraft seit 1.7.2025", "Steuerfrei sind höchstens die Sätze der Bundesbediensteten (§ 26 Z 4 lit. a EStG 1988).", "/fahrtkosten-rechner.html")
row("DE", "Arbeitsweg", "Entfernungspauschale je vollem Kilometer der Entfernung und Arbeitstag", "0,38 €", "§ 9 Abs. 1 Satz 3 Nr. 4 EStG", GII + "estg/__9.html", "abgerufene Fassung", "Höchstens 4.500 € im Kalenderjahr; mehr nur mit eigenem oder überlassenem Kraftwagen.", "/pendlerrechner.html?land=de&km=28&atage=220&auto=1")
row("DE", "Arbeitsweg", "Arbeitnehmer-Pauschbetrag (Werbungskosten ohne Nachweis)", "1.230 €", "§ 9a Satz 1 Nr. 1 Buchst. a EStG", GII + "estg/__9a.html", "abgerufene Fassung", "Die Entfernungspauschale wirkt sich erst aus, soweit alle Werbungskosten zusammen diesen Betrag übersteigen.", "/pendlerrechner.html?land=de&km=28&atage=220&auto=1")
row("DE", "Arbeitsweg", "Wegstreckenentschädigung bei Dienstreisen des Bundes", "0,20 € je km (höchstens 130 €) · 0,30 € je km bei erheblichem dienstlichem Interesse", "§ 5 Abs. 1 und 2 BRKG", GII + "brkg_2005/__5.html", "abgerufene Fassung")

row("AT", "Lohn und Einkommen", "Einkommensteuer-Tarif 2026: Grenzen der Tarifstufen", "bis 13.539 € 0 % · bis 21.992 € 20 % · bis 36.458 € 30 % · bis 70.365 € 40 % · bis 104.859 € 48 % · darüber 50 % · über 1 Mio. € 55 %", "§ 33 Abs. 1 EStG 1988", RIS + "bgbl/1988/400/P33/NOR40279893", "Fassung 30.7.2026 bis 31.12.2026", "Für 2027 nennt die Anmerkung zum Gesetzestext höhere Grenzen (BGBl. II Nr. 260/2026), erste Stufe 13.846 €.")
P67 = RIS + "bgbl/1988/400/P67/NOR40280879"
row("AT", "Lohn und Einkommen", "Sonstige Bezüge (13./14. Gehalt) innerhalb des Jahressechstels", "erste 620 € 0 % · nächste 24.380 € 6 % · nächste 25.000 € 27 % · nächste 33.333 € 35,75 %", "§ 67 Abs. 1 EStG 1988", P67, "Fassung 17.10.2026 bis 31.12.2027", "", "/bruttolohn-14-gehaelter.html")
row("AT", "Lohn und Einkommen", "Freigrenze: keine feste Besteuerung, wenn das Jahressechstel höchstens beträgt", "2.615 € (2026) · 2.675 € (2027)", "§ 67 Abs. 1 EStG 1988 samt Anmerkung 1", P67, "Fassung 17.10.2026 bis 31.12.2027", "Wert für 2027 laut Anmerkung: BGBl. II Nr. 260/2026.", "/bruttolohn-14-gehaelter.html")
row("AT", "Lohn und Einkommen", "Gesetzlicher Mindesturlaub (Dienstzeit unter 25 Jahren / danach)", "30 Werktage / 36 Werktage", "§ 2 Abs. 1 Urlaubsgesetz", RIS + "bgbl/1976/390/P2/NOR40144614", "Fassung in Kraft seit 1.1.2013", "", "/stundenlohn-rechner.html")
row("DE", "Lohn und Einkommen", "Grundfreibetrag ab dem Veranlagungszeitraum 2026", "12.348 €", "§ 32a Abs. 1 EStG", GII + "estg/__32a.html", "abgerufene Fassung")
row("DE", "Lohn und Einkommen", "Gesetzlicher Mindestlohn je Zeitstunde, brutto", "13,90 € ab 1.1.2026 · 14,60 € ab 1.1.2027", "§ 1 MiLoV5", GII + "milov5/__1.html", "abgerufene Fassung", "", "/stundenlohn-rechner.html?dir=h2m&amount=13.90&hours=40&salaries=12")
row("DE", "Lohn und Einkommen", "Gesetzlicher Mindesturlaub", "24 Werktage", "§ 3 Abs. 1 BUrlG", GII + "burlg/__3.html", "abgerufene Fassung", "Werktage sind alle Kalendertage außer Sonn- und gesetzlichen Feiertagen (§ 3 Abs. 2).", "/stundenlohn-rechner.html")
row("DE", "Lohn und Einkommen", "Trinkgelder an Arbeitnehmer von Dritten, freiwillig und ohne Rechtsanspruch", "steuerfrei", "§ 3 Nr. 51 EStG", GII + "estg/__3.html", "abgerufene Fassung", "", "/trinkgeld-rechner.html")

row("AT", "Kapitalerträge", "Kapitalertragsteuer auf Geldeinlagen bei Kreditinstituten", "25 %", "§ 27a Abs. 1 Z 1 EStG 1988", RIS + "bgbl/1988/400/P27a/NOR40263362", "Fassung in Kraft seit 20.7.2024", "", "/realzins-sparen-inflation.html")
row("AT", "Kapitalerträge", "Besonderer Steuersatz auf andere Einkünfte aus Kapitalvermögen", "27,5 %", "§ 27a Abs. 1 Z 2 EStG 1988", RIS + "bgbl/1988/400/P27a/NOR40263362", "Fassung in Kraft seit 20.7.2024", "", "/realzins-sparen-inflation.html")
row("DE", "Kapitalerträge", "Einkommensteuer auf Einkünfte aus Kapitalvermögen (Abgeltungsteuer)", "25 %", "§ 32d Abs. 1 EStG", GII + "estg/__32d.html", "abgerufene Fassung", "Dazu Solidaritätszuschlag, gegebenenfalls Kirchensteuer.", "/realzins-sparen-inflation.html")
row("DE", "Kapitalerträge", "Solidaritätszuschlag", "5,5 % der Bemessungsgrundlage", "§ 4 SolzG 1995", GII + "solzg_1995/__4.html", "abgerufene Fassung", "25 % × 1,055 = 26,375 % auf Kapitalerträge.", "/realzins-sparen-inflation.html")
row("DE", "Kapitalerträge", "Sparer-Pauschbetrag (einzeln / zusammen veranlagte Ehegatten)", "1.000 € / 2.000 €", "§ 20 Abs. 9 EStG", GII + "estg/__20.html", "abgerufene Fassung", "", "/realzins-sparen-inflation.html")

row("AT", "Zinsen und Verzug", "Gesetzliche Zinsen; Verzugszinsen, soweit keine Sonderregel gilt (etwa unter Privaten oder gegenüber Verbrauchern)", "4 % pro Jahr", "§ 1000 Abs. 1 und § 1333 Abs. 1 ABGB", RIS + "jgs/1811/946/P1000/NOR40117762", "Fassung in Kraft seit 11.6.2010", "Nicht für Geldforderungen zwischen Unternehmern (§ 456 UGB) und nicht für Forderungen im Zusammenhang mit einem Arbeitsverhältnis (§ 49a ASGG).", "/verzugszinsen-rechner.html?land=at_v&betrag=1200&von=2026-03-01&bis=2026-10-31")
row("AT", "Zinsen und Verzug", "Verzugszinsen zwischen Unternehmern", "9,2 Prozentpunkte über dem Basiszinssatz", "§ 456 UGB", RIS + "drgbl/1897/219/P456/NOR40148644", "Fassung in Kraft seit 16.3.2013", "Maßgeblich ist der Basiszinssatz am ersten Kalendertag des Halbjahres.", "/verzugszinsen-rechner.html?land=at_u&betrag=5000&von=2026-01-15&bis=2026-10-31")
row("AT", "Zinsen und Verzug", "Gesetzliche Zinsen für Forderungen im Zusammenhang mit einem Arbeitsverhältnis", "9,2 Prozentpunkte über dem Basiszinssatz", "§ 49a ASGG", RIS + "bgbl/1985/104/P49a/NOR40148637", "Fassung in Kraft seit 16.3.2013", "Maßgeblich ist der Basiszinssatz am Tag nach dem Eintritt der Fälligkeit. Beruht die Verzögerung auf einer vertretbaren Rechtsansicht des Schuldners, gelten nur die sonstigen Bestimmungen über die gesetzlichen Zinsen.", "/verzugszinsen-rechner.html?land=at_a&betrag=2500&von=2026-02-01&bis=2026-10-31")
row("AT", "Zinsen und Verzug", "Pauschale für Betreibungskosten zwischen Unternehmern", "40 €", "§ 458 UGB", RIS + "drgbl/1897/219/P458/NOR40148646", "Fassung in Kraft seit 16.3.2013")
row("AT", "Zinsen und Verzug", "Basiszinssatz der Oesterreichischen Nationalbank", f"{_de(BASIS_AT_AENDERUNGEN[-1][1])} % seit 16.9.2026 · am 1.7.2026: {_de(BASIS_AT[-1][1])} %", "OeNB, Basis- und Referenzzinssätze", OENB, "Tabelle zuletzt geändert am 5.10.2026", "Für § 456 UGB gilt im zweiten Halbjahr 2026 der Wert vom 1.7.2026.", "/verzugszinsen-rechner.html")
row("DE", "Zinsen und Verzug", "Verzugszinssatz, wenn ein Verbraucher beteiligt ist", "5 Prozentpunkte über dem Basiszinssatz", "§ 288 Abs. 1 BGB", GII + "bgb/__288.html", "abgerufene Fassung", "", "/verzugszinsen-rechner.html?land=de_v&betrag=1200&von=2026-03-01&bis=2026-10-31")
row("DE", "Zinsen und Verzug", "Verzugszinssatz für Entgeltforderungen ohne Verbraucherbeteiligung", "9 Prozentpunkte über dem Basiszinssatz", "§ 288 Abs. 2 BGB", GII + "bgb/__288.html", "abgerufene Fassung", "", "/verzugszinsen-rechner.html?land=de_u&betrag=5000&von=2026-01-15&bis=2026-10-31")
row("DE", "Zinsen und Verzug", "Verzugspauschale, wenn der Schuldner kein Verbraucher ist", "40 €", "§ 288 Abs. 5 BGB", GII + "bgb/__288.html", "abgerufene Fassung")
row("DE", "Zinsen und Verzug", "Basiszinssatz nach § 247 BGB", f"{_de(BASIS_DE[-1][1])} % seit 1.7.2026 · {_de(BASIS_DE[-2][1])} % seit 1.1.2026", "Deutsche Bundesbank, Basiszinssatz nach § 247 BGB", BBK, "Stand der Tabelle am Abruftag", "Ändert sich jeweils zum 1. Januar und 1. Juli.", "/verzugszinsen-rechner.html")
row("DE", "Zinsen und Verzug", "Gesetzlicher Zinssatz / bei beiderseitigen Handelsgeschäften", "4 % / 5 % pro Jahr", "§ 246 BGB · § 352 Abs. 1 HGB", GII + "bgb/__246.html", "abgerufene Fassung")

row("AT", "Kredit", "Rücktritt vom Kreditvertrag ohne Angabe von Gründen", "14 Tage", "§ 25 Abs. 1 Verbraucherkreditgesetz 2026", RIS + "bgbl/i/2026/36/P25/NOR40278371", "in Kraft ab 20.11.2026", "Gilt für Verträge, die nach dem 19.11.2026 geschlossen werden (§ 45 Abs. 2); für ältere Verträge gelten die bisherigen Bestimmungen weiter.", "/kreditrechner.html")
row("AT", "Kredit", "Entschädigung bei vorzeitiger Rückzahlung, Obergrenze", "1 % des vorzeitig zurückgezahlten Betrags · 0,5 % bei höchstens einem Jahr Restlaufzeit", "§ 29 Abs. 4 Verbraucherkreditgesetz 2026", RIS + "bgbl/i/2026/36/P29/NOR40278375", "in Kraft ab 20.11.2026", "Nie mehr als die Zinsen bis zum Laufzeitende. Dieselben Sätze standen bis 19.11.2026 in § 16 Abs. 3 Verbraucherkreditgesetz.", "/kredit-sondertilgung.html")
row("AT", "Kredit", "Keine Entschädigung, wenn die vorzeitige Rückzahlung innerhalb von zwölf Monaten nicht übersteigt", "10.000 €", "§ 29 Abs. 3 Z 3 Verbraucherkreditgesetz 2026", RIS + "bgbl/i/2026/36/P29/NOR40278375", "in Kraft ab 20.11.2026", "Ebenso keine Entschädigung ohne festen Sollzinssatz, bei Überziehungsmöglichkeiten und bei Tilgung durch eine dafür vereinbarte Versicherung.", "/kredit-sondertilgung.html")
row("DE", "Kredit", "Widerrufsfrist beim Verbraucherdarlehensvertrag", "14 Tage", "§ 495 Abs. 1 in Verbindung mit § 355 Abs. 2 BGB", GII + "bgb/__355.html", "abgerufene Fassung", "", "/kreditrechner.html")
row("DE", "Kredit", "Vorfälligkeitsentschädigung bei Allgemein-Verbraucherdarlehen, Obergrenze", "1 % des vorzeitig zurückgezahlten Betrags · 0,5 % bei höchstens einem Jahr Restlaufzeit", "§ 502 Abs. 3 BGB", GII + "bgb/__502.html", "abgerufene Fassung", "Nie mehr als die Sollzinsen bis zur vereinbarten Rückzahlung.", "/kredit-sondertilgung.html")

row("DE", "Preise", "Preisermäßigung: anzugeben ist der niedrigste Gesamtpreis der letzten", "30 Tage", "§ 11 Abs. 1 PAngV", GII + "pangv_2022/__11.html", "abgerufene Fassung", "", "/rabatt-rechner.html")

THEMEN = list(dict.fromkeys(r["thema"] for r in R))


def e(s):
    return html.escape(s, quote=True)


def tabelle():
    rows = []
    for r in R:
        land = "Österreich" if r["land"] == "AT" else "Deutschland"
        tool = f'<a href="{e(r["tool"])}">{"nachrechnen" if "?" in r["tool"] else "zum Thema"}</a>' if r["tool"] else ""
        hin = f'<span class="rf-h">{e(r["hinweis"])}</span>' if r["hinweis"] else ""
        rows.append(
            f'<tr data-land="{r["land"]}" data-thema="{e(r["thema"])}"><td data-th="Land und Thema">{land}<span class="rf-h">{e(r["thema"])}</span></td>'
            f'<td data-th="Was"><b>{e(r["name"])}</b>{hin}</td><td data-th="Wert" class="rf-w">{e(r["wert"])}</td>'
            f'<td data-th="Fundstelle"><a href="{e(r["url"])}" rel="noopener">{e(r["fund"])}</a><span class="rf-h">{e(r["stand"])} · abgerufen am {ABRUF}</span></td>'
            f'<td data-th="Rechner" class="no-print">{tool}</td></tr>')
    opt = "".join(f'<option value="{e(t)}">{e(t)}</option>' for t in THEMEN)
    return f"""<form class="rf-filter no-print" data-filter="saetze" onsubmit="return false" role="search">
<label class="f">Suche<input type="search" name="q" placeholder="z. B. Pendler, § 288, 4,9" autocomplete="off"></label>
<label class="f">Land<select name="land"><option value="">beide</option><option value="AT">Österreich</option><option value="DE">Deutschland</option></select></label>
<label class="f">Thema<select name="thema"><option value="">alle</option>{opt}</select></label>
<p class="rf-acts"><button type="button" class="linkbtn" data-filter-reset>Filter zurücksetzen</button> <button type="button" class="linkbtn" data-filter-csv>Angezeigte Zeilen als CSV</button> <button type="button" class="linkbtn" onclick="window.print()">Drucken</button></p>
</form>
<p class="small muted" data-filter-count="saetze" aria-live="polite">{len(R)} Einträge</p>
<div class="scroll"><table class="tbl text rf" id="saetze"><thead><tr><th>Land, Thema</th><th>Was</th><th>Wert</th><th>Fundstelle, Fassung, Abruf</th><th class="no-print">Rechner</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p class="hint" data-filter-empty="saetze" hidden>Kein Eintrag passt zu dieser Suche. Die Tabelle enthält nur Werte, die wir im Wortlaut der Quelle nachgelesen haben.</p>"""


def seite():
    n_at = sum(1 for r in R if r["land"] == "AT")
    return f"""<p>{len(R)} Sätze, Grenzen und Fristen, die in Alltagsrechnungen immer wieder gebraucht werden – {n_at} aus Österreich, {len(R) - n_at} aus Deutschland. Jede Zeile nennt die Fundstelle im Gesetz oder bei der amtlichen Stelle, die Fassung und das Datum, an dem wir den Wortlaut dort nachgelesen haben. „nachrechnen“ öffnet einen Rechner mit einer Beispielrechnung, in der dieser Wert vorkommt; „zum Thema“ führt zu einem Rechner oder Ratgeber, der den Wert erklärt, ihn aber nicht als Eingabe vorbelegt. Zeilen ohne Link haben kein passendes Werkzeug.</p>
<p class="jw"><strong>Werte bis 31.12.2026; Aktualisierung Anfang Jänner 2027.</strong> Mehrere Fassungen laufen zum Jahresende aus; was sich ändert, steht unter der Tabelle.</p>
{tabelle()}
<h2>So ist die Tabelle entstanden</h2>
<p>Alle Werte stammen aus dem Wortlaut der verlinkten Vorschrift, abgerufen am {ABRUF}: für Österreich aus der konsolidierten Fassung im Rechtsinformationssystem des Bundes (RIS), für Deutschland aus gesetze-im-internet.de, die Basiszinssätze aus den Tabellen der Oesterreichischen Nationalbank und der Deutschen Bundesbank. Zusammenfassungen anderer Websites haben wir nicht übernommen. Was wir nicht im Gesetzestext oder bei der zuständigen Stelle nachlesen konnten, steht nicht in der Tabelle – deshalb fehlen etwa Sozialversicherungssätze und Höchstbeitragsgrundlagen.</p>
<p>„Abgerufene Fassung“ heißt bei deutschen Vorschriften: der Text, den gesetze-im-internet.de am Abruftag als geltend zeigte; die Seite nennt bei der Einzelnorm kein Inkrafttretensdatum. Bei österreichischen Vorschriften nennt das RIS zu jeder Fassung, seit wann und gegebenenfalls bis wann sie gilt; diese Daten stehen in der Spalte „Fundstelle“.</p>
<h2>Was sich demnächst ändert</h2>
<ul><li><strong>Verbraucherkredite in Österreich:</strong> Am 20. November 2026 tritt das Verbraucherkreditgesetz 2026 in Kraft (BGBl. I Nr. 36/2026, Umsetzung der Richtlinie (EU) 2023/2225). Es gilt für Verträge, die nach dem 19. November 2026 geschlossen werden; für ältere Verträge bleiben die bisherigen Bestimmungen anwendbar (§ 45 Abs. 2 und 3). Rücktritt und vorzeitige Rückzahlung stehen ab 20. November 2026 in § 25 und § 29.</li>
<li><strong>Österreichische Steuerwerte 2027:</strong> Mehrere Fassungen im Einkommensteuergesetz laufen am 31. Dezember 2026 aus (Tarifstufen, Pendlereuro, Pendlerpauschale). Für die Tarifgrenzen und die Freigrenze beim Jahressechstel nennt der Gesetzestext die Werte für 2027 bereits in Anmerkungen; sie stehen in der Tabelle dabei.</li>
<li><strong>Basiszinssätze:</strong> Der deutsche Basiszinssatz ändert sich jeweils zum 1. Jänner und 1. Juli. Der österreichische ändert sich mit den Zinsbeschlüssen; für Verzugszinsen zwischen Unternehmern zählt der Wert am ersten Tag des Halbjahres.</li>
<li><strong>Mindestlohn Deutschland:</strong> 14,60 € ab 1. Jänner 2027 stehen bereits in der Verordnung.</li></ul>
<h2>Grenzen</h2>
<p>Die Tabelle gibt Zahlen wieder, nicht die Voraussetzungen im Einzelfall. Ob ein ermäßigter Steuersatz gilt, ob ein Pendlerpauschale zusteht oder ob Verzug eingetreten ist, hängt von Bedingungen ab, die im verlinkten Gesetzestext stehen. Die Tabelle ersetzt keine Steuer- oder Rechtsberatung. Findest du eine Abweichung zum aktuellen Gesetzestext, schreib uns bitte an <a href="mailto:office@adstern.com">office@adstern.com</a> – wir prüfen die Zeile und korrigieren sie mit neuem Abrufdatum.</p>"""


def saetze_js():
    """Die Zahlen für calc.js als JSON – build.py vergleicht sie mit der Zeile zwischen /*SAETZE*/ … /*/SAETZE*/."""
    import json
    d = {"pendler": {k: [list(x) for x in v] for k, v in PENDLER_AT.items()}, "pendlereuro": PENDLEREURO_AT, "entf": ENTF_DE, "entfMax": ENTF_DE_MAX, "anp": AN_PAUSCH_DE,
         "verzug": VERZUG, "verzugAb": BASIS_DE[0][0], "verzugBis": VERZUG_BIS, "basis": {"de": [list(x) for x in BASIS_DE], "at": [list(x) for x in BASIS_AT], "atTag": [list(x) for x in BASIS_AT_TAG]}}
    return json.dumps(d, ensure_ascii=False, separators=(",", ":"))
