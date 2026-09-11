# MuWeave homepage work

Die erste statische Umsetzung und ihre internen Grenzen sind in
[ARCHITECTURE.md](ARCHITECTURE.md) beschrieben. Hier stehen die verbleibenden
Arbeiten; der Erstellungsweg für Lehrpersonen ist in
[OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) als Produktentscheidung erfasst.

## Produktfunktionen des Zielbilds

Diese Abhängigkeiten gehören zur weiteren Produktentwicklung in
`software/Python/ggpackages/muweave-suite/` und den jeweiligen Backends.
Die aktuelle Homepage beschreibt sie wie vereinbart bereits im Präsens.

- [ ] Den KI-Lerncoach mit echter Modellanbindung in die Worksheet-Bedienung
  integrieren.
- [ ] Bei jeder Anfrage die wesentlichen fachlichen Inhalte des zur
  HTML-Publikation passenden KI-Kontexts und die autorenseitigen
  vorbereitenden Anweisungen übermitteln; deren Trennung von Lernendenbeiträgen
  und Gesprächsverlauf erhalten.
- [ ] Die didaktischen Vorgaben für Hinweise, Niveau, Sprache und Umgang mit
  Lösungen über mehrere aufeinanderfolgende Anfragen praktisch prüfen.
- [ ] Den nativen MathML-Ausgabeweg über die Abdeckung des gezeigten Beispiels
  hinaus vervollständigen, einschliesslich weiterer Beschriftungen und
  Interaktionen.

## Prüfung mit Menschen und weiteren Hilfsmitteln

- [ ] Die Homepage und die Formelvorlesung mit realen Screenreadern in Deutsch,
  Englisch und Französisch prüfen; Browser-/Screenreader-Kombinationen und
  tatsächlich getestete mathematische Strukturen festhalten.
- [ ] Weitere mathematische Beispiele mit Brüchen, Wurzeln, Indizes, Vektoren
  und Matrizen in diese Nutzungsprüfung aufnehmen. Die PDF-Zugänglichkeit
  gesondert beurteilen.
- [ ] Eine Lehrperson nach dem ersten Lesen erklären lassen, was MuWeave ist,
  welche Ausgaben entstehen und wie der Lerncoach pädagogisch gesteuert wird.

## Gemeinsames Symbol in Worksheets

- [ ] Das kanonische Website-SVG in einem eigenen PyHTML-Paketauftrag als
  synchronisierte Ressource übernehmen und das Favicon in eigenständige
  HTML-Worksheets einbetten.
- [ ] Offlineöffnung und gespeicherte Worksheet-Kopien mit dem gemeinsamen
  Browser-Icon prüfen; der Tabtitel bleibt der Dokumenttitel.
