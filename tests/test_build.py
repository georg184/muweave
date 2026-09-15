"""Protect complete translations, authentic exports and cache coherence."""

import html
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT: Path = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "website_build", ROOT / "scripts/build.py"
)
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)


class PublicationTests(unittest.TestCase):
    """Check boundaries that could silently publish misleading page content."""

    def test_copied_applet_publishes_exact_export_and_visible_source(self) -> None:
        """The embedded example and displayed/downloaded source share one local copy."""
        output = build.build()
        for language, edition in build.read_applet(ROOT).items():
            with self.subTest(language=language):
                prefix = "" if language == "de" else language
                document = (output / prefix / "index.html").read_text(encoding="utf-8")
                self.assertIn(html.escape(edition["source"]), document)
                self.assertIn(f"examples/116/{language}.html?v=", document)
                self.assertEqual(
                    (output / "examples" / edition["filename"]).read_text(
                        encoding="utf-8"
                    ),
                    edition["source"],
                )
                self.assertEqual(
                    (output / f"examples/116/{language}.html").read_bytes(),
                    (ROOT / f"resources/applet-116/{language}.html").read_bytes(),
                )

    def test_changed_local_applet_or_html_rejects_stale_snapshot(self) -> None:
        """A copied source edit or damaged export must not silently change its counterpart."""
        for changed in ("examples/116.muweave", "resources/applet-116/fr.html"):
            with (
                self.subTest(changed=changed),
                tempfile.TemporaryDirectory() as temporary,
            ):
                root = Path(temporary)
                for name in ("examples", "resources/applet-116", "scripts"):
                    shutil.copytree(ROOT / name, root / name)
                path = root / changed
                path.write_bytes(path.read_bytes() + b"\nChanged local copy.\n")
                with self.assertRaisesRegex(ValueError, "Refresh copied applet"):
                    build.read_applet(root)

    def test_spoken_caption_comes_from_retained_mathml_conversion(self) -> None:
        """All editions display the generated speech, with native math still intact."""
        output = build.build()
        speech = build.read_math_speech(ROOT)
        for language, prefix in (("de", ""), ("en", "en/"), ("fr", "fr/")):
            with self.subTest(language=language):
                document = (output / prefix / "index.html").read_text(encoding="utf-8")
                self.assertIn(
                    'id="math-spoken">' + html.escape(speech[language]) + "</p>",
                    document,
                )
                self.assertEqual(document.count("<math "), 1)
                self.assertIn("<mfrac>", document)
                self.assertIn("<msup>", document)
                self.assertNotIn("math_spoken", build.read_content(ROOT)[language])

    def test_formula_generator_or_recording_changes_reject_stale_speech(self) -> None:
        """An edited formula, toolchain or audio cannot silently drift from speech."""
        for changed in (
            "src/page.html",
            "scripts/refresh_math_speech.cjs",
            "package-lock.json",
            "assets/audio/math-en.wav",
        ):
            with (
                self.subTest(changed=changed),
                tempfile.TemporaryDirectory() as temporary,
            ):
                root = Path(temporary)
                for name in (
                    "src/page.html",
                    "resources/math-speech.json",
                    "scripts/refresh_math_speech.cjs",
                    "package.json",
                    "package-lock.json",
                    "assets/audio/math-de.wav",
                    "assets/audio/math-en.wav",
                    "assets/audio/math-fr.wav",
                ):
                    target = root / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / name, target)
                path = root / changed
                source = path.read_bytes()
                path.write_bytes(
                    source.replace(b"<mn>2</mn></msup>", b"<mn>3</mn></msup>")
                    if changed == "src/page.html"
                    else source + b"\n",
                )
                with self.assertRaisesRegex(
                    ValueError, "Refresh mathematical (speech|audio)"
                ):
                    build.read_math_speech(root)

    def test_license_is_visible_and_full_notices_are_published(self) -> None:
        """All editions expose the license immediately and retain local legal texts."""
        output = build.build()
        for language, relative in (
            ("de", "index.html"),
            ("en", "en/index.html"),
            ("fr", "fr/index.html"),
        ):
            content = build.read_content(ROOT)[language]
            document = (output / relative).read_text(encoding="utf-8")
            with self.subTest(language=language):
                self.assertLess(
                    document.index('class="license-badge"'),
                    document.index('class="outputs"'),
                )
                self.assertIn(content["license_badge"], document)
                self.assertIn('id="license"', document)
                self.assertIn('rel="license"', document)
                self.assertIn("assets/licenses/GPL-3.0.txt", document)
                self.assertIn("assets/licenses/muvocab-NOTICE.txt", document)
        for filename in (
            "GPL-3.0.txt",
            "muweave-suite-NOTICE.txt",
            "muvocab-NOTICE.txt",
        ):
            self.assertEqual(
                (output / "assets/licenses" / filename).read_bytes(),
                (ROOT / "assets/licenses" / filename).read_bytes(),
            )
        license_text = (output / "assets/licenses/GPL-3.0.txt").read_text()
        self.assertIn("Version 3, 29 June 2007", license_text)
        self.assertIn("END OF TERMS AND CONDITIONS", license_text)
        self.assertIn(
            "GPL-3.0-only",
            (output / "assets/licenses/muweave-suite-NOTICE.txt").read_text(),
        )

    def test_translations_and_template_are_complete(self) -> None:
        """Every edition must render without missing or unused editorial text."""
        output = build.build()
        for relative, locale in (
            ("index.html", "de-CH"),
            ("en/index.html", "en"),
            ("fr/index.html", "fr"),
            ("document-language/index.html", "de-CH"),
            ("en/document-language/index.html", "en"),
            ("fr/document-language/index.html", "fr"),
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

    def test_wordmark_preserves_metadata_code_and_translation_escaping(self) -> None:
        """Brand artwork belongs in prose; source and attribute boundaries stay text."""
        markup = '<span class="muweave-wordmark">µWeave</span>'
        result = build.render(
            "<head><title>{{name}}</title></head>"
            '<h1>{{name}}</h1><p aria-label="{{name}}">{{body}}</p>'
            '<pre><code>{{name}}</code></pre><script>"{{name}}"</script>',
            {"name": "µWeave", "body": '<script>µWeave & "text"</script>'},
            wordmark=markup,
        )
        self.assertEqual(result.count(markup), 2)
        self.assertIn("<title>µWeave</title>", result)
        self.assertIn('aria-label="µWeave"', result)
        self.assertIn("<code>µWeave</code>", result)
        self.assertIn('<script>"µWeave"</script>', result)
        self.assertIn(
            "&lt;script&gt;" + markup + " &amp; &quot;text&quot;&lt;/script&gt;", result
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

    def test_unused_translation_stops_build(self) -> None:
        """Multiple page templates must not silently discard editorial text."""
        content = build.read_content(ROOT)
        for edition in content.values():
            edition["unused_editorial_text"] = "This text needs a visible placement."
        with patch.object(build, "read_content", return_value=content):
            with self.assertRaisesRegex(ValueError, "Unused translation keys"):
                build.build()

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

    def test_changed_bold_library_setup_or_text_rejects_old_expansions(self) -> None:
        """Library, variable setup and translated text edits must invalidate expansions."""
        for changed_input in ("library", "document", "call"):
            with self.subTest(changed_input=changed_input):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    for directory in ("examples", "resources", "src"):
                        shutil.copytree(ROOT / directory, root / directory)
                    if changed_input in {"library", "document"}:
                        name = (
                            "formatting.py"
                            if changed_input == "library"
                            else "bold.muweave"
                        )
                        with (root / "examples" / name).open(
                            "a", encoding="utf-8"
                        ) as stream:
                            stream.write("Changed input.\n")
                    else:
                        path = root / "src/content/fr.json"
                        content = json.loads(path.read_text(encoding="utf-8"))
                        content["bold_call"] = 'Texte µbold("modifié").'
                        path.write_text(json.dumps(content), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "Refresh bold exports"):
                        build.validate_resources(root)


if __name__ == "__main__":
    unittest.main()
