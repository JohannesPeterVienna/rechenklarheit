# Rechenklarheit

Statische Website für https://rechenklarheit.de – 18 Rechner mit Rechenweg, eine Referenztabelle gesetzlicher Sätze und Ratgeber.

- `assets/calc.js` – alle Rechner (Browser)
- `content/calcs.py`, `content/articles.py` – Inhalte, Beispiele werden in Python berechnet
- `content/referenz.py` – Sätze und Grenzwerte aus Gesetz und amtlichen Quellen (Fundstelle, Fassung, Abrufdatum); einzige Stelle für diese Zahlen, `build.py` bricht ab, wenn `calc.js` abweicht
- `content/eigen.py` – Beispiele zum Anklicken, Pendler- und Verzugszinsen-Rechner, Grafiken der Ratgeber, zusammengelegte Seiten (Weiterleitungen)
- `build.py` – erzeugt `docs/` (GitHub Pages)

Bauen: `pip install jinja2 && python3 build.py`

Tests (laufen beim Bauen mit, Build bricht bei Fehlern ab): `node test_calc.js` (Rechner), `node test_einwilligung.js` (Einwilligung: Google-CMP vs. Statistik-Zettel). Nach dem Bauen zusätzlich `node test_werbeflaechen.js` (Playwright: leere Werbeflächen unsichtbar, gefüllte mit Abstand sichtbar) und `node test_seiten.js` (Playwright: alle Seiten der Sitemap bei 390 und 1366 px, jeder Rechner mit Beispielen, Unsinnseingaben, Vergleich, Link, CSV; Referenztabelle; Weiterleitungen).

Shop: abgeschaltet über `SHOP_AN = False` in `content/shop.py` (keine `shop.html`), bis ein echter Kauf funktioniert.

## Pflege zum Jahreswechsel und zu den Halbjahren

Alle gesetzlichen Zahlen stehen in `content/referenz.py`. Nach jeder Änderung `/*SAETZE*/…` in `assets/calc.js` aus `referenz.saetze_js()` neu setzen (der Build bricht sonst ab), Tests in `test_calc.js` anpassen, neu bauen.

- **Basiszinssätze** (1.1. und 1.7.): `BASIS_DE` um das neue Halbjahr ergänzen (Bundesbank); `BASIS_AT_AENDERUNGEN` um jeden neuen Änderungstag (OeNB) – `BASIS_AT` und `BASIS_AT_TAG` entstehen daraus. Schleife in `_at_halbjahre()` um das neue Jahr erweitern.
- **`VERZUG_BIS`** auf das Ende des Halbjahres setzen, für das beide Basiszinssätze feststehen; `max=` der Datumsfelder und den Hinweis „Werte bis …“ in `content/eigen.py` mitziehen.
- **Pendlerwerte** (Anfang Jänner): `PENDLER_AT`, `PENDLEREURO_AT` (Fassungen laufen am 31.12.2026 aus), `ENTF_DE`, `ENTF_DE_MAX`, `AN_PAUSCH_DE` im Gesetzestext nachlesen; Jahreszahl „2026“ im Pendlerrechner (Formularhinweis, Überschriften, Ergebniszeilen in `calc.js`) ersetzen.
- **Tabellenzeilen mit Jahreswerten:** Einkommensteuer-Tarif und Freigrenze AT, Grundfreibetrag und Mindestlohn DE.
- **`ABRUF`** nur für Zeilen erhöhen, die tatsächlich neu nachgelesen wurden; bei Bedarf je Zeile ein eigenes Abrufdatum einführen.
