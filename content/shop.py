"""Shop für Druckvorlagen (PDF) – Bezahlung über Lemon Squeezy (Store „AdStern Digital“, Merchant of Record).

Unsichtbar (noindex, kein Link, nicht in der Sitemap), solange kein Produkt Checkout-Link UND Preis hat.
Produktdateien erzeugt produkte/formelsammlung.py (nicht in docs/ – sonst wären sie frei herunterladbar).
"""

PRODUCTS = [
    {
        "slug": "formelsammlung-alltagsmathematik",
        "title": "Formelsammlung Alltagsmathematik – mit Rechenweg",
        "text": "Die Formeln aller Rechenklarheit-Rechner auf einem gestalteten Heft: Prozent, Mehrwertsteuer (AT und DE), Rabatt, "
                "Zinseszins, Kredit, Dreisatz, Bruch, Durchschnitt, Stundenlohn, Strom- und Fahrtkosten, Aufschlag und Marge – "
                "jeweils mit durchgerechnetem Beispiel und den typischen Fehlern. Zum Ausdrucken für Schule, Lehre und Alltag.",
        "format": "PDF · A4 · zum Ausdrucken",
        "price": "",          # Vorschlag 2,90 € – Entscheidung Johannes
        "checkout": "",       # Lemon-Squeezy-Link, erst nach Freischaltung des Stores
    },
]

SHOP_LIVE = any(p["checkout"] and p["price"] for p in PRODUCTS)
