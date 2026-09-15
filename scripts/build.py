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
from html.parser import HTMLParser
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]
PUBLIC_BASE: str = "https://georg184.github.io/muweave"
LANGUAGES: dict[str, tuple[str, str]] = {
    "de": ("de-CH", "de_CH"),
    "en": ("en", "en_GB"),
    "fr": ("fr", "fr_FR"),
}
TOKEN: re.Pattern[str] = re.compile(r"\{\{([a-z_]+)\}\}")


class _Wordmarks(HTMLParser):
    """Replace product names only in rendered prose, preserving escaped text."""

    def __init__(self, wordmark: str) -> None:
        """Initialize a parser with one trusted, retained command expansion.

        Args:
            wordmark: Actual inline HTML produced by the µweave command.
        """
        super().__init__(convert_charrefs=False)
        self.wordmark = wordmark
        self.parts: list[str] = []
        self.protected = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Preserve attributes and enter literal or metadata elements.

        Args:
            tag: Parsed element name.
            attrs: Parsed attributes, preserved through the original source.
        """
        self.parts.append(self.get_starttag_text())
        if tag in {"head", "code", "pre", "script", "style", "textarea"}:
            self.protected += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Preserve an empty element without opening a text scope.

        Args:
            tag: Parsed element name.
            attrs: Parsed attributes, preserved through the original source.
        """
        self.parts.append(self.get_starttag_text())

    def handle_endtag(self, tag: str) -> None:
        """Leave protected text scopes and preserve closing elements.

        Args:
            tag: Closing element name.
        """
        if tag in {"head", "code", "pre", "script", "style", "textarea"}:
            self.protected -= 1
        self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        """Insert the wordmark in ordinary visible text only.

        Args:
            data: Already escaped, non-attribute text from the static renderer.
        """
        self.parts.append(
            data if self.protected else data.replace("µWeave", self.wordmark)
        )

    def handle_entityref(self, name: str) -> None:
        """Preserve a named character entity.

        Args:
            name: Entity name without delimiters.
        """
        self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        """Preserve a numeric character reference.

        Args:
            name: Decimal or hexadecimal reference without delimiters.
        """
        self.parts.append(f"&#{name};")

    def handle_decl(self, decl: str) -> None:
        """Preserve the document declaration.

        Args:
            decl: Declaration text without delimiters.
        """
        self.parts.append(f"<!{decl}>")

    def handle_comment(self, data: str) -> None:
        """Preserve a comment without replacing its technical text.

        Args:
            data: Comment body.
        """
        self.parts.append(f"<!--{data}-->")


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
    bold = json.loads((resources / "bold.json").read_text(encoding="utf-8"))
    if (
        bold["schema_version"] != 4
        or bold["strip_outer_whitespace"] is not True
        or "bold.json" not in manifest["files"]
    ):
        raise ValueError("Unsupported or untracked bold example export")
    for name, key in (
        ("formatting.py", "library_sha256"),
        ("bold.muweave", "document_sha256"),
    ):
        if (
            hashlib.sha256((root / "examples" / name).read_bytes()).hexdigest()
            != bold[key]
        ):
            raise ValueError(f"Refresh bold exports after changing {name}")
    document = (root / "examples/bold.muweave").read_text(encoding="utf-8").strip()
    if document != bold["document_setup"]:
        raise ValueError("Refresh bold exports after changing the document setup")
    for language, content in read_content(root).items():
        if (
            document + "\n\n" + content["bold_call"]
            != bold["editions"][language]["source"]
        ):
            raise ValueError(f"Refresh bold exports after changing the {language} call")
    previews = json.loads((resources / "previews.json").read_text(encoding="utf-8"))
    brand = json.loads((resources / "brand.json").read_text(encoding="utf-8"))
    if (
        brand["schema_version"] != 1
        or brand["source"] != "µweave"
        or brand["text"] != "µWeave"
        or "brand.json" not in manifest["files"]
        or hashlib.sha256(
            (root / "assets/brand/muweave-symbol.svg").read_bytes()
        ).hexdigest()
        != brand["svg_sha256"]
    ):
        raise ValueError("Refresh brand exports after changing the product symbol")
    for language in LANGUAGES:
        for name in ("index.html", "preview.png"):
            path = resources / "examples" / language / name
            if (
                hashlib.sha256(path.read_bytes()).hexdigest()
                != previews[language][name]
            ):
                raise ValueError(f"Recapture worksheet preview: {language}/{name}")


