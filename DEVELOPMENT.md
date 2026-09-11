# MuWeave homepage development

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

Edit `src/page.html`, all three files in `src/content/`, and `assets/` to change
the homepage. The build rejects incomplete translations, outdated example
exports and stale previews. Its content-derived version changes automatically.
Never edit the generated `build/site/` files to implement a change.

## Verification

```sh
python -m unittest discover -s tests -p 'test_*.py' -v
python -m ruff check scripts tests
python -m ruff format --check scripts tests
node --check assets/js/site.js
```

The unit suite builds the website. For browser verification, use an independent
development environment with `requirements-dev.txt` installed and Chromium
installed through Playwright:

```sh
python tests/browser_check.py
```

The browser check starts its own loopback HTTP server and exercises language
selection, reload/history, optional storage, the static fallback, keyboard
navigation, viewport widths of 320, 390, 768 and 1440 pixels, local links,
version mismatch handling and the genuine worksheet slider. It writes views
and results under `build/screenshots/` for manual inspection.

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

Refreshing examples and documentation requires the installed MuWeave suite,
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

`capture.py` derives raster favicons from the canonical SVG and captures the
actual interactive graph element in each exported worksheet. Its preview
manifest binds each image to that exact HTML export. After changing the SVG
alone, `python scripts/capture.py --icons-only` is sufficient before rebuilding.

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
