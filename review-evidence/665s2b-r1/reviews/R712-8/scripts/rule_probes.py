#!/usr/bin/env python3
"""Reviewer probes: plant wrong charges in rows_grade.demand's rules (in-process, no file edit) and report whether
rows_grade.rule_findings refuses each, and how 1x1/1if R4 moves. Usage: rule_probes.py <repo root>"""
import math, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import rows_grade as r
base_rr, base_sw, base_rows = r.retained_retries, r.srp_window, r.RETAINED_ROWS
def R4():
    return r.rows(root, '1x1/1if')['R4'][0]
plants = {
 'retries one fewer (no retry before the first centisecond)': ('rr', lambda w, p, t: min(p, math.floor(w / t) + 1)),
 'retries one more': ('rr', lambda w, p, t: min(p, math.floor(w / t) + 3)),
 'retries once a pass (round-28 rule)': ('rr', lambda w, p, t: p),
 'retries not capped by passes': ('rr', lambda w, p, t: math.floor(w / t) + 2),
 'retries zero': ('rr', lambda w, p, t: 0),
 'SRP window the whole W': ('sw', lambda w, i: w),
 'SRP window less two records': ('sw', lambda w, i: max(0.0, w - 2 * i.c['record.aecp'] / 1000)),
 'SRP window less the AECP burst (round-28 rule)': ('sw', lambda w, i: max(0.0, w - i.rate['aecp'][0] * i.c['record.aecp'] / 1000)),
 'retries also in R5': ('rows', ('R4', 'R5')),
 'retries in no row': ('rows', ()),
}
print('head: R4 1x1/1if', R4(), 'rule_findings', r.rule_findings(root))
for name, (kind, val) in plants.items():
    r.retained_retries, r.srp_window, r.RETAINED_ROWS = base_rr, base_sw, base_rows
    if kind == 'rr': r.retained_retries = val
    elif kind == 'sw': r.srp_window = val
    else: r.RETAINED_ROWS = val
    f = r.rule_findings(root)
    print(f"{'REFUSED' if f else 'ESCAPED'} | {name} | R4 1x1/1if {R4()} | {len(f)} findings | {f[0] if f else ''}")
r.retained_retries, r.srp_window, r.RETAINED_ROWS = base_rr, base_sw, base_rows
orig = r.EXCLUDED
r.EXCLUDED = orig[1:]
f = r.rule_findings(root); print(f"{'REFUSED' if f else 'ESCAPED'} | COUNTERS_CHANGED dropped from EXCLUDED | {f[:1]}")
r.EXCLUDED = orig + ('TICK',)
f = r.rule_findings(root); print(f"{'REFUSED' if f else 'ESCAPED'} | TICK both counted and excluded | {f[:1]}")
