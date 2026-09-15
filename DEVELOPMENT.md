# µWeave homepage development

## Build and preview

The ordinary build requires Python 3.13 and its standard library. Run from this
repository:

```sh
python scripts/build.py
python -m http.server 8000 --bind 127.0.0.1 --directory build/site
```

Open `http://127.0.0.1:8000/`. German is at `/`, English at `/en/`, and French
at `/fr/`. The root respects the optional session preference; `/?lang=de`
selects German explicitly. The generated files work beneath the GitHub Pages
project prefix as well.

The linked explanation is at `/document-language/`, `/en/document-language/`
and `/fr/document-language/`. Language selection stays on that topic; its
return links lead to the matching homepage edition.

Keep the local server running while editing. After a source change, rerun
`python scripts/build.py` and reload the browser; no GitHub publication is
needed for local review.

Edit `src/page.html`, `src/document-language.html`, all three files in
`src/content/`, and `assets/` to change the website. The build rejects
incomplete translations, outdated example exports and stale previews. Its
content-derived version changes automatically.
Never edit the generated `build/site/` files to implement a change.

## Verification

```sh
python -m unittest discover -s tests -p 'test_*.py' -v
python -m ruff check scripts tests
python -m ruff format --check scripts tests
node --check assets/js/site.js
node --check scripts/refresh_math_speech.cjs
```

The unit suite builds the website. For browser verification, use an independent
development environment with `requirements-dev.txt` installed and Chromium
installed through Playwright:

```sh
python tests/browser_check.py
```

The browser check starts its own loopback HTTP server and exercises language
selection without scroll jumps (including stale section anchors), reload/history,
optional storage, the static fallback, keyboard
navigation, the linked explanation and its return links, viewport widths of
320, 390, 768 and 1440 pixels, local links, version mismatch handling and the
genuine worksheet slider. Item 116 checks cover all velocity alternatives,
signed displacement, dependent bounds, copied source and the applet-only view.
It writes views
and results under `build/screenshots/` for manual inspection.
The speech checks exercise real page controls against a replaced Web Speech
API: language choice, keyboard start, stop, late events, navigation cancellation,
missing/late voices, errors and startup timeout. Real media playback checks
cover the retained audio files in all three languages, natural completion,
stop, navigation and a failed request followed by retry. The browser's genuine
voice availability and recording playback are recorded separately. These checks
do not replace listening on the target device or a real screen-reader audit.

To include axe-core, supply a locally obtained script:

```sh
python tests/browser_check.py --axe /path/to/axe.min.js
```

The first publication was checked with axe-core 4.10.3. Automated results do
not establish spoken mathematics support in a particular screen reader.

In the shared ggpackages workspace, run official Python checks with
`./pythonvenv1_dbg/bin/python`. Browser dependencies belong in an agent-managed
environment such as `.codex-venv`; do not install them into the mirrored
workspace environments. A restricted sandbox may require an explicitly
writable `TEXMFVAR`/`TEXMFCACHE` directory and permission to launch Chromium.

## Refresh generated resources

The homepage's Item 116 example is a fixed copy. Its local sources are
`examples/116.muweave`, `116-en.muweave` and `116-fr.muweave`. Edit these copies
explicitly to change the homepage example; changing the original item library
has no effect, including when running this refresh:

```sh
python scripts/refresh_applet.py
python scripts/build.py
```

Run the first command with the installed MuWeave suite. It reads only these
local sources and retains complete, unchanged PyHTML exports with a manifest in
`resources/applet-116/`. Commit changed local sources and exports together.
Keep the copied applet's controls and internal legends; the surrounding lesson
prose is excluded. The homepage's iframe presentation is owned by `site.js` and
`site.css`, so changing that view does not require editing a generated export.
The ordinary static build needs no item-library access or MuWeave installation.

The homepage's mathematical speech is independent of the worksheet exports.
After changing its native formula in `src/page.html`, refresh the three speech
strings and WAV recordings with the pinned Node development tool (Node 18 or
newer) and eSpeak NG 1.52.0:

```sh
npm ci --ignore-scripts
npm run refresh:math-speech
npm run check:math-speech
python scripts/build.py
```

