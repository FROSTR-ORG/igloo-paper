# Sync Runbook

## Prerequisites

- Paper desktop is open.
- File is `igloo-ui-shared`.
- Page is `core`.
- Paper MCP is reachable at `http://127.0.0.1:29979/mcp`.
- Parent workspace submodules are initialized.

## Standard Sync

From the parent workspace:

```bash
make igloo-paper-sync
```

This runs the Paper export and strict drift verification:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/export_from_paper.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py --strict-drift
```

When token usage changes, refresh the usage coverage policy before verifying:

```bash
make igloo-paper-usage-coverage-sync
make igloo-paper-verify STRICT=1
```

If `make igloo-paper-sync` completes the export but fails strict drift with
prototype colors, typography, or unused coverage entries, do not rerun the
export immediately. Refresh usage coverage, then verify strict drift:

```bash
make igloo-paper-usage-coverage-sync
make igloo-paper-verify STRICT=1
```

Rerun `make igloo-paper-sync` only when the Paper canvas or export metadata has
changed again.

Use non-strict drift mode only when intentionally investigating new prototype
values:

```bash
make igloo-paper-sync STRICT=0
```

## When The Canvas Changes

1. Add exported artboards to `artboard-map.json`.
2. Classify live non-exported artboards in `artboard-policy.json`.
3. Update README curation in `export-metadata.json` when generated docs need
   stable grouping, naming, or descriptions.
4. Update `design-contract.json` when a design reference maps to an
   implementation surface.
5. Update the parent visual manifest when a screen is renamed, split, deleted,
   or replaced.
6. Run `make igloo-paper-sync`. The exporter removes stale generated files that
   were present in the previous manifest.

For renamed or deleted artboards, also update the `artboard-map.json`
`outputPath`, remove stale README-section entries from `export-metadata.json`,
remove stale IDs and paths from `design-contract.json`, and update
`scripts/verify.py` expected category counts when mapped exports are added or
deleted.

For collapsed or expanded UI variants, keep the default state on the primary
artboard. Add a separate artboard only when the variant needs implementation,
error-state, modal, or visual-review coverage.

## Troubleshooting

- Missing Paper MCP: reopen Paper desktop and confirm the MCP endpoint is live.
- Mapped artboard missing: update `artboard-map.json` before exporting.
- Extra live artboard: export it or classify it in `artboard-policy.json`.
- Noisy generated README: fix `export-metadata.json`, not the generated file.
- Strict drift failure after export: refresh current prototype coverage with
  `make igloo-paper-usage-coverage-sync`, then run
  `make igloo-paper-verify STRICT=1`; promote a token in Foundations only when
  the value should be canonical.
