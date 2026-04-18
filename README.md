# igloo-paper
Static export of the `igloo-ui` Paper file on the `core` page.

- Source of truth: the live Paper canvas
- Extraction coverage and output paths: `artboard-map.json`
- README curation, shared label ignores, and related-screen metadata: `export-metadata.json`
- Sync: `python3 scripts/export_from_paper.py`
- Verify: `python3 scripts/verify.py`
- Strict drift check: `python3 scripts/verify.py --strict-drift`

`design-system/tokens/` is generated from the Foundations artboard only. It is the canonical Foundations token set, not a whole-repo inventory of every color or type treatment used elsewhere in the exported prototype.
Current non-Foundation prototype usage is explicitly tracked in `design-system/tokens/usage-coverage.json` so strict drift checks catch newly introduced undocumented values.
