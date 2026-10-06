#!/usr/bin/env python3
"""Static plant check of every mutant arm that builds tb/pp_top or a file the
two merges into PR #164 changed (R502-2).

Text-edit drivers (notify, acmp, d3, gsi): each (file, old) must occur exactly
the number of times the driver requires. Patch drivers (aecp, aecp_dispatch,
ctr, adp_engine, maap, srp_top): every listed patch must pass `git apply
--check` against TREE. Nothing is built; this only shows that every arm still
plants at TREE. Usage: plant_check.py TREE
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
bad = 0
total = 0


def load(rel):
    spec = importlib.util.spec_from_file_location(rel.replace("/", "_"), tree / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str((tree / rel).parent))
    sys.path.insert(0, str(tree / "tb/common"))
    spec.loader.exec_module(mod)
    return mod


def text_edits(rel):
    global bad, total
    mod = load(rel)
    for m in mod.MUTANTS:
        total += 1
        for edit in m.edits:
            f, old = edit[0], edit[1]
            n = (tree / f).read_text().count(old)
            if n != 1:
                bad += 1
                print(f"REFUSE {rel} {m.name}: {f} anchor occurs {n} times")
    print(f"{rel}: {len(mod.MUTANTS)} arms checked")


def gsi(rel):
    global bad, total
    mod = load(rel)
    muts = mod.mutations()
    for name, f, old, _new, sites, _check in muts:
        total += 1
        n = (tree / f).read_text().count(old)
        if n != sites:
            bad += 1
            print(f"REFUSE {rel} {name}: {f} anchor occurs {n} times, wants {sites}")
    print(f"{rel}: {len(muts)} arms checked")


def patches(rel):
    global bad, total
    mod = load(rel)
    names = set()
    for row in mod.MUTANTS:
        names.add(row[1] if isinstance(row, (tuple, list)) and len(row) > 1 and
                  isinstance(row[1], str) and (mod.PATCHES / (row[1] + ".patch")).exists()
                  else row[0])
    for name in sorted(names):
        total += 1
        p = mod.PATCHES / (name + ".patch")
        r = subprocess.run(["git", "apply", "--check", str(p)], cwd=tree,
                           capture_output=True, text=True)
        if r.returncode != 0:
            bad += 1
            print(f"REFUSE {rel} {name}: {r.stderr.strip()}")
    print(f"{rel}: {len(names)} patches checked")


for rel in ("tb/pp_top/notify_mutants.py", "tb/pp_top/acmp_mutants.py",
            "tb/pp_top/d3_mutants.py"):
    text_edits(rel)
gsi("tb/pp_top/gsi_mutants.py")
for rel in ("tb/pp_top/aecp_mutants.py", "tb/pp_top/aecp_dispatch_mutants.py",
            "tb/pp_top/ctr_mutants.py", "tb/adp_engine/mutants.py", "tb/maap/mutants.py"):
    patches(rel)
print(f"plant check: {total} arms, {bad} refused")
sys.exit(1 if bad else 0)
