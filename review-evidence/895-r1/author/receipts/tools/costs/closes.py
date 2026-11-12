#!/usr/bin/env python3
"""What alone closes 8x8/2if's load in the column with tsn-c-stack#32 to 0.70 (SPLIT_CONTROL_MEMORY section 13's list),
by load_grade.load with each other cost held: an SRP record (its retry at its cost), SRP's, AECP's and ACMP's refill,
and the compute. usage: closes.py TREE"""
import sys
from pathlib import Path
tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import load_grade as lg  # noqa: E402
P, CEIL = '8x8/2if', 0.70
base_table = lg.STATED_US_DONOR
total = lambda table=None, refill=None: sum(_load(table, refill).values())
real_contract = lg.contract


def _load(table, refill):
    if refill:
        lg.contract = lambda root: dict(real_contract(root), refill=dict(real_contract(root)['refill'], **refill))
    try:
        return lg.load(tree, P, table or base_table)
    finally:
        lg.contract = real_contract


def bisect(f, lo, hi):
    """The v in [lo, hi] at which the monotone f crosses CEIL."""
    rising = f(hi) > f(lo)
    for _ in range(80):
        mid = (lo + hi) / 2
        over = f(mid) > CEIL
        lo, hi = (lo, mid) if over == rising else (mid, hi)
    return (lo + hi) / 2


now = total()
print(f'load {now:.4f}')
c = dict(base_table[P])
x = bisect(lambda v: total({**base_table, P: {**c, 'record.srp': v, 'item.retained': v}}), 0, c['record.srp'])
print(f"an SRP record {c['record.srp']} -> {x:.0f} us ({(x / c['record.srp'] - 1) * 100:.1f} %)")
r0 = real_contract(tree)['refill']
for ch in ('srp', 'aecp', 'acmp', 'adp', 'maap'):
    f = lambda v: total(refill={ch: v})
    if f(1e9) > CEIL:
        print(f'{ch} refill alone cannot')
        continue
    v = bisect(f, r0[ch], 1e6)
    print(f"{ch} refill {r0[ch]} -> {v:.2f} ms ({1000 / r0[ch]:.0f} to {1000 / v:.0f} records a second)")
print(f'compute {now / CEIL:.2f}x')
