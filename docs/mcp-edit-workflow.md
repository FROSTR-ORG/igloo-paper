# Paper MCP Edit Workflow

Use this workflow when editing the live Paper Desktop canvas through an agent
chat that has access to the Paper MCP server. This complements
`docs/sync-runbook.md`, which covers exporting and verifying the canvas after
the design edit is complete. In the parent workspace, use
`dev/docs/WORKFLOWS.md#paperui-workflows` first when deciding whether the task
is Paper-only, Paper-to-UI alignment, or a dual Paper plus implementation
change.

## Prerequisites

- Paper Desktop is open to the `igloo-ui-shared` file.
- The active page is `core`.
- Paper MCP is reachable at `http://127.0.0.1:29979/mcp`.
- The parent workspace has `repos/igloo-paper` initialized.
- The edit target is either selected in Paper Desktop or named by artboard.

## Chat-Driven Edit Loop

1. State the target artboard or select the target node in Paper Desktop.
2. Ask the agent to inspect the selection or named artboard before editing.
3. The agent should use Paper MCP to inspect hierarchy, styles, and screenshots.
4. Describe the intended change in product terms, not node IDs.
5. The agent should make targeted edits in small steps:
   - update text with text-edit tools
   - move existing nodes instead of deleting and recreating them
   - duplicate existing design pieces when that preserves the local visual system
   - add new markup only when the canvas does not already contain a reusable
     pattern
6. After meaningful edits, the agent must capture a screenshot and review:
   spacing, typography, contrast, alignment, and artboard fit.
7. The agent should fix review issues before continuing.
8. When the edit is complete, the agent must release Paper working indicators.

Do not treat screenshots as implementation data. Screenshots are for visual
review. When translating Paper into code, use Paper hierarchy, JSX, computed
styles, tokens, and generated design-contract metadata.

## Sync And Verification

After the live canvas looks right, export the design contract from the parent
workspace:

```bash
make igloo-paper-sync
```

Use non-strict sync only for investigation:

```bash
make igloo-paper-sync STRICT=0
```

Then verify strict drift before treating the export as ready:

```bash
make igloo-paper-verify STRICT=1
```

If new artboards are added, update these contract files before syncing:

- `artboard-map.json` for exported artboards
- `artboard-policy.json` for live artboards that should not export
- `export-metadata.json` when generated README grouping or descriptions change
- `design-contract.json` when a Paper reference maps to an implementation
  surface

## Commit Flow

1. Commit the `repos/igloo-paper` changes first.
2. Return to the parent workspace.
3. Stage the updated `repos/igloo-paper` submodule pointer.
4. Commit the parent pointer update with any related plan/report docs.
5. Keep implementation changes in `igloo-ui`, `igloo-pwa`, or other product
   repos separate unless the design change and implementation change are being
   landed as one reviewed unit.

## Failure Modes

- Missing MCP endpoint: reopen Paper Desktop and confirm the local MCP server is
  enabled.
- Sandbox blocks localhost: rerun the MCP-dependent command with local network
  permission.
- Strict drift fails: promote the token in Foundations or document prototype
  coverage before accepting the export.
- Extra live artboard appears: export it or classify it in `artboard-policy.json`.
- Generated files look wrong: fix the Paper canvas or export metadata, then run
  sync again. Do not hand-edit generated output.
