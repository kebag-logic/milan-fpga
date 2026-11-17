#!/usr/bin/env python3
"""Round 14's new control and mutant at a tree, by name. flip_grade.check_held_control at the tree's wiring (refused),
then under the harness mutant that leaves tx_held out of --check (selftest.mutated): every flip check that fails, and
whether the three earlier controls (tx_held_controls, which call tx_held directly) stay refused. Read only.
usage: python3 -I check_held_mutant.py TREE"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import flip_grade  # noqa: E402
import selftest  # noqa: E402
import selftest_mutants  # noqa: E402

NAME = "flip: --check does not call tx_held, so 8x8/1if's THE TRANSMIT figure goes unheld"
head = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
print(f'# the --check control and its harness mutant at {head}; {len(selftest_mutants.MUTANTS)} harness mutants')
print(f'{flip_grade.CHECK_HELD_CONTROL}, at the wiring: {flip_grade.check_held_control(root) or "refused"}')
with selftest.mutated(NAME):
    failing = [(n, d) for n, ok, d in flip_grade.flip_checks() if not ok]
    direct = flip_grade.tx_held_controls(root)
print(f'under the mutant "{NAME}":')
for n, d in failing:
    print(f'  FAIL: {n} ({d})')
print(f'  the three earlier controls: {"refused" if not direct else "escaped: " + ", ".join(direct)}')
print(f'after the mutant: {flip_grade.check_held_control(root) or "refused"}')
ok = len(failing) == 1 and failing[0][0] == f'the flip check refuses {flip_grade.CHECK_HELD_CONTROL}' and not direct
print(f'RESULT: {"PASS: the mutant is caught by the new check alone" if ok else "FAIL"}')
sys.exit(0 if ok else 1)
