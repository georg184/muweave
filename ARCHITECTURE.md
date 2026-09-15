# µWeave homepage architecture

## Static editions

`src/page.html` owns the homepage structure; `src/document-language.html`
owns the linked introduction to document description languages.
The introduction pairs Markdown and LaTeX source excerpts with labelled
illustrative appearances. Both code and previews use the same translated
heading and sentence; these are teaching illustrations, not compiler captures.
`src/content/de.json`, `en.json` and `fr.json` own equivalent editorial and
accessible text. The small
standard-library builder validates key parity and escapes every substituted
value, then produces both pages in all three languages. It checks translation
coverage across both templates while rejecting missing or unused text.
Relative links support both a local server and the `/muweave/` GitHub Pages
prefix.

The output overview uses a source card followed by a semantic list of three
outputs, each with an illustrative filename. Three independent SVG arrows
connect the source directly to the equal-height output cards. Each card
fits its content width within the available space; the left edges stay aligned.
CSS aligns the arrows with a horizontal layout on larger screens and separate
lanes on mobile. The arrows are decorative; all labels remain ordinary HTML text
in source-to-output reading order without CSS or JavaScript. The AI card
represents agent-readable content, illustrated by the Markdown output.
A straight vertical arrow starts at the midpoint of the AI card's top edge
and enters the HTML card's bottom edge. Its translated caption sits beside it
in the larger gap between these rows. Both follow the AI card's actual width;
CSS positions them without runtime geometry calculations.

`assets/js/site.js` handles language navigation, formula playback and mixed-version
detection. The flag buttons follow the existing `motion` presentation, with
native language names, pressed state and targets of at least 44 pixels.
Static language links remain available if JavaScript is disabled or fails to
load. An optional session preference is subordinate to explicit language URLs
and history restoration. The build supplies page-specific language links, so
switching stays on the current topic. Explicit flag activation clears a stale
section fragment and carries the current viewport through a one-use session
record bound to the destination URL. The destination restores it on `pageshow`;
reload and back/forward navigation retain the browser's normal restoration.
Direct section links, including implicit language redirects, still use their
anchors. The explanation's
return links select its matching homepage edition explicitly.

## Version coherence

The builder hashes published source inputs, assets, resources and its own code
to derive one version token. The three entry documents, CSS and JavaScript
share it; local entry asset URLs carry it. Startup compares the document,
JavaScript and CSS tokens and displays a localized reload message on mismatch.
A content hash avoids a forgotten manual timestamp bump. There is no service
worker and no external font or runtime dependency on the teacher homepage.

## Brand and mathematics

`muvocab/src/muvocab/_brand/muweave-symbol.svg` owns the canonical interwoven µ.
The website retains its exact copy in `assets/brand/muweave-symbol.svg`. Its crossing
gap is transparent so the mark works on both the page background and white
cards. Playwright renders it for Pillow's raster favicon conversions.
`resources/brand.json` retains the real bare `µweave` HTML expansion. After
escaping translations, the static builder inserts it into prose text nodes,
including the larger header wordmark. Metadata, accessibility attributes and
code keep plain text; technical `muweave` identifiers remain unchanged. The
inline logo replaces the µ glyph, and hidden µ text preserves the complete
selectable and accessible product name without adding a second visible symbol.
The homepage and the linked explanation use native MathML for their displayed
formulas, as expressly requested for this project.
For the homepage's audible demonstration, `scripts/refresh_math_speech.cjs`
passes the actual formula in `src/page.html` through the locked Speech Rule
Engine with ClearSpeak rules and explicit spoken multiplication. The retained
`resources/math-speech.json` binds German, English and French results to that
MathML and the generator/toolchain hashes. The ordinary Python build rejects
stale results without requiring Node or SRE. It inserts the generated text as
the visible caption, which the browser also uses verbatim for playback.
The refresh also generates one local WAV recording per language with eSpeak NG;
the same snapshot binds their bytes to the formula and speech strings. Neither
speech generator is shipped in the website runtime.

Playback starts only through the read-aloud button, using Web Speech synthesis
and a voice matching the current page language. The same button stops playback;
navigation cancels the current utterance. Late cancellation events cannot reset
a later reading. Voice discovery can recover through `voiceschanged`. Missing
APIs, absent language voices, startup timeouts and synthesis errors fall back
to the retained recording. Each recording playback owns a new audio element so
late media events cannot affect its successor. Loading starts only on activation;
stop/navigation pauses it, and media failures leave a translated, retryable
error. The readable caption and native MathML remain available without
JavaScript or a speech service. The speech controller does not replace
screen-reader mathematics or load SRE into the browser.
The worksheet exports use PyHTML's `typst-mathml` path. They contain their own
runtime and embedded semantic AI document.

