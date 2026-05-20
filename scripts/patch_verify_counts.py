#!/usr/bin/env python3
"""
Update expected artboard counts in scripts/verify.py for igloo-ui-shared migration.

Sets: 31 design-system, 55 screens, 1 divider (87 mapped artboards total).
"""

from __future__ import annotations

import re
from pathlib import Path

VERIFY = Path(__file__).resolve().parent / "verify.py"

REPLACEMENTS = [
    (r"EXPECTED_DESIGN_SYSTEM_COUNT\s*=\s*\d+", "EXPECTED_DESIGN_SYSTEM_COUNT = 31"),
    (r"EXPECTED_SCREEN_COUNT\s*=\s*\d+", "EXPECTED_SCREEN_COUNT = 55"),
    (r"EXPECTED_DIVIDER_COUNT\s*=\s*\d+", "EXPECTED_DIVIDER_COUNT = 1"),
    (r"EXPECTED_ARTBOARD_COUNT\s*=\s*\d+", "EXPECTED_ARTBOARD_COUNT = 87"),
]


def main() -> None:
    if not VERIFY.exists():
        raise SystemExit(f"Missing {VERIFY}")
    text = VERIFY.read_text(encoding="utf-8")
    for pattern, replacement in REPLACEMENTS:
        text, count = re.subn(pattern, replacement, text, count=1)
        if count == 0:
            print(f"warning: pattern not found: {pattern}")
    VERIFY.write_text(text, encoding="utf-8")
    print(f"Patched counts in {VERIFY}")


if __name__ == "__main__":
    main()
