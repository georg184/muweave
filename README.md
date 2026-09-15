# µWeave homepage

Die öffentliche Webseite erklärt µWeave für Lehrpersonen: eine Python-basierte
Dokumentenbeschreibungssprache für Worksheets, mit einer gemeinsamen Quelle
für PDF, interaktives HTML und fachlichen KI-Kontext.

Die Hauptseite ist auf Deutsch, Englisch und Französisch verfügbar. Sie führt
vom unmittelbaren Einstieg über Python, Lerncoach und vorlesbare Mathematik zu
einem echten Unterrichtsbeispiel. Der verlinkte Begriff
«Dokumentenbeschreibungssprache» führt zu einer allgemein verständlichen
Erklärseite mit Markdown- und LaTeX-Beispielen sowie einem kleinen
µWeave-Beispiel. Die Homepage verwendet eine neutrale Ansprache.
Technische Dokumentation ist
über einen Nebenlink im Fussbereich erreichbar.

Im Abschnitt «Mathematik auch hören» startet «Formel vorlesen» die Sprachausgabe;
derselbe Knopf stoppt sie wieder. Die gewählte Seitensprache bestimmt den
automatisch aus der Formel erzeugten Sprechtext und die verwendete
Browserstimme. Fehlt eine passende Stimme oder schlägt sie fehl, übernimmt ein
mitgeliefertes Hörbeispiel aus demselben Sprechtext. Ohne JavaScript bleiben
Sprechtext und native MathML-Formel lesbar.

Der Einstieg kennzeichnet die gesamte µWeave-Suite und ihre eigenen
Bibliotheksabhängigkeiten sichtbar als Open Source unter GPLv3
(`GPL-3.0-only`). Der verlinkte Lizenzabschnitt erläutert die Rechte an der
Software, die eigenständige Lizenzierung von Worksheet-Inhalten und die
unveränderten Drittanbieter-Lizenzen. Der vollständige GPL-Text ist lokal
verfügbar. Name und Logo werden mit dem Rechtevorbehalt von Georg G ausgewiesen;
die Logo-Grafik gehört nicht zur GPL-Freigabe der Software.

- Website: <https://georg184.github.io/muweave/>
- Eigenständiges Repository: <https://github.com/georg184/muweave>
- Lokaler Projektort: `software/HTML/ggprojects/muweave/`

## Beispiel und Produktstand

Das Unterrichtsbeispiel zeigt das Applet aus Item 116: Geschwindigkeit,
vorzeichenbehaftete Fläche und Ortsänderung. Auswahl und Regler sind direkt
auf der Homepage bedienbar. Darunter steht der vollständige passende Quelltext
mit Download. Die einleitenden und nachfolgenden Texte des Items sind weggelassen.

`examples/116.muweave` ist eine feste Kopie des deutschen Applet-Quelltexts;
`116-en.muweave` und `116-fr.muweave` enthalten seine übersetzten Beschriftungen.
Die Homepage verwendet daraus erzeugte lokale HTML-Kopien. Änderungen am
kanonischen Item 116 verändern diese Quellen und die Homepage nicht automatisch.

Der Lerncoach-Abschnitt zeigt unter dem Erklärungstext einen unveränderten
Screenshot aus einem deutschsprachigen HTML-Worksheet zur Geschwindigkeit.
`assets/images/Lerncoach_Beispiel.png` nimmt die volle Inhaltsbreite ein und
lässt sich per Klick in Originalgrösse öffnen. Alle Sprachfassungen verwenden
dasselbe Bild mit übersetzter Beschreibung und Bildunterschrift.

Eine Prüfung mit realen Screenreadern und die Übernahme des
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
