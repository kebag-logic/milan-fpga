#!/usr/bin/env python3
"""Verify published sweep artifact hashes against the files on the data path.
Usage: verify_artifacts.py <sweep-artifacts.json> <VALIDATION_STORAGE root>"""
import hashlib, json, sys
from pathlib import Path
arts = json.load(open(sys.argv[1])); root = sys.argv[2]
bad = 0
for a in arts:
    p = Path(a["path"].replace("$VALIDATION_STORAGE", root))
    if not p.exists():
        print("MISSING", a["path"]); bad += 1; continue
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    ok = h == a["sha256"] and p.stat().st_size == a["size"]
    bad += not ok
    print("OK  " if ok else "BAD ", a["path"])
print(f"checked={len(arts)} bad={bad}")
sys.exit(1 if bad else 0)
