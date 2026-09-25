# Migration Notes — V1 → V2

V2 keeps the original design intent but changes the execution model.

## Major changes
- `SKILL.md` reduced from a monolithic prompt to a compact orchestration guide.
- Detailed design/copy/fact/image rules moved to `references/`.
- Slide HTML moved into `assets/templates/`.
- Added `deck.yaml` / `deck.json` structured spec and `schemas/deck.schema.json`.
- Added deterministic `scripts/render_deck.py`.
- Added Playwright-based `scripts/validate_deck.py`.
- `inline_assets.py` now handles more than `<img src>` and can strict-scan unresolved local assets.
- `export_pdf.py` now distinguishes fidelity/raster and vector/print PDF.
- Added contact-sheet generation.
- Removed hardcoded macOS-only Chrome dependency; `CHROME_PATH` remains optional.
- Product specifications are no longer treated as permanent facts embedded in the core skill.
- Japanese spacing is a house-style choice rather than a universal mandatory rule.
- Speaker script and deep Q&A are optional/full-delivery artifacts instead of mandatory outputs.

## Compatibility
Users can still ask the agent naturally for an Espressif presentation. The agent should create the Deck Spec internally and run the renderer; users do not need to write YAML themselves.
