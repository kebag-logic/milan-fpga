#!/usr/bin/env python3
"""Validate the completed packet, then emit and verify its publication manifest."""
import hashlib
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parents[1]
report = (packet / "REPORT.md").read_text()
assert report.splitlines()[0] == "[R505] POSITIVE - exact head 2139f3dc10161b456dfbd51d2f73a63f9164e041"
assert report.splitlines()[-1] == "R505-1 FINISHED"
assert "SKELETON" not in report
assert all(f"| {lens} | CLEAN |" in report for lens in ["Conformance", "RTL", "Robustness", "Tests", "Docs"])
for script in (packet / "scripts").glob("*.py"):
    compile(script.read_bytes(), str(script), "exec")
assert json.loads((packet / "receipts/prior-findings.json").read_text())["disposition"] == "No prior public findings to retain or resolve"
assert json.loads((packet / "receipts/final-integrity.json").read_text())["all_disk_bytes_and_modes_match"]
for row in json.loads((packet / "receipts/analysis-summary.json").read_text()):
    assert row["files"] == 46 and row["expected_table_matches"]
assert json.loads((packet / "receipts/focused-suites.json").read_text())["identical_records"]
assert sum(r["killed"] for r in json.loads((packet / "receipts/campaign-summary.json").read_text())) == 5
for path in packet.rglob("*"):
    if "scratch" in path.relative_to(packet).parts:
        continue
    assert not path.is_symlink(), str(path)
    if path.is_file():
        assert "__pycache__" not in path.parts
files = sorted(p for p in packet.rglob("*") if p.is_file() and "scratch" not in p.relative_to(packet).parts and p.name != "MANIFEST.sha256")
assert all(p == packet / "REPORT.md" or p.relative_to(packet).parts[0] in ["scripts", "receipts", "public"] for p in files)
manifest = "".join(hashlib.sha256(path.read_bytes()).hexdigest() + "  " + path.relative_to(packet).as_posix() + "\n" for path in files)
(packet / "MANIFEST.sha256").write_text(manifest)
check = subprocess.run(["sha256sum", "--check", "MANIFEST.sha256"], cwd=packet, capture_output=True, text=True)
assert check.returncode == 0, check.stdout + check.stderr
print(json.dumps({"publishable_files": len(files), "manifest_sha256": hashlib.sha256(manifest.encode()).hexdigest(), "sha256sum_check_rc": check.returncode, "scratch_excluded": True, "report_final": True}, indent=2))
