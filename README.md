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
