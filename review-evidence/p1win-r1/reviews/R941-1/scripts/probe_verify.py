#!/usr/bin/env python3
"""R941-1 probe: a save's verify coverage through the head's bind grade (PR #1017, PR #1014 R932-1 F2).

Usage: probe_verify.py <clone>. Builds synthetic logs with the head's own self-test helpers and grades them with the
head's bind_save/save_grade. Each case states whether the save must be durable. Exit 0 when every case agrees.
"""
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(clone / 'tb/verilator/ctrl_service_budget'))

import bind_save  # noqa: E402
import grade  # noqa: E402
import selftest as m  # noqa: E402
import selftest_bind as sb  # noqa: E402

ms = m.SYS_HZ // 1000
IMAGE = sb.IMAGE
ops = [bind_save.op('BIND_RX', 0, 0x9500)]
one = sb.container({0: sb.BOUND}, 2)


def rows(verify=None, blank=None):
    return sb.graded(m, 'idle', ops, {0x9500: 10.0}, sb.save(ms, one, 110, verify=verify, blank=blank),
                     cut=sb.journal(one))


def durable(g):
    return g['rows'][0]['ms'] is not None and not g['faults']


half = IMAGE // 2
cases = [
    # name, verify runs (offset, bytes), want durable
    ('whole container in one run after the last page', None, True),
    ('halves in reverse order', [(half, IMAGE - half), (0, half)], True),
    ('all but the last 4 bytes (a missing verify tail)', [(0, IMAGE - 4)], False),
    ('overlapping runs whose byte sum exceeds the image but leave a gap', [(0, half + 64), (64, half)], False),
    ('only 4 bytes after the pages, the blank check read the whole slot before them (R932-1 F2 shape)',
     [(0, 4)], False),
    ('the last page only, read three times', [(IMAGE - 256, 256)] * 3, False),
]
bad = 0
for name, verify, want in cases:
    g = rows(verify)
    got = durable(g)
    ok = got == want
    bad += not ok
    print(f"{'PASS' if ok else 'FAIL'}: {name}: durable={got} want={want} ms={g['rows'][0]['ms']} "
          f"faults={len(g['faults'])}")
# a run of reads that straddles a page program must be refused, never counted
why = sb.refused(lambda: rows([(0, 4)], blank=(0, IMAGE)))
ok = 'spans a write of the device' in why
bad += not ok
print(f"{'PASS' if ok else 'FAIL'}: a whole-slot run from the blank check to after the pages is refused: {why[:90]}")
print(f'probe_verify: {len(cases) + 1} cases, {bad} disagreement(s)')
sys.exit(1 if bad else 0)
