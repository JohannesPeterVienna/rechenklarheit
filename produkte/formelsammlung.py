"""Formelsammlung Alltagsmathematik (PDF, A4) – Shop-Produkt von Rechenklarheit.

Alle Beispielzahlen werden hier berechnet, nicht abgetippt. Aufruf: python produkte/formelsammlung.py <Zielordner>
Nur PDF-Standardschriften (Times, Helvetica, Courier). Ergebnis gehört NICHT nach docs/.
"""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, white
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

INK = Color(.08, .08, .08); MUTED = Color(.37, .37, .35); PEN = Color(.149, .278, .776); GRID = Color(.91, .918, .933); RED = Color(.70, .14, .17)
W, H = A4
STAND = "Stand 5. November 2026"


def de(x, d=2):
    s = f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


def eur(x): return de(x) + " €"


def annuity(K, p, m):
    i = p / 100 / 12
    return K * i / (1 - (1 + i) ** -m)


def eff(K, m, p, fee, mon):
    a = annuity(K, p, m); lo, hi = 0.0, 0.1
    for _ in range(200):
        r = (lo + hi) / 2
        pv = sum((a + mon) / (1 + r) ** t for t in range(1, m + 1))
        if pv > K - fee: lo = r
        else: hi = r
    return a, a * m + fee + mon * m, ((1 + r) ** 12 - 1) * 100


_rate = annuity(20000, 4.5, 60)
_A = eff(20000, 60, 4.5, 0, 0); _B = eff(20000, 60, 3.9, 400, 3)
_zz = 10000 * 1.03 ** 10
import math
_dbl = math.log(2) / math.log(1.03)
_kwh = 100 * 4 * 365 / 1000
_l = 230 * 6.5 / 100
_tip = 87.40 * 1.10

