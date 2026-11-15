#!/usr/bin/env python3
"""Each leg's AECP records by command: the most CPU cycles, its rule figure, the group and the count (record_classes.py's
reader). usage: record_top.py TREE RESULTS..."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'))
import record_classes as rc
for p in sys.argv[2:]:
    leg, _ = rc.read_leg(Path(p))
    top = {}
    for g, recs in leg.groups.items():
        for r in recs:
            k = (r.command, r.status)
            n, best = top.get(k, (0, None))
            top[k] = (n + 1, max(best or (0, ''), (r.cycles, g)))
    print(f'{p}: {leg.point} {leg.variant}')
    for (c, s), (n, (cy, g)) in sorted(top.items(), key=lambda kv: -kv[1][1][0])[:12]:
        print(f'  command {c if c is None else f"0x{c:04x}"} status {s}: {n} records, most {cy:,} cycles, '
              f'{rc.rule(cy, leg.cpu_hz)} us ({g})')
