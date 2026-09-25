#!/usr/bin/env python3
"""Derive the gsi-mutants campaign size from the driver itself and compare it
with the crflic-mutants convention the Makefile comment cites.

Usage: python3 campaign_counts.py <clone>
Prints, per driver, the MUTATIONS length, the elaborations the driver adds
beyond its prerequisite leg (one per mutant: the clean executable is reused
from the prerequisite build), and the leg runs the driver performs (the clean
control re-run plus one per mutant). Exit 0 when gsi-mutants is 8/8/9 and
crflic-mutants is 3/3/4 (the Makefile's own stated counts for it).
"""
import ast
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "tb/verilator/milan_dp"
want = {"gsi_mutants.py": (8, 8, 9), "crflic_mutants.py": (3, 3, 4)}
ok = True
for name, expect in want.items():
    src = (root / name).read_text()
    tree = ast.parse(src)
    n = next(len(node.value.elts) for node in tree.body
             if isinstance(node, ast.Assign)
             and any(getattr(t, "id", "") == "MUTATIONS" for t in node.targets))
    reuses_clean = "clean if clean.is_file() else build(" in src
    got = (n, n, n + 1)
    print(f"{name}: arms={got[0]} extra_elaborations={got[1]} runs={got[2]} "
          f"reuses_prerequisite_clean_build={reuses_clean} expected={expect}")
    ok &= got == expect and reuses_clean
mk = (root / "Makefile").read_text()
for line in mk.splitlines():
    if "more elaborations" in line or "runs of the" in line:
        print("Makefile:", line.strip())
print("RESULT", "OK" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
