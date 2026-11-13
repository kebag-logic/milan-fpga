# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer-owned: compare two images' symbol tables (layout_probe output, `nm -S -n`, address size type name) and
# report which symbols moved or changed size, and whether every symbol placed after ANCHOR keeps its address.
# usage: layout_compare.py A.syms B.syms ANCHOR
import sys


def table(path):
    out = {}
    for line in open(path):
        addr, size, _kind, name = line.split()
        out.setdefault(name, (int(addr, 16), int(size, 16)))
    return out


a, b, anchor = table(sys.argv[1]), table(sys.argv[2]), sys.argv[3]
common = sorted(set(a) & set(b), key=lambda n: a[n][0])
moved = [n for n in common if a[n][0] != b[n][0]]
resized = [n for n in common if a[n][1] != b[n][1]]
after = [n for n in common if a[n][0] > a[anchor][0]]
after_moved = [n for n in after if a[n][0] != b[n][0]]
print(f"symbols {len(common)} only-A {len(set(a) - set(b))} only-B {len(set(b) - set(a))}")
print(f"resized {len(resized)}: " + ", ".join(f"{n} {a[n][1]:#x}->{b[n][1]:#x}" for n in resized))
print(f"moved {len(moved)}" + ("" if not moved else f" (first: {moved[0]} {a[moved[0]][0]:#x}->{b[moved[0]][0]:#x})"))
print(f"after {anchor}: {len(after)} symbols, {len(after_moved)} moved")
