# MuWeave homepage architecture

## Static editions

`src/page.html` owns the shared semantic structure. `src/content/de.json`,
`en.json` and `fr.json` own equivalent editorial and accessible text. The small
standard-library builder validates key parity and escapes every substituted
value, then produces three complete HTML pages. Relative links support both
a local server and the `/muweave/` GitHub Pages prefix.

`assets/js/site.js` only handles language navigation and mixed-version
detection. The flag buttons follow the existing `motion` presentation, with
native language names, pressed state and targets of at least 44 pixels.
Static language links remain available if JavaScript is disabled or fails to
load. An optional session preference is subordinate to explicit language URLs
and history restoration. Section anchors survive button-based switching.

## Version coherence

The builder hashes published source inputs, assets, resources and its own code
to derive one version token. The three entry documents, CSS and JavaScript
share it; local entry asset URLs carry it. Startup compares the document,
JavaScript and CSS tokens and displays a localized reload message on mismatch.
A content hash avoids a forgotten manual timestamp bump. There is no service
worker and no external font or runtime dependency on the teacher homepage.

## Brand and mathematics

`assets/brand/muweave-symbol.svg` is the canonical interwoven µ. Playwright
renders it for Pillow's raster favicon conversions. The homepage uses native
MathML for both displayed formulas, as expressly requested for this project.
The worksheet exports use PyHTML's `typst-mathml` path. They contain their own
runtime and embedded semantic AI document.

The same logo's integration into the PyHTML producer is separate package work.
The website does not modify the generated worksheet to add branding or to
simulate a coach. The homepage conversation is labelled illustrative content.

## Authentic examples and developer documentation

`examples/motion.muweave` owns the teaching example, its translated text and
its parameter-driven graph. The language configuration changes between
editions; each edition's three backends receive the same source, title, locale
and publication setting. HTML preserves the slider, PDF renders its authored
default, and AI preserves the semantic expression and declared controls.
`resources/manifest.json` records exact source and output hashes and the
actual imported component versions. A separate preview manifest prevents
serving a screenshot after its source HTML has changed.

`examples/formula.muweave` is the source displayed in the Python explanation.
The browser check compares the visible snippet with that file, and the
resource refresh retains its real PyHTML output.

The technical portal is built through the existing canonical MuWeave suite
documentation pipeline and archived for independent publication. Its source
manifest records the originating package documents. The static build extracts
the archive beneath `developers/`, with its own generated Sphinx assets and
links. Worksheets and the developer portal remain producer-owned artifacts;
the homepage runtime does not rewrite or govern their internal asset formats.

`build/site/` is disposable generated output. GitHub Actions reconstructs it
from this repository without accessing the neighbouring workspaces.