`resources/math-speech.json` and `assets/audio/math-*.wav` are generated; do not
translate or edit them by hand. Commit them with formula or generator changes.
An `ESPEAK_NG` environment variable can point to a development-local executable;
otherwise the command uses `espeak-ng` from `PATH`. The check command reruns
both generators and compares the snapshot and audio without changing published
resources. `package-lock.json`
retains the toolchain; the XML dependency override selects a corrected patch
release over SRE's deprecated pin. None of these Node dependencies is published
to visitors or needed for the ordinary static Pages build. Only the generated
text and recordings are published; no speech service or API key is required.

Refreshing examples and documentation requires the installed µWeave suite,
its local canonical workspace and a working LuaLaTeX installation. The static
Pages build does not install or run those tools.

```sh
python scripts/refresh_resources.py --workspace /path/to/software/Python/ggpackages
python scripts/capture.py
python scripts/build.py
```

Use the suite environment for `refresh_resources.py` and the browser environment
for `capture.py`. The first command exports `examples/motion.muweave` through
PyHTML, PyTeX5 and PyAI using the documented settings in
`resources/manifest.json`. It also renders `examples/formula.muweave`, collects
the canonical documentation with the suite's existing bundle writer, and
builds its portal with the suite's existing strict Sphinx pipeline.

The resulting documentation archive and source manifest are stored in
`resources/developers.zip` and `resources/developers-sources.json`. They are
generated snapshots; edit the owning packages to change their contents.
The worksheet HTML is copied byte for byte. No local `.work` file or learner
state is included.

`capture.py` derives raster favicons from the retained canonical SVG copy and
captures the actual interactive graph element in each exported worksheet. Its
preview manifest binds each image to that exact HTML export. After refreshing a
changed canonical SVG through `--brand-only`, run
`python scripts/capture.py --icons-only` before rebuilding.

The small `bold` demonstration can be refreshed independently with the installed
core µWeave package, without rebuilding worksheets or the documentation portal:

```sh
python scripts/refresh_resources.py --bold-only
python scripts/build.py
```

Refresh the licensed developer documentation and the retained license notices
without rebuilding unchanged worksheet examples:

```sh
python scripts/refresh_resources.py --workspace /path/to/software/Python/ggpackages --docs-only
python scripts/build.py
```

The GPL text and package notices in `assets/licenses/` are exact copies of the
suite's `LICENSE`/`NOTICE` and MuVocab's `NOTICE`. Edit those canonical package
files and refresh them through this command; do not edit the website copies.

Edit `examples/formatting.py` for the library functions, `examples/bold.muweave`
for the shared variables, and the three `bold_call` translations
for the combined text using variables, `expr`, Python's built-in `sum`, and `bold`.
The refresh gives each expansion a fresh library module with its `backend`
variable set to `latex`, `html`, or `markdown`. It supplies `bold` and `expr`
in a fresh core context before expanding the document. The script retains the
complete library, its displayed excerpt, the document inputs and resulting fragments in
`resources/bold.json`, then updates the resource-manifest hash. The full
resource refresh includes this step as well.

Review and commit the changed source and resource files together. PDF metadata
and documentation source locations can change on regeneration; deterministic
website generation means identical checked-in inputs yield identical site
bytes, not that separate LuaLaTeX runs necessarily have identical metadata.

## GitHub Pages

This directory has its own repository, `georg184/muweave`, with default branch
`main`. Pages uses GitHub Actions. `.github/workflows/deploy-pages.yml` checks
the build and deploys only `build/site/`; it uses the checked-in example and
documentation snapshots and needs no Python package credentials or AI keys.

After an authorized push, follow the workflow to its terminal state. Compare
the public `/muweave/version.json` with `build/site/version.json`, then verify
all three language entries, an example and the developer portal. A changed
runtime or content input automatically gets a different cache token.

## Product wordmark

Visible product names use `µWeave`; commands, filenames and Python identifiers
retain their technical spelling. The prose wordmark comes from the real bare
`µweave` command, with the unchanged woven symbol supplied by MuVocab.

Refresh only this shared artwork and its command expansion with:

```sh
python scripts/refresh_resources.py --brand-only
python scripts/build.py
```

The refresh requires the installed MuVocab package and copies its canonical
SVG byte for byte. After an intentional SVG change, also recapture the icons.
The ordinary static build uses only retained artifacts and the standard library.
