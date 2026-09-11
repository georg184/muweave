"""Rasterize the vector brand and capture previews of the actual worksheets.

Maintainer-only dependencies: Playwright with Chromium, and Pillow. No visual
content is reconstructed: previews are screenshots of the generated exports.
"""

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT: Path = Path(__file__).resolve().parents[1]


def capture(icons_only: bool = False) -> None:
    """Create browser icon sizes and unchanged worksheet screenshots.

    Args:
        icons_only: Skip worksheet captures when exports have not been built.
    """
    brand = ROOT / "assets/brand"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 256, "height": 256}, device_scale_factor=2
        )
        svg = (brand / "muweave-symbol.svg").read_text(encoding="utf-8")
        page.set_content(
            "<style>html,body{margin:0;background:transparent}svg{width:256px;height:256px;display:block}</style>"
            + svg
        )
        master_path = ROOT / "build/brand-master.png"
        master_path.parent.mkdir(exist_ok=True)
        page.screenshot(path=str(master_path), omit_background=True)
        with Image.open(master_path) as master:
            for size in (16, 32, 180):
                name = f"favicon-{size}.png" if size != 180 else "apple-touch-icon.png"
                master.resize((size, size), Image.Resampling.LANCZOS).save(brand / name)
            master.save(brand / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
        page.close()
        if not icons_only:
            previews: dict[str, dict[str, str]] = {}
            for language in ("de", "en", "fr"):
                edition = ROOT / "resources/examples" / language
                page = browser.new_page(
                    viewport={"width": 2200, "height": 1500}, device_scale_factor=1
                )
                page.goto((edition / "index.html").as_uri())
                page.wait_for_selector(".muvocab-reactive-graphic svg")
                page.evaluate("document.fonts.ready")
                page.locator(".muvocab-reactive-graphic").screenshot(
                    path=str(edition / "preview.png")
                )
                page.close()
                previews[language] = {
                    name: hashlib.sha256((edition / name).read_bytes()).hexdigest()
                    for name in ("index.html", "preview.png")
                }
            (ROOT / "resources/previews.json").write_text(
                json.dumps(previews, indent=2) + "\n", encoding="utf-8"
            )
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--icons-only", action="store_true")
    capture(parser.parse_args().icons_only)