The same logo's integration into the PyHTML producer is separate package work.
The website does not modify the generated worksheet to add branding. The
learning-coach section uses the author's unchanged screenshot in
`assets/images/Lerncoach_Beispiel.png`, showing a German worksheet and its
actual coach conversation. A single-column layout places the explanatory text
and author guidance above the full-width image. Intrinsic image dimensions
preserve its aspect ratio; a normal image link opens the original resolution.
All editions retain the same screenshot with localized alternative text,
link label and caption.

## Authentic examples and developer documentation

The homepage teaching example owns a fixed excerpt of canonical Item 116 in
`examples/116.muweave`, plus the translated `116-en.muweave` and
`116-fr.muweave` copies. The excerpt contains the complete interactive function
and its placement; surrounding lesson prose and the print-description part are
absent. `examples/116-origin.json` records the copied source's historical hashes.
Neither the ordinary build nor `scripts/refresh_applet.py` reads the canonical
item library. Changes there cannot automatically update the homepage.

The applet refresh uses the public PyHTML API with publication mode, native
MathML, no document title, no AI bundle and no coach. Its manifest under
`resources/applet-116/` binds all three local sources to their complete HTML
exports and records the producer versions. The ordinary build validates those
hashes and copies the exports byte for byte. The displayed and downloadable
source comes from the same selected local file.

An isolated iframe runs the retained applet's original runtime. The homepage
adds presentation CSS to that embedded view to hide worksheet tools and remove
document margins/zoom; the stored export is not rewritten. A resize observer
fits the frame to its content. Narrow screens can scroll the applet horizontally
without shrinking mathematical labels. The complete source is shown below in
a keyboard-scrollable code area. Browser checks cover all velocity alternatives,
signed displacement, dependent slider bounds and the embedded presentation.

`examples/motion.muweave` owns a separate retained example, its translated text and
its parameter-driven graph. The language configuration changes between
editions; each edition's three backends receive the same source, title, locale
and publication setting. HTML preserves the slider, PDF renders its authored
default, and AI preserves the semantic expression and declared controls.
`resources/manifest.json` records exact source and output hashes and the
actual imported component versions. A separate preview manifest prevents
serving a screenshot after its source HTML has changed.

`examples/formula.muweave` is the source displayed on the linked explanation page.
The browser check compares the visible snippet with that file, and the
resource refresh retains its real PyHTML output.

The homepage's Python section uses one combined document for variable insertion,
arithmetic, the Python built-in `sum`, and bold formatting. The separate
`examples/formatting.py` library owns the illustrative `expr` identity function
and `bold`. `examples/bold.muweave` defines the shared variables and final
result in a `µexec` block; each edition's
`bold_call` supplies the surrounding document text. The refresh loads a fresh
library module
for each expansion and sets its `backend` variable to `latex`, `html`, or
`markdown`. It supplies both functions in a fresh core `MuWeaveContext`
before expanding the document, so the displayed source needs no import.
Core µWeave also provides `expr` itself.
This is example-specific setup, not a MuVocab backend-query API or its production
bold implementation. The library excerpt is extracted from both actual functions,
omitting their maintainer docstrings. Resource schema version 4 binds the
library and document setup to expansions with those functions already available.
The refresh retains the exact sources, engine version and expanded fragments in
`resources/bold.json`,
trimming only outer whitespace left by the setup. The build rejects a
changed library, setup or text until those exports are refreshed. It displays the
retained fragments as escaped code; it does not execute Python or invoke any
document backend during a static build. Browser checks compare all visible
source and output snippets with the retained artifact.

The expansion diagram places the document left of three equal-height output
cards, connected by independent curved SVG arrows matching the overview.
The library occupies its own row above the diagram, centered horizontally
on the connector gap. A separate dashed downward arrow stops before the upper
curve; it indicates dependency without becoming a node in the expansion paths.
Grid geometry anchors the arrows as code wraps. Narrow screens retain that
horizontal relationship in a labelled region scrollable by touch or keyboard.

The technical portal is built through the existing canonical µWeave suite
documentation pipeline and archived for independent publication. Its source
manifest records the originating package documents. The static build extracts
the archive beneath `developers/`, with its own generated Sphinx assets and
links. Worksheets and the developer portal remain producer-owned artifacts. The
applet embedding changes only its view presentation, not its runtime or assets.

`build/site/` is disposable generated output. GitHub Actions reconstructs it
from this repository without accessing the neighbouring workspaces.
