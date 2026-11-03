#!/usr/bin/env python3
"""Cross-check the cleanup table in docs/testing/TESTING.md against MUTANTS.

usage: python3 -I -B table_check.py <tree>
Every mutant with a control must be in at least one row whose controls include it;
every mutant with none must be in no row; every name in a row must be in MUTANTS.
Prints each row's controls and mutants, then every mismatch; exit 1 on any.
"""
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / "scripts"))
import process_test_support as pts  # noqa: E402

text = (tree / "docs/testing/TESTING.md").read_text()
start = text.index("| Stated cleanup behaviour |")
rows = []
for line in text[start:].splitlines()[2:]:
    if not line.startswith("|"):
        break
    behaviour, controls, mutants = [cell.strip() for cell in line.strip("|").split("|")]
    rows.append((behaviour, re.findall(r"`([^`]+)`", controls), re.findall(r"`([^`]+)`", mutants)))
bad = []
named = {}
for number, (behaviour, controls, mutants) in enumerate(rows, 1):
    print(f"row {number}: {controls} <- {mutants}\n    {behaviour[:110]}")
    for name in mutants:
        named.setdefault(name, []).append(number)
        if name not in pts.MUTANTS:
            bad.append(f"row {number}: {name} is not in MUTANTS")
        elif pts.MUTANTS[name][0] not in controls:
            bad.append(f"row {number}: {name} names {pts.MUTANTS[name][0]}, not one of {controls}")
for name, (control, *_rest) in pts.MUTANTS.items():
    if name == "none":
        continue
    if control and name not in named:
        bad.append(f"{name} ({control}) is in no row")
    if not control and name in named:
        bad.append(f"{name} names no control but is in rows {named[name]}")
print(f"{len(rows)} rows, {len(named)} mutants named in rows, {len(pts.MUTANTS) - 1} in MUTANTS")
for line in bad:
    print("MISMATCH " + line)
sys.exit(1 if bad else 0)
