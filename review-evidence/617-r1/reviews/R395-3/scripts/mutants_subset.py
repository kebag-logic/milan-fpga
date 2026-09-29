#!/usr/bin/env python3
"""Run a subset of tb/verilator/capture_coherence/mutants.py, unmodified, so
the arm can be split across bounded foreground commands.

Usage: mutants_subset.py <suite_dir> <workdir> ITEM...
  ITEM = c:<leg> (a leg's clean control) | m:<index> (MUTATIONS[index]) | list
Each item prints the committed driver's own [PASS]/[FAIL] line.
"""
import sys
from pathlib import Path

suite = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(suite))
import mutants  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
passes = fails = 0
for item in sys.argv[3:]:
    if item == "list":
        for i, (leg, name, _, breaks) in enumerate(mutants.MUTATIONS):
            print(f"m:{i} [{leg}] {name} -> {breaks}")
        print("legs:", " ".join(f"c:{leg}" for leg in mutants.LEGS))
        continue
    kind, key = item.split(":", 1)
    if kind == "c":
        ok = mutants.clean_control(key, work)
    else:
        leg, name, edits, breaks = mutants.MUTATIONS[int(key)]
        ok = mutants.grade_mutant(leg, work, name, edits, breaks)
    sys.stdout.flush()
    passes += ok
    fails += not ok
print(f"\nsubset {' '.join(sys.argv[3:])}: {passes} PASS, {fails} FAIL")
sys.exit(1 if fails else 0)
