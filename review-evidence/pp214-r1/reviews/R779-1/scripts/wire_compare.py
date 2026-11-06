#!/usr/bin/env python3
"""Compare the frames two tb/srp_top runs put on the wire. usage: wire_compare.py <dir with head.<g>.log and base-rtl.<g>.log>"""
import collections, pathlib, sys
d = pathlib.Path(sys.argv[1])
def frames(p):
    return [l.split() for l in p.read_text(errors="replace").splitlines() if l.startswith("FRAME ")]
for g in ("share", "link", "domjoin"):
    a, b = frames(d / f"head.{g}.log"), frames(d / f"base-rtl.{g}.log")
    print(f"{g}: head {len(a)} frames, base {len(b)} frames, same ms and bytes in order: {a == b}")
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            print(f"  frame {i}\n    head {x[1]} ms {x[2]}\n    base {y[1]} ms {y[2]}")
