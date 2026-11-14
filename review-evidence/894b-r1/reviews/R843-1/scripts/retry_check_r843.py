"""Independent check of THE RETRY's round costs at a shape, from CPU budget harness logs.

Each round is a `SPAN ... ctrl_loop:round_of` line (fields: sys start, CPU start, CPU cycles, address, name); its notices
n are the `CALL ... aecp:finish` lines whose CPU cycle lies inside it, and its refused attempts k the `aecp_command`
CALL lines inside it less n. For each stated (cold, attempt) pair given, every round is held to
(cold + n x notice + k x attempt) x 100 CPU cycles, and the rounds over it are counted. The dearest round at each k,
notices charged at the stated notice cost, is printed, and every line through two of those points is enumerated: the
lines that keep every round under them and pass through the dearest round of every port refused (k = ports) are
listed with their cold start, so the least is read off without any hull shortcut. The rule's statement of a measured
cost (plus 5 %, rounded up to 5 us) is then applied to that line.
usage: python3 -I retry_check_r843.py --ports P --notice-us W --stated C,A [--stated C,A ...] LOG...
"""
import argparse
import math
from collections import defaultdict

CPU_PER_US = 100


def rounds(path):
    spans, finish, command = [], [], []
    with open(path, errors='replace') as f:
        for line in f:
            if line.startswith('SPAN ') and line.rstrip().endswith(' ctrl_loop:round_of'):
                p = line.split()
                spans.append((int(p[2]), int(p[3])))
            elif line.startswith('CALL '):
                p = line.split()
                if p[3] == 'aecp:finish':
                    finish.append(int(p[2]))
                elif p[3] == 'aecp_command':
                    command.append(int(p[2]))
    finish.sort()
    command.sort()

    def count(xs, lo, hi):
        # entries with lo <= x < hi, by linear-time-safe bisection written out
        import bisect
        return bisect.bisect_left(xs, hi) - bisect.bisect_left(xs, lo)
    out = []
    for start, cycles in spans:
        n = count(finish, start, start + cycles)
        out.append((n, count(command, start, start + cycles) - n, cycles))
    return out


def rule(cycles):
    return 5 * math.ceil(round(cycles * 1.05 / CPU_PER_US, 9) / 5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ports', type=int, required=True)
    ap.add_argument('--notice-us', type=int, required=True)
    ap.add_argument('--stated', action='append', required=True)
    ap.add_argument('logs', nargs='+')
    a = ap.parse_args()
    w = a.notice_us * CPU_PER_US
    every = []
    for path in a.logs:
        every += [(n, k, c, path.rsplit('/', 1)[-1]) for n, k, c in rounds(path)]
    tally = defaultdict(int)
    dearest = {}
    for n, k, c, name in every:
        tally[(n, k)] += 1
        if c - n * w > dearest.get(k, (-1,))[0]:
            dearest[k] = (c - n * w, n, c, name)
    print(f'{len(every):,} rounds in {len(a.logs)} logs; notice {a.notice_us} us; ports {a.ports}')
    print('rounds by (notices, refused):', dict(sorted(tally.items())))
    for k in sorted(dearest):
        y, n, c, name = dearest[k]
        print(f'k={k}: dearest {y:,} cycles net of notices ({name}: {n} notice(s), {c:,} cycles)')
    for s in a.stated:
        cold, att = (int(x) for x in s.split(','))
        over = [(n, k, c, name) for n, k, c, name in every if c > (cold + n * a.notice_us + k * att) * CPU_PER_US]
        worst = max(every, key=lambda r: r[2] / ((cold + r[0] * a.notice_us + r[1] * att) * CPU_PER_US))
        lim = (cold + worst[0] * a.notice_us + worst[1] * att) * CPU_PER_US
        print(f'stated {cold} + {a.notice_us} n + {att} k us: {len(over):,} round(s) over; closest {worst[3]} '
              f'({worst[0]}, {worst[1]}) {worst[2]:,} of {lim:,} ({100 * worst[2] / lim:.1f} %)')
        byk = defaultdict(int)
        for n, k, c, name in over:
            byk[(n, k)] += 1
        if over:
            print('   over by (notices, refused):', dict(sorted(byk.items())))
    p = a.ports
    if p not in dearest:
        print(f'no round of every port refused (k = {p}) measured: no line is derived')
        return 0
    yp = dearest[p][0]
    cands = []
    for k in sorted(dearest):
        if k == p:
            continue
        slope = (yp - dearest[k][0]) / (p - k)
        cold = yp - p * slope
        holds = all(c <= cold + n * w + kk * slope + 1e-6 for n, kk, c, _ in every)
        cands.append((cold, slope, k, holds))
        print(f'line through k={k} and k={p}: cold {cold:,.1f} cycles, attempt {slope:,.1f} cycles; holds every '
              f'round: {holds}')
    ok = [c for c in cands if c[3] and c[1] >= 0]
    if ok:
        cold, slope, k, _ = min(ok)
        print(f'least cold start among holding lines: {cold / CPU_PER_US:.2f} us once, {slope / CPU_PER_US:.2f} us an '
              f'attempt (through k={k}); by the rule {rule(cold)} and {rule(slope)} us')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
