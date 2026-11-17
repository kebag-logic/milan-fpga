"""Reviewer probe: re-run the self-test's transmit and LeaveAll mutants alone and list every check each one fails.

Usage: python3 -I -B probe_mutants.py <checkout>/tb/verilator/ctrl_service_budget
For each mutant in selftest_mutants.MUTANTS whose name starts 'transmit:' or 'leaveall:', applies it with
selftest.mutated and runs selftest.checks(); prints CAUGHT with the failing checks' names, or ESCAPED.
Also runs the unmutated checks once and requires every one to pass.
"""
import sys

sys.path.insert(0, sys.argv[1])
import grade  # noqa: E402
import selftest  # noqa: E402
import selftest_mutants  # noqa: E402

base = [(n, ok) for n, ok, _ in selftest.checks()]
print(f"unmutated: {len(base)} checks, {sum(not ok for _, ok in base)} failing")
bad = sum(not ok for _, ok in base)
names = [n for n in selftest_mutants.MUTANTS if n.startswith(('transmit:', 'leaveall:'))]
print(f"total mutants: {len(selftest_mutants.MUTANTS)}; transmit/leaveall mutants: {len(names)}")
for name in names:
    with selftest.mutated(name):
        try:
            failed = [n for n, ok, _ in selftest.checks() if not ok]
        except (grade.Refusal, KeyError, ValueError, IndexError, TypeError, RuntimeError) as error:
            failed = [f'refused: {error}']
    if failed:
        print(f"CAUGHT {name}")
        for f in failed:
            print(f"    by: {f[:200]}")
    else:
        print(f"ESCAPED {name}")
        bad += 1
print(f"probe: {bad} problems")
sys.exit(1 if bad else 0)
