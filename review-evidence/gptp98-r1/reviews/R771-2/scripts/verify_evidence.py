#!/usr/bin/env python3
"""Hash-check downloaded author receipts against the published MANIFEST.json.

usage: python3 -I verify_evidence.py EVIDENCE_DIR FILE...
EVIDENCE_DIR holds MANIFEST.json and the receipts, downloaded from
kebag-logic/milan-fpga@59152409 review-evidence/gptp98-r1/ by their paths.
"""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
m = {e["file"]: e["published_sha256"] for e in json.loads((root / "MANIFEST.json").read_text())}
bad = 0
for f in sys.argv[2:]:
    h = hashlib.sha256((root / f).read_bytes()).hexdigest()
    ok = m.get(f) == h
    bad += not ok
    print(f"{'MATCH' if ok else 'MISMATCH'} {h} {f}")
sys.exit(1 if bad else 0)
