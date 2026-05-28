# Generated Files

`generated-manifest.json` is the authoritative inventory of generated artifacts.
The exporter rewrites it during sync.

## Generated Surfaces

- `design/**/README.md`
- `design/**/reference.html`
- `design/**/screenshot.png`
- `design/glossary/*.md`
- `design/glossary/*-screenshot.png`
- `design/tokens/colors.json`
- `design/tokens/typography.json`
- `design/tokens/tokens.css`
- `screens/**/README.md`
- `screens/**/screen.html`
- `screens/**/screenshot.png`
- `screens/_shared/*.html`
- `assets/paper/*`

`design/tokens/usage-coverage.json` is policy metadata refreshed by
`make igloo-paper-usage-coverage-sync`; do not patch it by hand for routine
Paper sync drift.

## Editing Rule

Do not hand-edit generated files. Make the source change in Paper or metadata,
then run:

```bash
make igloo-paper-sync
```

Verification fails when generated files are missing from the manifest or stale
generated files remain outside it.
