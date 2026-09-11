# MuWeave homepage

Die öffentliche Webseite erklärt MuWeave für Lehrpersonen: eine Python-basierte
Dokumentensprache für Worksheets und Prüfungen, mit einer gemeinsamen Quelle
für PDF, interaktives HTML und fachlichen KI-Kontext.

Die Hauptseite ist auf Deutsch, Englisch und Französisch verfügbar. Sie führt
vom unmittelbaren Einstieg über Python, Lerncoach und vorlesbare Mathematik zu
einem echten Unterrichtsbeispiel. Technische Dokumentation ist über einen
Nebenlink im Fussbereich erreichbar.

- Website: <https://georg184.github.io/muweave/>
- Eigenständiges Repository: <https://github.com/georg184/muweave>
- Lokaler Projektort: `software/HTML/ggprojects/muweave/`

## Beispiel und Produktstand

`examples/motion.muweave` erzeugt in drei Sprachen ein Worksheet zur
beschleunigten Bewegung. Die veröffentlichten HTML-, PDF- und KI-Ausgaben
stammen aus dieser Quelle. Im HTML verändert ein echter MuWeave-Schieberegler
die Kurve; das PDF zeigt den Ausgangswert. Die HTML-Ausgaben enthalten natives
MathML und den zum Dokument passenden semantischen KI-Kontext.

Die Seitentexte beschreiben auf Wunsch des Auftraggebers das Produktziel im
Präsens. Die Laufzeitintegration des KI-Lerncoachs und seiner Autorenanweisungen
steht noch aus. Das Gespräch auf der Homepage ist eine beschriftete
Illustration. Eine Prüfung mit realen Screenreadern und die Übernahme des
Logos in sämtliche PyHTML-Worksheets bleiben ebenfalls offen.

Die Homepage benötigt zur Laufzeit weder einen Serverdienst noch externe
Schriften oder JavaScript-Bibliotheken. Die drei Sprachfassungen sind
vollständige statische Seiten und bleiben ohne JavaScript lesbar und verlinkt.

## Weiterführende Informationen

- [Lokale Erzeugung, Prüfungen und Veröffentlichung](DEVELOPMENT.md)
- [Implementierte Struktur und Eigentumsgrenzen](ARCHITECTURE.md)
- [Seitenkonzept und redaktionelle Grundlage](docs/WEBSITE_CONCEPT.md)
- [Überprüfbare Vorgaben](REQUIREMENTS.md)
- [Noch offene Arbeiten](TODO.md)

Die Dokumentensprache, ihre Backends und die kanonischen technischen
Dokumente verbleiben in `software/Python/ggpackages/`. Diese Webseite ist ein
eigenständiges HTML-Projekt und kein zusätzliches Python-Paket.
