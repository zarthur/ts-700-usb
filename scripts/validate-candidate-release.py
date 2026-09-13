#!/usr/bin/env python3
"""Validate a non-procurement TS-700SP candidate-release package."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

REQUIRED = (
    "README.txt", "source/ts700sp-interface.kicad_sch", "source/usb-ptt.kicad_sch",
    "source/audio.kicad_sch", "source/ts700sp-interface.kicad_pcb", "source/ts700sp-interface.kicad_pro", "source/cad-completion.md",
    "reports/ts700sp-interface-erc.json", "reports/usb-ptt-erc.json", "reports/audio-erc.json",
    "reports/drc.json", "review/schematic.pdf", "review/schematic.svg", "review/schematic.net",
    "review/board.step", "review/board.svg", "manufacturing-candidate/bom.csv",
    "manufacturing-candidate/gerbers", "manufacturing-candidate/drill", "manufacturing-candidate/placement.csv",
)
SHA = re.compile(r"^[0-9a-f]{40}$")
PROHIBITED = re.compile(r"\b(fabrication[- ]?ready|approved for manufacture|ready to order|procurement approved)\b", re.I)

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)

def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def report_has_violations(path: Path) -> bool:
    try:
        return bool(json.loads(path.read_text(encoding="utf-8")).get("violations"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"invalid KiCad JSON report {path}: {error}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--tool-version", help="required when writing a manifest")
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()
    package = args.package.resolve()
    if not package.is_dir(): fail(f"package is not a directory: {package}")
    if not SHA.fullmatch(args.source_sha): fail("source SHA must be a 40-character lowercase hexadecimal commit SHA")
    for relative in REQUIRED:
        item = package / relative
        if not item.exists() or (item.is_file() and not item.stat().st_size): fail(f"missing or empty required artifact: {relative}")
    manifest_path = package / "MANIFEST.json"
    if not args.write_manifest and not manifest_path.is_file(): fail("MANIFEST.json is required when validating an existing package")
    if args.write_manifest and not args.tool_version: fail("--tool-version is required with --write-manifest")
    readme = (package / "README.txt").read_text(encoding="utf-8")
    if "PROVISIONAL" not in readme or "NOT FOR FABRICATION" not in readme or args.source_sha not in readme: fail("README.txt lacks required provisional status, fabrication prohibition, or source SHA")
    for path in package.rglob("*"):
        if path.is_file() and path.name != "MANIFEST.json":
            try:
                if PROHIBITED.search(path.read_text(encoding="utf-8")): fail(f"release-like claim in {path.relative_to(package)}")
            except UnicodeDecodeError: pass
    for name in ("ts700sp-interface-erc.json", "usb-ptt-erc.json", "audio-erc.json", "drc.json"):
        report = package / "reports" / name
        if report_has_violations(report): fail(f"unexplained KiCad violations in reports/{name}")
    if not any((package / "manufacturing-candidate/gerbers").iterdir()): fail("Gerber directory is empty")
    if not any((package / "manufacturing-candidate/drill").iterdir()): fail("drill directory is empty")
    with (package / "manufacturing-candidate/bom.csv").open(newline="", encoding="utf-8") as handle:
        if not list(csv.reader(handle)): fail("BOM CSV has no rows")
    files = {str(path.relative_to(package)): {"sha256": digest(path), "bytes": path.stat().st_size}
             for path in sorted(package.rglob("*")) if path.is_file() and path.name != "MANIFEST.json"}
    manifest = {"format": 1, "status": "PROVISIONAL_NOT_FOR_FABRICATION_OR_PROCUREMENT", "source_sha": args.source_sha, "tool_version": args.tool_version, "files": files}
    if args.write_manifest:
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        saved = json.loads(manifest_path.read_text(encoding="utf-8"))
        if saved.get("source_sha") != args.source_sha or saved.get("status") != manifest["status"] or saved.get("files") != files: fail("manifest source SHA, status, or checksums do not match package contents")
    print(f"Candidate package validated: {package}")

if __name__ == "__main__": main()
