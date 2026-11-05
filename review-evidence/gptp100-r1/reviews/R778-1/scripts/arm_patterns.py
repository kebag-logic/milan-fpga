#!/usr/bin/env python3
"""usage: arm_patterns.py <engine dir> : count every MUTATIONS edit pattern in
its target file (each must appear exactly once), and list the arm's size."""
import importlib.util, sys
from pathlib import Path
eng = Path(sys.argv[1]).resolve(); sys.path.insert(0, str(eng))
spec = importlib.util.spec_from_file_location("mutants", eng / "mutants.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
bad = 0
for name, fname, pat, rep, breaks in m.MUTATIONS:
    src = (m.HDL / fname).read_text(encoding="utf-8")
    for p, _ in m.edits_of(pat, rep):
        if src.count(p) != 1:
            bad += 1; print(f"BAD {name!r}: {src.count(p)} matches in {fname}")
names = [e[0] for e in m.MUTATIONS]
print(f"mutants: {len(m.MUTATIONS)} (+1 control = {len(m.MUTATIONS)+1} arm checks); "
      f"#100 controls: {len(m.P100_MUTATIONS)}; duplicate names: {len(names)-len(set(names))}; "
      f"patterns not matching exactly once: {bad}")
sys.exit(1 if bad else 0)