SECTIONS = [
    ("Prozentrechnung", ["Prozentwert W = Grundwert G × p ÷ 100", "Prozentsatz p = W ÷ G × 100", "Grundwert G = W ÷ p × 100"],
     ["15 % von 80: 80 × 15 ÷ 100 = 12", "12 von 80 in Prozent: 12 ÷ 80 × 100 = 15 %", "12 sind 15 % von: 12 ÷ 15 × 100 = 80"],
     f"+25 % und danach −25 % ergeben nicht den Ausgangswert: 100 → 125 → {de(125 * 0.75)}. Die Basis ist jedes Mal eine andere."),
    ("Prozentuale Veränderung", ["Veränderung = (neu − alt) ÷ alt × 100"],
     ["Von 80 auf 96: (96 − 80) ÷ 80 × 100 = +20 %", f"Zurück von 96 auf 80: (80 − 96) ÷ 96 × 100 = {de(-16 / 96 * 100)} %"],
     "Prozent und Prozentpunkte nicht verwechseln: von 2 % auf 3 % sind +1 Prozentpunkt, aber +50 Prozent."),
    ("Mehrwertsteuer (Österreich und Deutschland)", ["Brutto = Netto × (1 + Steuersatz)", "Netto = Brutto ÷ (1 + Steuersatz)", "Österreich: 20 %, 13 %, 10 %, 4,9 % · Deutschland: 19 %, 7 %"],
     ["120 € brutto bei 20 %: 120 ÷ 1,20 = 100 € netto, darin 20 € Steuer", f"100 € netto bei 19 %: 100 × 1,19 = {eur(119)} brutto"],
     "Die Steuer nicht vom Bruttobetrag abziehen: 120 € − 20 % = 96 € ist falsch. Immer durch 1,20 teilen."),
    ("Rabatt und Skonto", ["Endpreis = Preis × (1 − r1) × (1 − r2)", "Skonto: Betrag × (1 − Skontosatz)"],
     [f"100 € mit 30 % und 20 % Rabatt: 100 × 0,70 × 0,80 = {eur(56)}", "Ersparnis: 44 % – nicht 50 %", f"1.000 € mit 2 % Skonto: 1.000 × 0,98 = {eur(980)}"],
     "Mehrere Rabatte nie addieren: Jeder wirkt auf den schon reduzierten Preis."),
    ("Zinseszins", ["K(n) = K(0) × (1 + p)^n", "72er-Regel: Verdopplungszeit etwa 72 ÷ Zinssatz"],
     [f"10.000 € zu 3 % auf 10 Jahre: 10.000 × 1,03^10 = {eur(_zz)}", f"Verdopplung bei 3 %: 72 ÷ 3 = etwa 24 Jahre (genau {de(_dbl, 1)} Jahre)"],
     "Zinsen auf Zinsen wachsen nicht linear: 3 % über 10 Jahre sind mehr als 30 %."),
    ("Ratenkredit (Annuität)", ["Rate = K × i ÷ (1 − (1 + i)^(−n))", "i = Sollzins ÷ 12, n = Anzahl der Monatsraten"],
     [f"20.000 € zu 4,5 % auf 60 Monate: Rate {eur(_rate)}", f"Gesamt: {eur(_rate * 60)}, davon Zinsen {eur(_rate * 60 - 20000)}"],
     "Eine längere Laufzeit senkt die Rate, macht den Kredit aber teurer."),
    ("Kreditangebote vergleichen", ["Gesamtkosten = Rate × Monate + Bearbeitungsgebühr + Kontoführung", "Effektivzins: Zins, bei dem alle Zahlungen dem ausbezahlten Betrag entsprechen"],
     [f"A: 4,5 %, keine Gebühren → {eur(_A[1])}, effektiv ca. {de(_A[2])} %", f"B: 3,9 %, 400 € + 3 €/Monat → {eur(_B[1])}, effektiv ca. {de(_B[2])} %"],
     f"Der niedrigere Sollzins (B) ist hier um {eur(_B[1] - _A[1])} teurer. Entscheidend sind Gesamtkosten und Effektivzins."),
    ("Inflation und Kaufkraft", ["Kaufkraft = Betrag ÷ (1 + Inflation)^n"],
     [f"1.000 € bei 2 % Inflation nach 10 Jahren: 1.000 ÷ 1,02^10 = {eur(1000 / 1.02 ** 10)}"],
     "Sparzinsen gleichen die Inflation nur aus, wenn sie nach Steuer mindestens so hoch sind."),
    ("Dreisatz", ["proportional: x = b ÷ a × c", "umgekehrt proportional: x = a × b ÷ c"],
     ["4 kg kosten 300 € → 6 kg: 300 ÷ 4 × 6 = 450 €", "4 Personen brauchen 6 Tage → 3 Personen: 4 × 6 ÷ 3 = 8 Tage"],
     "Erst prüfen: Wird es mit mehr vom einen auch mehr vom anderen (proportional) – oder weniger?"),
    ("Bruchrechnung", ["a/b + c/d = (a·d + c·b) ÷ (b·d)", "a/b × c/d = (a·c) ÷ (b·d) · Teilen: mit dem Kehrwert malnehmen"],
     ["1/3 + 1/4 = 4/12 + 3/12 = 7/12", "2/3 ÷ 4/5 = 2/3 × 5/4 = 10/12 = 5/6"],
     "Beim Addieren nie Zähler und Nenner einzeln addieren: 1/3 + 1/4 ist nicht 2/7."),
    ("Einheiten", ["1 m = 100 cm · 1 m² = 10.000 cm² · 1 m³ = 1.000 l", "°F = °C × 9 ÷ 5 + 32"],
     ["2,5 m² = 25.000 cm²", "20 °C = 20 × 9 ÷ 5 + 32 = 68 °F", "1 l = 1 dm³ = 1.000 cm³"],
     "Bei Flächen und Volumen zählt der Faktor im Quadrat bzw. hoch drei: 1 m² sind nicht 100 cm²."),
    ("Durchschnitt und Notenschnitt", ["Mittelwert = Summe ÷ Anzahl", "gewichtet = Summe(Note × Gewicht) ÷ Summe der Gewichte"],
     ["Noten 2, 3, 1: (2 + 3 + 1) ÷ 3 = 2,0", "Schularbeit 2 (doppelt), Test 3, Mitarbeit 1: (4 + 3 + 1) ÷ 4 = 2,0", "Median von 1, 2, 2, 5, 5: der mittlere Wert = 2"],
     "Ausreißer verschieben den Mittelwert stark – der Median ist dann aussagekräftiger."),
    ("Stundenlohn", ["Stundenlohn = Monatsgehalt × Gehälter ÷ (Wochenstunden × 52)"],
     [f"Österreich, 3.000 € × 14 ÷ (38,5 × 52) = {eur(3000 * 14 / (38.5 * 52))}", f"Deutschland, 3.000 € × 12 ÷ (40 × 52) = {eur(3000 * 12 / (40 * 52))}"],
     "In Österreich die Sonderzahlungen (13. und 14. Gehalt) nicht vergessen. Brutto, nicht netto."),
    ("Stromkosten", ["kWh = Watt × Stunden ÷ 1.000", "Kosten = kWh × Preis pro kWh"],
     [f"Fernseher 100 W, 4 h täglich: 100 × 4 × 365 ÷ 1.000 = {de(_kwh, 0)} kWh", f"bei 30 Cent: {de(_kwh, 0)} × 0,30 = {eur(_kwh * 0.30)} pro Jahr"],
     "Watt und Kilowattstunden nicht verwechseln – erst mal Stunden, dann durch 1.000."),
    ("Fahrtkosten", ["Kosten = km × Verbrauch ÷ 100 × Preis"],
     [f"230 km bei 6,5 l/100 km: 230 × 6,5 ÷ 100 = {de(_l)} l", f"bei 1,70 €/l: {de(_l)} × 1,70 = {eur(_l * 1.70)} für eine Strecke"],
     "Hin und zurück zählt doppelt; beim Teilen auf alle Mitfahrenden aufteilen."),
    ("Trinkgeld", ["Gesamt = Rechnung × (1 + Trinkgeld) · pro Person = Gesamt ÷ Personen"],
     [f"87,40 € + 10 %: {eur(_tip)}, aufgerundet 97,00 €", "durch 4 Personen: 97,00 ÷ 4 = 24,25 €"],
     "Erst runden, dann teilen – sonst stimmt die Summe am Ende nicht."),
    ("Aufschlag und Handelsspanne", ["Aufschlag = Gewinn ÷ Einkaufspreis × 100", "Handelsspanne (Marge) = Gewinn ÷ Verkaufspreis × 100"],
     [f"Einkauf 60 €, Verkauf 100 €: Aufschlag 40 ÷ 60 = {de(40 / 60 * 100)} %", "Handelsspanne 40 ÷ 100 = 40 %"],
     "Aufschlag und Marge sind nicht dasselbe: Wer 40 % Marge will, braucht 66,67 % Aufschlag."),
]


