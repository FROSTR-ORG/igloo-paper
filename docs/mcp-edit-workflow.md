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
   - prefer cloning local patterns over rebuilding them; for example, clone the
     Create flow stepper into Rotate when those flows share the same structure
   - use `move_nodes` for order changes and targeted `write_html mode=replace`
     only for a contained subtree, such as replacing an expanded settings body
     with a collapsed optional row
6. After meaningful edits, the agent must capture a screenshot and review:
   spacing, typography, contrast, alignment, and artboard fit.
7. The agent should summarize the review in one concrete verdict, for example:
   `Verdict: spacing good, hierarchy intact, button contrast weak; fix primary
   CTA color before export.`
8. The agent should fix review issues before continuing.
9. When sections are deleted or collapsed, check both the artboard and the
   inner content frame for old fixed heights. If content is clipped or a large
   empty gap remains, set the affected frame or artboard height to
   `fit-content` instead of guessing a new fixed height.
10. When the edit is complete, the agent must release Paper working indicators.

Do not treat screenshots as implementation data. Screenshots are for visual
review. When translating Paper into code, use Paper hierarchy, JSX, computed
styles, tokens, and generated design-contract metadata.

## Variant States

Use the primary artboard for the default state. Add separate artboards only
when a state is materially different enough to need implementation or visual
review coverage, such as validation errors, modal states, destructive
confirmation, or an expanded configuration section with important layout
behavior.

For optional controls, prefer showing the default collapsed state on the main
screen. Represent the expanded state only when product review or implementation
needs the detailed layout. Keep the naming explicit, for example `1. Collect
Shares`, `1b. Validation Error`, or `1c. Expanded Configuration`.

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

Refresh usage coverage after changing exported artboards or token usage:

```bash
make igloo-paper-usage-coverage-sync
```

Then verify strict drift before treating the export as ready:

```bash
make igloo-paper-verify STRICT=1
```

If artboards are added, renamed, split, or deleted, update these contract files before syncing:

- `artboard-map.json` for exported artboards
- `artboard-policy.json` for live artboards that should not export
- `export-metadata.json` when generated README grouping or descriptions change
- `design-contract.json` when a Paper reference maps to an implementation
  surface
- `test/igloo-pwa/visual-manifest.json` in the parent workspace when a screen
  reference is renamed, split, deleted, or replaced by a new implementation
  capture

For renames and deletes, use this checklist before syncing:

1. Rename the live Paper artboard to the final product name.
2. Update the matching `artboard-map.json` `name` and `outputPath`.
3. Remove deleted artboards from `artboard-map.json`.
4. Remove stale artboard IDs from `export-metadata.json` README sections.
5. Remove stale artboard IDs and generated paths from `design-contract.json`.
6. Update `scripts/verify.py` expected category counts when mapped exports are
   deleted or added.
7. Update the parent visual manifest when the screen has a PWA capture or Paper
   reference.
8. Run `make igloo-paper-sync`. If export succeeds but strict drift fails, run
   `make igloo-paper-usage-coverage-sync`, then `make igloo-paper-verify
   STRICT=1`. Do not rerun export unless the canvas or metadata changed.

The exporter prunes stale files that were generated in the previous manifest.
If an old generated screen remains after sync, check whether it is still mapped
in `artboard-map.json`, still listed in `export-metadata.json` or
`design-contract.json`, or still referenced by the visual manifest.

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
- Strict drift fails after a successful export: refresh coverage with
  `make igloo-paper-usage-coverage-sync`, then run
  `make igloo-paper-verify STRICT=1`. Promote a token in Foundations only when
  the value should become canonical rather than prototype coverage.
- Extra live artboard appears: export it or classify it in `artboard-policy.json`.
- Generated files look wrong: fix the Paper canvas or export metadata, then run
  sync again. Do not hand-edit generated output.
