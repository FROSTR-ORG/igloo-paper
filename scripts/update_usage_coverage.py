from __future__ import annotations

import json
from pathlib import Path

import verify


REPO_ROOT = Path(__file__).resolve().parents[1]
USAGE_COVERAGE_PATH = REPO_ROOT / "design" / "tokens" / "usage-coverage.json"
DESCRIPTION = (
    "Explicit coverage for color and typography values used by the current exported prototype "
    "outside the canonical Foundations artboard tokens. This file is intentionally checked by "
    "scripts/verify.py --strict-drift so newly introduced undocumented values still fail strict verification."
)
SAMPLE_LIMIT = 5


def canonical_foundation_colors() -> set[str]:
    colors = verify.load_json(verify.TOKEN_DIR / "colors.json")
    token_set: set[str] = set()
    for section in colors.values():
        if not isinstance(section, dict):
            continue
        for token in section.get("tokens", {}).values():
            value = token.get("value")
            if isinstance(value, str) and verify.HEX_RE.fullmatch(value):
                token_set.add(verify.normalize_hex(value))
    return token_set


def canonical_foundation_typography() -> set[tuple[str, str]]:
    typography = verify.load_json(verify.TOKEN_DIR / "typography.json")
    combos: set[tuple[str, str]] = set()
    for token in typography.get("type-scale", {}).values():
        font_size = token.get("font-size")
        line_height = token.get("line-height")
        if isinstance(font_size, str) and isinstance(line_height, str):
            combos.add((verify.normalize_px(font_size), verify.normalize_px(line_height)))
    return combos


def usage_entry(name: str, paths: set[str], **values: str) -> dict[str, object]:
    ordered_paths = sorted(paths)
    return {
        "name": name,
        **values,
        "fileCount": len(ordered_paths),
        "sampleFiles": ordered_paths[:SAMPLE_LIMIT],
    }


def build_usage_coverage() -> dict[str, object]:
    canonical_colors = canonical_foundation_colors()
    canonical_typography = canonical_foundation_typography()
    color_usage: dict[str, set[str]] = {}
    typography_usage: dict[tuple[str, str], set[str]] = {}

    for path in verify.html_targets():
        rel = path.relative_to(REPO_ROOT).as_posix()
        colors, _fonts, combos = verify.scan_html(path)
        for color in colors:
            if color not in canonical_colors:
                color_usage.setdefault(color, set()).add(rel)
        for combo in combos:
            if combo not in canonical_typography:
                typography_usage.setdefault(combo, set()).add(rel)

    return {
        "description": DESCRIPTION,
        "colors": [
            usage_entry(f"usage-color-{index:03d}", color_usage[color], value=color)
            for index, color in enumerate(sorted(color_usage), start=1)
        ],
        "typography": [
            usage_entry(
                f"usage-type-{index:03d}",
                typography_usage[combo],
                **{"font-size": combo[0], "line-height": combo[1]},
            )
            for index, combo in enumerate(sorted(typography_usage), start=1)
        ],
    }


def main() -> None:
    USAGE_COVERAGE_PATH.write_text(json.dumps(build_usage_coverage(), indent=2) + "\n")
    print(f"Updated {USAGE_COVERAGE_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
