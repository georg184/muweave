# MuWeave: Seitenkonzept, Gestaltung und Textentwurf

Audience: Website-Verantwortliche, Redaktion und umsetzende Entwickler.

Der Entwurf übersetzt den Auftrag in eine konkrete erste Homepage. Die
verbindlichen ausgewählten Bedingungen stehen in [REQUIREMENTS.md](../REQUIREMENTS.md),
die noch auszuführenden Arbeiten in [TODO.md](../TODO.md) und offene
Entscheidungen in [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md). Die redaktionelle Grundlage bleibt hier; die bereits umgesetzte technische
Struktur ist in der Projektarchitektur beschrieben.

Die Seitentexte beschreiben auf Wunsch des Auftraggebers das vereinbarte
Produktziel im Präsens: integrierter KI-Lerncoach und vorlesbare Mathematik
auf Basis von nativem MathML. Der interne Abschnitt «Zielbild und
Implementierungsgrundlage» und die Aufgabenliste unterscheiden dieses
Zielbild vom bereits implementierten Stand. Die Logoidee des verwobenen µ
ist als gestalterische Richtung angenommen.

## Ziel und Begriff

Eine Lehrperson soll durch Lesen des Seitenanfangs verstehen, was MuWeave
ist, was sie damit erstellen kann und weshalb Python und KI dazugehören.
Das Design unterstützt diese Erklärung mit guter Typografie, eindeutiger
Reihenfolge und einem anschliessenden echten Beispiel.

Die passende öffentliche Bezeichnung ist **Python-basierte Dokumentensprache**.
`.muweave` bezeichnet das zugehörige textuelle Quellformat. «Dokumentenformat»
ist als erste Annäherung verständlich, erklärt aber die ausführbaren
Ausdrücke, Funktionen und wiederverwendbaren Inhalte nicht vollständig.

Auf der Webseite steht MuWeave für das Gesamtsystem zur Dokumenterstellung.
Technisch ist der gleichnamige Kern ein formatneutraler Python-Makroprozessor;
die Suite ergänzt ihn um Unterrichtsvokabular und Ausgabewege. Diese
Paketaufteilung gehört in den Entwicklerbereich.

Der zentrale Gedanke wird auf Deutsch **Eine Quelle. Mehrere Ausgaben.**
genannt. «Single source, multiple outputs» ist die englische Entsprechung.
Eine gemeinsame Quelle trägt Inhalte, Mathematik, Aufgaben, Lösungen und
Interaktionsbeschreibungen. Die Ausgabe passt sich ihrem Medium an: Die
Druckfassung zeigt beispielsweise feste Werte und einen Verweis zur
interaktiven Fassung; im Browser werden die Werte veränderbar.

Das AI-Backend ist ein zentraler Teil dieser Ausrichtung. Es bereitet den
fachlichen Inhalt für den direkt integrierten Lerncoach auf. Bei jeder
Anfrage erhält der Coach die wesentlichen Inhalte in KI-gerechter Form sowie
die vom Autor festgelegten vorbereitenden Anweisungen (Pre-Prompt). Die
Lehrperson kann damit die Art der Hilfestellung und den didaktischen Rahmen
vorgeben. Die KI-gestützte Erstellung des Materials und die Begleitung der
Lernenden im fertigen Worksheet werden beide ausdrücklich erläutert.

Der zentrale konkrete Nutzen von Barrierefreiheit ist hier, dass ein
Screenreader auch mathematische Formeln vorlesen kann. Das technische Ziel
ist natives MathML im HTML-Worksheet. Die Homepage erklärt zuerst diesen
Nutzen; Detailfragen der Rendering-Technik gehören in den Entwicklerbereich.

## Reihenfolge der Hauptseite