def read_math_speech(root: Path) -> dict[str, str]:
    """Keep displayed and spoken text bound to the actual homepage formula.

    Args:
        root: Project with native MathML and the retained SRE speech snapshot.
    """
    snapshot = json.loads(
        (root / "resources/math-speech.json").read_text(encoding="utf-8")
    )
    formulas = re.findall(
        r"<math\b[^>]*>[\s\S]*?</math>",
        (root / "src/page.html").read_text(encoding="utf-8"),
    )
    inputs = {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest()
        for name in (
            "scripts/refresh_math_speech.cjs",
            "package.json",
            "package-lock.json",
        )
    }
    if (
        snapshot["schema_version"] != 1
        or len(formulas) != 1
        or hashlib.sha256(formulas[0].encode("utf-8")).hexdigest()
        != snapshot["mathml_sha256"]
        or inputs != snapshot["inputs"]
        or set(snapshot["editions"]) != set(LANGUAGES)
        or any(
            not isinstance(text, str) or not text.strip()
            for text in snapshot["editions"].values()
        )
    ):
        raise ValueError("Refresh mathematical speech: npm run refresh:math-speech")
    for language in LANGUAGES:
        recording = snapshot["recordings"][language]
        expected = f"assets/audio/math-{language}.wav"
        if (
            recording["path"] != expected
            or hashlib.sha256((root / expected).read_bytes()).hexdigest()
            != recording["sha256"]
        ):
            raise ValueError("Refresh mathematical audio: npm run refresh:math-speech")
    return snapshot["editions"]


def read_applet(root: Path) -> dict[str, dict[str, str]]:
    """Validate fixed local applet sources against their retained HTML copies.

    Args:
        root: Homepage checkout; the canonical item library is never consulted.
    """
    folder = root / "resources/applet-116"
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    if (
        manifest["schema_version"] != 1
        or set(manifest["editions"]) != set(LANGUAGES)
        or manifest["generator_sha256"]
        != hashlib.sha256((root / "scripts/refresh_applet.py").read_bytes()).hexdigest()
    ):
        raise ValueError("Refresh copied applet: python scripts/refresh_applet.py")
    editions = {}
    for language in LANGUAGES:
        filename = "116.muweave" if language == "de" else f"116-{language}.muweave"
        source = (root / "examples" / filename).read_bytes()
        retained = manifest["editions"][language]
        if (
            retained["source"] != filename
            or retained["source_sha256"] != hashlib.sha256(source).hexdigest()
            or retained["html_sha256"]
            != hashlib.sha256((folder / f"{language}.html").read_bytes()).hexdigest()
        ):
            raise ValueError(f"Refresh copied applet after changing {filename}")
        editions[language] = {"filename": filename, "source": source.decode("utf-8")}
    return editions


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


def render(
    template: str, values: dict[str, str], *, wordmark: str | None = None
) -> str:
    """Substitute escaped text while rejecting missing or unused placeholders.

    Args:
        template: Trusted shared HTML structure with named text placeholders.
        values: Complete language-specific text and generated URL values.
        wordmark: Optional trusted HTML expansion for visible product names.
    """
    needed = set(TOKEN.findall(template))
    if needed != set(values):
        raise ValueError(f"Template/content mismatch: {sorted(needed ^ set(values))}")
    result = TOKEN.sub(
        lambda match: html.escape(values[match.group(1)], quote=True), template
    )
    if wordmark is None:
        return result
    parser = _Wordmarks(wordmark)
    parser.feed(result)
    parser.close()
    return "".join(parser.parts)


