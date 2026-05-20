# Design Contract

`design-contract.json` maps Paper references to implementation surfaces. It is a
review aid, not a runtime import surface.

## Entry Shape

Each entry has:

- `name`
- `kind`
- `status`
- `paper`
- `implementation`
- `tokens`
- `notes`

Use `implemented` for mapped implementation paths that exist, `in-progress` for
active work with existing target paths, and `planned` for design references that
do not yet have implementation files.

## Current Focus

Initial contract coverage tracks:

- app shell and header surfaces
- core UI primitives such as button, card, input, modal, and badge
- dashboard state cards
- profile, recovery, and rotation flow panels

Verification checks implementation paths for `implemented` and `in-progress`
entries so stale mappings are caught during design sync.
