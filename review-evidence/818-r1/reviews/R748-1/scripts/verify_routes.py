#!/usr/bin/env python3
"""Verify recorded route report bytes against the author's published route-reports.tsv."""
import hashlib, sys
from pathlib import Path
tsv, *roots = sys.argv[1:]
base = dict(r.split("=", 1) for r in roots)
bad = ok = 0
for line in Path(tsv).read_text().splitlines()[1:]:
    rset, sub, rpt, size, sha = line.split("\t")
    p = Path(base[rset]) / sub / rpt
    data = p.read_bytes() if p.is_file() else b""
    good = len(data) == int(size) and hashlib.sha256(data).hexdigest() == sha
    ok += good; bad += not good
    if not good: print("MISMATCH", rset, sub, rpt)
print(f"route reports: {ok} match, {bad} mismatch")
sys.exit(1 if bad else 0)
