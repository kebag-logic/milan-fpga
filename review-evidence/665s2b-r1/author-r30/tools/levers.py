"""Each single lever that alone takes 8x8/2if's long-window load in a column to 0.70 (section 13's list), by bisection on
load_grade.load: an SRP record (and its retained retry, stated at its cost), SRP's refill, a notice to the registered
controllers, AECP's refill, an ACMP record, ACMP's refill, ADP's refill, MAAP's refill, and the compute.
usage: python3 -I levers.py LANE [COLUMN: pin|donor]"""
import sys
from pathlib import Path

lane = Path(sys.argv[1])
sys.path.insert(0, str(lane / 'tb/verilator/ctrl_service_budget'))
import load_grade as lg  # noqa: E402

col = lg.STATED_US if (sys.argv[2] if len(sys.argv) > 2 else 'donor') == 'pin' else lg.STATED_US_DONOR
P = '8x8/2if'
real_contract = lg.contract


def total(table=None, refill=None):
    if refill:
        lg.contract = lambda root: dict(real_contract(root), refill=dict(real_contract(root)['refill'], **refill))
    try:
        return sum(lg.load(lane, P, table or col).values())
    finally:
        lg.contract = real_contract


def bisect(f, lo, hi, n=60):
    """The value at which f crosses 0.70, f falling from lo to hi."""
    for _ in range(n):
        mid = (lo + hi) / 2
        if f(mid) > 0.70:
            lo = mid
        else:
            hi = mid
    return hi


base = total()
print(f'{P} load {base:.4f} ({"pin" if col is lg.STATED_US else "with tsn-c-stack#32"})')


def with_cost(keys, v):
    t = {p: dict(r) for p, r in col.items()}
    for k in keys:
        t[P][k] = v
    return total(t)


for name, keys in (('an SRP record (and its retained retry)', ('record.srp', 'item.retained')),
                   ('a notice to 32 recipients', ('item.aecp.notice',)),
                   ('an ACMP record', ('record.acmp',))):
    now = col[P][keys[0]]
    if with_cost(keys, 0) > 0.70:
        print(f'{name}: no value closes it')
        continue
    v = bisect(lambda x: with_cost(keys, now - x), 0, now)
    v = now - v
    print(f'{name}: from {now} to {v:.1f} us ({(v - now) / now * 100:+.1f} %)')
for ch in ('srp', 'aecp', 'acmp', 'adp', 'maap'):
    now = real_contract(lane)['refill'][ch]
    if total(refill={ch: now * 1000}) > 0.70:
        print(f"{ch}'s refill alone cannot")
        continue
    v = bisect(lambda x: total(refill={ch: x}), now, now * 1000)
    print(f"{ch}'s refill: from {now} to {v:.2f} ms")
print(f'compute: {max(1.0, base / 0.70):.3f}x')
