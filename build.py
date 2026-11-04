"""Erzeugt Rechenklarheit als statische Website in docs/ (GitHub Pages)."""
import shutil, sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
sys.path.insert(0, str(Path(__file__).parent))
from content.calcs import CALCS, PERCENT_FORM
from content.articles import ARTICLES
from content.pages import home_why, home_method, HOME_PUBLISHER, about_body

ROOT = Path(__file__).parent; OUT = ROOT / "docs"
SITE = "https://rechenklarheit.de"; V = "20261104a"; UPDATED = "November 2026"
CHECKED = "4. November 2026"; CHECKED_ISO = "2026-11-04"   # sichtbare Prüfzeile auf Rechner- und Ratgeberseiten
NAV = [("/", "Alle Rechner"), ("/prozentrechner.html", "Prozent"), ("/mehrwertsteuer-rechner.html", "Mehrwertsteuer"),
       ("/zinseszins-rechner.html", "Zinsen"), ("/kreditrechner.html", "Kredit"), ("/#ratgeber", "Ratgeber")]
env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True, trim_blocks=True, lstrip_blocks=True)
PAGES = []
LEGAL_ADDR = "AdStern :: Agentur für digitales Marketing<br>Seilerstätte 8, 1010 Wien, Österreich<br>E-Mail: <a href='mailto:office@adstern.com'>office@adstern.com</a><br>Web: <a href='https://www.adstern.com'>www.adstern.com</a>"
BYSLUG = {a["slug"]: a for a in ARTICLES}


def write(path, template, **ctx):
    base = dict(site=SITE, v=V, updated=UPDATED, nav=NAV, active=ctx.get("active", "/" + path), jsonld=[], ads=True,
                robots=None, og_title=None, calcs=CALCS, articles=ARTICLES, year=2027, checked=None)
    base.update(ctx)
    base["path"] = "/" if path == "index.html" else "/" + path
    if template == "calc.html":
        # Erste Anzeige erst nach dem ersten Erklärabschnitt unter dem Rechner, nicht direkt unter Formular/Ergebnis
        body = base["body"]
        cut = body.find("<h2", body.find("<h2") + 1) if body.count("<h2") > 1 else -1
        base["body_first"], base["body_rest"] = (body[:cut], body[cut:]) if cut > 0 else (body, "")
    (OUT / path).write_text(env.get_template(template).render(**base), encoding="utf-8")
    if base.get("robots") is None:
        PAGES.append((base["path"], ctx.get("priority", 0.6)))


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + h} for i, (h, n) in enumerate(items)]}


