#!/usr/bin/env python3
"""Verify repository-relative Markdown links without fetching external sites."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("#", "http:", "https:", "mailto:", "tel:", "data:")


def target(value: str) -> str:
    value = value.strip().strip("<>")
    return value.split(None, 1)[0].split("#", 1)[0]


def main() -> int:
    failures: list[str] = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        for match in LINK.finditer(path.read_text(encoding="utf-8")):
            value = target(match.group(1))
            if not value or value.lower().startswith(SKIP_PREFIXES):
                continue
            candidate = (path.parent / unquote(value)).resolve()
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                failures.append(f"{path.relative_to(ROOT)}: link escapes repository: {value}")
                continue
            if not candidate.exists():
                failures.append(f"{path.relative_to(ROOT)}: missing link target: {value}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("Repository-relative Markdown links: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
