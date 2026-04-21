from __future__ import annotations

import argparse
import base64
import html
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from paper_mcp import PaperClient


REPO_ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = REPO_ROOT / "artboard-map.json"
METADATA_PATH = REPO_ROOT / "export-metadata.json"
TOKEN_DIR = REPO_ROOT / "design-system" / "tokens"
GLOSSARY_DIR = REPO_ROOT / "design-system" / "glossary"
ASSET_DIR = REPO_ROOT / "assets" / "paper"
FOUNDATIONS_ID = "8B-0"
SHARED_COMPONENTS = {
    "app-header.html": "WA9-0",
    "app-footer.html": "D1D-0",
}
GLOSSARY_FILES = {
    "ONB-0": ("core-protocol.md", "core-protocol-screenshot.png"),
    "OSN-0": ("operations-setup.md", "operations-setup-screenshot.png"),
    "OXZ-0": ("policies-data-model.md", "policies-data-model-screenshot.png"),
}
FOUNDATION_COLOR_SECTIONS = [
    ("Color Palette Section", "Background Colors", "background-colors"),
    ("Blue Scale Section", "Blue Scale — Primary", "blue-scale-primary"),
    ("Semantic Colors Section", "Semantic Colors", "semantic-colors"),
    ("Interface Text Tones Section", "Interface Text Tones", "interface-text-tones"),
    ("Interface Borders & Overlays Section", "Interface Borders & Overlays", "interface-borders-overlays"),
]
CANONICAL_FONT_STACKS = {
    "Inter": '"Inter", system-ui, sans-serif',
    "Share Tech Mono": '"Share Tech Mono", system-ui, sans-serif',
}
CANONICAL_INTER_FONT_CLASS = "font-['Inter',system-ui,sans-serif]"
CANONICAL_MONO_FONT_CLASS = "font-['Share_Tech_Mono',system-ui,sans-serif]"
DEPRECATED_MONO_FONT_FAMILIES = {"paper mono preview", "paper mono", "ibm plex mono", "roboto mono"}
DEPRECATED_SANS_FONT_FAMILIES = {"matter", "inter tight", "system sans-serif", "noto sans", "archivo black"}
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?$")
PAPER_ASSET_RE = re.compile(r"https://app\.paper\.design/file-assets/[A-Za-z0-9]+/[A-Za-z0-9_.-]+")
ARBITRARY_FONT_RE = re.compile(r"font-\[([^\]]+)\]")
APP_FOOTER_CLASS_RE = re.compile(r'<div className="([^"]*border-t border-t-solid border-t-\[#1E3A8A33\][^"]*)">')
STRUCTURAL_LABELS = {"Header", "Frame", "Rectangle", "SVG", "Section Label"}
CANONICAL_APP_FOOTER_CLASS = (
    "flex flex-col items-center w-full shrink-0 py-5 mt-auto justify-start "
    "static h-0 border-t border-t-solid border-t-[#1E3A8A33]"
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def load_map() -> list[dict[str, Any]]:
    return load_json(MAP_PATH)


def load_metadata() -> dict[str, Any]:
    return load_json(METADATA_PATH)


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "section"


def normalize_hex(value: str | None) -> str:
    if not value:
        return ""
    return value.strip().upper()


def decode_text_segments(jsx: str) -> list[str]:
    matches = re.findall(r">([^<>]+)<", jsx)
    cleaned: list[str] = []
    for match in matches:
        text = html.unescape(" ".join(match.split())).strip()
        if text and text not in cleaned:
            cleaned.append(text)
    return cleaned


def parse_summary(summary: str) -> tuple[list[str], list[str]]:
    top_level: list[str] = []
    text_snippets: list[str] = []

    for line in summary.splitlines()[1:]:
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        match = re.search(r'"([^"]+)"', stripped)
        if indent == 2 and match:
            name = match.group(1).strip()
            if name and name not in top_level:
                top_level.append(name)
        text_match = re.search(r'Text "[^"]+" \([^)]+\) [^"]* "([^"]+)"', stripped)
        if text_match:
            value = text_match.group(1).replace("…", "...").strip()
            if value and value not in text_snippets:
                text_snippets.append(value)

    return top_level[:12], text_snippets[:12]


def state_label(name: str) -> str:
    if " — " not in name:
        return name
    return name.split(" — ", 1)[1]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n")


def write_png(path: Path, mime_type: str, encoded: str) -> None:
    if mime_type != "image/png":
        raise SystemExit(f"Expected Paper screenshot as image/png for {path.relative_to(REPO_ROOT)}, got {mime_type}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(encoded))


def local_asset_path(url: str) -> Path:
    filename = Path(urllib.parse.urlparse(url).path).name
    if not filename:
        raise SystemExit(f"Paper asset URL has no filename: {url}")
    target = ASSET_DIR / filename
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(url, headers={"User-Agent": "igloo-paper-export/0.1"})
        with urllib.request.urlopen(request, timeout=60) as response:
            target.write_bytes(response.read())
    return target


def localize_asset_urls(jsx: str, output_dir: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        target = local_asset_path(match.group(0))
        return Path(os.path.relpath(target, output_dir)).as_posix()

    return PAPER_ASSET_RE.sub(replace, jsx)


def primary_font_family(raw_font_class: str) -> str:
    primary = raw_font_class.split(",", 1)[0].strip().strip("'\"")
    return " ".join(primary.replace("_", " ").split()).lower()


def canonicalize_font_classes(jsx: str) -> str:
    def replace(match: re.Match[str]) -> str:
        primary = primary_font_family(match.group(1))
        if primary in DEPRECATED_MONO_FONT_FAMILIES:
            return CANONICAL_MONO_FONT_CLASS
        if primary in DEPRECATED_SANS_FONT_FAMILIES:
            return CANONICAL_INTER_FONT_CLASS
        return match.group(0)

    return ARBITRARY_FONT_RE.sub(replace, jsx)


def canonicalize_app_footer_contract(jsx: str) -> str:
    def replace_footer(match: re.Match[str]) -> str:
        tokens = set(match.group(1).split())
        if "mt-auto" not in tokens:
            return match.group(0)
        return f'<div className="{CANONICAL_APP_FOOTER_CLASS}">'

    jsx = APP_FOOTER_CLASS_RE.sub(replace_footer, jsx)
    canonical_root = re.escape(f'<div className="{CANONICAL_APP_FOOTER_CLASS}">')
    icon_row_re = re.compile(rf'({canonical_root}\n\s*)<div className="[^"]*">')
    return icon_row_re.sub(r'\1<div className="flex items-center gap-5">', jsx)


def node_info(client: PaperClient, node_id: str) -> dict[str, Any]:
    return client.get_node_info(node_id)


def node_children(client: PaperClient, node_id: str) -> list[dict[str, Any]]:
    return client.get_children(node_id)["children"]


def node_text(client: PaperClient, node_id: str) -> str:
    info = node_info(client, node_id)
    return (info.get("textContent") or info.get("name") or "").strip()


def clean_contents(artboard_id: str, items: list[str], metadata: dict[str, Any]) -> list[str]:
    override = metadata.get("artboard_overrides", {}).get(artboard_id, {})
    global_ignores = set(metadata.get("global_ignore_contents", [])) or STRUCTURAL_LABELS
    ignored = global_ignores | set(override.get("ignore_contents", []))
    renamed = override.get("rename_contents", {})

    if "contents" in override:
        return list(override["contents"])

    cleaned: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item in ignored:
            continue
        name = renamed.get(item, item)
        if not name or name in ignored or name in seen:
            continue
        seen.add(name)
        cleaned.append(name)
    return cleaned[:8]


def related_screens(
    artboard_id: str,
    entries_by_id: dict[str, dict[str, Any]],
    metadata: dict[str, Any],
) -> list[tuple[str, list[dict[str, str]]]]:
    groups: list[tuple[str, list[dict[str, str]]]] = []
    for group in metadata.get("screen_groups", []):
        if artboard_id not in group["entries"]:
            continue
        related: list[dict[str, str]] = []
        for other_id in group["entries"]:
            if other_id == artboard_id:
                continue
            other = entries_by_id.get(other_id)
            if other is None:
                continue
            related.append(
                {
                    "name": other["name"],
                    "path": f"{other['outputPath']}/README.md",
                }
            )
        if related:
            groups.append((group["title"], related))
    return groups


def make_design_readme(
    entry: dict[str, Any],
    artboard: dict[str, Any],
    summary: str,
    metadata: dict[str, Any],
) -> str:
    sections, snippets = parse_summary(summary)
    contents = clean_contents(entry["paperNodeId"], sections, metadata)
    override = metadata.get("artboard_overrides", {}).get(entry["paperNodeId"], {})
    description = override.get("description")
    if not description:
        description_bits = ", ".join(contents[:3]) if contents else "the current reusable layout and states"
        description = (
            f"This artboard documents the current Paper reference for {entry['name']}. "
            f"The synced export covers {description_bits} used across the Igloo design system."
        )

    lines = [
        f"# {entry['name']}",
        "",
        "## Description",
        description,
        "",
        "## Paper Source",
        f"- **Artboard ID:** {entry['paperNodeId']}",
        f"- **Artboard Name:** {artboard['name']}",
        f"- **Dimensions:** {artboard['width']} × {artboard['height']}",
        "",
        "## Contents",
    ]
    if contents:
        lines.extend(f"- **{name}**" for name in contents)
    else:
        lines.append("- Structural sections are available in `reference.html`.")

    if snippets:
        lines.extend(["", "## Representative Copy"])
        lines.extend(f"- {snippet}" for snippet in snippets[:6])

    lines.extend(
        [
            "",
            "## Files",
            "- `reference.html` — Tailwind-flavored Paper JSX export for the artboard.",
            "- `screenshot.png` — Screenshot exported from the current Paper canvas.",
        ]
    )
    return "\n".join(lines)


def make_screen_readme(
    entry: dict[str, Any],
    artboard: dict[str, Any],
    summary: str,
    metadata: dict[str, Any],
    entries_by_id: dict[str, dict[str, Any]],
) -> str:
    regions, snippets = parse_summary(summary)
    contents = clean_contents(entry["paperNodeId"], regions, metadata)
    groups = related_screens(entry["paperNodeId"], entries_by_id, metadata)

    lines = [
        f"# {entry['name']}",
        "",
        "## Description",
        f'This screen captures the `{entry["flow"]}` flow state "{state_label(entry["name"])}" in the current Igloo web prototype.',
        "",
        "## Paper Source",
        f"- **Artboard ID:** {entry['paperNodeId']}",
        f"- **Artboard Name:** {artboard['name']}",
        f"- **Dimensions:** {artboard['width']} × {artboard['height']}",
        "",
        "## Flow Context",
        f"- **Flow:** `{entry['flow']}`",
        f"- **State:** `{state_label(entry['name'])}`",
        "",
        "## Key Regions",
    ]
    if contents:
        lines.extend(f"- **{region}**" for region in contents)
    else:
        lines.append("- The full structure is available in `screen.html`.")

    if groups:
        lines.extend(["", "## Related Screens"])
        for title, related in groups:
            lines.extend(["", f"### {title}"])
            lines.extend(f"- {item['name']} — `{item['path']}`" for item in related)

    if snippets:
        lines.extend(["", "## Representative Copy"])
        lines.extend(f"- {snippet}" for snippet in snippets[:6])

    lines.extend(
        [
            "",
            "## Files",
            "- `screen.html` — Tailwind-flavored Paper JSX export for the screen.",
            "- `screenshot.png` — Screenshot exported from the current Paper canvas.",
        ]
    )
    return "\n".join(lines)


def parse_glossary(
    jsx: str,
    summary: str,
    title: str,
    artboard: dict[str, Any],
    artboard_id: str,
    metadata: dict[str, Any],
) -> str:
    ignored = set(metadata.get("global_ignore_contents", [])) or STRUCTURAL_LABELS
    section_names, _ = parse_summary(summary)
    section_names = [name for name in section_names if name not in ignored]
    text_items = decode_text_segments(jsx)

    current_section: str | None = None
    grouped: list[tuple[str, list[str]]] = []
    bucket: list[str] = []
    started = False

    for item in text_items:
        if item in section_names:
            if current_section is not None:
                grouped.append((current_section, bucket))
            current_section = item
            bucket = []
            started = True
            continue
        if started and current_section is not None:
            bucket.append(item)

    if current_section is not None:
        grouped.append((current_section, bucket))

    lines = [
        f"# {title}",
        "",
        "Derived from the current Paper glossary artboard export.",
        "",
        "## Paper Source",
        f"- **Artboard ID:** {artboard_id}",
        f"- **Artboard Name:** {artboard['name']}",
        f"- **Dimensions:** {artboard['width']} × {artboard['height']}",
    ]

    for section_name, items in grouped:
        lines.extend(["", f"## {section_name}"])
        for index in range(0, len(items), 2):
            term = items[index]
            description = items[index + 1] if index + 1 < len(items) else ""
            lines.extend(["", f"### {term}", description])

    return "\n".join(lines).strip() + "\n"


def glossary_readme() -> str:
    return "\n".join(
        [
            "# Glossary",
            "",
            "This directory contains the three glossary artboards exported from the current Paper canvas as markdown reference documents plus matching screenshots.",
            "",
            "## Files",
            "- `core-protocol.md` and `core-protocol-screenshot.png`",
            "- `operations-setup.md` and `operations-setup-screenshot.png`",
            "- `policies-data-model.md` and `policies-data-model-screenshot.png`",
        ]
    )


def parse_weight(note: str, fallback: Any) -> int:
    lowered = note.lower()
    if "semibold" in lowered:
        return 600
    if "bold" in lowered:
        return 700
    if isinstance(fallback, int):
        return fallback
    return 400


def primary_family_name(stack: str) -> str:
    first = stack.split(",", 1)[0].strip()
    return first.strip("'\"")


def canonical_family_name(name: str) -> str:
    normalized = " ".join(name.replace("_", " ").split()).lower()
    for canonical in CANONICAL_FONT_STACKS:
        if normalized == canonical.lower():
            return canonical
    raise SystemExit(f"Unsupported Foundations typography family: {name}")


def extract_color_section(client: PaperClient, content_id: str) -> dict[str, dict[str, str]]:
    rows = node_children(client, content_id)
    row_infos = [node_info(client, row["id"]) for row in rows]
    swatch_ids = [info["childIds"][0] for info in row_infos if info.get("childIds")]
    swatch_styles = client.get_computed_styles(swatch_ids) if swatch_ids else {}
    tokens: dict[str, dict[str, str]] = {}

    for info in row_infos:
        child_ids = info.get("childIds", [])
        if len(child_ids) < 2:
            continue
        swatch_id, label_id = child_ids[:2]
        label = node_text(client, label_id)
        value = normalize_hex(swatch_styles.get(swatch_id, {}).get("backgroundColor"))
        if not label or not value:
            continue
        token: dict[str, str] = {"value": value}
        if len(child_ids) > 2:
            third_text = node_text(client, child_ids[2])
            if third_text and not HEX_RE.fullmatch(normalize_hex(third_text)):
                token["description"] = third_text
        tokens[label] = token

    return tokens


def extract_colors(client: PaperClient, section_ids: dict[str, str]) -> dict[str, Any]:
    colors: dict[str, Any] = {}

    for frame_name, title, key in FOUNDATION_COLOR_SECTIONS:
        section_id = section_ids[frame_name]
        content_id = node_children(client, section_id)[1]["id"]
        colors[key] = {
            "title": title,
            "tokens": extract_color_section(client, content_id),
        }

    typography_status_children = node_children(client, section_ids["Typography & Status"])
    status_section_id = next(child["id"] for child in typography_status_children if child["name"] == "Status Colors")
    status_content_id = node_children(client, status_section_id)[1]["id"]
    colors["status"] = {
        "title": "Status",
        "tokens": extract_color_section(client, status_content_id),
    }
    return colors


def extract_typography(client: PaperClient, section_ids: dict[str, str]) -> dict[str, Any]:
    typography_status_children = node_children(client, section_ids["Typography & Status"])
    typography_section_id = next(child["id"] for child in typography_status_children if child["name"] == "Typography Scale")
    typography_children = node_children(client, typography_section_id)
    rows_container_id = next(child["id"] for child in typography_children if child["name"] == "Frame")
    rows = node_children(client, rows_container_id)
    row_infos = [node_info(client, row["id"]) for row in rows]
    sample_ids = [info["childIds"][0] for info in row_infos if len(info.get("childIds", [])) >= 2]
    sample_styles = client.get_computed_styles(sample_ids) if sample_ids else {}

    font_families: dict[str, Any] = {}
    type_scale: dict[str, Any] = {}

    for info in row_infos:
        child_ids = info.get("childIds", [])
        if len(child_ids) < 2:
            continue
        sample_id, note_id = child_ids[:2]
        sample = node_text(client, sample_id)
        note = node_text(client, note_id)
        style = sample_styles.get(sample_id, {})
        label = sample.split(" — ", 1)[0].strip()

        if info["name"] == "Secondary Mono Row":
            continue

        raw_family_name = note.split(" / ", 1)[0].strip() if " / " in note else primary_family_name(style.get("fontFamily", ""))
        family_name = canonical_family_name(raw_family_name)
        if family_name and family_name not in font_families:
            font_families[family_name] = {
                "stack": CANONICAL_FONT_STACKS[family_name],
                "usage": note,
            }

        token: dict[str, Any] = {
            "sample": sample,
            "font-family": family_name,
            "font-size": style.get("fontSize"),
            "line-height": style.get("lineHeight"),
            "font-weight": parse_weight(note, style.get("fontWeight")),
            "notes": note,
        }
        if style.get("letterSpacing"):
            token["letter-spacing"] = style["letterSpacing"]
        if "canonical" in note.lower():
            token["canonical"] = True
        type_scale[label] = {key: value for key, value in token.items() if value not in ("", None)}

    return {
        "font-families": font_families,
        "type-scale": type_scale,
    }


def render_tokens_css(colors: dict[str, Any], typography: dict[str, Any]) -> str:
    lines = [
        "/*",
        " * Igloo Design Tokens",
        ' * Extracted from Paper canvas "igloo-ui" -> Foundations artboard (8B-0) only.',
        " * This file is regenerated from the Foundations board and intentionally does not inventory",
        " * every color or type treatment used elsewhere in the prototype.",
        " */",
        "",
        ":root {",
    ]

    seen_color_vars: dict[str, str] = {}
    for section_key, section in colors.items():
        lines.append(f"  /* {section['title']} */")
        prefix = "status-" if section_key == "status" else ""
        for label, token in section["tokens"].items():
            var_name = f"--color-{prefix}{slugify(label)}"
            value = token["value"]
            if seen_color_vars.get(var_name) == value:
                continue
            seen_color_vars[var_name] = value
            lines.append(f"  {var_name}: {value};")
        lines.append("")

    lines.append("  /* Font families */")
    for family_name, token in typography["font-families"].items():
        lines.append(f"  --font-{slugify(family_name)}: {token['stack']};")
    lines.append("")

    lines.append("  /* Type scale */")
    for label, token in typography["type-scale"].items():
        prefix = f"--text-{slugify(label)}"
        family_name = token.get("font-family")
        if family_name:
            lines.append(f"  {prefix}-font-family: var(--font-{slugify(family_name)});")
        if token.get("font-size"):
            lines.append(f"  {prefix}-size: {token['font-size']};")
        if token.get("line-height"):
            lines.append(f"  {prefix}-line-height: {token['line-height']};")
        if token.get("font-weight") is not None:
            lines.append(f"  {prefix}-weight: {token['font-weight']};")
        if token.get("letter-spacing"):
            lines.append(f"  {prefix}-tracking: {token['letter-spacing']};")
    lines.append("}")
    return "\n".join(lines)


def export_token_files(client: PaperClient) -> None:
    section_ids = {child["name"]: child["id"] for child in node_children(client, FOUNDATIONS_ID)}
    colors = extract_colors(client, section_ids)
    typography = extract_typography(client, section_ids)
    css = render_tokens_css(colors, typography)
    write_json(TOKEN_DIR / "colors.json", colors)
    write_json(TOKEN_DIR / "typography.json", typography)
    write_text(TOKEN_DIR / "tokens.css", css)


def export_shared_components(client: PaperClient) -> None:
    shared_dir = REPO_ROOT / "screens" / "_shared"
    shared_dir.mkdir(parents=True, exist_ok=True)
    for filename, node_id in SHARED_COMPONENTS.items():
        jsx = canonicalize_app_footer_contract(canonicalize_font_classes(client.get_jsx(node_id)))
        write_text(shared_dir / filename, localize_asset_urls(jsx, shared_dir))


def export_glossary_entry(
    client: PaperClient,
    entry: dict[str, Any],
    artboard: dict[str, Any],
    metadata: dict[str, Any],
) -> None:
    paper_id = entry["paperNodeId"]
    summary = client.get_tree_summary(paper_id, depth=8)
    jsx = client.get_jsx(paper_id)
    mime_type, encoded = client.get_screenshot(paper_id)
    markdown_name, screenshot_name = GLOSSARY_FILES[paper_id]
    title = {
        "ONB-0": "Core & Protocol Glossary",
        "OSN-0": "Operations, Setup & Infrastructure Glossary",
        "OXZ-0": "Policies & Data Model Glossary",
    }[paper_id]
    write_text(GLOSSARY_DIR / markdown_name, parse_glossary(jsx, summary, title, artboard, paper_id, metadata))
    write_png(GLOSSARY_DIR / screenshot_name, mime_type, encoded)


def export_standard_entry(
    client: PaperClient,
    entry: dict[str, Any],
    artboard: dict[str, Any],
    metadata: dict[str, Any],
    entries_by_id: dict[str, dict[str, Any]],
) -> None:
    paper_id = entry["paperNodeId"]
    summary = client.get_tree_summary(paper_id, depth=5)
    jsx = canonicalize_app_footer_contract(canonicalize_font_classes(client.get_jsx(paper_id)))
    mime_type, encoded = client.get_screenshot(paper_id)
    output_dir = REPO_ROOT / entry["outputPath"]
    output_dir.mkdir(parents=True, exist_ok=True)
    jsx = localize_asset_urls(jsx, output_dir)

    if entry["category"] == "screen":
        write_text(output_dir / "screen.html", jsx)
        write_text(output_dir / "README.md", make_screen_readme(entry, artboard, summary, metadata, entries_by_id))
    else:
        write_text(output_dir / "reference.html", jsx)
        write_text(output_dir / "README.md", make_design_readme(entry, artboard, summary, metadata))
    write_png(output_dir / "screenshot.png", mime_type, encoded)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export igloo-paper artifacts from the Paper canvas.")
    parser.parse_args()

    entries = load_map()
    metadata = load_metadata()
    entries_by_id = {entry["paperNodeId"]: entry for entry in entries if entry["category"] != "divider"}

    client = PaperClient()
    client.initialize()
    basic_info = client.get_basic_info()
    artboards = {artboard["id"]: artboard for artboard in basic_info["artboards"]}

    export_token_files(client)
    export_shared_components(client)

    for entry in entries:
        if entry["category"] == "divider":
            continue
        paper_id = entry["paperNodeId"]
        artboard = artboards.get(paper_id)
        if artboard is None:
            raise SystemExit(f"Mapped artboard not present in Paper: {paper_id} {entry['name']}")

        if paper_id in GLOSSARY_FILES:
            export_glossary_entry(client, entry, artboard, metadata)
        else:
            export_standard_entry(client, entry, artboard, metadata, entries_by_id)

    write_text(GLOSSARY_DIR / "README.md", glossary_readme())


if __name__ == "__main__":
    main()
