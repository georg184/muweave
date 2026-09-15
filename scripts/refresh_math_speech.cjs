/* Generate retained speech from the homepage's actual native MathML. */
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");
const {execFileSync} = require("node:child_process");
const {createHash} = require("node:crypto");
const sre = require("speech-rule-engine");
const root = path.resolve(__dirname, "..");

/** Generate or verify all three speech strings with the locked engine.
 * @returns {Promise<void>}
 */
async function main() {
  if (process.argv.slice(2).some(argument => argument !== "--check")) {
    throw new Error("Usage: node scripts/refresh_math_speech.cjs [--check]");
  }
  const template = fs.readFileSync(path.join(root, "src/page.html"), "utf8");
  const formulas = template.match(/<math\b[^>]*>[\s\S]*?<\/math>/g) || [];
  if (formulas.length !== 1) throw new Error("Expected one homepage MathML formula");
  const settings = {domain: "clearspeak", style: "ImpliedTimes_MoreImpliedTimes", markup: "none"};
  const inputs = {};
  for (const name of ["scripts/refresh_math_speech.cjs", "package.json", "package-lock.json"]) {
    inputs[name] = createHash("sha256").update(fs.readFileSync(path.join(root, name))).digest("hex");
  }
  const editions = {};
  const recordings = {};
  const audioBytes = {};
  const espeak = process.env.ESPEAK_NG || "espeak-ng";
  const audioVersion = execFileSync(espeak, ["--version"], {encoding: "utf8"})
    .match(/text-to-speech:\s+(\S+)/)?.[1];
  if (audioVersion !== "1.52.0") throw new Error("Audio refresh requires eSpeak NG 1.52.0");
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "muweave-speech-"));
  try {
    for (const locale of ["de", "en", "fr"]) {
      await sre.setupEngine({...settings, locale});
      await sre.engineReady();
      const text = sre.toSpeech(formulas[0]).trim();
      if (!text) throw new Error(`Empty mathematical speech for ${locale}`);
      editions[locale] = text;
      const wav = path.join(temporary, `${locale}.wav`);
      execFileSync(espeak, ["-v", locale, "-s", "145", "-w", wav, "--stdin"], {input: text});
      audioBytes[locale] = fs.readFileSync(wav);
      recordings[locale] = {
        path: `assets/audio/math-${locale}.wav`,
        sha256: createHash("sha256").update(audioBytes[locale]).digest("hex"),
      };
    }
  } finally {
    fs.rmSync(temporary, {recursive: true, force: true});
  }
  const result = JSON.stringify({
    schema_version: 1,
    generator: {name: "speech-rule-engine", version: sre.version, ...settings},
    inputs,
    mathml_sha256: createHash("sha256").update(formulas[0]).digest("hex"),
    editions,
    audio_generator: {name: "espeak-ng", version: audioVersion, words_per_minute: 145},
    recordings,
  }, null, 2) + "\n";
  const output = path.join(root, "resources/math-speech.json");
  if (process.argv.includes("--check")) {
    if (fs.readFileSync(output, "utf8") !== result) {
      throw new Error("Refresh mathematical speech with npm run refresh:math-speech");
    }
    for (const [locale, recording] of Object.entries(recordings)) {
      if (!fs.readFileSync(path.join(root, recording.path)).equals(audioBytes[locale])) {
        throw new Error(`Refresh mathematical audio for ${locale}`);
      }
    }
    console.log("Mathematical speech matches the formula and locked generator in de/en/fr.");
  } else {
    fs.mkdirSync(path.join(root, "assets/audio"), {recursive: true});
    for (const [locale, recording] of Object.entries(recordings)) {
      fs.writeFileSync(path.join(root, recording.path), audioBytes[locale]);
    }
    fs.writeFileSync(output, result);
    console.log(output);
  }
}

main().catch(error => { console.error(error.message); process.exitCode = 1; });
