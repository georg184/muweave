/* Language navigation and mixed-version detection for the static site. */
"use strict";
(() => {
  const APP_VERSION = "@@VERSION@@";
  const LANGUAGES = ["de", "en", "fr"];
  const STORAGE_KEY = "muweave.homepage.language";
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

  /** Navigate to a translated static page while preserving the section.
   * @param {HTMLButtonElement} button The selected language control.
   * @param {boolean} replace Whether to replace the implicit entry history.
   * @returns {void}
   */
  function navigateLanguage(button, replace = false) {
    const target = new URL(button.dataset.href, window.location.href);
    target.hash = window.location.hash;
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

  /** Restore session preference after back/forward cache restoration.
   * @returns {void}
   */
  function onPageShow() { rememberLanguage(language); }

  buttons.forEach(button => button.addEventListener("click", onLanguageClick));
  window.addEventListener("pageshow", onPageShow);
})();
