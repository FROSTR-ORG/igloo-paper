#!/usr/bin/env python3
"""
Merge scripts/export-metadata.recover-flow.patch.json into export-metadata.json.

Adds Recover Flow Sections override and recover-flow screen group; updates
paper file pointer to igloo-ui-shared.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
METADATA = ROOT / "export-metadata.json"
PATCH = ROOT / "scripts" / "export-metadata.recover-flow.patch.json"


def deep_merge(base: dict, patch: dict) -> dict:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def main() -> None:
    if not METADATA.exists():
        raise SystemExit(f"Missing {METADATA}")
    data = json.loads(METADATA.read_text(encoding="utf-8"))
    patch = json.loads(PATCH.read_text(encoding="utf-8"))
    deep_merge(data, patch)
    METADATA.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Patched {METADATA}")


if __name__ == "__main__":
    main()
