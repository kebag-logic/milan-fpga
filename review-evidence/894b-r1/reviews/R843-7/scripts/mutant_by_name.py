#!/usr/bin/env python3
"""Reviewer probe: the round-14 harness mutant at TREE, by name. Counts the harness mutants, then runs the flip
checks (flip_grade.flip_checks) at the tree's wiring and under the mutant, and lists each failing check by name.
Read only. usage: python3 -I mutant_by_name.py TREE"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import flip_grade  # noqa: E402
import selftest  # noqa: E402
import selftest_mutants  # noqa: E402

NAME = "flip: --check does not call tx_held, so 8x8/1if's THE TRANSMIT figure goes unheld"
print(f'harness mutants: {len(selftest_mutants.MUTANTS)}; this one listed: {NAME in selftest_mutants.MUTANTS}')
base = [(n, d) for n, ok, d in flip_grade.flip_checks() if not ok]
print(f'at the wiring: {len(base)} failing flip check(s)')
with selftest.mutated(NAME):
    failing = [(n, d) for n, ok, d in flip_grade.flip_checks() if not ok]
print(f'under the mutant: {len(failing)} failing flip check(s)')
for n, d in failing:
    print(f'  FAIL: {n} ({d})')
after = [(n, d) for n, ok, d in flip_grade.flip_checks() if not ok]
print(f'after the mutant: {len(after)} failing flip check(s)')
want = f'the flip check refuses {flip_grade.CHECK_HELD_CONTROL}'
ok = not base and not after and [n for n, _ in failing] == [want]
print(f'RESULT: {"PASS: caught by that check alone" if ok else "FAIL"}')
sys.exit(0 if ok else 1)