def build(root: Path = ROOT) -> Path:
    """Validate and publish all editions below the project's ignored build path.

    Args:
        root: Website checkout; output is always contained in its build directory.
    """
    content = read_content(root)
    validate_resources(root)
    math_speech = read_math_speech(root)
    applet = read_applet(root)
    bold = json.loads((root / "resources/bold.json").read_text(encoding="utf-8"))
    brand = json.loads((root / "resources/brand.json").read_text(encoding="utf-8"))
    version = content_version(root)
    templates = {
        suffix: (root / "src" / filename).read_text(encoding="utf-8")
        for suffix, filename in (
            ("", "page.html"),
            ("document-language/", "document-language.html"),
        )
    }
    template_keys = {
        suffix: set(TOKEN.findall(template)) for suffix, template in templates.items()
    }
    unused = set(content["de"]) - set().union(*template_keys.values())
    if unused:
        raise ValueError(f"Unused translation keys: {sorted(unused)}")
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
        shutil.copytree(root / "resources/applet-116", destination / "examples/116")
        shutil.copytree(
            root / "resources/examples", destination / "examples", dirs_exist_ok=True
        )
        shutil.copyfile(
            root / "resources/formula.html", destination / "examples/formula.html"
        )
        shutil.copyfile(
            root / "resources/bold.json", destination / "examples/bold.json"
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
        canonical_urls: list[str] = []
        for language, (locale, og_locale) in LANGUAGES.items():
            with (root / "resources/examples" / language / "preview.png").open(
                "rb"
            ) as preview:
                header = preview.read(24)
            if header[:8] != b"\x89PNG\r\n\x1a\n":
                raise ValueError(f"Worksheet preview is not PNG: {language}")
            width, height = struct.unpack(">II", header[16:24])
            language_prefix = "" if language == "de" else f"{language}/"
            for suffix, template in templates.items():
                edition_paths = {
                    choice: ("" if choice == "de" else f"{choice}/") + suffix
                    for choice in LANGUAGES
                }
                edition_path = edition_paths[language]
                relative_root = "../" * edition_path.count("/") or "./"
                canonical = f"{PUBLIC_BASE}/{edition_path}"
                canonical_urls.append(canonical)
                values = content[language] | {
                    "math_spoken": math_speech[language],
                    "applet_source": applet[language]["source"],
                    "applet_filename": applet[language]["filename"],
                    "bold_definition": bold["library_excerpt"],
                    "bold_setup": bold["document_setup"],
                    **{
                        f"bold_{backend}": output
                        for backend, output in bold["editions"][language][
                            "outputs"
                        ].items()
                    },
                    "language": language,
                    "locale": locale,
                    "og_locale": og_locale,
                    "root": relative_root,
                    "canonical": canonical,
                    "version": version,
                    "home": relative_root
                    + language_prefix
                    + ("?lang=de" if language == "de" else ""),
                    "explanation": relative_root
                    + language_prefix
                    + "document-language/"
                    + ("?lang=de" if language == "de" else ""),
                    "example_base": f"{relative_root}examples/{language}/",
                    "preview_width": str(width),
                    "preview_height": str(height),
                    **{
                        f"active_{choice}": str(language == choice).lower()
                        for choice in LANGUAGES
                    },
                    **{
                        f"href_{choice}": relative_root
                        + choice_path
                        + ("?lang=de" if choice == "de" else "")
                        for choice, choice_path in edition_paths.items()
                    },
                    **{
                        f"alternate_{choice}": f"{PUBLIC_BASE}/{choice_path}"
                        for choice, choice_path in edition_paths.items()
                    },
                }
                path = destination / edition_path
                path.mkdir(parents=True, exist_ok=True)
                (path / "index.html").write_text(
                    render(
                        template,
                        {
                            key: value
                            for key, value in values.items()
                            if key in template_keys[suffix]
                        },
                        wordmark=brand["html"],
                    ),
                    encoding="utf-8",
                )
        (destination / ".nojekyll").write_text("", encoding="utf-8")
        (destination / "version.json").write_text(
            json.dumps({"version": version}) + "\n", encoding="utf-8"
        )
        sitemap = (
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + "".join(
                f"<url><loc>{canonical}</loc></url>" for canonical in canonical_urls
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
