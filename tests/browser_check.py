"""Exercise language navigation, small screens and genuine worksheet controls.

Run after scripts/build.py with an environment containing Playwright/Chromium.
The server serves only the generated site on an ephemeral loopback port.
"""

import argparse
import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright

ROOT: Path = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    """Serve the generated site without logging each successful asset request."""

    def log_message(self, format: str, *args: object) -> None:
        """Suppress server chatter; browser failures are asserted separately.

        Args:
            format: Base handler message format.
            args: Base handler message values.
        """


def check(axe_path: Path | None = None) -> None:
    """Run browser assertions and retain desktop/mobile views for inspection.

    Args:
        axe_path: Optional local axe-core script for automated accessibility checks.
    """
    site = ROOT / "build/site"
    screenshots = ROOT / "build/screenshots"
    screenshots.mkdir(exist_ok=True)
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(site))
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context(viewport={"width": 1440, "height": 1100})
            page = context.new_page()
            errors: list[str] = []
            accessibility: dict[str, object] = {}
            page.on("pageerror", lambda error: errors.append(str(error)))
            for language, suffix in (
                ("de", "/?lang=de"),
                ("en", "/en/"),
                ("fr", "/fr/"),
            ):
                page.goto(base + suffix)
                assert page.locator("html").get_attribute("data-language") == language
                assert (
                    page.locator('button[aria-pressed="true"]').get_attribute(
                        "data-language"
                    )
                    == language
                )
                assert page.locator(".version-error").is_hidden()
                assert page.locator("main math").count() == 2
                assert (
                    page.locator(".code-window pre").inner_text().strip()
                    == (ROOT / "examples/formula.muweave")
                    .read_text(encoding="utf-8")
                    .strip()
                )
                assert (
                    page.locator(
                        'main script[src*="mathjax"], main script[src*="katex"]'
                    ).count()
                    == 0
                )
                for href in page.locator("[href], [src]").evaluate_all(
                    "elements => elements.map(e => e.getAttribute('href') || e.getAttribute('src'))"
                ):
                    address = urlsplit(href)
                    if address.scheme or not address.path:
                        continue
                    resolved = urlsplit(
                        page.evaluate("href => new URL(href, location.href).href", href)
                    )
                    target = site / unquote(resolved.path).lstrip("/")
                    assert target.exists(), f"Broken local resource: {href}"
                page.screenshot(
                    path=str(screenshots / f"{language}-desktop.png"), full_page=True
                )
                for width in (320, 390, 768):
                    page.set_viewport_size({"width": width, "height": 844})
                    assert page.evaluate(
                        "document.documentElement.scrollWidth <= innerWidth"
                    ), f"Horizontal overflow: {language}/{width}"
                    for box in page.locator("button[data-language]").all():
                        bounds = box.bounding_box()
                        assert bounds["width"] >= 44 and bounds["height"] >= 44
                    if width == 390:
                        page.screenshot(
                            path=str(screenshots / f"{language}-mobile.png"),
                            full_page=True,
                        )
                page.set_viewport_size({"width": 1440, "height": 1100})
                if axe_path is not None:
                    page.add_script_tag(path=str(axe_path))
                    report = page.evaluate(
                        "async () => await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice']}})"
                    )
                    accessibility[language] = {
                        "violations": report["violations"],
                        "passes": len(report["passes"]),
                        "incomplete": [item["id"] for item in report["incomplete"]],
                    }
                    assert not report["violations"], json.dumps(
                        report["violations"], ensure_ascii=False
                    )

            # URL, session preference and browser history agree after switching.
            page.goto(base + "/?lang=de#coach")
            page.get_by_role("button", name="English", exact=True).click()
            page.wait_for_url("**/en/#coach")
            page.reload()
            assert page.locator("html").get_attribute("lang") == "en"
            page.get_by_role("button", name="Français", exact=True).click()
            page.wait_for_url("**/fr/#coach")
            page.go_back()
            assert page.locator("html").get_attribute("data-language") == "en"
            page.go_forward()
            assert page.locator("html").get_attribute("data-language") == "fr"
            page.goto(base + "/")
            page.wait_for_url("**/fr/")
            page.goto(base + "/?lang=de")
            assert page.locator("html").get_attribute("data-language") == "de"
            page.keyboard.press("Tab")
            assert page.get_by_role("link", name="Zum Inhalt").evaluate(
                "e => e === document.activeElement"
            )
            page.keyboard.press("Enter")
            page.keyboard.press("Tab")
            assert page.evaluate("document.activeElement.tagName") == "A"

            # Every worksheet is a real backend export with native mathematics.
            worksheet_results: dict[str, object] = {}
            for language in ("de", "en", "fr"):
                page.goto(base + f"/examples/{language}/index.html")
                slider = page.locator('input[data-muvocab-reactive-parameter="a"]')
                assert slider.input_value() == "1.5"
                graph = page.locator(".muvocab-reactive-output svg")
                before = graph.inner_html()
                slider.focus()
                slider.press("ArrowRight")
                assert slider.input_value() == "2"
                page.wait_for_function(
                    "before => document.querySelector('.muvocab-reactive-output svg').innerHTML !== before",
                    arg=before,
                    timeout=5000,
                )
                assert page.locator("#document math").count() > 0
                assert page.locator("#document mfrac").count() > 0
                assert page.locator("script[src]").count() == 0
                embedded = page.locator(
                    'script[type="application/json"]'
                ).all_text_contents()
                assert any("muweave-ai" in item for item in embedded)
                worksheet_results[language] = {
                    "slider_before": "1.5",
                    "slider_after": "2",
                    "graph_changed": True,
                    "mathml_formulas": page.locator("#document math").count(),
                }
            assert not errors, errors
            context.close()

            # An unavailable session store must not disable the selector.
            restricted = browser.new_context()
            restricted.add_init_script(
                "Object.defineProperty(window, 'sessionStorage', {get() {throw new Error('Storage unavailable')}})"
            )
            page = restricted.new_page()
            page.goto(base + "/")
            page.get_by_role("button", name="Français", exact=True).click()
            page.wait_for_url("**/fr/")
            restricted.close()

            # Static language links and all product copy work without JavaScript.
            offline = browser.new_context(java_script_enabled=False)
            page = offline.new_page()
            page.goto(base + "/")
            assert page.get_by_role("link", name="English", exact=True).is_visible()
            page.get_by_role("link", name="English", exact=True).click()
            assert page.locator("html").get_attribute("lang") == "en"
            assert page.get_by_text(
                "A learning coach that knows the teaching material", exact=True
            ).is_visible()
            offline.close()

            # Mixed cached versions fail visibly before the controller runs.
            mismatch = browser.new_context()
            page = mismatch.new_page()
            page.route(
                "**/assets/js/site.js*",
                lambda route: route.fulfill(
                    path=str(ROOT / "assets/js/site.js"), content_type="text/javascript"
                ),
            )
            page.goto(base + "/en/")
            assert page.get_by_role(
                "heading", name="Please reload the page."
            ).is_visible()
            assert page.locator(".site-shell").is_hidden()
            mismatch.close()
            browser.close()
        (screenshots / "checks.json").write_text(
            json.dumps(
                {
                    "languages": ["de", "en", "fr"],
                    "viewports": [320, 390, 768, 1440],
                    "worksheet": worksheet_results,
                    "javascript_errors": errors,
                    "axe": accessibility,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print("Browser checks passed; screenshots are in build/screenshots.")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--axe", type=Path)
    check(parser.parse_args().axe)