| Position | Sichtbarer Inhalt | Aufgabe |
| --- | --- | --- |
| Seitenkopf | MuWeave mit kleinem Zeichen; rechts Sprachwahl | Produktname und Sprache sofort erkennen |
| Direkt darunter | Leitsatz in wenigen gut lesbaren Zeilen | Ziel und Nutzen benennen |
| Ohne Unterbrechung | Kurze Erklärung der Dokumentensprache und Worksheets mit Lerncoach | «Was ist das?» beantworten |
| Anschliessend | Eine Quelle → PDF, interaktives HTML, KI-Kontext für den Lerncoach | Das Ausgabeprinzip sichtbar machen |
| Nächster Abschnitt | Python als Teil des Dokuments | Mächtigkeit und KI-gestützte Erstellung erklären |
| Direkt danach | Der integrierte Lerncoach: Kontext bei jeder Anfrage und Autoren-Pre-Prompt | Das pädagogische Kernfeature erklären |
| Anschliessend | Mathematik auch hören | Vorlesbare Formeln mit nativem MathML konkret machen |
| Danach | Ein Unterrichtsbeispiel mit seinen Ausgaben | Die Erklärung an echtem Material zeigen |
| Abschluss | Ein konkreter Einstieg für Lehrpersonen | Den nächsten tatsächlich verfügbaren Schritt anbieten |
| Fussbereich | Dokumentation für Entwickler; Projekt auf GitHub | Sekundäre Zugänge bereitstellen |

Der Kopf enthält zunächst keine zusätzliche Navigationsleiste. Spätere
Sprunglinks zu Beispielen und Einstieg sind erst sinnvoll, wenn die Seite
entsprechend wächst. Der grundsätzliche Zusammenhang wird im Fliesstext
erklärt und bleibt beim Scrollen zusammenhängend lesbar.

Schematischer Aufbau:

```text
┌───────────────────────────────────────────────────────────┐
│  [µ-Zeichen] MuWeave                         [DE] [EN] [FR] │
│                                                           │
│  Leitsatz                                                 │
│  Was MuWeave ist: kurze Erklärung                         │
│                                                           │
│                    eine .muweave-Quelle                    │
│                    /        |        \                    │
│                  PDF    Worksheet    KI-Kontext           │
│                           └── Lerncoach ←───┘              │
├───────────────────────────────────────────────────────────┤
│  Python als Teil des Dokuments                            │
│  Kurzer Text; bei Bedarf ein kleines erläuterndes Beispiel │
├───────────────────────────────────────────────────────────┤
│  Lerncoach: Kontext bei jeder Anfrage · Autoren-Pre-Prompt │
│  Mathematik auch hören: native MathML-Formeln               │
├───────────────────────────────────────────────────────────┤
│  Ein Unterrichtsbeispiel                                   │
│  Sichtbare Vorschau · HTML öffnen · PDF ansehen            │
├───────────────────────────────────────────────────────────┤
│  Einstieg                                                 │
│  Dokumentation für Entwickler · GitHub                     │
└───────────────────────────────────────────────────────────┘
```

Die Buchstaben im Schema stehen für die vorhandenen Flaggenbuttons.
Das Ausgabeschema wird als semantisches HTML mit einer klaren Lesereihenfolge
gebaut und auf schmalen Bildschirmen vertikal angeordnet. Es braucht keine
Animation. Der sichtbare Erklärungstext vermittelt denselben Zusammenhang.

## Textentwürfe in den drei Sprachen

Die folgenden Texte sind redaktionelle Arbeitsfassungen für dieselben
Abschnitte. Der Produktname bleibt überall **MuWeave**. Deutsche Texte folgen
schweizerischer Rechtschreibung. «Worksheets» bleibt im deutschen Leitsatz
erhalten und wird im Erklärungstext als «Arbeitsblätter» verständlich gemacht.

### Deutsch

**Leitsatz**

> KI-gestützte Erstellung interaktiver, barrierefreier Worksheets und
> Prüfungen – mit einheitlicher Gestaltung und nativ integriertem
> KI-Lerncoach.

**Was ist MuWeave?**

MuWeave ist eine Python-basierte Dokumentensprache für Unterrichtsmaterialien.
In einer `.muweave`-Datei beschreibst du Texte, Formeln, Aufgaben, Lösungen
und interaktive Elemente. Daraus entstehen druckfertige PDFs, interaktive
Arbeitsblätter mit integriertem KI-Lerncoach und strukturierte Inhalte für
KI-Modelle. Du pflegst eine gemeinsame Quelle für diese Ausgaben.

