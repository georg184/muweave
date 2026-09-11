"""Build a complete static teacher-facing site using Python's standard library.

Translations fail closed on missing, empty or unused keys. Runtime assets and
entry documents receive one content-derived version. Checked-in exports are
verified against their manifest and then copied without rewriting their HTML.
"""

import hashlib
import html
import json
import re
import shutil
import struct
import tempfile
import zipfile
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]
PUBLIC_BASE: str = "https://georg184.github.io/muweave"
LANGUAGES: dict[str, tuple[str, str]] = {
    "de": ("de-CH", "de_CH"),
    "en": ("en", "en_GB"),
    "fr": ("fr", "fr_FR"),
}
TOKEN: re.Pattern[str] = re.compile(r"\{\{([a-z_]+)\}\}")


def read_content(root: Path) -> dict[str, dict[str, str]]:
    """Load equivalent, complete translations from the supplied project.

    Args:
        root: Website project whose translation files should be validated.
    """
    editions = {
        language: json.loads(
            (root / "src/content" / f"{language}.json").read_text(encoding="utf-8")
        )
        for language in LANGUAGES
    }
    keys = set(editions["de"])
    for language, content in editions.items():
        if set(content) != keys:
            raise ValueError(
                f"Translation keys differ for {language}: {sorted(keys ^ set(content))}"
            )
        if any(
            not isinstance(value, str) or not value.strip()
            for value in content.values()
        ):
            raise ValueError(f"Empty or non-text translation in {language}")
    return editions


def validate_resources(root: Path) -> None:
    """Reject stale exports or an example modified since its last generation.

    Args:
        root: Project containing source examples and their export manifest.
    """
    resources = root / "resources"
    manifest = json.loads((resources / "manifest.json").read_text(encoding="utf-8"))
    if manifest["schema_version"] != 1:
        raise ValueError("Unsupported resource manifest version")
    for name, key in (
        ("motion.muweave", "source_sha256"),
        ("formula.muweave", "formula_sha256"),
    ):
        if (
            hashlib.sha256((root / "examples" / name).read_bytes()).hexdigest()
            != manifest[key]
        ):
            raise ValueError(f"Refresh exports after changing {name}")
    for relative, digest in manifest["files"].items():
        path = resources / relative
        if not path.resolve().is_relative_to(resources.resolve()):
            raise ValueError("Resource manifest path escapes the resources directory")
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Resource differs from its generated export: {relative}")
    previews = json.loads((resources / "previews.json").read_text(encoding="utf-8"))
    for language in LANGUAGES:
        for name in ("index.html", "preview.png"):
            path = resources / "examples" / language / name
            if (
                hashlib.sha256(path.read_bytes()).hexdigest()
                != previews[language][name]
            ):
                raise ValueError(f"Recapture worksheet preview: {language}/{name}")


def content_version(root: Path) -> str:
    """Derive the shared cache token from every published input and the builder.

    Args:
        root: Project directory; ignored build output does not affect the token.
    """
    digest = hashlib.sha256()
    paths = [root / "scripts/build.py"]
    for directory in ("src", "assets", "examples", "resources"):
        paths.extend(path for path in (root / directory).rglob("*") if path.is_file())
    for path in sorted(paths):
        digest.update(path.relative_to(root).as_posix().encode("utf-8") + b"\0")
        digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()[:16]


def render(template: str, values: dict[str, str]) -> str:
    """Substitute escaped text while rejecting missing or unused placeholders.

    Args:
        template: Trusted shared HTML structure with named text placeholders.
        values: Complete language-specific text and generated URL values.
    """
    needed = set(TOKEN.findall(template))
    if needed != set(values):
        raise ValueError(f"Template/content mismatch: {sorted(needed ^ set(values))}")
    return TOKEN.sub(
        lambda match: html.escape(values[match.group(1)], quote=True), template
    )


def build(root: Path = ROOT) -> Path:
    """Validate and publish all editions below the project's ignored build path.

    Args:
        root: Website checkout; output is always contained in its build directory.
    """
    content = read_content(root)
    validate_resources(root)
    version = content_version(root)
    template = (root / "src/page.html").read_text(encoding="utf-8")
    build_root = root / "build"
    build_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".site-", dir=build_root) as temporary:
        destination = Path(temporary)
        shutil.copytree(root / "assets", destination / "assets")
        for name in ("css/site.css", "js/site.js"):
            path = destination / "assets" / name
            path.write_text(
                path.read_text(encoding="utf-8").replace("@@VERSION@@", version),
                encoding="utf-8",
            )
        shutil.copytree(root / "examples", destination / "examples")
        shutil.copytree(
            root / "resources/examples", destination / "examples", dirs_exist_ok=True
        )
        shutil.copyfile(
            root / "resources/formula.html", destination / "examples/formula.html"
        )
        shutil.copyfile(
            root / "resources/manifest.json", destination / "examples/manifest.json"
        )
        shutil.copyfile(
            root / "resources/previews.json", destination / "examples/previews.json"
        )
        portal = destination / "developers"
        with zipfile.ZipFile(root / "resources/developers.zip") as archive:
            for entry in archive.infolist():
                if (
                    not (portal / entry.filename)
                    .resolve()
                    .is_relative_to(portal.resolve())
                ):
                    raise ValueError("Developer archive contains an unsafe path")
            archive.extractall(portal)
        for language, (locale, og_locale) in LANGUAGES.items():
            relative_root = "./" if language == "de" else "../"
            path = destination if language == "de" else destination / language
            path.mkdir(exist_ok=True)
            with (root / "resources/examples" / language / "preview.png").open(
                "rb"
            ) as preview:
                header = preview.read(24)
            if header[:8] != b"\x89PNG\r\n\x1a\n":
                raise ValueError(f"Worksheet preview is not PNG: {language}")
            width, height = struct.unpack(">II", header[16:24])
            values = content[language] | {
                "language": language,
                "locale": locale,
                "og_locale": og_locale,
                "root": relative_root,
                "public_base": PUBLIC_BASE,
                "canonical": PUBLIC_BASE
                + ("/" if language == "de" else f"/{language}/"),
                "version": version,
                "example_base": f"{relative_root}examples/{language}/",
                "preview_width": str(width),
                "preview_height": str(height),
                **{
                    f"active_{choice}": str(language == choice).lower()
                    for choice in LANGUAGES
                },
            }
            (path / "index.html").write_text(render(template, values), encoding="utf-8")
        (destination / ".nojekyll").write_text("", encoding="utf-8")
        (destination / "version.json").write_text(
            json.dumps({"version": version}) + "\n", encoding="utf-8"
        )
        sitemap = (
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + "".join(
                f"<url><loc>{PUBLIC_BASE}{suffix}</loc></url>"
                for suffix in ("/", "/en/", "/fr/")
            )
            + "</urlset>\n"
        )
        (destination / "sitemap.xml").write_text(sitemap, encoding="utf-8")
        output = build_root / "site"
        if output.exists():
            shutil.rmtree(output)
        destination.rename(output)
    return output


if __name__ == "__main__":
    print(build())
