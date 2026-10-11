#!/usr/bin/env python3
"""Classify head MRPDUs that carry octets after the MRPDU EndMark: origin and base equality.

Usage: r597_trailing.py <base dump> <head dump>
"""
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r597_mrpdu as m
base, head = m.load(Path(sys.argv[1])), m.load(Path(sys.argv[2]))
c = Counter(); ex = {}
for exe in sorted(head):
    for rb, rh in zip(base[exe], head[exe]):
        for a, b in zip(rb, rh):
            if a[0] != "T":
                continue
            try:
                d = m.decode(b[3])
            except m.Malformed:
                continue
            if d["trailing"]:
                tail = b[3][len(b[3]) - d["trailing"]:]
                key = (exe.split("/")[1] if "/" in exe else exe, a[3] == b[3], d["trailing"],
                       len(d["messages"]), d["etype"], tail[:8].hex(), b[3][6:12].hex())
                c[key] += 1
for k, n in sorted(c.items()):
    print(n, "exe=%s base_identical=%s trailing=%d messages=%d etype=%#x tail8=%s sa=%s" % k)
