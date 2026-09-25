# Espressif Deck Generator Skill

A versioned archive of the Espressif presentation/deck generation skill.

## Versions

- `v1/` — original skill as provided, with only generated macOS/cache artifacts removed.
- `v2/` — refactored skill with a smaller core `SKILL.md`, structured deck spec, deterministic renderer, validation, improved standalone export, PDF modes, and examples.

## Recommended version

Use **v2** for new work. Keep **v1** as the original baseline/reference.

## Installation

Copy the selected version's contents into your Agent Skills directory as `espressif-deck-generator`.

For Gemini CLI, a typical user-level location is:

```text
~/.gemini/skills/espressif-deck-generator/
```

Then reload skills in Gemini CLI.

## Repository layout

```text
.
├── v1/
│   ├── SKILL.md
│   └── scripts/
└── v2/
    ├── SKILL.md
    ├── README.md
    ├── MIGRATION_V2.md
    ├── references/
    ├── schemas/
    ├── assets/
    ├── scripts/
    └── examples/
```

## Notes

Technical product specifications can change. The v2 skill is designed to re-verify important product facts from official sources rather than treating examples as permanent truth.
