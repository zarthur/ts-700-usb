#!/usr/bin/env python3
"""Regression coverage for candidate-release report and checksum validation."""
from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
VALIDATOR = SCRIPTS / "validate-candidate-release.py"
FIXTURES = Path(__file__).parent / "fixtures" / "candidate-release"
SHA = "a" * 40


class CandidateReleaseValidatorTests(unittest.TestCase):
    def make_package(self, report_fixture: str = "clean.json") -> Path:
        package = Path(tempfile.mkdtemp(prefix="ts700-candidate-test-"))
        for relative in (
            "source", "reports", "review", "manufacturing-candidate/gerbers",
            "manufacturing-candidate/drill",
        ):
            (package / relative).mkdir(parents=True, exist_ok=True)
        (package / "README.txt").write_text(
            f"SOURCE SHA: {SHA}\nPROVISIONAL — NOT FOR FABRICATION\n", encoding="utf-8"
        )
        for name in (
            "ts700sp-interface.kicad_sch", "usb-ptt.kicad_sch", "audio.kicad_sch",
            "ts700sp-interface.kicad_pcb", "ts700sp-interface.kicad_pro", "cad-completion.md",
        ):
            (package / "source" / name).write_text("source\n", encoding="utf-8")
        report = (FIXTURES / report_fixture).read_text(encoding="utf-8")
        for name in ("ts700sp-interface-erc.json", "usb-ptt-erc.json", "audio-erc.json", "drc.json"):
            (package / "reports" / name).write_text(report if name == "drc.json" else (FIXTURES / "clean.json").read_text(encoding="utf-8"), encoding="utf-8")
        for name in ("schematic.pdf", "schematic.svg", "schematic.net", "board.step", "board.svg"):
            (package / "review" / name).write_text("review\n", encoding="utf-8")
        (package / "manufacturing-candidate/bom.csv").write_text("Reference,Value\nR1,1k\n", encoding="utf-8")
        (package / "manufacturing-candidate/gerbers/test.gbr").write_text("g\n", encoding="utf-8")
        (package / "manufacturing-candidate/drill/test.drl").write_text("d\n", encoding="utf-8")
        (package / "manufacturing-candidate/placement.csv").write_text("Ref,PosX\nR1,0\n", encoding="utf-8")
        self.addCleanup(shutil.rmtree, package)
        return package

    def invoke(self, package: Path, write: bool = False) -> subprocess.CompletedProcess[str]:
        command = ["python3", str(VALIDATOR), "--package", str(package), "--source-sha", SHA]
        if write:
            command.extend(("--tool-version", "10.0.6", "--write-manifest"))
        return subprocess.run(command, capture_output=True, text=True, check=False)

    def test_clean_report_and_manifest_pass(self) -> None:
        package = self.make_package()
        self.assertEqual(self.invoke(package, write=True).returncode, 0)
        self.assertEqual(self.invoke(package).returncode, 0)

    def test_top_level_violation_fails(self) -> None:
        result = self.invoke(self.make_package("top-level-violation.json"), write=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unexplained KiCad violations", result.stderr)

    def test_nested_sheet_violation_fails(self) -> None:
        result = self.invoke(self.make_package("nested-sheet-violation.json"), write=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unexplained KiCad violations", result.stderr)

    def test_malformed_report_fails(self) -> None:
        result = self.invoke(self.make_package("malformed.json"), write=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid KiCad JSON report", result.stderr)

    def test_checksum_mismatch_fails(self) -> None:
        package = self.make_package()
        self.assertEqual(self.invoke(package, write=True).returncode, 0)
        (package / "review/board.svg").write_text("changed\n", encoding="utf-8")
        result = self.invoke(package)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("checksums do not match", result.stderr)


if __name__ == "__main__":
    unittest.main()
