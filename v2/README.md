# Espressif Deck Generator V2

A Gemini/Agent Skill for generating consistent Espressif-style HTML/Web presentations with a structured Deck Spec, deterministic renderer and browser validation.

## Install / replace

The skill directory name should be `espressif-deck-generator` and must contain `SKILL.md` at its root. Gemini CLI currently discovers user skills under `~/.gemini/skills/` or `~/.agents/skills/`, and workspace skills under `.gemini/skills/` / `.agents/skills/`.

Typical replacement:
```bash
rm -rf ~/.gemini/skills/espressif-deck-generator
cp -R espressif-deck-generator ~/.gemini/skills/
```
Then reload/list skills in Gemini CLI.

## Render
```bash
uv run --with pyyaml python scripts/render_deck.py examples/lightning-talk.yaml -o output/deck.html
```
JSON input does not require PyYAML.

## Validate
```bash
uv run --with playwright python scripts/validate_deck.py output/deck.html --report output/validation-report.json
```
If Chromium is not installed for Playwright, install it in the environment first (for example `playwright install chromium`).

## Standalone
```bash
python3 scripts/inline_assets.py output/deck.html -o output/deck_standalone.html --strict
```
The renderer already embeds the skill CSS/JS into generated HTML. This packager additionally embeds project-local images, SVG, fonts/background references, local stylesheets and scripts.

## PDF
Fidelity/raster PDF:
```bash
uv run --with playwright --with reportlab python scripts/export_pdf.py output/deck.html --mode fidelity -o output/deck_fidelity.pdf
```

Vector/print PDF:
```bash
uv run --with playwright python scripts/export_pdf.py output/deck.html --mode vector -o output/deck_vector.pdf
```

Set `CHROME_PATH` only when you deliberately want a system Chrome executable. Otherwise Playwright Chromium is used.

## Contact sheet
```bash
uv run --with playwright --with pillow python scripts/make_contact_sheet.py output/deck.html -o output/deck_contact_sheet.png
```

## Architecture
```text
User request
   ↓
research / fact verification
   ↓
storyboard
   ↓
deck.yaml / deck.json
   ↓
render_deck.py
   ↓
deck.html
   ↓
validate_deck.py
   ↓
standalone / PDF / contact sheet
```

## Notes
- Example product values are layout placeholders, not authoritative product specifications.
- Use `references/fact-checking.md` for current technical claims.
- Prefer editing the Deck Spec or reusable components instead of patching the final HTML with one-off inline CSS.
