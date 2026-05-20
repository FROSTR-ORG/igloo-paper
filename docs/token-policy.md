# Token Policy

Foundations is the canonical source for Igloo Paper tokens.

Generated token outputs:

- `design/tokens/colors.json`
- `design/tokens/typography.json`
- `design/tokens/tokens.css`

Hand-maintained drift policy:

- `design/tokens/usage-coverage.json`

## Promotion Rule

Promote reusable colors or typography to Foundations first. Do not normalize
drift by editing generated HTML.

Use `usage-coverage.json` only to document current non-Foundation prototype
usage that is intentionally tolerated while implementation catches up.

## Strict Drift

`make igloo-paper-sync` and `make igloo-paper-verify STRICT=1` fail on
undocumented color or typography drift. `STRICT=0` prints drift warnings for
investigation but should not be used as the final validation mode.
