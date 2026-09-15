"""Check the speech UI at the browser API boundary without pretending to hear audio."""

import json
from pathlib import Path

from playwright.sync_api import Browser, expect

SPEECH_FAKE: str = r"""
(() => {
  class Utterance {
    constructor(text) { this.text = text; }
  }
  class Synthesis extends EventTarget {
    getVoices() { return window.speechTest.voices; }
    speak(utterance) {
      if (window.speechTest.throwOnSpeak) throw new Error('Speech service failed');
      window.speechTest.utterances.push(utterance);
    }
    cancel() {
      window.speechTest.cancels++;
      sessionStorage.setItem('test.speech.cancelled', 'yes');
    }
  }
  window.speechTest = {
    voices: [
      {name: 'Wrong default', lang: 'es-ES', default: true, localService: true},
      {name: 'Deutsch', lang: 'de-DE', localService: true},
      {name: 'English', lang: 'en-GB', localService: true},
      {name: 'Français', lang: 'fr-FR', localService: true},
    ],
    utterances: [], cancels: 0, throwOnSpeak: false,
    emit(index, event, error) {
      this.utterances[index]['on' + event]?.({error});
    },
    setVoices(voices) {
      this.voices = voices;
      speechSynthesis.dispatchEvent(new Event('voiceschanged'));
    },
  };
  Object.defineProperty(window, 'speechSynthesis', {configurable: true, value: new Synthesis()});
  Object.defineProperty(window, 'SpeechSynthesisUtterance', {configurable: true, value: Utterance});
})();
"""

AUDIO_OBSERVER: str = r"""
(() => {
  const NativeAudio = window.Audio;
  window.testAudio = [];
  window.Audio = function(url) {
    const audio = new NativeAudio(url);
    window.testAudio.push(audio);
    return audio;
  };
})();
"""


