"""Run portable controls and all transmit/LeaveAll mutants: CHECKOUT argument."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(sys.argv[1]).resolve() / 'tb/verilator/ctrl_service_budget'))
import selftest
import selftest_mutants

checks = selftest.checks()
bad = [(n, d) for n, ok, d in checks if not ok]
print(f'BASELINE: {len(checks)} checks, {len(bad)} failures')
for n, d in bad:
    print('FAIL:', n, d)
assert not bad
selected = [n for n in selftest_mutants.MUTANTS if n.startswith(('transmit:', 'leaveall:'))]
for name in selected:
    with selftest.mutated(name):
        failed = [(n, d) for n, ok, d in selftest.checks() if not ok]
    assert failed, name
    print('CAUGHT:', name)
    for n, d in failed:
        print('  CHECK:', n)
print(f'PASS: {len(selected)} focused mutants caught by controls, no exception catches')
