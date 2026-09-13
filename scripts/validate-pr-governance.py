#!/usr/bin/env python3
"""Validate the governance record in a pull-request body.

This is deliberately documentary: it does not claim that CAD visual review or
physical hardware validation has occurred.  Those gates remain human evidence.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def field(body: str, label: str) -> str:
    match = re.search(rf"(?im)^\s*-\s*{re.escape(label)}\s*:\s*(.+?)\s*$", body)
    return match.group(1).strip().strip("`") if match else ""


def usable(value: str) -> bool:
    lowered = value.lower()
    placeholders = ("40-character", "paths, commands", "state none", "non-author", "pending", "tbd", "todo")
    return bool(value) and not any(placeholder in lowered for placeholder in placeholders)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--body-file", required=True, type=Path)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--issue-output", type=Path)
    args = parser.parse_args()
    body = args.body_file.read_text(encoding="utf-8")
    errors: list[str] = []
    links = re.findall(r"(?im)^\s*(Refs|Closes|Fixes|Resolves)\s+#(\d+)\b", body)
    if len(links) != 1:
        errors.append("declare exactly one linked issue using Refs, Closes, Fixes, or Resolves")
    source = field(body, "Source revision")
    if source.lower() != args.head_sha.lower():
        errors.append("Source revision must exactly match the current PR head SHA")
    evidence = field(body, "Evidence / reports")
    blockers = field(body, "Measurements or explicitly retained blockers")
    if not usable(evidence):
        errors.append("Evidence / reports must contain concrete evidence or report locations")
    if not usable(blockers):
        errors.append("Measurements or explicitly retained blockers must state none or list blockers")
    unresolved = field(body, "Unresolved physical criteria").lower()
    if unresolved not in {"yes", "no"}:
        errors.append("Unresolved physical criteria must be exactly yes or no")
    if unresolved == "yes" and links and links[0][0].lower() != "refs":
        errors.append("PRs with unresolved physical criteria must use Refs, not an issue-closing keyword")
    reviewer = field(body, "Reviewer")
    reviewed_sha = field(body, "Reviewed final SHA")
    if not usable(reviewer):
        errors.append("Reviewer must name an independent reviewer")
    elif reviewer.lstrip("@").lower() == args.author.lstrip("@").lower():
        errors.append("Author cannot be the independent reviewer")
    if reviewed_sha.lower() != args.head_sha.lower():
        errors.append("Reviewed final SHA must exactly match the current PR head SHA")
    if errors:
        print("PR governance validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    issue = links[0][1]
    if args.issue_output:
        args.issue_output.write_text(issue + "\n", encoding="utf-8")
    print(f"PR governance record: OK (issue #{issue})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
