"""Refresh authentic worksheet exports and the canonical developer portal.

This maintainer command uses the installed MuWeave suite and LuaLaTeX. The
ordinary website build only needs Python's standard library and the resulting
checked-in resources. Generated worksheet HTML is retained byte for byte.
"""

import argparse
import hashlib
import importlib
import json
import runpy
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]
EDITIONS: dict[str, tuple[str, str]] = {
    "de": ("de-CH", "Beschleunigte Bewegung"),
    "en": ("en", "Accelerated motion"),
    "fr": ("fr", "Mouvement accéléré"),
}


def refresh(workspace: Path) -> None:
    """Produce the three editions from one source and snapshot documentation.

    Args:
        workspace: Canonical ggpackages workspace with the installed suite.
    """
    resources = ROOT / "resources"
    resources.mkdir(exist_ok=True)
    source = ROOT / "examples/motion.muweave"
    manifest: dict[str, object] = {
        "schema_version": 1,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "formula_sha256": hashlib.sha256(
            (ROOT / "examples/formula.muweave").read_bytes()
        ).hexdigest(),
        "components": {
            name: importlib.import_module(name.replace("-", "_")).__version__
            for name in (
                "muweave",
                "muvocab",
                "pyhtml",
                "pytex5",
                "pyai",
                "muweave-suite",
            )
        },
        "editions": {},
    }
    with tempfile.TemporaryDirectory(prefix="muweave-exports-") as temporary:
        staging = Path(temporary)
        for language, (locale, title) in EDITIONS.items():
            output = staging / language
            output.mkdir()
            shared = [
                str(source),
                "--publish",
                "--language",
                locale,
                "--title",
                title,
                "--config",
                f"example.language={language}",
            ]
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pyhtml",
                    *shared,
                    "--html-math-renderer",
                    "typst-mathml",
                    "--output",
                    str(output / "index.html"),
                ],
                check=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytex5",
                    *shared,
                    "--document",
                    "--output",
                    str(output / "worksheet.tex"),
                ],
                check=True,
            )
            subprocess.run(
                [sys.executable, "-m", "pyai", *shared, "--output", str(output / "ai")],
                check=True,
            )
            destination = resources / "examples" / language
            destination.mkdir(parents=True, exist_ok=True)
            for name in ("index.html", "worksheet.pdf"):
                shutil.copyfile(output / name, destination / name)
            shutil.copytree(output / "ai", destination / "ai", dirs_exist_ok=True)
            manifest["editions"][language] = {
                "locale": locale,
                "title": title,
                "config": {"example.language": language},
                "publish": True,
                "html_math_renderer": "typst-mathml",
            }

        # Keep the small source illustration tied to a real MuWeave export too.
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pyhtml",
                str(ROOT / "examples/formula.muweave"),
                "--publish",
                "--html-math-renderer",
                "typst-mathml",
                "--output",
                str(resources / "formula.html"),
            ],
            check=True,
        )
        namespace = runpy.run_path(
            str(workspace / "muweave-suite/scripts/sync_documentation_bundle.py")
        )
        snapshot = staging / "documentation"
        namespace["_write_bundle"](snapshot)
        from muweave_suite._local_docs import build_local_site

        developer_html = build_local_site(
            snapshot, staging / "portal", workspace
        ).parent
        shutil.copyfile(
            snapshot / "_manifest.json", resources / "developers-sources.json"
        )
        with zipfile.ZipFile(
            resources / "developers.zip",
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            for path in sorted(developer_html.rglob("*")):
                if path.is_file() and path.name != ".buildinfo":
                    entry = zipfile.ZipInfo(
                        path.relative_to(developer_html).as_posix(),
                        date_time=(2026, 1, 1, 0, 0, 0),
                    )
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(entry, path.read_bytes())
    manifest["files"] = {
        path.relative_to(resources).as_posix(): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in sorted(resources.rglob("*"))
        if path.is_file()
        and path.relative_to(resources).as_posix() not in {"manifest.json", "previews.json"}
        and path.name != "preview.png"
    }
    (resources / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    """Read the canonical workspace and refresh publication resources."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    refresh(args.workspace.resolve())


if __name__ == "__main__":
    main()
