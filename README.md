# Rechenklarheit

Statische Website für https://rechenklarheit.de – 11 Rechner mit Rechenweg plus Ratgeber.

- `assets/calc.js` – alle Rechner (Browser)
- `content/calcs.py`, `content/articles.py` – Inhalte, Beispiele werden in Python berechnet
- `build.py` – erzeugt `docs/` (GitHub Pages)

Bauen: `pip install jinja2 && python3 build.py`