**Eine Quelle. Mehrere Ausgaben.**

Die Druckfassung eignet sich für Papier und Prüfungen. Im Browser können
Lernende interaktive Elemente bedienen und vorgesehene Antwortfelder nutzen.
Der Lerncoach unterstützt sie dabei direkt im Worksheet. Die KI-Fassung
liefert ihm den fachlichen Inhalt und seine Zusammenhänge bei jeder Anfrage.
Jede Ausgabe nutzt die Möglichkeiten ihres Mediums und folgt einer
gemeinsamen Gestaltung.

**Python als Teil des Dokuments**

Python steht direkt im MuWeave-Quelltext zur Verfügung. Damit lassen sich
Werte berechnen, Aufgaben variieren und Inhalte wiederverwenden. Auch
interaktive Darstellungen können so beschrieben werden. Diese
Ausdrucksmöglichkeiten machen MuWeave zu einem Werkzeug für anspruchsvolles
Unterrichtsmaterial. KI-Modelle können beim Schreiben und Anpassen ihre
Fähigkeiten zur Python-Programmierung einsetzen.

Von Hand ist MuWeave anders zu lesen als LaTeX, aber nicht grundsätzlich
schwieriger. Markdown bleibt für einfache Texte unmittelbarer. Im Zentrum
von MuWeave steht die Ausdruckskraft für Inhalt, Berechnung und Interaktion.

**Ein Lerncoach, der das Unterrichtsmaterial kennt**

Der KI-Lerncoach begleitet Lernende direkt im Worksheet. Bei jeder Anfrage
erhält er die wesentlichen fachlichen Inhalte in einer für KI aufbereiteten
Form: Aufgaben, Formeln, Begriffe und ihre Zusammenhänge. So kann er seine
Hilfestellung auf das Unterrichtsmaterial beziehen.

Als Autor legst du in vorbereitenden Anweisungen, dem Pre-Prompt, fest, wie
der Coach unterstützen soll. Dazu gehören etwa das sprachliche Niveau,
die Art der Hinweise und der Umgang mit Lösungen. Diese Vorgaben werden
bei jeder Anfrage ebenfalls mitgegeben. Du kannst beispielsweise vorgeben:

> Gib zunächst einen Hinweis und verwende die Begriffe des Worksheets.
> Frage nach dem bisherigen Ansatz, bevor du den nächsten Lösungsschritt
> erläuterst.

**Mathematik auch hören**

Screenreader können neben dem Text auch die mathematischen Formeln vorlesen.
Dafür enthält das Worksheet die Formeln als natives MathML. Brüche, Wurzeln,
Indizes und weitere mathematische Strukturen bleiben so für die
Vorlesefunktion zugänglich.

### English

**Tagline**

> AI-assisted creation of interactive, accessible worksheets and exams –
> with a consistent look and feel and a natively integrated AI learning coach.

**What is MuWeave?**

MuWeave is a Python-based document language for teaching materials. In a
`.muweave` file, you describe text, formulas, tasks, solutions and interactive
elements. The same source produces print-ready PDFs, interactive worksheets
with an integrated AI learning coach and structured content for AI models.
You maintain one common source for these outputs.

**One source. Multiple outputs.**

The print version is designed for paper and exams. In the browser, learners
can use interactive elements and designated answer fields, with help from
the learning coach directly in the worksheet. The AI version supplies the
subject matter and its relationships to the coach with every prompt. Each
output uses the possibilities of its medium and follows a shared visual design.

**Python as part of the document**

Python is available directly in MuWeave source. It lets you calculate values,
create variations of tasks and reuse content. It can also describe interactive
visualisations. This expressive power makes MuWeave a tool for demanding
teaching materials. AI models can use their Python programming capabilities
to help write and adapt those materials.

Reading MuWeave source differs from reading LaTeX, but is not inherently
harder. Markdown remains more immediate for simple text. MuWeave focuses on
the expressive power needed for content, computation and interaction.

**A learning coach that knows the teaching material**

The AI learning coach supports learners directly in the worksheet. With every
prompt, it receives the essential subject content in a form prepared for AI:
tasks, formulas, concepts and their relationships. This lets it relate its
guidance to the teaching material.

