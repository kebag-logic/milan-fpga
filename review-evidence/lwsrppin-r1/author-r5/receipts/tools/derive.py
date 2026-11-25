#!/usr/bin/env python3
"""derive.py LANE: each held-egress row's figure as egress_ledger.py derives it, beside the rule computed apart in
Decimal and the ruling's expected figure, with the image that sets it."""
import runpy
import sys
from decimal import ROUND_CEILING, Decimal

g = runpy.run_path(f'{sys.argv[1]}/tb/verilator/ctrl_service_budget/egress_ledger.py')
EXPECTED = {'backlog.owed.if0': 64.31, 'backlog.owed_behind0.if0': 64.51, 'backlog.owed_behind1.if0': 64.71,
            'backlog.owed_behind2.if0': 64.91, 'backlog.owed_behind3.if0': 65.11,
            'backlog-owed.service.acmp.last.if0': 63.29, 'backlog-owed.service.aecp.last.if0': 63.23}
names = ('MERGED', 'COMPOSED', 'LISTENED', 'TRAIN', 'PINNED')
hold = g['HOLD_MS']
print(f'hold {hold} ms (scenario.py); figure = hold + (largest - hold) x 1.05, rounded up to 0.01 ms')
print('| Row | Largest, ms | Set by | Service x 1.05, ms | Tool figure | Rule apart (Decimal) | Ruling expects | Equal |')
print('|---|---:|---|---:|---:|---:|---:|---|')
bad = 0
for row, ms in g['MEASURED']['8x8-1if'].items():
    by = [n for n in names if g[n][row] == ms]
    svc = (Decimal(str(ms)) - hold) * Decimal('1.05')
    rule = float(hold + svc.quantize(Decimal('0.01'), ROUND_CEILING))
    tool = g['LEDGER']['8x8-1if'][row]
    ok = tool == rule == EXPECTED[row]
    bad += not ok
    print(f'| `{row}` | {ms:.5f} | {",".join(by)} | {svc} | {tool} | {rule} | {EXPECTED[row]} | {"yes" if ok else "NO"} |')
print(f'RESULT: {"all 7 equal" if not bad else f"{bad} differ"}')
sys.exit(1 if bad else 0)
