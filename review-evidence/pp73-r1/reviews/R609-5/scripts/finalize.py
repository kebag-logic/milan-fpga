#!/usr/bin/env python3
"""Seal the publication set without including scratch or the manifest itself."""
import hashlib
import json
from pathlib import Path

packet = Path(__file__).resolve().parents[1]
report = (packet / "REPORT.md").read_text()
assert report.splitlines()[0] == "[R609] POSITIVE - exact head 4bee75b2e647507a71ece50359fceb135c334757"
assert report.splitlines()[-1] == "R609-5 FINISHED"
assert "SKELETON" not in report
integrity = json.loads((packet / "receipts/integrity.json").read_text())
assert integrity["tracked_bytes_and_modes_match"] and integrity["index_matches_head"]
assert integrity["tracked_files"] == 618 and not integrity["gitlinks"]
assert all(row["returncode"] == 0 for row in json.loads((packet / "receipts/campaigns.json").read_text()))
assert all(row["passed"] for row in json.loads((packet / "receipts/controls/results.json").read_text()))
paths = [packet / "REPORT.md"]
for directory in ("scripts", "receipts"):
    paths.extend(p for p in (packet / directory).rglob("*") if p.is_file())
paths = sorted(paths, key=lambda p: p.relative_to(packet).as_posix())
lines = []
for path in paths:
    relative = path.relative_to(packet).as_posix()
    assert not path.is_symlink() and "scratch/" not in relative
    lines.append(hashlib.sha256(path.read_bytes()).hexdigest() + "  " + relative)
(packet / "MANIFEST.sha256").write_text("\n".join(lines)+"\n")
print(f"Sealed {len(paths)} publication files; scratch excluded.")
