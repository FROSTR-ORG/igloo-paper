# INSTRUCTIONS

Runbook for re-syncing `igloo-paper` from the live Paper canvas.

## Source Of Truth

- Paper desktop file: `igloo-ui`
- Page: `core`
- `artboard-map.json` defines which artboards are exported and where they land in the repo.
- `export-metadata.json` defines documentation-only curation:
  - related screen groupings
  - shared README label ignore rules
  - README contents overrides
  - README description overrides
- `design-system/tokens/` is generated from the Foundations artboard (`8B-0`) only.
- `design-system/tokens/usage-coverage.json` explicitly allowlists current non-Foundation prototype color and type usage for strict drift checks.

## Prerequisites

- Paper desktop must be open with the `igloo-ui` file on the `core` page.
- Paper MCP must be reachable at `http://127.0.0.1:29979/mcp`.
- Use Python 3.9+ from the repo root.

## Canonical Commands

```bash
python3 scripts/export_from_paper.py
python3 scripts/verify.py
python3 scripts/verify.py --strict-drift
```

`verify.py` is the default structural pass. It allows non-Foundation color and typography drift but reports it as warnings. `--strict-drift` upgrades those warnings to failures.

## Export Contract

- Non-glossary design-system directories contain `README.md`, `reference.html`, and `screenshot.png`.
- Screen directories contain `README.md`, `screen.html`, and `screenshot.png`.
- `screens/_shared/` contains `app-header.html` and `app-footer.html`.
- `assets/paper/` contains localized Paper file assets referenced by exported HTML.
- `design-system/glossary/` contains:
  - `README.md`
  - `core-protocol.md`
  - `operations-setup.md`
  - `policies-data-model.md`
  - `core-protocol-screenshot.png`
  - `operations-setup-screenshot.png`
  - `policies-data-model-screenshot.png`

## Sync Procedure

1. Confirm the Paper canvas is open and the MCP endpoint is reachable.
2. If the live Paper artboard list changed, update `artboard-map.json` first.
3. If README grouping or naming needs curation, update `export-metadata.json`.
4. Run `python3 scripts/export_from_paper.py`.
5. Run `python3 scripts/verify.py`.
6. Run `python3 scripts/verify.py --strict-drift` when you want Foundations token coverage to be enforced instead of reported.

## Canonical Screen Slugs

These renamed paths are the current canonical screen outputs and the old slugs must not remain on disk:

- `screens/welcome/1c-1-unlock-profile-modal`
- `screens/import/3-review-save-profile`
- `screens/onboard/2b-onboarding-failed`
- `screens/onboard/3-onboarding-complete`
- `screens/dashboard/1c-policies`
- `screens/dashboard/2c-signing-blocked`
- `screens/dashboard/3-settings-lock-profile`

## Verification Coverage

`scripts/verify.py` checks:

- `artboard-map.json` counts and required renamed screen paths
- required files for every exported directory
- glossary filename correctness
- shared header/footer presence
- deprecated directory absence
- Paper artboard reconciliation
- README curation overrides from `export-metadata.json`
- localized Paper asset references
- PNG screenshot file signatures
- Foundations-token drift across exported HTML

## Troubleshooting

- If Paper MCP is unavailable, re-open Paper desktop and confirm the MCP endpoint is live.
- If a mapped artboard is missing, update `artboard-map.json` before re-running the export.
- If README content looks noisy, fix the relevant entry in `export-metadata.json` instead of hand-editing generated READMEs.
- If strict drift fails, update Foundations or intentionally refresh `design-system/tokens/usage-coverage.json` so newly introduced prototype values are documented.