As the author, you define preliminary instructions, or a pre-prompt, to guide
how the coach helps. These can cover language level, the kinds of hints it
provides and how it handles solutions. Those instructions accompany every
prompt as well. For example, you can specify:

> Start with a hint and use the worksheet's terminology. Ask about the
> learner's approach before explaining the next step towards the solution.

**Hear the mathematics, too**

Screen readers can read mathematical formulas aloud alongside the text.
The worksheet includes formulas as native MathML, preserving fractions,
roots, indices and other mathematical structures for spoken presentation.

### Français

**Phrase directrice**

> Création assistée par l'IA de fiches de travail et d'épreuves interactives
> et accessibles, avec une présentation cohérente et un coach pédagogique IA
> intégré nativement.

**Qu'est-ce que MuWeave ?**

MuWeave est un langage de documents fondé sur Python, destiné aux supports
pédagogiques. Dans un fichier `.muweave`, vous décrivez les textes, les
formules, les exercices, les solutions et les éléments interactifs. Cette
même source produit des PDF prêts à imprimer, des fiches interactives pour
le navigateur avec un coach pédagogique IA intégré et des contenus structurés
pour les modèles d'IA. Vous maintenez une source commune pour ces différentes
sorties.

**Une source. Plusieurs formats de sortie.**

La version imprimée est conçue pour le papier et les épreuves. Dans le
navigateur, les élèves peuvent manipuler les éléments interactifs et utiliser
les espaces de réponse prévus, avec l'aide du coach directement dans la
fiche. La version destinée à l'IA lui fournit le contenu disciplinaire et
ses relations à chaque demande. Chaque sortie exploite les possibilités
de son support et suit une présentation commune.

**Python au cœur du document**

Python est directement disponible dans le texte source MuWeave. Il permet
de calculer des valeurs, de créer des variantes d'exercices et de réutiliser
des contenus. Il permet aussi de décrire des représentations interactives.
Cette richesse d'expression fait de MuWeave un outil pour des supports
pédagogiques élaborés. Les modèles d'IA peuvent mobiliser leurs capacités
de programmation en Python pour aider à rédiger et à adapter ces supports.

La lecture du texte source MuWeave diffère de celle de LaTeX, sans être
fondamentalement plus difficile. Markdown reste plus immédiat pour les textes
simples. MuWeave privilégie la richesse d'expression nécessaire au contenu,
au calcul et à l'interactivité.

**Un coach qui connaît le support pédagogique**

Le coach pédagogique IA accompagne les élèves directement dans la fiche.
À chaque demande, il reçoit les contenus disciplinaires essentiels sous
une forme adaptée à l'IA : exercices, formules, notions et relations entre
ces éléments. Il peut ainsi relier son aide au support pédagogique.

En tant qu'auteur, vous définissez des consignes préalables, ou pré-prompt,
qui orientent son accompagnement : niveau de langue, nature des indices
et manière d'aborder les solutions, par exemple. Ces consignes sont elles
aussi transmises à chaque demande. Vous pouvez notamment préciser :

> Commence par un indice et utilise les termes de la fiche. Demande à
> l'élève quelle démarche il a suivie avant d'expliquer l'étape suivante.

**Écouter aussi les mathématiques**

Les lecteurs d'écran peuvent lire à voix haute les formules mathématiques
en plus du texte. La fiche contient les formules en MathML natif, ce qui
préserve les fractions, les racines, les indices et les autres structures
mathématiques pour la lecture vocale.

## Visuelle Richtung

Die Seite soll an eine sorgfältig gestaltete Publikation erinnern: hell,
ruhig und präzise. Ein warmer fast weisser Hintergrund (`#F7F8F5`), dunkle
Schrift (`#173038`) und ein gedämpfter Petrolton (`#086F6B`) bilden den
Ausgangspunkt. Weisse Beispieloberflächen und feine Trennlinien strukturieren
die längere Seite. Die endgültigen Farbpaarungen werden auf Kontrast geprüft.

