#!/usr/bin/env python3
"""Compare regenerated ucode ROM images word by word: print differing word ranges."""
import sys
def load(p): return [l.strip() for l in open(p) if l.strip()]
def ranges(a, b):
    d = [i for i in range(max(len(a), len(b))) if (a[i] if i < len(a) else None) != (b[i] if i < len(b) else None)]
    out, s = [], None
    for i in d:
        if s is None: s = p = i
        elif i == p + 1: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return out, len(d)
a, b = load(sys.argv[1]), load(sys.argv[2])
r, n = ranges(a, b)
print(f"{sys.argv[1]} vs {sys.argv[2]}: {n} words differ: " + ", ".join(f"{x}..{y}" for x, y in r))
if len(sys.argv) > 3:  # relocation check: words A..A+len at old offset in b vs new offset in a
    for spec in sys.argv[3:]:
        new, old, ln = map(int, spec.split(":"))
        same = a[new:new+ln] == b[old:old+ln]
        print(f"  head[{new}..{new+ln-1}] == other[{old}..{old+ln-1}]: {same}")