def grid(c):
    c.setStrokeColor(GRID); c.setLineWidth(.4)
    step = 5 * mm
    x = 0
    while x <= W: c.line(x, 0, x, H); x += step
    y = 0
    while y <= H: c.line(0, y, W, y); y += step


def footer(c, n):
    c.setFont("Helvetica", 7.5); c.setFillColor(MUTED)
    c.drawString(18 * mm, 10 * mm, "Rechenklarheit · rechenklarheit.de · Formelsammlung Alltagsmathematik")
    c.drawRightString(W - 18 * mm, 10 * mm, f"{STAND} · ohne Gewähr · Seite {n}")


def cover(c):
    grid(c)
    c.setFillColor(INK); c.setFont("Times-Bold", 40); c.drawString(18 * mm, H - 70 * mm, "Formelsammlung")
    c.setFont("Times-Roman", 26); c.drawString(18 * mm, H - 84 * mm, "Alltagsmathematik mit Rechenweg")
    c.setStrokeColor(INK); c.setLineWidth(1.6); c.line(18 * mm, H - 90 * mm, W - 18 * mm, H - 90 * mm)
    c.setFont("Courier", 16); c.setFillColor(PEN)
    c.drawString(18 * mm, H - 110 * mm, "15 % von 80 = 80 × 15 ÷ 100 = 12")
    c.setFillColor(INK); c.setFont("Helvetica", 11)
    y = H - 135 * mm
    for i, (t, *_rest) in enumerate(SECTIONS):
        c.drawString(18 * mm, y, f"{i + 1:02d}"); c.drawString(30 * mm, y, t); y -= 6.4 * mm
    c.setFont("Helvetica", 9); c.setFillColor(MUTED)
    c.drawString(18 * mm, 24 * mm, "Alle Beispiele sind nachgerechnet. Zum Ausdrucken für Schule, Lehre und Alltag – nur für den privaten Gebrauch.")
    footer(c, 1)


