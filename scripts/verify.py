from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from paper_mcp import PaperClient, PaperMCPError


REPO_ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = REPO_ROOT / "artboard-map.json"
METADATA_PATH = REPO_ROOT / "export-metadata.json"
TOKEN_DIR = REPO_ROOT / "design-system" / "tokens"
USAGE_COVERAGE_PATH = TOKEN_DIR / "usage-coverage.json"
GLOSSARY_DIR = REPO_ROOT / "design-system" / "glossary"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
STALE_IDS = {"QCP-0", "U7Z-0", "UAK-0", "KQO-0", "SXR-0", "EIF-0"}
STALE_DIRS = [
    REPO_ROOT / "screens" / "welcome" / "1c-returning-multi-alt",
    REPO_ROOT / "screens" / "welcome" / "1c-3-rotate-keyset-modal",
    REPO_ROOT / "screens" / "welcome" / "1c-4-rotate-keyset-error-modal",
    REPO_ROOT / "screens" / "welcome" / "1c-1-unlock-modal",
    REPO_ROOT / "screens" / "import" / "3-review-save",
    REPO_ROOT / "screens" / "onboard" / "2b-failed",
    REPO_ROOT / "screens" / "onboard" / "3-complete",
    REPO_ROOT / "screens" / "dashboard" / "1c-profile-switcher",
    REPO_ROOT / "screens" / "dashboard" / "1d-with-rotate-share",
    REPO_ROOT / "screens" / "dashboard" / "2c-quorum-not-met",
    REPO_ROOT / "screens" / "dashboard" / "2d-signing-blocked",
    REPO_ROOT / "screens" / "dashboard" / "3-settings",
    REPO_ROOT / "screens" / "dashboard" / "7-pending-approvals",
    REPO_ROOT / "screens" / "dashboard" / "8-switch-profile",
]
EXPECTED_SCREEN_PATHS = {
    "QI3-0": "screens/welcome/1c-1-unlock-profile-modal",
    "6XP-0": "screens/import/3-review-save-profile",
    "73U-0": "screens/onboard/2b-onboarding-failed",
    "726-0": "screens/onboard/3-onboarding-complete",
    "T62-0": "screens/dashboard/2c-signing-blocked",
    "518-0": "screens/dashboard/3-settings-lock-profile",
}
GLOSSARY_FILES = {
    "core-protocol.md",
    "operations-setup.md",
    "policies-data-model.md",
    "core-protocol-screenshot.png",
    "operations-setup-screenshot.png",
    "policies-data-model-screenshot.png",
    "README.md",
}
HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?")
PAPER_ASSET_URL_RE = re.compile(r"https://app\.paper\.design/file-assets/")
LOCAL_ASSET_RE = re.compile(r"(?P<path>(?:\.\./)+assets/paper/[A-Za-z0-9_.-]+)")
FONT_CLASS_RE = re.compile(r"font-\['([^']+)'")
INLINE_FONT_RE = re.compile(r"fontFamily:\s*['\"]([^'\"]+)['\"]")
SIZE_CLASS_RE = re.compile(r"text-(\[[0-9.]+px\]|xs|sm|base|lg|xl|2xl|3xl|4xl)(?:/(\[[0-9.]+px\]|[0-9.]+))?")
TAILWIND_TEXT_SIZES = {
    "xs": ("12px", "16px"),
    "sm": ("14px", "20px"),
    "base": ("16px", "24px"),
    "lg": ("18px", "28px"),
    "xl": ("20px", "28px"),
    "2xl": ("24px", "32px"),
    "3xl": ("30px", "36px"),
    "4xl": ("36px", "40px"),
}
MAX_DRIFT_ITEMS = 20


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def ensure(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def load_map() -> list[dict[str, Any]]:
    return load_json(MAP_PATH)


def load_metadata() -> dict[str, Any]:
    return load_json(METADATA_PATH)


def is_png(path: Path) -> bool:
    return path.read_bytes()[: len(PNG_SIGNATURE)] == PNG_SIGNATURE


def normalize_hex(value: str) -> str:
    return value.upper()


def normalize_family(value: str) -> str:
    primary = value.split(",", 1)[0].strip().strip("'\"")
    return " ".join(primary.replace("_", " ").split()).lower()


def normalize_px(value: str) -> str:
    return value.strip().lower()


def spacing_to_px(value: str) -> str:
    return f"{float(value) * 4:g}px"


def size_token_to_px(token: str) -> tuple[str | None, str | None]:
    if token.startswith("[") and token.endswith("]"):
        return normalize_px(token[1:-1]), None
    return TAILWIND_TEXT_SIZES.get(token, (None, None))


def line_token_to_px(token: str | None, default: str | None) -> str | None:
    if token is None:
        return default
    if token.startswith("[") and token.endswith("]"):
        return normalize_px(token[1:-1])
    return spacing_to_px(token)


def section_bullets(text: str, heading: str) -> list[str]:
    match = re.search(rf"^## {re.escape(heading)}\n(.*?)(?:\n## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    bullets: list[str] = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if stripped.startswith("- **") and stripped.endswith("**"):
            bullets.append(stripped[4:-2])
    return bullets


def verify_map(entries: list[dict[str, Any]]) -> None:
    ensure(len(entries) == 69, f"artboard-map.json should contain 69 entries, found {len(entries)}")
    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry["category"]] = counts.get(entry["category"], 0) + 1
    ensure(counts.get("design-system") == 24, f"expected 24 design-system entries, found {counts.get('design-system')}")
    ensure(counts.get("screen") == 44, f"expected 44 screen entries, found {counts.get('screen')}")
    ensure(counts.get("divider") == 1, f"expected 1 divider entry, found {counts.get('divider')}")

    entries_by_id = {entry["paperNodeId"]: entry for entry in entries}
    for artboard_id, output_path in EXPECTED_SCREEN_PATHS.items():
        ensure(entries_by_id[artboard_id]["outputPath"] == output_path, f"{artboard_id} should map to {output_path}")


def verify_outputs(entries: list[dict[str, Any]]) -> None:
    for entry in entries:
        output_path = entry["outputPath"]
        if not output_path:
            continue
        path = REPO_ROOT / output_path
        ensure(path.exists(), f"missing output directory {output_path}")
        if entry["paperNodeId"] in {"ONB-0", "OSN-0", "OXZ-0"}:
            continue
        required = ["README.md", "screen.html", "screenshot.png"] if entry["category"] == "screen" else ["README.md", "reference.html", "screenshot.png"]
        for name in required:
            target = path / name
            ensure(target.exists(), f"missing file {target.relative_to(REPO_ROOT)}")
            ensure(target.stat().st_size > 0, f"empty file {target.relative_to(REPO_ROOT)}")
            if target.name == "screenshot.png":
                ensure(is_png(target), f"screenshot is not PNG data: {target.relative_to(REPO_ROOT)}")

    shared_dir = REPO_ROOT / "screens" / "_shared"
    for name in ["app-header.html", "app-footer.html"]:
        target = shared_dir / name
        ensure(target.exists(), f"missing shared component {target.relative_to(REPO_ROOT)}")
        ensure(target.stat().st_size > 0, f"empty shared component {target.relative_to(REPO_ROOT)}")

    ensure(GLOSSARY_DIR.exists(), "missing glossary directory")
    existing = {path.name for path in GLOSSARY_DIR.iterdir() if path.is_file()}
    ensure(GLOSSARY_FILES.issubset(existing), f"glossary files missing: {sorted(GLOSSARY_FILES - existing)}")
    for name in GLOSSARY_FILES:
        target = GLOSSARY_DIR / name
        ensure(target.stat().st_size > 0, f"empty glossary artifact {target.relative_to(REPO_ROOT)}")
        if target.name.endswith("-screenshot.png"):
            ensure(is_png(target), f"glossary screenshot is not PNG data: {target.relative_to(REPO_ROOT)}")

    colors = load_json(TOKEN_DIR / "colors.json")
    typography = load_json(TOKEN_DIR / "typography.json")
    ensure("background-colors" in colors, "colors.json missing Foundations background colors")
    ensure("font-families" in typography, "typography.json missing font-families")
    ensure((TOKEN_DIR / "tokens.css").stat().st_size > 0, "tokens.css is empty")

    for stale_dir in STALE_DIRS:
        ensure(not stale_dir.exists(), f"deprecated or stale directory still exists: {stale_dir.relative_to(REPO_ROOT)}")


def verify_readmes(entries: list[dict[str, Any]], metadata: dict[str, Any]) -> None:
    entries_by_id = {entry["paperNodeId"]: entry for entry in entries if entry["category"] != "divider"}
    group_membership = defaultdict(list)
    for group in metadata.get("screen_groups", []):
        for artboard_id in group["entries"]:
            group_membership[artboard_id].append(group["id"])

    for entry in entries:
        if entry["category"] != "screen":
            continue
        readme = (REPO_ROOT / entry["outputPath"] / "README.md").read_text()
        ensure("**Previous:**" not in readme and "**Next:**" not in readme, f"screen README still uses Previous/Next: {entry['outputPath']}/README.md")
        if len(group_membership.get(entry["paperNodeId"], [])) > 0:
            ensure("## Related Screens" in readme, f"screen README missing Related Screens: {entry['outputPath']}/README.md")

    for artboard_id, override in metadata.get("artboard_overrides", {}).items():
        entry = entries_by_id.get(artboard_id)
        ensure(entry is not None, f"metadata override references unknown artboard {artboard_id}")
        readme_path = REPO_ROOT / entry["outputPath"] / "README.md"
        text = readme_path.read_text()
        contents = section_bullets(text, "Contents")
        banned = set(override.get("ignore_contents", [])) | set(override.get("rename_contents", {}).keys())
        for label in banned:
            ensure(label not in contents, f"README still contains banned content label {label}: {readme_path.relative_to(REPO_ROOT)}")
        if "contents" in override:
            ensure(contents == override["contents"], f"README contents do not match override for {readme_path.relative_to(REPO_ROOT)}")
        if "description" in override:
            ensure(override["description"] in text, f"README description override missing for {readme_path.relative_to(REPO_ROOT)}")


def verify_against_paper(entries: list[dict[str, Any]]) -> None:
    try:
        client = PaperClient()
        client.initialize()
        basic = client.get_basic_info()
    except PaperMCPError as exc:
        fail(f"could not reach Paper MCP: {exc}")

    artboard_ids = {artboard["id"] for artboard in basic["artboards"]}
    mapped_ids = {entry["paperNodeId"] for entry in entries if entry["category"] != "divider"}
    missing = sorted(mapped_ids - artboard_ids)
    ensure(not missing, f"mapped ids missing from Paper: {missing}")
    present_stale = sorted(STALE_IDS & artboard_ids)
    ensure(not present_stale, f"stale ids unexpectedly present in Paper: {present_stale}")


def collect_color_tokens() -> set[str]:
    colors = load_json(TOKEN_DIR / "colors.json")
    token_set: set[str] = set()
    for section in colors.values():
        if not isinstance(section, dict):
            continue
        for token in section.get("tokens", {}).values():
            value = token.get("value")
            if isinstance(value, str) and HEX_RE.fullmatch(value):
                token_set.add(normalize_hex(value))
    usage_coverage = load_json(USAGE_COVERAGE_PATH) if USAGE_COVERAGE_PATH.exists() else {}
    for token in usage_coverage.get("colors", []):
        value = token.get("value") if isinstance(token, dict) else token
        if isinstance(value, str) and HEX_RE.fullmatch(value):
            token_set.add(normalize_hex(value))
    return token_set


def collect_font_tokens() -> set[str]:
    typography = load_json(TOKEN_DIR / "typography.json")
    return {normalize_family(name) for name in typography.get("font-families", {})}


def collect_type_tokens() -> set[tuple[str, str]]:
    typography = load_json(TOKEN_DIR / "typography.json")
    combos: set[tuple[str, str]] = set()
    for token in typography.get("type-scale", {}).values():
        font_size = token.get("font-size")
        line_height = token.get("line-height")
        if isinstance(font_size, str) and isinstance(line_height, str):
            combos.add((normalize_px(font_size), normalize_px(line_height)))
    usage_coverage = load_json(USAGE_COVERAGE_PATH) if USAGE_COVERAGE_PATH.exists() else {}
    for token in usage_coverage.get("typography", []):
        if not isinstance(token, dict):
            continue
        font_size = token.get("font-size")
        line_height = token.get("line-height")
        if isinstance(font_size, str) and isinstance(line_height, str):
            combos.add((normalize_px(font_size), normalize_px(line_height)))
    return combos


def html_targets() -> list[Path]:
    files = list(REPO_ROOT.glob("design-system/**/reference.html"))
    files.extend(REPO_ROOT.glob("screens/**/screen.html"))
    files.append(REPO_ROOT / "screens" / "_shared" / "app-header.html")
    files.append(REPO_ROOT / "screens" / "_shared" / "app-footer.html")
    return sorted({path for path in files if path.exists()})


def verify_local_assets() -> None:
    for path in html_targets():
        text = path.read_text()
        ensure(not PAPER_ASSET_URL_RE.search(text), f"remote Paper asset URL remains in {path.relative_to(REPO_ROOT)}")
        for match in LOCAL_ASSET_RE.finditer(text):
            target = (path.parent / match.group("path")).resolve()
            ensure(target.exists(), f"missing localized asset {target.relative_to(REPO_ROOT)} referenced by {path.relative_to(REPO_ROOT)}")


def scan_html(path: Path) -> tuple[set[str], set[str], set[tuple[str, str]]]:
    text = path.read_text()
    colors = {normalize_hex(match.group(0)) for match in HEX_RE.finditer(text)}

    fonts: set[str] = set()
    for match in FONT_CLASS_RE.finditer(text):
        fonts.add(normalize_family(match.group(1)))
    for match in INLINE_FONT_RE.finditer(text):
        fonts.add(normalize_family(match.group(1)))

    combos: set[tuple[str, str]] = set()
    for match in SIZE_CLASS_RE.finditer(text):
        size_token, line_token = match.groups()
        font_size, default_line_height = size_token_to_px(size_token)
        if not font_size:
            continue
        line_height = line_token_to_px(line_token, default_line_height)
        if line_height:
            combos.add((font_size, line_height))
    return colors, fonts, combos


def print_drift_bucket(label: str, items: dict[Any, set[str]]) -> None:
    if not items:
        return
    print(f"{label}:")
    keys = sorted(items)
    for key in keys[:MAX_DRIFT_ITEMS]:
        samples = ", ".join(sorted(items[key])[:3])
        print(f"  - {key}: {samples}")
    if len(keys) > MAX_DRIFT_ITEMS:
        print(f"  - ... {len(keys) - MAX_DRIFT_ITEMS} more")


def verify_drift(strict_drift: bool) -> None:
    canonical_colors = collect_color_tokens()
    canonical_fonts = collect_font_tokens()
    canonical_typography = collect_type_tokens()

    color_usage: dict[str, set[str]] = defaultdict(set)
    font_usage: dict[str, set[str]] = defaultdict(set)
    typography_usage: dict[tuple[str, str], set[str]] = defaultdict(set)

    for path in html_targets():
        rel = path.relative_to(REPO_ROOT).as_posix()
        colors, fonts, combos = scan_html(path)
        for color in colors:
            color_usage[color].add(rel)
        for font in fonts:
            font_usage[font].add(rel)
        for combo in combos:
            typography_usage[combo].add(rel)

    color_drift = {color: paths for color, paths in color_usage.items() if color not in canonical_colors}
    font_drift = {font: paths for font, paths in font_usage.items() if font not in canonical_fonts}
    typography_drift = {combo: paths for combo, paths in typography_usage.items() if combo not in canonical_typography}

    if color_drift:
        print(("FAIL" if strict_drift else "WARN") + f": color drift against Foundations tokens ({len(color_drift)} values)")
        print_drift_bucket("colors", color_drift)
    if font_drift:
        print(f"FAIL: font drift against Foundations tokens ({len(font_drift)} families)")
        print_drift_bucket("fonts", font_drift)
    if typography_drift:
        print(("FAIL" if strict_drift else "WARN") + f": typography drift against Foundations tokens ({len(typography_drift)} size/line-height pairs)")
        formatted = {f"{size} / {line_height}": paths for (size, line_height), paths in typography_drift.items()}
        print_drift_bucket("typography", formatted)

    print(
        "Drift summary:"
        f" colors={len(color_drift)}"
        f" fonts={len(font_drift)}"
        f" typography={len(typography_drift)}"
    )

    if font_drift:
        fail("font drift detected outside Foundations typography families")
    if strict_drift and color_drift:
        fail("strict drift mode detected colors outside Foundations and usage-coverage token coverage")
    if strict_drift and typography_drift:
        fail("strict drift mode detected typography pairs outside Foundations and usage-coverage token coverage")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify the igloo-paper export.")
    parser.add_argument("--strict-drift", action="store_true", help="Treat non-Foundation color and typography drift as failures.")
    args = parser.parse_args()

    entries = load_map()
    metadata = load_metadata()
    verify_map(entries)
    verify_outputs(entries)
    verify_readmes(entries, metadata)
    verify_local_assets()
    verify_against_paper(entries)
    verify_drift(args.strict_drift)
    print("PASS: structural export checks passed, metadata curation checks passed, and Paper reconciliation succeeded.")


if __name__ == "__main__":
    main()
