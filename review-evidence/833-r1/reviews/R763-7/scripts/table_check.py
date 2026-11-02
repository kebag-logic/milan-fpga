#!/usr/bin/env python3
"""Each cleanup-table row's mutants exist and are bound to a control the row lists (review probe).

Usage: python3 -I table_check.py <repo>
"""
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "scripts"))
import process_test_support as pts  # noqa: E402

text = (repo / "docs/testing/TESTING.md").read_text()
start = text.index("| Stated cleanup behaviour |")
rows = [line for line in text[start:].split("\n\n")[0].splitlines()[2:]]
bad, listed = 0, set()
for n, row in enumerate(rows, 1):
    cells = [cell.strip() for cell in row.strip("|").split(" | ")]
    controls = set(re.findall(r"`(owner_\w+)`", cells[1]))
    mutants = re.findall(r"`([\w.-]+)`", cells[2])
    for name in mutants:
        listed.add(name)
        if name not in pts.MUTANTS:
            print(f"row {n}: {name}: NOT A MUTANT"); bad += 1; continue
        control = pts.MUTANTS[name][0]
        ok = control in controls
        bad += not ok
        print(f"row {n}: {name} -> {control} {'ok' if ok else 'NOT LISTED ON ROW ' + str(sorted(controls))}")
unbound = sorted(name for name, entry in pts.MUTANTS.items() if entry[0] and name not in listed and name != "none")
print(f"bound mutants on no row: {unbound}")
nulls = {name: entry[1] for name, entry in pts.MUTANTS.items() if entry[0] is None}
for name, why in nulls.items():
    print(f"unbound by design: {name}: {why}")
print(f"table check: {len(rows)} rows, {len(listed)} listed mutants, {bad} problems")
sys.exit(1 if bad else 0)
