"""Refresh authentic worksheet exports and the canonical developer portal.

This maintainer command uses the installed MuWeave suite and LuaLaTeX. The
ordinary website build only needs Python's standard library and the resulting
checked-in resources. Generated worksheet HTML is retained byte for byte.
"""

import argparse
import ast
import hashlib
import importlib
import json
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import types
import zipfile
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]
EDITIONS: dict[str, tuple[str, str]] = {
    "de": ("de-CH", "Beschleunigte Bewegung"),
    "en": ("en", "Accelerated motion"),
    "fr": ("fr", "Mouvement accéléré"),
}


def refresh_brand() -> None:
    """Retain the real inline µweave expansion and its unchanged canonical SVG."""
    from importlib.resources import files

    import muvocab
    import muweave
    import pyai
    import pyhtml

    source = "µweave"
    schema = muvocab.create_text_command_schema()
    parsed = muweave.parse_string(source, text_command_schema=schema)
    fragment = pyhtml.expand_parsed_body(parsed, muvocab.create_html_context(schema))
    matches = re.findall(
        r'<p>(<span class="muweave-wordmark".*</span>)</p>', fragment.html, re.DOTALL
    )
    if len(matches) != 1 or fragment.asset_store_json or fragment.requires_math_runtime:
        raise ValueError(
            "The product name must expand to one self-contained inline wordmark"
        )
    text = pyai.build_parsed(parsed, muvocab.create_ai_context(schema)).markdown.strip()
    symbol = files("muvocab").joinpath("_brand/muweave-symbol.svg").read_bytes()
    snapshot = {
        "schema_version": 1,
        "source": source,
        "muweave_version": muweave.__version__,
        "muvocab_version": muvocab.__version__,
        "html": matches[0],
        "text": text,
        "svg_sha256": hashlib.sha256(symbol).hexdigest(),
    }
    (ROOT / "resources/brand.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "assets/brand/muweave-symbol.svg").write_bytes(symbol)


def refresh_bold() -> None:
    """Expand the document with library functions supplied by each backend."""
    import muweave

    library_path = ROOT / "examples/formatting.py"
    library_source = library_path.read_text(encoding="utf-8")
    library_code = compile(library_source, str(library_path), "exec")
    functions = [
        node
        for node in ast.parse(library_source).body
        if isinstance(node, ast.FunctionDef) and node.name in {"expr", "bold"}
    ]
    if {function.name for function in functions} != {"expr", "bold"}:
        raise ValueError("The example library must define expr and bold")
    # Show the actual functions without their maintainer docstrings.
    lines = library_source.splitlines()
    excerpts: list[str] = []
    for function in functions:
        excerpt = "\n".join(lines[function.lineno - 1 : function.end_lineno])
        if ast.get_docstring(function) is not None:
            excerpt = "\n".join(
                lines[function.lineno - 1 : function.body[0].lineno - 1]
                + lines[function.body[0].end_lineno : function.end_lineno]
            )
        excerpts.append(excerpt)
    document = (ROOT / "examples/bold.muweave").read_text(encoding="utf-8")
    snapshot: dict[str, object] = {
        "schema_version": 4,
        "muweave_version": muweave.__version__,
        "library_source": library_source,
        "library_excerpt": "\n\n".join(excerpts),
        "library_sha256": hashlib.sha256(library_source.encode("utf-8")).hexdigest(),
        "document_setup": document.strip(),
        "document_sha256": hashlib.sha256(document.encode("utf-8")).hexdigest(),
        "strip_outer_whitespace": True,
        "editions": {},
    }
    for language in EDITIONS:
        content = json.loads(
            (ROOT / "src/content" / f"{language}.json").read_text(encoding="utf-8")
        )
        source = document.strip() + "\n\n" + content["bold_call"]
        outputs: dict[str, str] = {}
        for backend in ("latex", "html", "markdown"):
            library = types.ModuleType("formatting")
            library.__file__ = str(library_path)
            exec(library_code, library.__dict__)
            library.backend = backend
            context = muweave.MuWeaveContext()
            context.namespace.update(bold=library.bold, expr=library.expr)
            outputs[backend] = muweave.expand_string(
                source,
                context,
                source_name=f"bold-{language}.muweave",
            ).strip()
        snapshot["editions"][language] = {
            "source": source,
            "outputs": outputs,
        }
    (ROOT / "resources/bold.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def refresh_documentation(workspace: Path) -> None:
    """Refresh the complete developer portal and canonical licensing resources.

    Args:
        workspace: MuWeave package workspace containing canonical documentation.
    """
    resources = ROOT / "resources"
    with tempfile.TemporaryDirectory(prefix="muweave-documentation-") as temporary:
        staging = Path(temporary)
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

    licenses = ROOT / "assets/licenses"
    licenses.mkdir(parents=True, exist_ok=True)
    for source, name in (
        (workspace / "muweave-suite/LICENSE", "GPL-3.0.txt"),
        (workspace / "muweave-suite/NOTICE", "muweave-suite-NOTICE.txt"),
        (workspace / "muvocab/NOTICE", "muvocab-NOTICE.txt"),
    ):
        shutil.copyfile(source, licenses / name)


def refresh(workspace: Path) -> None:
    """Produce the three editions from one source and snapshot documentation.

    Args:
        workspace: Canonical ggpackages workspace with the installed suite.
    """
    resources = ROOT / "resources"
    resources.mkdir(exist_ok=True)
    refresh_bold()
    refresh_brand()
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
        refresh_documentation(workspace)
    manifest["files"] = {
        path.relative_to(resources).as_posix(): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in sorted(resources.rglob("*"))
        if path.is_file()
        and path.relative_to(resources).as_posix()
        not in {"manifest.json", "previews.json"}
        and path.name != "preview.png"
    }
    (resources / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    """Read the canonical workspace and refresh publication resources."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path)
    partial = parser.add_mutually_exclusive_group()
    partial.add_argument(
        "--bold-only",
        action="store_true",
        help="Refresh only the small Python example.",
    )
    partial.add_argument(
        "--brand-only", action="store_true", help="Refresh only the product wordmark."
    )
    partial.add_argument(
        "--docs-only",
        action="store_true",
        help="Refresh only developer documentation and licensing resources.",
    )
    args = parser.parse_args()
    if args.docs_only and args.workspace is None:
        parser.error("--docs-only requires --workspace")
    if args.bold_only or args.brand_only or args.docs_only:
        if args.docs_only:
            refresh_documentation(args.workspace.resolve())
            refreshed = ("developers.zip", "developers-sources.json")
        elif args.brand_only:
            refresh_brand()
            refreshed = ("brand.json",)
        else:
            refresh_bold()
            refreshed = ("bold.json",)
        manifest_path = ROOT / "resources/manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for resource in refreshed:
            manifest["files"][resource] = hashlib.sha256(
                (ROOT / "resources" / resource).read_bytes()
            ).hexdigest()
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    elif args.workspace is None:
        parser.error(
            "--workspace is required unless --bold-only or --brand-only is used"
        )
    else:
        refresh(args.workspace.resolve())


if __name__ == "__main__":
    main()
