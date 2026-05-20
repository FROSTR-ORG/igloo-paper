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

This runs:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/export_from_paper.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py --strict-drift
```

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
5. Run `make igloo-paper-sync`.

## Troubleshooting

- Missing Paper MCP: reopen Paper desktop and confirm the MCP endpoint is live.
- Mapped artboard missing: update `artboard-map.json` before exporting.
- Extra live artboard: export it or classify it in `artboard-policy.json`.
- Noisy generated README: fix `export-metadata.json`, not the generated file.
- Strict drift failure: promote the token in Foundations or document current
  prototype coverage in `design/tokens/usage-coverage.json`.