Eine gut lesbare Sans-Serif-Schrift aus einem lokalen Systemfont-Stack hält
den Einstieg schnell und unabhängig von externen Schriftanbietern. Der Titel
erhält eine klare, grosszügige Schriftgrösse, der Fliesstext etwa 18 px bei
einem Zeilenabstand von 1.6 und einer Zeilenlänge um 65 Zeichen. Abstände
machen die Gedankenfolge sichtbar; der Einleitungsteil erhält keine feste
bildschirmfüllende Höhe.

Auf einem üblichen Desktopbildschirm sollen Titel, Leitsatz, Definition und
die kompakte Ausgabeübersicht zusammen sichtbar sein. Mobil folgt derselbe
Inhalt in derselben Reihenfolge untereinander. Die Erklärung darf weder durch
die Sprachwahl verdeckt noch für eine dekorative Fläche nach unten verdrängt
werden. Farben dienen als Akzente; Links und Zustände erhalten auch eine
erkennbare Form, Beschriftung oder Unterstreichung.

Ein repräsentatives Beispiel zeigt einen kleinen Ausschnitt aus einem echten
Worksheet. Der Entwurf sieht zunächst ein Beispiel aus der Kinematik vor,
etwa eine veränderbare Sekante oder einen Zusammenhang zwischen Orts- und
Geschwindigkeitsdiagramm. HTML und PDF stammen aus derselben kanonischen
Quelle. Ein sichtbarer Kurztext erklärt, was ausprobiert werden kann; die
vollständigen Ausgaben sind direkt erreichbar. Umfangreiche interaktive
Ressourcen werden erst bei Bedarf geladen.

An demselben Beispiel wird auch der Lerncoach gezeigt: eine fachliche Frage,
der zugehörige Kontext und eine zu den Autorenanweisungen passende
Hilfestellung. Ein kurzes Vorlesebeispiel macht die Mathematik-Zugänglichkeit
erfahrbar. Das Beispiel soll diese zusammengehörenden Möglichkeiten an einem
Unterrichtsinhalt zeigen; die Einleitung bleibt dabei kurz. Ein gestalterischer
Entwurf des Coach-Fensters wird intern als Entwurf behandelt, bis eine reale
Integration vorgeführt werden kann.

## Sprachumschalter

Die Referenz ist die existierende Umsetzung in `ggprojects/motion`:

- `index.html`: `languageSwitcher`, drei native Buttons, `aria-pressed`,
  Sprachnamen als `aria-label` und `title`; Flaggen sind dekorativ.
- `css/styles.css`: `.language-switcher` als helle abgerundete Gruppe,
  nebeneinanderliegende Flaggenbuttons und hinterlegte aktive Auswahl.
- `js/app.js`: `storedLanguage`, `applyLanguage`, Pflege von `lang`,
  Seitentitel und Auswahlzustand; robuste Sitzungsspeicherung.
- `README.md`, Abschnitt «Language Maintenance»: gemeinsamer Sprachzustand
  und vollständige Pflege von Deutsch, Englisch und Französisch.

Die Homepage übernimmt das Muster mit 🇩🇪, 🇬🇧 und 🇫🇷. Die Gruppe sitzt rechts
oben innerhalb des Seitenkopfs. Bei schmaler Ansicht bleibt sie im normalen
Layout und verdeckt keinen Inhalt. Die Trefferflächen werden für diese
Seite mit mindestens 44 px geplant. Tastaturfokus und aktive Sprache bleiben
auch ohne Farberkennung unterscheidbar. Die Bedienelemente behalten ihre
Sprachnamen, falls das System Flaggen nur als Buchstabencodes darstellt.

Für vollständige statische und verlinkbare Sprachfassungen ist vorgesehen:

- `/` als deutscher Einstieg; `en/` und `fr/` als direkt erreichbare Seiten.
- Eine gemeinsame Vorlage und drei Inhaltsdateien erzeugen diese Seiten.
- Eine explizite Sprach-URL gewinnt vor einer gespeicherten Auswahl. Nur der
  Einstieg ohne ausdrückliche Sprachwahl darf die Sitzungsauswahl übernehmen.
