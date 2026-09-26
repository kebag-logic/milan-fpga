#!/usr/bin/env python3
"""Apply the parent's Rule 12 per-module scan to every processor *.py.

Usage: parent_idiom_scan.py <parent-scripts-dir> <base-tree> <head-tree>

<parent-scripts-dir> holds check_py_idiom.py, code_quality_scope.py and
py_idiom.budget fetched from kebag-logic/milan-fpga at dev 831f94f4. Only the
gate's pure per-file `scan()` is called (no parent tree, no bank); the budget's
ratchets for the two signature/docstring rows are 0, so any non-zero count in a
processor module fails the parent gate once that module is pinned.
"""
import importlib.util
import sys
from pathlib import Path

GATE_DIR, BASE, HEAD = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(GATE_DIR))
spec = importlib.util.spec_from_file_location("gate", GATE_DIR / "check_py_idiom.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

budget = gate.parse_budget((GATE_DIR / "py_idiom.budget").read_text())
print("parent budget:", {k: budget.get(k) for k in gate.RATCHETED})
worst = 0
for label, tree in (("base", BASE), ("head", HEAD)):
    totals = dict.fromkeys(gate.RATCHETED + gate.REFUSED, 0)
    for path in sorted(tree.rglob("*.py")):
        rel = path.relative_to(tree).as_posix()
        counts, sites = gate.scan(path.read_text(), f"protocol-processor/{rel}")
        for key, value in counts.items():
            totals[key] += value
        nonzero = {k: v for k, v in counts.items() if v}
        if nonzero:
            print(f"{label}  {rel}: {nonzero}")
            for key in ("unannotated public function", "undocumented public function",
                        *gate.REFUSED):
                for lineno, detail in sites.get(key, []):
                    print(f"      {key} :{lineno} {detail}")
    print(f"{label} totals (non-zero): {{{', '.join(f'{k!r}: {v}' for k, v in totals.items() if v)}}}")
    if label == "head":
        worst = totals["unannotated public function"] + totals["undocumented public function"]
sys.exit(1 if worst else 0)
