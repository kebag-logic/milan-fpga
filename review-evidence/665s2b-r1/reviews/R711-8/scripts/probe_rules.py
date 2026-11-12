"""Reviewer probes (R711-8): plant wrong charges in rows_grade/load_grade in memory and report which checks refuse.
Run from tb/verilator/ctrl_service_budget of the reviewed clone: python3 -B <this> ."""
import math, sys
from pathlib import Path
sys.path.insert(0, '.')
import load_grade as L, rows_grade as r, flip_grade as F
root = Path('../../..').resolve()
def show(name, fn):
    try:
        print(name, '->', fn())
    except Exception as e:
        print(name, '-> EXC', type(e).__name__, e)
base = r.rows(root, '1x1/1if')['R4'][0]
print('head R4 1x1/1if', base, 'rule_findings', r.rule_findings(root))
plants = {
 'retry floor(W/10)+1 (one fewer)': ('retained_retries', lambda w, p, t: min(p, math.floor(w / t) + 1)),
 'retry floor(W/10)+3 (one more)': ('retained_retries', lambda w, p, t: min(p, math.floor(w / t) + 3)),
 'retry uncapped by passes': ('retained_retries', lambda w, p, t: math.floor(w / t) + 2),
 'srp window over whole W': ('srp_window', lambda w, i: w),
 'srp window less two records': ('srp_window', lambda w, i: max(0.0, w - 2 * i.c['record.aecp'] / 1000)),
 'retained in no row': ('RETAINED_ROWS', ()),
 'retained in R5 only': ('RETAINED_ROWS', ('R4', 'R5')),
}
for name, (attr, val) in plants.items():
    saved = getattr(r, attr); setattr(r, attr, val)
    try:
        w = r.rows(root, '1x1/1if')['R4'][0]
        f = r.rule_findings(root, ('1x1/1if',))
        print(f'{name}: R4 {w} (head {base}); rule_findings {len(f)}: {f[:1]}')
    finally:
        setattr(r, attr, saved)
# the column binding: swapped names, and the self-test's control
saved = L.COLUMNS
L.COLUMNS = (('at the pin', L.STATED_US_DONOR), ('with tsn-c-stack#32', L.STATED_US))
try:
    esc = L.controls(root)
    print('COLUMNS swapped: controls escaped', [e for e in esc], '; --check findings', L.findings(root))
    print(' held lines', L.held(root)[:2])
finally:
    L.COLUMNS = saved
L.COLUMNS = (('at the pin', L.STATED_US),)
try:
    print('COLUMNS one only: controls escaped', L.controls(root))
finally:
    L.COLUMNS = saved
print('head controls escaped', L.controls(root))
