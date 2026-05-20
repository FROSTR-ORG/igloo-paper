from __future__ import annotations

from pathlib import Path


def token_dir(repo_root: Path) -> Path:
    return repo_root / "design" / "tokens"


def glossary_dir(repo_root: Path) -> Path:
    return repo_root / "design" / "glossary"
