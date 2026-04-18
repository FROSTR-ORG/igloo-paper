# Environment

Environment requirements for maintaining the `igloo-paper` export.

## Dependencies

- Paper desktop with the `igloo-ui` file open on the `core` page
- Paper MCP available at `http://127.0.0.1:29979/mcp`
- Python 3.9+ for:
  - `scripts/export_from_paper.py`
  - `scripts/verify.py`

This repo has no runtime app stack, no package-manager dependency, and no secrets.

## Paper Canvas Details

- File: `igloo-ui`
- Page: `core`
- Artboard count: 69
- Shared extracted nodes: `34D-0` (`AppHeader`) and `D1D-0` (`AppFooter`)

## Verification Modes

- `python3 scripts/verify.py`
  - structural export checks
  - metadata curation checks
  - Paper reconciliation
  - drift warnings for non-Foundation colors and typography pairs
- `python3 scripts/verify.py --strict-drift`
  - same checks
  - fails on non-Foundation color drift
  - fails on non-Foundation typography pair drift
  - still fails on unsupported font families in all modes

## Output Assumptions

- The exporter regenerates README files, HTML exports, screenshots, and Foundations tokens in place.
- Deprecated screen paths from older slug naming should not remain in the working tree.
