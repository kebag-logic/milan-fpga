"""OLS slope with a 95% interval, and its sensitivity to single cycles.

usage: slope_sensitivity.py <HANDOFF.md>
"""
import math, re, statistics, sys
t = open(sys.argv[1]).read()
for d in ('listener', 'talker'):
    v = [float(m[1]) for m in re.finditer(r'^\| ' + d + r' \| ' + d + r'-\d{3} \| [0-9.]+ \| \d+ \| \d+ \| ([0-9.]+) \|', t, re.M)]
    def fit(pts):
        x = [p[0] for p in pts]; y = [p[1] for p in pts]; n = len(x)
        mx, my = statistics.mean(x), statistics.mean(y); sxx = sum((a - mx) ** 2 for a in x)
        b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
        res = [c - (my + b * (a - mx)) for a, c in zip(x, y)]
        se = math.sqrt(sum(r * r for r in res) / (n - 2) / sxx)
        return b, se
    pts = list(enumerate(v, 1))
    b, se = fit(pts)
    loo = [fit([p for p in pts if p[0] != k])[0] for k in range(1, 101)]
    pos = [k for k, s in zip(range(1, 101), loo) if s > 0]
    print(f'{d}: slope {b:+.3e} s/cycle, 95% interval [{b - 1.984 * se:+.3e}, {b + 1.984 * se:+.3e}]; '
          f'leave-one-out range [{min(loo):+.3e}, {max(loo):+.3e}]; cycles whose removal makes it positive: {pos}')
    print(f'   upper 95% bound extrapolated over 100 cycles: {(b + 1.984 * se) * 100 * 1000:+.2f} ms')
