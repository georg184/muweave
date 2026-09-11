# MuWeave homepage requirements

These selected conditions add homepage-specific constraints to the parent
workspace's `REQUIREMENTS.md`. The content and design proposal is in
`docs/WEBSITE_CONCEPT.md`; implementation work is tracked in `TODO.md`.

## MWH-ENTRY-01 — Immediate explanation

The homepage's main content begins with the title `MuWeave`, its educational
purpose statement, and an explanation identifying MuWeave as a Python-based
document language. That explanation connects one source to PDF, interactive
HTML, and structured AI-readable content before examples or entry actions,
and introduces the integrated worksheet learning coach as a core capability.
The explanation is visible in normal document flow without opening a menu,
tab, accordion, dialog, or another page.

- Owner: homepage markup and localized editorial content.
- Evidence: generated entry HTML, translations, DOM order, and browser views.
- Criterion: every language exposes that sequence directly on initial entry.

## MWH-AUDIENCE-01 — Teacher-facing primary content

The homepage explains the educational use of MuWeave in ordinary language.
Developer documentation is accessible through a secondary link labelled for
that audience. API inventories, package architecture, and developer setup
instructions are absent from the main introduction. Explanatory Python source
may illustrate the document language after its purpose has been established.

- Owner: homepage content and navigation.
- Evidence: entry copy, headings, links, and rendered navigation.
- Criterion: the main reading path explains the product without requiring
  developer documentation or exposing the toolchain's package catalogue.

## MWH-LANG-01 — Three complete language editions

The homepage supports German, English, and French. Its language selector uses
the existing ggprojects three-button flag pattern, identifies each language
accessibly, and exposes the selected state. The common `GGP-I18N-01` contract
applies to all visible content and accessibility text.

- Owner: localized pages and the language controller.
- Evidence: translation sources, fallback HTML, control markup, and switching
  tests including reload and history navigation.
- Criterion: all three editions provide equivalent content and a consistent
  selected language; a storage failure does not prevent reading or switching.

## MWH-CLAIMS-01 — Traceable product statements

The editorial concept distinguishes the agreed target product from verified
implementation status. Homepage drafts describe that target in the present
tense, including its learning coach and native-MathML accessibility.
Maintainer documentation relates target capabilities to their implementation
and verification work. Demonstrations, implementation reports, and test
results describe the artifacts actually exercised.

- Owner: website editorial content and its supporting references.
- Evidence: copy, target concept, open work, canonical component documentation,
  and the exact artifacts covered by any stated assessment.
- Criterion: readers of the maintainer documentation can distinguish target
  copy from implementation evidence; no demonstration or verification report
  presents an unimplemented function or an unperformed test as completed.

## MWH-COACH-01 — Integrated educational AI

The homepage presents the learning coach as part of the worksheet. It explains
that each prompt receives the essential subject content in an AI-suitable
representation, and that the author defines preliminary instructions guiding
the coach's educational approach. The AI backend is connected to this use
case, rather than described only as a separate export format.

- Owner: homepage introduction and localized learning-coach explanation.
- Evidence: all three language editions and their relationship to the source
  and output overview.
- Criterion: each edition explains integration, context on every prompt, and
  author-defined guidance before the illustrative teaching example.

## MWH-MATHML-01 — Readable mathematical structure

The homepage makes the intended accessibility benefit concrete: mathematical
formulas are available to screen readers through native MathML in the HTML
worksheet. It does not equate that benefit with universal accessibility of
every output or claim that MathJax and KaTeX cannot support accessibility.

- Owner: localized accessibility explanation and its supporting references.
- Evidence: all three editions, mathematical examples, and documented scope
  of the intended screen-reader behavior.
- Criterion: the explanation identifies spoken mathematics and native MathML
  without implying an unrelated PDF or blanket conformance guarantee.

## MWH-EXAMPLE-01 — Authentic source and outputs

Every example presented as demonstrating multiple MuWeave outputs derives
those outputs from the same identified source and documented build settings.
The website retains or references the actual generated artifacts instead of
recreating their behavior as a separate demonstration implementation.

- Owner: example sources, export procedure, and published examples.
- Evidence: source, build settings, generated PDF/HTML, and semantic AI content.
- Criterion: the shown outputs can be reproduced from that source; differences
  such as print defaults and interactive controls are accurately explained.
