#!/usr/bin/env python3
"""Run the eight original opportunity controls and seven ownership/anchor mutations."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'))
import selftest
import selftest_leaveall
import selftest_mutants

def checks():
    return selftest_leaveall.leave_all_checks(selftest.synthetic, selftest.SYS_HZ,
                                             selftest.CPU_HZ, selftest.tx_record)

assert all(ok for _, ok, _ in checks())
names = [n for n in selftest_mutants.MUTANTS if n.startswith('leaveall:') or
         n.startswith(('transmit: an MRPDU a timer owes timed from its run-out',
                       "transmit: the participant's join timer run out a centisecond early",
                       'transmit: a build that sends nothing late only',
                       'transmit: an expiry with no owner recorded',
                       'transmit: an unowned run-out'))]
assert len(names) == 15
for name in names:
    with selftest.mutated(name):
        failed = [n for n, ok, _ in checks() if not ok]
    assert failed, name
    print('CAUGHT', name)
    for check in failed:
        print('  ', check)
print('15 mutations caught, including all eight original controls; clean controls pass')