def main():
    import subprocess, re
    # Rechner-Test: Build bricht bei Fehlern ab. Die Zahl der Prüfungen steht auf Startseite und „Über uns“.
    test = subprocess.run(["node", str(ROOT / "test_calc.js")], check=True, capture_output=True, text=True)
    print(test.stdout.strip())
    n_tests = sum(int(x) for x in re.findall(r"(\d+) [A-ZÄÖÜ]", test.stdout))
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for f in (ROOT / "assets").iterdir(): shutil.copy(f, OUT / "assets" / f.name)

    intro = """<p>Prozent heißt „von Hundert“. 15 % von 80 sind also 15 Hundertstel von 80: 80 × 15 ÷ 100 = 12.
    Damit lässt sich fast jede Alltagsfrage lösen – vom Rabatt im Geschäft über die Mehrwertsteuer auf der Rechnung bis zur Gehaltserhöhung.</p>
    <p>Die zwei häufigsten Stolperfallen: der falsche <a href="/grundwert-richtig-waehlen.html">Grundwert</a> und die Verwechslung von
    <a href="/prozent-oder-prozentpunkte.html">Prozent und Prozentpunkten</a>. Beide erklären wir mit Beispielen.</p>"""
    write("index.html", "home.html", title="Rechenklarheit – Rechner mit Rechenweg: Prozent, Mehrwertsteuer, Zinsen & mehr",
          description="Kostenlose Online-Rechner mit Rechenweg: Prozentrechner, Mehrwertsteuer für Österreich und Deutschland, Rabatt, Zinseszins, Kredit, Dreisatz, Brüche, Einheiten.",
          hero_form=PERCENT_FORM, intro=intro, why=home_why(n_tests), method=home_method(n_tests), publisher=HOME_PUBLISHER,
          articles=ARTICLES, priority=1.0, active="/",
          jsonld=[{"@context": "https://schema.org", "@type": "WebSite", "name": "Rechenklarheit", "url": SITE + "/", "inLanguage": "de"}])

    for c in CALCS:
        crumbs = [("/", "Rechner"), ("/" + c["slug"] + ".html", c["short"])]
        ld = [crumbs_ld(crumbs), {"@context": "https://schema.org", "@type": "WebApplication", "name": c["h1"], "url": f"{SITE}/{c['slug']}.html",
              "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "inLanguage": "de",
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}}]
        write(c["slug"] + ".html", "calc.html", title=f"{c['title']} | Rechenklarheit", description=c["description"], h1=c["h1"],
              lead=c["lead"], formula=c.get("formula"), form=c["form"], body=c["body"], slug=c["slug"], crumbs=crumbs,
              related=[BYSLUG[s] for s in c.get("related", []) if s in BYSLUG], jsonld=ld, priority=0.9, checked=CHECKED)

    for a in ARTICLES:
        crumbs = [("/", "Rechner"), ("/" + a["slug"] + ".html", a["title"])]
        ld = [crumbs_ld(crumbs), {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["description"],
              "inLanguage": "de", "datePublished": a["published"], "dateModified": CHECKED_ISO,
              "author": {"@type": "Organization", "name": "AdStern", "url": "https://www.adstern.com"},
              "publisher": {"@type": "Organization", "name": "AdStern", "url": "https://www.adstern.com"}}]
        write(a["slug"] + ".html", "page.html", title=f"{a['title']} | Rechenklarheit", description=a["description"], h1=a["title"],
              lead=a["teaser"], body=a["body"], crumbs=crumbs, related=[BYSLUG[s] for s in a["related"]], jsonld=ld, priority=0.7,
              checked=CHECKED)

    write("about.html", "page.html", title="Über Rechenklarheit", description="Wer hinter Rechenklarheit steht und wie die Rechner arbeiten.",
          h1="Über Rechenklarheit", lead="Rechner, die zeigen, wie gerechnet wird.", priority=0.3,
          body=about_body(n_tests))
    write("imprint.html", "page.html", title="Impressum | Rechenklarheit", description="Impressum von Rechenklarheit.", h1="Impressum",
          ads=False, robots="noindex,follow", body=f"""<h2>Medieninhaber und Herausgeber</h2><p>{LEGAL_ADDR}</p>
<h2>Unternehmensangaben</h2><p>Unternehmensgegenstand: Werbeagentur<br>UID-Nummer: ATU54682507<br>Gewerbebehörde: Magistratisches Bezirksamt für den 1. und 8. Bezirk, Wien<br>Kammerzugehörigkeit: Wirtschaftskammer Wien, Fachgruppe Werbung und Marktkommunikation<br>Berufsbezeichnung: Werbeagentur (Gewerbe, verliehen in Österreich)<br>Anwendbare Rechtsvorschriften: Gewerbeordnung, abrufbar unter <a href="https://www.ris.bka.gv.at" rel="noopener">www.ris.bka.gv.at</a></p>
<p>Angaben nach § 5 E-Commerce-Gesetz und § 25 Mediengesetz.</p>
<h2>Grundlegende Richtung</h2><p>Rechenklarheit ist eine unabhängige Informationsseite mit Online-Rechnern und Erklärungen zu Alltagsmathematik, Steuern und Finanzen. Die Seite finanziert sich über Werbung.</p>
<h2>Haftung</h2><p>Alle Rechner und Angaben wurden sorgfältig erstellt, erfolgen aber ohne Gewähr. Sie ersetzen keine Steuer-, Rechts- oder Finanzberatung.</p>""")
    body = (ROOT / "content" / "privacy_body.html").read_text(encoding="utf-8")
    body = body.replace("Kalender, Planer und Rechner arbeiten", "Alle Rechner arbeiten").replace(
        " Damit die Seite sich dein Bundesland merkt, speichern wir es im lokalen Speicher deines Browsers (localStorage). Diese Speicherung ist für die von dir gewünschte Funktion erforderlich (§ 165 Abs. 3 TKG 2021). Du kannst sie jederzeit über die Browser-Einstellungen löschen.", " Wir speichern keine Eingaben.")
    assert "Bundesland" not in body
    write("privacy.html", "page.html", title="Datenschutz | Rechenklarheit", description="Datenschutzerklärung von Rechenklarheit.",
          h1="Datenschutzerklärung", lead="Stand: 29. Oktober 2026", ads=False, robots="noindex,follow", body=body)
    write("404.html", "page.html", title="Seite nicht gefunden | Rechenklarheit", description="Diese Seite gibt es nicht.",
          h1="Diese Seite gibt es nicht", lead="Hier geht es zu allen Rechnern.", ads=False, robots="noindex",
          body="<p><a href='/'>Alle Rechner</a></p>")

    (OUT / "assets" / "icon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect x="1.5" y="1.5" width="29" height="29" rx="7" fill="#2647C6"/><path d="M8 11h7M11.5 7.5v7M18 11h6M8 21.5l5-5M13 21.5l-5-5M18 19h6M18 23h6" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg>')
    (OUT / "CNAME").write_text("rechenklarheit.de\n"); (OUT / ".nojekyll").write_text("")
    (OUT / "google9bf1079fd4bf073e.html").write_text("google-site-verification: google9bf1079fd4bf073e.html")
    (OUT / "ads.txt").write_text("google.com, pub-7811071715414905, DIRECT, f08c47fec0942fa0\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{CHECKED_ISO}</lastmod><priority>{pr}</priority></url>" for p, pr in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print(f"{len(PAGES)} indexierbare Seiten")


if __name__ == "__main__":
    main()