- Die deutschen Sprachverweise können mit `?lang=de` eine ausdrückliche
  Rückkehr zur deutschen Rootseite kenntlich machen. Ohne Sitzung oder gültige
  Auswahl ist Deutsch der Ausgangspunkt.
- Die Flaggenbuttons führen zur entsprechenden Sprachseite und erhalten
  vorhandene Abschnittsanker. Die Auswahl wird wie in `motion` sitzungsweise
  gespeichert. Ein Speicherfehler unterbindet die Navigation nicht.
- Ohne JavaScript bleiben die vollständigen HTML-Inhalte und gewöhnliche
  Sprachverweise in einem `noscript`-Bereich verfügbar.
- Seitentitel, Beschreibung, `lang`, Alternativtexte und zugängliche Namen
  gehören zur jeweiligen Sprachfassung; Sprachalternativen bekommen
  passende `hreflang`-Verweise.

Die Sprachen werden gemeinsam ausgeliefert. Der Inhalt der Sprachfassungen
wird aus einem gemeinsamen Satz semantischer Textschlüssel erzeugt; es gibt
keine drei unabhängig gepflegten Seitenlayouts.

## Logo und Favicon

Gewählt ist ein vereinfachtes **µ aus zwei ineinandergreifenden
Bändern**. Der Bezug auf «Weave» bleibt im Zeichen selbst sichtbar. Die
Wortmarke daneben lautet MuWeave. Das reine Zeichen soll ohne Wortmarke als
Favicon funktionieren und auch einfarbig erkennbar bleiben.

Der Entwurf beginnt als SVG. Die Form wird zuerst bei 16 px und 32 px
beurteilt, danach als grössere Wortmarke. Feine Details, kleine Beschriftungen
und notwendige Farbverläufe würden die Erkennbarkeit im Browser-Tab schwächen.
Aus dem festgelegten Master entstehen ein SVG-Favicon und nötige
Raster-/ICO-Ableitungen. Die Reinzeichnung konkretisiert die angenommene
Logoidee und prüft sie in diesen Grössen.

Die kanonische Markengrafik liegt im Homepageprojekt unter `assets/brand/`.
PyHTML erhält später eine nachvollziehbar synchronisierte Paketressource
mit Herkunft und Prüfsumme. Die eigenständigen Worksheets betten das Symbol
ein, damit es ohne Verbindung zur Homepage verfügbar ist. Gespeicherte
Worksheet-Kopien behalten es. Der Tabtitel bleibt der jeweilige Dokumenttitel.
Das ist eine spätere, eigene PyHTML-Änderung mit Paketprüfung und Versionierung.

## Zielbild und Implementierungsgrundlage

### KI-gestützte Erstellung und Python

Die direkte Verwendung von Python ist im MuWeave-Kern dokumentiert. Der
Autorenleitfaden beschreibt den Arbeitsablauf für KI-Agenten. Das erlaubt
die konkrete Aussage, dass KI-Modelle ihre Python-Fähigkeiten beim Erstellen
von MuWeave-Quellen nutzen können.

Die Forschung [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)
belegt Python-Codegenerierung an konkreten Modellen und Aufgaben. Daraus
folgt keine pauschale Rangfolge zwischen allen Sprachen und Modellen. Der
Textentwurf formuliert deshalb die nutzbare Verbindung zu Python. Der
Lesbarkeitsvergleich mit LaTeX und Markdown ist eine redaktionelle Einordnung,
keine gemessene Eigenschaft.

### Integrierter Lerncoach und AI-Backend

Der vereinbarte Funktionsumfang ist ein direkt im Worksheet bedienbarer
KI-Lerncoach. Jede Anfrage führt die wesentlichen fachlichen Inhalte in
KI-gerechter Form und die vorbereitenden Autorenanweisungen mit. Der
Pre-Prompt steuert unter anderem Hilfestrategie, Sprache, Anspruchsniveau
und Umgang mit Lösungen. Er ist ein bewusst verfasster Teil der pädagogischen
Vorgaben. Die genaue Autoren-API wird bei der Produktimplementierung festgelegt;
der Webseitenentwurf erfindet dafür keine MuWeave-Kommandos.

Das beabsichtigte Prinzip für jede Anfrage:

