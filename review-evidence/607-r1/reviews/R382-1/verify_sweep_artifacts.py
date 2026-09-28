#!/usr/bin/env python3
"""Verify locally retained sweep artifacts against the published sweep-artifacts.json hashes.
Usage: verify_sweep_artifacts.py <sweep-artifacts.json> <VALIDATION_STORAGE root>"""
import hashlib, json, sys
from pathlib import Path
index, root = json.load(open(sys.argv[1])), sys.argv[2]
ok = bad = missing = 0
for item in index:
    p = Path(item["path"].replace("$VALIDATION_STORAGE", root))
    if not p.exists():
        missing += 1; print("MISSING", item["path"]); continue
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    if h.hexdigest() == item["sha256"] and p.stat().st_size == item["size"]:
        ok += 1
    else:
        bad += 1; print("MISMATCH", item["path"])
print(f"verified={ok} mismatched={bad} missing={missing} total={len(index)}")
sys.exit(1 if bad or missing else 0)
