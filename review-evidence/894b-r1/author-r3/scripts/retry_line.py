"""THE RETRY's round costs at a shape from a measurement (#894's round 3 ruling, issuecomment-6878014227, item 1).

Every round the loop calls (ctrl_loop.c's round_of, a SPAN line) is held by round_grade.py to C + n x W + k x A: C its
cold start (AECP_ROUND_COLD_US), W a notice (AECP_NOTICE_US), A a refused attempt (AECP_ATTEMPT_US), n the notices it
built (aecp:finish CALL lines inside it) and k its refused attempts (aecp_command CALL lines less n). The measurement of
C and A is #665's definition of the attempt (aecp.h: what a round of AECP_ROUND_PORTS refusals costs past its first
attempt's cold misses, a refusal) and of the cold start (what any round implies once its notices and refusals are
charged): the line over the dearest round at each count of refused attempts, notices charged at the stated W, that
holds every round and a round of every port refused at its cost, and of those lines the one with the least cold start.
That is the upper hull's last edge, ending at the dearest round of every port refused. Each is then stated at the
measurement plus 5 %, rounded up to 5 us (100 CPU cycles a microsecond).

Also checks that a statement every other measured round was held to (OLD: C, A in us; such rounds' runs exited 0 with
no STATED line) lies under the measured line for every k up to the ports, so those rounds need no log here.

usage: python3 -I retry_line.py --ports P --notice-us W [--old C,A] LOG...
"""
import argparse
import math
import sys
from bisect import bisect_left
from collections import defaultdict

ROUND, ATTEMPT, BUILT = 'ctrl_loop:round_of', 'aecp_command', 'aecp:finish'
CPU_PER_US = 100


def rounds(path):
    """Each round of one log: (notices, refused, cycles)."""
    spans, calls = [], defaultdict(list)
    with open(path, errors='replace') as f:
        for line in f:
            if line.startswith('SPAN ') and line.rstrip().endswith(ROUND):
                p = line.split()
                spans.append((int(p[2]), int(p[3])))
            elif line.startswith('CALL '):
                p = line.split()
                if p[3] in (ATTEMPT, BUILT):
                    calls[p[3]].append(int(p[2]))
    for v in calls.values():
        v.sort()
    a, b = calls[ATTEMPT], calls[BUILT]
    out = []
    for start, cycles in spans:
        end = start + cycles
        n = bisect_left(b, end) - bisect_left(b, start)
        k = bisect_left(a, end) - bisect_left(a, start) - n
        out.append((n, k, cycles))
    return out


def stated(cycles):
    """A measured cost stated: plus 5 %, rounded up to 5 us."""
    return 5 * math.ceil(cycles * 1.05 / CPU_PER_US / 5 - 1e-9)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ports', type=int, required=True)
    ap.add_argument('--notice-us', type=int, required=True)
    ap.add_argument('--old', default=None)
    ap.add_argument('logs', nargs='+')
    args = ap.parse_args()
    w = args.notice_us * CPU_PER_US
    every, dearest, where = [], {}, {}
    for path in args.logs:
        name = path.rsplit('/', 1)[-1].removesuffix('.log')
        for n, k, cycles in rounds(path):
            every.append((n, k, cycles, name))
            y = cycles - n * w
            if y > dearest.get(k, -1):
                dearest[k], where[k] = y, f'{name}: {n} notice(s), {k} refused, {cycles:,} cycles'
    p = args.ports
    print(f'# {len(every):,} rounds in {len(args.logs)} logs; notices charged at {args.notice_us} us; ports {p}')
    print('| Refused attempts k | The dearest round, notices charged (cycles) | Round |')
    print('|---:|---:|---|')
    for k in sorted(dearest):
        print(f'| {k} | {dearest[k]:,} | {where[k]} |')
    if p not in dearest:
        print(f'REFUSED: no round of every port refused ({p}) measured')
        return 2
    if max(dearest) > p:
        print(f'REFUSED: a round of more refused attempts than ports ({max(dearest)} > {p})')
        return 2
    # the upper hull's last edge into (p, D_p): the steepest slope from an earlier point that keeps every point under
    others = [k for k in dearest if k < p]
    slope = min(((dearest[p] - dearest[k]) / (p - k) for k in others), default=0.0)
    slope = max(slope, 0.0)
    cold = dearest[p] - p * slope
    over = [r for r in every if r[2] > cold + r[0] * w + r[1] * slope + 1e-6]
    print(f'The line: cold start {cold:,.1f} cycles ({cold / CPU_PER_US:.2f} us), a refused attempt {slope:,.1f} '
          f'cycles ({slope / CPU_PER_US:.2f} us); rounds over it: {len(over)}')
    c_us, a_us = stated(cold), stated(slope)
    print(f'Stated at the measurement plus 5 %, rounded up to 5 us: AECP_ROUND_COLD_US {c_us} us, '
          f'AECP_ATTEMPT_US {a_us} us')
    limit = lambda n, k: (c_us + n * args.notice_us + k * a_us) * CPU_PER_US
    worst = max(every, key=lambda r: r[2] / limit(r[0], r[1]))
    print(f'At the statement every round within: {all(r[2] <= limit(r[0], r[1]) for r in every)}; the closest '
          f'{worst[3]} ({worst[0]} notice(s), {worst[1]} refused) {worst[2]:,} of {limit(worst[0], worst[1]):,} '
          f'cycles ({100 * worst[2] / limit(worst[0], worst[1]):.1f} %)')
    if args.old:
        oc, oa = (int(x) for x in args.old.split(','))
        under = all((oc + k * oa) * CPU_PER_US <= cold + k * slope + 1e-6 for k in range(p + 1))
        print(f'The statement {oc} + k x {oa} us (notices alike) under the measured line for every k up to {p}: '
              f'{under}')
    return 0 if not over else 1


if __name__ == '__main__':
    sys.exit(main())
