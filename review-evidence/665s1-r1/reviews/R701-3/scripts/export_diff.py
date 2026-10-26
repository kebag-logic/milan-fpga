#!/usr/bin/env python3
"""Compare export dirs file by file (raw sha256). Report files differing between
base1 and head, and whether each such file also differs between base1 and base2
(run noise). A file differing head-vs-base but identical base-vs-base is a real
difference. Usage: export_diff.py <base1> <base2> <head>"""
import hashlib, sys
from pathlib import Path
def tab(d):
    d = Path(d); return {str(p.relative_to(d)): hashlib.sha256(p.read_bytes()).hexdigest() for p in d.rglob("*") if p.is_file()}
b1, b2, h = map(tab, sys.argv[1:4])
keys = set(b1) | set(b2) | set(h)
real = []; noise = []
for k in sorted(keys):
    if b1.get(k) != h.get(k):
        (noise if b1.get(k) != b2.get(k) else real).append(k)
print(f"files base1={len(b1)} base2={len(b2)} head={len(h)}; differ head-vs-base1={len(real)+len(noise)}; of which base1-vs-base2 also differ (noise)={len(noise)}; REAL={len(real)}")
for k in real: print("REAL", k)
for k in noise: print("noise", k)
sys.exit(1 if real else 0)