```text
Autorenanweisungen (Pre-Prompt)
  + wesentlicher fachlicher Kontext aus dem Worksheet-AI-Bundle
  + zugeordnete Lernendenbeiträge und relevanter Gesprächsverlauf
  + aktuelle Frage
  → KI-Lerncoach → Antwort im Worksheet
```

«Bei jeder Anfrage» bedeutet, dass der benötigte Kontext jeder Modellanfrage
zugänglich ist. Wie die wesentlichen Inhalte ausgewählt und innerhalb des
jeweiligen Kontextfensters übermittelt werden, bleibt eine Implementierungsfrage.
Die fachliche Quelle wird dafür nicht jedes Mal neu ausgeführt. Statischer
Autoreninhalt, Autorenanweisungen, Lernendenbeiträge und Coach-Nachrichten
behalten ihre getrennte Zuordnung.

Die direkte HTML-Ausgabe enthält standardmässig semantischen KI-Kontext aus
derselben einmaligen typisierten Expansion wie der sichtbare Inhalt. PyAI
stellt ausserdem eigenständige strukturierte JSON- und Markdown-Ausgaben
bereit. Diese implementierte Grundlage speist die noch zu ergänzende
Coach-Oberfläche, Modellanbindung, Zusammenstellung jeder Anfrage und
autorenseitige Pre-Prompt-Konfiguration. Die Seitentexte beschreiben bereits
das vereinbarte Gesamtergebnis; sie sind kein Implementierungsbericht.

Die fachliche Planung des Laufzeitkontexts liegt in der Suite. Das AI-Backend
bleibt Eigentümer der semantischen Inhaltsaufbereitung; die Worksheet-/Host-
Integration verbindet sie mit dem Coach. Auch bei einer Modellanbindung über
einen separaten Dienst bleibt die Bedienoberfläche unmittelbar im Worksheet.
Die statische Offlinefähigkeit des Arbeitsblatts bedeutet nicht automatisch,
dass der gewählte KI-Dienst ohne Netzverbindung verfügbar ist.

Der Umgang mit Lösungen folgt den gewählten Ausgabe- und Hilferegeln.
Pre-Prompts beschreiben die beabsichtigte pädagogische Unterstützung; eine
technisch durchgesetzte Lösungsfreigabe muss die spätere Integration gesondert
abbilden. Die Homepage behauptet keine neue automatische Benotung.

### Barrierefreiheit und gemeinsame Gestaltung

Im vereinbarten Zielbild bezieht sich das zentrale Versprechen auf vorlesbare
mathematische Formeln. Das HTML-Worksheet enthält dafür natives MathML, das
im Browser dargestellt wird und seine mathematische Struktur für unterstützte
Screenreader erhält. Der angestrebte Ausgabeweg benötigt zur Formeldarstellung
keine MathJax- oder KaTeX-Laufzeit auf dem Gerät der Lernenden.

