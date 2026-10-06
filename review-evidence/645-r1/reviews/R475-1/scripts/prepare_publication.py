#!/usr/bin/env python3
"""Redact only private installation prefixes; retain raw logs in scratch."""
import hashlib
import json
import re
from pathlib import Path

PACKET = Path(__file__).resolve().parents[1]
RAW = PACKET / "scratch/unpublished-raw"
PREFIX = re.compile(rb"/home/[^/\s]+/\.local/share/containers/storage/overlay/[^/\s]+/diff/usr/share/verilator")
records = []
for relative in (
    "receipts/capture-unit.log",
    "receipts/follow-build.log",
    "receipts/span-build.log",
    "receipts/settle-build.log",
):
    path = PACKET / relative
    source = path.read_bytes()
    raw_path = RAW / relative
    if not PREFIX.search(source) and raw_path.exists():
        source = raw_path.read_bytes()
    published, count = PREFIX.subn(b"<SIMULATOR_ROOT>", source)
    assert count, f"Expected private prefix missing in {relative}"
    assert b"/home/" not in published, f"Unrecognized private path in {relative}"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_bytes(source)
    path.write_bytes(published)
    records.append({
        "path": relative,
        "substitutions": count,
        "original_sha256": hashlib.sha256(source).hexdigest(),
        "published_sha256": hashlib.sha256(published).hexdigest(),
        "original_bytes": len(source),
        "published_bytes": len(published),
    })
(PACKET / "receipts/publication-redactions.json").write_text(json.dumps({
    "scope": "Private simulator installation prefixes only; no measurement, test result, or verdict changed.",
    "replacement": "<SIMULATOR_ROOT>",
    "originals": "Unpublished scratch/unpublished-raw; hashes below preserve their identities.",
    "files": records,
}, indent=2) + "\n")
print(f"Prepared {len(records)} public logs; originals retained under scratch.")
