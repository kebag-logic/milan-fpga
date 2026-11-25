#!/usr/bin/env python3
"""R931-1 probe: does the bind grade (tb/verilator/ctrl_service_budget/bind_save.py) hold what its text states?
Usage: probe_bind_grade.py <checkout>. Grades synthetic logs with the checkout's own self-test helpers."""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
for p in ('tb/verilator/ctrl_service_budget', 'scripts', 'tb/verilator/fw_service_budget', 'tb/tools', 'sw/litex'):
    sys.path.insert(0, str(root / p))
import selftest as m                                   # noqa: E402
import bind_save, selftest_bind as sb                  # noqa: E402
half = 640 * 1024 // 2
good = sb.container({0: sb.BOUND}, 6)
journal = good.ljust(half, b'\xff') + sb.container({}, 5).ljust(half, b'\xff')
op = bind_save.op('BIND_RX', 0, 0x9500)
# 1: a 'frame' group whose save is a whole commit (an erase), inside 250 ms
g = sb.graded(m, [op], [(good, 200.0)], journal, kind='frame')
print('frame group, its save WHOLE with an erase:', {k: g[k] for k in ('kind', 'saves', 'frames', 'erases')},
      'misses', bind_save.misses(g, 'save-bind-frame'))
# 2: a burst with erases
g = sb.graded(m, [op], [(good, 100.0), (good, 200.0)], journal, kind='burst')
print('burst group, every save WHOLE with an erase:', {k: g[k] for k in ('kind', 'saves', 'frames', 'erases')},
      'misses', bind_save.misses(g, 'save-bind-burst'))
