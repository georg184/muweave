"""Protect complete translations, authentic exports and cache coherence."""

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "website_build", ROOT / "scripts/build.py"
)
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)


class PublicationTests(unittest.TestCase):
    """Check boundaries that could silently publish misleading page content."""

    def test_translations_and_template_are_complete(self) -> None:
        """Every edition must render without missing or unused editorial text."""
        output = build.build()
        for relative, locale in (
            ("index.html", "de-CH"),
            ("en/index.html", "en"),
            ("fr/index.html", "fr"),
        ):
            document = (output / relative).read_text(encoding="utf-8")
            self.assertIn(f'lang="{locale}"', document)
            self.assertNotIn("{{", document)
            self.assertNotIn("@@VERSION@@", document)
            self.assertEqual(document.count('aria-pressed="true"'), 1)

    def test_translation_cannot_inject_html(self) -> None:
        """Translation and metadata values remain text even when they contain markup."""
        self.assertEqual(
            build.render(
                '<p title="{{title}}">{{text}}</p>',
                {"title": 'A "quote"', "text": "<script>&"},
            ),
            '<p title="A &quot;quote&quot;">&lt;script&gt;&amp;</p>',
        )

    def test_missing_translation_stops_build(self) -> None:
        """An incomplete French edition must not silently fall back to German."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(ROOT / "src", root / "src")
            path = root / "src/content/fr.json"
            content = json.loads(path.read_text(encoding="utf-8"))
            del content["coach_body"]
            path.write_text(json.dumps(content), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Translation keys differ for fr"):
                build.read_content(root)

    def test_runtime_edit_changes_version(self) -> None:
        """Changing JS must invalidate cached HTML, CSS and JS as one release."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("src", "assets", "scripts"):
                shutil.copytree(ROOT / name, root / name)
            before = build.content_version(root)
            self.assertEqual(before, build.content_version(root))
            with (root / "assets/js/site.js").open("a", encoding="utf-8") as stream:
                stream.write("\n/* changed runtime */\n")
            self.assertNotEqual(before, build.content_version(root))

    def test_changed_source_rejects_old_exports(self) -> None:
        """A changed downloadable source must not accompany obsolete output claims."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(ROOT / "examples", root / "examples")
            (root / "resources").mkdir()
            shutil.copyfile(
                ROOT / "resources/manifest.json", root / "resources/manifest.json"
            )
            with (root / "examples/motion.muweave").open(
                "a", encoding="utf-8"
            ) as stream:
                stream.write("Changed lesson.\n")
            with self.assertRaisesRegex(ValueError, "Refresh exports"):
                build.validate_resources(root)


if __name__ == "__main__":
    unittest.main()
