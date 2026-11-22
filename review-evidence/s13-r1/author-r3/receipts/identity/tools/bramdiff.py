#!/usr/bin/env python3
"""bramdiff.py A.bram B.bram: two images' block RAM contents (bramdump.tcl), cell by cell: every cell present in both
at the same LOC, and for each INIT* property that differs the bit positions that differ. Prints the cells that
differ, the bits per property, and the total; exit 0 when no cell differs."""
import sys
def load(path):
    rows = {}
    for line in open(path):
        name, ref, loc, *props = line.split()
        rows[name] = (ref, loc, dict(p.split("=", 1) for p in props))
    return rows
a, b = load(sys.argv[1]), load(sys.argv[2])
print(f"block RAM cells: A {len(a)} B {len(b)}; only A {len(set(a) - set(b))}, only B {len(set(b) - set(a))}")
moved = [n for n in set(a) & set(b) if a[n][:2] != b[n][:2]]
print(f"cells whose type or LOC differ: {len(moved)}")
total = 0
for n in sorted(set(a) & set(b)):
    pa, pb = a[n][2], b[n][2]
    diffs = []
    for k in sorted(set(pa) | set(pb)):
        if pa.get(k) != pb.get(k):
            va = int(pa[k].split("'h")[1], 16); vb = int(pb[k].split("'h")[1], 16)
            bits = [i for i in range((va ^ vb).bit_length()) if (va ^ vb) >> i & 1]
            diffs.append((k, bits))
            total += len(bits)
    if diffs:
        print(f"  {n} {a[n][1]}: " + "; ".join(f"{k} bit(s) {bits}" for k, bits in diffs))
print(f"INIT bits differing: {total}")
sys.exit(1 if total or moved or set(a) ^ set(b) else 0)