def check_speech(browser: Browser, base: str, root: Path) -> dict[str, object]:
    """Exercise language, lifecycle and unavailable-service boundaries in real DOMs.

    Args:
        browser: Running Playwright browser; synthesis alone is replaced in test contexts.
        base: Local URL serving this checkout's generated site.
        root: Website checkout containing the retained mathematical speech.
    """
    speech = json.loads((root / "resources/math-speech.json").read_text())["editions"]
    for language, suffix, voice_locale, next_language in (
        ("de", "/?lang=de", "de-DE", "en"),
        ("en", "/en/", "en-GB", "fr"),
        ("fr", "/fr/", "fr-FR", "de"),
    ):
        messages = json.loads((root / f"src/content/{language}.json").read_text())
        with browser.new_context() as context:
            context.add_init_script(SPEECH_FAKE)
            page = context.new_page()
            page.goto(base + suffix)
            page.clock.install()
            button = page.locator("#math-speak")
            status = page.locator("#math-speech-status")
            expect(button).to_be_enabled()
            assert page.evaluate("speechTest.utterances.length") == 0
            button.focus()
            page.keyboard.press("Enter")
            expect(button).to_have_text(messages["math_speech_stop"])
            expect(page.locator(".speech-stop-icon")).to_be_visible()
            expect(page.locator(".speech-play-icon")).to_be_hidden()
            assert page.evaluate(
                "({text: speechTest.utterances[0].text, lang: speechTest.utterances[0].lang})"
            ) == {"text": speech[language], "lang": voice_locale}
            page.evaluate("speechTest.emit(0, 'start')")
            expect(status).to_have_text(messages["math_speech_speaking"])
            button.click()
            expect(status).to_have_text(messages["math_speech_stopped"])
            assert page.evaluate("speechTest.cancels") == 1

            # Cancellation events may arrive after a second reading has started.
            button.click()
            page.evaluate(
                "speechTest.emit(0, 'end'); speechTest.emit(0, 'error', 'canceled')"
            )
            expect(button).to_have_text(messages["math_speech_stop"])
            page.evaluate("speechTest.emit(1, 'start'); speechTest.emit(1, 'end')")
            expect(button).to_have_text(messages["math_speech_play"])
            expect(status).to_have_text(messages["math_speech_ended"])
            expect(page.locator(".speech-play-icon")).to_be_visible()

            button.click()
            page.evaluate("sessionStorage.removeItem('test.speech.cancelled')")
            page.locator(f'button[data-language="{next_language}"]').click()
            expect(page.locator("html")).to_have_attribute(
                "data-language", next_language
            )
            assert (
                page.evaluate("sessionStorage.getItem('test.speech.cancelled')")
                == "yes"
            )
            assert page.evaluate("speechTest.utterances.length") == 0
            page.go_back()
            expect(page.locator("#math-speak")).to_have_text(
                messages["math_speech_play"]
            )

        for failure in ("error", "throw", "timeout"):
            with browser.new_context() as context:
                context.add_init_script(SPEECH_FAKE + AUDIO_OBSERVER)
                page = context.new_page()
                page.goto(base + suffix)
                page.clock.install()
                if failure == "throw":
                    page.evaluate("speechTest.throwOnSpeak = true")
                page.locator("#math-speak").click()
                if failure == "error":
                    page.evaluate(
                        "speechTest.emit(0, 'error', 'synthesis-unavailable')"
                    )
                elif failure == "timeout":
                    page.clock.fast_forward(8100)
                expect(page.locator("#math-speech-status")).to_have_text(
                    messages["math_speech_speaking"]
                )
                page.wait_for_function("testAudio[0]?.currentTime > 0")
                page.locator("#math-speak").click()
                assert page.evaluate("testAudio[0].paused")

        for unsupported in (False, True):
            with browser.new_context() as context:
                setup = (
                    "Object.defineProperty(window, 'speechSynthesis', {value: undefined});"
                    if unsupported
                    else "speechTest.voices = [];"
                )
                context.add_init_script(SPEECH_FAKE + setup + AUDIO_OBSERVER)
                page = context.new_page()
                page.goto(base + suffix)
                expect(page.locator("#math-speak")).to_be_enabled()
                expect(page.locator("#math-spoken")).to_have_text(speech[language])
                assert page.evaluate("testAudio.length") == 0
                page.locator("#math-speak").click()
                expect(page.locator("#math-speech-status")).to_have_text(
                    messages["math_speech_speaking"]
                )
                page.wait_for_function("testAudio[0]?.currentTime > 0")
                assert (
                    page.evaluate("testAudio[0].src")
                    .split("?")[0]
                    .endswith(f"math-{language}.wav")
                )
                page.locator("#math-speak").click()
                assert page.evaluate("testAudio[0].paused")
                if not unsupported:
                    # A wrong-language default is never used; late matching voices recover.
                    page.evaluate(
                        "speechTest.setVoices([{lang: 'es-ES', default: true}])"
                    )
                    page.locator("#math-speak").click()
                    expect(page.locator("#math-speech-status")).to_have_text(
                        messages["math_speech_ended"], timeout=10000
                    )
                    assert page.evaluate("speechTest.utterances.length") == 0
                    page.evaluate(
                        "lang => speechTest.setVoices([{lang}])", voice_locale
                    )
                    expect(page.locator("#math-speak")).to_be_enabled()
                    page.locator("#math-speak").click()
                    assert (
                        page.evaluate("speechTest.utterances[0].lang") == voice_locale
                    )
                else:
                    # Failed audio stays retryable; leaving the page stops a later playback.
                    page.route("**/assets/audio/*.wav*", lambda route: route.abort())
                    page.locator("#math-speak").click()
                    expect(page.locator("#math-speech-status")).to_have_text(
                        messages["math_speech_error"]
                    )
                    page.unroute("**/assets/audio/*.wav*")
                    page.locator("#math-speak").click()
                    expect(page.locator("#math-speech-status")).to_have_text(
                        messages["math_speech_speaking"]
                    )
                    page.evaluate(
                        "window.addEventListener('pagehide', () => sessionStorage.setItem('test.audio.paused', String(testAudio.every(audio => audio.paused))))"
                    )
                    page.locator(f'button[data-language="{next_language}"]').click()
                    expect(page.locator("html")).to_have_attribute(
                        "data-language", next_language
                    )
                    assert (
                        page.evaluate("sessionStorage.getItem('test.audio.paused')")
                        == "true"
                    )

    # Inspect genuine browser support separately; a fake voice is not audible evidence.
    with browser.new_context() as context:
        context.add_init_script(AUDIO_OBSERVER)
        page = context.new_page()
        page.goto(base + "/?lang=de")
        page.wait_for_timeout(2200)
        native = page.evaluate("""() => ({
          api: typeof SpeechSynthesisUtterance === 'function' && !!window.speechSynthesis,
          voices: window.speechSynthesis?.getVoices().map(voice => voice.lang) || [],
          buttonEnabled: !document.getElementById('math-speak').disabled,
          status: document.getElementById('math-speech-status').textContent,
        })""")
        page.locator(".math-section").screenshot(
            path=str(root / "build/screenshots/math-desktop.png")
        )
        page.set_viewport_size({"width": 390, "height": 844})
        page.locator(".math-section").screenshot(
            path=str(root / "build/screenshots/math-mobile.png")
        )
        assert native["buttonEnabled"]
        page.locator("#math-speak").click()
        page.wait_for_function(
            "document.getElementById('math-speech-status').textContent === document.getElementById('math-speech').dataset.speaking"
        )
        if not any(locale.lower().startswith("de") for locale in native["voices"]):
            page.wait_for_function("testAudio[0]?.currentTime > 0")
            native["recording_playback"] = page.evaluate(
                "({time: testAudio[0].currentTime, duration: testAudio[0].duration, paused: testAudio[0].paused})"
            )
        page.locator("#math-speak").click()
    return {
        "mocked_speech_languages": ["de", "en", "fr"],
        "real_audio_languages": ["de", "en", "fr"],
        "native_browser": native,
    }
