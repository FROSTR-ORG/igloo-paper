# Onboarding

`igloo-paper` is the design-contract checkpoint for Igloo UI work. It is not a
runtime dependency.

Start with:

1. `README.md` for the command surface.
2. `AGENTS.md` for repo-local rules.
3. `docs/sync-runbook.md` before exporting from Paper.
4. `docs/design-contract.md` before comparing Paper references with implementation.

## Local Setup

Open Paper desktop to the `igloo-ui-shared` file on the `core` page. Confirm
Paper MCP is reachable before running a sync.

Use the parent workspace wrappers:

```bash
make igloo-paper-sync
make igloo-paper-verify STRICT=1
```

These commands set `PYTHONDONTWRITEBYTECODE=1` so verification does not leave
Python cache artifacts.

## Ownership Boundary

This repo owns design reference artifacts and mapping metadata only. Component
implementation belongs in `repos/igloo-ui`; runtime and package semantics belong
in the product/runtime repos.
