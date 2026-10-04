#!/usr/bin/env python3
"""Redact host paths in every text receipt under DIR, in place.

usage: redact.py DIR SIM_ROOT PACKET CLONE WRAPPER_DIR
Longest prefixes are replaced first: <SIM_ROOT>, <SCRATCH> (PACKET/scratch),
<PACKET>, <CLONE>, <SIM_WRAPPER_DIR>.
"""
import sys
from pathlib import Path

d, sim, packet, clone, wrap = sys.argv[1:6]
subs = sorted([(sim, "<SIM_ROOT>"), (packet + "/scratch", "<SCRATCH>"), (packet, "<PACKET>"),
               (clone, "<CLONE>"), (wrap, "<SIM_WRAPPER_DIR>")], key=lambda s: -len(s[0]))
n = 0
for f in sorted(Path(d).rglob("*")):
    if not f.is_file():
        continue
    try:
        t = f.read_text()
    except UnicodeDecodeError:
        continue
    u = t
    for a, b in subs:
        u = u.replace(a, b)
    if u != t:
        f.write_text(u)
        n += 1
print(f"redacted {n} files")
