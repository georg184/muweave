"""Verify the fixed Item 116 copy through its actual embedded controls."""

import math
from pathlib import Path

from playwright.sync_api import Page, expect


def check_applet(page: Page, root: Path, language: str) -> dict[str, object]:
    """Exercise all velocity functions, dependent bounds and the published source.

    Args:
        page: The selected homepage edition in a running browser.
        root: Homepage checkout containing the fixed source copies.
        language: Current edition, used for source and screenshot selection.
    """
    iframe = page.locator("#example-applet")
    iframe.scroll_into_view_if_needed()
    expect(iframe).to_have_class("applet-frame is-ready", timeout=30000)
    frame = page.frame_locator("#example-applet")
    child = iframe.element_handle().content_frame()
    expect(frame.locator("#sidebar")).to_be_hidden()
    expect(frame.locator(".document-zoom-anchor")).to_be_hidden()
    assert frame.locator(".muweave-shell-status").count() == 0
    assert frame.locator(".muvocab-reactive-graphic").count() == 1
    assert frame.locator("#document h1").count() == 0
    assert frame.locator("#document > .document-body > p").count() == 0
    assert frame.locator(".muvocab-reactive-output svg").count() == 2
    assert frame.locator("#document math").count() > 0
    assert frame.locator("script[src]").count() == 0
    source_name = "116.muweave" if language == "de" else f"116-{language}.muweave"
    assert page.locator(".applet-source code").text_content() == (
        root / "examples" / source_name
    ).read_text(encoding="utf-8")
    assert page.locator(".math-figure figcaption").count() == 0

    select = frame.locator('select[data-muvocab-reactive-parameter="velocity"]')
    start = frame.locator('input[data-muvocab-reactive-parameter="t_A"]')
    duration = frame.locator('input[data-muvocab-reactive-parameter="delta_t"]')
    result = frame.locator(".muvocab-computed-output-value")
    expect(select).to_have_value("2")
    expect(result).to_have_text("10")
    assert start.input_value() == "1"
    assert duration.input_value() == "3"
    initial_graph = frame.locator(".muvocab-reactive-output").inner_html()
    expected_values = (
        6,
        -6,
        10,
        3.375,
        4 * (math.sin(3) - math.sin(0.75)),
        3 - 1.6 * (math.cos(5) - math.cos(1.25)),
    )
    values = []
    for option, expected in enumerate(expected_values):
        select.select_option(str(option))
        child.wait_for_function(
            "expected => Math.abs(Number(document.querySelector('.muvocab-computed-output-value').textContent.replace('−', '-')) - expected) < 0.001",
            arg=expected,
        )
        value = float(result.inner_text().replace("−", "-"))
        assert abs(value - expected) < 0.001, (language, option, value, expected)
        values.append(value)
    assert frame.locator(".muvocab-reactive-output").inner_html() != initial_graph
    select.select_option("0")
    start.focus()
    start.press("End")
    expect(duration).to_be_disabled()
    assert start.input_value() == "9"
    assert duration.input_value() == "0"
    expect(result).to_have_text("0")
    start.press("Home")
    expect(duration).to_be_enabled()
    assert duration.input_value() == "0"
    duration.focus()
    duration.press("End")
    expect(result).to_have_text("18")

    # Restore the authored defaults for the published screenshots.
    select.select_option("2")
    start.evaluate(
        "element => { element.value = 1; element.dispatchEvent(new Event('input', {bubbles: true})); }"
    )
    duration.evaluate(
        "element => { element.value = 3; element.dispatchEvent(new Event('input', {bubbles: true})); }"
    )
    expect(result).to_have_text("10")
    page.locator(".example-section").screenshot(
        path=str(root / f"build/screenshots/applet-{language}.png")
    )
    page.evaluate("window.scrollTo(0, 0)")
    return {
        "velocity_results": values,
        "dependent_bounds": True,
        "copied_source": source_name,
    }
