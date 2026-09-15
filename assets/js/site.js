/* Language navigation, mathematical speech and static version coherence. */
"use strict";
(() => {
  const APP_VERSION = "@@VERSION@@";
  const LANGUAGES = ["de", "en", "fr"];
  const STORAGE_KEY = "muweave.homepage.language";
  const SCROLL_KEY = "muweave.homepage.language-scroll";
  const language = document.documentElement.dataset.language;
  const cssVersion = getComputedStyle(document.documentElement)
    .getPropertyValue("--site-version").trim().replaceAll('"', "");

  if (window.GG_APP_VERSION !== APP_VERSION || cssVersion !== APP_VERSION) {
    document.body.classList.add("version-mismatch");
    document.getElementById("version-error").hidden = false;
    return;
  }
  document.documentElement.classList.add("has-js");

  /** Read the optional session preference. @returns {string|null} */
  function storedLanguage() {
    try {
      const stored = sessionStorage.getItem(STORAGE_KEY);
      return LANGUAGES.includes(stored) ? stored : null;
    } catch {
      return null;
    }
  }

  /** Persist an edition without requiring storage access.
   * @param {string} selected The language represented by the destination.
   * @returns {void}
   */
  function rememberLanguage(selected) {
    try { sessionStorage.setItem(STORAGE_KEY, selected); } catch { /* Optional. */ }
  }

  /** Navigate to a translated page without following a stale section anchor.
   * @param {HTMLButtonElement} button The selected language control.
   * @param {boolean} replace Whether to replace the implicit entry history.
   * @returns {void}
   */
  function navigateLanguage(button, replace = false) {
    const target = new URL(button.dataset.href, window.location.href);
    if (replace) {
      // An implicit language redirect still honors a directly requested anchor.
      target.hash = window.location.hash;
    } else {
      target.hash = "";
      try {
        sessionStorage.setItem(SCROLL_KEY, JSON.stringify({
          href: target.href, x: window.scrollX, y: window.scrollY,
        }));
      } catch { /* Switching remains available without session storage. */ }
    }
    rememberLanguage(button.dataset.language);
    if (replace) window.location.replace(target.href);
    else window.location.assign(target.href);
  }

  const buttons = Array.from(document.querySelectorAll("button[data-language]"));
  const navigation = performance.getEntriesByType("navigation")[0];
  const explicitLanguage = new URL(window.location.href).searchParams.has("lang");
  const preferred = storedLanguage();
  if (language === "de" && !explicitLanguage && preferred && preferred !== "de"
      && navigation?.type !== "back_forward") {
    navigateLanguage(buttons.find(button => button.dataset.language === preferred), true);
    return;
  }
  rememberLanguage(language);

  /** Apply a button's explicit language choice.
   * @param {MouseEvent} event The activation from mouse, touch or keyboard.
   * @returns {void}
   */
  function onLanguageClick(event) {
    const button = event.currentTarget;
    if (button.dataset.language !== language) navigateLanguage(button);
    else rememberLanguage(language);
  }

  /** Restore a flag switch's viewport after loading, leaving history to the browser.
   * @param {PageTransitionEvent} event Whether the page came from the back/forward cache.
   * @returns {void}
   */
  function onPageShow(event) {
    rememberLanguage(language);
    if (event.persisted) return;
    try {
      const position = JSON.parse(sessionStorage.getItem(SCROLL_KEY));
      sessionStorage.removeItem(SCROLL_KEY);
      if (navigation?.type === "navigate" && position?.href === window.location.href
          && Number.isFinite(position.x) && Number.isFinite(position.y)) {
        window.scrollTo({left: position.x, top: position.y, behavior: "instant"});
      }
    } catch { /* Reading and switching never depend on optional session storage. */ }
  }

  buttons.forEach(button => button.addEventListener("click", onLanguageClick));
  window.addEventListener("pageshow", onPageShow);

  const appletFrame = document.getElementById("example-applet");
  if (appletFrame) {
    const appletStatus = document.getElementById("applet-status");
    let appletObserver = null;

    /** Present the copied worksheet's applet without its document tools.
     * The retained HTML/runtime bytes remain unchanged; only this embedded view
     * receives host-owned presentation CSS.
     * @returns {void}
     */
    function showApplet() {
      const doc = appletFrame.contentDocument;
      if (!doc || doc.URL === "about:blank") return;
      const graphic = doc.querySelector('[data-muvocab-reactive-id="kinematics:velocity-area-position"]');
      const workspace = doc.getElementById("workspace");
      if (!graphic || !workspace) {
        appletStatus.hidden = false;
        appletStatus.textContent = appletStatus.dataset.error;
        appletFrame.classList.remove("is-ready");
        return;
      }
      appletObserver?.disconnect();
      const style = doc.createElement("style");
      style.textContent = `
        :root { --document-width: max(794px, 100vw) !important; --body-font-size: clamp(10pt, 1.65vw, 13pt); }
        html, body { min-width: 0 !important; min-height: 0 !important; background: white; overflow: hidden; }
        #sidebar, #sidebar-splitter, .document-zoom-anchor,
        #pen-canvas, #pen-canvas-tiles, #drawing-ruler { display: none !important; }
        #workspace { margin: 0 !important; padding: 12px !important; min-width: 0 !important; min-height: 0 !important; }
        #document-stack { width: 100% !important; transform: none !important; zoom: 1 !important; margin: 0 !important; }
        #document { width: 100% !important; min-width: 0 !important; min-height: 0 !important; box-shadow: none !important; border: 0 !important; margin: 0 !important; padding: 0 !important; }
        .muvocab-reactive-output .muvocab-columns { grid-template-columns: minmax(440px, 1.6fr) minmax(0, 1fr) !important; }
      `;
      doc.head.append(style);
      const resize = () => {
        if (appletFrame.contentDocument !== doc) return;
        appletFrame.style.height = `${Math.ceil(workspace.getBoundingClientRect().height)}px`;
      };
      appletObserver = new appletFrame.contentWindow.ResizeObserver(resize);
      appletObserver.observe(workspace);
      doc.fonts.ready.then(resize);
      resize();
      appletStatus.hidden = true;
      appletFrame.classList.add("is-ready");
    }

    appletFrame.addEventListener("load", showApplet);
    if (appletFrame.contentDocument?.readyState === "complete") showApplet();
  }

  const speechPanel = document.getElementById("math-speech");
  if (!speechPanel) return;
  const speechButton = document.getElementById("math-speak");
  const speechLabel = speechButton.querySelector("span");
  const playIcon = speechButton.querySelector(".speech-play-icon");
  const stopIcon = speechButton.querySelector(".speech-stop-icon");
  const speechStatus = document.getElementById("math-speech-status");
  const messages = speechPanel.dataset;
  const synth = window.speechSynthesis;
  const browserSpeech = synth && typeof window.SpeechSynthesisUtterance === "function";
  const locale = document.documentElement.lang.toLowerCase();
  let voice = null;
  let activeSpeech = null; // Retain the utterance until its final event.
  let activeAudio = null;
  let preferRecording = false;
  let startTimeout = null;

  /** Restore the idle control without letting old utterance events affect a new one.
   * @param {string} message Localized completion, cancellation or failure text.
   * @returns {void}
   */
  function finishSpeech(message) {
    activeSpeech = null;
    if (activeAudio) {
      const audio = activeAudio;
      activeAudio = null;
      audio.pause();
    }
    window.clearTimeout(startTimeout);
    speechLabel.textContent = speechButton.dataset.play;
    playIcon.toggleAttribute("hidden", false);
    stopIcon.toggleAttribute("hidden", true);
    speechStatus.textContent = message;
  }

  /** Select a voice in the page's language, preferring its locale and local voices.
   * @returns {void}
   */
  function updateVoices() {
    if (!browserSpeech) return;
    const candidates = synth.getVoices().filter(candidate =>
      candidate.lang.toLowerCase().replaceAll("_", "-").split("-")[0] === language);
    voice = candidates.find(candidate => candidate.lang.toLowerCase() === locale)
      || candidates.find(candidate => candidate.localService && candidate.default)
      || candidates.find(candidate => candidate.localService)
      || candidates.find(candidate => candidate.default)
      || candidates[0] || null;
  }

  /** Play the generated local recording when browser speech is absent or fails.
   * @returns {void}
   */
  function playRecording() {
    if (activeSpeech) {
      activeSpeech = null;
      synth.cancel();
      preferRecording = true;
    }
    window.clearTimeout(startTimeout);
    const audio = new Audio(messages.audio);
    activeAudio = audio;
    audio.onplaying = () => {
      if (activeAudio !== audio) return;
      window.clearTimeout(startTimeout);
      speechStatus.textContent = messages.speaking;
    };
    audio.onended = () => {
      if (activeAudio === audio) finishSpeech(messages.ended);
    };
    audio.onerror = () => {
      if (activeAudio === audio) finishSpeech(messages.error);
    };
    startTimeout = window.setTimeout(() => {
      if (activeAudio === audio) finishSpeech(messages.error);
    }, 8000);
    audio.play().catch(() => {
      if (activeAudio === audio) finishSpeech(messages.error);
    });
  }

  /** Start on explicit activation, or cancel the currently queued/spoken formula.
   * @returns {void}
   */
  function toggleSpeech() {
    if (activeSpeech || activeAudio) {
      const wasSpeaking = Boolean(activeSpeech);
      finishSpeech(messages.stopped);
      if (wasSpeaking) synth.cancel();
      return;
    }
    updateVoices();
    speechLabel.textContent = speechButton.dataset.stop;
    playIcon.toggleAttribute("hidden", true);
    stopIcon.toggleAttribute("hidden", false);
    speechStatus.textContent = messages.starting;
    if (!voice || preferRecording) {
      playRecording();
      return;
    }
    const utterance = new SpeechSynthesisUtterance(
      document.getElementById("math-spoken").textContent.trim());
    utterance.lang = voice.lang;
    utterance.voice = voice;
    utterance.rate = 0.9;
    utterance.onstart = () => {
      if (activeSpeech !== utterance) return;
      window.clearTimeout(startTimeout);
      speechStatus.textContent = messages.speaking;
    };
    utterance.onend = () => {
      if (activeSpeech === utterance) finishSpeech(messages.ended);
    };
    utterance.onerror = event => {
      if (activeSpeech !== utterance) return;
      if (["canceled", "interrupted"].includes(event.error)) finishSpeech(messages.stopped);
      else playRecording();
    };
    activeSpeech = utterance;
    // Some browsers never emit an error when the system speech service is absent.
    startTimeout = window.setTimeout(() => {
      if (activeSpeech !== utterance) return;
      playRecording();
    }, 8000);
    try {
      synth.speak(utterance);
    } catch {
      playRecording();
    }
  }

  speechButton.addEventListener("click", toggleSpeech);
  if (browserSpeech) synth.addEventListener("voiceschanged", updateVoices);
  updateVoices();
  speechButton.disabled = false;
  window.addEventListener("focus", updateVoices);
  window.addEventListener("pagehide", () => {
    if (!activeSpeech && !activeAudio) return;
    const wasSpeaking = Boolean(activeSpeech);
    finishSpeech(messages.stopped);
    if (wasSpeaking) synth.cancel();
  });
})();
