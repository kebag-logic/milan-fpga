#!/usr/bin/env python3
"""Import a gen_ucode.py and print its occupied ROM word intervals and the
entry-point constants that start inside each, so overlaps and free runs can be
read directly.  usage: rom_occupancy.py PATH/TO/gen_ucode.py"""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("g", sys.argv[1])
g = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0]]
spec.loader.exec_module(g)
occ = sorted(g.occupied)
iv, s = [], None
for i in occ:
    if s is None: s = p = i
    elif i == p + 1: p = i
    else: iv.append((s, p)); s = p = i
iv.append((s, p))
names = {}
for k, v in vars(g).items():
    if k.startswith("E_") and isinstance(v, int): names.setdefault(v, []).append(k)
for a, b in iv:
    ent = [f"{n}@{x}" for x in range(a, b + 1) for n in names.get(x, [])]
    print(f"{a:5d}..{b:5d} ({b-a+1:3d}) {' '.join(ent)}")
print("placed entries:", len(g.placed))
