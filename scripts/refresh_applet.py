"""Export the homepage's fixed copies of Item 116 with the installed MuWeave suite.

The canonical item library is deliberately not read. Edit the homepage's local
source copies explicitly before refreshing these retained HTML artifacts.
"""

import hashlib
import json
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]


def refresh(root: Path = ROOT) -> None:
    """Retain complete PyHTML artifacts generated from the local applet sources.

    Args:
        root: Homepage checkout owning all source copies and generated resources.
    """
    import muvocab
    import muweave
    import pyhtml

    destination = root / "resources/applet-116"
    destination.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "origin": json.loads((root / "examples/116-origin.json").read_text()),
        "generator_sha256": hashlib.sha256(
            (root / "scripts/refresh_applet.py").read_bytes()
        ).hexdigest(),
        "components": {
            "muweave": muweave.__version__,
            "muvocab": muvocab.__version__,
            "pyhtml": pyhtml.__version__,
        },
        "settings": {
            "publish": True,
            "embed_ai": False,
            "coach": False,
            "html_math_renderer": "typst-mathml",
            "body_width_ratio": 1,
            "body_height_ratio": 1,
        },
        "editions": {},
    }
    for language, locale in (("de", "de-CH"), ("en", "en"), ("fr", "fr")):
        name = "116.muweave" if language == "de" else f"116-{language}.muweave"
        source = (root / "examples" / name).read_text(encoding="utf-8")
        schema = muvocab.create_text_command_schema()
        context = muvocab.create_html_context(schema, publish=True)
        document = pyhtml.expand_string(
            source,
            context,
            source_name=name,
            output_name=f"116-{language}.html",
            language=locale,
            embed_ai=False,
            coach=False,
            body_width_ratio=1,
            body_height_ratio=1,
            html_math_renderer="typst-mathml",
        )
        (destination / f"{language}.html").write_text(document, encoding="utf-8")
        manifest["editions"][language] = {
            "source": name,
            "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
            "html_sha256": hashlib.sha256(document.encode("utf-8")).hexdigest(),
        }
    (destination / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    refresh()
    print(ROOT / "resources/applet-116")
