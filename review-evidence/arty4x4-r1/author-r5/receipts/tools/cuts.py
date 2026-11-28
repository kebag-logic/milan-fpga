"""The cost cuts a 4x4/1if row at 80 MHz needs (round 2, desk): (1) the uniform cut of every measured cost, by
bisection; (2) a greedy smallest set: each step cuts, by 5 % of its measured cycles, the one stated cost whose cut
most narrows the gap to a qualifying row, until a candidate qualifies by the unchanged rule. The gap of a search is
the least, over its candidates, of the worst ratio of ACMP, txL and last notice to their owner bounds.
usage: cuts.py N MHZ OUT.json   (cwd = checkout root)"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import whatif

n, mhz, out = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
cyc, retry, _ = whatif.cycles_at(n)
KEYS = [k for k, v in cyc.items() if v > 0 and k != 'share'] + ['retry.' + k for k in retry]


def evaluate(scale):
    res = whatif.search(n, mhz, scale)
    q = [r for r in res['candidates'] if r['qualifies']]
    ok = bool(q) and res['load'] <= 0.70 and res['share_ok']
    gap = min(whatif.excess(r) for r in res['candidates'])
    return ok, gap, res


# (1) uniform
lo, hi = 0.5, 1.0
assert evaluate({k: lo for k in KEYS})[0], 'even a 50 % cut of every cost leaves no row'
while hi - lo > 0.0025:
    mid = (lo + hi) / 2
    if evaluate({k: mid for k in KEYS})[0]:
        lo = mid
    else:
        hi = mid
uniform = lo
print('UNIFORM keep', round(uniform, 4), 'cut', round(100 * (1 - uniform), 2), '%', flush=True)

# (2) greedy
scale, steps = {}, []
ok, gap, res = evaluate(scale)
while not ok:
    best = None
    for k in KEYS:
        if scale.get(k, 1.0) <= 0.5 + 1e-9:
            continue
        trial = {**scale, k: round(scale.get(k, 1.0) - 0.05, 4)}
        t_ok, t_gap, _ = evaluate(trial)
        key = (not t_ok, t_gap)
        if best is None or key < best[0]:
            best = (key, k, trial, t_ok, t_gap)
    _, k, scale, ok, gap = best
    steps.append(dict(key=k, keep=scale[k], gap=gap, qualifies=ok))
    print('STEP', k, scale[k], round(gap, 4), ok, flush=True)
ok, gap, res = evaluate(scale)
summary = whatif.summary(res)
base_c, base_r, _ = whatif.costs_us(cyc, retry, mhz)
cut_c, cut_r, _ = whatif.costs_us(cyc, retry, mhz, scale)
table = []
for k, keep in sorted(scale.items(), key=lambda kv: kv[1]):
    if k.startswith('retry.'):
        a, b = base_r[k[6:]], cut_r[k[6:]]
    else:
        a, b = base_c[k], cut_c[k]
    table.append(dict(cost=k, keep=keep, stated_us=a, needed_us=b, cut_us=a - b, cut_pct=round(100 * (1 - keep), 1)))
out.write_text(json.dumps(dict(n=n, mhz=mhz, uniform_keep=uniform, greedy=table, steps=steps, row=summary), indent=1))
print(json.dumps(dict(uniform_keep=uniform, greedy=table, row=summary['best']), indent=1))
