# First homepage publication checks

Audience: website maintainers and reviewers.

Local review date: 2026-09-11. The exact published resource identities and
component versions are recorded in `resources/manifest.json`; screenshots
are tied to their source exports by `resources/previews.json`.

## Exercised behavior

- The five standard-library tests pass, covering complete translations,
  escaped metadata/text, template parity, cache invalidation and stale exports.
- Ruff and JavaScript syntax checks pass.
- Chromium checks pass for German, English and French at viewport widths
  of 320, 390, 768 and 1440 pixels, without horizontal page overflow. Language
  controls retain a minimum target size of 44 pixels.
- Language selection, reload, back/forward navigation, remembered preference,
  explicit German entry and retained section anchors agree. The selector also
  works when session storage is unavailable. Static language links and text
  work with JavaScript disabled.
- Local entry links and assets resolve. Injecting mismatched JavaScript stops
  normal startup and shows the localized reload message.
- The code sample shown on each page matches `examples/formula.muweave`.
- In each authentic worksheet export, keyboard adjustment changes acceleration
  from 1.5 to 2 and updates the actual graph. Each contains native MathML with
  a fraction and an embedded semantic AI document, without external scripts.
- The PDF exports build through LuaLaTeX. The German single-page PDF and the
  graph screenshot were visually checked against the source/default value.
- The canonical developer portal builds successfully with Sphinx's strict
  warnings-as-errors pipeline.
- Desktop and mobile homepage views were visually reviewed. The logo was
  checked as a vector wordmark and the generated small browser icons.

axe-core 4.10.3 reports no violations in any of the three homepage editions
under the selected WCAG A/AA and best-practice rules. Each edition has 42
passing checks. Its `aria-prohibited-attr` and `color-contrast` rules also
contain cases requiring manual assessment; the report is not a complete
accessibility certification.

## Explicit limits

The coach dialogue is illustrative. No model request, author pre-prompt
delivery or conversational behavior was tested or implemented by this website
work. Native MathML presence and browser rendering were checked; spoken
mathematics with actual screen readers remains outstanding. The PDF is not
tagged and has not been assessed as an accessible PDF. The homepage logo has
not yet been added to the PyHTML producer.

The linked worksheets preserve the backend's own desktop document controls
and layout. The homepage's responsive layout checks do not certify that
separate worksheet interface or the generated developer portal.
