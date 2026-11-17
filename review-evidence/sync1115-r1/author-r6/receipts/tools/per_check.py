"""per_check.py HARNESS: each LeaveAll mutant, which of selftest_leaveall's checks it fails (every check, not the first)."""
import sys
from contextlib import ExitStack
sys.path.insert(0, sys.argv[1])
import selftest, selftest_leaveall, selftest_mutants  # noqa: E401,E402
def fails():
    return [name for name, ok, _ in selftest_leaveall.leave_all_checks(
        selftest.synthetic, selftest.SYS_HZ, selftest.CPU_HZ, selftest.tx_record) if not ok]
print('unmutated failing:', fails())
for name, patches in selftest_mutants.MUTANTS.items():
    if not name.startswith(('leaveall:', 'transmit:')):
        continue
    with ExitStack() as st:
        for p in patches():
            st.enter_context(p)
        try:
            f = fails()
        except Exception as e:  # a mutant that raises is caught too
            f = [f'raised {type(e).__name__}']
    print(f'{name}\n  ' + '\n  '.join(f) if f else f'{name}\n  ESCAPED')
