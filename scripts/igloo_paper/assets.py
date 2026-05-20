from __future__ import annotations

from pathlib import Path


def asset_dir(repo_root: Path) -> Path:
    return repo_root / "assets" / "paper"
