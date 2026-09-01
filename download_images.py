#!/usr/bin/env python3
"""
download_images.py

Laedt alle OeBV-Grafiken fuer die Marschwertungs-Unterlagen nach img/ herunter.

Quelle: Oesterreichischer Blasmusikverband, "Musik in Bewegung"
        https://wiki.blasmusik.at/display/MIB/Musik+in+Bewegung
Verwendung nur fuer den internen Vereinsgebrauch.

Aufruf:
    python download_images.py            normal
    python download_images.py --force    vorhandene Dateien neu laden

Braucht nur Python 3 (keine Zusatzpakete).
"""

import sys
import ssl
import urllib.request
import urllib.error
from pathlib import Path

BASE4 = "https://wiki.blasmusik.at/download/attachments/9601801"
BASE5 = "https://wiki.blasmusik.at/download/attachments/9601953"
BASE5T = "https://wiki.blasmusik.at/download/thumbnails/9601953"
BASE6 = "https://wiki.blasmusik.at/download/attachments/9601749"

# (Dateiname, URL, Fallback-URL oder None)
IMAGES = [
    # Kapitel 4 - Abfallen und Aufmarschieren
    ("04-zeichen-abfallen-ohne-spiel.png",
     f"{BASE4}/image2019-1-22_19-36-46.png?version=1&modificationDate=1548182206060&api=v2", None),
    ("04-zeichen-abfallen-mit-spiel.png",
     f"{BASE4}/image2019-1-22_19-37-23.png?version=1&modificationDate=1548182242803&api=v2", None),
    ("04-abfallen-1.png",
     f"{BASE4}/3_Grafiken_Abfallen-Aufmarschieren-02.png?version=2&modificationDate=1622117945903&api=v2", None),
    ("04-abfallen-2.png",
     f"{BASE4}/3_Grafiken_Abfallen-Aufmarschieren-03.png?version=2&modificationDate=1622117947480&api=v2", None),
    ("04-abfallen-3.png",
     f"{BASE4}/3_Grafiken_Abfallen-Aufmarschieren-04.png?version=2&modificationDate=1622117948137&api=v2", None),
    ("04-aufmarschieren-1.png",
     f"{BASE4}/3_Grafiken_Abfallen-Aufmarschieren-05.png?version=2&modificationDate=1622117948980&api=v2", None),
    ("04-aufmarschieren-2.png",
     f"{BASE4}/image-2025-1-29_12-11-20.png?version=1&modificationDate=1738149770910&api=v2", None),
    ("04-aufmarschieren-3.png",
     f"{BASE4}/3_Grafiken_Abfallen-Aufmarschieren-07.png?version=2&modificationDate=1622117949730&api=v2", None),
    ("04-aufmarschieren-4.png",
     f"{BASE4}/3_Grafiken_Abfallen-Aufmarschieren-08.png?version=2&modificationDate=1622117949963&api=v2", None),

    # Kapitel 5 - Grosse Wende (Vollaufloesung, sonst Thumbnail)
    ("05-ausgangsformation.png",
     f"{BASE5}/image2019-5-9_8-24-56.png?version=1&modificationDate=1557383096597&api=v2",
     f"{BASE5T}/image2019-5-9_8-24-56.png?version=1&modificationDate=1557383096597&api=v2"),
    ("05-stabfuehrer-wendet.png",
     f"{BASE5}/image2019-5-9_8-29-35.png?version=1&modificationDate=1557383375603&api=v2",
     f"{BASE5T}/image2019-5-9_8-29-35.png?version=1&modificationDate=1557383375603&api=v2"),
    ("05-marketenderinnen.png",
     f"{BASE5}/image2019-5-9_8-30-57.png?version=1&modificationDate=1557383457753&api=v2",
     f"{BASE5T}/image2019-5-9_8-30-57.png?version=1&modificationDate=1557383457753&api=v2"),
    ("05-erste-linie.png",
     f"{BASE5}/image2019-5-9_8-32-14.png?version=1&modificationDate=1557383534197&api=v2",
     f"{BASE5T}/image2019-5-9_8-32-14.png?version=1&modificationDate=1557383534197&api=v2"),
    ("05-abschluss.png",
     f"{BASE5}/image2019-5-9_8-33-4.png?version=1&modificationDate=1557383585007&api=v2",
     f"{BASE5T}/image2019-5-9_8-33-4.png?version=1&modificationDate=1557383585007&api=v2"),

    # Kapitel 6 - Schwenkung
    ("06-zeichen-rechts.png",
     f"{BASE6}/image2019-1-22_19-28-15.png?version=1&modificationDate=1548181695163&api=v2", None),
    ("06-zeichen-links.jpg",
     f"{BASE6}/Abb63.jpg?version=1&modificationDate=1551762056433&api=v2", None),
    ("06-vorstossen.png",
     f"{BASE6}/image2019-1-22_19-32-25.png?version=1&modificationDate=1548181944870&api=v2", None),
    ("06-schwenkung-1.png",
     f"{BASE6}/4_Schwenkung%20der%20Musikkapelle_Var1_Zeichenfl%C3%A4che%201.png?version=8&modificationDate=1742116111220&api=v2", None),
    ("06-schwenkung-2.png",
     f"{BASE6}/4_Schwenkung%20der%20Musikkapelle_Var1-02.png?version=3&modificationDate=1742116123567&api=v2", None),
    ("06-schwenkung-3.png",
     f"{BASE6}/4_Schwenkung%20der%20Musikkapelle_Var1-03.png?version=5&modificationDate=1742116135647&api=v2", None),
]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def hole(url, ziel, ctx):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as antwort:
        daten = antwort.read()
    if len(daten) < 500:
        raise ValueError(f"Antwort verdaechtig klein ({len(daten)} Bytes)")
    ziel.write_bytes(daten)
    return len(daten)


def main():
    force = "--force" in sys.argv

    ordner = Path(__file__).resolve().parent
    img = ordner / "img"
    img.mkdir(exist_ok=True)

    print(f"Zielordner: {img}")
    print(f"{len(IMAGES)} Grafiken\n")

    # Falls die Firma/Uni ein eigenes Zertifikat einsetzt und SSL zickt:
    ctx = ssl.create_default_context()

    ok = 0
    fehler = []

    for name, url, fallback in IMAGES:
        ziel = img / name

        if ziel.exists() and not force:
            print(f"  ueberspringe  {name}  (schon da)")
            ok += 1
            continue

        try:
            groesse = hole(url, ziel, ctx)
            print(f"  OK            {name}  ({groesse // 1024} KB)")
            ok += 1
            continue
        except Exception as e:
            erster_fehler = e

        if fallback:
            try:
                groesse = hole(fallback, ziel, ctx)
                print(f"  OK            {name}  ({groesse // 1024} KB, Thumbnail)")
                ok += 1
                continue
            except Exception as e:
                erster_fehler = e

        print(f"  FEHLER        {name}  -> {erster_fehler}")
        fehler.append(name)

    print()
    print(f"Fertig: {ok} von {len(IMAGES)} Grafiken in {img}")

    if fehler:
        print("\nNicht geladen:")
        for f in fehler:
            print(f"  {f}")
        print("\nTipp: Pruefe, ob die Datei im OeBV-Wiki noch unter derselben")
        print("Adresse liegt. Bei Zertifikatsfehlern hilft oft ein anderes Netz.")
        return 1

    print("Alle Grafiken vorhanden. Die Markdown-Dateien finden sie unter img/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
