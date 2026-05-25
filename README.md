# igloo-paper

Versioned design-contract export for the `igloo-ui-shared` Paper file on the
`core` page.

This repo is reference-only. Product packages and apps must not import Paper
JSX, screenshots, generated HTML, or repo paths from here.

## Source

- Live source: Paper desktop file `igloo-ui-shared` (`01KS0ZAKQ6KF98SHDJHB6STG1K`)
- Export map: `artboard-map.json`
- Non-exported artboard policy: `artboard-policy.json`
- Design-to-implementation map: `design-contract.json`
- Generated-file inventory: `generated-manifest.json`

## Commands

From the parent workspace:

```bash
make igloo-paper-sync
make igloo-paper-sync STRICT=0
make igloo-paper-verify STRICT=1
```

From this repo:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/export_from_paper.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify.py --strict-drift
```

## Docs

- `AGENTS.md` - repo-local contributor rules
- `docs/onboarding.md` - first-read workflow
- `docs/mcp-edit-workflow.md` - live Paper Desktop edits through Paper MCP
- `docs/sync-runbook.md` - export and verification procedure
- `docs/generated-files.md` - generated artifact contract
- `docs/token-policy.md` - Foundations token and drift policy
- `docs/design-contract.md` - mapping between Paper references and implementation surfaces
