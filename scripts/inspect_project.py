#!/usr/bin/env python3
"""Read-only project reconnaissance for scheduled maintenance runs."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path


MANIFESTS = {
    "pyproject.toml", "setup.py", "package.json", "Cargo.toml", "go.mod",
    "pom.xml", "build.gradle", "Gemfile", "composer.json", "Makefile",
}
CONTEXT_FILES = {
    "project-goal.md", "developer-preferences.md", "progress.md",
    "decisions.md", "rejected-ideas.md",
}


def run_git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, text=True, capture_output=True,
            check=False, timeout=10, encoding="utf-8", errors="replace",
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.path).resolve()

    files = []
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            try:
                files.append(str(path.relative_to(root)))
            except ValueError:
                pass
    files.sort()

    result = {
        "path": str(root),
        "git": {
            "root": run_git(root, "rev-parse", "--show-toplevel"),
            "branch": run_git(root, "branch", "--show-current"),
            "status": run_git(root, "status", "--short"),
            "recent_commits": run_git(root, "log", "-5", "--oneline"),
        },
        "manifests": sorted(name for name in MANIFESTS if (root / name).exists()),
        "context_files": sorted(name for name in CONTEXT_FILES if (root / name).exists()),
        "file_count": len(files),
        "top_level_files": [name for name in files if os.sep not in name][:50],
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
