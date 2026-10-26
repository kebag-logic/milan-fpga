#!/usr/bin/env python3
"""When a group's SRP records are released (RX_TAIL writes) relative to its composed window, and the
length of every pass that releases one; also the group's longest pass that starts after the window.
Usage: srp_service.py CHECKOUT LOG..."""
import sys
sys.path.insert(0, sys.argv[1] + '/sw/mailbox')
from mailbox_model import load
c = load()
chreg = {r.name: r.offset for r in c.ch_registers}
names = [x.name for x in c.channels]
srp_tail = (c.ch_base + names.index('srp') * c.ch_stride + chreg['RX_TAIL']) // 4
for path in sys.argv[2:]:
    lines = open(path).read().splitlines()
    marks = {l.split()[2]: int(l.split()[1]) for l in lines if l.startswith('MARK')}
    t0, t1 = marks.get('composed'), marks.get('composed_end')
    srp_commits = [int(l.split()[1]) for l in lines if l.startswith('RXC') and l.split()[2] == str(names.index('srp'))]
    rel, after = [], []
    for l in lines:
        if not l.startswith('PASS'):
            continue
        f = l.split(); s = int(f[2]); cyc = int(f[4])
        n = sum(1 for x in (l.split(' W', 1)[1].split() if ' W' in l else []) if int(x.split(':')[1], 16) == srp_tail)
        if n:
            rel.append((s, cyc, n))
        if t1 is not None and s > t1:
            after.append((cyc, s))
    in_win = [x for x in srp_commits if t0 <= x <= t1] if t0 is not None else []
    print(f'== {path.split("/")[-1]}: window {t0}..{t1} ({(t1 - t0) / 1e5:.2f} ms); SRP commits in window {len(in_win)}')
    if in_win and rel:
        first = min(x for x in in_win)
        later = [r for r in rel if r[0] >= first]
        if later:
            print(f'  first SRP release after the load: {(later[0][0] - first) / 1e5:.2f} ms after the first SRP commit; '
                  f'last: {(later[-1][0] + 2 * later[-1][1] - first) / 1e5:.2f} ms; releasing passes {len(later)}, '
                  f'their longest {max(r[1] for r in later):,} CPU cycles ({max(r[1] for r in later) / 5e4:.2f} ms); '
                  f'releasing passes inside the window {sum(1 for r in later if r[0] <= t1)}')
        else:
            print('  no SRP release after the load in the log')
    if after:
        top = max(after)
        print(f'  longest pass starting after the window: {top[0]:,} CPU cycles ({top[0] / 5e4:.2f} ms) at +{(top[1] - t1) / 1e5:.2f} ms')
