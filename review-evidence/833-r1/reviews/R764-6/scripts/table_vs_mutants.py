#!/usr/bin/env python3
"""Cross-check the cleanup table in TESTING.md against MUTANTS (review probe, read-only).

Usage: python3 -I table_vs_mutants.py <repo>
For every table row: each named mutant exists, names a control, and that control is in the
row's "Pinned by" cell. For every MUTANTS entry with a control: some row names it. Each
mutant edit matches the product exactly once.
"""
import importlib.util
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("pts", repo / "scripts/process_test_support.py")
sys.path.insert(0, str(repo / "scripts"))
pts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pts)
product = (repo / "scripts/owned_process.py").read_text()
text = (repo / "docs/testing/TESTING.md").read_text().splitlines()
rows = [l for l in text if l.startswith("| ") and "`owner_" in l]
bad = 0
named = {}
for i, row in enumerate(rows, 1):
    cells = [c.strip() for c in row.strip("|").split("|")]
    controls = set(re.findall(r"`(owner_\w+)`", cells[1]))
    mutants = re.findall(r"`([\w.\-]+)`", cells[2])
    for m in mutants:
        named.setdefault(m, []).append(i)
        if m not in pts.MUTANTS:
            print(f"row {i}: mutant {m} not in MUTANTS"); bad += 1; continue
        c = pts.MUTANTS[m][0]
        if c not in controls:
            print(f"row {i}: mutant {m} names control {c}, row pins {sorted(controls)}"); bad += 1
    used = {pts.MUTANTS[m][0] for m in mutants if m in pts.MUTANTS}
    for c in controls - used:
        print(f"row {i}: control {c} is listed as pinning but no listed mutant targets it")
    print(f"row {i}: {len(mutants)} mutants, controls {sorted(controls)}")
for m, entry in pts.MUTANTS.items():
    control = entry[0]
    if control and m not in named:
        print(f"MUTANTS {m} ({control}) is in no table row"); bad += 1
    if not control and m != "none" and m in named:
        print(f"MUTANTS {m} names no control but is in rows {named[m]}"); bad += 1
    for old, new in entry[2:]:
        n = product.count(old)
        if n != 1:
            print(f"MUTANTS {m}: edit matches {n} times"); bad += 1
for m, r in named.items():
    if len(r) > 1:
        print(f"mutant {m} in rows {r}")
print(f"rows={len(rows)} mutants={len(pts.MUTANTS)} with-control={sum(1 for e in pts.MUTANTS.values() if e[0])}"
      f" no-control={[m for m, e in pts.MUTANTS.items() if not e[0]]} bad={bad}")
sys.exit(1 if bad else 0)
