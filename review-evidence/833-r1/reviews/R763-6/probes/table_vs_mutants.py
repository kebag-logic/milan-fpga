#!/usr/bin/env python3
"""Cross-check TESTING.md's cleanup table against MUTANTS.

Usage: python3 -I table_vs_mutants.py REPO_ROOT

Every mutant with a control must be named in exactly one row, and its control
must be one of that row's "Pinned by" controls. Mutants with no control must be
in no row. Every name in the table must be a MUTANTS key. Exit 1 on any mismatch.
"""
import ast
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
tree = ast.parse((root / "scripts/process_test_support.py").read_text())
mutants = next(ast.literal_eval(node.value) for node in tree.body
               if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "MUTANTS")
rows = []
for line in (root / "docs/testing/TESTING.md").read_text().splitlines():
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if len(cells) == 3 and cells[1].startswith("`owner_"):
        rows.append((cells[0][:60], set(re.findall(r"`([^`]+)`", cells[1])), re.findall(r"`([^`]+)`", cells[2])))
bad = []
named = {}
for text, controls, names in rows:
    for name in names:
        named.setdefault(name, []).append((text, controls))
for name in named:
    if name not in mutants:
        bad.append(f"{name}: in the table, not in MUTANTS")
for name, (control, _words, *_edits) in mutants.items():
    if name == "none":
        continue
    places = named.get(name, [])
    if control is None and places:
        bad.append(f"{name}: no control, but named in {len(places)} row(s)")
    if control is not None:
        if len(places) != 1:
            bad.append(f"{name}: control {control}, named in {len(places)} rows")
        elif control not in places[0][1]:
            bad.append(f"{name}: control {control} not among the row's {sorted(places[0][1])}")
print(f"{len(rows)} rows, {sum(len(n) for _t, _c, n in rows)} names, {len(mutants) - 1} mutants, "
      f"{sum(1 for k, v in mutants.items() if k != 'none' and v[0])} with a control")
for line in bad:
    print("MISMATCH " + line)
print("table vs MUTANTS: " + ("FAIL" if bad else "PASS"))
sys.exit(1 if bad else 0)
