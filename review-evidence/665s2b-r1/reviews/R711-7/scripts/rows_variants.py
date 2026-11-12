#!/usr/bin/env python3
"""Re-solve rows_grade's R4, R5 and R6 from a tree (argv[1]) with each reviewer correction applied to demand(), alone
and together, by patching demand()'s source text; prints W and the changed terms. Read-only on the tree."""
import inspect, sys, textwrap
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import rows_grade as rg
SRC = textwrap.dedent(inspect.getsource(rg.demand))
PATCHES = {
    # srp_mbx.c: at most one retained retry a centisecond (retry_spent, given back by the centisecond consumer)
    'retained-per-centisecond': ("out['item.retained'] = min(passes, srp_in) * c['item.retained']",
                                 "out['item.retained'] = min(passes, srp_in, ticks) * c['item.retained']"),
    # SRP's arrivals over the whole window, less the last AECP record's own work only
    'srp-arrivals-whole-window': ("draining = max(0.0, w_ms - out['aecp'] / 1000)",
                                  "draining = max(0.0, w_ms - c['record.aecp'] / 1000)"),
}
def build(names):
    src = SRC
    for n in names:
        old, new = PATCHES[n]
        assert src.count(old) == 1, n
        src = src.replace(old, new)
    ns = dict(vars(rg))
    exec(compile(src, f'<demand {names}>', 'exec'), ns)
    return ns['demand']
orig = rg.demand
for point in sys.argv[2:] or ['1x1/1if']:
    inp = rg.point_inputs(root, point)
    for names in ((), ('retained-per-centisecond',), ('srp-arrivals-whole-window',),
                  ('retained-per-centisecond', 'srp-arrivals-whole-window')):
        rg.demand = build(names) if names else orig
        out = []
        for row in rg.SOLVED:
            w, d = rg.solve(row, inp)
            out.append(f"{row} {w:.2f} (srp {d['srp']/1000:.2f}, item.retained {d['item.retained']/1000:.2f}, "
                       f"passes {d['passes']/1000/((inp.c['events_none']+inp.c['base'])/1000):.0f})")
        print(point, '+'.join(names) or 'as built', '|', '; '.join(out))
    rg.demand = orig
