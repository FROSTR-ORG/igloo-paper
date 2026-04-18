# Architecture — Igloo Paper Reference Repository

## Purpose

This repository is a static export of the Igloo Paper file. It is not a runnable product app. The repo is optimized for reference, review, and downstream implementation work.

The current export covers 69 Paper artboards:

- 24 design-system artboards
- 44 screen artboards
- 1 divider artboard

## Core Contracts

- Paper is the source of truth.
- `artboard-map.json` defines export coverage and repo paths.
- `export-metadata.json` defines documentation-only curation such as related screen groups, shared README label ignores, and README label overrides.
- `design-system/tokens/` is generated from Foundations (`8B-0`) only.
- `scripts/verify.py` is structural by default and drift-enforcing only with `--strict-drift`.

## Repository Layout

### `design-system/`

- `tokens/` contains Foundations-derived `colors.json`, `typography.json`, and `tokens.css`.
- `foundations/`, `components/`, `patterns/`, `icons-logos/`, and `tooltips-help/` each contain exported reference directories with `README.md`, `reference.html`, and `screenshot.png`.
- `glossary/` is markdown-first and contains three exported glossary docs plus uniquely named screenshots.

### `screens/`

- Each screen directory contains `README.md`, `screen.html`, and `screenshot.png`.
- `_shared/` contains extracted `app-header.html` and `app-footer.html`.
- Screen READMEs use metadata-driven `Related Screens` groups instead of linear previous/next sequencing.

## Export Flow

```text
Paper (igloo-ui / core)
  -> get_basic_info
  -> get_children / get_tree_summary
  -> get_jsx
  -> get_screenshot
  -> repo export files
```

The exporter writes structural HTML, screenshots, and generated README files. README content is mostly heuristic, then curated through `export-metadata.json`.

## Drift Model

The Foundations board defines the canonical token set currently represented in the repo. Other exported screens and component boards may still use additional colors and typography pairs that are not yet documented there.

- Default verification reports this drift as warnings.
- Strict verification treats that drift as failure.