def lines(c, text, font, size, width):
    return simpleSplit(text, font, size, width)


def section_height(c, sec, width):
    t, fx, ex, warn = sec
    h = 10 * mm + len(fx) * 6.5 * mm + 6 * mm
    for e in ex: h += len(lines(c, e, "Helvetica", 10, width - 6 * mm)) * 4.8 * mm
    h += 5 * mm + len(lines(c, "Achtung: " + warn, "Helvetica", 9.5, width - 6 * mm)) * 4.6 * mm + 8 * mm
    return h


def draw_section(c, i, sec, x, y, width):
    t, fx, ex, warn = sec
    c.setFillColor(INK); c.setFont("Times-Bold", 15); c.drawString(x, y, f"{i:02d}  {t}")
    c.setStrokeColor(INK); c.setLineWidth(1); c.line(x, y - 2.5 * mm, x + width, y - 2.5 * mm)
    y -= 9.5 * mm
    c.setFont("Courier-Bold", 10.5); c.setFillColor(PEN)
    for f in fx:
        c.drawString(x + 2 * mm, y, f); y -= 6.5 * mm
    y -= 1 * mm
    c.setFont("Helvetica-Bold", 9); c.setFillColor(MUTED); c.drawString(x, y, "BEISPIEL"); y -= 5 * mm
    c.setFont("Helvetica", 10); c.setFillColor(INK)
    for e in ex:
        for ln in lines(c, e, "Helvetica", 10, width - 6 * mm):
            c.drawString(x + 2 * mm, y, ln); y -= 4.8 * mm
    y -= 1.5 * mm
    c.setFillColor(RED); c.setFont("Helvetica-Bold", 9.5); c.drawString(x, y, "Achtung:")
    c.setFillColor(INK); c.setFont("Helvetica", 9.5)
    wl = lines(c, "Achtung: " + warn, "Helvetica", 9.5, width - 6 * mm)
    first = True
    for ln in wl:
        if first: c.drawString(x + c.stringWidth("Achtung: ", "Helvetica-Bold", 9.5), y, ln[len("Achtung: "):]); first = False
        else: c.drawString(x, y, ln)
        y -= 4.6 * mm
    return y - 6 * mm


def main(target):
    target = Path(target); target.mkdir(parents=True, exist_ok=True)
    out = target / "rechenklarheit-formelsammlung-alltagsmathematik.pdf"
    c = canvas.Canvas(str(out), pagesize=A4); c.setTitle("Formelsammlung Alltagsmathematik – Rechenklarheit"); c.setAuthor("Rechenklarheit (AdStern)")
    cover(c); c.showPage()
    page = 2; width = W - 36 * mm; x = 18 * mm
    grid(c); y = H - 22 * mm
    for i, sec in enumerate(SECTIONS, 1):
        h = section_height(c, sec, width)
        if y - h < 20 * mm:
            footer(c, page); c.showPage(); page += 1; grid(c); y = H - 22 * mm
        y = draw_section(c, i, sec, x, y, width)
    footer(c, page); c.save()
    print(out, page, "Seiten")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent.parent / "rk-produkte")
