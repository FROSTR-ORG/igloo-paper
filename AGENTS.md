# Repository Guidelines

## Role

`igloo-paper` is a static, versioned design-contract repository for the live
Paper file. It stores generated reference material and metadata used to compare
Paper design intent with implementation work.

Do not add runtime package code, app build dependencies, or imports from this
repo into `igloo-ui`, `igloo-shared`, or host apps.

## Source Of Truth

- Paper desktop file: `igloo-ui-shared` (`01KS0ZAKQ6KF98SHDJHB6STG1K`)
- Page: `core`
- Exported artboards: `artboard-map.json`
- Classified non-exported live artboards: `artboard-policy.json`
- README curation and related-screen metadata: `export-metadata.json`
- Implementation mapping: `design-contract.json`
- Generated artifacts: `generated-manifest.json`

## Commands

Use the parent workspace command surface when possible:

```bash
make igloo-paper-sync
make igloo-paper-sync STRICT=0
make igloo-paper-verify STRICT=1
```

Local equivalents:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/export_from_paper.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py --strict-drift
```

`STRICT=1` is the default parent behavior. It treats undocumented color and
typography drift as a failure.

## Generated Files

Generated export material lives under:

- `design/`
- `screens/`
- `assets/paper/`

Do not hand-edit generated READMEs, screenshots, HTML, glossary markdown, token
outputs, or localized Paper assets. Change the Paper canvas, `artboard-map.json`,
or `export-metadata.json`, then re-run the sync command.

Scratch and staging output belongs under `tmp/` in this repo or parent
`./.tmp/`. Public commands must not leave `__pycache__`, `.pyc`, temp, or
partial-export artifacts behind.

## Verification Expectations

`scripts/verify.py` checks:

- exported files and PNG signatures
- generated-manifest coverage
- README curation
- localized Paper assets
- live Paper reconciliation
- non-exported artboard classification
- design-contract path validity
- Foundations token drift
- absence of hard-cut legacy files and paths

See `docs/sync-runbook.md` for the full procedure.
