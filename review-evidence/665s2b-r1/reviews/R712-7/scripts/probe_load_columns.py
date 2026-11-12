"""Probe: load_grade.findings refuses 1x1/1if by column name, in each column alone; and the selftest's
pin-only control is real (a findings() that grades the donor column alone lets it escape).
usage: python3 -I probe_load_columns.py <repo-root>"""
import copy, importlib, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
lg = importlib.import_module('load_grade')
fails = 0
def show(tag, found):
    print(f'{tag}:'); [print('   ', f) for f in found if f.startswith('1x1/1if')]
# (a) pin-only rise
pin = copy.deepcopy(lg.STATED_US); pin['1x1/1if']['record.aecp'] = 3000
f = lg.findings(root, pin=pin); show('pin rise (record.aecp=3000 at the pin)', f)
fails += not (any(' at the pin is over' in x for x in f) and not any('with tsn-c-stack#32 is over' in x for x in f))
# (b) donor-only rise
don = copy.deepcopy(lg.STATED_US_DONOR); don['1x1/1if']['record.acmp'] = 3000
f = lg.findings(root, table=don); show('donor rise (record.acmp=3000 with #32)', f)
fails += not (any('with tsn-c-stack#32 is over' in x for x in f) and not any(' at the pin is over' in x for x in f))
# (c) boundary: scale the pin column's record.srp until the load sits just at/above 0.70
def load_with(v):
    t = copy.deepcopy(lg.STATED_US); t['1x1/1if']['record.srp'] = v
    return sum(lg.load(root, '1x1/1if', t).values()), lg.findings(root, pin=t)
lo, hi = 0, 20000
while hi - lo > 1:
    mid = (lo + hi) // 2
    if load_with(mid)[0] > 0.70: hi = mid
    else: lo = mid
for v in (lo, hi):
    L, f = load_with(v); print(f'boundary record.srp={v}: pin load {L:.5f}, refused={any(" at the pin is over" in x for x in f)}')
    fails += (L > 0.70) != any(' at the pin is over' in x for x in f)
# (d) mutant: the gate as it was (donor column only) must let the selftest's pin-only control escape
orig = lg.COLUMNS
lg.COLUMNS = (orig[1],)
esc = lg.controls(root)
print('mutant donor-only COLUMNS: escaped controls =', esc)
fails += 'a rise at the pin alone' not in esc
lg.COLUMNS = tuple((n, c) for (n, _), (_, c) in zip(orig, orig[::-1]))   # names swapped onto the other column
esc = lg.controls(root)
print('mutant names swapped (informational, a SUGGESTION if empty): escaped controls =', esc)
held = lg.held(root); print('   its HELD lines:', held)
lg.COLUMNS = orig
print('RESULT', 'PASS' if fails == 0 else f'FAIL {fails}')
sys.exit(1 if fails else 0)
