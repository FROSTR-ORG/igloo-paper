#!/usr/bin/env python3
"""
Remap artboard-map.json paperNodeId values from a Paper get_basic_info snapshot.

Matches entries by exact artboard name (stable across file copies). Updates
paperNodeId in place; adds missing entries when --generate-missing is set.

Usage:
  python3 scripts/remap_artboard_ids.py
  python3 scripts/remap_artboard_ids.py --snapshot scripts/paper_artboards.shared.json
  python3 scripts/remap_artboard_ids.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MAP = ROOT / "artboard-map.json"
DEFAULT_SNAPSHOT = ROOT / "scripts" / "paper_artboards.shared.json"

# Design-system artboard name → repo output path (stable keys)
DS_OUTPUT_BY_NAME: dict[str, str] = {
    "Foundations": "design-system/foundations",
    "Core Components": "design-system/components/core",
    "Interactive Controls": "design-system/components/interactive-controls",
    "Data Display — Tables, Lists & Logs": "design-system/components/data-display-tables",
    "Data Display — Progress & Profile Cards": "design-system/components/data-display-progress",
    "Overlays & Feedback": "design-system/components/overlays-feedback",
    "Settings Sidebar & Lock Profile": "design-system/components/settings-sidebar",
    "Navigation & Layout": "design-system/components/navigation-layout",
    "Glossary — Core & Protocol": "design-system/glossary/core-protocol",
    "Glossary — Operations, Setup & Infrastructure": "design-system/glossary/operations-setup-infrastructure",
    "Glossary — Policies & Data Model": "design-system/glossary/policies-data-model",
    "Tooltips & Help Text — Tooltip Patterns": "design-system/tooltips-help/tooltip-patterns",
    "Tooltips & Help Text — Contextual Help": "design-system/tooltips-help/contextual-help",
    "Signer & States — Status & Empty": "design-system/patterns/signer-states-status-empty",
    "Signer & States — Recovery & Share Handling": "design-system/patterns/signer-states-recovery-share-handling",
    "Signer & States — Tags & Rotation States": "design-system/patterns/signer-states-tags-rotation",
    "Flows & QR Codes — Transfer States": "design-system/patterns/flows-qr-transfer",
    "Flows & QR Codes — Steppers & Recovery": "design-system/patterns/flows-qr-steppers",
    "Icons & Logos": "design-system/icons-logos",
    "Form Controls": "design-system/components/form-controls",
    "Pool & Signing Readiness": "design-system/patterns/pool-signing-readiness",
    "Rotate Keyset + Shared Distribution Sections": "design-system/patterns/rotate-keyset-distribution",
    "Key Lifecycle Progress Sections": "design-system/patterns/key-lifecycle-progress",
    "Data Display — Review & Summary Panels": "design-system/components/data-display-review-summary",
    "Onboard Sponsor Flow Sections": "design-system/patterns/onboard-sponsor",
    "Welcome Flow Sections": "design-system/patterns/welcome-flow",
    "Create Keyset Flow Sections": "design-system/patterns/create-keyset",
    "Onboard Flow Sections": "design-system/patterns/onboard-recipient",
    "Recover Flow Sections": "design-system/patterns/recover-flow",
    "Import Flow Sections": "design-system/patterns/import-flow",
    "Replace Share Flow Sections": "design-system/patterns/replace-share",
    "— Igloo Web App Screens —": "screens/_divider",
}

FLOW_SLUG: dict[str, str] = {
    "Welcome": "welcome",
    "Import": "import",
    "Onboard": "onboard",
    "Onboard Sponsor": "onboard-sponsor",
    "Create": "create",
    "Shared": "shared",
    "Dashboard": "dashboard",
    "Rotate Keyset": "rotate-keyset",
    "Replace Share": "replace-share",
    "Recover": "recover",
}

# Paper artboard name → stable repo outputPath when slugify() diverges from existing folders.
OUTPUT_PATH_OVERRIDES: dict[str, str] = {
    "Web — Dashboard — 1b. Loading Profile": "screens/dashboard/1b-connecting",
    "Web — Dashboard — 1b Error. Profile Load Failed": "screens/dashboard/1b-profile-load-failed",
    "Web — Dashboard — 4b. Profile Export Complete": "screens/dashboard/4b-export-complete",
}


def slugify(value: str) -> str:
    """Convert screen label text to a repo directory slug."""
    slug = value.lower()
    slug = slug.replace(".", "")
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def web_output_path(name: str) -> str | None:
    """Map a web screen artboard name to screens/<flow>/<slug>."""
    if name in OUTPUT_PATH_OVERRIDES:
        return OUTPUT_PATH_OVERRIDES[name]
    if not name.startswith("Web — "):
        return None
    body = name.removeprefix("Web — ")
    if " — " not in body:
        return None
    flow_label, screen_label = body.split(" — ", 1)
    flow = FLOW_SLUG.get(flow_label)
    if not flow:
        raise ValueError(f"Unknown web flow label: {flow_label!r} in {name!r}")
    return f"screens/{flow}/{slugify(screen_label)}"


def output_path_for_name(name: str) -> tuple[str, str | None]:
    """Return (category, outputPath) for an artboard name."""
    if name in DS_OUTPUT_BY_NAME:
        path = DS_OUTPUT_BY_NAME[name]
        if path == "screens/_divider":
            return "divider", path
        return "design-system", path
    web_path = web_output_path(name)
    if web_path:
        flow = web_path.split("/")[1]
        return "screen", web_path
    raise ValueError(f"No output mapping for artboard: {name!r}")


def load_json(path: Path) -> object:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def build_snapshot_indexes(snapshot: dict) -> tuple[dict[str, str], dict[str, str]]:
    """Build name → id and outputPath → id indexes from a Paper snapshot."""
    name_index: dict[str, str] = {}
    path_index: dict[str, str] = {}
    for artboard in snapshot.get("artboards", []):
        name = artboard["name"]
        node_id = artboard["id"]
        if name in name_index:
            raise ValueError(f"Duplicate artboard name in snapshot: {name!r}")
        name_index[name] = node_id
        try:
            category, output_path = output_path_for_name(name)
        except ValueError:
            continue
        if output_path in path_index:
            raise ValueError(f"Duplicate output path in snapshot: {output_path!r}")
        path_index[output_path] = node_id
    return name_index, path_index


def resolve_snapshot_id(
    entry: dict,
    name_index: dict[str, str],
    path_index: dict[str, str],
) -> str | None:
    """Match a map entry to a snapshot node id by outputPath, then name."""
    output_path = entry.get("outputPath")
    if output_path and output_path in path_index:
        return path_index[output_path]

    name = entry.get("name") or entry.get("paperName")
    if not name:
        return None
    if name in name_index:
        return name_index[name]

    if not name.startswith("Web — "):
        prefixed = f"Web — {name}"
        if prefixed in name_index:
            return name_index[prefixed]

    return None


def remap_entries(
    entries: list[dict],
    name_index: dict[str, str],
    path_index: dict[str, str],
    *,
    generate_missing: bool,
) -> tuple[list[dict], list[str]]:
    """Update paperNodeId on existing entries; optionally append missing boards."""
    warnings: list[str] = []
    seen_paths: set[str] = set()
    seen_names: set[str] = set()

    for entry in entries:
        name = entry.get("name") or entry.get("paperName")
        if name:
            seen_names.add(name)
        output_path = entry.get("outputPath")
        if output_path:
            seen_paths.add(output_path)

        new_id = resolve_snapshot_id(entry, name_index, path_index)
        if not new_id:
            warnings.append(f"No snapshot match for mapped entry: {name!r}")
            continue
        entry["paperNodeId"] = new_id
        entry["id"] = new_id

    if generate_missing:
        for name, node_id in sorted(name_index.items()):
            if name.startswith("Row Label"):
                continue
            try:
                category, output_path = output_path_for_name(name)
            except ValueError as exc:
                warnings.append(str(exc))
                continue
            if output_path in seen_paths or name in seen_names:
                continue
            flow = None
            if category == "screen":
                flow = output_path.split("/")[1]
            display_name = name.removeprefix("Web — ") if name.startswith("Web — ") else name
            entries.append(
                {
                    "id": node_id,
                    "paperNodeId": node_id,
                    "name": display_name,
                    "category": category,
                    "flow": flow,
                    "outputPath": output_path,
                }
            )
            seen_paths.add(output_path)
            seen_names.add(display_name)

    return entries, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Remap artboard-map.json to igloo-ui-shared node IDs")
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--generate-missing", action="store_true", help="Add map entries for snapshot artboards not in map")
    args = parser.parse_args()

    snapshot = load_json(args.snapshot)
    name_index, path_index = build_snapshot_indexes(snapshot)

    if args.map.exists():
        entries = load_json(args.map)
        if not isinstance(entries, list):
            print("artboard-map.json must be a JSON array", file=sys.stderr)
            return 1
    elif args.generate_missing:
        entries = []
    else:
        print(f"Missing {args.map}; pass --generate-missing to create from snapshot", file=sys.stderr)
        return 1

    updated, warnings = remap_entries(
        entries,
        name_index,
        path_index,
        generate_missing=args.generate_missing,
    )

    unmatched = [name for name in name_index if name not in {e.get("name") for e in updated} and not name.startswith("Row Label")]
    if unmatched:
        warnings.append(f"Snapshot artboards not in map ({len(unmatched)}): " + ", ".join(unmatched[:5]) + ("…" if len(unmatched) > 5 else ""))

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)

    ds_count = sum(1 for e in updated if e.get("category") == "design-system")
    screen_count = sum(1 for e in updated if e.get("category") == "screen")
    divider_count = sum(1 for e in updated if e.get("category") == "divider")
    print(f"Mapped {len(updated)} entries — DS: {ds_count}, screens: {screen_count}, divider: {divider_count}")

    if args.dry_run:
        return 0

    args.map.write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.map}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
