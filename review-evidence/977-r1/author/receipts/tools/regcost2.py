#!/usr/bin/env python3
"""regcost2.py UNIT_CYCLES REG_US LOG...: from CPU budget harness logs of the registering groups, each SRP record's
apply (srp_mbx:apply_receive outside the polls) past the unit, divided by the Talker values its charge counted
(srp_mbx:rx_charge's return: (charge - unit) / REG_US, the last charge before the apply), and THE SETTLE's run after
it (the first ctrl_app_srp:settle span after the apply that did work), divided the same. Prints the dearest of each and
of their sum per value, and each by the rule (plus 5 %, rounded up to 5 us at 100 cycles a microsecond)."""
import math
import sys
from bisect import bisect_left, bisect_right

unit, sinks = int(sys.argv[1]), int(sys.argv[2])
rule = lambda c: 5 * math.ceil(c / 100 * 1.05 / 5)
best = dict(record=(0, None), settle=(0, None), all=(0, None))
for log in sys.argv[3:]:
    spans = {}
    for line in open(log, errors='replace'):
        if line.startswith('SPAN '):
            p = line.split()
            if len(p) != 6:
                continue
            spans.setdefault(p[5], []).append((int(p[2]), int(p[3]), int(p[4], 16)))
    for v in spans.values():
        v.sort()
    first, last = spans.get('adp_mbx:on_poll', []), spans.get('ctrl_app_srp:deliver', [])
    charges = spans.get('srp_mbx:rx_charge', [])
    settles = [s for s in spans.get('ctrl_app_srp:settle', []) if s[2] != 0]
    cstarts = [c[0] for c in charges]
    sstarts = [s[0] for s in settles]
    for s, c, _ in spans.get('srp_mbx:apply_receive', []):
        values = sinks
        if c <= unit:
            continue
        j = bisect_right(sstarts, s)
        settle = settles[j][1] if j < len(settles) else 0
        for key, cycles in (('record', (c - unit) / values), ('settle', settle / values),
                            ('all', (c - unit + settle) / values)):
            if cycles > best[key][0]:
                best[key] = (cycles, (log.split('/')[-2], s, c, values, settle))
for key, (cycles, where) in best.items():
    print(f'{key}: {cycles:,.0f} cycles a Talker value, {rule(cycles)} us by the rule; {where}')
