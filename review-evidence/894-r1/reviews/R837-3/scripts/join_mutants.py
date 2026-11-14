#!/usr/bin/env python3
"""Run the harness self-test's checks once, then each 'joins:' mutant (selftest_mutants.MUTANTS) against
them, as selftest.main does for every mutant (argv[1] = the tree)."""
import sys
sys.path.insert(0, sys.argv[1] + '/tb/verilator/ctrl_service_budget')
import grade, selftest, selftest_mutants
checks = selftest.checks()
bad = [n for n, ok, _ in checks if not ok]
print(f"checks: {len(checks)}, failing: {len(bad)} {bad[:3]}")
for n, ok, _ in checks:
    if 'join' in n or 'run-out' in n or 'horizon' in n:
        print(('PASS: ' if ok else 'FAIL: ') + n)
escaped = 0
for name in selftest_mutants.MUTANTS:
    if not name.startswith('joins'):
        continue
    with selftest.mutated(name):
        try:
            failed = [n for n, ok, _ in selftest.checks() if not ok]
        except (grade.Refusal, KeyError, ValueError, IndexError, TypeError, RuntimeError) as error:
            failed = [f'refused: {error}']
    print((f'MUTANT caught: {name}: {failed[0]}' if failed else f'MUTANT ESCAPED: {name}')[:260])
    escaped += not failed
print(f'join mutants escaped: {escaped}')
