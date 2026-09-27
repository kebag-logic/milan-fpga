"""Recompute the page's distribution, growth and cross-table consistency.

usage: recompute_distribution.py <page.md> <HANDOFF.md>
Reads only the two text files; prints a receipt and exits non-zero on mismatch.
"""
import math, re, statistics, sys

page, handoff = (open(p).read() for p in sys.argv[1:3])
bad = []

def rows(text, first):
    out = []
    for line in text.splitlines():
        if line.startswith('| ' + first):
            out.append([c.strip() for c in line.strip('|').split('|')])
    return out

# page cycle table: | DUT listener | n | restart | PDUs | LA | TA | L | Ready | Result |
pc = {'listener': [], 'talker': []}
for r in rows(page, 'DUT '):
    if len(r) == 9 and r[1].isdigit():
        pc[r[0].split()[1]].append((int(r[1]), float(r[2]), r))
# handoff ledger: | listener | listener-001 | hold | resp | first | latency | overruns | cap | result |
hc = {'listener': [], 'talker': []}
for r in rows(handoff, 'listener |') + rows(handoff, 'talker |'):
    if len(r) == 9 and re.match(r'(listener|talker)-\d{3}$', r[1]):
        hc[r[0]].append((int(r[1][-3:]), float(r[2]), int(r[3]), int(r[4]), float(r[5]), r[8]))

def pct95(a):
    return sorted(a)[math.ceil(.95 * len(a)) - 1]

def slope(a):
    x = range(1, len(a) + 1); mx = statistics.mean(x); my = statistics.mean(a)
    return sum((i - mx) * (v - my) for i, v in zip(x, a)) / sum((i - mx) ** 2 for i in x)

for d in ('listener', 'talker'):
    p = sorted(pc[d]); h = sorted(hc[d])
    print(f'== {d}: page rows {len(p)}, handoff rows {len(h)}')
    if [n for n, *_ in p] != list(range(1, 101)) or [n for n, *_ in h] != list(range(1, 101)):
        bad.append(f'{d}: cycle numbering not 1..100')
    for (n, pv, _), (hn, hold, resp, first, lat, res) in zip(p, h):
        if abs((first - resp) / 1e9 - lat) > 1e-9:
            bad.append(f'{d} {n}: handoff first-resp {(first-resp)/1e9} != latency {lat}')
        if f'{lat:.6f}' != f'{pv:.6f}':
            bad.append(f'{d} {n}: page {pv} != handoff {lat}')
        if res != 'PASS' or lat >= 1:
            bad.append(f'{d} {n}: result {res} latency {lat}')
        if not (2.0 <= hold < 2.01):
            bad.append(f'{d} {n}: hold {hold}')
    v = [lat for *_, lat, _ in h]
    print(f'   min {min(v):.9f} median {statistics.median(v):.9f} p95(nearest rank) {pct95(v):.9f} max {max(v):.9f}')
    print(f'   below 1 s: {sum(x < 1 for x in v)}; holds {min(x[1] for x in h):.6f}..{max(x[1] for x in h):.6f}')
    print(f'   first-ten median {statistics.median(v[:10]):.6f} last-ten median {statistics.median(v[-10:]):.6f} OLS slope {slope(v):.6f} s/cycle')
    # alternative trend checks, independent of OLS
    half = statistics.median(v[:50]), statistics.median(v[50:])
    rho_num = None
    rk = {i: r for r, i in enumerate(sorted(range(100), key=lambda i: v[i]))}
    dsq = sum((i - rk[i]) ** 2 for i in range(100)); rho = 1 - 6 * dsq / (100 * (100 ** 2 - 1))
    print(f'   first-half median {half[0]:.6f} second-half median {half[1]:.6f} Spearman rho(cycle, latency) {rho:+.4f}')
    for s in range(0, 100, 10):
        b = v[s:s + 10]
        print(f'   block {s+1}-{s+10}: median {statistics.median(b):.6f} max {max(b):.6f}')
    # also extremes
    order = sorted(range(100), key=lambda i: v[i])
    print('   five smallest:', [(i + 1, round(v[i], 6)) for i in order[:5]])
    print('   five largest :', [(i + 1, round(v[i], 6)) for i in order[-5:]])
    # first-AVTP phase within a 2 ms CRF period, relative to response
    print(f'   latencies below one 2 ms CRF period: {[(i+1, round(v[i],6)) for i in range(100) if v[i] < 0.002]}')

print('MISMATCHES:', len(bad))
for b in bad: print('  ', b)
sys.exit(1 if bad else 0)
