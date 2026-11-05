"""Shop für Druckvorlagen (PDF) – Bezahlung über Lemon Squeezy (Store „AdStern Digital“, Merchant of Record).

Abgeschaltet (shop.html wird nicht gebaut → 404, kein Link, nicht in der Sitemap), solange SHOP_AN False ist.
SHOP_AN erst auf True stellen, wenn ein echter Kauf funktioniert (nicht nur der Lemon-Squeezy-Testmodus) und
mindestens ein Produkt Checkout-Link UND Preis hat.
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

SHOP_AN = False   # AdSense-Prüfung 5.11.2026: keine Shop-Seite ohne funktionierenden Kauf

SHOP_LIVE = SHOP_AN and any(p["checkout"] and p["price"] for p in PRODUCTS)
