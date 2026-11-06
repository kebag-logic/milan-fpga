#!/usr/bin/env python3
"""List every engine mutation-arm entry and check its pattern appears once.

usage: mutant_patterns.py <repo root>
Prints index, target file, pattern count(s) and name; exits 1 if any
pattern does not appear exactly once in its target at this tree.
"""
import importlib.util, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
eng = root / "tb/verilator/engine"
sys.path.insert(0, str(eng)); sys.path.insert(0, str(root / "tb/verilator"))
spec = importlib.util.spec_from_file_location("mutants", eng / "mutants.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
bad = 0
for i, (name, fname, pat, rep, breaks) in enumerate(m.MUTATIONS, 1):
    src = (root / "hdl" / fname).read_text(encoding="utf-8")
    counts = [src.count(p) for p, _ in m.edits_of(pat, rep)]
    ok = all(c == 1 for c in counts)
    bad += not ok
    print(f"{i:03d} {'ok ' if ok else 'BAD'} {fname} {counts} {name}")
print(f"{len(m.MUTATIONS)} mutants, {bad} with a pattern not exactly once")
sys.exit(1 if bad else 0)
