#!/usr/bin/env python3
"""Hash every installed file of the local verilator-5.050-1 Arch package
against the sha256 digests its own pacman mtree records."""
import gzip
import hashlib
import sys
from pathlib import Path

LAYER = Path(sys.argv[1])  # the image layer root holding usr/ and var/lib/pacman/
mtree = LAYER / "var/lib/pacman/local/verilator-5.050-1/mtree"
total = ok = bad = missing = 0
for raw in gzip.open(mtree, "rt"):
    if not raw.startswith("./usr"):
        continue
    parts = raw.split()
    fields = dict(p.split("=", 1) for p in parts[1:] if "=" in p)
    if fields.get("type", "file") != "file" or "sha256digest" not in fields:
        continue
    total += 1
    path = LAYER / parts[0][2:]
    if not path.exists():
        missing += 1
        print("MISSING", parts[0])
        continue
    if hashlib.sha256(path.read_bytes()).hexdigest() == fields["sha256digest"]:
        ok += 1
    else:
        bad += 1
        print("MISMATCH", parts[0])
print(f"files={total} ok={ok} mismatch={bad} missing={missing}")
sys.exit(1 if bad else 0)
