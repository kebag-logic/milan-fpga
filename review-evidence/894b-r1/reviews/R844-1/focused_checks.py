"""Run focused shape, round, slice, and timer controls against a supplied checkout."""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import selftest
import selftest_round
import selftest_notice
import shape_costs

checks = selftest_round.round_checks(selftest.synthetic, selftest.SYS_HZ, selftest.CPU_HZ)
checks += selftest_notice.timer_checks(selftest.synthetic, selftest.tx_sequence)
for name, ok, detail in checks:
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else ': ' + str(detail)))
failed = sum(not ok for _, ok, _ in checks)
names = [n for n in selftest.selftest_mutants.MUTANTS if n.startswith(('shapes:', 'round:', 'transmit: THE TRANSMIT'))]
for name in names:
    with selftest.mutated(name):
        try:
            result = selftest_round.round_checks(selftest.synthetic, selftest.SYS_HZ, selftest.CPU_HZ)
            result += selftest_notice.timer_checks(selftest.synthetic, selftest.tx_sequence)
            caught = [n for n, ok, _ in result if not ok]
        except (ValueError, KeyError, RuntimeError, TypeError, IndexError) as exc:
            caught = [str(exc)]
    print(('CAUGHT ' if caught else 'ESCAPED ') + name + ': ' + '; '.join(caught[:2]))
    failed += not bool(caught)
print(f'{len(checks)} checks, {len(names)} mutations, {failed} failures')
raise SystemExit(bool(failed))
