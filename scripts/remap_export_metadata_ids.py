#!/usr/bin/env python3
"""
Remap node IDs in export-metadata.json using artboard-map.old.json → artboard-map.json.

Matches by stable outputPath first, then artboard name. Rewrites screen_groups
entries and artboard_overrides keys.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_MAP = ROOT / "artboard-map.old.json"
NEW_MAP = ROOT / "artboard-map.json"
METADATA = ROOT / "export-metadata.json"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def build_id_map(old_entries: list[dict], new_entries: list[dict]) -> dict[str, str]:
    new_by_path = {e["outputPath"]: e["paperNodeId"] for e in new_entries if e.get("outputPath")}
    new_by_name = {e["name"]: e["paperNodeId"] for e in new_entries}

    mapping: dict[str, str] = {}
    for entry in old_entries:
        old_id = entry["paperNodeId"]
        output_path = entry.get("outputPath")
        name = entry.get("name")
        if output_path and output_path in new_by_path:
            mapping[old_id] = new_by_path[output_path]
        elif name and name in new_by_name:
            mapping[old_id] = new_by_name[name]
        else:
            prefixed = f"Web — {name}" if name and not name.startswith("Web — ") else name
            match = next((e for e in new_entries if e.get("name") == name), None)
            if match:
                mapping[old_id] = match["paperNodeId"]
            elif prefixed:
                match = next((e for e in new_entries if e.get("name") == name), None)
                if match:
                    mapping[old_id] = match["paperNodeId"]
    return mapping


def remap_id(node_id: str, mapping: dict[str, str]) -> str:
    return mapping.get(node_id, node_id)


def main() -> None:
    old_entries = load_json(OLD_MAP)
    new_entries = load_json(NEW_MAP)
    metadata = load_json(METADATA)
    if not isinstance(metadata, dict):
        raise SystemExit("export-metadata.json must be an object")

    mapping = build_id_map(old_entries, new_entries)

    # Manual overrides for flow-section artboards renamed/replaced on copy.
    manual = {
        "1C1N-0": "B8N-0",
        "1CA3-0": "B3Y-0",
        "1CJ7-0": "AO3-0",
        "1COB-0": "AT6-0",
        "1CTF-0": "AYG-0",
        "1BUV-0": "AIH-0",
        "R49-0": "9WY-0",
        "N4P-0": "25D-0",
        "M5V-0": "HI-0",
        "QPC-0": "1DQ-0",
        "S9W-0": "AAY-0",
        "347-0": "3QR-0",
        "8B-0": "1-0",
        "ONB-0": "1QH-0",
        "OSN-0": "1SQ-0",
        "OXZ-0": "1US-0",
    }
    mapping.update(manual)

    for group in metadata.get("screen_groups", []):
        group["entries"] = [remap_id(node_id, mapping) for node_id in group["entries"]]

    overrides = metadata.get("artboard_overrides", {})
    metadata["artboard_overrides"] = {
        remap_id(key, mapping): value for key, value in overrides.items()
    }

    # Recover Flow Sections (new board)
    metadata["artboard_overrides"]["BI4-0"] = {
        "contents": [
            "Collect Shares Section",
            "Recover Success Section",
        ]
    }

    metadata["paper_file"] = {
        "name": "igloo-ui-shared",
        "id": "01KS0ZAKQ6KF98SHDJHB6STG1K",
        "page": "core",
    }

    # Add 3c unsaved modal to settings-export group if missing
    for group in metadata.get("screen_groups", []):
        if group.get("id") == "dashboard-settings-export":
            if "5O7-0" not in group["entries"]:
                group["entries"].append("5O7-0")

    METADATA.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Remapped export-metadata.json ({len(mapping)} id mappings)")


if __name__ == "__main__":
    main()