Technische Einordnung: [MathML](https://www.w3.org/TR/mathml-core/) beschreibt
mathematische Notation und Struktur. MathJax und KaTeX sind Werkzeuge zur
Formeldarstellung; [MathJax bietet eigene Zugänglichkeitsfunktionen](https://docs.mathjax.org/en/latest/basic/accessibility.html),
und [KaTeX unterstützt auch MathML-Ausgabe](https://katex.org/docs/options).
Die Wahl des nativen MathML-Wegs ist die festgelegte technische Richtung und
keine Behauptung, diese anderen Werkzeuge könnten keine vorlesbaren Formeln
liefern.

Ein optionaler nativer MathML-Pfad existiert bereits in PyHTML. Die kanonische
Mathematikreferenz beschreibt seine Abdeckung und noch offene Grenzen;
MathJax ist derzeit weiterhin der Standard. Die vervollständigte native
Ausgabe und ihre Prüfung mit Screenreadern gehören zur noch offenen
Produktarbeit. Die Textentwürfe verwenden dafür das gewünschte Zielbild ohne
die bisherige Ausweichformulierung «Fokus auf Barrierefreiheit».

Die Homepage wird mit [WCAG 2.2, Stufe AA](https://www.w3.org/TR/WCAG22/)
als Prüfziel geplant. Dazu gehören unter anderem semantische Struktur,
Tastaturbedienbarkeit, sichtbarer Fokus, Kontrast, Vergrösserung und
Textalternativen. Automatische Prüfung und manuelle Nutzung ergänzen sich.

Die konkrete Vorlesefunktion wird mit Browser-/Screenreader-Kombinationen
und mathematischen Beispielen in Deutsch, Englisch und Französisch geprüft.
Dazu gehören Brüche, Wurzeln, Indizes, Vektoren, Matrizen und eingebettete
Formeln im Lesefluss. Das Vorhandensein eines MathML-Baums ersetzt diese
Nutzungsprüfung nicht. Die PDF-Struktur und die Zugänglichkeit weiterer
Bedienelemente sind eigene Prüfpunkte; das konkrete MathML-Versprechen ist
keine pauschale Konformitätsaussage über sämtliche Ausgaben.

«Einheitliche Gestaltung» meint gemeinsame Typografie, mathematische
Notation, Farben und didaktische Elemente mit Anpassungen an Bildschirm
und Papier. Es verspricht kein identisches Seitenlayout und keine
Interaktion auf Papier.

## Technische Umsetzung und Ablage

Die erste Umsetzung liegt als unabhängige statische Website unter
`ggprojects/muweave/`. Die implementierte Struktur und ihre Eigentumsgrenzen
stehen in [ARCHITECTURE.md](../ARCHITECTURE.md); Erzeugung, Ressourcenpflege,
Prüfungen und GitHub Pages in [DEVELOPMENT.md](../DEVELOPMENT.md).

Die redaktionellen Texte werden in `src/content/` gepflegt. Ein Inhalts-Hash
liefert den gemeinsamen Cacheversionstoken automatisch. Das Unterrichtsbeispiel
zur beschleunigten Bewegung besitzt echte PDF-, HTML- und KI-Exporte;
`developers/` enthält das aus den kanonischen Paketquellen erzeugte technische
Portal. Der Lerncoach-Dialog auf der Homepage ist eine gekennzeichnete
Illustration des vereinbarten Produktziels.

## Lokale fachliche Grundlagen

Die Pfade sind relativ zum gemeinsamen Verzeichnis `software/` angegeben;
sie dienen dem lokalen Nachschlagen und werden nicht als öffentliche Links
auf die Homepage übernommen.

| Thema | Kanonischer Einstieg |
| --- | --- |
| Dokumentensprache und Python | `Python/ggpackages/muweave/README.md`, `REQUIREMENTS.md` |
| Gesamtsystem und Autorenablauf | `Python/ggpackages/muweave-suite/docs/AGENT_AUTHORING.md` |
| Genaue Autorenoperationen | `Python/ggpackages/muvocab/docs/AUTHORING.md`, `AUTHOR_API.md` |
| Eigenständiges HTML und Bedienfunktionen | `Python/ggpackages/pyhtml/README.md` |
| KI-Kontext und Lerncoach-Grundlage | `Python/ggpackages/muweave-suite/docs/ai_export.rst` |
| Offene Laufzeitintegration | `Python/ggpackages/muweave-suite/TODO.md`, `OPEN_QUESTIONS.md` |
| Nativer MathML-Pfad und aktuelle Abdeckung | `Python/ggpackages/pyhtml/docs/MATHEMATICS.md` |
| Wiederverwendung und Veröffentlichung | `Python/ggpackages/muweave_library/README.md`, `DEVELOPMENT.md` |
| Sprachumschalter | `HTML/ggprojects/motion/index.html`, `css/styles.css`, `js/app.js`, `README.md` |
| Eigenständige Website und Auslieferung | `HTML/ggprojects/README.md`, `REQUIREMENTS.md`, `DEVELOPMENT.md` |

Die beiden Einführungen
`Python/ggpackages/muweave_documents/PROMPT-MUWEAVE-DEVELOPER.md` und
`PROMPT-MUWEAVE-DOCUMENT-AUTHOR.md` bilden die Arbeitsgrundlage für die
jeweilige Rolle; sie sind keine Inhalte für den öffentlichen Einstieg.
